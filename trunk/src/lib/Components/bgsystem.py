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
import signal
import tempfile
import time
import thread
import threading
import xmlrpclib
import ConfigParser

import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Components.base import Component, exposed, automatic, query
import Cobalt.bridge
from Cobalt.bridge import BridgeException
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Components.bg_base_system import NodeCard, PartitionDict, BGProcessGroupDict, BGBaseSystem, JobValidationError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics
from Cobalt.DataTypes.ProcessGroup import ProcessGroup


__all__ = [
    "BGProcessGroup",
    "Simulator",
]

logger = logging.getLogger(__name__)
Cobalt.bridge.set_serial(Cobalt.bridge.systype)


class BGProcessGroup(ProcessGroup):
    """ProcessGroup modified by Blue Gene systems"""
    fields = ProcessGroup.fields + ["nodect"]

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get('nodect', None)

    
# convenience function used several times below
def _get_state(bridge_partition):
    if bridge_partition.state == "RM_PARTITION_FREE":
        return "idle"
    else:
        return "busy"
 

class BGSystem (BGBaseSystem):
    
    """Blue Gene system component.
    
    Methods:
    configure -- load partitions from the bridge API
    add_process_groups -- add (start) an mpirun process on the system (exposed, ~query)
    get_process_groups -- retrieve mpirun processes (exposed, query)
    wait_process_groups -- get process groups that have exited, and remove them from the system (exposed, query)
    signal_process_groups -- send a signal to the head process of the specified process groups (exposed, query)
    update_partition_state -- update partition state from the bridge API (runs as a thread)
    """
    
    name = "system"
    implementation = "bgsystem"
    
    logger = logger

    
    _configfields = ['diag_script_location', 'diag_log_file', 'kernel']
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgsystem'):
        print '''"bgsystem" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['bgsystem']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file [bgsystem] section: %s" % (" ".join(mfields))
        sys.exit(1)
    if config.get('kernel') == "true":
        _kernel_configfields = ['bootprofiles', 'partitionboot']
        mfields = [field for field in _kernel_configfields if not config.has_key(field)]
        if mfields:
            print "Missing option(s) in cobalt config file [bgsystem] section: %s" % (" ".join(mfields))
            sys.exit(1)

    def __init__ (self, *args, **kwargs):
        BGBaseSystem.__init__(self, *args, **kwargs)
        sys.setrecursionlimit(5000)
        self.process_groups.item_cls = BGProcessGroup
        self.diag_pids = dict()
        self.configure()
                
        # initiate the process before starting any threads
        thread.start_new_thread(self.update_partition_state, tuple())
    
    def __getstate__(self):
        flags = {}
        for part in self._partitions.values():
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
        return {'managed_partitions':self._managed_partitions, 'version':2,
                'partition_flags': flags, 'next_pg_id':self.process_groups.id_gen.idnum+1}
    
    def __setstate__(self, state):
        sys.setrecursionlimit(5000)
        Cobalt.Util.fix_set(state)
        self._managed_partitions = state['managed_partitions']
        self._partitions = PartitionDict()
        self.process_groups = BGProcessGroupDict()
        self.process_groups.item_cls = BGProcessGroup
        if state.has_key("next_pg_id"):
            self.process_groups.id_gen.set(state['next_pg_id'])
        self.node_card_cache = dict()
        self._partitions_lock = thread.allocate_lock()
        self.pending_diags = dict()
        self.failed_diags = list()
        self.diag_pids = dict()
        self.pending_script_waits = set()
        self.bridge_in_error = False
        self.cached_partitions = None
        self.offline_partitions = []

        self.configure()
        if 'partition_flags' in state:
            for pname, flags in state['partition_flags'].items():
                if pname in self._partitions:
                    self._partitions[pname].scheduled = flags[0]
                    self._partitions[pname].functional = flags[1]
                    self._partitions[pname].queue = flags[2]
                else:
                    logger.info("Partition %s is no longer defined" % pname)
        
        self.update_relatives()
        # initiate the process before starting any threads
        thread.start_new_thread(self.update_partition_state, tuple())
        self.lock = threading.Lock()
        self.statistics = Statistics()

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def _get_node_card(self, name, state):
        if not self.node_card_cache.has_key(name):
            self.node_card_cache[name] = NodeCard(name, state)
            
        return self.node_card_cache[name]

    def _new_partition_dict(self, partition_def, bp_cache={}):
        # that 32 is not really constant -- it needs to either be read from cobalt.conf or from the bridge API -- replaced for now by config file check.
        #NODES_PER_NODECARD = 32
        #we're going to get this from the bridge.  I think we can get the 
        #size of the target partition and eliminate this.
        

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
            size = partition_def.partition_size, #self.NODES_PER_NODECARD * len(node_list),
            node_cards = node_list,
            switches = [ s.id for s in partition_def.switches ],
            state = _get_state(partition_def),
        )
        return d


    def _detect_wiring_deps(self, partition, wiring_cache={}):
        def _kernel():
            s2 = set(p.switches)

            if s1.intersection(s2):
                p._wiring_conflicts.add(partition.name)
                partition._wiring_conflicts.add(p.name)
                self.logger.debug("%s and %s havening problems (wiring conflict)" % (partition.name, p.name))

        s1 = set(partition.switches)

        if wiring_cache.has_key(partition.size):
            for p in wiring_cache[partition.size]:
                if partition.name!=p.name:
                    _kernel()
        else:
            wiring_cache[partition.size] = [partition]
            for p in self._partitions.values():
                if p.size==partition.size and partition.name!=p.name:
                    wiring_cache[partition.size].append(p)
                    _kernel()

 
    def configure (self):
        
        """Read partition data from the bridge."""
        
        self.logger.info("configure()")
        try:
            system_def = Cobalt.bridge.PartitionList.by_filter()
        except BridgeException:
            print "Error communicating with the bridge during initial config.  Terminating."
            sys.exit(1)

                
        # initialize a new partition dict with all partitions
        #
        partitions = PartitionDict()
        
        tmp_list = []

        wiring_cache = {}
        bp_cache = {}
        
        for partition_def in system_def:
            tmp_list.append(self._new_partition_dict(partition_def, bp_cache))
        
        partitions.q_add(tmp_list)

        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)

        # find the wiring deps
        start = time.time()
        for p in self._partitions.values():
            self._detect_wiring_deps(p, wiring_cache)

        end = time.time()
        self.logger.info("took %f seconds to find wiring deps" % (end - start))
 
        # update state information
        for p in self._partitions.values():
            if p.state != "busy":
                for nc in p.node_cards:
                    if nc.used_by:
                        if self.partition_really_busy(p, nc):
                            p.state = "blocked (%s)" % nc.used_by
                            break
                for dep_name in p._wiring_conflicts:
                    if self._partitions[dep_name].state == "busy":
                        p.state = "blocked-wiring (%s)" % dep_name
                        break
        
    def partition_really_busy(self, part, nc):
        '''Check to see if a 16-node partiton is really busy, or it just
        it's neighbor is using the nodecard.

        True if really busy, else False
        '''
        if part.size != 16: #Everything else is a full nodecard
            return True
        really_busy = False
        for nc in part.node_cards:
            #break out information and see if this is in-use by a sibling.
            #get the size of the nc.used_by partition, if it's used by something 32 or larger then we really are busy
            if self._partitions[nc.used_by].size > 16:
                really_busy = True
                break
            if nc.used_by:
                try:
                    rack, midplane, nodecard = Cobalt.Components.bg_base_system.parse_nodecard_location(nc.used_by)
                except RuntimeError:
                    #This isn't in use by a nodecard-level partition, so yeah, this is busy.
                    really_busy = True
                    break
                if (int(rack) != nc.rack 
                        or int(midplane) != nc.midplane 
                        or int(nodecard) != nc.nodecard):
                    really_busy = True
                    break
        return really_busy

  
    def update_partition_state(self):
        """Use the quicker bridge method that doesn't return nodecard information to update the states of the partitions"""
        
        def _start_partition_cleanup(p):
            self.logger.info("partition %s: marking partition for cleaning", p.name)
            p.cleanup_pending = True
            partitions_cleanup.append(p)
            _set_partition_cleanup_state(p)
            p.reserved_until = False
            p.reserved_by = None
            p.used_by = None

        def _set_partition_cleanup_state(p):
            p.state = "cleanup"
            for part in p._children:
                if bridge_partition_cache[part.name].state == "RM_PARTITION_FREE":
                    part.state = "blocked (%s)" % (p.name,)
                else:
                    part.state = "cleanup"
            for part in p._parents:
                if part.state == "idle":
                    part.state = "blocked (%s)" % (p.name,)

        while True:
            try:
                system_def = Cobalt.bridge.PartitionList.info_by_filter()
            except BridgeException:
                self.logger.error("Error communicating with the bridge to update partition state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
                continue # then try again
    
            try:
                bg_object = Cobalt.bridge.BlueGene.by_serial()
                for bp in bg_object.base_partitions:
                    for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                        self.node_card_cache[bp.id + "-" + nc.id].state = nc.state
            except:
                self.logger.error("Error communicating with the bridge to update nodecard state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
                continue # then try again

            self.bridge_in_error = False
            busted_switches = []
            for s in bg_object.switches:
                if s.state != "RM_SWITCH_UP":
                    busted_switches.append(s.id)

            # set all of the nodecards to not busy
            for nc in self.node_card_cache.values():
                nc.used_by = ''

            # update the state of each partition
            self._partitions_lock.acquire()
            now = time.time()
            partitions_cleanup = []
            bridge_partition_cache = {}
            self.offline_partitions = []
            missing_partitions = set(self._partitions.keys())
            new_partitions = []
            try:
                for partition in system_def:
                    bridge_partition_cache[partition.id] = partition
                    missing_partitions.discard(partition.id)
                    if self._partitions.has_key(partition.id):
                        p = self._partitions[partition.id]
                        p.state = _get_state(partition)
                        p._update_node_cards()
                        if p.reserved_until and now > p.reserved_until:
                            p.reserved_until = False
                            p.reserved_by = None
                    else:
                        new_partitions.append(partition)


                # remove the missing partitions and their wiring relations
                for pname in missing_partitions:
                    self.logger.info("missing partition removed: %s", pname)
                    p = self._partitions[pname]
                    for dep_name in p._wiring_conflicts:
                        self.logger.debug("removing wiring dependency from: %s", dep_name)
                        self._partitions[dep_name]._wiring_conflicts.discard(p.name)
                    if p.name in self._managed_partitions:
                        self._managed_partitions.discard(p.name)
                    del self._partitions[p.name]

                bp_cache = {}
                wiring_cache = {}
                # throttle the adding of new partitions so updating of
                # machine state doesn't get bogged down
                for partition in new_partitions[:8]:
                    self.logger.info("new partition found: %s", partition.id)
                    bridge_p = Cobalt.bridge.Partition.by_id(partition.id)
                    self._partitions.q_add([self._new_partition_dict(bridge_p, bp_cache)])
                    p = self._partitions[bridge_p.id]
                    self._detect_wiring_deps(p, wiring_cache)

                # if partitions were added or removed, then update the relationships between partitions
                if len(missing_partitions) > 0 or len(new_partitions) > 0:
                    self.update_relatives()

                for p in self._partitions.values():
                    if p.cleanup_pending:
                        if p.used_by:
                            # if the partition has a pending cleanup request, then set the state so that cleanup will be
                            # performed
                            _start_partition_cleanup(p)
                        else:
                            # if the cleanup has already been initiated, then see how it's going
                            busy = []
                            parts = list(p._all_children)
                            parts.append(p)
                            for part in parts:
                                bpart = bridge_partition_cache[part.name]
                                try:
                                    if bpart.state != "RM_PARTITION_FREE":
                                        self.logger.debug(
                                            "partition %s: sub-partition %s is still busy; attempting another destroy",
                                            p.name, part.name)
                                        busy.append(part.name)
                                        bpart.destroy()
                                except Cobalt.bridge.IncompatibleState:
                                    pass
                                except:
                                    self.logger.info(
                                        "partition %s: an exception occurred while attempting to destroy partition %s",
                                        p.name, part.name, exc_info=1)
                            if len(busy) > 0:
                                _set_partition_cleanup_state(p)
                                self.logger.info("partition %s: still cleaning; busy partition(s): %s", p.name, ", ".join(busy))
                            else:
                                p.cleanup_pending = False
                                self.logger.info("partition %s: cleaning complete", p.name)
                    if p.state == "busy":
                        # FIXME: this should not be necessary any longer since all jobs reserve the resources. --brt

                        # when the partition becomes busy, if a script job isn't reserving it, then release the reservation
                        if not p.reserved_by:
                            p.reserved_until = False
                    elif p.state != "cleanup":
                        if p.reserved_until:
                            p.state = "allocated"
                            for part in p._parents:
                                if part.state == "idle":
                                    part.state = "blocked (%s)" % (p.name,)
                            for part in p._children:
                                if part.state == "idle":
                                    part.state = "blocked (%s)" % (p.name,)
                        elif bridge_partition_cache[p.name].state == "RM_PARTITION_FREE" and p.used_by:
                            # FIXME: should we check the partition state or use reserved by == NULL instead?  now that all jobs
                            # reserve resources, a partition without a reservation that is also in use should probably be cleaned
                            # up regardless of partition state.  --brt

                            # if the job assigned to the partition has completed, then set the state so that cleanup will be
                            # performed
                            _start_partition_cleanup(p)
                            continue
                        for diag_part in self.pending_diags:
                            if p.name == diag_part.name or p.name in diag_part.parents or p.name in diag_part.children:
                                p.state = "blocked by pending diags"
                        for nc in p.node_cards:
                            if nc.used_by:
                                if self.partition_really_busy(p, nc):
                                    p.state = "blocked (%s)" % nc.used_by
                            if nc.state != "RM_NODECARD_UP":
                                p.state = "hardware offline: nodecard %s" % nc.id
                                self.offline_partitions.append(p.name)
                        for s in p.switches:
                            if s in busted_switches:
                                p.state = "hardware offline: switch %s" % s 
                                self.offline_partitions.append(p.name)
                        for dep_name in p._wiring_conflicts:
                            if self._partitions[dep_name].state in ["busy", "allocated", "cleanup"]:
                                p.state = "blocked-wiring (%s)" % dep_name
                                break
                        for part_name in self.failed_diags:
                            part = self._partitions[part_name]
                            if p.name == part.name:
                                p.state = "failed diags"
                            elif p.name in part.parents or p.name in part.children:
                                p.state = "blocked by failed diags"
            except:
                self.logger.error("error in update_partition_state", exc_info=True)

            self._partitions_lock.release()

            # cleanup partitions and set their kernels back to the default (while _not_ holding the lock)
            pnames_cleaned = []
            for p in partitions_cleanup:
                self.logger.info("partition %s: starting partition destruction", p.name)
                pnames_destroyed = []
                parts = list(p._all_children)
                parts.append(p)
                for part in parts:
                    pnames_cleaned.append(part.name)
                    bpart = bridge_partition_cache[part.name]
                    try:
                        if bpart.state != "RM_PARTITION_FREE":
                            bpart.destroy()
                            pnames_destroyed.append(part.name)
                    except Cobalt.bridge.IncompatibleState:
                        pass
                    except:
                        self.logger.info("partition %s: an exception occurred while attempting to destroy partition %s",
                            p.name, part.name, exc_info=1)
                if len(pnames_destroyed) > 0:
                    self.logger.info("partition %s: partition destruction initiated for %s", p.name, ", ".join(pnames_destroyed))
                else:
                    self.logger.info("partition %s: no partition destruction was required", p.name)
                try:
                    self._clear_kernel(p.name)
                    self.logger.info("partition %s: kernel settings cleared", p.name)
                except:
                    self.logger.error("partition %s: failed to clear kernel settings", p.name)
            job_filter = Cobalt.bridge.JobFilter()
            job_filter.job_type = Cobalt.bridge.JOB_TYPE_ALL_FLAG
            jobs = Cobalt.bridge.JobList.by_filter(job_filter)
            for job in jobs:
                if job.partition_id in pnames_cleaned:
                    try:
                        job.cancel()
                        self.logger.info("partition %s: task %d canceled", job.partition_id, job.db_id)
                    except (Cobalt.bridge.IncompatibleState, Cobalt.bridge.JobNotFound):
                        pass

            Cobalt.Util.sleep(10)

    def _mark_partition_for_cleaning(self, pname, jobid):
        self._partitions_lock.acquire()
        try:
            p = self._partitions[pname]
            if p.used_by == jobid:
                p.cleanup_pending = True
                self.logger.info("partition %s: partition marked for cleanup", pname)
            elif p.used_by != None:
                self.logger.info("partition %s: job %s was not the current partition user (%s); partition not marked " + \
                    "for cleanup", pname, jobid, p.used_by)
        except:
            self.logger.exception("partition %s: unexpected exception while marking the partition for cleanup", pname)
        self._partitions_lock.release()

    def _validate_kernel(self, kernel):
        if self.config.get('kernel') != 'true':
            return True
        kernel_dir = "%s/%s" % (os.path.expandvars(self.config.get('bootprofiles')), kernel)
        return os.path.exists(kernel_dir)

    def _set_kernel(self, partition, kernel):
        '''Set the kernel to be used by jobs run on the specified partition'''
        if self.config.get('kernel') != 'true':
            if kernel != "default":
                raise Exception("custom kernel capabilities disabled")
            return
        partition_link = "%s/%s" % (os.path.expandvars(self.config.get('partitionboot')), partition)
        kernel_dir = "%s/%s" % (os.path.expandvars(self.config.get('bootprofiles')), kernel)
        try:
            current = os.readlink(partition_link)
        except OSError:
            self.logger.error("partition %s: failed to read partitionboot location %s" % (partition, partition_link))
            raise Exception("failed to read partitionboot location %s" % (partition_link,))
        if current != kernel_dir:
            if not self._validate_kernel(kernel):
                self.logger.error("partition %s: kernel directory \"%s\" does not exist" % (partition, kernel_dir))
                raise Exception("kernel directory \"%s\" does not exist" % (kernel_dir,))
            self.logger.info("partition %s: updating boot image; currently set to \"%s\"" % (partition, current.split('/')[-1]))
            try:
                os.unlink(partition_link)
                os.symlink(kernel_dir, partition_link)
            except OSError:
                self.logger.error("partition %s: failed to reset boot location" % (partition,))
                raise Exception("failed to reset boot location for partition" % (partition,))
            self.logger.info("partition %s: boot image updated; now set to \"%s\"" % (partition, kernel))

    def _clear_kernel(self, partition):
        '''Set the kernel to be used by a partition to the default value'''
        if self.config.get('kernel') == 'true':
            try:
                self._set_kernel(partition, "default")
            except:
                logger.error("partition %s: failed to reset boot location" % (partition,))

    def generate_xml(self):
        """This method produces an XML file describing the managed partitions, suitable for use with the simulator."""
        ret = "<BG>\n"
        ret += "<PartitionList>\n"
        for p_name in self._managed_partitions:
            p = self._partitions[p_name]

            ret += "   <Partition name='%s'>\n" % p.name
            for nc in p.node_cards:
                ret += "      <NodeCard id='%s' />\n" % nc.id
            for s in p.switches:
                ret += "      <Switch id='%s' />\n" % s
            ret += "   </Partition>\n"
        
        ret += "</PartitionList>\n"

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
            pgroup.nodect = self._partitions[pgroup.location[0]].size
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
                if self.reserve_resources_until(pgroup.location, float(pgroup.starttime) + 60*float(pgroup.walltime),
                        pgroup.jobid):
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
            self._mark_partition_for_cleaning(process_group.location[0], process_group.jobid)
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
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        spec = BGBaseSystem.validate_job(self, spec)
        if not self._validate_kernel(spec['kernel']):
            raise JobValidationError("kernel does not exist")
        return spec
    validate_job = exposed(validate_job)

    def launch_diags(self, partition, test_name):
        diag_exe = os.path.join(os.path.expandvars(self.config.get("diag_script_location")), test_name) 
        try:
            sdata = os.stat(diag_exe)
        except:
            self.logger.error("Diagnostic %s not available" % test_name)
            return
        pid = os.fork()
        if pid:
            self.diag_pids[pid] = (partition, test_name)
        else:
            try:
                stdout = open(os.path.expandvars(self.config.get("diag_log_file")) or "/dev/null", 'a')
                stdout.write("[%s] starting %s on partition %s\n" % (time.ctime(), test_name, partition))
                stdout.flush()
                os.dup2(stdout.fileno(), sys.__stdout__.fileno())
            except (IOError, OSError), e:
                logger.error("error opening diag_log_file file: %s (stdout will be lost)" % e)
            try:
                stderr = open(os.path.expandvars(self.config.get("diag_log_file")) or "/dev/null", 'a')
                os.dup2(stderr.fileno(), sys.__stderr__.fileno())
            except (IOError, OSError), e:
                logger.error("error opening diag_log_file file: %s (stderr will be lost)" % e)

            try:
                os.execl(diag_exe, diag_exe, partition.name)
            except:
                os._exit(255)
