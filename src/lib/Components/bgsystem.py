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

import atexit
import pwd
import sets
import logging
import sys
import os
import operator
import random
import signal
import tempfile
import time
import thread
import ConfigParser
from datetime import datetime

import Cobalt
import Cobalt.Data
from Cobalt.Data import Data, DataDict, DataList, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
import Cobalt.bridge as bgl

__all__ = [
    "JobCreationError",
    "Partition", "PartitionDict",
    "Job", "JobDict",
    "Simulator",
]

logger = logging.getLogger(__name__)
bgl.set_serial("BGL")

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
    
    fields = Data.fields + [
        "tag", "scheduled", "name", "functional",
        "queue", "size", "parents", "children", "state",
    ]
    
    def __init__ (self, spec):
        """Initialize a new partition."""
        Data.__init__(self, spec)
        spec = spec.copy()
        self.scheduled = spec.pop("scheduled", False)
        self.name = spec.pop("name", None)
        self.functional = spec.pop("functional", False)
        self.queue = spec.pop("queue", "default")
        self.size = spec.pop("size", None)
        self._parents = sets.Set()
        self._children = sets.Set()
        self._busy = False
        self.state = spec.pop("state", "idle")
        self.tag = spec.get("tag", "partition")
        
    
    def _get_parents (self):
        return [parent.name for parent in self._parents]
    
    parents = property(_get_parents)
    
    def _get_children (self):
        return [child.name for child in self._children]
    
    children = property(_get_children)
    
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
    
    def mutex(self, other_part):
        """Returns a boolean that indicates whether two partitions are mutually exclusive in their use"""
        val = bool(self.nodecards & other_part.nodecards)
        return val
    
    state = property(_get_state, _set_state)
    

class PartitionDict (DataDict):
    
    """Default container for partitions.
    
    Keyed by partition name.
    """
    
    item_cls = Partition
    key = "name"


class Job (Data):
    # read in config from cobalt.conf
    required_fields = ['user', 'executable', 'args', 'location', 'size', 'cwd']
    fields = Data.fields + [
        "system_id", "outputfile", "errorfile", "location", "user", "executable", "cwd", "size",
        "mode", "args", "inputfile", "kerneloptions", "env", "true_mpi_args", "id", "pid", 
    ]
    
    _configfields = ['mmcs_server_ip', 'db2_instance', 'bridge_config', 'mpirun', 'db2_properties', 'db2_connect']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgpm'):
        print '''"bgpm" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['bgpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1

    def __init__(self, spec):
        self.system_id = spec['system_id']
        self.outputfile = spec.get('outputfile', False)
        self.errorfile = spec.get('errorfile', False)
        self.location = spec.get('location', False)
        self.user = spec.get('user', "")
        self.executable = spec.get('executable')
        self.cwd = spec.get('cwd')
        self.size = str(spec.get('size'))
        self.mode = spec.get('mode', 'co')
        self.args = " ".join(spec.get('args', []))
        self.inputfile = spec.get('inputfile', '')
        self.kerneloptions = spec.get('kerneloptions', '')
        self.env = spec.get('env', {})
        self.true_mpi_args = spec.get('true_mpi_args')
        self.id = spec.get('id')
        self.pid = -1
        
        self.start()

    def start(self):
        '''starts a job
        daemonizes the mpirun process, passing the mpirun pid back to the
        parent process via a pipe'''

#         self.log.info("Job %s/%s: Running %s" % (spec.get('id'), spec.get('user'), " ".join(cmd)))

        # make pipe for daemon mpirun to talk to bgsystem
        newpipe_r, newpipe_w = os.pipe()

        pid = os.fork()
        try:
            print 'pid is', pid
            if not pid:
                os.close(newpipe_r)
                os.setsid()
                pid2 = os.fork()
                print "next pid is", pid2
                if pid2 != 0:
                    newpipe_w = os.fdopen(newpipe_w, 'w')
                    newpipe_w.write(str(pid2))
                    newpipe_w.close()
                    os._exit(0)
    
                #start daemonized child
                os.close(newpipe_w)
    
                f = open("/tmp/out.txt", "w", 1)
                f.write("forked\n")
                
                #setup output and error files
                outlog = self.outputfile or tempfile.mktemp()
                errlog = self.errorfile or tempfile.mktemp()
    
                #check for location to run
                if not self.location:
                    raise ProcessGroupCreationError, "location"
                partition = self.location[0]
    
                #check for valid user/group
                try:
                    userid, groupid = pwd.getpwnam(self.user)[2:4]
                except KeyError:
                    raise ProcessGroupCreationError, "user/group"
    
                program = self.executable
                cwd = self.cwd
                pnum = self.size
                mode = self.mode
                args = self.args
                inputfile = self.inputfile
                kerneloptions = self.kerneloptions
                # strip out BGLMPI_MAPPING until mpirun bug is fixed 
                mapfile = ''
                if self.env.has_key('BGLMPI_MAPPING'):
                    mapfile = self.env['BGLMPI_MAPPING']
                    del self.env['BGLMPI_MAPPING']
                envs = " ".join(["%s=%s" % envdata for envdata in self.env.iteritems()])
                atexit._atexit = []
    
                try:
                    os.setgid(groupid)
                    os.setuid(userid)
                except OSError:
                    logger.error("Failed to change userid/groupid for PG %s" % (self.id))
                    sys.exit(0)
    
                #os.system("%s > /dev/null 2>&1" % (self.config['db2_connect']))
                os.environ["DB_PROPERTY"] = self.config['db2_properties']
                os.environ["BRIDGE_CONFIG_FILE"] = self.config['bridge_config']
                os.environ["MMCS_SERVER_IP"] = self.config['mmcs_server_ip']
                os.environ["DB2INSTANCE"] = self.config['db2_instance']
                os.environ["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
                os.environ["COBALT_JOBID"] = self.id
                if inputfile != '':
                    infile = open(inputfile, 'r')
                    os.dup2(infile.fileno(), sys.__stdin__.fileno())
                else:
                    null = open('/dev/null', 'r')
                    os.dup2(null.fileno(), sys.__stdin__.fileno())
                cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun']),
                       '-np', pnum, '-partition', partition,
                       '-mode', mode, '-cwd', cwd, '-exe', program)
                if args != '':
                    cmd = cmd + ('-args', args)
                if envs != '':
                    cmd = cmd + ('-env',  envs)
                if kerneloptions != '':
                    cmd = cmd + ('-kernel_options', kerneloptions)
                if mapfile != '':
                    cmd = cmd + ('-mapfile', mapfile)
    
                try:
                    err = open(errlog, 'a')
                    os.chmod(errlog, 0600)
                    os.dup2(err.fileno(), sys.__stderr__.fileno())
                except IOError:
                    logger.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (self.id, self.user, errlog))
                except OSError:
                    logger.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (self.id, self.user, errlog))
    
                try:
                    out = open(outlog, 'a')
                    os.chmod(outlog, 0600)
                    os.dup2(out.fileno(), sys.__stdout__.fileno())
                except IOError:
                    logger.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (self.id, self.user, outlog))
                except OSError:
                    logger.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (self.id, self.user, errlog))
    
                # If this mpirun command originated from a user script, its arguments
                # have been passed along in a special attribute.  These arguments have
                # already been modified to include the partition that cobalt has selected
                # for the job, and can just replace the arguments built above.
                if self.true_mpi_args:
                    cmd = (self.config.get('bgpm', 'mpirun'), os.path.basename(self.config.get('bgpm', 'mpirun'))) + tuple(self.true_mpi_args)
    
                f.write("here we go : %s\n" %  cmd)
                f.close()
                try:
                    apply(os.execl, cmd)
                except Exception, e:
                    print 'got exception when trying to exec mpirun', e
                    raise SystemExit, 1
    
                sys.exit(0)
    
            else:
                #parent process reads daemon child's pid through pipe
                os.close(newpipe_w)
                newpipe_r = os.fdopen(newpipe_r, 'r')
                childpid = newpipe_r.read()
                newpipe_r.close()
                rc = os.waitpid(pid, 0)  #wait for 1st fork'ed child to quit
                logger.info('rc from waitpid was (%d, %d)' % rc)
                self.pid = childpid

        except Exception, e:
            print "something has gone dreadfully wrong: ", e
            sys.exit(1)
            
class JobList (DataList):
    item_cls = Job
    def __init__(self):
        self.id_gen = IncrID()
 
    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if "system_id" not in spec or spec['system_id'] == "*":
                spec['system_id'] = self.id_gen.next()
        return DataList.q_add(self, specs)



class BGSystem (Component):
    
    """Generic system simulator.
    
    Methods:
    configure -- load partitions from an xml file
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
        self.jobs = JobList()
        self.configure()
    
    def _get_partitions (self):
        return PartitionDict([
            (partition.name, partition) for partition in self._partitions.itervalues()
            if partition.name in self._managed_partitions
        ])
    
    partitions = property(_get_partitions)
    
    def configure (self):
        
        """Read partition data from the bridge.
        """
        
        self.logger.info("configure()")
        system_def = bgl.PartitionList.by_filter()

        # that 32 is not really constant -- it needs to either be read from cobalt.conf or from the bridge API
        NODES_PER_NODECARD = 32
                
        # initialize a new partition dict with all partitions
        #
        partitions = PartitionDict()
        partitions.q_add([
            dict(
                name = partition_def.id,
                queue = "default",
                size = NODES_PER_NODECARD * len(partition_def.node_cards),
            )
            for partition_def in system_def
        ])
        
        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)
    
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
    
    
    
    
    def add_jobs (self, specs):
        
        """Create a job.
        
        Arguments:
        spec -- dictionary hash specifying a job to start
        """
        jobs = self.jobs.q_add(specs)
        print repr(jobs)
        return jobs
    add_jobs = exposed(query(all_fields=True)(add_jobs))
    
    def get_jobs (self, specs):
        '''queries jobs via pid or PyBridge
        returns those jobs that are running'''
        return [job for job in specs
                if self.checkpid(job.get('pid'))]
    get_jobs = exposed(query(get_jobs))

    def checkpid(self, somepid):
        '''checks if the specified pid is still around'''
        ps = os.popen('ps ax')
        pids = ps.readlines()
        ps.close()
        pidlist = [p.split()[0] for p in pids]
        if str(somepid) in pidlist:
            return True
        else:
            return False
    
    def del_jobs (self, specs):
        ret = []
        for spec in specs:
            ret.append(self.signal_jobs(spec))
        
        return ret
    del_jobs = exposed(query(del_jobs))
    
    def signal_jobs (self, specs, signame="SIGINT"):
        '''kills a job using via signal to pid'''
        # status_t jm_signal_job(db_job_id_t jid, rm_signal_t signal);
        print 'bgsystem got a signal_jobs call with signal %s' % signame
        for spec in specs:
            pid = spec.get('pid')
            try:
                os.kill(int(pid), getattr(signal, signame))
            except OSError, error:
                self.logger.error("Signal failure for pid %s:%s" % (pid, error.strerror))
            
        return 0
    signal_jobs = exposed(query(signal_jobs))
    
