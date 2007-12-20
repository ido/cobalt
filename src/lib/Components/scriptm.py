'''
Implements a script-manager component.

The script-manager component is used to execute scripts that have been 
submitted to the job queue.  When a job in the queue with mode "script" is 
selected for execution, that job is handed off to the script-manager.  Scripts
do not execute on the compute nodes, which is why "script" jobs are not 
handled by the process-manager. 

The script-manager invokes the script, which may in turn invoke our custom
mpirun command.  The job ID of the script is placed into the environment
variable COBALT_JOBID so that the custom mpirun command can look up job
specific information like the partition to run on and the maximum number of
nodes that can be requested.
'''
__revision__ = '$Revision: $'

import logging, os, pwd, signal, sys, tempfile, time

import Cobalt.Logging
from Cobalt.Data import Data, DataList
from Cobalt.Components.base import Component, exposed, automatic, query

class ProcessGroup(Data):
    '''Run a script'''

    fields = Data.fields + [
        "tag", "name", "location", "state", "user", "outputfile", "errorfile", "executable", 
    ]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = spec.get("tag", "process-group")
        self.name = spec.pop("name", None)
        self.location = spec.pop("location", None)
        self.state = spec.pop("state", 'running')
        self.user = spec.pop("user", None)
        self.outputfile = spec.pop("outputfile", None)
        self.errorfile = spec.pop("errorfile", None)
        self.executable = spec.pop("executable", None)
        
        self.log = logging.getLogger('pg')
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            raise ProcessGroupCreationError, "user/group"
        if self.outputfile is not None:
            self.outlog = self.outputfile
        else:
            self.outlog = tempfile.mktemp()            
        if self.errorfile is not None:
            self.errlog = self.errorfile
        else:
            self.errlog = tempfile.mktemp()

        self.pid = os.fork()
        if not self.pid:
            program = self.executable
            self.t = tempfile.NamedTemporaryFile()
            self.t.write("\n".join(self.location) + '\n')
            self.t.flush()
            # create a nodefile in /tmp
            os.environ['COBALT_NODEFILE'] = self.t.name
            os.environ["COBALT_JOBID"] = str(self.id)
            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                self.log.error("Failed to change userid/groupid for PG %s" % (self.id))
                sys.exit(0)
            try:
                err = open(self.errlog, 'a')
                os.chmod(self.errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (self.id, self.user, self.errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (self.id, self.user, self.errlog))
            try:
                out = open(self.outlog, 'a')
                os.chmod(self.outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (self.id, self.user, self.outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (self.id, self.user, self.errlog))
            os.execl(self.executable, self.executable)

    def FinishProcess(self, status):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        self.state = 'finished'
        self.log.info("Job %s/%s: ProcessGroup %s Finished with exit code %d. pid %s" % \
                      (self.id, self.user, self.id, int(status)/256, self.pid))

    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(self.pid, getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.id, error.strerror))
        return 0

class ProcessGroupList(DataList):
    item_cls = ProcessGroup
    
# add a DataList element or something like that... which is built to contain things of type ProcessGroup
class ScriptManager(Component):
    '''The ScriptManager supports the running of scripts on a BG machine'''
    name = 'script-manager'

    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = logging.getLogger("Cobalt.Components.ScriptManager")

    def __init__ (self, *args, **kwargs):
        """Initialize a new ServiceLocator.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.ignore = []
        self.lastwait = 0
        self.pgroups = ProcessGroupList()
    
    def manage_children(self):
        if (time.time() - self.lastwait) > 6:
            while True:
                try:
                    self.lastwait = time.time()
                    (pid, stat) = os.waitpid(-1, os.WNOHANG)
                except OSError:
                    break
                if pid == 0:
                    break
                pgrps = [pgrp for pgrp in self.pgroups if pgrp.pid == pid]
                if len(pgrps) == 0:
                    self.logger.error("Failed to locate process group for pid %s" % (pid))
                elif len(pgrps) == 1:
                    pgrps[0].FinishProcess(stat)
                else:
                    self.logger.error("Got more than one match for pid %s" % (pid))
    manage_children = automatic(manage_children)

    def add_jobs(self, specs):
        '''Create new process group element'''
        self.logger.info("creating process group %r" % specs)
        return self.pgroups.q_add(specs)
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs(self, specs):
        '''query existing process group'''
        self.logger.info("querying for process group %r" % specs)
        return self.pgroups.q_get(specs)
    get_jobs = exposed(query(get_jobs))

    def wait_jobs(self, specs):
        '''Remove completed process group'''
        self.logger.info("removing process group %r" % specs)
        return self.pgroups.q_del(specs)
    wait_jobs = exposed(query(wait_jobs))

    def signal_jobs(self, specs, sig):
        '''signal existing process group with specified signal'''
        ret = []
        for spec in specs:
            self.logger.info("signaling process group %r with signal %r" % (spec, sig))
            for pg in self.pgroups:
                if pg.id == spec['id']:
                    ret.append(pg.Signal(sig))
        # could not find pg, so return False
        return ret
    signal_jobs = exposed(signal_jobs)
    
    def SigChildHand(self, sig, frame):
        '''Dont Handle SIGCHLDs'''
        pass
    