"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- virtual process group running on the system
Simulator -- simulated system component
"""

import pwd
import logging
import sys
import os
import operator
import random
import time
import thread
from datetime import datetime
from ConfigParser import ConfigParser

try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree

import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Components import cluster_base_system
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Components.cluster_base_system import ProcessGroupDict, ClusterBaseSystem
from Cobalt.Exceptions import ProcessGroupCreationError
from Cobalt.DataTypes.ProcessGroup import ProcessGroup


__all__ = [
    "ClusterProcessGroup", 
    "Simulator",
]

logger = logging.getLogger(__name__)




class ClusterProcessGroup (ProcessGroup):

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec, logger)
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



class Simulator (ClusteSystem):
    
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

    Override the ClusterSystem so that it is recognized as a simulator component.  Done right, 
    this can go away entirely.
    
    """
    
    name = "system"
    implementation = "cluster_simulator"
    
    logger = logger

    def __init__ (self, *args, **kwargs):
        ClusterBaseSystem.__init__(self, *args, **kwargs)
        self.process_groups.item_cls = ClusterProcessGroup
    
    
    def __setstate__(self, state):
        ClusterBaseSystem.__setstate__(self, state)
        self.process_groups.item_cls = ClusterProcessGroup
        
        
    def add_process_groups (self, specs):
        
        """Create a simulated process group.
        
        Arguments:
        spec -- dictionary hash specifying a process group to start
        """
        
        self.logger.info("add_process_groups(%r)" % (specs))
        process_groups = self.process_groups.q_add(specs)
        for process_group in process_groups:
            self.start(process_group)
        return  process_groups
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
            self.logger.info("finished on hosts: %s", Cobalt.Util.merge_nodelist(self.process_groups[process_group.id].location))
            for host in self.process_groups[process_group.id].location:
                self.running_nodes.discard(host)
            del self.process_groups[process_group.id]
        return process_groups
    wait_process_groups = exposed(query(wait_process_groups))
    
    def signal_process_groups (self, specs, signame="SIGINT"):
        """Simulate the signaling of a process_group."""
        self.logger.info("signal_process_groups(%r, %r)" % (specs, signame))
        process_groups = self.process_groups.q_get(specs)
        for process_group in process_groups:
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
                Cobalt.Util.sleep(1) # tumblers better than pumpers
        
        print >> stderr, "FE_MPI (Info) : ProcessGroup", process_group.id, "switched to state TERMINATED ('T')"
        print >> stderr, "FE_MPI (Info) : ProcessGroup sucessfully terminated"
        print >> stderr, "BE_MPI (Info) : Releasing partition", partition
        print >> stderr, "BE_MPI (Info) : Partition", partition, "switched to state FREE ('F')"
        print >> stderr, "BE_MPI (Info) : BE completed"
        print >> stderr, "FE_MPI (Info) : FE completed"
        print >> stderr, "FE_MPI (Info) : Exit status:", my_exit_status
        
        process_group.exit_status = my_exit_status
    
    
