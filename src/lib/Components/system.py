"""Hardware abstraction layer for the system on which jobs are run.

Classes:
Partition -- atomic set of nodes
PartitionDict -- default container for partitions
Job -- virtual job running on the system
JobDict -- default container for jobs
Simulator -- simulated system component

Exceptions:
JobCreationError -- error when creating a job
"""

import pwd
import sets
import logging
import sys
import os
import operator
import random
import time
import thread
from datetime import datetime
from ConfigParser import ConfigParser

import lxml
import lxml.etree

import Cobalt
import Cobalt.Data
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query

__all__ = [
    "JobCreationError",
    "Partition", "PartitionDict",
    "Job", "JobDict",
    "Simulator",
]

logger = logging.getLogger(__name__)


class JobCreationError (Exception):
    """An error occured when creation a job."""

class ExitEarlyError (Exception):
    """simulate a goto!!!"""

class Partition (Data):
    
    """An atomic set of nodes.
    
    Partitions can be reserved to run jobs on.
    
    Attributes:
    tag -- partition
    scheduled -- ? (default False)
    name -- canonical name
    functional -- the partition is available for reservations
    queue -- ?
    parents -- super(containing)-partitions
    children -- sub-partitions
    size -- number of nodes in the partition
    
    Properties:
    state -- "idle", "busy", or "blocked"
    """
    
    fields = Data.fields.copy()
    fields.update(dict(
        tag = "partition",
        scheduled = False,
        name = None,
        functional = False,
        queue = "default",
        size = None,
        parents = None,
        children = None,
        state = None,
    ))
    
    def __init__ (self, *args, **kwargs):
        """Initialize a new partition."""
        self._parents = sets.Set()
        self._children = sets.Set()
        self._busy = False
        Data.__init__(self, *args, **kwargs)
    
    def _get_parents (self):
        return [parent.name for parent in self._parents]
    
    def _set_parents (self, value):
        pass
    
    parents = property(_get_parents, _set_parents)
    
    def _get_children (self):
        return [child.name for child in self._children]
    
    def _set_children (self):
        pass
    
    children = property(_get_children, _set_children)
    
    def __str__ (self):
        return self.name
    
    def __repr__ (self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)
    
    def _get_state (self):
        for partition in self._parents | self._children:
            if partition._busy:
                return "blocked"
        if self._busy:
            return "busy"
        return "idle"
    
    def _set_state (self, value):
        if self.state == "blocked":
            raise ValueError("blocked")
        if value == "idle":
            self._busy = False
        elif value == "busy":
            self._busy = True
        else:
            raise ValueError(value)
    
    state = property(_get_state, _set_state)
    

class PartitionDict (DataDict):
    
    """Default container for partitions.
    
    Keyed by partition name.
    """
    
    item_cls = Partition
    key = "name"


class Job (Cobalt.Data.Job):
    
    """An extension of a cobalt job.
    
    Attributes:
    uid -- user id of the running process
    gid -- group id of the running process
    cmd -- commandline executed
    pid -- process id
    """
    
    id_gen = IncrID()
    
    def __init__ (self, *args, **kwargs):
        self.uid = None
        self.gid = None
        self.cmd = None
        self.pid = self.id_gen.next()
        Data.__init__(self, *args, **kwargs)


class JobDict (DataDict):
    
    """Default container for jobs.
    
    Keyed by job id.
    """
    
    item_cls = Job
    key = "id"


class Simulator (Component):
    
    """Generic system simulator.
    
    Methods:
    configure -- load partitions from an xml file
    get_state -- db2-like description of partition state (exposed)
    get_partitions -- retrieve partitions in the simulator (exposed, query)
    reserve_partition -- lock a partition for use by a job (exposed)
    release_partition -- release a locked (busy) partition (exposed)
    add_jobs -- add (start) a job on the system (exposed, ~query)
    get_jobs -- retrieve running jobs (exposed, query)
    del_jobs -- delete jobs (exposed, query)
    run_jobs -- run all jobs (automatic)
    mpirun -- produce mpirun-like output
    """
    
    name = "system"
    implementation = "simulator"
    
    logger = logger

    def __init__ (self, *args, **kwargs):
        """Initialize a system simulator."""
        Component.__init__(self, *args, **kwargs)
        self._partitions = PartitionDict()
        self._managed_partitions = sets.Set()
        self.jobs = JobDict()
        config_file = kwargs.get("config_file", None)
        if config_file is not None:
            self.configure(config_file)
    
    def _get_partitions (self):
        return PartitionDict([
            (partition.name, partition) for partition in self._partitions.itervalues()
            if partition.name in self._managed_partitions
        ])
    
    partitions = property(_get_partitions)
    
    def configure (self, config_file):
        
        """Configure simulated partitions.
        
        Arguments:
        config_file -- xml configuration file
        """
        
        self.logger.info("configure()")
        system_doc = lxml.etree.parse(config_file)
        system_def = system_doc.getroot()
        
        # initialize a new partition dict with all partitions
        partitions = PartitionDict()
        partitions.q_add([
            dict(
                name = partition_def.get("name"),
                queue = "default",
                scheduled = True,
                functional = True,
                size = partition_def.get("size"),
            )
            for partition_def in system_def.getiterator("Partition")
        ])
        
        # parent/child relationships
        for partition_def in system_def.getiterator("Partition"):
            partition = partitions[partition_def.get("name")]
            partition._children.update([
                partitions[child_def.get("name")]
                for child_def in partition_def.getiterator("Partition")
                if child_def.get("name") != partition.name
            ])
            for child in partition._children:
                child._parents.add(partition)
        
        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)
    
    def get_state (self):
        """Retrieve db2-like status list.
        
        Status form:
        [('partition0','I'), ('partition1', 'F'), ...]
        
        I -- partition is in use
        F -- partition is free
        """
        self.logger.info("get_state()")
        busy_partitions = self.partitions.q_get([{'state':"busy"}])
        return [
            (partition.name, partition in busy_partitions and 'I' or 'F')
            for partition in self.partitions
        ]
    get_state = exposed(get_state)
    
    def add_partitions (self, specs):
        self.logger.info("add_partitions(%r)" % (specs))
        specs = [{'name':spec.get("name")} for spec in specs]
        partitions = [
            partition for partition in self._partitions.q_get(specs)
            if partition.name not in self._managed_partitions
        ]
        self._managed_partitions.update([
            partition.name for partition in partitions
        ])
        return partitions
    add_partition = exposed(query(add_partitions))
    
    def get_partitions (self, specs):
        """Query partitions on simulator."""
        self.logger.info("get_partitions(%r)" % (specs))
        return self.partitions.q_get(specs)
    get_partitions = exposed(query(get_partitions))
    
    def del_partitions (self, specs):
        self.logger.info("del_partitions(%r)" % (specs))
        partitions = [
            partition for partition in self._partitions.q_get(specs)
            if partition.name in self._managed_partitions
        ]
        self._managed_partitions -= [partition.name for partition in partitions]
        return partitions
    del_partitions = exposed(query(del_partitions))
    
    def set_partitions (self, specs, updates):
        def _set_partitions(part, newattr):
            part.update(newattr)
        return self._partitions.q_get(specs, _set_partitions, updates)
    set_partitions = exposed(query(set_partitions))
    
    def reserve_partition (self, name, size=None):
        """Reserve a partition and block all related partitions.
        
        Arguments:
        name -- name of the partition to reserve
        size -- size of the job reserving the partition (optional)
        """
        try:
            partition = self.partitions[name]
        except KeyError:
            self.logger.error("reserve_partition(%r, %r) [does not exist]" % (name, size))
            return False
        if partition.state != "idle":
            self.logger.error("reserve_partition(%r, %r) [%s]" % (name, size, partition.state))
            return False
        if not partition.functional:
            self.logger.error("reserve_partition(%r, %r) [not functional]" % (name, size))
        if size is not None and size > partition.size:
            self.logger.error("reserve_partition(%r, %r) [size mismatch]" % (name, size))
            return False
        partition.state = "busy"
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
        partition.state = "idle"
        self.logger.info("release_partition(%r)")
        return True
    release_partition = exposed(release_partition)
    
    def _get_owner (self, spec):
        """Get intended uid, gid for a job from a job spec."""
        user_name = spec.get("user", None)
        if not user_name:
            raise JobCreationError("user")
        try:
            uid, gid = pwd.getpwnam(user_name)[2:4]
        except KeyError:
            raise JobCreationError("user")
        return (uid, gid)
    
    def _get_env (self, spec, config_files=None):
        """Get intended environment dict for a job from a job spec."""
        if config_files is None:
            config_files = Cobalt.CONFIG_FILES
        config = ConfigParser()
        config.read(config_files)
        env = dict()
        env["DB_PROPERTY"] = config.get("bgpm", "db2_properties")
        env["BRIDGE_CONFIG_FILE"] = config.get("bgpm", "bridge_config")
        env["MMCS_SERVER_IP"] = config.get("bgpm", "mmcs_server_ip")
        env["DB2INSTANCE"] = config.get("bgpm", "db2_instance")
        env["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
        env["COBALT_JOBID"] = spec['id']
        return env
    
    def _get_cmd (self, spec, config_files=None):
        """Get a command string for a job from a job spec."""
        if config_files is None:
            config_files = Cobalt.CONFIG_FILES
        config = ConfigParser()
        config.read(config_files)
        
        argv = [
            config.get("bgpm", "mpirun"),
            os.path.basename(config.get("bgpm", "mpirun")),
        ]
        
        if "true_mpi_args" in spec and spec['true_mpi_args'] is not None:
            # arguments have been passed along in a special attribute.  These arguments have
            # already been modified to include the partition that cobalt has selected
            # for the job.
            argv.extend(spec['true_mpi_args'])
            return " ".join(argv)
    
        argv.extend([
            "-np", str(spec['size']),
            "-mode", spec.get("mode", None) or "co",
            "-cwd", spec['cwd'],
            "-exe", spec['executable'],
        ])
        
        try:
            partition = spec["location"][0]
        except (KeyError, IndexError):
            raise JobCreationError("location")
        argv.extend(["-partition", partition])
        
        kerneloptions = spec.get("kerneloptions", None)
        if kerneloptions:
            argv.extend(['-kernel_options', kerneloptions])
        
        args = spec.get('args', [])
        if args:
            argv.extend(["-args", " ".join(args)])
        
        envs = spec.get("envs", None)
        if envs:
            env_kvstring = " ".join(["%s=%s" % (key, value) for key, value in envs.iteritems()])
            argv.extend(["-env",  env_kvstring])
        
        if "BGLMPI_MAPPING" in (spec.get("env", None) or {}):
            # strip out BGLMPI_MAPPING until mpirun bug is fixed
            mapfile = spec['env']['BGLMPI_MAPPING']
            del spec['env']['BGLMPI_MAPPING']
            argv.extend(["-mapfile", mapfile])
        return " ".join(argv)
    
    def add_jobs (self, specs):
        
        """Create a simulated job.
        
        Arguments:
        spec -- dictionary hash specifying a job to start
        """
        
        self.logger.info("add_jobs(%r)" % (specs))
        def jobspec (spec):
            uid, gid = self._get_owner(spec)
            jobspec = dict(
                id = spec.get("id"),
                stdin = spec.get("stdin", "/dev/null"),
                stdout = spec.get("stdout", "/dev/null"),
                stderr = spec.get("stderr", "/dev/null"),
                uid = uid,
                gid = gid,
                env = self._get_env(spec),
                cmd = self._get_cmd(spec),
                walltime = spec.get("walltime", '1'),
            )
            if not jobspec['walltime']:
                jobspec['walltime'] = '1'
            return jobspec
        
        jobspecs = [jobspec(spec) for spec in specs]
        new_jobs = self.jobs.q_add(jobspecs)
        for job in new_jobs:
            stdout = open(job.stdout, "a")
            stderr = open(job.stderr, "a")
            env = os.environ.copy()
            env.update(job.env)
            thread.start_new_thread(self.mpirun, (job.cmd.split(), ), {'stdout':stdout, 'stderr':stderr, 'env':env, 'walltime':int(job.walltime)})
            
        return new_jobs
    add_jobs = exposed(query(all_fields=True)(add_jobs))
    
    def get_jobs (self, specs):
        """Query jobs running on the simulator."""
        self.logger.info("get_jobs(%r)" % (specs))
        return self.jobs.q_get(specs)
    get_jobs = exposed(query(get_jobs))
    
    def del_jobs (self, specs):
        """Delete jobs running on the simulator."""
        self.logger.info("del_jobs(%r)" % (specs))
        return self.jobs.q_del(specs)
    del_jobs = exposed(query(del_jobs))
    
    def signal_jobs (self, specs, signame="SIGINT"):
        """Simulate the signaling of a job."""
        self.logger.info("signal_jobs(%r, %r)" % (specs, signame))
        if signame == "SIGKILL":
            return self.del_jobs(specs)
        else:
            return self.get_jobs(specs)
    signal_jobs = exposed(query(signal_jobs))
    
    def mpirun (self, argv, **kwargs):
        
        """Produce appropriate output on stdout, stderr for a job.
        
        Arguments:
        argv -- argv for the command to run (command.split())
        
        Keyword arguments:
        stdin -- file to read from as stdin (not used)
        stdout -- file to write to as stdout
        stderr -- file to write to as stderr
        environ -- environment dictionary for job
        
        stdin, stdout, stderr expect file-like objects (not file names)
        """
        
        stdin = kwargs.get("stdin", sys.stdin)
        stdout = kwargs.get("stdout", sys.stdout)
        stderr = kwargs.get("stderr", sys.stderr)
        environ = kwargs.get("env", {})
        
        try:
            try:
                partition = argv[argv.index("-partition") + 1]
            except ValueError:
                print >> stderr, "ERROR: '-partition' is a required flag"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            except IndexError:
                print >> stderr, "ERROR: '-partition' requires a value"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            
            try:
                mode = argv[argv.index("-mode") + 1]
            except ValueError:
                print >> stderr, "ERROR: '-mode' is a required flag"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            except IndexError:
                print >> stderr, "ERROR: '-mode' requires a value"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            
            try:
                size = argv[argv.index("-np") + 1]
            except ValueError:
                print >> stderr, "ERROR: '-np' is a required flag"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            except IndexError:
                print >> stderr, "ERROR: '-np' requires a value"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            try:
                size = int(size)
            except ValueError:
                print >> stderr, "ERROR: '-np' got invalid value %r" % (size)
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
            
            print >> stdout, "ENVIRONMENT"
            print >> stdout, "-----------"
            for key, value in environ.iteritems():
                print >> stdout, "%s=%s" % (key, value)
            print >> stdout
            
            print >> stderr, "FE_MPI (Info) : Initializing MPIRUN"
            try:
                jobid = environ["COBALT_JOBID"]
            except KeyError:
                print >> stderr, "FE_MPI (Info) : COBALT_JOBID not found"
                print >> stderr, "FE_MPI (Info) : Exit status:   1"
                raise ExitEarlyError
            bjobid = int(jobid) + 1024
            reserved = self.reserve_partition(partition, size)
            if not reserved:
                print >> stderr, "BE_MPI (ERROR): Failed to run process on partition"
                print >> stderr, "BE_MPI (Info) : BE completed"
                print >> stderr, "FE_MPI (ERROR): Failure list:"
                print >> stderr, "FE_MPI (ERROR): - 1. Job execution failed - unable to reserve partition", partition
                print >> stderr, "FE_MPI (Info) : FE completed"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            print >> stderr, "FE_MPI (Info) : Adding job"
            print >> stderr, "FE_MPI (Info) : Job added with id", bjobid
            print >> stderr, "FE_MPI (Info) : Waiting for job to terminate"
            
            print >> stdout, "Running job with args:", argv
            
            start_time = time.time()
            run_time = 0.7 * 60 * kwargs.get("walltime", 1)
            print "running for about %f seconds" % run_time
            while True:
                if time.time() > (start_time + run_time):
                    print >> stderr, "FE_MPI (Info) : Job", bjobid, "switched to state TERMINATED ('T')"
                    print >> stderr, "FE_MPI (Info) : Job sucessfully terminated"
                    break
                elif jobid not in [job.id for job in self.jobs.itervalues()]:
                    print >> stderr, "FE_MPI (Info) : Job", bjobid, "switched to state TERMINATED ('T')"
                    print >> stderr, "FE_MPI (Info) : Job killed before finished"
                    break
                time.sleep(5)
                
            print >> stderr, "BE_MPI (Info) : Releasing partition", partition
            released = self.release_partition(partition)
            if not released:
                print >> stderr, "BE_MPI (ERROR): Partition", partition, "could not switch to state FREE ('F')"
                print >> stderr, "BE_MPI (Info) : BE completed"
                print >> stderr, "FE_MPI (Info) : FE completed"
                print >> stderr, "FE_MPI (Info) : Exit status: 1"
                raise ExitEarlyError
            print >> stderr, "BE_MPI (Info) : Partition", partition, "switched to state FREE ('F')"
            print >> stderr, "BE_MPI (Info) : BE completed"
            print >> stderr, "FE_MPI (Info) : FE completed"
            print >> stderr, "FE_MPI (Info) : Exit status: 0"

        except ExitEarlyError:
            # yay goto!!!
            pass
        
        self.jobs.q_del([{'id':jobid}])
