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
import errno
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
check_required_options = Cobalt.Util.check_required_options
get_config_option = Cobalt.Util.get_config_option
Timer = Cobalt.Util.Timer
from Cobalt.Components.base import Component, exposed, automatic, query
import Cobalt.bridge
from Cobalt.bridge import BridgeException
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Components.bg_base_system import NodeCard, Partition, PartitionDict, BGProcessGroupDict, BGBaseSystem, \
    JobValidationError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics
from Cobalt.DataTypes.ProcessGroup import ProcessGroup


__all__ = [
    "BGProcessGroup",
    "Simulator",
]

logger = logging.getLogger(__name__.split('.')[-1])
Cobalt.bridge.set_serial(Cobalt.bridge.systype)


class BGProcessGroup(ProcessGroup):
    """ProcessGroup modified by Blue Gene systems"""
    fields = ProcessGroup.fields + ["nodect"]

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get('nodect', None)


class BGPartition (Partition):
    def __init__(self, spec):
        Partition.__init__(self, spec)
        self.cleanup_pending = False
        self.cleanup_timer = None

    def get_state(self):
        state = {}
        state.update(Partition.get_state(self))
        state['cleanup_pending'] = self.cleanup_pending
        return state

    def restore_state(self, state):
        Partition.restore_state(self, state)
        try:
            self.cleanup_pending = state['cleanup_pending']
            if self.cleanup_pending and self.state == 'idle':
                self.state = 'cleanup'
        except KeyError:
            self.cleanup_pending = False

class BGPartitionDict (PartitionDict):
    item_cls = BGPartition


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
    update_partition_state -- update partition state from the bridge API (runs as a thread)
    """
    
    name = "system"
    implementation = __name__.split('.')[-1]

    logger = logger

    
    _configfields = ['kernel']
    mfields = check_required_options([('bgsystem', 'kernel')])
    if mfields:
        print "Missing option(s) in cobalt config file [bgsystem] section: %s" % (" ".join([f for (s,f) in mfields]))
        sys.exit(1)
    if get_config_option('bgsystem', 'kernel') in Cobalt.Util.config_true_values:
        mfields = check_required_options([('bgsystem', 'bootprofiles'), ('bgsystem', 'partitionboot')])
        if mfields:
            print "Missing option(s) in cobalt config file [bgsystem] section: %s" % (" ".join([f for (s,f) in mfields]))
            sys.exit(1)

    partition_dict_cls = BGPartitionDict

    def __init__ (self, *args, **kwargs):
        BGBaseSystem.__init__(self, *args, **kwargs)
        sys.setrecursionlimit(5000)
        self.process_groups.item_cls = BGProcessGroup
        self.node_card_cache = dict()
        self.configure()
                
        # initiate the process before starting any threads
        thread.start_new_thread(self.update_partition_state, tuple())
    
    def __getstate__(self):
        state = {}
        state.update(BGBaseSystem.__getstate__(self))
        state.update({
                'bgsystem_version':3})
        return state

    def __setstate__(self, state):
        BGBaseSystem.__setstate__(self, state)
        self.process_groups.item_cls = BGProcessGroup
        self.node_card_cache = dict()
        self.configure()
        self.update_relatives()
        self._restore_partition_state(state)

        # initiate the process before starting any threads
        thread.start_new_thread(self.update_partition_state, tuple())

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me, float(get_config_option('bgsystem', 'save_me_interval', 10)))

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
        partitions = self.partition_dict_cls()
        
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

        cleanup_timeout = get_config_option('bgsystem', 'cleanup_timeout', 30)

        def _start_partition_cleanup(p):
            self.logger.info("partition %s: marking partition for cleaning", p.name)
            p.cleanup_pending = True
            p.cleanup_timer = None
            partitions_reset_kernel.append(p)
            p.reserved_until = False
            p.reserved_by = None
            p.used_by = None

        while True:
            try:
                system_def = Cobalt.bridge.PartitionList.info_by_filter()
            except BridgeException:
                self.logger.error("Error communicating with the bridge to update partition state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
                continue # then try again
            except:
                self.logger.error("Unexpected exception", exc_info=True)
                Cobalt.Util.sleep(5) # wait a little bit...
                continue
    
            try:
                bg_object = Cobalt.bridge.BlueGene.by_serial()
                for bp in bg_object.base_partitions:
                    for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                        self.node_card_cache[bp.id + "-" + nc.id].state = nc.state
                # set all of the nodecards to not busy
                for nc in self.node_card_cache.values():
                    nc.used_by = ''
                busted_switches = []
                for s in bg_object.switches:
                    if s.state != "RM_SWITCH_UP":
                        busted_switches.append(s.id)
            except BridgeException:
                self.logger.error("Error communicating with the bridge to update nodecard state information.")
                self.bridge_in_error = True
                Cobalt.Util.sleep(5) # wait a little bit...
                continue # then try again
            except:
                self.logger.error("Unexpected exception", exc_info=True)
                Cobalt.Util.sleep(5) # wait a little bit...
                continue

            try:
                # update the state of each partition
                self._partitions_lock.acquire()
                self.bridge_in_error = False
                now = time.time()
                partitions_reset_kernel = []
                partitions_destroy = []
                partitions_cleaning = []
                bridge_partition_cache = {}
                missing_partitions = set(self._partitions.keys())
                new_partitions = []
                self.offline_partitions = []

                for partition in system_def:
                    bridge_partition_cache[partition.id] = partition
                    missing_partitions.discard(partition.id)
                    if self._partitions.has_key(partition.id):
                        p = self._partitions[partition.id]
                        p.state = _get_state(partition)
                        p._update_node_cards()
                        if p.cleanup_pending and p.used_by:
                            # if the partition has a pending cleanup request, then set the state so that cleanup will be
                            # performed
                            _start_partition_cleanup(p)
                        elif p.reserved_until and now > p.reserved_until:
                            # if the job assigned to the partition has completed, then set the state so that cleanup will be
                            # performed
                            self.logger.info("partition %s: reservation for job %s has expired; clearing reservation.",
                                p.name, p.used_by)
                            _start_partition_cleanup(p)
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
                    try:
                        bridge_p = Cobalt.bridge.Partition.by_id(partition.id)
                    except PartitionNotFound:
                        self.logger.warning("partition %s: new partition no longer exists", partition.id)
                    except:
                        self.logger.error("partition %s: failed to acquire partition info from the bridge",
                            partition.id, exc_info=True)
                    else:
                        self._partitions.q_add([self._new_partition_dict(bridge_p, bp_cache)])
                        p = self._partitions[bridge_p.id]
                        self._detect_wiring_deps(p, wiring_cache)

                # if partitions were added or removed, then update the relationships between partitions
                if len(missing_partitions) > 0 or len(new_partitions) > 0:
                    self.update_relatives()

                # if any partitions are being cleaned up, then check on the progress
                for p in self._partitions.values():
                    if p.cleanup_pending:
                        busy = []
                        parts = list(p._all_children)
                        parts.append(p)
                        for part in parts:
                            bpart = bridge_partition_cache[part.name]
                            try:
                                if bpart.state != "RM_PARTITION_FREE":
                                    busy.append(part.name)
                            except Cobalt.bridge.IncompatibleState:
                                pass
                            except:
                                self.logger.error(
                                    "partition %s: an exception occurred while attempting to destroy partition %s",
                                    p.name, part.name, exc_info=1)
                        if len(busy) > 0:
                            self.logger.info("partition %s: still cleaning busy partition(s): %s", p.name, ", ".join(busy))
                            partitions_destroy.append(p)
                            p.cleanup_timer = None
                        elif not p.cleanup_timer:
                            self.logger.info("partition %s: cleanup entering wait mode", p.name)
                            p.cleanup_timer = Timer(cleanup_timeout)
                            p.cleanup_timer.start()
                        elif not p.cleanup_timer.has_expired:
                            self.logger.info("partition %s: cleanup in wait mode for %s more seconds",
                                p.name, cleanup_timeout - p.cleanup_timer.elapsed_time)
                        else:
                            p.cleanup_pending = False
                            p.cleanup_timer = None
                            self.logger.info("partition %s: cleaning complete", p.name)

                # determine and set the state for each of the partitions
                for p in self._partitions.values():
                    if p.state != 'idle':
                        continue

                    if p.cleanup_pending:
                        p.state = 'cleanup'
                        continue

                    for part_name in self.failed_partitions:
                        try:
                            part = self._partitions[part_name]
                        except KeyError:
                            pass
                        else:
                            if p == part:
                                p.state = "failed diags"
                                break
                            elif p in part._parents or p in part._children:
                                p.state = "blocked (%s)" % (part.name,)
                                break
                    if p.state != 'idle':
                        continue

                    for nc in p.node_cards:
                        if nc.state != "RM_NODECARD_UP":
                            p.state = "hardware offline: nodecard %s" % nc.id
                            self.offline_partitions.append(p.name)
                            break
                        elif nc.used_by:
                            if self.partition_really_busy(p, nc):
                                p.state = "blocked (%s)" % nc.used_by
                                break
                    if p.state != 'idle':
                        continue

                    for s in p.switches:
                        if s in busted_switches:
                            p.state = "hardware offline: switch %s" % s 
                            self.offline_partitions.append(p.name)
                            break
                    if p.state != 'idle':
                        continue

                    for dep_name in p._wiring_conflicts:
                        if self._partitions[dep_name].state == "busy" or p.used_by or p.cleanup_pending:
                            p.state = "blocked-wiring (%s)" % dep_name
                            break
                    if p.state != 'idle':
                        continue

                    if p.reserved_until:
                        p.state = "allocated"
                        continue

                    allocated = None
                    cleaning = None
                    for part in p._parents.union(p._children):
                        if part.reserved_until:
                            allocated = part
                        if part.cleanup_pending:
                            cleaning = part
                    if cleaning:
                        if bridge_partition_cache[part.name].state == "RM_PARTITION_FREE":
                            p.state = "blocked (%s)" % (cleaning.name,)
                        else:
                            p.state = 'cleanup'
                    elif allocated:
                        p.state = "blocked (%s)" % (allocated.name,)
            except:
                self.logger.error("error in update_partition_state", exc_info=True)
                try:
                    for p in self._partitions.values():
                        if p.state == 'idle':
                            p.state = "blocked (update error)"
                except:
                    # the partitions may have incorrect states so we set bridge_in_error to prevent resource assignment
                    self.bridge_in_error = True

            self._partitions_lock.release()

            # cleanup partitions and set their kernels back to the default (while _not_ holding the lock)
            for p in partitions_reset_kernel:
                try:
                    self._clear_kernel(p.name)
                    self.logger.info("partition %s: kernel settings cleared", p.name)
                except:
                    self.logger.error("partition %s: failed to clear kernel settings", p.name)

            try:
                pnames_cleaned = []
                for p in partitions_destroy:
                    pnames_destroyed = []
                    parts = list(p._all_children)
                    parts.append(p)
                    for part in parts:
                        pnames_cleaned.append(part.name)
                        bpart = bridge_partition_cache[part.name]
                        try:
                            if bpart.state in ["RM_PARTITION_READY", "RM_PARTITION_ERROR"]:
                                self.logger.debug("partition %s: state=%s; issuing partition destroy", part.name, bpart.state)
                                bpart.destroy()
                                pnames_destroyed.append(part.name)
                        except Cobalt.bridge.IncompatibleState:
                            pass
                        except:
                            self.logger.info("partition %s: an exception occurred while attempting to destroy partition %s",
                                p.name, part.name, exc_info=1)
                    if len(pnames_destroyed) > 0:
                        self.logger.info("partition %s: partition destruction initiated for %s",
                            p.name, ", ".join(pnames_destroyed))
                try:
                    job_filter = Cobalt.bridge.JobFilter()
                    job_filter.job_type = Cobalt.bridge.JOB_TYPE_ALL_FLAG
                    jobs = Cobalt.bridge.JobList.by_filter(job_filter)
                except BridgeException:
                    self.logger.error("Error communicating with the bridge to obtain job information.")
                else:
                    for job in jobs:
                        if job.partition_id in pnames_cleaned:
                            try:
                                job.cancel()
                                self.logger.info("partition %s: task %d canceled", job.partition_id, job.db_id)
                            except (Cobalt.bridge.IncompatibleState, Cobalt.bridge.JobNotFound):
                                pass
                            except:
                                self.logger.error("partition %s: unexpected exception while canceling task %d",
                                    job.partition_id, job.db_id, exc_info=True)
            except:
                self.logger.error("error in update_partition_state", exc_info=True)

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
        if get_config_option('bgsystem', 'kernel', 'false').lower() not in Cobalt.Util.config_true_values:
            return True
        kernel_dir = "%s/%s" % (os.path.expandvars(get_config_option('bgsystem', 'bootprofiles')), kernel)
        return os.path.exists(kernel_dir)

    def _set_kernel(self, partition, kernel):
        '''Set the kernel to be used by jobs run on the specified partition'''
        if get_config_option('bgsystem', 'kernel', 'false') not in Cobalt.Util.config_true_values:
            if kernel != "default":
                raise Exception("custom kernel capabilities disabled")
            return
        partition_link = "%s/%s" % (os.path.expandvars(get_config_option('bgsystem', 'partitionboot')), partition)
        kernel_dir = "%s/%s" % (os.path.expandvars(get_config_option('bgsystem', 'bootprofiles')), kernel)
        try:
            current = os.readlink(partition_link)
        except OSError, e:
            if e.errno == errno.ENOENT:
                self.logger.warning("partition %s: partitionboot location %s does not exist; creating link",
                    partition, partition_link)
                current = None
            elif e.errno == errno.EINVAL:
                self.logger.warning("partition %s: partitionboot location %s is not a symlink; removing and resetting",
                    partition, partition_link)
                current = None
            else:
                self.logger.warning("partition %s: failed to read partitionboot location %s: %s",
                    partition, partition_link, e.strerror)
                raise
        if current != kernel_dir:
            if not self._validate_kernel(kernel):
                self.logger.error("partition %s: kernel directory \"%s\" does not exist", partition, kernel_dir)
                raise Exception("kernel directory \"%s\" does not exist" % (kernel_dir,))
            if current:
                self.logger.info("partition %s: updating boot image; currently set to \"%s\"", partition, current.split('/')[-1])
            try:
                try:
                    os.unlink(partition_link)
                except OSError, e:
                    if e.errno != errno.ENOENT:
                        self.logger.error("partition %s: unable to unlink \"%s\": %s", partition, partition_link, e.strerror)
                        raise
                try:
                    os.symlink(kernel_dir, partition_link)
                except OSError, e:
                    self.logger.error("partition %s: failed to reset boot location \"%s\" to \"%s\": %s" %
                        (partition, partition_link, kernel_dir, e.strerror))
                    raise
            except OSError:
                raise Exception("failed to reset boot location for partition", partition)
            self.logger.info("partition %s: boot image updated; now set to \"%s\"", partition, kernel)

    def _clear_kernel(self, partition):
        '''Set the kernel to be used by a partition to the default value'''
        if get_config_option('bgsystem', 'kernel', 'false') in Cobalt.Util.config_true_values:
            try:
                self._set_kernel(partition, "default")
            except:
                logger.error("partition %s: failed to reset boot location", partition)
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
    
    def validate_job(self, spec):
        """
        validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        spec = BGBaseSystem.validate_job(self, spec)
        if not self._validate_kernel(spec['kernel']):
            raise JobValidationError("kernel does not exist")
        return spec
    validate_job = exposed(validate_job)
