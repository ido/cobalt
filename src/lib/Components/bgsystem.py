"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- a group of processes started with mpirun
BGSystem -- Blue Gene system component
"""

import atexit
import pwd
import sets
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
try:
    set = set
except NameError:
    from sets import Set as set

import Cobalt
import Cobalt.Data
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
    fields = ProcessGroup.fields + ["nodect", "script_id"]

    _configfields = ['mpirun']
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgpm'):
        print '''"bgpm" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['bgpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        sys.exit(1)
    
    def __init__(self, spec):
        ProcessGroup.__init__(self, spec, logger)
        self.nodect = None
        self.script_id = None
    
    def _runjob (self):
        """Runs a job"""
        #check for valid user/group
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            raise ProcessGroupCreationError("error getting uid/gid")
        
        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            logger.error("failed to change userid/groupid for process group %s" % (self.id))
            os._exit(1)

        if self.umask != None:
            try:
                os.umask(self.umask)
            except:
                logger.error("Failed to set umask to %s" % self.umask)
        try:
            partition = self.location[0]
        except IndexError:
            raise ProcessGroupCreationError("no location")

        kerneloptions = self.kerneloptions

        # export subset of MPIRUN_* variables to mpirun's environment
        # we explicitly state the ones we want since some are "dangerous"
        exportenv = [ 'MPIRUN_CONNECTION', 'MPIRUN_KERNEL_OPTIONS',
                      'MPIRUN_MAPFILE', 'MPIRUN_START_GDBSERVER',
                      'MPIRUN_LABEL', 'MPIRUN_NW', 'MPIRUN_VERBOSE',
                      'MPIRUN_ENABLE_TTY_REPORTING', 'MPIRUN_STRACE' ]
        app_envs = []
        for key, value in self.env.iteritems():
            if key in exportenv:
                os.environ[key] = value
            else:
                app_envs.append((key, value))
            
        envs = " ".join(["%s=%s" % x for x in app_envs])
        atexit._atexit = []

        stdin = open(self.stdin or "/dev/null", 'r')
        os.dup2(stdin.fileno(), sys.__stdin__.fileno())
        try:
            stdout = open(self.stdout or tempfile.mktemp(), 'a')
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
        except (IOError, OSError), e:
            logger.error("process group %s: error opening stdout file %s: %s (stdout will be lost)" % (self.id, self.stdout, e))
        try:
            stderr = open(self.stderr or tempfile.mktemp(), 'a')
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
        except (IOError, OSError), e:
            logger.error("process group %s: error opening stderr file %s: %s (stderr will be lost)" % (self.id, self.stderr, e))

        cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun']),
              '-host', self.config['mmcs_server_ip'], '-np', str(self.size),
               '-partition', partition, '-mode', self.mode, '-cwd', self.cwd,
               '-exe', self.executable)
        if self.args:
            cmd = cmd + ('-args', self.args)
        if envs:
            cmd = cmd + ('-env',  envs)
        if kerneloptions:
            cmd = cmd + ('-kernel_options', kerneloptions)
        
        # If this mpirun command originated from a user script, its arguments
        # have been passed along in a special attribute.  These arguments have
        # already been modified to include the partition that cobalt has selected
        # for the job, and can just replace the arguments built above.
        if self.true_mpi_args:
            cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun'])) + tuple(self.true_mpi_args)
    
        try:
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
            print >> cobalt_log_file, "called with environment:\n"
            for key in os.environ:
                print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
            print >> cobalt_log_file, "\n"
            cobalt_log_file.close()
        except:
            logger.error("Job %s/%s:  unable to open cobaltlog file %s" % \
                         (self.id, self.user, self.cobalt_log_file))

        os.execl(*cmd)



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
        return {'managed_partitions':self._managed_partitions, 'version':1,
                'partition_flags': flags}
    
    def __setstate__(self, state):
        sys.setrecursionlimit(5000)
        self._managed_partitions = state['managed_partitions']
        self._partitions = PartitionDict()
        self.process_groups = BGProcessGroupDict()
        self.process_groups.item_cls = BGProcessGroup
        self.node_card_cache = dict()
        self._partitions_lock = thread.allocate_lock()
        self.pending_diags = dict()
        self.failed_diags = list()
        self.diag_pids = dict()
        self.pending_script_waits = sets.Set()
        self.bridge_in_error = False
        self.cached_partitions = None

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
        thread.start_new_thread(self.update_partition_state, tuple())
        self.lock = threading.Lock()
        self.statistics = Statistics()

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def configure (self):
        
        """Read partition data from the bridge."""
        
        def _get_state(bridge_partition):
            if bridge_partition.state == "RM_PARTITION_FREE":
                return "idle"
            else:
                return "busy"
    
        def _get_node_card(name, state):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name, state)
                
            return self.node_card_cache[name]
            
        self.logger.info("configure()")
        try:
            system_def = Cobalt.bridge.PartitionList.by_filter()
        except BridgeException:
            print "Error communicating with the bridge during initial config.  Terminating."
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
        
        for partition_def in system_def:
            node_list = []
            nc_count = len(list(partition_def.node_cards))
            if not wiring_cache.has_key(nc_count):
                wiring_cache[nc_count] = []
            wiring_cache[nc_count].append(partition_def)

            if partition_def.small:
                bp_name = partition_def.base_partitions[0].id
                for nc in partition_def._node_cards:
                    node_list.append(_get_node_card(bp_name + "-" + nc.id, nc.state))
            else:
                try:
                    for bp in partition_def.base_partitions:
                        if bp.id not in bp_cache:
                            bp_cache[bp.id] = []
                            for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                                bp_cache[bp.id].append(_get_node_card(bp.id + "-" + nc.id, nc.state))
                        node_list += bp_cache[bp.id]
                except BridgeException:
                    print "Error communicating with the bridge during initial config.  Terminating."
                    sys.exit(1)

            tmp_list.append( dict(
                name = partition_def.id,
                queue = "default",
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                switches = [ s.id for s in partition_def.switches ],
                state = _get_state(partition_def),
            ))
        
        partitions.q_add(tmp_list)
        
        # find the wiring deps
        start = time.time()
        for size in wiring_cache:
            for p in wiring_cache[size]:
                s1 = sets.Set( [s.id for s in p.switches] )
                for other in wiring_cache[size]:
                    if (p.id == other.id):
                        continue

                    s2 = sets.Set( [s.id for s in other.switches] )
                    
                    if s1.intersection(s2):
                        partitions[p.id]._wiring_conflicts.add(other.id)
        
        end = time.time()
        print "took %f seconds to find wiring deps" % (end - start)
 
        # update state information
        for p in partitions.values():
            if p.state != "busy":
                for nc in p.node_cards:
                    if nc.used_by:
                        p.state = "blocked (%s)" % nc.used_by
                        break
                for dep_name in p._wiring_conflicts:
                    if partitions[dep_name].state == "busy":
                        p.state = "blocked-wiring (%s)" % dep_name
                        break
        
        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)
    
    def update_partition_state(self):
        """Use the quicker bridge method that doesn't return nodecard information to update the states of the partitions"""
        
        def _get_state(bridge_partition):
            if bridge_partition.state == "RM_PARTITION_FREE":
                return "idle"
            else:
                return "busy"

        while True:
            try:
                system_def = Cobalt.bridge.PartitionList.info_by_filter()
            except BridgeException:
                self.logger.error("Error communicating with the bridge to update partition state information.")
                self.bridge_in_error = True
                time.sleep(5) # wait a little bit...
                continue # then try again
    
            try:
                bg_object = Cobalt.bridge.BlueGene.by_serial()
                for bp in bg_object.base_partitions:
                    for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                        self.node_card_cache[bp.id + "-" + nc.id].state = nc.state
            except:
                self.logger.error("Error communicating with the bridge to update nodecard state information.")
                self.bridge_in_error = True
                time.sleep(5) # wait a little bit...
                continue # then try again

            self.bridge_in_error = False
            busted_switches = []
            for s in bg_object.switches:
                if s.state != "RM_SWITCH_UP":
                    busted_switches.append(s.id)

            # first, set all of the nodecards to not busy
            for nc in self.node_card_cache.values():
                nc.used_by = ''

            # determine which partitions just became idle...
            pnames = []
            self._partitions_lock.acquire()
            try:
                for partition in system_def:
                    if self._partitions.has_key(partition.id) and partition.id in self._managed_partitions:
                        state = _get_state(partition)
                        if self._partitions[partition.id].state in ["busy", "starting job"] and state == "idle":
                            if not self._partitions[partition.id].reserved_until:
                                pnames.append(partition.id)
            except:
                self.logger.exception("Unexpected error occurred while computing list of partitions which just became idle.")
            finally:
                self._partitions_lock.release()

            # ...and set their kernels back to the default (while _not_ holding the lock)
            for pname in pnames:
                self._clear_kernel(pname)

            # update the state of each partition
            self._partitions_lock.acquire()
            try:
                for partition in system_def:
                    if self._partitions.has_key(partition.id):
                        self._partitions[partition.id].state = _get_state(partition)
                        self._partitions[partition.id]._update_node_cards()
    
                now = time.time()
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
                            if nc.state != "RM_NODECARD_UP":
                                p.state = "hardware offline: nodecard %s" % nc.id
                                break 
                        for s in p.switches:
                            if s in busted_switches:
                                p.state = "hardware offline: switch %s" % s 
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
                        
                    # when the partition becomes busy, if a script job isn't reserving
                    # it, then release the reservation
                    else:
                        if not p.reserved_by:
                            p.reserved_until = False

                    if p.reserved_until:
                        if now > p.reserved_until:
                            p.reserved_until = False
                            p.reserved_by = None

            except:
                self.logger.error("error in update_partition_state", exc_info=True)
                        
            self._partitions_lock.release()
            
            time.sleep(10)

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

        script_specs = []
        other_specs = []
        for spec in specs:
            if spec.get('mode', False) == "script":
                script_specs.append(spec)
            else:
                other_specs.append(spec)

        # start up script jobs
        script_pgroups = []
        if script_specs:
            for spec in script_specs:
                try:
                    self._set_kernel(spec.get('location')[0], spec.get('kernel', "default"))
                except Exception, e:
                    new_pgroup = self.process_groups.q_add([spec])
                    pgroup = new_pgroup[0]
                    pgroup.nodect = self._partitions[pgroup.location[0]].size
                    pgroup.exit_status = 1
                    self.logger.info("process group %s: job %s/%s failed to set the kernel; %s", pgroup.id, pgroup.jobid, 
                        pgroup.user, e)
                else:
                    try:
                        script_pgroup = ComponentProxy("script-manager").add_jobs([spec])
                    except (ComponentLookupError, xmlrpclib.Fault):
                        self._clear_kernel(spec.get('location')[0])
                        # FIXME: jobs that were already started are not reported
                        raise ProcessGroupCreationError("system::add_process_groups failed to communicate with script-manager")
                    new_pgroup = self.process_groups.q_add([spec])
                    pgroup = new_pgroup[0]
                    pgroup.script_id = script_pgroup[0]['id']
                    pgroup.nodect = self._partitions[pgroup.location[0]].size
                    self.logger.info("job %s/%s: process group %s created to track script", pgroup.jobid, pgroup.user, pgroup.id)
                    self.reserve_resources_until(spec['location'], time.time() + 60*float(spec['walltime']), pgroup.jobid)
                    if pgroup.kernel != "default":
                        self.logger.info("process group %s: job %s/%s using kernel %s", pgroup.id, pgroup.jobid, pgroup.user, 
                            pgroup.kernel)
                    script_pgroups.append(pgroup)

        # start up non-script mode jobs
        process_groups = self.process_groups.q_add(other_specs)
        for pgroup in process_groups:
            pgroup.nodect = self._partitions[pgroup.location[0]].size
            self.logger.info("job %s/%s: process group %s created to track mpirun status", pgroup.jobid, pgroup.user, pgroup.id)
            try:
                if not pgroup.true_mpi_args:
                    self._set_kernel(pgroup.location[0], pgroup.kernel)
            except Exception, e:
                # FIXME: setting exit_status to signal the job has failed isn't really the right thing to do.  another flag
                # should be added to the process group that wait_process_group uses to determine when a process group is no
                # longer active.  an error message should also be attached to the process group so that cqm can report the
                # problem to the user.
                pgroup.exit_status = 1
                self.logger.info("process group %s: job %s/%s failed to set the kernel; %s", pgroup.id, pgroup.jobid, 
                    pgroup.user, e)
            else:
                if pgroup.kernel != "default" and not pgroup.true_mpi_args:
                    self.logger.info("process group %s: job %s/%s using kernel %s", pgroup.id, pgroup.jobid, pgroup.user,
                        pgroup.kernel)
                pgroup.start()
            
        return script_pgroups + process_groups
    
    add_process_groups = exposed(query(add_process_groups))
    
    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def _get_exit_status (self):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError: # there are no child processes
                break
            if pid == 0: # there are no zombie processes
                break
            status = status >> 8
            for each in self.process_groups.itervalues():
                if each.head_pid == pid:
                    each.exit_status = status
                    self.logger.info("process group %i: job %s/%s exited with status %i" % \
                        (each.id, each.jobid, each.user, status))
            if pid in self.diag_pids:
                part, test = self.diag_pids[pid]
                del self.diag_pids[pid]
                self.logger.info("Diagnostic %s on %s finished. rc=%d" % \
                                 (test, part.name, status))
                self.finish_diags(part, test, status)
    _get_exit_status = automatic(_get_exit_status)
    
    def wait_process_groups (self, specs):
        self._get_exit_status()
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            del self.process_groups[process_group.id]
        return process_groups
    wait_process_groups = exposed(query(wait_process_groups))
    
    def signal_process_groups (self, specs, signame="SIGINT"):
        my_process_groups = self.process_groups.q_get(specs)
        for pg in my_process_groups:
            if pg.exit_status is None:
                if pg.mode == "script":
                    try:
                        ComponentProxy("script-manager").signal_jobs([{'id':pg.script_id}], signame)
                    except (ComponentLookupError, xmlrpclib.Fault):
                        self.logger.error("Failed to communicate with script manager when killing job")
                else:
                    try:
                        os.kill(int(pg.head_pid), getattr(signal, signame))
                    except OSError, e:
                        self.logger.error("signal failure for process group %s: %s" % (pg.id, e))
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
