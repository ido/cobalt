import logging
import os
import pwd
import subprocess
import tempfile
import Cobalt.Components.pg_forker
PGPreexec = Cobalt.Components.pg_forker.PGPreexec
PGForker = Cobalt.Components.pg_forker.PGForker
import Cobalt.Util
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string

_logger = logging.getLogger(__name__)


class UserScriptPreexec(PGPreexec):
    def __init__(self, child, cmd_str, env):
        PGPreexec.__init__(self, child, cmd_str, env)

    def do_first(self):
        PGPreexec.do_first(self)

        # create a nodefile in /tmp
        try:
            tf = tempfile.NamedTemporaryFile()
            tf.write("\n".join(self.pg.location) + '\n')
            tf.flush()
            self.env['COBALT_NODEFILE'] = tf.name
            tf.close()
        except:
            _logger.error("%s: unable to create node file", self.label, exc_info=True)

    def do_last(self):
        PGPreexec.do_last(self)


class UserScriptForker (PGForker):
    """Component for starting script jobs"""
    
    name = "user_script_forker"
    # implementation = "generic"

    def __init__ (self, *args, **kwargs):
        """Initialize a new user script forker.
        
        All arguments are passed to the base forker constructor.
        """
        PGForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return PGForker.__getstate__(self)

    def __setstate__(self, state):
        PGForker.__setstate__(self, state)

    def _fork(self, child, data):
        PGForker._fork(self, child, data)
        pg = child.pg
        if data.has_key('nodect'):
            pg.nodect = data['nodect']
        else:
            pg.nodect = pg.size

        try:
            user_info = pwd.getpwnam(pg.user)
            shell = user_info.pw_shell
            homedir = user_info.pw_dir
        except:
            _logger.error("%s: unable to obtain information about user %s", child.label, pg.user)
            raise

        if pg.cwd:
            cwd = pg.cwd
        else:
            cwd = homedir

        postfork_env = {}
        postfork_env.update(pg.env)
        postfork_env['HOME'] = homedir
        postfork_env['USER'] = pg.user
        postfork_env["COBALT_PARTNAME"] = pg.partition
        postfork_env["COBALT_PARTSIZE"] = str(pg.nodect)
        postfork_env["COBALT_JOBSIZE"] = str(pg.size)
        # add the cobalt env vars last so as overwrite any value provided by the user
        self._add_cobalt_env_vars(child, postfork_env)

        # One last bit of mangling to prevent premature splitting of args
        # quote the argument strings so the shell doesn't eat them.
        cmd_str = convert_argv_to_quoted_command_string([child.cmd] + child.args)

        try:
            preexec_fn = UserScriptPreexec(child, cmd_str, postfork_env)
        except:
            _logger.error("%s: instantiation of preexec class failed; aborting execution")
            raise

        try:
            child.proc = subprocess.Popen(["-", "-c", cmd_str], executable=shell, cwd=cwd, preexec_fn=preexec_fn, env=postfork_env)
            child.pid = child.proc.pid
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
