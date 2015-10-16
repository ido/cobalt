import logging
import os
import pwd
import tempfile
import signal

import Cobalt
import Cobalt.Components.pg_forker
PGChild = Cobalt.Components.pg_forker.PGChild
PGForker = Cobalt.Components.pg_forker.PGForker
import Cobalt.Util
exposed = Cobalt.Components.base.exposed
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
        if os.environ.has_key('COBALT_CONFIG_FILES'):
            self.env['COBALT_CONFIG_FILES'] = os.environ['COBALT_CONFIG_FILES']
        if os.environ.has_key('COBALT_SOURCE_DIR'):
            self.env['COBALT_SOURCE_DIR'] = os.environ['COBALT_SOURCE_DIR']
        if os.environ.has_key('COBALT_RUNTIME_DIR'):
            self.env['COBALT_RUNTIME_DIR'] = os.environ['COBALT_RUNTIME_DIR']

        if self.pg.subblock == True:
            self.env["COBALT_SUBBLOCK"] = str(self.pg.subblock)
            self.env["COBALT_PARTNAME"] = self.pg.subblock_parent
            self.env["COBALT_CORNER"] = self.pg.corner
            self.env["COBALT_SHAPE"] = "x".join([str(ext) for ext in self.pg.extents])

            #TODO: Have to add better env variables to describe what you're getting shape-wise
            # This is a must-do for Mira


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

    def signal(self, signum, pg=True):
        _logger.info('Data has: %s', self.pg)
        if self.pg.attrs.has_key('nopgkill'):
            pg = False
        PGChild.signal(self, signum, pg)



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

    def signal(self, child_id, signame):
        """
        Signal a child process.
        
        Arguments:
        child_id -- id of the child to signal
        signame -- signal name
        """

        _logger.debug("Using overridden signal method.")

        if not self.children.has_key(child_id):
            _logger.error("Child %s: child not found; unable to signal", child_id)
            return

        try:
            signum = getattr(signal, signame)
        except AttributeError:
            _logger.error("%s: %s is not a valid signal name; child not signaled", child.label, signame)
            raise
        pg = True
        if self.children[child_id].pg.attrs.has_key('nopgkill'):
            pg = False
        super(UserScriptChild, self.children[child_id]).signal(signum, pg=pg)

    signal = exposed(signal) 
