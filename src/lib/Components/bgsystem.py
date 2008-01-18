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
import traceback
from datetime import datetime

import Cobalt
import Cobalt.Data
from Cobalt.Data import Data, DataDict, DataList, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
import Cobalt.bridge
from Cobalt.bridge import BridgeException

__all__ = [
    "JobCreationError",
    "Partition", "PartitionDict",
    "Job", "JobDict",
    "Simulator",
]

logger = logging.getLogger(__name__)
Cobalt.bridge.set_serial("BGP")

class JobCreationError (Exception):
    """An error occured when creation a job."""

class ExitEarlyError (Exception):
    """simulate a goto!!!"""


class NodeCard (object):
    def __init__(self, name):
        self.id = name
        self.busy = False
        
    def __eq__(self, other):
        return self.id == other.id
        

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
        # these hold Partition objects
        self._parents = sets.Set()
        self._children = sets.Set()
        self.state = spec.pop("state", "idle")
        self.tag = spec.get("tag", "partition")
        self.node_cards = spec.get("node_cards", [])
        # this holds partition names
        self._wiring_conflicts = sets.Set()

        self._update_node_cards()

    def _update_node_cards(self):
        if self.state == "busy":
            for nc in self.node_cards:
                nc.busy = True
    
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
        sys.exit(1)
    config = _config._sections['bgpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        sys.exit(1)

    def __init__(self, spec):
        Data.__init__(self, spec)
        spec = spec.copy()
        self.system_id = spec['system_id']
        self.outputfile = spec.get('stdout', False)
        self.errorfile = spec.get('stderr', False)
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
                if pid2 != 0:
                    newpipe_w = os.fdopen(newpipe_w, 'w')
                    newpipe_w.write(str(pid2))
                    newpipe_w.close()
                    os._exit(0)
    
                #start daemonized child
                os.close(newpipe_w)
    
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
                if self.env is None:
                    self.env = {}
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
                    os._exit(0)
    
                #os.system("%s > /dev/null 2>&1" % (self.config['db2_connect']))
                os.environ["DB_PROPERTY"] = self.config['db2_properties']
                os.environ["BRIDGE_CONFIG_FILE"] = self.config['bridge_config']
                os.environ["MMCS_SERVER_IP"] = self.config['mmcs_server_ip']
                os.environ["DB2INSTANCE"] = self.config['db2_instance']
                os.environ["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
                os.environ["COBALT_JOBID"] = str(self.id)
                if inputfile:
                    infile = open(inputfile, 'r')
                    os.dup2(infile.fileno(), sys.__stdin__.fileno())
                else:
                    null = open('/dev/null', 'r')
                    os.dup2(null.fileno(), sys.__stdin__.fileno())
                cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun']),
                       '-np', pnum, '-partition', partition,
                       '-mode', mode, '-cwd', cwd, '-exe', program)
                if args:
                    cmd = cmd + ('-args', args)
                if envs:
                    cmd = cmd + ('-env',  envs)
                if kerneloptions:
                    cmd = cmd + ('-kernel_options', kerneloptions)
                if mapfile:
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
    
                try:
                    apply(os.execl, cmd)
                except Exception, e:
                    print 'got exception when trying to exec mpirun', e
                    os._exit(1)
    
                os._exit(0)
    
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
            print "something has gone dreadfully wrong starting a job: ", e
            traceback.print_exc(file=sys.stdout)
            os._exit(1)
            
class JobDict (DataDict):
    item_cls = Job
    key = "id"
    
    def __init__(self):
        self.id_gen = IncrID()
 
    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if "system_id" not in spec or spec['system_id'] == "*":
                spec['system_id'] = self.id_gen.next()
        return DataDict.q_add(self, specs)



class BGSystem (Component):
    
    """Generic system simulator.
    
    Methods:
    configure -- load partitions from the bridge API
    get_partitions -- retrieve partitions managed by cobalt (exposed, query)
    add_jobs -- add (start) a job on the system (exposed, ~query)
    get_jobs -- retrieve running jobs (exposed, query)
    del_jobs -- delete jobs (exposed, query)
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
        self.node_card_cache = dict()

        # do this last
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
        
        def _get_state(bridge_partition):
            if bridge_partition.state == "RM_PARTITION_FREE":
                return "idle"
            else:
                return "busy"
    
        def _get_node_card(name):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name)
                
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
        
        for partition_def in system_def:
            node_list = []
            nc_count = len(list(partition_def.node_cards))
            if partition_def.connection == "RM_TORUS":
                if not wiring_cache.has_key(nc_count):
                    wiring_cache[nc_count] = []
                wiring_cache[nc_count].append(partition_def)

            if partition_def.small:
                bp_name = partition_def.base_partitions[0].id
                for nc in partition_def._node_cards:
                    node_list.append(_get_node_card(bp_name + "-" + nc.id))
            else:
                try:
                    for bp in partition_def.base_partitions:
                        bp_name = bp.id
                        for nc in Cobalt.bridge.NodeCardList.by_base_partition(bp):
                            node_list.append(_get_node_card(bp_name + "-" + nc.id))
                except BridgeException:
                    print "Error communicating with the bridge during initial config.  Terminating."
                    sys.exit(1)

            tmp_list.append( dict(
                name = partition_def.id,
                queue = "default",
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                state = _get_state(partition_def),
            ))
        
        partitions.q_add(tmp_list)
                                         
#        partitions.q_add([
#            dict(
#                name = partition_def.id,
#                queue = "default",
#                size = NODES_PER_NODECARD * len(partition_def.node_cards), 
#                node_cards = [ _get_node_card(nc.id) for nc in partition_def.node_cards ],
#                state = _get_state(partition_def),
#            )
#            for partition_def in system_def
#        ])
        
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
                        print "%s and %s have a wiring conflict" % (p.id, other.id)
                        partitions[p.id]._wiring_conflicts.add(other.id)
        
        end = time.time()
        print "took %f seconds to find wiring deps" % (end - start)
 
        # update state information
        for p in partitions.values():
            if p.state != "busy":
                for nc in p.node_cards:
                    if nc.busy:
                        p.state = "blocked"
                        break
                for dep_name in p._wiring_conflicts:
                    if partitions[dep_name].state == "busy":
                        p.state = "blocked-wiring"
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

        try:
            system_def = Cobalt.bridge.PartitionList.info_by_filter()
        except BridgeException:
            self.logger.error("Error communicating with the bridge to update partition state information.")
            return

        # first, set all of the nodecards to not busy
        for nc in self.node_card_cache.values():
            nc.busy = False
            
        for partition in system_def:
            if self._partitions.has_key(partition.id):
                self._partitions[partition.id].state = _get_state(partition)
                self._partitions[partition.id]._update_node_cards()
            
        for p in self._partitions.values():
            if p.state != "busy":
                for nc in p.node_cards:
                    if nc.busy:
                        p.state = "blocked"
                        break
                for dep_name in p._wiring_conflicts:
                    if self._partitions[dep_name].state == "busy":
                        p.state = "blocked-wiring"
                        break
    
    update_partition_state = automatic(update_partition_state)

    
    def update_relatives(self):
        """Call this method after changing the contents of self._managed_partitions"""
        for p_name in self._managed_partitions:
            self._partitions[p_name]._parents = sets.Set()
            self._partitions[p_name]._children = sets.Set()

        for p_name in self._managed_partitions:
            p = self._partitions[p_name]
            
            # toss the wiring dependencies in with the parents
            for dep_name in p._wiring_conflicts:
                if dep_name in self._managed_partitions:
                    p._parents.add(self._partitions[dep_name])
            
            for other_name in self._managed_partitions:
                if p.name == other_name:
                    break

                other = self._partitions[other_name]
                p_set = sets.Set(p.node_cards)
                other_set = sets.Set(other.node_cards)

                # if p is a subset of other, then p is a child
                if p_set.intersection(other_set)==p_set:
                    p._parents.add(other)
                    other._children.add(p)
                # if p contains other, then p is a parent
                elif p_set.union(other_set)==p_set:
                    p._children.add(other)
                    other._parents.add(p)
                    
            

    
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
        self.update_relatives()
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
        self._managed_partitions -= sets.Set( [partition.name for partition in partitions] )
        self.update_relatives()
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
        return self.jobs.q_add(specs)
    add_jobs = exposed(query(all_fields=True)(add_jobs))
    
    def get_jobs (self, specs):
        '''queries jobs via pid or PyBridge
        returns those jobs that are running'''
        self.logger.info("get_jobs(%r)" % (specs))
        my_jobs = self.jobs.q_get(specs)
        self.logger.info("my_jobs(%r)" % (my_jobs))
        ret = [job for job in my_jobs
                if self.checkpid(job.pid)]
        return ret
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
        my_jobs = self.jobs.q_get(specs)
        for job in my_jobs:
            pid = job.pid
            try:
                os.kill(int(pid), getattr(signal, signame))
                del self.jobs[job.id]
            except OSError, error:
                self.logger.error("Signal failure for pid %s:%s" % (pid, error.strerror))

        return my_jobs
    signal_jobs = exposed(query(signal_jobs))
    
