"""Contains the ProcessGroup and ProcessGroupDict Data Types"""

__revision__ = "$Revision$"



from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError



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
                            "jobid", "kerneloptions", "location", "mode",
                            "nodefile", "size", "state", "stderr","stdin",
                            "stdout", "true_mpi_args", "umask", "user"]

    required = ["executable", "location", "user"]

    def __init__(self, spec):
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

    def _get_state(self):
        """Gets the current 'state' property of the process group"""
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    state = property(_get_state)



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
