"""Contains the ProcessGroup and ProcessGroupDict Data Types"""

__revision__ = "$Revision$"


import logging
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError
from Cobalt.Proxy import ComponentProxy

_logger = logging.getLogger()
                                          
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
    umask -- permissions to set
    user -- the user the process group is running under
    """

    fields = Data.fields + ["args", "cobalt_log_file", "cwd", "env",
                            "executable", "exit_status", "head_pid", "id",
                            "jobid", "kernel", "kerneloptions", "location",
                            "mode", "nodefile", "size", "state", "stderr",
                            "stdin", "stdout", "umask", "user", "starttime",
                            "walltime", "resid", "runid", "forker"]

    required = Data.required + ["args", "cwd", "executable", "jobid",
                                "location", "size", "user"]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = "process group"
        # self.args = " ".join(spec.get("args", []))
        self.args = spec.get("args", [])
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
        self.umask = spec.get("umask")
        self.user = spec.get("user", "")
        self.starttime = spec.get("starttime")
        self.walltime = spec.get("walltime")
        self.killtime = spec.get("killtime")
        self.resid = spec.get("resid", None)
        self.runid = spec.get("runid", None)
        self.forker = spec.get("forker", None)

        # self.logger = logger

    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['logger', 'state']:
                data[key] = value
        return data

    def __setstate__(self, data):
        self.__dict__.update(data)
        # self.logger = logging.getLogger()

    def _get_state(self):
        """Gets the current 'state' property of the process group"""
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    state = property(_get_state)

    def start(self):
        """Start the process group by contact the appropriate forker component"""
        try:
            data = self.prefork()
            self.head_pid = ComponentProxy(self.forker, retry=False).fork([self.executable] + self.args, self.tag,
                "Job %s/%s/%s" %(self.jobid, self.user, self.id), self.env, data, self.runid)
        except:
            _logger.error("Job %s/%s/%s: problem forking; %s did not return a child id", self.jobid, self.user, self.id,
                self.forker)
            raise

    def prefork (self):
        """This method is called before the fork, while it's still safe to 
        call object methods.  It returns a dictionary, which can be passed to 
        a totally static function which handles the exec from inside the child
        process.
        
        """
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['logger', 'state']:
                data[key] = value
        return data


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
