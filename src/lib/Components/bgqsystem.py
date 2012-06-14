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
#This is definitely going away. import Cobalt.bridge
#from Cobalt.bridge import BridgeException
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Components.bgq_base_system import NodeCard, BlockDict, BGProcessGroupDict, BGBaseSystem, JobValidationError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from pybgsched import SWIG_vector_to_list

from bgq_base_system import node_position_exp, nodecard_exp, midplane_exp, rack_exp
from bgq_base_system import NODECARD_A_DIM_MASK, NODECARD_B_DIM_MASK, NODECARD_C_DIM_MASK, NODECARD_D_DIM_MASK, NODECARD_E_DIM_MASK
from bgq_base_system import A_DIM, B_DIM, C_DIM, D_DIM, E_DIM
from bgq_base_system import get_extents_from_size

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
#Cobalt.bridge.set_serial(Cobalt.bridge.systype)

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
    fields = ProcessGroup.fields + ["nodect", "subblock", "subblock_parent", "corner", "extents"]

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get('nodect', None)
        self.subblock = False
        self.subblock_parent = None
        self.corner = None
        self.extents = None
    
# convenience function used several times below
def _get_state(bridge_partition):
    '''Convenience function to get at the block state.

    '''
    pass
    if bridge_partition.getStatus() == pybgsched.Block.Free:
        return "idle"
    else:
        return "busy"

blocked_re = re.compile("blocked")

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
            self.configure(config_file=sim_xml_file)

        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        self.killing_jobs = {} 
        self.booting_blocks = {}
        self.pgroups_pending_boot = []
        self.pgroups_wait_reboot = []
        self.suspend_booting = False


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
    
    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def _get_node_card(self, name, state="idle"):
        if not self.node_card_cache.has_key(name):
            self.node_card_cache[name] = NodeCard(name, state)
            
        return self.node_card_cache[name]

    def _get_midplane_from_location(self, loc_name):
        '''get the midplane associated with a hardware location, like a switch, or a nodecard.'''

        rack_pos = int(rack_exp.search(loc_name).groups()[0])
        midplane_pos = int(midplane_exp.search(loc_name).groups()[0])

        if self.compute_hardware_vec == None:
            raise RuntimeError("attempting to obtain nodecard state without initializing compute_hardware_vec.")
        mp = self.compute_hardware_vec.getMidplane("R%02d-M%d" % (rack_pos, midplane_pos))
        return mp

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
    

    def get_switch_state(self, sw_name):
        
        #first character in the switch name is the direction of the switch:
        # A,B,C, or D format: L_RXX-MY
        sw_id = sw_name.split("_")[0]
        mp = self._get_midplane_from_location(sw_name)
        return mp.getSwitch(sw_char_to_dim_dict[sw_id]).getState()  

    def _detect_wiring_deps(self, block, wiring_cache={}):
        """
        into a general resource intersection check.

        """
        def _kernel():
            s2 = set(p.switches)

            if s1.intersection(s2):
                p._wiring_conflicts.add(block.name)
                block._wiring_conflicts.add(p.name)
                self.logger.debug("%s and %s have a wiring conflict" % (block.name, p.name))
        
        if int(block.size) <= 512:
            #anything midplane or smaller cannot have wiring conflicts.
            #Also, I think we will have to look closer at switch states to determine if a block is actually
            #caught in a conflict.  Two midplanes in the same rack should never have a wiring conflict (maybe?)
            #TODO: Check this assumption --PMR
            return

        s1 = set(block.switches)


        if wiring_cache.has_key(block.size):
            for p in wiring_cache[block.size]:
                if block.name!=p.name:
                    _kernel()
        else:
            wiring_cache[block.size] = [block]
            for p in self._blocks.values():
                if p.size==block.size and block.name!=p.name:
                    wiring_cache[block.size].append(p)
                    _kernel()
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
        
        def init_fail_exit():
            self.logger.critical("System Component Exiting!")
            sys.exit(1)

        try:
            pybgsched.init(get_config_option("bgsystem","bg_properties","/bgsys/local/etc/bg.properties"))
        except IOError:
            self.logger.critical("IOError initializing bridge.  Check bg.properties file and database connection.")
            init_fail_exit()
        except RuntimeError:
            self.logger.critical("Abnormal RuntimeError from the bridge during initialization.")
            init_fail_exit()
        try:
            #grab the hardware state:
            hw_start = time.time()
            self.compute_hardware_vec = pybgsched.getComputeHardware()
            hw_end = time.time()
            self.logger.debug("Acquiring hardware state: took %s sec", hw_end - hw_start)
        except RuntimeError:
            self.logger.critical ("Error communicating with the bridge while acquiring hardware information.")
            init_fail_exit()
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
            init_fail_exit()
                
        # initialize a new partition dict with all partitions
        
        blocks = BlockDict()
        
        tmp_list = []

        wiring_cache = {}
        
        for block_def in system_def:
            tmp_list.append(self._new_block_dict(block_def))
        
        blocks.q_add(tmp_list)

        # update object state
        self._blocks.clear()
        self._blocks.update(blocks)

        # find the wiring deps
        wd_start = time.time()
        for block in self._blocks.values():
            self._detect_wiring_deps(block, wiring_cache)
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
                #corner_node_j_loc_list = get_corner_nodes_for_size(rack_pos, midplane_pos, nodecard_pos, curr_size)
                for i in range(0,2):
                    #curr_name = "%sR%02d-M%d-N%02d-64" % (rack_pos, midplane_pos, nodecard_pos+(2*i))
                    #nodecard_list = []
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
                    block_nodecards = ["R%02d-M%d-N%02d" % (rack_pos, midplane_pos, nodecard_pos+(2*i)),
                                       "R%02d-M%d-N%02d" % (rack_pos, midplane_pos, nodecard_pos+(2*i)+1)]
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

        switch_list=[]
        midplane_list=[]
        nodecard_list=[]
        io_link_list=[]
        midplane_ids = block_def.getMidplanes()
        midplane_nodecards = []
        for midplane_id in midplane_ids:
            #grab the switch data from all associated midplanes
            midplane = self.compute_hardware_vec.getMidplane(midplane_id)
            midplane_list.append(midplane)
            for i in range(0, 4):
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

        d = dict(
            name = block_def.getName(), 
            queue = "default",
            size = block_def.getComputeNodeCount(),
            midplanes = midplane_list,
            node_cards = nodecard_list,
            switches = switch_list,
            state = block_def.getStatus(),
            block_type = 'normal'
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

        # this is going to hold partition objects from the bridge (not our own Partition)
        #wiring_cache = {}
        
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

            #if not wiring_cache.has_key(nc_count):
            #    wiring_cache[nc_count] = []
            #wiring_cache[nc_count].append(partition_def.get("name"))

            #for s in partition_def.getiterator("Switch"):
            #    switch_list.append(s.get("id"))
            
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
   
    def update_block_state(self):
        """Use the quicker bridge method that doesn't return nodecard information to update the states of the partitions"""
        
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
                    
                    compute_block = self.get_compute_block(block.name)
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

        def _get_jobs_on_block(block_name):
            try: 
                job_block_filter = pybgsched.JobFilter()
                job_block_filter.setComputeBlockName(block_name)
                jobs = SWIG_vector_to_list(pybgsched.getJobs(job_block_filter))
            except:
                self.logger.critical("Unable to obtain list of jobs for block %s from bridge!", block_name)
                raise
            return jobs


        def _children_still_allocated(block):
            for b in block._children:
                    if b.used_by:
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
            else:
                #ensure nothing else is running on the subblock parent.  If we're the last one out, 
                #then free the subblock.
                self.logger.info("initiaitng normal block cleanup for subblockblock %s, parent: %s", b.name, b.subblock_parent)
                pb = self._blocks[b.subblock_parent]
                still_reserved_children = _children_still_allocated(pb)
                block_jobs = _get_jobs_on_block(b.subblock_parent)
                
                if not still_reserved_children:
                    self.logger.info("All subblock jobs done, freeing block %s", pb.name)
                    if pb.state not in ["cleanup", "cleanup-initiate"]:
                        _start_block_cleanup(pb)
                        self.logger.info("block %s: block marked for cleanup", pb.name)
                    pb.freeing = True
                else:
                    local_job_found = False
                    for job in block_jobs:
                        if job.getCorner() == b.corner_node and job.getShape().getNodeCount() == b.size and job.getID() not in self.killing_jobs.keys():
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
            block_jobs = _get_jobs_on_block(b.subblock_parent)
            #At this point new for the Q.  Blow everything away!
            if len(block_jobs) != 0:
                for job in block_jobs:
                    if job.getId() in self.killing_jobs.keys():
                        pass
                    nuke_job(job, b.name)  
            b.state = "cleanup"


            #don't track jobs whose kills have already completed.
            check_killing_jobs() #reap any ongoing kills
       

        def nuke_job(bg_job, block_name):
            #As soon as I get an API this is going to change.  Assume all on SN.
            #for now make a call to kill_job Job should die after 60 sec, if not earlier.

            try:
                retval = ComponentProxy('system_script_forker').fork(
                        ['/bgsys/drivers/ppcfloor/hlcs/bin/kill_job', '%d'%bg_job.getId() ], 'bg_system_cleanup', '%s cleanup:'% bg_job.getId())
                self.logger.info("killing backend job: %s for block %s", bg_job.getId(), block_name)
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
            #self.logger.debug("Acquiring block update lock.")
            
            #acquire states: this is going to be the biggest pull from the control system.
            self.bridge_in_error = False
            try:
                #grab hardware state
                #self.logger.debug("acquiring hardware state")
                # Should this be locked?
                self.compute_hardware_vec = pybgsched.getComputeHardware()
            except:
                self.logger.error("Error communicating with the bridge to update partition state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
            try:
                #self.logger.debug("acquiring block states")
                #grab block states
                bf = pybgsched.BlockFilter()
                bg_cached_blocks = SWIG_vector_to_list(pybgsched.getBlocks(bf))
            except:
                self.logger.error("Error communicating with the bridge to update block information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
            if self.bridge_in_error:
                self.logger.critical("Cannot contact bridge, update suspended.")
                #try again until we can acquire a link to the control system
                continue

   
   
            # first, set all of the nodecards to not busy
            for nc in self.node_card_cache.values():
                nc.used_by = ''
            self._blocks_lock.acquire()
            now = time.time()
            bridge_partition_cache = {}
            self.offline_blocks = []
            missing_blocks = set(self._blocks.keys())
            new_blocks = []

            try:
                for block in bg_cached_blocks:
                    #find and update idle based on whether control system reads block as
                    #free or not. 
                    
                    bridge_partition_cache[block.getName()] = block
                    missing_blocks.discard(block.getName())
                    if self._blocks.has_key(block.getName()):
                        b = self._blocks[block.getName()]
                        b.state = _get_state(block)
                        if b.state == 'idle' and b.freeing == True:
                            b.freeing = False
                            for child in b._children:
                                b.freeing = False
                        b._update_node_cards()
                        if b.reserved_until and now > b.reserved_until:
                            b.reserved_until = False
                            b.reserved_by = None
                    else:
                        new_blocks.append(block)

                
                # remove the missing partitions and their wiring relations
                for bname in missing_blocks:
                    if self._blocks[bname].size < 128 and self._blocks[bname].subblock_parent not in missing_blocks:
                        continue
                    self.logger.info("missing block removed: %s", bname)
                    b = self._blocks[bname]
                    for dep_name in b._wiring_conflicts:
                        self.logger.debug("removing wiring dependency from: %s", dep_name)
                        self._blocks[dep_name]._wiring_conflicts.discard(b.name)
                    if b.name in self._managed_blocks:
                        self._managed_blocks.discard(b.name)
                    del self._blocks[b.name]

                bp_cache = {}
                wiring_cache = {}
                
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
                    self._detect_wiring_deps(b, wiring_cache)

                # if partitions were added or removed, then update the relationships between partitions
                if len(missing_blocks) > 0 or len(new_blocks) > 0:
                    self.update_relatives()
               
                for b in self._blocks.values():
                    #start off all pseudoblocks as idle, we can make them not idle soon.
                    if b.block_type == "pseudoblock":
                        b.state = 'idle'
                
                for b in self._blocks.values():
                  

                    if b.cleanup_pending:
                        if b.used_by:
                            # if the partition has a pending cleanup request, then set the state so that cleanup will be
                            # performed
                            self.logger.debug("USED BY SET TO: %s", b.used_by)
                            _start_block_cleanup(b)
                            if b.state not in ['cleanup', 'cleanup-initiate']:
                                b.cleanup_pending = False
                                b.freeing = False
                                self.logger.info("partition %s: cleaning complete", b.name)

                        else:
                            # if the cleanup has already been initiated, then see how it's going
                            busy = []
                            parts = list(b._children)
                            parts.append(b)
                            for part in parts:
                                if part.block_type != 'pseudoblock' and bridge_partition_cache[part.name].getStatus() != pybgsched.Block.Free:
                                    busy.append(part.name)
                                elif part.block_type == 'pseudoblock' and bridge_partition_cache[part.subblock_parent].getStatus() != pybgsched.Block.Free:
                                    busy.append(part.name)
                            if len(busy) > 0:
                                _set_block_cleanup_state(b)
                            if b.state in ['cleanup', 'cleanup-initiate']:
                                self.logger.info("partition %s: still cleaning; busy partition(s): %s", b.name, ", ".join(busy))
                            else:
                                b.cleanup_pending = False
                                b.freeing = False
                                self.logger.info("partition %s: cleaning complete", b.name)
                    
                     
                    if b.block_type == "pseudoblock":
                        #we don't get this from the control system here.
                        #b.state = 'idle'
                        if b.state != 'idle':
                            continue #already sorted this guy out.
                        
                        is_allocated = self.check_allocated(b)
                        if is_allocated: #we aren't going to be busy if we're not allocated (for much longer)
                            #but we might be busy
                            block_jobs = _get_jobs_on_block(b.subblock_parent)
                            for job in block_jobs:
                                if job.getCorner() in [node.name for node in b.nodes] and job.getComputeNodesUsed() == b.size: 
                                    #If I have a backend job on my nodes, then I'm busy.
                                    b.state = "busy"
                                    #we're really busy and need to mark relatives.
                                    for block in b._relatives:
                                        if block.state == "idle":
                                            block.state = "blocked (%s)" % (b.name)
                                    break

                        if b.state == ['busy', 'allocated']:
                            continue #yeah we're done with this block
                        
                        is_blocked = self.check_subblock_blocked(b)
                        if is_blocked:
                            continue #we are state blocked.
                        
                        #Remember: bad hardware takes out all child pseudoblocks as well, since you
                        #can't boot the parent.
                        #bad hardware hoits!
                        subblock_parent_block = self._blocks[b.subblock_parent]
                        for nc in subblock_parent_block.node_cards:
                           if nc.used_by:
                               #block if other stuff is running on our node cards.  
                               #remember subblock jobs can violate this 
                               #TODO: test with subblock
                               if b.subblock_parent != nc.used_by or b.subblock_parent == b.name: 
                                   b.state = "blocked (%s)" % nc.used_by

                           if self.get_nodecard_state(nc.name) != pybgsched.Hardware.Available:
                               #if control system reports down, then we're really down.
                               b.state = "hardware offline (%s): nodecard %s" % (self.get_nodecard_state_str(nc.name), nc.name)
                               self.offline_blocks.append(b.name)
                               if self.get_nodecard_state(nc.name) == pybgsched.Hardware.Error and nc.used_by != '':
                                   #we are in a soft error and should attempt to free
                                   if not nc.used_by in freeing_error_blocks:
                                       try:
                                           pybgsched.Block.initiateFree(nc.used_by)
                                           self.logger.warning("Attempting to free block %s to clear error.", nc.used_by)
                                       except RuntimeError:
                                           pass
                                       except:
                                           self.logger.debug("error initiating free for soft error block.")
                                       freeing_error_blocks.append(nc.used_by)
                         # I think we can fall into cleanup code here?


                    #check the state of the block's IOLinks.  If not all are connected, put the block into an error state.
                    bad_links = pybgsched.StringVector()
                    if not pybgsched.Block.isIOConnected(b.subblock_parent, bad_links):
                        b.state = "IO Link Unconnected: %s" % bad_links[0]
                    #don't even bother if we failed the last test, this one checks do we have enough links/midplane to start?
                    #Assume losing 50% of links is fatal for now.  Will need to ultimately make this configurable.
                    #Even better if I can get IONs that are mapped to blocks, but that will have to come in on Rev2 --PMR
                    else:
                        try:
                            current_system_block = pybgsched.BlockFilter()
                            current_system_block.setName(b.subblock_parent)
                            current_system_block.setExtendedInfo(True)
                            sys_block = pybgsched.getBlocks(current_system_block)[0] 
                            midplanes = sys_block.getMidplanes()
                        except:
                            self.logger.critical('Error fetching block data in update blocks. Marking %s down due to control system error.', b.name)
                            b.state = "Control System Error"
                            continue
                        for mp in midplanes:
                            try:
                                iolv = pybgsched.getIOLinks(mp)
                            except RuntimeError, e:
                                if str(e) == "Data record(s) not found.":
                                    b.state = "Insufficient IO Links: %s" % mp
                                else:
                                    self.logger.warning("Unknown RunntimeError encountered!")
                                    raise
                                break
                            io_links = SWIG_vector_to_list(iolv)
                            if len(io_links) < 4:#FIXME: Make this a threshold
                                b.state = "Insufficient IO Links: %s" % mp
                                break
                            for link in io_links:
                                if link.getState() != pybgsched.IOLink.Available:
                                    b.state = "hardware offline (%s) IOLink %s:" %(link.getStateString(), link.getDestinationLocation())

                    # We have a prayer of booting now: so why shouldn't we boot this block?
                    # The answer is below:

                    if b.state == "busy":
                        # FIXME: this should not be necessary any longer since all jobs reserve the resources. --brt
                        # when the partition becomes busy, if a script job isn't reserving it, then release the reservation
                        if not b.reserved_by:
                            b.reserved_until = False
                        # We may not actually be busy, if not then fall back to idle and take a pass below.
                        block_jobs = _get_jobs_on_block(b.subblock_parent) 
                        if b.block_type != "pseudoblock" and len(block_jobs) == 1 and block_jobs[0].getComputeNodesUsed() == b.size:
                            #no, we really are busy.  Make sure our pseudoblock children are marked as such.
                            for block in b._children:
                                if block.state == "idle":
                                    block.state = "blocked (%s)" % b.name
                        elif b.size > 128: #FIXME: make this settable in the cobalt.conf
                            pass #Yep, busy.  Probably a script job
                        
                    elif b.state not in ["cleanup","cleanup-initiate"] and b.block_type != 'pseudoblock':
                        #block out childeren involved in the cleaning partitons
                        is_allocated = self.check_allocated(b)
                        if (not is_allocated) and (b.block_type != 'pseudoblock') and (bridge_partition_cache[b.name].getStatus() == pybgsched.Block.Free) and (b.used_by):
                            # FIXME: should we check the partition state or use reserved by == NULL instead?  now that all jobs
                            # reserve resources, a partition without a reservation that is also in use should probably be cleaned
                            # up regardless of partition state.  --brt

                            # if the job assigned to the partition has completed, then set the state so that cleanup will be
                            # performed
                            _start_block_cleanup(b)
                            continue

                        freeing_error_blocks = []
                        for nc in b.node_cards:
                            if nc.used_by:
                                #block if other stuff is running on our node cards.  
                                #remember subblock jobs can violate this 
                                #TODO: test with subblock
                                b.state = "blocked (%s)" % nc.used_by

                            if self.get_nodecard_state(nc.name) != pybgsched.Hardware.Available:
                                #if control system reports down, then we're really down.
                                b.state = "hardware offline (%s): nodecard %s" % (self.get_nodecard_state_str(nc.name), nc.name)
                                self.offline_blocks.append(b.name)
                                if self.get_nodecard_state(nc.name) == pybgsched.Hardware.Error and nc.used_by != '':
                                    #we are in a soft error and should attempt to free
                                    if not nc.used_by in freeing_error_blocks:
                                        try:
                                            pybgsched.Block.initiateFree(nc.used_by)
                                            self.logger.warning("Attempting to free block %s to clear error.", nc.used_by)
                                        except RuntimeError:
                                            pass
                                        except:
                                            self.logger.debug("error initiating free for soft error block.")
                                        freeing_error_blocks.append(nc.used_by)

                        for sw in b.switches:
                            if self.get_switch_state(sw) != pybgsched.Hardware.Available:
                                b.state = "hardware offline: switch %s" % sw 
                                self.offline_blocks.append(b.name)
                        for dep_name in b._wiring_conflicts:
                            if self._blocks[dep_name].state in ["busy", "allocated", "cleanup"]:
                                b.state = "blocked-wiring (%s)" % dep_name
                                break
                        
            except:
                self.logger.error("error in update_block_state", exc_info=True)

            self._blocks_lock.release()
                
            Cobalt.Util.sleep(10)
        #End while(true)

    def check_IO_connected(self, block, hardware):
        pass

    def check_sufficient_IO(self, block, hardware):
        pass

    def check_allocated(self, b):
        '''Check to see if this block is allocated by cobalt to a job.
           
           If so, then mark all of this block's parents and children as
           blocked, by the allocated partition.

        '''
        
        allocated = False
        if b.reserved_until:
            b.state = "allocated"
            allocated = True
            for block in b._relatives:
                if block.state == "idle":
                    block.state = "blocked (%s)" % (b.name,)
        return allocated

    def initiate_cleanup(self, block):
        pass

    def check_subblock_blocked(self, block):
        '''mark a subblock as blocked based on relative's activities.
           return true if we are blocked (don't really have to update status beyond that.
         
        '''
        
        retval = False
        for rel in block._relatives:
            if rel.state in ['busy', 'allocated', 'cleanup', 'cleanup-initiate']:
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

    def check_nodeboard_offline(self, block, freeing_error_blocks):
     
        for nc in b.node_cards:
            if nc.used_by:
                #block if other stuff is running on our node cards.  
                #remember subblock jobs can violate this 
                #TODO: test with subblock
                b.state = "blocked (%s)" % nc.used_by
            
            if self.get_nodecard_state(nc.name) != pybgsched.Hardware.Available:
                #if control system reports down, then we're really down.
                b.state = "hardware offline (%s): nodecard %s" % (self.get_nodecard_state_str(nc.name), nc.name)
                self.offline_blocks.append(b.name)
                if self.get_nodecard_state(nc.name) == pybgsched.Hardware.Error and nc.used_by != '':
                    #we are in a soft error and should attempt to free
                    if not nc.used_by in freeing_error_blocks:
                        try:
                            #_start_block_cleanup(b)
                            pybgsched.Block.initiateFree(nc.used_by)
                            self.logger.warning("Attempting to free block %s to clear error.", nc.used_by)
                        except RuntimeError:
                            pass
                        except:
                            self.logger.debug("error initiating free for soft error block.")
                        freeing_error_blocks.append(nc.used_by)

        return

    def check_switch_offline(self, block):
        pass

    def check_wiring_conflict(self, block):
        pass


    def _mark_block_for_cleaning(self, block_name, jobid):
        '''Mark a partition as needing to have cleanup code run on it.
           Once marked, the block must eventually become usable by another job, 
           or must be placed in an error state pending admin intervention.

        '''
        

        self._blocks_lock.acquire()
        try:
            block = self._blocks[block_name]
            if block.used_by == jobid or jobid == None:
                block.cleanup_pending = True
                self.logger.info("block %s: block marked for cleanup", block_name)
                block.state = "cleanup"
                block.freeing = True
                #if this block is going to cleanup, the by definition, 
                #the reservation (aka "the Party") is over.
                #self.reserve_resources_until(block_name, None, jobid)

            elif block.used_by != None:
                #may have to relax this for psedoblock case.
                self.logger.info("block %s: job %s was not the current partition user (%s); block not marked " + \
                    "for cleanup", block, jobid, block.used_by)
        except:
            self.logger.exception("block %s: unexpected exception while marking the block for cleanup", block_name)
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

            ret += "   <Block name='%s'>\n" % p.name
            for nc in b.node_cards:
                ret += "      <NodeCard id='%s' />\n" % nc.name
            #for s in p.switches:
            #    ret += "      <Switch id='%s' />\n" % s
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

        # FIXME: setting exit_status to signal the job has failed isn't really the right thing to do.  another flag should be
        # added to the process group that wait_process_group uses to determine when a process group is no longer active.  an
        # error message should also be attached to the process group so that cqm can report the problem to the user.

        start_apg_timer = time.time()
        process_groups = self.process_groups.q_add(specs)
        for pgroup in process_groups:
            pgroup.label = "Job %s/%s/%s" % (pgroup.jobid, pgroup.user, pgroup.id)
            pgroup.nodect = self._blocks[pgroup.location[0]].size
            self.logger.info("%s: process group %s created to track job status", pgroup.label, pgroup.id)
            try:
                self._set_kernel(pgroup.location[0], pgroup.kernel)
            except Exception, e:
                self.logger.error("%s: failed to set the kernel; %s", pgroup.label, e)
                pgroup.exit_status = 255
            else:
                if pgroup.kernel != "default":
                    self.logger.info("%s: now using kernel %s", pgroup.label, pgroup.kernel)
                if pgroup.mode == "script":
                    pgroup.forker = 'user_script_forker'
                else:
                    pgroup.forker = 'bg_runjob_forker'
                if self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
                    boot_location_block = self._blocks[pgroup.location[0]]
                    boot_location = boot_location_block.subblock_parent
                    try:
                        compute_block = self.get_compute_block(boot_location)
                        pybgsched.Block.addUser(boot_location, pgroup.user)
                    except RuntimeError:
                        self._fail_boot(pgroup, boot_location, "%s: Unable to retrieve control system data for block %s. Aborting job." % (pgroup.label, boot_location))

                    if boot_location_block.block_type == 'pseudoblock':
                        #we have to boot a subblock job.  This block may already be booted.
                        pgroup.subblock = True
                        pgroup.subblock_parent = boot_location
                        pgroup.corner = boot_location_block.corner_node
                        pgroup.extents = boot_location_block.extents
                        if compute_block.getStatus() in [pybgsched.Block.Allocated, pybgsched.Block.Booting]:
                            #we are in the middle of starting another on the same subblock. We need to wait until this 
                            #block has completed booting.
                            self.pgroups_pending_boot.append(pgroup)
                            continue
                        elif compute_block.getStatus() == pybgsched.Block.Initialized:
                            #already booted, we can start right away.
                            if not (self._blocks[boot_location].state in ['cleanup','cleanup-initiate']) or self._blocks[boot_location].freeing: #well almost.  the block appears to be freeing.
                                self._log_successful_boot(pgroup, boot_location, "%s: Block %s for location %s already booted.  Starting task for job %s. (APG)" % (pgroup.label, boot_location, pgroup.location[0], pgroup.jobid))
                                compute_block.addUser(boot_location, pgroup.user)
                                self._start_process_group(pgroup)
                                continue
                            else: #we're going to have to wait for this block to free and reboot the block.
                                self.logger.info("%s trying to start on freeing block %s. waiting until free.", pgroup.label, boot_location)
                                self.pgroups_wait_reboot.append(pgroup)
                                continue
                        #otherwise we should proceed through normal block booting proceedures.
                    boot_completed = self.initiate_boot(boot_location)    
               else:
                    self._fail_boot(pgroup, pgroup.location[0], "%s: the internal reservation on %s expired; job has been terminated"% (pgroup.label,
                                                    pgroup.location))
        
        end_apg_timer = time.time()
        self.logger.debug("add_process_groups startup time: %s sec", (end_apg_timer - start_apg_timer))
        return process_groups
   
    def get_compute_block(self, block, extended_info=False):
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

    def initiate_boot(self, boot_location):
        '''Initiate the boot on a block, return True if the boot started successfully, otherwise return false.

        '''

        try: #start the nonblocking boot.
            boot_block.initiateBoot(boot_location)
            self._log_successful_boot(pgroup, boot_location, "%s: Initiating boot at location %s." % (pgroup.label, boot_location))
        except RuntimeError:
            self._fail_boot(pgroup, boot_location, "%s: Unable to boot block %s due to RuntimeError. Aborting job startup." % (pgroup.label, boot_location))
        else:
            self.booting_blocks[boot_location] = pgroup
            return True
        return False
        


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



    def _fail_boot(self, pgroup, location, failure_string=None):

        '''Code to cleanup and log the failure of a boot.
        Also, ensure entries to appropriate log files and .cobaltlogs happen.

        pgroup -- the pgroup affected by the failed boot attempt
        location -- the block location where the failure occurred
        failure_string -- an optional string. If not set, default boot failure logging message is used.

        '''
        
        if failure_string == None:
            failure_string = "%s: Job %s terminated due to boot failure. No task was started." % (pgroup.label, pgroup.jobid)

        self.logger.warning(failure_string)
        #COBALTLOG
        cobalt_log_write(pgroup.cobalt_log_file, failure_string, pgroup.user)
        pgroup.exit_status = 255
        #strip pgroup out of appropriate places?
        self._mark_block_for_cleaning(location, pgroup.jobid)

        return
    
    def subblock_parent_cleaning(self, block_name):
        self._blocks_lock.acquire()
        retval = (self._blocks[self._blocks[block_name].subblock_parent].state in ['cleanup', 'cleanup-initiate'])
        self._blocks_lock.release()
        return retval

    def check_pgroups_wait_reboot (self):

        '''Sometimes we have to wait until we can reboot the block. 
        This is what allows us to do so.

        A block can move from this to starting the job, checking an ongoing boot, it can also initiate a boot if the block is seen as free.

        '''
        #TODO: check to see if the block is healthy enough to boot,  if we have a sudden case of dead-link,
        #bad-hardware, et al. we should totally bail out.

        if self.suspend_booting:
            #booting isn't happening right now, just exit.
            return

        progressing_pgroups = []
        for pgroup in self.pgroups_wait_reboot:
            
            if not self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
                self._fail_boot(pgroup, pgroup.location[0], "%s: the internal reservation on %s expired; job has been terminated"% (pgroup.label,
                                                                        pgroup.location))
                progressing_pgroups.append(pgroup)
                continue
            
            parent_block_name = self._blocks[pgroup.location[0]].subblock_parent
            reboot_block = self.get_compute_block(parent_block_name)
            if reboot_block.getStatus() == pybgsched.Block.Free: #block freed: initiate reboot
                progressing_pgroups.append(pgroup) 
                boot_location_block = self._blocks[pgroup.location[0]]
                boot_location = boot_location_block.subblock_parent
                try: #Initiate boot here, I guess?  Need to make this not block.
                    #if we're already booted, (subblock), we can immediately move to start.
                    boot_block = self.get_compute_block(boot_location)
                    boot_block.addUser(boot_location, pgroup.user)
                    boot_block.initiateBoot(boot_location)
                    self._log_successful_boot(pgroup, boot_location, 
                        "%s: Initiating boot at location %s." % (pgroup.label, boot_location))
                except RuntimeError:
                    self._fail_boot(pgroup, boot_location, 
                        "%s: Unable to boot block %s. Aborting job startup." % (pgroup.label, boot_location))
                    progressing_pgroups.append(pgroup)
                else:
                    self.booting_blocks[boot_location] = pgroup   
            elif reboot_block.getStatus() in [pybgsched.Block.Allocated, pybgsched.Block.Booting]: # block rebooting, check pending boot
                self.logger.warning("%s: Block for pending subblock job on %s is booting.  Waiting for boot completion.", pgroup.label, pgroup.location[0])
                progressing_pgroups.append(pgroup)
                self.pgroups_pending_boot.append(pgroup)
            elif reboot_block.getStatus == pybgsched.Block.Initialized:
                if self._blocks[reboot_block.getName()].freeing == False: #block rebooted. Go ahead and start job.
                    self._log_successful_boot(pgroup, boot_location, 
                            "%s: Block for pending subblock job on %s is rebooted.  Starting job." % (pgroup.label, pgroup.location[0]))
                    progressing_pgroups.append(pgroup)
                    reboot_block.addUser(pgroup.subblock_parent, pgroup.user)
                    self._start_process_group(pgroup)

        for pgroup in progressing_pgroups:
            self.pgroups_wait_reboot.remove(pgroup)

    check_pgroups_wait_reboot = automatic(check_pgroups_wait_reboot, automatic_method_default_interval)

    def check_pgroups_pending_boot(self):
        '''check up on groups that are waiting to start up.

        '''
        if self.suspend_booting:
            #booting isn't happening right now, just exit.
            return

        booted_pgroups = []
        for pgroup in self.pgroups_pending_boot:
            if not self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
                self._fail_boot(pgroup, pgroup.location[0], "%s: the internal reservation on %s expired; job has been terminated"% (pgroup.label,
                                                                        pgroup.location))
                booted_pgroups.append(pgroup)
                continue
            boot_block = self.get_compute_block(pgroup.subblock_parent)

            if boot_block.getStatus() == pybgsched.Block.Initialized:
                self._log_successful_boot(pgroup, pgroup.subblock_parent, "%s: Block %s for location %s successfully booted.  Starting task for job %s. (CPPB)" % (pgroup.label, pgroup.subblock_parent, pgroup.location[0], pgroup.jobid))
                boot_block.addUser(pgroup.subblock_parent, pgroup.user)
                self._start_process_group(pgroup)
                booted_pgroups.append(pgroup)
            elif boot_block.getStatus() == pybgsched.Block.Free: #Something has gone very wrong here, abort. Should we try and boot again?
                #may have had an inopportune free, go ahead and make this and try and reboot.
                self.pgroups_wait_reboot.append(pgroup)
                self.logger.warning("%s: Block for pending subblock job on %s free. Attempting reboot.", pgroup.label, pgroup.location[0])
                booted_pgroups.append(pgroup)

        #clean up the ones we've stopped tracking
        for pgroup in booted_pgroups:
            self.pgroups_pending_boot.remove(pgroup)

    check_pgroups_pending_boot = automatic(check_pgroups_pending_boot, automatic_method_default_interval)
   
    def check_boot_status(self):
        
        booted_blocks = []
        for block_loc in self.booting_blocks.keys():
            pgroup = self.booting_blocks[block_loc]


            try:
                block_location_filter = pybgsched.BlockFilter()
                block_location_filter.setName(block_loc)
                boot_block = pybgsched.getBlocks(block_location_filter)[0]
            except RuntimeError:
                self.logger.warning("Unable to get block status from control system during block boot.")
                continue

            status = boot_block.getStatus()
            status_str = boot_block.getStatusString()
            if self._blocks[block_loc].freeing == True:
                self.logger.warning("%s: Booting aborted by an incoming free request, will attempt to reboot block %s.", pgroup.label, block_loc)
                self.pgroups_wait_reboot.append(pgroup)
                booted_blocks.append(block_loc)
                continue
            if status not in [pybgsched.Block.Initialized, pybgsched.Block.Allocated, pybgsched.Block.Booting]:
                #we are in a state we really shouldn't be in.  Time to fail.
                if status == pybgsched.Block.Free:
                    self.logger.warning("%s: Block %s found in free state.  Attempting reboot.", pgroup.label, pgroup.location[0])
                    if not pgroup in self.pgroups_wait_reboot:
                        self.pgroups_wait_reboot.append(pgroup)
                        booted_blocks.append(block_loc)
                else:
                    self._fail_boot(pgroup, pgroup.location[0], "%s: Unable to boot block %s. Aborting job startup. Block stautus was %s" % (pgroup.label, pgroup.location[0], status_str))
                    booted_blocks.append(block_loc) 
            elif status != pybgsched.Block.Initialized:
                self.logger.debug("%s: Block: %s waiting for boot: %s",pgroup.label, pgroup.location[0],  boot_block.getStatusString())
                continue
            else:
                #we are good: start the job.
                self._log_successful_boot(pgroup, block_loc, "%s: Block %s for location %s successfully booted.  Starting task for job %s. (CBS)" % (pgroup.label, block_loc, pgroup.location[0], pgroup.jobid))
                pgroup = self.booting_blocks[block_loc]
                self._start_process_group(pgroup, block_loc)
    
        for block_loc in booted_blocks:
            self.booting_blocks.pop(block_loc)

    check_boot_status = automatic(check_boot_status, automatic_method_default_interval)
    
    def _start_process_group(self, pgroup, block_loc=None):
        '''Start a process group at a specified location.
            
           A block_loc of None means to not do any boot check or boot tracking cleanup.

        '''
        booted_blocks = []
        #check the reservation, if we still have the block, then proceed to start, otherwise die here.

        if not self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
            self._fail_boot(pgroup, pgroup.location[0], "%s: the internal reservation on %s expired; job has been terminated"% (pgroup.label,
                                                                        pgroup.location))
            #pgroup.exit_status = 255
            return
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
                    for boot_pg in self.booting_blocks.values():
                        if boot_pg.id == pg.id:
                            found = True
                            break
                    for boot_pg in self.pgroups_pending_boot:
                        if boot_pg.id == pg.id:
                            found = True
                            break
                    for boot_pg in self.pgroups_wait_reboot:
                        if boot_pg.id == pg.id:
                            found = True
                            break
                    if found:
                        continue

                    if pg.exit_status is None:
                        # the forker has lost the child for our process group
                        self.logger.info("%s: job exited with unknown status", pg.label)
                        # FIXME: should we use a negative number instead to indicate internal errors? --brt
                        pg.exit_status = 1234567
                        clean_block = True
                if clean_block:
                    self.reserve_resources_until(pg.location, None, pg.jobid)
                    self._mark_block_for_cleaning(pg.location[0], pg.jobid)

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
    validate_job = exposed(validate_job)

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
    def initiate_proxy_boot(self, location, user=None, jobid=None):
        return self.initiate_boot(location)

    @exposed is_block_initialized(self, location):
        b = self.get_compute_block(location)
        return if b.getStatus() == pybgsched.Block.Initialized 
        
    @exposed
    def initiate_proxy_free(self, location, user=None, jobid=None):
        raise NotImplementedError, "Proxy freeing is not supported for this configuration."

