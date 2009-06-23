"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- a group of processes started with mpirun
BGSystem -- Blue Gene system component
"""

import atexit
import pwd
import grp
import sets
import logging
import sys
import os
import signal
import tempfile
import time
import thread
import ConfigParser
import tempfile
import subprocess
try:
    set = set
except NameError:
    from sets import Set as set

import Cobalt
import Cobalt.Data
from Cobalt.Components import cluster_base_system
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Exceptions import ProcessGroupCreationError
from Cobalt.Components.cluster_base_system import ProcessGroupDict, ClusterBaseSystem


__all__ = [
    "ProcessGroup",
    "Simulator",
]

logger = logging.getLogger(__name__)

class ProcessGroup (cluster_base_system.ProcessGroup):
    _configfields = ['prologue', 'epilogue', 'epilogue_timeout', 'epi_epilogue']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('cluster_system'):
        print '''"cluster_system" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['cluster_system']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file [cluster_system] section: %s" % (" ".join(mfields))
        sys.exit(1)

    
    def __init__(self, spec):
        cluster_base_system.ProcessGroup.__init__(self, spec)
        self.nodefile = ""
        self.start()
    
    def _mpirun (self):
        # create the nodefile
        self.nodefile = "/var/tmp/cobalt.%s" % self.jobid
        fd = open(self.nodefile, "w")
        for host in self.location:
            fd.write(host + "\n")
        fd.close()

        #check for valid user/group
        try:
            tmp_data = pwd.getpwnam(self.user)
            userid = tmp_data.pw_uid
            groupid = tmp_data.pw_gid
        except KeyError:
            raise ProcessGroupCreationError("error getting uid/gid")

        group_name = grp.getgrgid(groupid)[0]
        
        # run the prologue, while still root
        for host in self.location:
            h = host.split(":")[0]
            try:
                os.system("scp %s %s:/var/tmp" % (self.nodefile, h))
            except:
                logger.error("Job %s/%s failed to copy nodefile %s to host %s" % (self.jobid, self.user, self.nodefile, h))
            try:
                os.system("ssh %s %s %s %s %s" % (h, self.config.get("prologue"), self.jobid, self.user, group_name))
            except:
                logger.error("Job %s/%s failed to run prologue on host %s" % (self.jobid, self.user, h))

        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            logger.error("failed to change userid/groupid for process group %s" % (self.id))
            os._exit(1)

        try:
            os.umask(self.umask)
        except:
            logger.error("Failed to set umask to %s" % self.umask)

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

        rank0 = self.location[0].split(":")[0]
        cmd_string = "/usr/bin/cobalt-launcher.py --nf %s --jobid %s --cwd %s --exe %s" % (self.nodefile, self.jobid, self.cwd, self.executable)
        cmd = ("/usr/bin/ssh", "/usr/bin/ssh", rank0, cmd_string)
        
        # If this mpirun command originated from a user script, its arguments
        # have been passed along in a special attribute.  These arguments have
        # already been modified to include the partition that cobalt has selected
        # for the job, and can just replace the arguments built above.
        if self.true_mpi_args:
            cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun'])) + tuple(self.true_mpi_args)
    
        try:
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
            cobalt_log_file.close()
        except:
            logger.error("Job %s/%s:  unable to open cobaltlog file %s" % \
                         (self.id, self.user, self.cobalt_log_file))

        os.execl(*cmd)
    
    def start (self):
        
        """Start the process group.
        
        Fork for mpirun.
        """

        child_pid = os.fork()
        if not child_pid:
            try:
                self._mpirun()
            except:
                logger.error("unable to start mpirun", exc_info=1)
                os._exit(1)
        else:
            self.head_pid = child_pid



class ClusterSystem (ClusterBaseSystem):
    
    """cluster system component.
    
    Methods:
    configure -- load partitions from the bridge API
    add_process_groups -- add (start) an mpirun process on the system (exposed, ~query)
    get_process_groups -- retrieve mpirun processes (exposed, query)
    wait_process_groups -- get process groups that have exited, and remove them from the system (exposed, query)
    signal_process_groups -- send a signal to the head process of the specified process groups (exposed, query)
    update_partition_state -- update partition state from the bridge API (runs as a thread)
    """
    
    name = "system"
    implementation = "cluster_system"
    
    logger = logger

    
    def __init__ (self, *args, **kwargs):
        ClusterBaseSystem.__init__(self, *args, **kwargs)
        self.process_groups.item_cls = ProcessGroup

        
    
    def add_process_groups (self, specs):
        
        """Create a process group.
        
        Arguments:
        spec -- dictionary hash specifying a process group to start
        """
        
        return self.process_groups.q_add(specs)
    
    add_process_groups = exposed(query(add_process_groups))
    
    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def _get_exit_status (self):
        for each in self.process_groups.itervalues():
            try:
                pid, status = os.waitpid(each.head_pid, os.WNOHANG)
            except OSError: # the child has terminated
                continue

            # if the child has terminated
            if each.head_pid == pid:
                status = status >> 8
                each.exit_status = status
                self.logger.info("pg %i exited with status %i" % (each.id, status))
                    
    _get_exit_status = automatic(_get_exit_status)
    
    def wait_process_groups (self, specs):
        self._get_exit_status()
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            thread.start_new_thread(self.clean_nodes, (process_group,))
        return process_groups
    wait_process_groups = locking(exposed(query(wait_process_groups)))
    
    def signal_process_groups (self, specs, signame="SIGINT"):
        my_process_groups = self.process_groups.q_get(specs)
        for pg in my_process_groups:
            try:
                os.kill(int(pg.head_pid), getattr(signal, signame))
            except OSError, e:
                self.logger.error("signal failure for process group %s: %s" % (pg.id, e))
        return my_process_groups
    signal_process_groups = exposed(query(signal_process_groups))

    def clean_nodes(self, pg):
        try:
            tmp_data = pwd.getpwnam(pg.user)
            groupid = tmp_data.pw_gid
            group_name = grp.getgrgid(groupid)[0]
        except KeyError:
            group_name = ""
            self.logger.error("Job %s/%s unable to determine group name for epilogue" % (pg.jobid, pg.user))
 
        processes = []
        for host in pg.location:
            h = host.split(":")[0]
            try:
                p = subprocess.Popen(["/usr/bin/ssh", h, pg.config.get("epilogue"), str(pg.jobid), pg.user, group_name])
                p.host = h
                processes.append(p)
            except:
                self.logger.error("Job %s/%s failed to run epilogue on host %s" % (pg.jobid, pg.user, h))
        
        start = time.time()
        dirty_nodes = []
        while True:
            running = False
            for p in processes:
                if p.poll() is None:
                    running = True
                    break
            
            if not running:
                break
            
            if time.time() - start > float(pg.config.get("epilogue_timeout")):
                for p in processes:
                    if p.poll() is None:
                        try:
                            os.kill(p.pid, signal.SIGTERM)
                            dirty_nodes.append(p.host)
                            self.logger.error("Job %s/%s epilogue timed out on host %s" % (pg.jobid, pg.user, p.host))
                        except:
                            self.logger.error("epilogue for %s already terminated" %p.host)
                break
            else:
                time.sleep(5)
            
            
        self.lock.acquire()
        try:
            for host in pg.location:
                self.running_nodes.discard(host)
                self.logger.error("freeing %s" % host)
            
            if dirty_nodes:    
                for host in dirty_nodes:
                    self.down_nodes.add(host)
                p = subprocess.Popen([pg.config.get("epi_epilogue"), str(pg.jobid), pg.user, group_name] + dirty_nodes)
            
            del self.process_groups[pg.id]
        except:
            self.logger.error("error in clean_nodes", exc_info=True)
        self.lock.release()
        