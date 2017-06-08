"""Contains the ProcessGroup and ProcessGroupDict Data Types"""

__revision__ = "$Revision$"


import logging
import signal
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError, ProcessGroupStartupError
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy

_logger = logging.getLogger()

#Get a list of valid signal strings
SIGNALS = [ s for s in signal.__dict__.keys()
        if (s.startswith("SIG") and not s.startswith("SIG_"))]

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
    kernel -- alternate kernel to boot
    kerneloptions -- options to pass to kernel
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
    sigkill_time -- time at which to send a sigkill (seconds since epoch)
    queue -- queue job was run from
    project -- accounting project tied to the job

    Only used by BlueGene/Q systems:
    ion_kernel -- alternatve ION kernel to boot
    ion_kerneloptions -- boot options to pass the ION kernel

    """

    fields = Data.fields + ["args", "cobalt_log_file", "cwd", "env",
                            "executable", "exit_status", "head_pid", "id",
                            "jobid", "kernel", "kerneloptions", "location",
                            "mode", "nodefile", "size", "state", "stderr",
                            "stdin", "stdout", "umask", "user", "starttime",
                            "walltime", "resid", "runid", "forker",
                            "subblock", "subblock_parent", "corner", "extents",
                            "attrs", "alps_res_id", "queue", "project"]

    required = Data.required + ["args", "cwd", "executable", "jobid",
                                "location", "size", "user"]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = "process group"
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
        self.ion_kernel = spec.get("ion_kernel", "default")
        self.ion_kerneloptions = spec.get("ion_kerneloptions", None)
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
        self.ranks_per_node = spec.get("ranks_per_node", None)
        self.subblock = spec.get("subblock", False)
        self.subblock_parent = spec.get("subblock_parent", None)
        self.corner = spec.get("corner", None)
        self.extents = spec.get("extents", None)
        self.attrs = spec.get("attrs", {})
        self.label = "%s/%s/%s" % (self.jobid, self.user, self.id)
        self.sigkill_timeout = None
        #TODO: extract into subclass
        self.alps_res_id = spec.get('alps_res_id', None)
        self.startup_timeout = spec.get("pgroup_startup_timeout", 0)
        self.project = spec.get('project', None)
        self.queue = spec.get('queue', None)

    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['logger', 'state']:
                data[key] = value
        return data

    def __setstate__(self, data):
        self.__dict__.update(data)

    def _get_state(self):
        """Gets the current 'state' property of the process group"""
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    state = property(_get_state)

    def start(self):
        """Start the process group by contact the appropriate forker component"""
        if self.mode == 'interactive':
            self.head_pid = 1
        else:
            try:
                data = self.prefork()
                self.head_pid = ComponentProxy(self.forker, retry=False).fork([self.executable] + self.args, self.tag,
                    "Job %s/%s/%s" %(self.jobid, self.user, self.id), self.env, data, self.runid)
            except:
                err = "Job %s/%s/%s: problem forking; %s did not return a child id" % (self.jobid,
                        self.user, self.id, self.forker)
                _logger.error(err)
                raise ProcessGroupStartupError(err)

    def signal(self, signame="SIGINT"):
        '''Validate and send signal to ProcessGroup.  Consult your system and
        python documentation for valid signals to send.

        Input:
            signame - the string name of a signal to send.  This must be a
                      signal supported by python's 'signal' library.

        Returns:
            True if signal successfully sent.  False otherwise

        Exceptions:
            ValueError - The signame was set to an invalid value.

        '''
        success = False
        if signame not in SIGNALS:
            raise ValueError("%s is not a valid signal on this system." % signame)
        try:
            ComponentProxy(self.forker).signal(self.head_pid, signame)
        except ComponentLookupError:
            _logger.error("pg %s: Unable to reach forker to send signal %s",
                    self.id, signame)
        except Exception:
            _logger.error("Unexpected exception in ProcessGroup.signal:",
                    exc_info=True)
        else:
            success = True
        return success

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

    def update_data(self, child):
        '''incorprate child termination data into the process group.

        Input:
            child - child data from a forker component.

        '''

        if child['complete']:
            if self.exit_status is None:
                self.exit_status = child['exit_status']
            if child['lost_child']:
                self.exit_status = 256
                _logger.warning('%s: child process reported lost from %s',
                        self.label, self.forker)
            if child['signum'] == 0:
                _logger.info("%s: job exited with status %s", self.label, self.exit_status)
            else:
                if child["core_dump"]:
                    core_dump_str = ", core dumped"
                else:
                    core_dump_str = ""
                _logger.info("%s: terminated with signal %s%s", self.label, child["signum"], core_dump_str)



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
