"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- virtual process group running on the system
Simulator -- simulated system component
"""

import pwd
from sets import Set as set
import logging
import sys
import os
import operator
import random
import time
import thread
import threading
import sets
import xmlrpclib
from datetime import datetime
from ConfigParser import ConfigParser

try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree

import Cobalt
import Cobalt.Data
from Cobalt.Components import bg_base_system
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Components.bg_base_system import NodeCard, Partition, PartitionDict, ProcessGroupDict, BGBaseSystem
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics


__all__ = [
    "ProcessGroup", 
    "Simulator",
]

logger = logging.getLogger(__name__)




class ProcessGroup (bg_base_system.ProcessGroup):
    def __init__(self, spec):
        bg_base_system.ProcessGroup.__init__(self, spec)
        self.signals = []
    
    def _get_argv (self, config_files=None):
        """Get a command string for a process group for a process group."""
        if config_files is None:
            config_files = Cobalt.CONFIG_FILES
        config = ConfigParser()
        config.read(config_files)
        
        argv = [
            config.get("bgpm", "mpirun"),
            os.path.basename(config.get("bgpm", "mpirun")),
        ]
        
        if self.true_mpi_args is not None:
            # arguments have been passed along in a special attribute.  These arguments have
            # already been modified to include the partition that cobalt has selected
            # for the process group.
            argv.extend(self.true_mpi_args)
            return argv
    
        argv.extend([
            "-np", str(self.size),
            "-mode", self.mode,
            "-cwd", self.cwd,
            "-exe", self.executable,
        ])
        
        try:
            partition = self.location[0]
        except (KeyError, IndexError):
            raise ProcessGroupCreationError("location")
        argv.extend(["-partition", partition])
        
        if self.kerneloptions:
            argv.extend(['-kernel_options', self.kerneloptions])
        
        if self.args:
            argv.extend(["-args", " ".join(self.args)])
        
        if self.env:
            env_kvstring = " ".join(["%s=%s" % (key, value) for key, value in self.env.iteritems()])
            argv.extend(["-env",  env_kvstring])
        
        return argv



class Simulator (BGBaseSystem):
    
    """Generic system simulator.
    
    Methods:
    configure -- load partitions from an xml file
    reserve_partition -- lock a partition for use by a process_group (exposed)
    release_partition -- release a locked (busy) partition (exposed)
    add_process_groups -- add (start) a process group on the system (exposed, query)
    get_process_groups -- retrieve process groups (exposed, query)
    wait_process_groups -- get process groups that have exited, and remove them from the system (exposed, query)
    signal_process_groups -- send a signal to the head process of the specified process groups (exposed, query)
    update_partition_state -- simulates updating partition state from the bridge API (automatic)
    """
    
    name = "system"
    implementation = "simulator"
    
    logger = logger

    def __init__ (self, *args, **kwargs):
        BGBaseSystem.__init__(self, *args, **kwargs)
        self.process_groups.item_cls = ProcessGroup
        self.config_file = kwargs.get("config_file", None)
        self.failed_components = sets.Set()
        if self.config_file is not None:
            self.configure(self.config_file)
    
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
        return {'managed_partitions':self._managed_partitions, 'version':2, 'config_file':self.config_file, 'partition_flags': flags}
    
    def __setstate__(self, state):
        self._managed_partitions = state['managed_partitions']
        self.config_file = state['config_file']
        self._partitions = PartitionDict()
        self.process_groups = ProcessGroupDict()
        self.process_groups.item_cls = ProcessGroup
        self.node_card_cache = dict()
        self._partitions_lock = thread.allocate_lock()
        self.failed_components = sets.Set()
        self.pending_diags = dict()
        self.failed_diags = list()
        if self.config_file is not None:
            self.configure(self.config_file)

        if 'partition_flags' in state:
            for pname, flags in state['partition_flags'].items():
                if pname in self._partitions:
                    self._partitions[pname].scheduled = flags[0]
                    self._partitions[pname].functional = flags[1]
                    self._partitions[pname].queue = flags[2]
                else:
                    logger.info("Partition %s is no longer defined" % pname)

        self.update_relatives()
        self.lock = threading.Lock()
        self.statistics = Statistics()
        
    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)


    def configure (self, config_file):
        
        """Configure simulated partitions.
        
        Arguments:
        config_file -- xml configuration file
        """
        
        def _get_node_card(name):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name)
                
            return self.node_card_cache[name]
            
            
        self.logger.info("configure()")
        try:
            system_doc = ElementTree.parse(config_file)
        except IOError:
            self.logger.error("unable to open file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)
        except:
            self.logger.error("problem loading data from file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)
            
        system_def = system_doc.getroot()
        if system_def.tag != "BG":
            self.logger.error("unexpected root element in %r: %r" % (config_file, system_def.tag))
            self.logger.error("exiting...")
            sys.exit(1)
        
        # that 32 is not really constant -- it needs to either be read from cobalt.conf or from the bridge API
        NODES_PER_NODECARD = 32
                
        # initialize a new partition dict with all partitions
        #
        partitions = PartitionDict()
        
        tmp_list = []

        # this is going to hold partition objects from the bridge (not our own Partition)
        wiring_cache = {}
        bp_cache = {}
        
        for partition_def in system_def.getiterator("Partition"):
            node_list = []
            switch_list = []
            
            for nc in partition_def.getiterator("NodeCard"): 
                node_list.append(_get_node_card(nc.get("id")))

            nc_count = len(node_list)
            
            if not wiring_cache.has_key(nc_count):
                wiring_cache[nc_count] = []
            wiring_cache[nc_count].append(partition_def.get("name"))

            for s in partition_def.getiterator("Switch"):
                switch_list.append(s.get("id"))

            tmp_list.append( dict(
                name = partition_def.get("name"),
                queue = partition_def.get("queue", "default"),
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                switches = switch_list,
                state = "idle",
            ))
        
        partitions.q_add(tmp_list)
        
        # find the wiring deps
        for size in wiring_cache:
            for p in wiring_cache[size]:
                p = partitions[p]
                s1 = sets.Set( p.switches )
                for other in wiring_cache[size]:
                    other = partitions[other]
                    if (p.name == other.name):
                        continue

                    s2 = sets.Set( other.switches )
                    
                    if s1.intersection(s2):
                        print "found a wiring dep between %s and %s" % (p.name, other.name)
                        partitions[p.name]._wiring_conflicts.add(other.name)
        
            
        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)

    
    def reserve_partition (self, name, size=None):
        """Reserve a partition and block all related partitions.
        
        Arguments:
        name -- name of the partition to reserve
        size -- size of the process group reserving the partition (optional)
        """
        
        try:
            partition = self.partitions[name]
        except KeyError:
            self.logger.error("reserve_partition(%r, %r) [does not exist]" % (name, size))
            return False
        if partition.state != "starting job":
            self.logger.error("reserve_partition(%r, %r) [%s]" % (name, size, partition.state))
            return False
        if not partition.functional:
            self.logger.error("reserve_partition(%r, %r) [not functional]" % (name, size))
        if size is not None and size > partition.size:
            self.logger.error("reserve_partition(%r, %r) [size mismatch]" % (name, size))
            return False

        self._partitions_lock.acquire()
        try:
            partition.state = "busy"
            partition.reserved_until = False
        except:
            self.logger.error("error in reserve_partition", exc_info=True)
        self._partitions_lock.release()
        # explicitly call this, since the above "busy" is instantaneously available
        self.update_partition_state()
        
        self.logger.info("reserve_partition(%r, %r)" % (name, size))
        return True
    reserve_partition = exposed(reserve_partition)
    
    def release_partition (self, name):
        """Release a reserved partition.
        
        Arguments:
        name -- name of the partition to release
        """
        try:
            partition = self.partitions[name]
        except KeyError:
            self.logger.error("release_partition(%r) [already free]" % (name))
            return False
        if not partition.state == "busy":
            self.logger.info("release_partition(%r) [not busy]" % (name))
            return False
                
        self._partitions_lock.acquire()
        try:
            partition.state = "idle"
        except:
            self.logger.error("error in release_partition", exc_info=True)
        self._partitions_lock.release()
        
        # explicitly unblock the blocked partitions
        self.update_partition_state()

        self.logger.info("release_partition(%r)" % (name))
        return True
    release_partition = exposed(release_partition)
    
    def add_process_groups (self, specs):
        
        """Create a simulated process group.
        
        Arguments:
        spec -- dictionary hash specifying a process group to start
        """
        
        self.logger.info("add_process_groups(%r)" % (specs))
        
        script_specs = []
        other_specs = []
        for spec in specs:
            if spec['mode'] == "script":
                script_specs.append(spec)
            else:
                other_specs.append(spec)
        
        # start up script jobs
        new_pgroups = []
        if script_specs:
            try:
                for spec in script_specs:
                    script_pgroup = ComponentProxy("script-manager").add_jobs([spec])
                    self.reserve_partition_until(spec['location'][0], time.time() + 60*float(spec['walltime']))
                    new_pgroup = self.process_groups.q_add([spec])
                    new_pgroup[0].script_id = script_pgroup[0]['id']
                    new_pgroups.append(new_pgroup[0])
            except (ComponentLookupError, xmlrpclib.Fault):
                raise ProcessGroupCreationError("system::add_process_groups failed to communicate with script-manager")

        process_groups = self.process_groups.q_add(other_specs)
        for process_group in process_groups:
            self.start(process_group)
            
        return new_pgroups + process_groups
    add_process_groups = exposed(query(all_fields=True)(add_process_groups))
    
    def get_process_groups (self, specs):
        """Query process_groups from the simulator."""
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def wait_process_groups (self, specs):
        """get process groups that have finished running."""
        self.logger.info("wait_process_groups(%r)" % (specs))
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            del self.process_groups[process_group.id]
        return process_groups
    wait_process_groups = exposed(query(wait_process_groups))
    
    def signal_process_groups (self, specs, signame="SIGINT"):
        """Simulate the signaling of a process_group."""
        self.logger.info("signal_process_groups(%r, %r)" % (specs, signame))
        process_groups = self.process_groups.q_get(specs)
        for process_group in process_groups:
            if process_group.mode == "script":
                try:
                    pgroup = ComponentProxy("script-manager").signal_jobs([{'id':process_group.script_id}], "SIGTERM")
                except (ComponentLookupError, xmlrpclib.Fault):
                    logger.error("Failed to communicate with script manager when killing job")
            else:
                process_group.signals.append(signame)
        return process_groups
    signal_process_groups = exposed(query(signal_process_groups))
    
    def start (self, process_group):
        thread.start_new_thread(self._mpirun, (process_group, ))
    
    def _mpirun (self, process_group):
        argv = process_group._get_argv()
        stdout = open(process_group.stdout or "/dev/null", "a")
        stderr = open(process_group.stderr or "/dev/null", "a")
        
        try:
            cobalt_log_file = open(process_group.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(argv[1:])
            cobalt_log_file.close()
        except:
            logger.error("Job %s/%s:  unable to open cobaltlog file %s" % (process_group.id, process_group.user, process_group.cobalt_log_file))
        
        try:
            partition = argv[argv.index("-partition") + 1]
        except ValueError:
            print >> stderr, "ERROR: '-partition' is a required flag"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        except IndexError:
            print >> stderr, "ERROR: '-partition' requires a value"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        
        try:
            mode = argv[argv.index("-mode") + 1]
        except ValueError:
            print >> stderr, "ERROR: '-mode' is a required flag"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        except IndexError:
            print >> stderr, "ERROR: '-mode' requires a value"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        
        try:
            size = argv[argv.index("-np") + 1]
        except ValueError:
            print >> stderr, "ERROR: '-np' is a required flag"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        except IndexError:
            print >> stderr, "ERROR: '-np' requires a value"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        try:
            size = int(size)
        except ValueError:
            print >> stderr, "ERROR: '-np' got invalid value %r" % (size)
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
        
        print >> stdout, "ENVIRONMENT"
        print >> stdout, "-----------"
        for key, value in process_group.env.iteritems():
            print >> stdout, "%s=%s" % (key, value)
        print >> stdout
        
        print >> stderr, "FE_MPI (Info) : Initializing MPIRUN"
        reserved = self.reserve_partition(partition, size)
        if not reserved:
            print >> stderr, "BE_MPI (ERROR): Failed to run process on partition"
            print >> stderr, "BE_MPI (Info) : BE completed"
            print >> stderr, "FE_MPI (ERROR): Failure list:"
            print >> stderr, "FE_MPI (ERROR): - 1. ProcessGroup execution failed - unable to reserve partition", partition
            print >> stderr, "FE_MPI (Info) : FE completed"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        
        
        hardware_failure = False
        for nc in self.partitions[partition].node_cards:
            if nc.id in self.failed_components:
                hardware_failure = True
                break
        for switch in self.partitions[partition].switches:
            if switch in self.failed_components:
                hardware_failure = True
                break

        if hardware_failure:
            excuses = ["incorrectly polarized packet accelerator", "the Internet is full", "side fumbling detected", "unilateral phase detractors offline", ]
            print >> stderr, "BE_MPI (ERROR): Booting aborted - partition is in DEALLOCATING ('D') state"
            print >> stderr, "BE_MPI (ERROR): Partition has not reached the READY ('I') state"
            print >> stderr, "BE_MPI (Info) : Checking for block error text:"
            print >> stderr, "BE_MPI (ERROR): block error text '%s.'" % random.choice(excuses)
            print >> stderr, "BE_MPI (Info) : Starting cleanup sequence"
            time.sleep(20)
            self.release_partition(partition)
            print >> stderr, "BE_MPI (Info) : Partition", partition, "switched to state FREE ('F')"
            print >> stderr, "FE_MPI (ERROR): Failure list:"
            print >> stderr, "FE_MPI (ERROR): - 1.", partition, "couldn't boot."
            print >> stderr, "FE_MPI (Info) : FE completed"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return


        
        print >> stderr, "FE_MPI (Info) : process group with id", process_group.id
        print >> stderr, "FE_MPI (Info) : Waiting for process_group to terminate"
        
        print >> stdout, "Running process_group: %s" % " ".join(argv)
        
        start_time = time.time()
        run_time = random.randint(60, 180)
        my_exit_status = 0
         
        print "running for about %f seconds" % run_time
        while time.time() < (start_time + run_time):
            if "SIGKILL" in process_group.signals:
                process_group.exit_status = 1
                return
            elif "SIGTERM" in process_group.signals:
                print >> stderr, "FE_MPI (Info) : ProcessGroup got signal SIGTERM"
                my_exit_status = 1
                break
            else:
                time.sleep(1) # tumblers better than pumpers
        
        print >> stderr, "FE_MPI (Info) : ProcessGroup", process_group.id, "switched to state TERMINATED ('T')"
        print >> stderr, "FE_MPI (Info) : ProcessGroup sucessfully terminated"
        print >> stderr, "BE_MPI (Info) : Releasing partition", partition
        released = self.release_partition(partition)
        if not released:
            print >> stderr, "BE_MPI (ERROR): Partition", partition, "could not switch to state FREE ('F')"
            print >> stderr, "BE_MPI (Info) : BE completed"
            print >> stderr, "FE_MPI (Info) : FE completed"
            print >> stderr, "FE_MPI (Info) : Exit status: 1"
            process_group.exit_status = 1
            return
        print >> stderr, "BE_MPI (Info) : Partition", partition, "switched to state FREE ('F')"
        print >> stderr, "BE_MPI (Info) : BE completed"
        print >> stderr, "FE_MPI (Info) : FE completed"
        print >> stderr, "FE_MPI (Info) : Exit status:", my_exit_status
        
        process_group.exit_status = my_exit_status
    
    
    def update_partition_state(self):
        # first, set all of the nodecards to not busy
        for nc in self.node_card_cache.values():
            nc.used_by = ''

        self._partitions_lock.acquire()
        try:
            for p in self._partitions.values():
                p._update_node_cards()
                
            now = time.time()
            
            # since we don't have the bridge, a partition which isn't busy
            # should be set to idle and then blocked states can be derived
            for p in self._partitions.values():
                if p.state != "busy":
                    p.state = "idle"
                    
            for p in self._partitions.values():
                if p.state != "busy":
                    if p.reserved_until:
                        p.state = "starting job"
                        for part in p._parents:
                            if part.state == "idle":
                                part.state = "blocked by starting job"
                        for part in p._children:
                            if part.state == "idle":
                                part.state = "blocked by starting job"
                    for diag_part in self.pending_diags:
                        if p.name == diag_part.name or p.name in diag_part.parents or p.name in diag_part.children:
                            p.state = "blocked by pending diags"
                    for nc in p.node_cards:
                        if nc.used_by:
                            p.state = "blocked (%s)" % nc.used_by
                            break
                    for dep_name in p._wiring_conflicts:
                        if self._partitions[dep_name].state == "busy":
                            p.state = "blocked-wiring (%s)" % dep_name
                            break
                    for part_name in self.failed_diags:
                        part = self._partitions[part_name]
                        if p.name == part.name:
                            p.state = "failed diags"
                        elif p.name in part.parents or p.name in part.children:
                            p.state = "blocked by failed diags"
                else:
                    p.reserved_until = False
    
                if p.reserved_until:
                    if now > p.reserved_until:
                        p.reserved_until = False
        except:
            self.logger.error("error in update_partition_state", exc_info=True)
        
        self._partitions_lock.release()
    update_partition_state = automatic(update_partition_state)

    def add_failed_components(self, component_names):
        success = []
        for name in component_names:
            if self.node_card_cache.has_key(name):
                self.failed_components.add(name)
                success.append(name)
            else:
                for p in self._partitions.values():
                    if name in p.switches:
                        self.failed_components.add(name)
                        success.append(name)
                        break
        return success
    add_failed_component = exposed(add_failed_components)
    
    def del_failed_components(self, component_names):
        success = []
        for name in component_names:
            try:
                self.failed_components.remove(name)
                success.append(name)
            except KeyError:
                pass
            
        return success
    del_failed_components = exposed(del_failed_components)
    
    def list_failed_components(self, component_names):
        return list(self.failed_components)
    list_failed_components = exposed(list_failed_components)
    
    def launch_diags(self, partition, test_name):
        exit_value = 0
        for nc in partition.node_cards:
            if nc.id in self.failed_components:
                exit_value = 1
        for switch in partition.switches:
            if switch in self.failed_components:
                exit_value = 2

        self.finish_diags(partition, test_name, exit_value)
