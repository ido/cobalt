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
    #if bridge_partition.state == "RM_PARTITION_FREE":
    #    return "idle"
    #else:
    #    return "busy"

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
        self.configure(config_file="bgq_simulator.xml")
        

        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        


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

        self.configure(config_file="bgq_simulator.xml")
        if 'block_flags' in state:
            for bname, flags in state['block_flags'].items():
                if bname in self._blocks:
                    self._blocks[bname].scheduled = flags[0]
                    self._blocks[bname].functional = flags[1]
                    self._blocks[bname].queue = flags[2]
                else:
                    logger.info("Block %s is no longer defined" % bname)
       
        self.update_relatives()
        # initiate the process before starting any threads
        thread.start_new_thread(self.update_block_state, tuple())
        self.lock = threading.Lock()
        self.statistics = Statistics()

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def _get_node_card(self, name, state):
        if not self.node_card_cache.has_key(name):
            self.node_card_cache[name] = NodeCard(name, state)
            
        return self.node_card_cache[name]

    def _new_block_dict(self, block_def, bp_cache={}):
        

        '''This is bridge-tastic.

        '''
        blockcomment = '''
        NODES_PER_NODECARD = 32

        node_list = []

        if partition_def.small:
            bp_name = partition_def.base_partitions[0].id
            for nc in partition_def._node_cards:
                node_list.append(self._get_node_card(bp_name + "-" + nc.id, nc.state))
        else:
            try:
                for bp in partition_def.base_partitions:
                    if bp.id not in bp_cache:
                        bp_cache[bp.id] = []
                        for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                            bp_cache[bp.id].append(self._get_node_card(bp.id + "-" + nc.id, nc.state))
                    node_list += bp_cache[bp.id]
            except BridgeException:
                print "Error communicating with the bridge during initial config.  Terminating."
                sys.exit(1)

        d = dict(
            name = partition_def.id,
            queue = "default",
            size = NODES_PER_NODECARD * len(node_list),
            node_cards = node_list,
            switches = [ s.id for s in partition_def.switches ],
            state = _get_state(partition_def),
        )
        return d
        '''
        pass


    def _detect_wiring_deps(self, block, wiring_cache={}):
        """Detect dependencies on shared links.  This will probably get rolled 
        into a general resource intersection check.

        """
        #TODO: Add once we have a bridge
        return 
 
    def configure (self, bridgeless=True, config_file=None):
        
        """Read partition data from the bridge, ultimately.  Until then we're working from an XML file.
        
        """
           
        if config_file == None and bridgeless:
            raise RuntimeError("config file for bridgeless operation not specified.")
        
        def _get_node_card(name):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name)
                
            return self.node_card_cache[name]

            
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
                node_card_list.append(_get_node_card(nc.get("id")))
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
            blocks_cleanup.append(p)
            _set_block_cleanup_state(p)
            p.reserved_until = False
            p.reserved_by = None
            p.used_by = None

        def _set_block_cleanup_state(b):
            #will have to set this in the final component, for now just go through the motions
            #If nothing else, we're still blocked.
            b.state = "cleanup"
            #block.state = "blocked (%s)" % (p.name,)
        
        while True:
            self._blocks_lock.acquire()
            # first, set all of the nodecards to not busy
            for nc in self.node_card_cache.values():
                nc.used_by = ''

            try:
                for p in self._blocks.values():
                    p._update_node_cards()
                
                now = time.time()
            
                # since we don't have the bridge, a partition which isn't busy
                # should be set to idle and then blocked states can be derived
                for p in self._blocks.values():
                    if p.admin_failed:
                        p.state ="admin failed"
                        for rel in p._relatives:
                            rel.state = "admin failed relative"


                    if p.state != "busy":
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
            Cobalt.Util.sleep(10)

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
                block.state = "cleanup"            
                block.reserved_until = False
                block.reserved_by = None
                block.used_by = None


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
                    pgroup.forker = 'bg_mpirun_forker'
                if self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime), pgroup.jobid):
                    try:
                        pgroup.start()
                        if pgroup.head_pid == None:
                            self.logger.error("%s: process group failed to start using the %s component; releasing resources",
                                pgroup.label, pgroup.forker)
                            self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
                            pgroup.exit_status = 255
                    except (ComponentLookupError, xmlrpclib.Fault), e:
                        self.logger.error("%s: failed to contact the %s component", pgroup.label, pgroup.forker)
                        # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
                        # until the job has exhausted its maximum alloted time
                        del self.process_groups[pgroup.id]
                        raise
                    except (ComponentLookupError, xmlrpclib.Fault), e:
                        self.logger.error("%s: a fault occurred while attempting to start the process group using the %s "
                            "component", pgroup.label, pgroup.forker)
                        # do not release the resources; instead re-raise the exception and allow cqm to the opportunity to retry
                        # until the job has exhausted its maximum alloted time
                        del self.process_groups[process_group.id]
                        raise
                    except:
                        self.logger.error("%s: an unexpected exception occurred while attempting to start the process group "
                            "using the %s component; releasing resources", pgroup.label, pgroup.forker, exc_info=True)
                        self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
                        pgroup.exit_status = 255
                else:
                    self.logger.error("%s: the internal reservation on %s expired; job has been terminated", pgroup.label,
                        pgroup.location)
                    pgroup.exit_status = 255
        return process_groups
    
    add_process_groups = exposed(query(add_process_groups))
    
    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def _get_exit_status (self):
        running = []
        active_forker_components = []
        for forker_component in ['bg_mpirun_forker', 'user_script_forker']:
            try:
                running.extend(ComponentProxy(forker_component).active_list("process group"))
                active_forker_components.append(forker_component)
            except:
                self.logger.error("failed to contact %s component for list of running jobs", forker_component)

        for each in self.process_groups.itervalues():
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
