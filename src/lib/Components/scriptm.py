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
__revision__ = '$Revision$'

import logging, os, pwd, signal, sys, tempfile, time, grp
import xmlrpclib

import Cobalt.Logging
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ProcessGroupCreationError, DataCreationError, ComponentLookupError


class ProcessGroup(Data):
    '''Run a script'''

    fields = Data.fields + [
        "tag", "name", "location", "state", "user", "stdout", "stderr", "executable", "jobid",
        "path", "cwd", "args", "env", "stdin", "kerneloptions", "id", "exit_status", "job_size",
    ]

    def __init__(self, spec):
        Data.__init__(self, spec)
        spec = spec.copy()
        self.tag = spec.get("tag", "process-group")
        self.umask = spec.get('umask', 022)
        self.name = spec.pop("name", None)
        self.location = spec.pop("location", None)
        self.state = spec.pop("state", 'running')
        self.user = spec.pop("user", None)
        self.stdout = spec.pop("stdout", None)
        self.stderr = spec.pop("stderr", None)
        self.cobalt_log_file = spec.get('cobalt_log_file')
        self.executable = spec.pop("executable", None)
        self.jobid = spec.pop("jobid", None)
        self.resid = spec.pop("resid",None)
        self.path = spec.pop("path", None)
        self.cwd = spec.pop("cwd", None)
        self.args = spec.pop("args", [])
        self.env = spec.pop("env", None)
        self.stdin = spec.pop("stdin", None)
        self.kerneloptions = spec.pop("kerneloptions", None)
        self.job_size = spec.pop("size", None)
        self.id = spec.get("id")
        
        self.mpi_system_id = None
        self.exit_status = None
        
        self.log = logging.getLogger('pg')
        try:
            tmp_info = pwd.getpwnam(self.user)
            userid = tmp_info[2]
            groupid = tmp_info[3]
            home_dir = tmp_info[5]
        except KeyError:
            raise ProcessGroupCreationError, "user/group"
        if self.stdout is not None:
            self.outlog = self.stdout
        else:
            self.outlog = tempfile.mktemp()            
        if self.stderr is not None:
            self.errlog = self.stderr
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
            os.environ["COBALT_JOBID"] = str(self.jobid)
            if self.resid != None:
                os.environ["COBALT_RESID"] = str(self.resid)
            os.environ["COBALT_PARTNAME"] = self.location[0]
            os.environ["COBALT_JOBSIZE"] = str(self.job_size)
            os.environ['USER'] = self.user
            os.environ['HOME'] = home_dir
            # get supplementary groups
            supplementary_group_ids = []
            for g in grp.getgrall():
                if self.user in g.gr_mem:
                    supplementary_group_ids.append(g.gr_gid)
            try:
                os.setgroups([])
                os.setgroups(supplementary_group_ids)
            except:
                self.log.error("Failed to set supplementary groups for PG %s", self.jobid, exc_info=True)
            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                self.log.error("Failed to change userid/groupid for PG %s" % (self.jobid))
                sys.exit(0)
            try:
                os.umask(self.umask)
            except:
                self.log.error("Failed to set umask to %s" % self.umask)
            try:
                err = open(self.errlog, 'a')
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (self.jobid, self.user, self.errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (self.jobid, self.user, self.errlog))
            try:
                out = open(self.outlog, 'a')
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (self.jobid, self.user, self.outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (self.jobid, self.user, self.errlog))
            cmd = [self.executable, self.executable] + self.args

            chdir_error = ""
            try:
                os.chdir(self.cwd)
            except:
                self.log.error("Job %s/%s: unable to set cwd to %s" % (self.jobid, self.user, self.cwd))
                chdir_error = "unable to set cwd to %s" % self.cwd
                
            try:
                cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
                if chdir_error:
                    print >> cobalt_log_file, chdir_error + "\n" 
                print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
                print >> cobalt_log_file, "called with environment:\n"
                for key in os.environ:
                    print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                print >> cobalt_log_file, "\n"
                cobalt_log_file.close()
            except:
                self.log.error("Job %s/%s: unable to open cobaltlog file %s" % (self.jobid, self.user, self.cobalt_log_file))

            try:
                os.execl(*cmd)
            except Exception, e:
                self.log.error("Job %s/%s: Something went wrong in starting the script job." % (self.jobid, self.user), exc_info=1)
                os._exit(1)
                

    def FinishProcess(self):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        try:
            pgroup = ComponentProxy("system").signal_process_groups([{'id':self.mpi_system_id}], "SIGTERM")
            self.log.info("killed MPI process with id %s" % self.mpi_system_id)
            self.state = 'finished'
            return True
        except ComponentLookupError:
            self.log.error("Failed to communicate with the system when killing MPI job")
            return False


    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(self.pid, getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.jobid, error.strerror))
        return 0

    def invoke_mpi_from_script(self, spec):
        '''Run an mpirun job that was invoked by a script.'''
        self.state = 'running'

        stdin = spec.get("stdin", self.stdin)
        stdout = spec.get("stdout", self.stdout)
        stderr = spec.get("stderr", self.stderr)
        
        try:
            pgroup = ComponentProxy("system").add_process_groups([{
                'jobid':self.jobid,
                'tag':'process-group',
                'user':self.user, 
                'stdout':stdout,
                'stderr':stderr,
                'cobalt_log_file':self.cobalt_log_file,
                'cwd':self.cwd, 
                'location': self.location,
                'stdin':stdin,
                'true_mpi_args':spec['true_mpi_args'], 
                'env':{'path':self.path},
                'size':0,
                'args':[],
                'executable':"this will be ignored"}])
        except (ComponentLookupError, xmlrpclib.Fault):
            self.log.error("Job %s: Failed to start up user script job" % (self.jobid))
            return


        if not pgroup[0].has_key('id'):
            self.log.error("Process Group creation failed for Job %s" % self.jobid)
            self.set('state', 'sm-failure')
        else:
            self.mpi_system_id = pgroup[0]['id']

class ProcessGroupDict(DataDict):
    item_cls = ProcessGroup
    key = "id"
    
    def __init__(self):
        self.id_gen = IncrID()
 
    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if spec.get("id", "*") != "*":
                raise DataCreationError("cannot specify an id")
            spec['id'] = self.id_gen.next()
        return DataDict.q_add(self, specs)


    
# add a DataList element or something like that... which is built to contain things of type ProcessGroup
class ScriptManager(Component):
    '''The ScriptManager supports the running of scripts on a BG machine'''
    name = 'script-manager'

    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = logging.getLogger("Cobalt.Components.ScriptManager")
    implementation = 'scriptm'

    def __init__ (self, *args, **kwargs):
        """Initialize a new ServiceLocator.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.ignore = []
        self.lastwait = 0
        self.pgroups = ProcessGroupDict()
        self.zombie_mpi = {}
    
    def manage_children(self):
        for pgroup in self.zombie_mpi.keys():
            if pgroup.FinishProcess():
                del self.zombie_mpi[pgroup]
                
        self.lock.acquire()
        try:
            if (time.time() - self.lastwait) > 6:
                while True:
                    try:
                        self.lastwait = time.time()
                        (pid, stat) = os.waitpid(-1, os.WNOHANG)
                    except OSError:
                        break
                    if pid == 0:
                        break
                    pgrps = [pgrp for pgrp in self.pgroups.itervalues() if pgrp.pid == pid]
                    if len(pgrps) == 0:
                        self.logger.error("Failed to locate process group for pid %s" % (pid))
                    elif len(pgrps) == 1:
                        pgroup = pgrps[0]
                        pgroup.exit_status = stat
                        self.logger.info("Job %s/%s: ProcessGroup %s Finished with exit code %d. pid %s" % \
                          (pgroup.jobid, pgroup.user, pgroup.jobid, int(stat)/256, pgroup.pid))

                        if os.WIFSIGNALED(stat):
                            self.logger.info("Job %s/%s: ProcessGroup %s received signal %s" % \
                          (pgroup.jobid, pgroup.user, pgroup.jobid, os.WTERMSIG(stat)))
                            try:
                                err = open(pgroup.cobalt_log_file, 'a')
                                print >> err, "The script job exited after receiving signal %s" % os.WTERMSIG(stat)
                                err.close()
                            except IOError:
                                self.logger.error( "Job %s/%s: ProcessGroup %s failed to update .error file" % (pgroup.jobid, pgroup.user, pgroup.jobid))

                        self.zombie_mpi[pgroup] = True
                            
                    else:
                        self.logger.error("Got more than one match for pid %s" % (pid))
        except:
            # just to make sure we don't keep the lock forever
            self.logger.error("error in manage_children", exc_info=True)
        self.lock.release()
    manage_children = locking(automatic(manage_children))

    def add_jobs(self, specs):
        '''Create new process group element'''
        self.logger.info("creating process group %r" % specs)
        return self.pgroups.q_add(specs)
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs(self, specs):
        '''query existing process group'''
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
            for pg in self.pgroups.itervalues():
                if pg.id == int(spec['id']):
                    ret.append(pg.Signal(sig))
        # could not find pg, so return False
        return ret
    signal_jobs = exposed(signal_jobs)
    
    def SigChildHand(self, sig, frame):
        '''Dont Handle SIGCHLDs'''
        pass
    
    
    def invoke_mpi_from_script(self, spec):
        '''Invoke the real mpirun on behalf of a script being executed by the script manager.'''
        self.lock.acquire()
        try:
            jobs = self.pgroups.q_get([{'jobid':spec['jobid'], 'user':spec['user']}])
        except:
            # just make sure we don't keep the lock forever
            self.logger.error("error in invoke_mpi_from_script", exc_info=True)
        self.lock.release()

        if len(jobs) != 1:
            self.logger.error("invoke_mpi_from_script matched more than one job with spec %r" % spec)
            return -1
        else:
            jobs[0].invoke_mpi_from_script(spec)
            return jobs[0].mpi_system_id
    invoke_mpi_from_script = locking(exposed(invoke_mpi_from_script))


