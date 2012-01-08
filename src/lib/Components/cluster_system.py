"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- a group of processes started with mpirun
BGSystem -- Blue Gene system component
"""

import pwd
import grp
import logging
import thread
import sys
import os
import re
import ConfigParser
import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Components.base import exposed, automatic, query, locking
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Components.cluster_base_system import ClusterBaseSystem
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from Cobalt.Proxy import ComponentProxy
from Cobalt.Util import config_true_values


__all__ = [
    "ClusterProcessGroup",
    "ClusterSystem"
]

logger = logging.getLogger(__name__)

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

if not config.has_section('cluster_system'):
    print '''"ERROR: cluster_system" section missing from cobalt config file'''
    sys.exit(1)

def get_cluster_system_config(option, default):
    try:
        value = config.get('cluster_system', option)
    except ConfigParser.NoOptionError:
        value = default
    return value



class ClusterProcessGroup(ProcessGroup):
    
    def __init__(self, spec):
        spec['forker'] = "cluster_run_forker"
        ProcessGroup.__init__(self, spec)
        self.nodefile = ""
        self.start()
        
    
    def prefork (self):
        ret = {}
        ret = ProcessGroup.prefork(self)

        sim_mode  = get_cluster_system_config("simulation_mode", 'false').lower() in config_true_values
        if not sim_mode:
            nodefile_dir = get_cluster_system_config("nodefile_dir", "/var/tmp")
            self.nodefile = os.path.join(nodefile_dir, "cobalt.%s" % self.jobid)
        else:
            self.nodefile = "fake"
        
        try:
            #This is the head node, return this to the user.
            rank0 = self.location[0].split(":")[0]
        except IndexError:
            raise ProcessGroupCreationError("no location")

        split_args = self.args
        cmd_args = ('--nf', str(self.nodefile),
                    '--jobid', str(self.jobid),
                    '--cwd', str(self.cwd),
                    '--exe', str(self.executable))
        
        cmd_exe = None
        if sim_mode: 
            logger.debug("We are setting up with simulation mode.")
            cmd_exe = get_cluster_system_config("simulation_executable", None)
            if None == cmd_exe:
                logger.critical("Job: %s/%s: Executable for simulator not specified! This job will not run!")
                raise RuntimeError("Unspecified simulation_executable in cobalt config")
        else:
            #FIXME: Need to put launcher location into config
            cmd_exe = '/usr/bin/cobalt-launcher.py' 
        
        #run the user script off the login node, and on the compute node
        if (get_cluster_system_config("run_remote", 'true').lower() in config_true_values and
                not sim_mode):
            cmd = ("/usr/bin/ssh", rank0, cmd_exe) + cmd_args + tuple(split_args)
        else:
            cmd = (cmd_exe,) + cmd_args + tuple(split_args)

        ret["cmd" ] = cmd
        ret["args"] = cmd[1:]
        ret["executable"] = cmd[0]
        self.executable = ret["executable"]
        self.cmd = ret["cmd"]
        self.args = list(ret["args"])

        return ret

    


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
        self.process_groups.item_cls = ClusterProcessGroup
        
    def __getstate__(self):
        state = {}
        state.update(Component.__getstate__(self))
        # state.update({
        #         "cluster_system_version": 1 }) 
        return state

    def __setstate__(self, state):
        ClusterBaseSystem.__setstate__(self, state)
        self.process_groups.item_cls = ClusterProcessGroup
    
    def add_process_groups (self, specs):
        """Create a process group.
        
        Arguments:
        spec -- dictionary hash specifying a process group to start
        """

        self.logger.info("add_process_groups(%r)", specs)
        process_groups = self.process_groups.q_add(specs)
        for pgroup in process_groups:
            self.logger.info("Job %s/%s: process group %s created to track script", 
                    pgroup.user, pgroup.jobid, pgroup.id)
        #System has started the job.  We need remove them from the temp, alloc array
        #in cluster_base_system.
        for pg in process_groups:
            for location in pg.location:
                del self.alloc_only_nodes[location]

        return process_groups
    add_process_groups = exposed(query(add_process_groups))
    
    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    def _get_exit_status (self, forker="cluster_run_forker"):
        try:
            running = ComponentProxy(forker).active_list("process group")
        except:
            self.logger.error("failed to contact forker component for list of running jobs")
            return

        for each in self.process_groups.itervalues():
            if each.head_pid not in running and each.exit_status is None:
                # FIXME: i bet we should consider a retry thing here -- if we fail enough times, just
                # assume the process is dead?  or maybe just say there's no exit code the first time it happens?
                # maybe the second choice is better
                try:
                    dead_dict = ComponentProxy(forker).get_status(each.head_pid)
                except Queue.Empty: #<---FIXME: What should this be?
                    self.logger.error("failed call for get_status from cluster_run_forker component for pg %s", each.head_pid)
                    return
                
                if dead_dict is None:
                    self.logger.info("Job %s/%s: process group %i: exited with unknown status", each.user, each.jobid, each.id)
                    each.exit_status = 1234567
                else:
                    each.exit_status = dead_dict["exit_status"]
                    if dead_dict["signum"] == 0:
                        self.logger.info("process group %i: job %s/%s exited with status %i", 
                            each.id, each.jobid, each.user, each.exit_status)
                    else:
                        if dead_dict["core_dump"]:
                            core_dump_str = ", core dumped"
                        else:
                            core_dump_str = ""
                        self.logger.info("process group %i: job %s/%s terminated with signal %s%s", 
                            each.id, each.jobid, each.user, dead_dict["signum"], core_dump_str)
    
    _get_exit_status = automatic(_get_exit_status)
    
    def wait_process_groups (self, specs):
        self._get_exit_status()
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            self.clean_nodes(pg.location, pg.user, pg.jobid) #FIXME: This call is a good place to look for problems
        return process_groups
    wait_process_groups = locking(exposed(query(wait_process_groups)))
   
     
    def signal_process_groups (self, specs, signame="SIGINT"):
        my_process_groups = self.process_groups.q_get(specs)
        for pg in my_process_groups:
            if pg.exit_status is None:
                try:
                    ComponentProxy(forker).signal(pg.head_pid, signame)
                except:
                    self.logger.error("Failed to communicate with forker when signalling job")

        return my_process_groups
    signal_process_groups = exposed(query(signal_process_groups))

    def del_process_groups(self, jobid):
        '''delete a process group and don't track it anymore.

           jobid -- jobid associated with the process group we are removing

        '''

        del_items = self.process_groups.q_del([{'jobid':jobid}])
        

        if del_items == []:
            self.logger.warning("Job %s: Process group not found for this jobid.", jobid)
        else:
            self.logger.info("Job %s: Process group deleted.", jobid)

