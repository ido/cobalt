import logging
import subprocess
PIPE = subprocess.PIPE
import Cobalt.Components.base_forker
BaseForker = Cobalt.Components.base_forker.BaseForker
BasePreexec = Cobalt.Components.base_forker.BasePreexec
import Cobalt.Util
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string

_logger = logging.getLogger(__name__)


class SystemScriptPreexec (BasePreexec):
    def __init__(self, child):
        BasePreexec.__init__(self, child)

    def do_first(self):
        BasePreexec.do_first(self)

    def do_last(self):
        BasePreexec.do_last(self)


class SystemScriptForker (BaseForker):
    
    """Component for starting system script jobs such as the prologue and epilogue scripts run by cqm"""
    
    name = "system_script_forker"
    # implementation = "generic"

    def __init__ (self, *args, **kwargs):
        """Initialize a new system script forker.
        
        All arguments are passed to the base forker constructor.
        """
        BaseForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return BaseForker.__getstate__(self)

    def __setstate__(self, state):
        BaseForker.__setstate__(self, state)

    def _fork(self, child, data):
        # One last bit of mangling to prevent premature splitting of args
        # quote the argument strings so the shell doesn't eat them.
        command_str = convert_argv_to_quoted_command_string([child.cmd] + child.args)

        try:
            preexec_fn = SystemScriptPreexec(child)
        except:
            _logger.error("%s: instantiation of preexec class failed; aborting execution")
            raise

        try:
            _logger.debug("%s: attempting to run %s", child.label, command_str)
            child.proc = subprocess.Popen(command_str, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=preexec_fn)
            child.pid = child.proc.pid
            child.ignore_output = False
            _logger.info("%s: forked with pid %s", child.label, child.pid)
        except OSError as e:
            _logger.error("%s: failed to execute with a code of %s: %s", child.label, e.errno, e)
        except ValueError:
            _logger.error("%s: failed to run due to bad arguments.", child.label)
        except Exception as e:
            _logger.error("%s: failed due to an unexpected exception: %s", child.label, e)
            _logger.debug("%s: Parent Traceback:", child.label, exc_info=True)
            if e.__dict__.has_key('child_traceback'):
                _logger.debug("%s: Child Traceback:\n %s", child.label, e.child_traceback)
            #It may be valuable to get the child traceback for debugging.
            raise
