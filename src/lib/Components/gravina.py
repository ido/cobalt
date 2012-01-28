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
from Cobalt.Util import get_config_option
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

sw_char_to_dim_dict = {'A': pybgsched.Dimension(pybgsched.Dimension.A),
                       'B': pybgsched.Dimension(pybgsched.Dimension.B),
                       'C': pybgsched.Dimension(pybgsched.Dimension.C),
                       'D': pybgsched.Dimension(pybgsched.Dimension.D),
                       'E': pybgsched.Dimension(pybgsched.Dimension.E),
                       }


class BGProcessGroup(ProcessGroup):
    """ProcessGroup modified by Blue Gene systems"""
    fields = ProcessGroup.fields + ["nodect"]

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get('nodect', None)

    
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
    implementation = "gravina"
    
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
        self.configure(config_file=sim_xml_file)

        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        self.killing_jobs = {} 
        self.booting_blocks = {}

    def __getstate__(self):
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
        return {'managed_blocks':self._managed_blocks, 'version':1,
                'block_flags': flags, 'next_pg_id':self.process_groups.id_gen.idnum+1}
    
    def __setstate__(self, state):
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
                self.logger.debug("%s and %s havening problems" % (block.name, p.name))
        
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
            self.logger.debug("Bridge Init Complete.")
        else:
            self._configure_from_file(bridgeless, config_file)
            self.logger.debug("File Init Complete.")


    def _configure_from_bridge(self):

        """Read partition data from the bridge."""
        
        self.logger.info("configure()")
        
        start = time.time()
        #This initialization must occur successfully prior to anything else being done
        #with the scheduler API, or else you'll segfault out.  Absolute paths should be
        #used for init.  While init can take a relative path, the refreshConfig function will
        #error out.
        
        def init_fail_exit():
            self.logger.alert("System Component Exiting!")
            sys.exit(1)

        try:
            pybgsched.init(get_config_option("bgsystem","bg_properties","/home/richp/bg.properties"))
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
        subblock_spec_dict = self.parse_subblock_config()
        subblocks = []
        subblockDict = BlockDict()
        for block_id, minimum_size in subblock_spec_dict.iteritems():
            subblocks.extend(self.gen_subblocks(block_id, minimum_size))
        subblockDict.q_add(subblocks)
        self._blocks.update(subblockDict)
        end = time.time()
        self.logger.info("subblock configuration took %f sec" % (end - start))
            
        return
    
    ## BGSystem.parse_subblock_config
    #  Inputs: cobalt config file
    #  Output: dictionary: key: block names, values: minimum size to slice to
    #  
    #  Read from the config file a list of blocks and the smallest size to divide them to.
    #  The expected string in the config file looks like Loc:XX,Loc2:YY,Loc3:ZZ
    def parse_subblock_config(self):
        subblock_config_string = get_config_option("bgsystem","subblock_config","Empty")
        self.logger.debug(subblock_config_string)
        if subblock_config_string == "Empty":
            return {}
        retdict = {}
        for subblock_config in subblock_config_string.split(","):
            split_config = subblock_config.split(":")
            retdict[split_config[0]] = int(split_config[1])

        self.logger.debug('Setting new dict to: %s' % retdict)
        return retdict

    def gen_subblocks(self, parent_name, min_size):

        parent_block = self._blocks[parent_name]
        self.logger.debug("%s", parent_block)
        curr_size = parent_block.size #most likely to be 128
        nodecard_pos = int(nodecard_exp.search(parent_block.name).groups()[0])
        midplane_pos = int(midplane_exp.search(parent_block.name).groups()[0])
        rack_pos = int(rack_exp.search(parent_block.name).groups()[0])

        #get parent midplane information.  we only need this once:
        hw = pybgsched.getComputeHardware()
        midplane = hw.getMidplane("R%02d-M%d" % (rack_pos, midplane_pos))
        ret_blocks = []
        while (curr_size >= min_size):
            if curr_size >= 128:
                curr_size = 64
                continue
            if curr_size == 64:
                for i in range(0,2):
                    curr_name = "R%02d-M%d-N%02d-64" % (rack_pos, midplane_pos, nodecard_pos+(2*i))
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
                    
                    ret_blocks.append((dict(
                        name = curr_name, 
                        queue = "default",
                        size = curr_size,
                        node_cards = nodecard_list,
                        subblock_parent = parent_name,
                        state = 'idle'
                        )))
    
            elif curr_size == 32:
                for i in range(0,4):
                    curr_name = "R%02d-M%d-N%02d-32" % (rack_pos, midplane_pos, nodecard_pos+i)
                    nodecard_list = [] 
                    block_nodecards = ["R%02d-M%d-N%02d" % (rack_pos, midplane_pos, nodecard_pos+i)]
                                       
                    nc = midplane.getNodeBoard(i)
                    if nc.getLocation() in block_nodecards:
                        state = "idle"
                        if pybgsched.hardware_in_error_state(nc):
                            state = "error"
                        nodecard_list.append(self._get_node_card(nc.getLocation(), state))
                    ret_blocks.append((dict(
                        name = curr_name, 
                        queue = "default",
                        size = curr_size,
                        node_cards = nodecard_list,
                        subblock_parent = parent_name,
                        state = 'idle'
                        )))
            else:
                break
            curr_size = curr_size / 2
        
        return ret_blocks

    def _new_block_dict(self, block_def):
        #pull block info into a dict so that we can create internal blocks to track.
        
        #block_def must be a block from pybgsched

        switch_list=[]
        midplane_list=[]
        nodecard_list=[]
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
            state = block_def.getStatus()
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
            self.logger.info("partition %s: marking partition for cleaning", block.name)
            block.cleanup_pending = True
            blocks_cleanup.append(block)
            _set_block_cleanup_state(block)
            block.reserved_until = False
            block.reserved_by = None
            block.used_by = None

        def _set_block_cleanup_state(b):

            #set the block to the free state and kill everything on it.
            try:
                self.logger.debug("CLEANUP: Block %s reporting state as %s.", b.name, b.state)
                if b.state not in ["idle","cleanup-initiate", "cleanup"]: 
                    clean_location_filter = pybgsched.BlockFilter()
                    clean_location_filter.setName(b.name)
                    clean_block = pybgsched.getBlocks(clean_location_filter)[0]
                    pybgsched.Block.removeUser(b.name, clean_block.getUser())
                    self.logger.debug("Block %s reporting status: %s", b.name, clean_block.getStatusString())
                    if clean_block.getStatus() == pybgsched.Block.Initialized:
                        pybgsched.Block.initiateFree(b.name)
                    b.state = "cleanup-initiate"
                elif b.state == "idle":
                    self.logger.info("block %s: no block cleanup was required", b.name)
                    return
            except RuntimeError:
                #we are already freeing, ignore and go on
                self.logger.info("Free for block %s already in progress", b.name)
            except:
                self.logger.critical("Unable to initiate block free from bridge!")
                raise
            #at this point new jobs cannot start on this block
            block_jobs = None

            #don't track jobs whose kills have already completed.
            check_killing_jobs()
            #from here on, we should be able to see if the block has returned to the free state, if, so
            #and nothing else is blocking, we can safely set to idle.
            
            
            #block.state = "blocked (%s)" % (p.name,)

            if b.state == "cleanup":
                return
            try:
                
                job_block_filter = pybgsched.JobFilter()
                job_block_filter.setComputeBlockName(b.name)
                jobs = SWIG_vector_to_list(pybgsched.getJobs(job_block_filter))
            except:
                self.logger.critical("Unable to obtain list of jobs for block %s from bridge!", b.name)
                raise
            #At this point new
            if len(jobs) != 0:
                for job in jobs:
                    if job.getId() in self.killing_jobs.keys():
                        pass
                    nuke_job(job, b.name)  
            b.state = "cleanup"


            #don't track jobs whose kills have already completed.
            check_killing_jobs()
            #from here on, we should be able to see if the block has returned to the free state, if, so
            #and nothing else is blocking, we can safely set to idle.
            
            
            #block.state = "blocked (%s)" % (p.name,)
        
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
            for bg_jobid, script_id in self.killing_jobs.iteritems():
               ret = system_script_forker.child_completed(script_id)
               if ret != None:
                   complete_jobs.append(bg_jobid)

            if complete_jobs != []:
                for job in complete_jobs:
                    del self.killing_jobs[job]
            return


        while True:
            #self.logger.debug("Acquiring block update lock.")
            
            #acquire states: this is going to be the biggest pull from the control system.
            self.bridge_in_error = False
            try:
                #grab hardware state
                #self.logger.debug("acquiring hardware state")
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
            blocks_cleanup = []
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
                    self.logger.info("missing partition removed: %s", bname)
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
                    self._blocks.q_add([self._new_block_dict(new_block_info)])
                    b = self._blocks[block.getName()]
                    self._detect_wiring_deps(b, wiring_cache)

                # if partitions were added or removed, then update the relationships between partitions
                if len(missing_blocks) > 0 or len(new_blocks) > 0:
                    self.update_relatives()
                
                for b in self._blocks.values():
                    
                    if b.block_type == "pseudoblock":
                        #we don't get this from the control system here.
                        b.state = 'idle'
                        
                    #self.logger.debug("Updating block %s", b.name)
                    if b.cleanup_pending:
                        if b.used_by:
                            # if the partition has a pending cleanup request, then set the state so that cleanup will be
                            # performed
                            _start_block_cleanup(b)
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
                                self.logger.info("partition %s: still cleaning; busy partition(s): %s", b.name, ", ".join(busy))
                            else:
                                b.state = "idle"
                                b.cleanup_pending = False
                                self.logger.info("partition %s: cleaning complete", b.name)
                    if b.state == "busy":
                        # FIXME: this should not be necessary any longer since all jobs reserve the resources. --brt
                        # when the partition becomes busy, if a script job isn't reserving it, then release the reservation
                        if not b.reserved_by:
                            b.reserved_until = False
                    elif b.state not in ["cleanup","cleanup-initiate"]:
                        #block out childeren involved in the cleaning partitons
                        if b.reserved_until:
                            b.state = "allocated"
                            for block in b._parents:
                                if block.state == "idle":
                                    block.state = "blocked (%s)" % (b.name,)
                            for block in b._children:
                                if block.state == "idle":
                                    block.state = "blocked (%s)" % (b.name,)
                        elif b.block_type != 'pseudoblock' and bridge_partition_cache[b.name].getStatus() == pybgsched.Block.Free and b.used_by:
                            # FIXME: should we check the partition state or use reserved by == NULL instead?  now that all jobs
                            # reserve resources, a partition without a reservation that is also in use should probably be cleaned
                            # up regardless of partition state.  --brt

                            # if the job assigned to the partition has completed, then set the state so that cleanup will be
                            # performed
                            _start_block_cleanup(b)
                            continue

                        #TODO: Assess if this is even needed before.  We now run diags through a zero-priority queue.
                        #for diag_part in self.pending_diags:
                        #    if p.name == diag_part.name or p.name in diag_part.parents or p.name in diag_part.children:
                        #        p.state = "blocked by pending diags"

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
                                            #_start_block_cleanup(b)
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
                        
                        #Not doing diags in cobalt anymore.
                        #for part_name in self.failed_diags:
                        #    part = self._partitions[part_name]
                        #    if p.name == part.name:
                        #        p.state = "failed diags"
                        #    elif p.name in part.parents or p.name in part.children:
                        #        p.state = "blocked by failed diags"
            except:
                self.logger.error("error in update_block_state", exc_info=True)

            self._blocks_lock.release()
            
            #now continue with the cleanup

            # cleanup partitions and set their kernels back to the default (while _not_ holding the lock)
            pnames_cleaned = []
            for p in blocks_cleanup:
                self.logger.info("block %s: starting block cleanup", p.name)
                
                #if len(pnames_destroyed) > 0:
                #    self.logger.info("partition %s: partition destruction initiated for %s", p.name, ", ".join(pnames_destroyed))
                #else:
                #    self.logger.info("partition %s: no partition destruction was required", p.name)
                #try:
                #    self._clear_kernel(p.name)
                #    self.logger.info("partition %s: kernel settings cleared", p.name)
                #except:
                #    self.logger.error("partition %s: failed to clear kernel settings", p.name)
            #job-killing now handled elsewhere

            Cobalt.Util.sleep(10)

            #simulation mode. No idea how I'm going to unify these.
            blockcomment = '''
            try:
                for p in self._blocks.values():
                    p._update_node_cards()
                
                #now = time.time()
            
                # since we don't have the bridge, a partition which isn't busy
                # should be set to idle and then blocked states can be derived
                for p in self._blocks.values():

                    # did we use the partadm --failed flag?
                    # TODO: Reevaluate removing this.  Diags are no longer internal
                    #       We have other ways of doing this.  And how does this
                    #       affect out ability to determine availability?
                    if p.admin_failed:
                        p.state ="admin failed"
                        for rel in p._relatives:
                            rel.state = "admin failed relative"


                    if p.state != "busy":
                        #Assume idle?
                        p.state = "idle"
                    if p.reserved_until and now > p.reserved_until:
                        p.reserved_until = None
                        p.reserved_by = None
                    
                for p in self._blocks.values():
                    if p.state == "busy":
                        # when the partition becomes busy, if a script job isn't reserving it, then release the reservation
                        if not p.reserved_by:
                            p.reserved_until = False

                    else:
                        just_marked = False
                        if p.reserved_until:
                            p.state = "allocated"
                            for part in p._relatives:
                                if part.state == "idle":
                                    part.state = "blocked (%s)" % (p.name,)
                                    just_marked = True
                        #for nc in p.node_cards:
                        #    if nc.used_by:
                        #        if not just_marked or not (p.state in ["busy", "cleanup", "admin failed", "allocated"]):
                        #            p.state = "blocked (%s)" % nc.used_by
                        #            break
                        #for dep_name in p._wiring_conflicts:
                        #    if self._blocks[dep_name].state in ["allocated", "busy"]:
                        #        p.state = "blocked-wiring (%s)" % dep_name
                        #        break
            except:
                self.logger.error("error in update_block_state", exc_info=True)
        
            self._blocks_lock.release()
            '''


    def _mark_block_for_cleaning(self, block_name, jobid):
        '''Mark a partition as needing to have cleanup code run on it.
           Once marked, the block must eventually become usable by another job, 
           or must be placed in an error state pending admin intervention.

        '''
        self._blocks_lock.acquire()
        try:
            block = self._blocks[block_name]
            if block.used_by == jobid:
                block.cleanup_pending = True
                self.logger.info("block %s: block marked for cleanup", block_name)
                #block.state = "cleanup"            
                #block.reserved_until = False
                #block.reserved_by = None
                #block.used_by = None


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
    
    def add_process_groups (self, specs):
        
        """Create a process group.
        
        Arguments:
        spec -- dictionary hash specifying a process group to start
        """
        
        self.logger.info("add_process_groups(%r)" % (specs))

        # FIXME: setting exit_status to signal the job has failed isn't really the right thing to do.  another flag should be
        # added to the process group that wait_process_group uses to determine when a process group is no longer active.  an
        # error message should also be attached to the process group so that cqm can report the problem to the user.
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
                    
                    #TODO:This absolutely has to move.  
                    try: #Initiate boot here, I guess?  Need to make this not block.
                        #if we're already booted, (subblock), we can immediately move to start.
                        block_location_filter = pybgsched.BlockFilter()
                        block_location_filter.setName(pgroup.location[0])
                        boot_block = pybgsched.getBlocks(block_location_filter)[0]
                        boot_block.addUser(pgroup.location[0], pgroup.user)
                        boot_block.initiateBoot(pgroup.location[0])
                    except RuntimeError:
                        self.logger.warning("Unable to boot block %s.  Aborting job startup.")
                    else:
                        self.booting_blocks[pgroup.location[0]] = pgroup
                        
                else:
                    self.logger.error("%s: the internal reservation on %s expired; job has been terminated", pgroup.label,
                        pgroup.location)
                    pgroup.exit_status = 255
        return process_groups
    
    add_process_groups = exposed(query(add_process_groups))
    
    @automatic
    def check_boot_status(self):

        booted_blocks = []

        for block_loc in self.booting_blocks.keys():
            try:
                block_location_filter = pybgsched.BlockFilter()
                block_location_filter.setName(block_loc)
                boot_block = pybgsched.getBlocks(block_location_filter)[0]
            except RuntimeError:
                self.logger.warning("Unable to get block status from control system during block boot.")
                continue

            status = boot_block.getStatus()
            status_str = boot_block.getStatusString()
            if status not in [pybgsched.Block.Initialized, pybgsched.Block.Allocated]:
                #we are in a state we really shouldn't be in.  Time to fail.
                self.logger.warning("Error in block initialization. Aborting job startup.")
            elif status != pybgsched.Block.Initialized:
                self.logger.debug("waiting for boot: %s", boot_block.getStatusString())
                continue
            else:
                #we are good: start the job.
                self.logger.info("Block %s successfully booted.  Initiating job", block_loc)
                pgroup = self.booting_blocks[block_loc]
                try:
                    pgroup.start()
                    #should the fork fail, do not release the block location from status check, just let it retry.
                    #TODO: need to insure that the job is removed if this takes too long.
                        #move to a wait loop function
                        #while status != pybgsched.Block.Initialized:
                        #    boot_block = pybgsched.getBlocks(block_location_filter)[0]
                        #    status = boot_block.getStatus()
                        #    status_str = boot_block.getStatusString()
                        #    time.sleep(10)
                    #except RuntimeError:
                        #self.logger.warning("Unable to boot block %s.  Aborting job startup.")

                    #move to a job_start function
                    booted_blocks.append(block_loc)
                    if pgroup.head_pid == None:
                    
                        self.logger.error("%s: process group failed to start using the %s component; releasing resources",
                                pgroup.label, pgroup.forker)
                        self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
                        pgroup.exit_status = 255
                except (ComponentLookupError, xmlrpclib.Fault), e:
                    self.logger.error("%s: failed to contact the %s component", pgroup.label, pgroup.forker)
                    # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
                    # until the job has exhausted its maximum alloted time
                    #del self.process_groups[pgroup.id]
                    continue #do we need to start the whole thing again (retry state from cqm?)
                except (ComponentLookupError, xmlrpclib.Fault), e:
                    self.logger.error("%s: a fault occurred while attempting to start the process group using the %s "
                            "component", pgroup.label, pgroup.forker)
                        # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
                        # until the job has exhausted its maximum alloted time
                        #del self.process_groups[process_group.id]
                    #raise
                    continue
                except:
                    self.logger.error("%s: an unexpected exception occurred while attempting to start the process group "
                         "using the %s component; releasing resources", pgroup.label, pgroup.forker, exc_info=True)
                    self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
                    pgroup.exit_status = 255
                #else:
                #    self.logger.error("%s: the internal reservation on %s expired; job has been terminated", pgroup.label,
                #        pgroup.location)
                #    pgroup.exit_status = 255
        for block_id in booted_blocks:
            del self.booting_blocks[block_id]
    
    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def _get_exit_status (self):
        running = []
        active_forker_components = []
        for forker_component in ['bg_runjob_forker', 'user_script_forker']:
            try:
                running.extend(ComponentProxy(forker_component).active_list("process group"))
                active_forker_components.append(forker_component)
            except:
                self.logger.error("failed to contact %s component for list of running jobs", forker_component)

        for each in self.process_groups.itervalues():

            #skip if we're still booting
            found = False
            for pg in self.booting_blocks.values():
                if each.id == pg.id:
                    found = True
                    break
            if found:
                continue

            if each.head_pid not in running and each.exit_status is None and each.forker in active_forker_components:
                # FIXME: i bet we should consider a retry thing here -- if we fail enough times, just
                # assume the process is dead?  or maybe just say there's no exit code the first time it happens?
                # maybe the second choice is better
                try:
                    if each.head_pid != None:
                        dead_dict = ComponentProxy(each.forker).get_status(each.head_pid)
                    else:
                        dead_dict = None
                except:
                    self.logger.error("%s: RPC to get_status method in %s component failed", each.label, each.forker)
                    return
                
                if dead_dict is None:
                    self.logger.info("%s: job exited with unknown status", each.label)
                    # FIXME: should we use a negative number instead to indicate internal errors? --brt
                    each.exit_status = 1234567
                else:
                    each.exit_status = dead_dict["exit_status"]
                    if dead_dict["signum"] == 0:
                        self.logger.info("%s: job exited with status %i", each.label, each.exit_status)
                    else:
                        if dead_dict["core_dump"]:
                            core_dump_str = ", core dumped"
                        else:
                            core_dump_str = ""
                        self.logger.info("%s: terminated with signal %s%s", each.label, dead_dict["signum"], core_dump_str)
                self.reserve_resources_until(each.location, None, each.jobid)

                
    _get_exit_status = automatic(_get_exit_status)
    
    def wait_process_groups (self, specs):
        """Get the exit status of any completed process groups.  If completed,
        initiate the partition cleaning process, and remove the process group 
        from system's list of active processes.

        """
        self._get_exit_status()
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            self._mark_block_for_cleaning(process_group.location[0], process_group.jobid)
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

                if signame == "SIGKILL":
                    self._mark_partition_for_cleaning(pg.location[0], pg.jobid)

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

    #Diags are now gone.
