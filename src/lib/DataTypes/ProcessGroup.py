"""Contains the ProcessGroup and ProcessGroupDict Data Types"""

__revision__ = "$Revision$"


import os
import sys
import atexit
import signal
import logging
import Queue
import multiprocessing as mp

import Cobalt.Logging
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError

class Child(object):
    def __init__(self):
        self.pid = None
        self.exit_status = None
        self.signum = 0
        self.core_dump = False
        
def forker(cmd_q):
    Cobalt.Logging.setup_logging("forker")
    logger = logging.getLogger("forker")

    children = {}
    
    while True:
        cmd,data,resp_q = cmd_q.get()

        # before handling each request, check for dead children
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError: # there are no child processes
                break
            # this is how waitpid + WNOHANG reports things are running
            # but not yet dead
            if pid == 0:
                break
            signum = 0
            core_dump = False
            if os.WIFEXITED(status):
                status = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                signum = os.WTERMSIG(status)
                if os.WCOREDUMP(status):
                    core_dump = True
            else:
                break
            
            for each in children.itervalues():
                if each.pid == pid:
                    if signum == 0:
                        each.exit_status = status
                    else:
                        each.exit_status = 128 + signum
                        each.core_dump = core_dump
                        each.signum = signum

        # now handle the request
        if cmd == "fork":
            child_pid = os.fork()
            if not child_pid:
                try:
                    
                    pg_id = data["id"]
                    try:
                        os.setgid(data["groupid"])
                        os.setuid(data["userid"])
                    except OSError:
                        logger.error("failed to change userid/groupid for process group %s" % (pg_id))
                        os._exit(1)
            
                    if data["umask"] != None:
                        try:
                            os.umask(data["umask"])
                        except:
                            logger.error("Failed to set umask to %s" % data["umask"])

                    for key, value in data["postfork_env"].iteritems():
                        os.environ[key] = value
                        
                    atexit._atexit = []
            
                    try:
                        stdin = open(data["stdin"], 'r')
                    except (IOError, OSError, TypeError), e:
                        logger.error("process group %s: error opening stdin file %s: %s (stdin will be /dev/null)" % (pg_id, data["stdin"], e))
                        stdin = open("/dev/null", 'r')
                    os.dup2(stdin.fileno(), 0)
                    
                    try:
                        stdout = open(data["stdout"], 'a')
                    except (IOError, OSError, TypeError), e:
                        logger.error("process group %s: error opening stdout file %s: %s (stdout will be lost)" % (pg_id, data["stdout"], e))
                        stdout = open("/dev/null", 'a')
                    os.dup2(stdout.fileno(), sys.__stdout__.fileno())
                    
                    try:
                        stderr = open(data["stderr"], 'a')
                    except (IOError, OSError, TypeError), e:
                        logger.error("process group %s: error opening stderr file %s: %s (stderr will be lost)" % (pg_id, data["stderr"], e))
                        stderr = open("/dev/null", 'a')
                    os.dup2(stderr.fileno(), sys.__stderr__.fileno())
                    
                    cmd = data["cmd"]
                    try:
                        cobalt_log_file = open(data["cobalt_log_file"], "a")
                        print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
                        print >> cobalt_log_file, "called with environment:\n"
                        for key in os.environ:
                            print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                        print >> cobalt_log_file, "\n"
                        cobalt_log_file.close()
                    except:
                        logger.error("process group %s unable to open cobaltlog file %s" % \
                                     (pg_id, data["cobalt_log_file"]))
            
                    os.execl(*cmd)
                    
                except:
                    logger.error("Unable to start job", exc_info=1)
                    os._exit(1)
            else:
                kid = Child()
                kid.pid = child_pid
                children[child_pid] = kid
                resp_q.put(child_pid)
        elif cmd == "signal":
            try:
                os.kill(int(data["pid"]), getattr(signal, data["signame"]))
            except OSError, e:
                logger.error("signal failure for process group %s: %s" % (data["id"], e))
        elif cmd == "active_list":
            ret = []
            for kid in children.itervalues():
                if kid.exit_status is None:
                    ret.append(kid.pid)
                    
            resp_q.put(ret)
        elif cmd == "get_status":
            if children.has_key(data):
                dead = children[data]
                if dead.exit_status is not None:
                    del children[data]
                    resp_q.put(dead)
                else:
                    resp_q.put(None)
            else:
                resp_q.put(None)
        elif cmd == "quit":
            os._exit(0)


        

class ProcessGroup(Data):
    """A job that runs on the system
    
    Attributes:
    tag -- defines what this Data object is (by default "process group")
    args -- Arguments to be passed to the executable script when run
    cobalt_log_file -- log file in which to record env info before script runs
    cwd -- current working directory for the job
    env -- environment variables to set for the job
    executable -- absolute path to the executable to be run
    exit_status -- the exit status of the job
    head_pid -- the PID of the child process that becomes the job
    id -- integer id to identify process group
    jobid -- jobid of process group
    kernel --
    kerneloptions -- 
    location -- location in system where job will run
    mode -- "script" or other
    nodefile -- used to make a file listing locations that job can run
    size -- 
    state -- "running" or "terminated"
    stderr -- file to use for stderr of script
    stdin -- file to use for stdin of script
    stdout -- file to use for stdout of script
    true_mpi_args -- 
    umask -- permissions to set
    user -- the user the process group is running under
    """

    fields = Data.fields + ["args", "cobalt_log_file", "cwd", "env",
                            "executable", "exit_status", "head_pid", "id",
                            "jobid", "kernel", "kerneloptions", "location",
                            "mode", "nodefile", "size", "state", "stderr",
                            "stdin", "stdout", "true_mpi_args", "umask",
                            "user"]

    required = Data.required + ["args", "cwd", "executable", "jobid",
                                "location", "size", "user"]

    def __init__(self, spec, logger, cmd_queue):
        Data.__init__(self, spec)
        self.tag = "process group"
        self.args = " ".join(spec.get("args", []))
        self.cobalt_log_file = spec.get("cobalt_log_file")
        self.cwd = spec.get("cwd")
        self.env = spec.get("env", {})
        self.executable = spec.get("executable")
        self.exit_status = None
        self.head_pid = None
        self.id = spec.get("id")
        self.jobid = spec.get("jobid")
        self.kernel = spec.get("kernel")
        self.kerneloptions = spec.get("kerneloptions")
        self.location = spec.get("location", [])
        self.mode = spec.get("mode")
        self.nodefile = None
        self.size = spec.get("size")
        self.stderr = spec.get("stderr")
        self.stdin = spec.get("stdin")
        self.stdout = spec.get("stdout")
        self.true_mpi_args = spec.get("true_mpi_args")
        self.umask = spec.get("umask")
        self.user = spec.get("user", "")

        self.logger = logger
        self.cmd_queue = cmd_queue

    def _get_state(self):
        """Gets the current 'state' property of the process group"""
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    state = property(_get_state)

    def start(self):
        """Start the process group by forking to _mpirun()"""
        resp_q = mp.Manager().Queue()
        
        data = self.prefork()
        
        self.cmd_queue.put( ("fork", data, resp_q) )
        
        try:
            self.head_pid = resp_q.get(timeout=5)
        except Queue.Empty:
            self.logger.error("problem forking: pg %s did not find a child pid", self.id)

    def prefork (self):
        """This method is called before the fork, while it's still safe to call 
        object methods.  It returns a dictionary, which can be passed to a totally
        static function which handles the exec from inside the child process."""
        
        return {}
    
    def _runjob(self):
        """This method is called from the forked process in start() to run a job
        on the system.  It should be overridden by whatever specialized Process
        Group class extends this one within each system component."""
        os._exit(0)



class ProcessGroupDict(DataDict):
    """A container for holding process groups, keyed by id"""

    item_cls = ProcessGroup
    key = "id"
    
    def __init__(self):
        DataDict.__init__(self)
        self.id_gen = IncrID()

    def q_add(self, specs, callback=None, cargs={}):
        """Add a process group to the container"""
        for spec in specs:
            if spec.get("id", "*") != "*":
                raise DataCreationError("cannot specify an id")
            spec["id"] = self.id_gen.next()
        return DataDict.q_add(self, specs, callback, cargs)
