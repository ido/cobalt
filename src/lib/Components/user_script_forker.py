import logging
import os
import pwd
import tempfile

import Cobalt
import Cobalt.Components.pg_forker
PGChild = Cobalt.Components.pg_forker.PGChild
PGForker = Cobalt.Components.pg_forker.PGForker
import Cobalt.Util
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string

_logger = logging.getLogger(__name__.split('.')[-1])


class UserScriptChild (PGChild):
    def __init__(self, id = None, **kwargs):
        PGChild.__init__(self, id=id, **kwargs)

        try:
            self.bg_partition = self.pg.location[0]
        except IndexError:
            _logger.error("%s: no partition was specified", self.label)
            raise

        data = kwargs['data']
        if data.has_key('nodect'):
            self.pg.nodect = data['nodect']
        else:
            self.pg.nodect = self.pg.size

    def __getstate__(self):
        state = {}
        state.update(PGChild.__getstate__(self))
        return state

    def __setstate__(self, state):
        PGChild.__setstate__(self, state)

    def preexec_first(self):
        PGChild.preexec_first(self)

        try:
            user_info = pwd.getpwnam(self.pg.user)
            shell = user_info.pw_shell
            homedir = user_info.pw_dir
        except:
            _logger.error("%s: unable to obtain account information for user %s", self.label, self.pg.user)
            self.print_clf_error("unable to obtain account information for user %s", self.pg.user)
            raise

        if not self.cwd:
            self.cwd = homedir

        self.env = {}
        self.env.update(self.pg.env)
        self.env['HOME'] = homedir
        self.env['USER'] = self.pg.user
        self.env['LOGNAME'] = self.pg.user
        self.env['SHELL'] = shell
        self.env["COBALT_PARTNAME"] = self.bg_partition
        self.env["COBALT_PARTSIZE"] = str(self.pg.nodect)
        self.env["COBALT_JOBSIZE"] = str(self.pg.size)

        # create a nodefile in /tmp
        try:
            tf = tempfile.NamedTemporaryFile()
            tf.write("\n".join(self.pg.location) + '\n')
            tf.flush()
            self.env['COBALT_NODEFILE'] = tf.name
            tf.close()
        except:
            _logger.error("%s: unable to create node file", self.label, exc_info=True)

        # One last bit of mangling to prevent premature splitting of args
        # quote the argument strings so the shell doesn't eat them.
        self.cmd_string = convert_argv_to_quoted_command_string(self.args)
        self.exe = shell
        self.args = ["-", "-c", "exec " + self.cmd_string]

    def preexec_last(self):
        PGChild.preexec_last(self)


class UserScriptForker (PGForker):
    """Component for starting script jobs"""

    name = __name__.split('.')[-1]
    implementation = name

    child_cls = UserScriptChild

    logger = _logger

    def __init__ (self, *args, **kwargs):
        """Initialize a new user script forker.
        
        All arguments are passed to the base forker constructor.
        """
        PGForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return PGForker.__getstate__(self)

    def __setstate__(self, state):
        PGForker.__setstate__(self, state)
