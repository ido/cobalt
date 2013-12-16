"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- a group of processes started with mpirun
BGSystem -- Blue Gene system component
"""

import logging
import sys
import os
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

    logger = logger

    def __init__(self, spec):
        spec['forker'] = "user_script_forker"
        ProcessGroup.__init__(self, spec)
        self.nodefile = ""
        self.label = "%s/%s/%s" %(self.jobid, self.user, self.id)
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
        cmd_args = ['--nf', str(self.nodefile),
                    '--jobid', str(self.jobid),
                    '--cwd', str(self.cwd),]

        qsub_env_list = ["%s=%s" % (key, val) for key, val in self.env.iteritems()]
        for env in qsub_env_list:
            cmd_args.extend(['--env', env])
        cmd_args.append(self.executable)

        logger.debug("sim mode: %s", sim_mode)
        cmd_exe = None
        if sim_mode:
            logger.debug("We are setting up with simulation mode.")
            cmd_exe = get_cluster_system_config("simulation_executable", None)
            if None == cmd_exe:
                logger.critical("Job: %s/%s: Executable for simulator not specified! This job will not run!")
                raise RuntimeError("Unspecified simulation_executable in cobalt config")
        else:
            cmd_exe = get_cluster_system_config('launcher','/usr/bin/cobalt-launcher.py')

        #run the user script off the login node, and on the compute node
        if (get_cluster_system_config("run_remote", 'true').lower() in config_true_values and not sim_mode):
            cmd = ("/usr/bin/ssh", rank0, cmd_exe, ) + tuple(cmd_args) + tuple(split_args)
        else:
            cmd = (cmd_exe,) + tuple(cmd_args) + tuple(split_args)

        ret["cmd" ] = cmd
        ret["args"] = cmd[1:]
        ret["executable"] = cmd[0]
        self.executable = ret["executable"]
        self.cmd = ret["cmd"]
        self.args = list(ret["args"])

        return ret

    def start(self):
        """Start the process group by contact the appropriate forker component"""
        try:
            data = self.prefork()
            self.head_pid = ComponentProxy(self.forker, retry=False).fork([self.executable] + self.args, self.tag,
                "Job %s/%s/%s" %(self.jobid, self.user, self.id), self.env, data, self.runid)
        except:
            self.logger.error("Job %s/%s/%s: problem forking; %s did not return a child id", self.jobid, self.user, self.id,
                self.forker)
            raise

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
        state.update(ClusterBaseSystem.__getstate__(self))
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
            self.logger.info("Job %s/%s: process group %s created to track script", pgroup.user, pgroup.jobid, pgroup.id)
        #System has started the job.  We need remove them from the temp, alloc array
        #in cluster_base_system.
        self.apg_started = True
        for pgroup in process_groups:
            for location in pgroup.location:
                try:
                    del self.alloc_only_nodes[location]
                except KeyError:
                    logger.critical("%s already removed from alloc_only_nodes list", location)
        return process_groups
    add_process_groups = exposed(query(add_process_groups))

    def get_process_groups (self, specs):
        self._get_exit_status()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))

    def _get_exit_status (self):
        children = {}
        cleanup = {}
        for forker in ['user_script_forker']:
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
                clean_partition = False
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
                        clean_partition = True
                else:
                    if pg.exit_status is None:
                        # the forker has lost the child for our process group
                        self.logger.info("%s: job exited with unknown status", pg.label)
                        # FIXME: should we use a negative number instead to indicate internal errors? --brt
                        pg.exit_status = 1234567
                        clean_partition = True
                if clean_partition:
                    pass
                    #self.reserve_resources_until(pg.location, None, pg.jobid)
                    #self._mark_partition_for_cleaning(pg.location[0], pg.jobid)

        # check for children that no longer have a process group associated
        # with them and add them to the cleanup list.  This might have
        # happpened if a previous cleanup attempt failed and the process group
        # has already been waited upon
        for forker, child_id in children.keys():
            if children[(forker, child_id)]['pg'] is None:
                cleanup[forker].append(child['id'])

        # cleanup any children that have completed and been processed
        for forker in cleanup.keys():
            if len(cleanup[forker]) > 0:
                try:
                    ComponentProxy(forker).cleanup_children(cleanup[forker])
                except ComponentLookupError:
                    self.logger.error("failed to contact the %s component to cleanup children", forker)
                except:
                    self.logger.error("unexpected exception while requesting that the %s component perform cleanup",
                        forker, exc_info=True)
    _get_exit_status = automatic(_get_exit_status,
            float(get_cluster_system_config('get_exit_status_interval', 10)))

    def wait_process_groups (self, specs):
        self._get_exit_status()
        process_groups = [pg for pg in self.process_groups.q_get(specs) if pg.exit_status is not None]
        for process_group in process_groups:
            self.clean_nodes(process_group.location, process_group.user, process_group.jobid)
        return process_groups
    wait_process_groups = locking(exposed(query(wait_process_groups)))

    def signal_process_groups (self, specs, signame="SIGINT"):
        my_process_groups = self.process_groups.q_get(specs)
        for pg in my_process_groups:
            if pg.exit_status is None:
                try:
                    ComponentProxy(pg.forker).signal(pg.head_pid, signame)
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
            return
