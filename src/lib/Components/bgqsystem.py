"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- a group of processes started with mpirun
BGSystem -- Blue Gene system component
"""

import atexit
import pwd
import grp
import logging
import sys
import os
import re
import signal
import tempfile
import time
import thread
import threading
import xmlrpclib
import ConfigParser
import traceback
import pybgsched


import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Util import get_config_option, disk_writer_thread 
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics
from Cobalt.DataTypes.ProcessGroup import ProcessGroup

from pybgsched import SWIG_vector_to_list


from Cobalt.Components.BGQBooter import BGQBooter

from Cobalt.Components.bgq_base_system import node_position_exp, nodecard_exp, midplane_exp, rack_exp, wire_exp
from Cobalt.Components.bgq_base_system import NODECARD_A_DIM_MASK, NODECARD_B_DIM_MASK, NODECARD_C_DIM_MASK, NODECARD_D_DIM_MASK, NODECARD_E_DIM_MASK
from Cobalt.Components.bgq_base_system import A_DIM, B_DIM, C_DIM, D_DIM, E_DIM
from Cobalt.Components.bgq_base_system import get_extents_from_size
from Cobalt.Components.bgq_base_system import Wire
from Cobalt.Components.bgq_base_system import NodeCard, BlockDict, BGProcessGroupDict, BGBaseSystem, JobValidationError

try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree

__all__ = [
    "BGProcessGroup",
    "Simulator",
]

logger = logging.getLogger(__name__)
Cobalt.Util.init_cobalt_config()

#writer so that cobalt log writes don't hang up scheduling.
cobalt_log_writer = disk_writer_thread()
cobalt_log_writer.daemon = True
cobalt_log_writer.start()
logger.info("cobalt log writer thread enabled.")

def cobalt_log_write(filename, msg, user=None):
    '''send the cobalt_log writer thread a filename, msg tuple.

    '''
    if user == None:
        user = pwd.getpwuid(os.getuid())[0] #set as who I'm running as.
    cobalt_log_writer.send((filename, msg, user))

def cobalt_log_terminate():
    '''Terminate the writer thread by sending it None.

    '''
    cobalt_log_writer.send(None)

automatic_method_default_interval = get_config_option('system','automatic_method_default_interval',10.0)

sw_char_to_dim_dict = {'A': pybgsched.Dimension(pybgsched.Dimension.A),
                       'B': pybgsched.Dimension(pybgsched.Dimension.B),
                       'C': pybgsched.Dimension(pybgsched.Dimension.C),
                       'D': pybgsched.Dimension(pybgsched.Dimension.D),
                       'E': pybgsched.Dimension(pybgsched.Dimension.E),
                       }


class BGProcessGroup(ProcessGroup):
    """ProcessGroup modified by BlueGene/Q systems"""
    fields = ProcessGroup.fields + ["nodect", "subblock", "subblock_parent", "corner", "extents",
            'script_preboot']

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get('nodect', None)
        self.subblock = False
        self.subblock_parent = None
        self.corner = None
        self.extents = None
        self.script_preboot = spec.get('script_preboot', True)

    def __repr__(self):
        return "<BGProcessGroup id=%s, jobid=%s, location=%s>" % (self.id, self.jobid, self.location)

    def __str__(self):
            return self.__repr__()

# convenience function used several times below
def _get_state(bridge_partition):
    '''Convenience function to get at the block state.

    '''
    pass
    if bridge_partition.getStatus() == pybgsched.Block.Free:
        return "idle"
    else:
        return "busy"

def get_compute_block(block, extended_info=False):
    '''We do this a lot, this is just to make the information call more readable.

    block -- a string containing the block name
    extended_info -- Default: False.  If set to true, pulls extended info for the
        block like hardware information.

    '''
    block_location_filter = pybgsched.BlockFilter()
    block_location_filter.setName(block)
    if extended_info:
        block_location_filter.setExtendedInfo(True)
    return pybgsched.getBlocks(block_location_filter)[0]

class BGSystem (BGBaseSystem):

    """Blue Gene system component.

    Methods:
    configure -- load partitions from the bridge API
    add_process_groups -- add (start) an mpirun process on the system (exposed, ~query)
    get_process_groups -- retrieve mpirun processes (exposed, query)
    wait_process_groups -- get process groups that have exited, and remove them from the system (exposed, query)
    signal_process_groups -- send a signal to the head process of the specified process groups (exposed, query)
    update_block_state -- update partition state from the bridge API (runs as a thread)
    """

    name = "system"
    implementation = "bgqsystem"

    logger = logger


    def __init__ (self, *args, **kwargs):
        #former members of mfields: these must be in-place or startup will fail.
        #Do these first.  If we're choking, there is no reason to go on.
        self.kernel = 'default'

        BGBaseSystem.__init__(self, *args, **kwargs)
        sys.setrecursionlimit(5000)
        self.process_groups.item_cls = BGProcessGroup
        self.node_card_cache = dict()
        self.compute_hardware_vec = None
        try:
            sim_xml_file = get_config_option("gravina","simulator_xml")
        except ConfigParser.NoOptionError:
            sim_xml_file = None
        except ConfigParser.NoSectionError:
            sim_xml_file = None

        run_config = kwargs.pop('run_config',True)
        if run_config:
            logger.debug('init config()')
            self.configure(config_file=sim_xml_file)

        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        self.killing_jobs = {} 
        self.suspend_booting = False
        self.failed_io_block_names = set()
        self.booter = BGQBooter(self._blocks, self._blocks_lock)
        self.booter.start()

    def __getstate__(self):

        state = {}
        state.update(Component.__getstate__(self))
        flags = {}
        for part in self._blocks.values():
            sched = None
            func = None
            queue = None
            if hasattr(part, 'scheduled'):
                sched = part.scheduled
            if hasattr(part, 'functional'):
                func = part.functional
            if hasattr(part, 'queue'):
                queue = part.queue
            flags[part.name] =  (sched, func, queue)
        state.update({'managed_blocks':self._managed_blocks, 'version':1,
                'block_flags': flags, 'next_pg_id':self.process_groups.id_gen.idnum+1,
                'suspend_booting':self.suspend_booting})
        return state


    def __setstate__(self, state):

        Component.__setstate__(self, state) 
        sys.setrecursionlimit(5000)
        Cobalt.Util.fix_set(state)
        self._managed_blocks = state['managed_blocks']
        self._blocks = BlockDict()
        self.process_groups = BGProcessGroupDict()
        self.process_groups.item_cls = BGProcessGroup
        if state.has_key("next_pg_id"):
            self.process_groups.id_gen.set(state['next_pg_id'])
        self.node_card_cache = dict()
        self._blocks_lock = thread.allocate_lock()
        self.pending_script_waits = set()
        self.bridge_in_error = False
        self.cached_blocks = None
        self.offline_blocks = []
        self.compute_hardware_vec = None
        self.suspend_booting = False
        if state.has_key('suspend_booting'):
            self.suspend_booting = state['suspend_booting']

        try:
            sim_xml_file = get_config_option("gravina","simulator_xml")
        except ConfigParser.NoOptionError:
            sim_xml_file = None
        except ConfigParser.NoSectionError:
            sim_xml_file = None

        logger.debug('__setstate__ config()')
        self.configure(config_file=sim_xml_file)

        if 'block_flags' in state:
            for bname, flags in state['block_flags'].items():
                if bname in self._blocks:
                    self._blocks[bname].scheduled = flags[0]
                    self._blocks[bname].functional = flags[1]
                    self._blocks[bname].queue = flags[2]
                else:
                    self.logger.info("Block %s is no longer defined" % bname)

        self.update_relatives()
        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        self.lock = threading.Lock()
        self.statistics = Statistics()
        self.killing_jobs = {} #bg_jobid:forker_handle
        self.booting_blocks = {} #block location:pgroup

        self.pgroups_pending_boot = []
        self.pgroups_wait_reboot = []

        self.fail_io_block_names = set()
        self.booter = BGQBooter(self._blocks, self._blocks_lock)
        self.booter.start()

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def _get_node_card(self, name, state="idle"):
        if not self.node_card_cache.has_key(name):
            self.node_card_cache[name] = NodeCard(name, state)

        return self.node_card_cache[name]

    def _get_midplane_from_location(self, loc_name):
        '''get the midplane associated with a hardware location, like a switch, or a nodecard.
        The midplane data is pulled out of the compute hardware cache.

        '''
        rack_pos = int(rack_exp.search(loc_name).groups()[0], 16)
        midplane_pos = int(midplane_exp.search(loc_name).groups()[0])
        if self.compute_hardware_vec == None:
            raise RuntimeError("attempting to obtain nodecard state without initializing compute_hardware_vec.")
        mp = self.compute_hardware_vec.getMidplane("R%02X-M%d" % (rack_pos, midplane_pos))
        return mp

    def get_nodecard_isMetaState(self, loc_name):
        nodecard_pos = int(nodecard_exp.search(loc_name).groups()[0])
        mp = self._get_midplane_from_location(loc_name)
        return mp.getNodeBoard(nodecard_pos).isMetaState()

    def get_nodecard_state(self, loc_name):
        '''Get the node card state as described by the control system.'''
        nodecard_pos = int(nodecard_exp.search(loc_name).groups()[0])

        mp = self._get_midplane_from_location(loc_name)
        return mp.getNodeBoard(nodecard_pos).getState()

    def get_nodecard_state_str(self, loc_name):
        '''Get the node card state as described by the control system.'''
        nodecard_pos = int(nodecard_exp.search(loc_name).groups()[0])

        mp = self._get_midplane_from_location(loc_name)
        return mp.getNodeBoard(nodecard_pos).getStateString()


    def get_node_in_error(self, nodeboard_name):
        """Return aeuple of a node name and a state if we have a node in a non-available, non-softwarefailure
        state.  Return none, if all nodes are in SoftwareFailure and Available for both the state and the 
        node name

        """
        nodes = SWIG_vector_to_list(pybgsched.getNodes(nodeboard_name))
        node_name = None
        state_str = None
        for node in nodes:
            if node.getState() not in [pybgsched.Hardware.Available, pybgsched.Hardware.SoftwareFailure]:
                node_name = node.getLocation()
                state_str = node.getStateString()
                break

        return node_name, state_str

    def get_switch_state(self, sw_name):

        #first character in the switch name is the direction of the switch:
        # A,B,C, or D format: L_RXX-MY
        sw_id = sw_name.split("_")[0]
        mp = self._get_midplane_from_location(sw_name)
        return mp.getSwitch(sw_char_to_dim_dict[sw_id]).getState()

    def get_wire_state(self, wire):
        '''This is grabs the state of a cable from the outbound port (port1)
        The control system tracks this from the outbound port of a switch

        This corresponds to a Cable object in the control system.

        '''
        mp = self._get_midplane_from_location(wire.port1)
        return mp.getSwitch(pybgsched.Dimension(wire.dim)).getCable().getState()

    def _detect_wiring_deps(self, block):
        """
        wiring conflicts: Two blocks are in a wiring conflict iff
            - they have no nodeboards in common
            - they have wires in common on dimensions where their
                length > 1 in midplanes
            - if b1 conflict b2 then b2 conflict b1 (?)

        """
        def _can_dim_conflict(dim, dim_size):
            curr_dim_size = self.compute_hardware_vec.getMachineSize(pybgsched.Dimension(dim))
            return (not (dim_size == 1 or
                         dim_size == curr_dim_size or
                         dim_size == curr_dim_size - 1))

        def _gen_block_dims(bg_block):
            dim_dict = {}
            conflict = False
            if bg_block.isSmall():
                return dim_dict, conflict
            for dim in range(0, 4):
                dim_dict[dim] = bg_block.getDimensionSize(pybgsched.Dimension(dim))
                curr_dim_size = self.compute_hardware_vec.getMachineSize(pybgsched.Dimension(dim))
                if not (dim_dict[dim] == 1 or
                        dim_dict[dim] == curr_dim_size or
                        dim_dict[dim] == curr_dim_size - 1):
                    conflict = True
            return dim_dict, conflict

        if len(block.wires) == 0:
            return

        bg_block = get_compute_block(block.name, True)
        if bg_block.isSmall():
            #small blocks can't have wiring conflicts
            self.logger.debug("%s cannot have a conflict, skipping",
                            block.name)
            return
        bg_block_dims, can_conflict = _gen_block_dims(bg_block)
        if not can_conflict:

            self.logger.debug("%s cannot have a conflict, skipping %s",
                            block.name, bg_block_dims)
            return

        for other in self._blocks.values():
            if block.name == other.name:
                continue
            if len(block.wires) == 0:
                continue
            block_nodeset = set(block.node_card_names)
            other_nodeset = set(other.node_card_names)
            if block_nodeset.isdisjoint(other_nodeset):
                # we have no node-level hardware in common now check for
                # wiring conflicts
                bg_other = get_compute_block(other.name, True)
                #if bg_other.isSmall():
                #    continue
                bg_other_dims, can_conflict = _gen_block_dims(bg_other)
                if not can_conflict:
                    continue
                #Check wire pairs along dimension sizes that can conflict:
                for dim, block_dim_size in bg_block_dims.iteritems():
                    other_dim_size = bg_other_dims[dim]
                    if (_can_dim_conflict(dim, block_dim_size) and
                        _can_dim_conflict(dim, other_dim_size)):
                        block_wires_in_dim = set([wire for wire in block.wires
                                              if wire.dim == dim])
                        other_wires_in_dim = set([wire for wire in other.wires
                                              if wire.dim == dim])
                        if not block_wires_in_dim.isdisjoint(other_wires_in_dim):
                            block._wiring_conflicts.add(other.name)
                            other._wiring_conflicts.add(block.name)
                            self.logger.debug("%s and %s have a wiring conflict",
                            block.name, other.name)

        return

    def configure (self, bridgeless=True, config_file=None):

        if config_file == None and bridgeless:
            self._configure_from_bridge()  
            self.logger.info("Bridge Init Complete.")
        else:
            self._configure_from_file(bridgeless, config_file)
            self.logger.info("File Init Complete.")


    def _configure_from_bridge(self):

        """Read partition data from the bridge."""

        self.logger.info("configure()")
        start = time.time()
        #This initialization must occur successfully prior to anything else being done
        #with the scheduler API, or else you'll segfault out.  Absolute paths should be
        #used for init.  While init can take a relative path, the refreshConfig function will
        #error out.

        def __init_fail_exit():
            self.logger.critical("System Component Exiting!")
            sys.exit(1)

        try:
            pybgsched.init(get_config_option("bgsystem","bg_properties","/bgsys/local/etc/bg.properties"))
        except IOError:
            self.logger.critical("IOError initializing bridge.  Check bg.properties file and database connection.")
            __init_fail_exit()
        except RuntimeError:
            self.logger.critical("Abnormal RuntimeError from the bridge during initialization.")
            __init_fail_exit()
        try:
            #grab the hardware state:
            hw_start = time.time()
            self.compute_hardware_vec = pybgsched.getComputeHardware()
            hw_end = time.time()
            self.logger.debug("Acquiring hardware state: took %s sec", hw_end - hw_start)
        except RuntimeError:
            self.logger.critical ("Error communicating with the bridge while acquiring hardware information.")
            __init_fail_exit()
        try:
            #get all blocks on the system
            blk_start = time.time()
            ext_info_block_filter = pybgsched.BlockFilter()
            ext_info_block_filter.setExtendedInfo(True) #get the midplane data 
            system_def = pybgsched.getBlocks(ext_info_block_filter)
            blk_end = time.time()
            self.logger.debug("Acquiring block states: took %s sec", blk_end - blk_start)
        except RuntimeError:
            self.logger.critical ("Error communicating with the bridge during Block Initialization.")
            __init_fail_exit()

        #Extract and cache the midplane wiring data.  I am assuming that adding
        #more bluegene requires a restart
        midplane_wiring_cache_start = time.time()
        self._midplane_wiring_cache = {}
        midplane_locs = []
        machine_size = {}
        for dim in range(0,pybgsched.Dimension.D+1):
            machine_size[dim] = self.compute_hardware_vec.getMachineSize(
                    pybgsched.Dimension(dim))
        for A in range(0, machine_size[pybgsched.Dimension.A]):
            for B in range(0, machine_size[pybgsched.Dimension.B]):
                for C in range(0, machine_size[pybgsched.Dimension.C]):
                    for D in range(0, machine_size[pybgsched.Dimension.D]):
                        midplane_locs.append(self.compute_hardware_vec.getMidplane(
                            pybgsched.Coordinates(A,B,C,D)).getLocation())
        for mp in midplane_locs:
            self._midplane_wiring_cache[mp] = []
            for dim in range(0, pybgsched.Dimension.D+1):
                outbound_sw = self.compute_hardware_vec.getMidplane(mp).getSwitch(pybgsched.Dimension(dim))
                #small systems may not have cables for all switches (anything with a size 1mp dim)
                if outbound_sw.getCable() == None:
                    continue
                dimension, rack, midplane = self.__parse_wire(outbound_sw.getCable().getDestinationLocation())
                inbound_sw = self.compute_hardware_vec.getMidplane("R%02X-M%d"%(rack,midplane)).getSwitch(pybgsched.Dimension(dim))

                self._midplane_wiring_cache[mp].append(
                        Wire(outbound_sw.getCable().getLocation(),
                             outbound_sw.getCable().getDestinationLocation(),
                             dim))
                self._midplane_wiring_cache[mp].append(
                        Wire(inbound_sw.getCable().getLocation(),
                             inbound_sw.getCable().getDestinationLocation(),
                             dim))

        midplane_wiring_cache_end = time.time()
        self.logger.debug("Building midplane wiring cache: took %s sec", 
                midplane_wiring_cache_end - midplane_wiring_cache_start)
        # initialize a new partition dict with all partitions


        blocks = BlockDict()

        tmp_list = []

        for block_def in system_def:
            tmp_list.append(self._new_block_dict(block_def))

        blocks.q_add(tmp_list)

        # update object state
        self._blocks.clear()
        self._blocks.update(blocks)

        # find the wiring deps
        wd_start = time.time()
        for block in self._blocks.values():
            self._detect_wiring_deps(block)
        wd_end = time.time()
        self.logger.debug("Detecting Wiring Deps: took %s sec", wd_end - wd_start)

        # update state information
        for block in self._blocks.values():
            if block.state != "busy":
                for nc in block.node_cards:
                    if nc.used_by:
                        block.state = "blocked (%s)" % nc.used_by
                        break
                for dep_name in block._wiring_conflicts:
                    if self._blocks[dep_name].state == "busy":
                        block.state = "blocked-wiring (%s)" % dep_name
                        break

        end = time.time()
        self.logger.info("block configuration took %f sec" % (end - start))
        start = time.time()
        #set up subblocks, this is software only, and shared between modes (ultimately)
        subblock_config_string = get_config_option("bgsystem","subblock_config","Empty")
        subblock_spec_dict = self.parse_subblock_config(subblock_config_string)
        subblocks = []
        subblockDict = BlockDict()
        ignore_subblock_sizes_str = get_config_option("bgsystem","ignore_subblock_sizes","Empty")
        ignore_sizes = []
        if ignore_subblock_sizes_str != "Empty":
            ignore_sizes.extend([int(ignore_size) for ignore_size in list(ignore_subblock_sizes_str.split(','))])

        for block_id, minimum_size in subblock_spec_dict.iteritems():
            subblocks.extend(self.gen_subblocks(block_id, minimum_size, ignore_sizes))
        subblockDict.q_add(subblocks)
        self._blocks.update(subblockDict)
        end = time.time()
        self.logger.info("subblock configuration took %f sec" % (end - start))

        return

    ## BGSystem.parse_subblock_config
    #  Inputs: string of subblock configuration information
    #  Output: dictionary: key: block names, values: minimum size to slice to
    #  
    #  Read from the config file a list of blocks and the smallest size to divide them to.
    #  The expected string in the config file looks like Loc:XX,Loc2:YY,Loc3:ZZ
    def parse_subblock_config(self, subblock_config_string):
        #subblock_config_string = get_config_option("bgsystem","subblock_config","Empty")
        #self.logger.debug(subblock_config_string)
        if subblock_config_string in ["Empty", '', None]:
            return {}
        retdict = {}
        for subblock_config in subblock_config_string.split(","):
            split_config = subblock_config.split(":")
            retdict[split_config[0]] = int(split_config[1])

        #self.logger.debug('Setting new dict to: %s' % retdict)
        return retdict

    def __parse_wire(self, wire):
        wire_dict = wire_exp.search(wire).groupdict()
        return wire_dict['dim'], int(wire_dict['rack'], 16), int(wire_dict['midplane'])

    def gen_subblocks(self, parent_name, min_size, ignore_sizes=[]):

        '''Generate subblock names based on a parent and the minimum size.  
        For now, this is restricted to size 128 partitions.

        keyword arguments:
        parent_name -- name of the block that we are using as the parent of 
                       subblocks we're generating.
        min_size    -- the smallest size block to generate

        '''
        try:
            parent_block = self._blocks[parent_name]
        except KeyError:
            self.logger.warning("Nonexistent block specified as parent. "\
                    "Generating zero blocks for name: %s", parent_name)
            return []
        self.logger.info("Generating subblocks for block %s, down to size %d", 
                parent_block, min_size)
        curr_size = parent_block.size #most likely to be 128
        #TODO: Make this work for <=512 for block size
        if curr_size != 128:
            self.logger.info("subrun pseudoblocks only supported for size 128 nodes")
            return []

        bg_block_filter = pybgsched.BlockFilter()
        bg_block_filter.setName(parent_name)
        bg_block_filter.setExtendedInfo(True)
        bg_parent_block = pybgsched.getBlocks(bg_block_filter)[0]

        bgpb_nodeboards = SWIG_vector_to_list(bg_parent_block.getNodeBoards())

        #FIXME: make MAX_NODEBOARD or the like.
        nodecard_pos = 15
        for nb in bgpb_nodeboards:
          nb_pos = int(nodecard_exp.search(nb).groups()[0])
          nodecard_pos = min(nodecard_pos, nb_pos)

        midplane_hw_loc = SWIG_vector_to_list(bg_parent_block.getMidplanes())[0]

        midplane_pos = int(midplane_exp.search(midplane_hw_loc).groups()[0])
        rack_pos = int(rack_exp.search(midplane_hw_loc).groups()[0])
        #get parent midplane information.  we only need this once:
        midplane = self.compute_hardware_vec.getMidplane(midplane_hw_loc)
        midplane_logical_coords = pybgsched.getMidplaneCoordinates(midplane_hw_loc)

        subblock_prefix = get_config_option("bgsystem", "subblock_prefix", "COBALT")

        ret_blocks = []
        while (curr_size >= min_size):
            if curr_size in ignore_sizes:
                curr_size = curr_size / 2
                continue

            if curr_size >= 128:
                curr_size = 64
                continue
            if curr_size == 64:
                extents = get_extents_from_size(curr_size)

                for i in range(0,2):
                    curr_nb_pos = nodecard_pos + (2*i)
                    a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2
                    b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2
                    c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2
                    d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2
                    e_corner = 0

                    curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                            a_corner, b_corner, c_corner, d_corner, e_corner,
                            a_corner + extents[A_DIM] - 1,
                            b_corner + extents[B_DIM] - 1,
                            c_corner + extents[C_DIM] - 1,
                            d_corner + extents[D_DIM] - 1,
                            e_corner + extents[E_DIM] - 1,
                            curr_size)

                    nodecard_list = []
                    block_nodecards = ["R%02X-M%d-N%02d" % (rack_pos, midplane_pos, nodecard_pos+(2*i)),
                                       "R%02X-M%d-N%02d" % (rack_pos, midplane_pos, nodecard_pos+(2*i)+1)]
                    for j in range(0,2):
                        nc = midplane.getNodeBoard(nodecard_pos+(2*i)+j)
                        if nc.getLocation() in block_nodecards:
                            state = "idle"
                            if pybgsched.hardware_in_error_state(nc):
                                state = "error"
                            nodecard_list.append(self._get_node_card(nc.getLocation(), state))

                    corner_node = self._get_compute_node_from_global_coords([a_corner, b_corner, c_corner, d_corner, e_corner])
                    self.logger.debug("Creating subblock name: %s, corner: %s, extents %s.", curr_name, corner_node, extents)

                    ret_blocks.append((dict(
                        name = curr_name, 
                        queue = "default",
                        size = curr_size,
                        node_cards = nodecard_list,
                        subblock_parent = parent_name,
                        corner_node = corner_node,
                        extents = extents,
                        state = 'idle',
                        block_type = 'pseudoblock'
                        )))

            elif curr_size == 32:

                extents = get_extents_from_size(curr_size)
                for i in range(0,4):
                    curr_nb_pos = nodecard_pos + i
                    a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2
                    b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2
                    c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2
                    d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2
                    e_corner = 0

                    curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                            a_corner, b_corner, c_corner, d_corner, e_corner,
                            a_corner + extents[A_DIM] - 1,
                            b_corner + extents[B_DIM] - 1,
                            c_corner + extents[C_DIM] - 1,
                            d_corner + extents[D_DIM] - 1,
                            e_corner + extents[E_DIM] - 1,
                            curr_size)

                    nodecard_list = [] 
                    block_nodecards = ["R%02d-M%d-N%02d" % (rack_pos, midplane_pos, curr_nb_pos)]

                    nc = midplane.getNodeBoard(curr_nb_pos)
                    if nc.getLocation() in block_nodecards:
                        state = "idle"
                        if pybgsched.hardware_in_error_state(nc):
                            state = "error"
                        nodecard_list.append(self._get_node_card(nc.getLocation(), state))

                    corner_node = self._get_compute_node_from_global_coords([a_corner, b_corner, c_corner, d_corner, e_corner])
                    self.logger.debug("Creating subblock name: %s, corner: %s, extents %s, nodecards: %s", curr_name, corner_node, extents, nodecard_list)

                    ret_blocks.append((dict(
                        name = curr_name, 
                        queue = "default",
                        size = curr_size,
                        node_cards = nodecard_list,
                        subblock_parent = parent_name,
                        corner_node = corner_node,
                        extents = extents,
                        state = 'idle',
                        block_type = 'pseudoblock'
                        )))

            else:
                extents = get_extents_from_size(curr_size)

                #yes, do these for each nodecard.
                for curr_nb_pos in range(nodecard_pos, nodecard_pos + 4):
                    for i in range(0, (32/curr_size)):

                        #Yes these bitmasks are important.
                        a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 1)))
                        b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 2)))
                        c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 4)))
                        d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 8)))
                        e_corner = int(bool(i & 16))

                        curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                                a_corner, b_corner, c_corner, d_corner, e_corner,
                                a_corner + extents[A_DIM] - 1,
                                b_corner + extents[B_DIM] - 1,
                                c_corner + extents[C_DIM] - 1,
                                d_corner + extents[D_DIM] - 1,
                                e_corner + extents[E_DIM] - 1,
                                curr_size)

                        nodecard_list = [] 

                        block_nodecards = ["R%02X-M%d-N%02d" % (rack_pos, midplane_pos, curr_nb_pos)]
                        nc = midplane.getNodeBoard(curr_nb_pos)
                        if nc.getLocation() in block_nodecards:
                            state = "idle"
                            if pybgsched.hardware_in_error_state(nc):
                                state = "error"
                            nodecard_list.append(self._get_node_card(nc.getLocation(), state))

                        corner_node = self._get_compute_node_from_global_coords([a_corner, b_corner, c_corner, d_corner, e_corner])
                        self.logger.debug("Creating subblock name: %s, corner: %s, extents %s, nodecards: %s", curr_name, corner_node, extents, nodecard_list)

                        ret_blocks.append((dict(
                            name = curr_name, 
                            queue = "default",
                            size = curr_size,
                            node_cards = nodecard_list,
                            subblock_parent = parent_name,
                            corner_node = corner_node,
                            extents = extents,
                            state = 'idle',
                            block_type = 'pseudoblock'
                            )))
                    # for i
                # for curr_nb_pos

            curr_size = curr_size / 2
        return ret_blocks

    def _get_compute_node_from_global_coords(self, global_coords):
        '''Takes a global machine coord and generates the compute node at that location

        '''
        #Once again proving that Integer division is the right default.
        midplane_coords = [c/4 for c in global_coords]
        midplane_torus_coords = [c%4 for c in global_coords]
        nodeboard_loc = [c/2 for c in midplane_torus_coords] #if a 2 or a 3 reversed dim
        node_coords = [c%2 for c in midplane_torus_coords] #location on a nodeboard itself

        nodeboard_pos = nodeboard_loc[A_DIM] * 4 + \
                        nodeboard_loc[B_DIM] * 8 + \
                        nodeboard_loc[C_DIM] * 1 + \
                        nodeboard_loc[D_DIM] * 2
        node_pos = Cobalt.Components.bgq_base_system.get_transformed_loc(nodeboard_pos, node_coords)

        #TODO: make less machine specific, more configurable.  For T&D and Mira this should work, though.

        rack_pos = 0

        rack_pos = rack_pos + midplane_coords[A_DIM]*8
        rack_pos = rack_pos + midplane_coords[A_DIM]*16
        #TODO: have to handle C dimension.  Will fix for mira, Vesta, Cetus not needed.
        rack_pos = rack_pos + (midplane_coords[D_DIM]/2) #will add 1 if the D-dim is 2 or 3.

        midplane_pos = 0
        if midplane_coords[D_DIM] in [1,2]:
            midplane_pos = 1
        return "R%02X-M%d-N%02d-J%02d" % (rack_pos, midplane_pos, nodeboard_pos, node_pos)

    def _new_block_dict(self, block_def):
        #pull block info into a dict so that we can create internal blocks to track.

        #block_def must be a block from pybgsched

        switch_list = []
        midplane_list = []
        nodecard_list = []
        pt_nodecard_list = []
        io_link_list = []
        wire_set = set()
        midplane_ids = block_def.getMidplanes()
        passthrough_ids = block_def.getPassthroughMidplanes()
        midplane_nodecards = []
        midplane_pt_nodecards = []
        midplane_geometry = []
        node_geometry = []

        if block_def.isLarge():
            for i in range(0, D_DIM+1):
                midplane_geometry.append(block_def.getDimensionSize(pybgsched.Dimension(i)))
                node_geometry.append(block_def.getDimensionSize(pybgsched.Dimension(i)) * 4)
        else:
            midplane_geometry = [0,0,0,0]
            node_geometry = Cobalt.Components.bgq_base_system.get_extents_from_size(block_def.getComputeNodeCount())

        for midplane_id in midplane_ids:
            #grab the switch data from all associated midplanes
            midplane = self.compute_hardware_vec.getMidplane(midplane_id)
            midplane_list.append(midplane.getLocation())
            for i in range(0, D_DIM+1):
                switch_list.append(midplane.getSwitch(pybgsched.Dimension(i)).getLocation())
                midplane_nodecards.extend([nb.getLocation() 
                    for nb in SWIG_vector_to_list(pybgsched.getNodeBoards(midplane.getLocation()))])
            #for small partitions may have a subset of nodecards, fortunately the block knows this.i
            #try: #This calls out, not using cached ComputeHardware data.  Not sure if this is desirable.
            #    possible_nodecards = pybgsched.getNodeBoards(midplane_id)
            #except RuntimeError:
            #    self.logger.critical ("Error communicating with the bridge during NodeBoard acquisition")
            #    init_fail_exit()

            block_nodecards = SWIG_vector_to_list(block_def.getNodeBoards())
            if block_nodecards == []:
                block_nodecards = midplane_nodecards
            for i in range(0, midplane.MaxNodeBoards):
                nc = midplane.getNodeBoard(i)
                if nc.getLocation() in block_nodecards:
                    state = "idle"
                    if pybgsched.hardware_in_error_state(nc):
                        state = "error"
                    nodecard_list.append(self._get_node_card(nc.getLocation(), state))

        # Add in passthrough switches
        for midplane_id in passthrough_ids:
            midplane = self.compute_hardware_vec.getMidplane(midplane_id)
            for i in range(0,D_DIM+1):
                switch_list.append(midplane.getSwitch(pybgsched.Dimension(i)).getLocation())

        # Wiring
        mp_and_passthru_mp_list = set(midplane_ids)
        passthrough_mp_list = set(SWIG_vector_to_list(block_def.getPassthroughMidplanes()))
        mp_and_passthru_mp_list |= passthrough_mp_list
        #add wires for a dimension, make sure to get passthru midplanes as well.
        #no passthrough for sub-midplane blocks
        #for mp in mp_and_passthru_mp_list:
            #for wire in self._midplane_wiring_cache[mp]:
                #if (wire.port1_mp in mp_and_passthru_mp_list and
                        #wire.port2_mp in mp_and_passthru_mp_list):
                    #wire_set.add(wire)

        # Get wiring for included midplanes:
        # Include wires whose ends are both in this list or have 
        # one end in passthrough.
        for mp in midplane_list:
            for wire in self._midplane_wiring_cache[mp]:
                if (wire.port1_mp in midplane_list and
                        wire.port2_mp in midplane_list):
                    wire_set.add(wire)
                elif (wire.port1_mp in passthrough_mp_list or
                        wire.port2_mp in passthrough_mp_list):
                    wire_set.add(wire)

        if len(passthrough_mp_list):
            # Get passthrough wiring
            pt_wire_set = set()
            for wire in wire_set:
                pt_mp = None
                if wire in pt_wire_set: #don't bother if we already got this wire
                    continue
                if wire.port1_mp in passthrough_mp_list:
                    pt_mp = wire.port1_mp
                while pt_mp != None:
                    dim = wire.dim
                    pt_mp_wires = self._midplane_wiring_cache[pt_mp]
                    pt_mp == None
                    for pt_wire in pt_mp_wires:
                        found_next_pt_mp = False
                        if pt_wire.dim == dim:
                            pt_wire_set.add(pt_wire)
                        if pt_wire.port1_mp == pt_mp and pt_wire.port2_mp in midplane_list:
                            pt_mp = pt_wire.port2_mp
                            found_next_pt_mp = True
                    if not found_next_pt_mp:
                        pt_mp = None

            wire_set |= pt_wire_set


        #add to passthrough nodecards
        for mp in passthrough_mp_list:
            midplane_pt_nodecards = [nb.getLocation()
                for nb in SWIG_vector_to_list(pybgsched.getNodeBoards(mp))]
            for i in range(0, midplane.MaxNodeBoards):
                nc = self.compute_hardware_vec.getMidplane(mp).getNodeBoard(i)
                if nc.getLocation() in midplane_pt_nodecards:
                    state = "idle"
                    if pybgsched.hardware_in_error_state(nc) and not nc.isMetaState():
                        state = "error"
                    pt_nodecard_list.append(self._get_node_card(nc.getLocation(), state))


        d = dict(
            name = block_def.getName(),
            queue = "default",
            size = block_def.getComputeNodeCount(),
            midplane_geometry = midplane_geometry,
            node_geometry = node_geometry,
            midplanes = midplane_list,
            node_cards = nodecard_list,
            passthrough_node_cards = pt_nodecard_list,
            switches = switch_list,
            state = block_def.getStatus(),
            block_type = 'normal',
            wires = wire_set
        )
        return d


    def _configure_from_file (self, bridgeless=True, config_file=None):

        """Read partition data from the bridge, ultimately.  Until then we're working from an XML file.

        """

        if config_file == None and bridgeless:
            raise RuntimeError("config file for bridgeless operation not specified.")

        def _get_node(name):
            if not self.node_cache.has_key(name):
                self.node_cache[name] = NodeCard(name)

            return self.node_cache[name]

        self.logger.info("configure()")
        try:
            system_doc = ElementTree.parse(config_file)
        except IOError:
            self.logger.error("unable to open file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)
        except:
            traceback.print_exc()
            self.logger.error("problem loading data from file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)

        system_def = system_doc.getroot()
        if system_def.tag != "BG":
            self.logger.error("unexpected root element in %r: %r" % (config_file, system_def.tag))
            self.logger.error("exiting...")
            sys.exit(1)


        # initialize a new partition dict with all partitions
        #
        blocks = BlockDict()

        tmp_list = []


        for block_def in system_def.getiterator("Block"):
            node_list = [] #this is now really Nodes
            node_card_list = [] #node_cards are no longer aliased as nodes.
            #ion_list = []
            #ion_blocks = []
            switch_list = []

            for nc in block_def.getiterator("NodeCard"):
                node_card_list.append(self._get_node_card(nc.get("id")))
            nc_count = len(node_card_list)
            if nc_count <= 0:
                raise RuntimeError("BOOM: Block %s defined without nodecards!", block_def.get('name'))

            tmp_list.append( dict(
                name = block_def.get("name"),
                queue = block_def.get("queue", "default"),
                size = block_def.get("size", None),
                node_cards = node_card_list,
                #switches = switch_list,
                state = "idle",
            ))
        blocks.q_add(tmp_list)


        # update object state
        self._blocks.clear()
        self._blocks.update(blocks)
        return

    def _recompute_block_state(self):
        '''Recompute the hardware and cleaning/allocated blockage for all
        managed blocks.

        '''

        self.offline_blocks = []
        for b in self._blocks.values():

            if b.name not in self._managed_blocks:
                continue

            if b.state == 'busy':
                if not b.reserved_by:
                    b.reserved_until = False

            if b.state != 'idle':
                continue

            if b.cleanup_pending:
                b.state = 'cleanup'
                continue
            #failed diags/marked failed not in here

            self.check_block_hardware(b)
            if b.state != 'idle':
                continue

            if b.used_by:
                b.state = "allocated"
                if b.block_type != "pseudoblock":
                    continue

            #pseudoblock handling, busy isn't handled by the control system.
            if b.block_type == "pseudoblock":

                if b.used_by:
                    #mark busy if there is a related job
                    block_jobs = self._get_jobs_on_block(b.subblock_parent)
                    for job in block_jobs:
                        if (job.getCorner() in [node.name for node in b.nodes] and
                                job.getComputeNodesUsed() == b.size):
                            #If I have a backend job on my nodes, then I'm busy.
                            b.state = "busy"
                            break

                if b.state != 'idle':
                    continue

                is_blocked = self.check_subblock_blocked(b)
                if is_blocked:
                    continue

                # check the subblock parent to see if block is bootable,
                # if the parent can't be booted, the pseudoblock is not
                # going to be able to run anything

                subblock_parent_block = self._blocks[b.subblock_parent]
                for nc in subblock_parent_block.node_cards:
                    if nc.used_by:
                        if (b.subblock_parent != nc.used_by or
                                b.subblock_parent == b.name):
                            b.state = "blocked (%s)" % nc.used_by
                            break
                if b.state != 'idle':
                    continue

                self.check_block_hardware(subblock_parent_block, subblock_parent=True)
                if subblock_parent_block.state != 'idle':
                    b.state = subblock_parent_block.state
                    continue

            #mark blocked in parent/child partition is allocated/cleaning
            allocated = None
            cleaning = None
            for rel_block in b._relatives:
                if rel_block.used_by or rel_block.state == 'busy':
                    if rel_block.block_type != 'pseudoblock':
                        allocated = rel_block
                        break
                    else:
                        # if it is the subblock parent we're not really busy
                        if rel_block.name != b.subblock_parent:
                            allocated = rel_block
                            break
                if rel_block.cleanup_pending:
                    cleaning = rel_block
                    break
            if cleaning:
                b.state = 'blocked (%s)' % (cleaning.name,)
            elif allocated:
                b.state = "blocked (%s)" % (allocated.name,)

    def check_block_hardware(self, block, subblock_parent=False):
        '''Check the cached hardware state and see if the block would
        be blocked by failed hardware.

        subblock_parent notes that this is a check for a pseudoblock's parent,
        and, therefore, should ignore the blocked-busy detection, that must be
        handled by the pseudoblock itself.

        '''

        def offline_if_not_available(block, nc):
            '''Mark a block offline with an appropriate error indicator
            if any of the block's nodecards are in a state other than A in
            the control system. True if the block should be offlined.

            '''
            if self.get_nodecard_state(nc.name) != pybgsched.Hardware.Available:
                #if control system reports down, then we're really down.
                block.state = "hardware offline (%s): nodeboard %s" % (self.get_nodecard_state_str(nc.name), nc.name)
                self.offline_blocks.append(block.name)
                if (self.get_nodecard_state(nc.name) == pybgsched.Hardware.Error and
                        self.get_nodecard_isMetaState(nc.name)):
                    #We have a nonzero number of nodes in error, the nodecard is actually fine
                    #take the first node that is in a non-software failure, non-available state
                    error_node_name, state_str = self.get_node_in_error(nc.name)
                    if error_node_name:
                        block.state = "hardware offline (%s): node %s" % (state_str, error_node_name)
                    else:
                        block.state = "hardware offline (%s): nodeboard %s" % ("SoftwareFailure", nc.name)
                return True
            return False

        #Nodeboards in error
        freeing_error_blocks = []
        for nc in block.node_cards:
            if subblock_parent and nc.used_by:
                #block if other stuff is running on our node cards.
                #remember subblock jobs can violate this
                block.state = "blocked (%s)" % nc.used_by

            offlined = offline_if_not_available(block, nc)
            if offlined:
               return

        #Subblock parent with a nodeboard in error should cause all subblocks to become unavailable.
        if block.block_type == 'pseudoblock':
            subblock_parent_block = self._blocks[block.subblock_parent]
            for nc in subblock_parent_block.node_cards:
                offlined = offline_if_not_available(block, nc)
                if offlined:
                    return

        #IOlink status

        if block.name in self.failed_io_block_names:
            block.state = "Insufficient IO Links"
            return

        if block.midplanes.intersection(self.failed_io_midplane_cache):
            block.state = "Insufficient IO Links"
            return

        link_offline = False
        for mp in block.midplanes:
            dead_ion_links = 0
            for link in self.io_link_to_mp_dict[mp]:
                if link.getState() != pybgsched.IOLink.Available:
                    block.state = "hardware offline (%s) IOLink %s" %(link.getStateString(), link.getDestinationLocation())
                    link_offline = True
                    return
                if link.getIONodeState() != pybgsched.Hardware.Available:
                    dead_ion_links += 1
                    if dead_ion_links > 4: #FIXME: make this configurable
                        block.state = "hardware offline (%s) IO Node %s" % (link.getIONodeStateString(),link.getDestinationLocation())
                        link_offline = True
                        return

        #Block for passthrough
        for nc in block.passthrough_node_cards:
            if (self.get_nodecard_state(nc.name) != pybgsched.Hardware.Available and
                    (not self.get_nodecard_isMetaState(nc.name))):
                #the nodeboard itself is in error, nothing getting through.
                block.state = "hardware offline: passthrough nodeboard %s" % nc.name
                self.offline_blocks.append(block.name)
                return

        #Block for dead switch
        for sw in block.switches:
            if self.get_switch_state(sw) != pybgsched.Hardware.Available:
                block.state = "hardware offline: switch %s" % sw 
                self.offline_blocks.append(block.name)
                return

        #Block for dead cables
        for wire in block.wires:
            if self.get_wire_state(wire) != pybgsched.Hardware.Available:
                block.state = "hardware offline: wire %s" % wire
                self.offline_blocks.append(block.name)
                return

        #wiring conflicts are caught by parent/child
        for dep_name in block._wiring_conflicts:
            try:
                dep_block = self._blocks[dep_name]
            except KeyError:
                self.logger.warning("block %s: wiring conflict %s does not exist in partition table",
                    block.name, dep_name)
            if (dep_block.used_by or
                    dep_block.cleanup_pending or
                    dep_block.state == 'busy'):
                block.state = "blocked-wiring (%s)" % dep_name
                return
        return


    def _get_jobs_on_block(self, block_name):
        try:
            job_block_filter = pybgsched.JobFilter()
            job_block_filter.setComputeBlockName(block_name)
            jobs = SWIG_vector_to_list(pybgsched.getJobs(job_block_filter))
        except:
            self.logger.critical("Unable to obtain list of jobs for block %s from bridge!", block_name)
            raise
        return jobs

    def update_block_state(self):
        """This is the main "state" update loop.  Error states, busy detection
        and cleanup all happen here.  This is to be broken up, similar to what has 
        been done for the BG/P side.

        """
        def _start_block_cleanup(block):
            self.logger.info("Block %s: starting cleanup.", block.name)
            block.cleanup_pending = True
            block.reserved_until = False
            block.reserved_by = None
            block.used_by = None
            _set_block_cleanup_state(block)

        def _initiate_block_free(block):

            try:
                self.logger.debug("CLEANUP: Block %s reporting state as %s", block.name, block.state)
                if block.state not in ["idle", "cleanup-initiate", "cleanup"]:

                    compute_block = get_compute_block(block.name)
                    if compute_block.getStatus() == pybgsched.Block.Initialized:
                        pybgsched.Block.initiateFree(block.name)
                        block.freeing = True
                elif block.state == "idle":
                    self.logger.info("block %s: no block cleanup was required", block.name)
                    return
            except RuntimeError:
                #we are already freeing, ignore and go on
                self.logger.info("Free for block %s already in progress", block.name)
            except:
                #ummm, I think the control system went away!
                self.logger.critical("Unable to initiate block free from bridge!")
                raise
            return

        def _children_still_allocated(block):
            for child_block in block._children:
                if child_block.used_by:
                        return True
            return False

        def _set_block_cleanup_state(b):

            #set the block to the free state and kill everything on it.
            #only if we aren't a subblock job!
            if b.block_type != 'pseudoblock':
                #not a subblock, proceed to clean up normally.
                self.logger.info("Continuing control-system block cleanup for block %s", b.name)
                _initiate_block_free(b)
                b.state = 'cleanup-initiate'
                #also initiate for every busy child block
                for child in b._children:
                    _initiate_block_free(child)
            else:
                #ensure nothing else is running on the subblock parent.  If we're the last one out, 
                #then free the subblock.
                self.logger.info("initiaitng normal block cleanup for subblockblock %s, parent: %s", b.name, b.subblock_parent)
                pb = self._blocks[b.subblock_parent]
                still_reserved_children = _children_still_allocated(pb)
                block_jobs = self._get_jobs_on_block(b.subblock_parent)

                if not still_reserved_children:
                    self.logger.info("All subblock jobs done, freeing block %s", pb.name)
                    if pb.state not in ["cleanup", "cleanup-initiate"]:
                        _start_block_cleanup(pb)
                        self.logger.info("block %s: block marked for cleanup", pb.name)
                    pb.freeing = True
                else:
                    local_job_found = False
                    for job in block_jobs:
                        #Find a job that is supposed to be running on this 
                        #subblock and kill it.
                        if (job.getCorner() == b.corner_node and 
                            job.getShape() == "x".join(b.extents) and 
                            (job.getID() not in self.killing_jobs.keys())):
                            local_job_found =  True
                            nuke_job(job.getID(), b.subblock_parent)
                    if local_job_found:
                        b.state = "cleanup"


            #NOTE: at this point new jobs cannot start on this block if we're not a pseudoblock

            #don't track jobs whose kills have already completed.
            check_killing_jobs()
            #from here on, we should be able to see if the block has returned to the free state, if, so
            #and nothing else is blocking, we can safely set to idle.

            if b.block_type == 'pseudoblock':
                if len(self.killing_jobs) > 0:
                    b.state = 'cleanup'
                return

            #Non-pseudoblock jobs only from here on.
            #Children may have jobs as well due to ensemble jobs
            block_jobs = self._get_jobs_on_block(b.subblock_parent)
            for child_block in b._children:
                block_jobs.extend(self._get_jobs_on_block(child_block.name))

            if len(block_jobs) != 0:
                for job in block_jobs:
                    if job.getId() in self.killing_jobs.keys():
                        pass
                    nuke_job(job, b.name)
            b.state = 'cleanup'

            #don't track jobs whose kills have already completed.
            check_killing_jobs() #reap any ongoing kills


        def nuke_job(bg_job, block_name):
            #As soon as I get an API this is going to change.  Assume all on SN.
            #for now make a call to kill_job Job should die after 60 sec, if not earlier.

            try:
                retval = ComponentProxy('system_script_forker').fork(
                        ['/bgsys/drivers/ppcfloor/hlcs/bin/kill_job',
                            '%d'%bg_job.getId() ],
                        'bg_system_cleanup',
                        '%s cleanup:'% bg_job.getId())
                self.logger.info("killing backend job: %s for block %s",
                        bg_job.getId(), block_name)
            except xmlrpclib.Fault:
                self.logger.warning("XMLRPC Error while killing backend job: %s for block %s, will retry.", bg_job.getId(), block_name)
            except:
                self.logger.critical("Unknown Error while killing backend job: %s for block %s, will retry.", bg_job.getId(), block_name)
            else:
                self.killing_jobs[bg_job.getId()] = retval

            return

        def check_killing_jobs():

            try:
                system_script_forker = ComponentProxy('system_script_forker')
            except:
                self.logger.critical("Cannot connect to system_script forker.")
                return
            complete_jobs = []
            rev_killing_jobs = dict([(v,k) for (k,v) in self.killing_jobs.iteritems()])
            removed_jobs = []
            current_killing_jobs = system_script_forker.get_children(None, self.killing_jobs.values())

            for job in current_killing_jobs:
                if job['complete']:
                    del self.killing_jobs[rev_killing_jobs[int(job['id'])]]
                    removed_jobs.append(job['id'])
            system_script_forker.cleanup_children(removed_jobs)
            return


        while True:

            #acquire states: this is going to be the biggest pull from the control system.
            bf_start = time.time()
            hardware_fetch_time = Cobalt.Util.Timer()
            io_cache_time = Cobalt.Util.Timer()
            block_cache_time = Cobalt.Util.Timer()
            block_modification_time = Cobalt.Util.Timer()

            self.bridge_in_error = False
            try:
                #grab hardware state
                #self.logger.debug("acquiring hardware state")
                # Should this be locked?
                hardware_fetch_time.start()
                self.compute_hardware_vec = pybgsched.getComputeHardware()
                hardware_fetch_time.stop()
                self.logger.log(1, "hardware_fetch time: %f", hardware_fetch_time.elapsed_time)
            except:
                self.logger.critical("Error communicating with the bridge to update hardware state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
            try:
                #self.logger.debug("acquiring block states")
                #grab block states
                block_cache_time.start()
                bf = pybgsched.BlockFilter()
                bg_cached_blocks = SWIG_vector_to_list(pybgsched.getBlocks(bf))
                block_cache_time.stop()
                self.logger.log(1, "block_cache time: %f", block_cache_time.elapsed_time)
            except Exception as e:
                self.logger.critical("Error communicating with the bridge to update block information.")
                self.logger.critical("%s", traceback.format_exc())
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
            if self.bridge_in_error:
                self.logger.critical("Cannot contact bridge, update suspended.")
                #try again until we can acquire a link to the control system
                continue

            # build an IOLinks status cache, a midplane only goes in here if
            # it will not boot due to failed links
            io_cache_time.start()
            self.failed_io_midplane_cache = set()
            new_failed_io_block_names = set()
            #self.io_link_to_mp_dict = {}
            new_io_link_to_mp_dict = {}
            failed_mp = pybgsched.StringVector()
            unconnected_io = pybgsched.StringVector()
            io_comm_bridge_in_error = False

            for block_name in self._managed_blocks:
                if self._blocks[block_name].block_type == 'pseudoblock':
                    continue
                failed_mp.clear()
                unconnected_io.clear()
                try:
                    pybgsched.Block.checkIO(block_name, unconnected_io, failed_mp)
                except:
                    self.logger.critical("Error communicating with the bridge to update block IO information.")
                    self.logger.critical("%s", traceback.format_exc())
                    self.bridge_in_error = True
                    Cobalt.Util.sleep(5) # wait a little bit...
                    break

                if failed_mp.size() > 0:
                    new_failed_io_block_names.add(block_name)

            if self.bridge_in_error == True:
                continue
            self.failed_io_block_names = new_failed_io_block_names

            for mp_a in range(0, self.compute_hardware_vec.getMachineSize(sw_char_to_dim_dict['A'])):
                for mp_b in range(0, self.compute_hardware_vec.getMachineSize(sw_char_to_dim_dict['B'])):
                    for mp_c in range(0, self.compute_hardware_vec.getMachineSize(sw_char_to_dim_dict['C'])):
                        for mp_d in range(0, self.compute_hardware_vec.getMachineSize(sw_char_to_dim_dict['D'])):
                            mp = self.compute_hardware_vec.getMidplane(pybgsched.Coordinates(mp_a, mp_b, mp_c, mp_d)).getLocation()
                            try:
                                iolv = pybgsched.getIOLinks(mp)
                            except RuntimeError, e:
                                # if for one reason or another we can't get links, this mp is a non-starter.
                                if str(e) == "Data record(s) not found.":
                                    #if we have no links, then this midplane is definitely dead:
                                    self.logger.warning("No IO links found for midplane: %s". mp)
                                else:
                                    self.logger.warning("Unknown RunntimeError encountered!")
                                self.failed_io_midplane_cache.add(mp)
                                new_io_link_to_mp_dict[mp] = []
                                continue

                            io_links = SWIG_vector_to_list(iolv)
                            if len(io_links) < 4: #FIXME: Make this a threshold
                                self.failed_io_midplane_cache.add(mp)
                            new_io_link_to_mp_dict[mp] = io_links

            self.io_link_to_mp_dict = new_io_link_to_mp_dict
            io_cache_time.stop()
            self.logger.log(1, "io_cache time: %f", io_cache_time.elapsed_time)

            # first, set all of the nodecards to not busy
            for nc in self.node_card_cache.values():
                nc.used_by = ''
            self._blocks_lock.acquire()
            now = time.time()
            self.bridge_partition_cache = {}
            self.offline_blocks = []
            missing_blocks = set(self._blocks.keys())
            new_blocks = []

            block_modification_time.start()
            try:
                for block in bg_cached_blocks:
                    #find and update idle based on whether control system reads block as
                    #free or not.

                    self.bridge_partition_cache[block.getName()] = block
                    missing_blocks.discard(block.getName())
                    if self._blocks.has_key(block.getName()):
                        b = self._blocks[block.getName()]
                        b.state = _get_state(block)
                        if b.state == 'idle' and b.freeing == True:
                            b.freeing = False
                        b._update_node_cards()
                        if b.reserved_until and now > b.reserved_until:
                            b.reserved_until = False
                            b.reserved_by = None
                    else:
                        new_blocks.append(block)

                # remove the missing partitions and their wiring relations
                really_subblocks = []
                for bname in missing_blocks:
                    if self._blocks[bname].size < 128 and self._blocks[bname].subblock_parent not in missing_blocks:
                        really_subblocks.append(bname)
                        continue
                    self.logger.info("missing block removed: %s", bname)
                    b = self._blocks[bname]
                    for dep_name in b._wiring_conflicts:
                        self.logger.debug("removing wiring dependency from: %s", dep_name)
                        self._blocks[dep_name]._wiring_conflicts.discard(b.name)
                    if b.name in self._managed_blocks:
                        self._managed_blocks.discard(b.name)
                    del self._blocks[b.name]

                for bname in really_subblocks:
                    missing_blocks.remove(bname)

                bp_cache = {}

                # throttle the adding of new partitions so updating of
                # machine state doesn't get bogged down
                for block in new_blocks[:8]:
                    self.logger.info("new block found: %s", block.getName())
                    #we need the full info for the new ones
                    detailed_block_filter = pybgsched.BlockFilter()
                    detailed_block_filter.setName(block.getName())
                    detailed_block_filter.setExtendedInfo(True)
                    new_block_info = pybgsched.getBlocks(detailed_block_filter)
                    #bridge_p = Cobalt.bridge.Partition.by_id(partition.id)
                    self._blocks.q_add([self._new_block_dict(new_block_info[0])])
                    b = self._blocks[block.getName()]
                    self._detect_wiring_deps(b)

                # if partitions were added or removed, then update the relationships between partitions
                if len(missing_blocks) > 0 or len(new_blocks) > 0:
                    self.logger.debug("update_block_state updating relatives for new blocks.")
                    self.update_relatives()
                block_modification_time.stop()
                self.logger.log(1, "block_modification time: %f", block_modification_time.elapsed_time)
                bf_end = time.time()
                self.logger.log(1,'update loop init: %f sec',bf_end - bf_start)

                for b in self._blocks.values():
                    #start off all pseudoblocks as idle, we can make them not idle soon.
                    if b.block_type == "pseudoblock":
                        b.state = 'idle'

                block_update_start = time.time()
                cleanup_time = Cobalt.Util.Timer()
                recompute_block_state_time = Cobalt.Util.Timer()
                for b in self._blocks.values():
                    cleanup_time.start()
                    if b.cleanup_pending:
                        if b.used_by:
                            # start a requested job cleanup
                            _start_block_cleanup(b)
                            if b.state not in ['cleanup', 'cleanup-initiate']:
                                b.cleanup_pending = False
                                b.freeing = False
                                self.logger.info("partition %s: cleaning complete",
                                        b.name)
                        else:
                            # check ongoing cleanup
                            busy = []
                            parts = list(b._children)
                            parts.append(b)
                            for part in parts:
                                if (part.block_type != 'pseudoblock' and
                                        self.bridge_partition_cache[part.name].getStatus() != pybgsched.Block.Free):
                                    busy.append(part.name)
                                elif (part.block_type == 'pseudoblock' and
                                        self.bridge_partition_cache[part.subblock_parent].getStatus() != pybgsched.Block.Free):
                                    busy.append(part.name)
                            if len(busy) > 0:
                                _set_block_cleanup_state(b)
                            if b.state in ['cleanup', 'cleanup-initiate']:
                                self.logger.info("partition %s: still cleaning; busy partition(s): %s", b.name, ", ".join(busy))
                            else:
                                b.cleanup_pending = False
                                b.freeing = False
                                self.logger.info("partition %s: cleaning complete", b.name)

                    if b.state not in ["cleanup","cleanup-initiate"] and b.block_type != 'pseudoblock':
                        # Cleanup blocks that have had their jobs terminate early.
                        (b.block_type != 'pseudoblock') and (self.bridge_partition_cache[b.name].getStatus() == pybgsched.Block.Free) and (b.used_by)
                        if (not b.reserved_by and
                                b.block_type != 'pseudoblock' and
                                self.bridge_partition_cache[b.name].getStatus() == pybgsched.Block.Free and
                                b.used_by):
                            #FIXME: as noted by Brian, we should make this anything without a reservation.
                            # more likely set a flag to note blocks running outside of Cobalt.
                            _start_block_cleanup(b)
                            cleanup_time.stop()
                            continue
                    cleanup_time.stop()

                self.logger.log(1, 'cleanup_time: %f', cleanup_time.elapsed_time)

                recompute_block_state_time.start()
                self._recompute_block_state()
                recompute_block_state_time.stop()
                self.logger.log(1,'recompute_block_state: %f', recompute_block_state_time.elapsed_time)

                block_update_end = time.time()
                self.logger.log(1,'block_update overall: %f', block_update_end - block_update_start)
            except:
                self.logger.error("error in update_block_state", exc_info=True)
            self._blocks_lock.release()

            Cobalt.Util.sleep(10)
        #End while(true)



    def check_subblock_blocked(self, block):
        '''mark a subblock as blocked based on relative's activities.
           return true if we are blocked (don't really have to update status beyond that.

        '''

        retval = False
        for rel in block._relatives:
            if rel.state in ['busy', 'allocated', 'cleanup', 'cleanup-initiate', 'foo']:
                if rel.name != block.subblock_parent:
                    retval = True
                    block.state = 'blocked (%s)' % rel.name
                    break
                else:
                    if rel.state == 'busy':
                        found = False
                        for pg in self.process_groups.itervalues():
                            #if we have a pgroup with our parent's location
                            #then we're really blocked.  Gets script jobs too.
                            if pg.location[0] == rel.name:
                                found = True
                                break
                        if found:
                            retval = True
                            block.state = 'blocked (%s)' % rel.name
                            break
                    else:
                        retval = True
                        block.state = 'blocked (%s)' % rel.name
                        break

        return retval



    def _mark_block_for_cleaning(self, block_name, jobid, locking=True):
        '''Mark a partition as needing to have cleanup code run on it.
           Once marked, the block must eventually become usable by another job, 
           or must be placed in an error state pending admin intervention.

        '''
        if locking:
            self._blocks_lock.acquire()
        self.logger.info("block %s: prepping for cleanup, used by=%s, jobid=%s", block_name, 
                self._blocks[block_name].used_by, jobid)
        try:
            block = self._blocks[block_name]
            if block.used_by == jobid or jobid == None:
                block.cleanup_pending = True
                self.logger.info("block %s: block marked for cleanup", block_name)
                block.state = "cleanup"
                block.freeing = True
                block.current_reboots = 0
                #if this block is going to cleanup, the by definition, 
                #the reservation (aka "the Party") is over.
                #self.reserve_resources_until(block_name, None, jobid)

            elif block.used_by != None:
                #may have to relax this for psedoblock case.
                self.logger.info("block %s: job %s was not the current partition user (%s); block not marked " + \
                    "for cleanup", block, jobid, block.used_by)
        except:
            self.logger.exception("block %s: unexpected exception while marking the block for cleanup", block_name)
        if locking:
            self._blocks_lock.release()

    def _validate_kernel(self, kernel):
        '''Keeping around for when we actually get kernel support added in for this system.

        '''
        if self.config.get('kernel') != 'true':
            return True
        kernel_dir = "%s/%s" % (os.path.expandvars(self.config.get('bootprofiles')), kernel)
        return os.path.exists(kernel_dir)

    def _set_kernel(self, partition, kernel):
        '''Set the kernel to be used by jobs run on the specified partition

        This has to be redone.
        '''
        pass

    def _clear_kernel(self, partition):
        '''Set the kernel to be used by a partition to the default value

        No real change needed here
        '''

        if self.config.get('kernel') == 'true':
            try:
                self._set_kernel(partition, "default")
            except:
                logger.error("partition %s: failed to reset boot location" % (partition,))

    def generate_xml(self):
        """This method produces an XML file describing the managed partitions, suitable for use with the simulator."""
        ret = "<BG>\n"
        ret += "<BlockList>\n"
        for b_name in self._managed_blocks:
            b = self._blocks[b_name]

            ret += "   <Block name='%s'>\n" % b.name
            for nc in b.node_cards:
                ret += "      <NodeBoard id='%s' />\n" % nc.name
            for s in b.switches:
                ret += "      <Switch id='%s' />\n" % s
            for w in b.wires:
                ret += "      <Wire 'id=%s' />\n" % w
            ret += "   </Block>\n"
        ret += "</BlockList>\n"
        ret += "</BG>\n"

        return ret
    generate_xml = exposed(generate_xml)

    @exposed
    @query
    def add_process_groups (self, specs):

        """Create a process group.

        Arguments:
        spec -- dictionary hash specifying a process group to start
        """

        if self.suspend_booting:
            #booting isn't happening right now, just exit.
            self.logger.critical("Booting suspended.  Unable to add process group right now.")
            raise RuntimeError, "Booting is halted!"

        self.logger.info("add_process_groups(%r)" % (specs))

        # FIXME: setting exit_status to signal the job has failed isn't really
        # the right thing to do.  another flag should be added to the process
        # group that wait_process_group uses to determine when a process group
        # is no longer active.  An  error message should also be attached to
        # the process group so that cqm can report the problem to the user.

        start_apg_timer = time.time()
        process_groups = self.process_groups.q_add(specs)
        for pgroup in process_groups:
            pgroup.label = "Job %s/%s/%s" % (pgroup.jobid,
                    pgroup.user, pgroup.id)
            pgroup.nodect = self._blocks[pgroup.location[0]].size
            self.logger.info("%s: process group %s created to track job status",
                    pgroup.label, pgroup.id)
            try:
                self._set_kernel(pgroup.location[0], pgroup.kernel)
            except Exception, e:
                self.logger.error("%s: failed to set the kernel; %s", 
                        pgroup.label, e)
                pgroup.exit_status = 255
            else:
                if pgroup.kernel != "default":
                    self.logger.info("%s: now using kernel %s", 
                            pgroup.label, pgroup.kernel)
                if pgroup.mode == "script":
                    pgroup.forker = 'user_script_forker'
                    if pgroup.script_preboot == False:
                        self.logger.info("%s: no preboot requested.  Starting job immediately. Block %s allocated for this job.",
                                pgroup.label, pgroup.location[0])
                        #extend the resource resrevation to cover the job's runtime.
                        reserve_status = self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid)
                        self._start_process_group(pgroup)
                    else:
                        self.booter.initiate_boot(pgroup.location[0], pgroup.jobid, pgroup.user, self._blocks[pgroup.location[0]].subblock_parent, tag='internal')
                else:
                    pgroup.forker = 'bg_runjob_forker'
                    self.booter.initiate_boot(pgroup.location[0], pgroup.jobid, pgroup.user, self._blocks[pgroup.location[0]].subblock_parent, tag='internal')
        end_apg_timer = time.time()
        self.logger.debug("add_process_groups startup time: %s sec", (end_apg_timer - start_apg_timer))
        return process_groups


    def _log_boot_messages(self, pgroup):
        '''log messages from the booter to logfiles appropriate to the ongoing boot.

        '''
        boots = self.booter.get_boots_by_jobid(pgroup.jobid)
        for boot in boots:
            while True:
                status_string = boot.pop_status_string()
                if status_string == None:
                    break
                self.logger.info(status_string)
                cobalt_log_write(pgroup.cobalt_log_file, status_string, pgroup.user)
        return

    def _log_successful_boot(self, pgroup, location, success_string=None):
        '''Code to stamp in the cobatlog and syslog that a boot completed successfully.

        pgroup -- the pgroup affected by the failed boot attempt
        location -- the block location where the failure occurred
        success_string -- an optional string. If not set, default boot failure logging message is used.
        '''
        if success_string == None:
            success_string = "%s: Block %s for location %s successfully booted.  Starting task for job %s." % (pgroup.label, location, pgroup.location[0], pgroup.jobid)
        self.logger.info(success_string)
        cobalt_log_write(pgroup.cobalt_log_file, success_string, pgroup.user)


    def subblock_parent_cleaning(self, block_name):
        self._blocks_lock.acquire()
        retval = (self._blocks[self._blocks[block_name].subblock_parent].state in ['cleanup', 'cleanup-initiate'])
        self._blocks_lock.release()
        return retval


    def check_boot_status(self):
        '''Query ongoing boots.  Once a boot has completed (or failed) take appropriate action for the job, depending on request origin.

        '''
        #if the boot is one of ours and it has completed ping start process groups
        #let the user reap completed boots (auto reap if jobid no longer in process groups)
        #if failed then reap (if boot not found for query assume boot failed and reaped)
        boots = self.booter.stat()
        for boot in boots:
            if boot.tag != 'internal':
                #don't worry about user-invoked boots.
                continue
            pgroup = self.process_groups.q_get([{'jobid':boot.context.job_id}])[0]
            self._log_boot_messages(pgroup)
            if boot.state in ['complete', 'failed']:
                #should only have one pgroup for jobid
                #pgroup = self.process_groups.q_get([{'jobid':boot.context.job_id}])[0]
                #self._log_boot_messages(pgroup)
                if boot.state == 'complete': #and pgroup.mode != 'script': #and not a script.  Scripts have already started.
                    #TODO: add a "boot for me" flag.
                    self._start_process_group(pgroup)
                self.booter.reap(boot.context.block_id)
    check_boot_status = automatic(check_boot_status, 1.0)#automatic_method_default_interval)

    def _start_process_group(self, pgroup, block_loc=None):
        '''Start a process group at a specified location.

           A block_loc of None means to not do any boot check or boot tracking cleanup.

        '''
        booted_blocks = []
        #check the reservation, if we still have the block, then proceed to start, otherwise die here.

        if not self.reserve_resources_until(pgroup.location, 
                float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
            self._fail_boot(pgroup, pgroup.location[0], 
                    "%s: the internal reservation on %s expired; job has been terminated" % (pgroup.label,
                        pgroup.location))
            return
        cobalt_block = self._blocks[pgroup.location[0]]
        cobalt_block.current_reboots = 0
        try:
            self.logger.info("%s: Forking task on %s.",pgroup.label, pgroup.location[0])
            pgroup.start()
            if block_loc != None:
                booted_blocks.append(block_loc)
            if pgroup.head_pid == None:
                self.logger.error("%s: process group failed to start using the %s component; releasing resources",
                        pgroup.label, pgroup.forker)
                self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
                self._mark_block_for_cleaning(block_loc, pgroup.jobid)
                pgroup.exit_status = 255
        except (ComponentLookupError), e:
            self.logger.error("%s: failed to contact the %s component", pgroup.label, pgroup.forker)
            # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
            # until the job has exhausted its maximum alloted time
            #del self.process_groups[pgroup.id]
            return #do we need to start the whole thing again (retry state from cqm?)
        except (xmlrpclib.Fault), e:
            self.logger.error("%s: a fault occurred while attempting to start the process group using the %s "
                    "component", pgroup.label, pgroup.forker)
            # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
            # until the job has exhausted its maximum alloted time
            #del self.process_groups[process_group.id]
            #raise
            pgroup.exit_status = 255
            self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
            self._mark_block_for_cleaning(block_loc, pgroup.jobid)
            booted_blocks.append(block_loc)
            return
        except:
            self.logger.error("%s: an unexpected exception occurred while attempting to start the process group "
                    "using the %s component; releasing resources", pgroup.label, pgroup.forker, exc_info=True)
            self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
            self._mark_block_for_cleaning(block_loc, pgroup.jobid)
            pgroup.exit_status = 255
        finally:
            for block_id in booted_blocks:
                del self.booting_blocks[block_id]

        return

    check_boot_status = automatic(check_boot_status, automatic_method_default_interval)
    
    def get_process_groups (self, specs):
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))

    def _get_exit_status (self):
        '''Get the exit status of a process group that has completed.

        Args:
        None

        Side Effects: Lots!
            If a forked processes' return code is detected, then the it is set
            in the process group and the job's resources are marked for cleaning.
            It will also set information about signals.  Once the child is 
            detected as having ended, the resource reservation is released, and
            the block is marked for cleanup.

            The forker is then prodded to cull it's cache of the ended process.

            If this component cannot determine the exit staus of the now 
            defunct or otherwise nonexistent forked process, then it sets the 
            exit status to a sentinel (1234567).  

        '''

        children = {}
        cleanup = {}
        for forker in ['bg_runjob_forker', 'user_script_forker']:
            try:
                for child in ComponentProxy(forker).get_children("process group", None):
                    children[(forker, child['id'])] = child
                    child['pg'] = None
                cleanup[forker] = []
            except ComponentLookupError, e:
                self.logger.error("failed to contact the %s component to obtain a list of children", forker)
            except:
                self.logger.error("unexpected exception while getting a list of children from the %s component",
                    forker, exc_info=True)
        for pg in self.process_groups.itervalues():
            if pg.forker in cleanup:
                clean_block = False
                if (pg.forker, pg.head_pid) in children:
                    child = children[(pg.forker, pg.head_pid)]
                    child['pg'] = pg
                    if child['complete']:
                        if pg.exit_status is None:
                            pg.exit_status = child["exit_status"]
                            if child["signum"] == 0:
                                self.logger.info("%s: job exited with status %s", pg.label, pg.exit_status)
                            else:
                                if child["core_dump"]:
                                    core_dump_str = ", core dumped"
                                else:
                                    core_dump_str = ""
                                self.logger.info("%s: terminated with signal %s%s", pg.label, child["signum"], core_dump_str)
                        cleanup[pg.forker].append(child['id'])
                        clean_block = True
                else:
                    #if we are still booting we need to ignore the process group.  Only you can prevent 1234567's --PMR
                    found = False
                    boots = self.booter.get_boots_by_jobid(pg.jobid)
                    if boots != []:
                        continue
                    if pg.exit_status is None:
                        # the forker has lost the child for our process group
                        self.logger.info("%s: job exited with unknown status", pg.label)
                        # FIXME: should we use a negative number instead to indicate internal errors? --brt
                        pg.exit_status = 1234567
                        clean_block = True
                if clean_block:
                    self.reserve_resources_until(pg.location, None, pg.jobid)
                    #self._mark_block_for_cleaning(pg.location[0], pg.jobid)

        # check for children that no longer have a process group associated with them and add them to the cleanup list.  this
        # might have happpened if a previous cleanup attempt failed and the process group has already been waited upon
        for forker, child_id in children.keys():
            if children[(forker, child_id)]['pg'] is None:
                cleanup[forker].append(child['id'])

        # cleanup any children that have completed and been processed
        for forker in cleanup.keys():
            if len(cleanup[forker]) > 0:
                try:
                    ComponentProxy(forker).cleanup_children(cleanup[forker])
                except ComponentLookupError, e:
                    self.logger.error("failed to contact the %s component to cleanup children", forker)
                except:
                    self.logger.error("unexpected exception while requesting that the %s component perform cleanup",
                        forker, exc_info=True)
    _get_exit_status = automatic(_get_exit_status, float(get_config_option('bgsystem', 'get_exit_status_interval', automatic_method_default_interval)))


    def wait_process_groups (self, specs):
        """Get the exit status of any completed process groups.  If completed,
        initiate the partition cleaning process, and remove the process group 
        from system's list of active processes.

        """

        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            del self.process_groups[process_group.id]
        return process_groups
    wait_process_groups = exposed(query(wait_process_groups))

    def signal_process_groups (self, specs, signame="SIGINT"):
        """Send a signal to a currently running process group as specified by signame.

        if no signame, then SIGINT is the default.

        """

        my_process_groups = self.process_groups.q_get(specs)
        for pg in my_process_groups:
            if pg.exit_status is None:
                try:
                    if pg.head_pid != None:
                        self.logger.warning("%s: sending signal %s via %s", pg.label, signame, pg.forker)
                        ComponentProxy(pg.forker).signal(pg.head_pid, signame)
                    else:
                        self.logger.warning("%s: attempted to send a signal to job that never started", pg.label)
                except:
                    self.logger.error("%s: failed to communicate with %s when signaling job", pg.label, pg.forker)

        return my_process_groups
    signal_process_groups = exposed(query(signal_process_groups))

    @exposed
    def validate_job(self, spec):
        #can we do this earlier, it really sucks to figure out that your job can't run
        #when you're being queued and in the cqm "Running" state.
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        spec = BGBaseSystem.validate_job(self, spec)
        #No kernel stuff.  That will go here.
        return spec

    @exposed
    def halt_booting(self, user):
        self.logger.critical("Booting halted by: %s", user)
        self.suspend_booting = True
        return

    @exposed
    def resume_booting(self, user):
        self.logger.critical("Booting resumed by: %s", user)
        self.suspend_booting = False
        return

    @exposed
    def booting_status(self):
        return self.suspend_booting

    @exposed
    def set_cleaning(self, block, jobid, whoami):
        self.logger.warning("User %s force-cleaning block %s.", whoami, block)
        self._mark_block_for_cleaning(block, jobid)
        #self.reserve_resources_until(pgroup.location, None, jobid)
        return

    @exposed
    def initiate_proxy_boot(self, location, user=None, jobid=None, resid=None):
        '''Start a boot at a location on the user's behalf.  Require a valid cobalt jobid or resid for a location
        along with the proper user.

        Return True if boot was initiated succefully.  Otherwise, we failed to authenticate.

        '''
        retval = False
        is_authorized = self._auth_user_for_block(location, user, jobid, resid)
        if is_authorized:
            #mark the block as 'busy' so that we don't collide when rapidly booting blocks.
            self._blocks[location].state = 'busy'
            self.booter.initiate_boot(location, jobid, user, location, tag='external')
            retval = True
        return retval

    @exposed 
    def is_block_initialized(self, location):
        '''Check to see if we have successfully initialized a block, if so, reap and report back that it is initialized

        '''
        b = get_compute_block(location)
        return b.getStatus() == pybgsched.Block.Initialized 

    @exposed
    def get_block_bgsched_status(self, location):
        '''Return a string bgsched block status.  This is how we can tell a block is free.
        This should correspond to the block state.

        '''
        compute_block = get_compute_block(location)
        if compute_block != None:
            return compute_block.getStatusString()
        return None

    @exposed
    def initiate_proxy_free(self, location, user=None, jobid=None, resid=None):
        '''Free a block on the user's behalf.  Require jobid or resid and user.  User must be submitting user, or user on reservation

        The user is responsibile for makeing sure all jobs are dead on this block.  Once this has been invoked, no jobs will run on this block.

        '''
        #confirm, then poke control system to kill all jobs on block and free.
        retval = False
        is_authorized = self._auth_user_for_block(location, user, jobid, resid)
        if is_authorized:
            #mark the block as 'busy' so that we don't collide when rapidly booting blocks.
            self._blocks[location].state = 'cleanup'
            pybgsched.Block.initiateFree(location)
            pybgsched.Block.removeUser(location, user)
            self.logger.info('%s/%s: User requested free on block %s.', user, jobid, location)
            #get the jobs on the location and all child blocks, and signal the jobs.  After 60 sec, the block should then go into Terminating and free itself.

            block_jobs = self._get_jobs_on_block(location)
            if len(block_jobs) != 0:
                for job in block_jobs:
                    try:
                        retval = pybgsched.runjob.kill(job.getID(), signal.SIGTERM)
                        if retval != 0:
                            raise RuntimeError, "bgsched::runjob::kill failed to kill job!"
                        self.logger.info("killing backend job: %s for block %s", job.getId(), location)
                    except:
                        self.logger.critical("Unknown Error while killing backend job: %s for block %s, will retry.", job.getID(), location, exc_info=True)

            retval = True
        return retval


    @exposed
    def get_boot_statuses_and_strings(self, location=None):
        '''Allow a client to fetch the status of ongoing boots.  Returns a tuple of a boot id, status dict, and status strings.

            location - location to check for.  If not provided, return None for strings.

        '''
        status = self.booter.stat(location)[0] #there is only one boot at a given location
        if location != None:
            status_strings = self.booter.fetch_status_strings(location)
        return (status.boot_id, status.state, status_strings)

    @exposed
    def reap_boot(self, boot_id):
        '''Allow the client to clean up ongoing boot objects on it's own.

        '''
        return self.booter.reap(boot_id)


    @exposed
    def get_idle_blocks(self, parent_block, size=None, geometry=None):
        '''Fetch idle blocks.  Allow for size/geometry constraint

            parent_block - the block whose children need to be returned
            size - Return blocks of specified size, None returns all sizes.  Default None
            geometry - Geometry of block in nodes in the form of a list [A,B,C,D,E].  None allows any geometry.  Default None

        '''
        def cmp_blocks(blk1, blk2):
            retval = 0
            if blk1.size > blk2.size:
                retval =  1
            elif blk1.size < blk2.size:
                retval =  -1
            elif blk1.name > blk2.name:
                retval = 1
            elif blk2.name < blk2.name:
                retval = -1
            return retval

        ret_list = []
        self._blocks_lock.acquire()
        try:
            target_block = self._blocks[parent_block]
            ret_list = [block for block in list(target_block._children) if self._only_allocated(block)]
            if self._only_allocated(self._blocks[parent_block]):
                ret_list.append(self._blocks[parent_block])
            if size != None:
                ret_list = [block for block in ret_list if block.size == size]
            if geometry != None:
                ret_list = [block for block in ret_list if block.node_geometry == geometry]
        finally:
            #make sure we release this lock
            self._blocks_lock.release()
        ret_list.sort(cmp=cmp_blocks)
        return [block.name for block in ret_list]

    def _only_allocated(self, block):
        '''Determine if a block is actully bootable (i.e. not allocated, and not in a condition that the control system
        would consider "busy".

        block -- a Cobalt Block object

        Output:
            Returns true if the block is bootable, if any of it's parents or children are marked busy, cleanup-initiate, cleanup
            or the block itself is in any of those states return false.

        '''

        blocked_states = set(['busy', 'cleanup-initiate', 'cleanup'])
        if block.state in blocked_states:
            return False
        for relative in block._relatives:
            if relative.state in blocked_states:
                return False
        return True

