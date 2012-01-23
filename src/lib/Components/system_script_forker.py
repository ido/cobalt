import logging
import os
import tempfile

import Cobalt
import Cobalt.Components.base_forker
BaseForker = Cobalt.Components.base_forker.BaseForker
BaseChild = Cobalt.Components.base_forker.BaseChild
import Cobalt.Util
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string

_logger = logging.getLogger(__name__.split('.')[-1])


class SystemScriptChild (BaseChild):
    def __init__(self, id = None, **kwargs):
        BaseChild.__init__(self, id=id, **kwargs)

        try:
            self.stdin_file = open("/dev/null")
        except (OSError, IOError), e:
            _logger.error("%s: unable to open /dev/null (to redirect stdin): %s", self.label, e)
            raise

        stdout_fn = None
        try:
            try:
                stdout_fd, stdout_fn = tempfile.mkstemp(prefix="cobalt_ssf_%s_" % (self.id,), suffix=".stdout")
            except (OSError, IOError), e:
                _logger.error("%s: unable to create temporary stdout file: %s", self.label, e)
            else:
                try:
                    self.stdout_file = os.fdopen(stdout_fd, 'a+', 1)
                except (OSError, IOError), e:
                    _logger.error("%s: unable to open temporary stdout file: %s", self.label, e)
        finally:
            if stdout_fn is not None:
                try:
                    os.unlink(stdout_fn)
                except (OSError, IOError), e:
                    _logger.warning("%s: unable to remove temporary stdout file: %s", self.label, e)
        if self.stdout_file is None:
            try:
                _logger.warning("%s: redirecting stdout to /dev/null", self.label)
                self.stdout_file = open("/dev/null")
            except (OSError, IOError), e:
                _logger.error("%s: unable to open /dev/null (to redirect stdout): %s", self.label, e)
                raise

        stderr_fn = None
        try:
            try:
                stderr_fd, stderr_fn = tempfile.mkstemp(prefix="cobalt_ssf_%s_" % (self.id,), suffix=".stderr")
            except (OSError, IOError), e:
                _logger.error("%s: unable to create temporary stderr file: %s", self.label, e)
            else:
                try:
                    self.stderr_file = os.fdopen(stderr_fd, 'a+', 1)
                except (OSError, IOError), e:
                    _logger.error("%s: unable to open temporary stderr file: %s", self.label, e)
        finally:
            if stderr_fn is not None:
                try:
                    os.unlink(stderr_fn)
                except (OSError, IOError), e:
                    _logger.warning("%s: unable to remove temporary stderr file: %s", self.label, e)
        if self.stderr_file is None:
            try:
                _logger.warning("%s: redirecting stderr to /dev/null", self.label)
                self.stderr_file = open("/dev/null")
            except (OSError, IOError), e:
                _logger.error("%s: unable to open /dev/null (to redirect stderr): %s", self.label, e)
                raise

        self.return_output = True

    def __getstate__(self):
        state = {}
        state.update(BaseChild.__getstate__(self))
        return state

    def __setstate__(self, state):
        BaseChild.__setstate__(self, state)

    def preexec_first(self):
        BaseChild.preexec_first(self)

        # /bin/sh is used to execute system shell scripts.  the original executable and arguments are converted to a single
        # string with quoting properly escaped to prevent premature splitting of args.
        self.args = ['/bin/sh', '-c', convert_argv_to_quoted_command_string(self.args)]

    def preexec_last(self):
        BaseChild.preexec_last(self)


class SystemScriptForker (BaseForker):
    """
    Component for starting system script jobs such as the prologue and epilogue scripts run by cqm
    """
    
    name = __name__.split('.')[-1]
    implementation = name

    child_cls = SystemScriptChild

    logger = _logger

    def __init__ (self, *args, **kwargs):
        """
        Initialize a new system script forker.
        
        All arguments are passed to the base forker constructor.
        """
        BaseForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return BaseForker.__getstate__(self)

    def __setstate__(self, state):
        BaseForker.__setstate__(self, state)
