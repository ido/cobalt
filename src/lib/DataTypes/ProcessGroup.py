"""Contains the ProcessGroup and ProcessGroupDict Data Types"""

__revision__ = "$Revision$"


import os
import sys
import signal
import logging

import Cobalt.Logging
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError
from Cobalt.Proxy import ComponentProxy

class job_preexec(object):
    '''Class for handling pre-exec tasks for a job.
    Initilaization takes a job-data object.  This allows id's to be set 
    properly and other bookkeeping tasks to be correctly set.

    '''

    def __init__(self, data, logger):

        self.data = data
        self.logger = logger

    def __call__(self):
        '''Set important bits for cobalt jobs and redirect files as needed.
        
        '''
        data = self.data
        label = "%s/%s" % (data["jobid"], data["id"])    
        try:
            # only root can call os.setgroups so we need to do this
            # before calling os.setuid
            try:
                os.setgroups([])
                os.setgroups(data["other_groups"])
            except:
                self.logger.error("task %s: failed to set supplementary groups",
                        label, exc_info=True)
            try:
                os.setgid(data["primary_group"])
                os.setuid(data["userid"])
            except OSError:
                self.logger.error("task %s: failed to change userid/groupid", 
                        label)
                os._exit(1)
                       
            if data["umask"] != None:
                try:
                    os.umask(data["umask"])
                except:
                    self.logger.error("task %s: failed to set umask to %s", 
                            label, data["umask"])

            for key, value in data["postfork_env"].iteritems():
                os.environ[key] = value
                    
            atexit._atexit = []
        
            try:
                stdin = open(data["stdin"] or "/dev/null", 'r')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stdin file %s: %s (stdin will be /dev/null)", label, data["stdin"], e)
                stdin = open("/dev/null", 'r')
            os.dup2(stdin.fileno(), 0)
                
            new_out = None
            try:
                stdout = open(data["stdout"], 'a')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stdout file %s: %s", 
                        label, data["stdout"], e)
                output_to_devnull = False
                try:
                    scratch_dir = get_forker_config("scratch_dir", None)
                    if scratch_dir:
                        new_out = os.path.join(scratch_dir, 
                                "%s.output" % data["jobid"])
                        self.logger.error("task %s: sending stdout to scratch_dir %s", label, new_out)
                        stdout = open(new_out, 'a')
                    else:
                        self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stdout")
                        output_to_devnull = True
                except Exception, e:
                    output_to_devnull = True
                    self.logger.error("task %s: error opening stdout file %s: %s", label, new_out, e)
                                          
                if output_to_devnull:
                    stdout = open("/dev/null", 'a')
                    new_out = "/dev/null"
                    self.logger.error("task %s: sending stdout to /dev/null",
                            label)
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
                
            new_err = None
            try:
                stderr = open(data["stderr"], 'a')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stderr file %s: %s", label, data["stderr"], e)
                error_to_devnull = False
                try:
                    scratch_dir = get_forker_config("scratch_dir", None)
                    if scratch_dir:
                        new_err = os.path.join(scratch_dir, 
                                "%s.error" % data["jobid"])
                        self.logger.error("task %s: sending stderr to scratch_dir %s", label, new_err)
                        stderr = open(new_err, 'a')
                    else:
                        self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stderr")
                        error_to_devnull = True
                except Exception, e: 
                    error_to_devnull = True
                    self.logger.error("task %s: error opening stderr file %s: %s", label, new_err, e)
                                          
                if error_to_devnull:
                    stderr = open("/dev/null", 'a')
                    new_err = "/dev/null"
                    self.logger.error("task %s: sending stderr to /dev/null", label)
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
                
            cmd = data["cmd"]
            try:
                cobalt_log_file = open(data["cobalt_log_file"], "a")
                if new_out:
                    print >> cobalt_log_file, "failed to open %s" % data["stdout"]
                    print >> cobalt_log_file, "stdout sent to %s\n" % new_out
                if new_err:
                    print >> cobalt_log_file, "failed to open %s" % data["stderr"]
                    print >> cobalt_log_file, "stderr sent to %s\n" % new_err
                print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
                print >> cobalt_log_file, "called with environment:\n"
                for key in os.environ:
                    print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                print >> cobalt_log_file, "\n"
                cobalt_log_file.close()
            except:
                self.logger.error("task %s: unable to open cobaltlog file %s", 
                                 label, data["cobalt_log_file"])
        except:
            self.logger.error("task %s: Unhandled exception.")
            raise


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

    def __init__(self, spec, logger):
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

    def _get_state(self):
        """Gets the current 'state' property of the process group"""
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    state = property(_get_state)

    def start(self):
        """Start the process group by forking to _mpirun()"""
        try:
            data = self.prefork()
            preexec_fn = job_preexec(data, self.logger)
            self.head_pid = ComponentProxy("forker").fork([data['cmd']], 
                self.tag, "Job %s/%s" %(self.jobid, self.user), None, 
                preexec_fn)
        except:
            self.logger.error("problem forking: pg %s did not find a "
                "child pid", self.id)

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
