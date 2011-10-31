import grp
import logging
import os
import pwd
import sys
import Cobalt.DataTypes.ProcessGroup
ProcessGroup = Cobalt.DataTypes.ProcessGroup.ProcessGroup
import Cobalt.Components.base_forker
BaseForker = Cobalt.Components.base_forker.BaseForker
BasePreexec = Cobalt.Components.base_forker.BasePreexec
get_forker_config = Cobalt.Components.base_forker.get_forker_config

__all__ = [
    "PGForker",
    "PGPreexec",
]

_logger = logging.getLogger(__name__.split('.')[-1])

_scratch_dir = get_forker_config("scratch_dir", None)
if get_forker_config("ignore_setgroup_errors", "false") in ["true", "True", "TRUE", "1"]:
    _ignore_setgroup_errors = True
else:
    _ignore_setgroup_errors = False


class PGPreexec(BasePreexec):
    '''Class for handling pre-exec tasks for a job.
    Initilaization takes a job-data object.  This allows id's to be set 
    properly and other bookkeeping tasks to be correctly set.

    '''

    def __init__(self, child, cmd_str, env):
        BasePreexec.__init__(self, child)
        self.cmd_str = cmd_str
        self.env = env
        self.pg = child.pg
        self.cobalt_log_file = None
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def _open_input(self, filename, desc):
        in_file = None
        try:
            try:
                in_file = open(filename or "/dev/null", 'r')
            except (IOError, OSError, TypeError), e:
                _logger.error("%s: error opening %s file %s; redirecting to /dev/null: %s", self.label, desc, filename, e)
                in_file = open("/dev/null", 'r')
        except Exception, e:
                _logger.error("%s: an unexpected error occurred while opening input file %s: %s", self.label, filename, e)
        return in_file
    
    def _open_output(self, filename, scratch_filename, desc):
        out_file = None
        try:
            try:
                out_file = open(filename, 'a')
            except (IOError, OSError, TypeError), e:
                _logger.error("%s: error opening %s file %s: %s", self.label, desc, filename, e)
                output_to_devnull = False
                if _scratch_dir:
                    try:
                        fn = os.path.join(_scratch_dir, scratch_filename)
                    except Exception, e:
                        _logger.error("%s: unable to construct path to scratch file", self.label)
                        output_to_devnull = True
                    else:
                        try:
                            _logger.error("%s: sending %s to scratch_dir %s", self.label, desc, fn)
                        except Exception, e:
                            _logger.error("%s: error opening %s file %s: %s", self.label, desc, fn, e)
                            out_file = open(fn, 'a')
                            output_to_devnull = True
                else:
                    _logger.error(
                        "%s: set the scratch_dir option in the [forker] section of cobalt.conf to salvage %s",
                        self.label, desc)
                    output_to_devnull = True
    
                if output_to_devnull:
                    out_file = open("/dev/null", 'a')
                    _logger.error("%s: sending %s to /dev/null", self.label, desc)
        except Exception, e:
            _logger.error("%s: an unexpected error occurred while opening output file %s: %s", self.label, filename, e)
        return out_file

    def _set_supplementary_groups(self, username):
        supplementary_group_ids = []
        for g in grp.getgrall():
            if username in g.gr_mem:
                supplementary_group_ids.append(g.gr_gid)
        try:
            os.setgroups([])
            os.setgroups(supplementary_group_ids)
        except:
            _logger.error("%s: failed to set supplementary groups for user %s", self.label, username)
            if not _ignore_setgroup_errors:
                raise

    def _set_uid_gid(self, username):
        try:
            uid, gid = pwd.getpwnam(username)[2:4]
        except KeyError:
            _logger.error("%s: failed to get uid/gid for user %s", self.label, username)
            raise
        try:
            os.setgid(gid)
        except OSError:
            _logger.error("%s: failed to change group id to %d", self.label, gid)
            raise
        try:
            os.setuid(uid)
        except OSError:
            _logger.error("%s: failed to change user id to %d", self.label, uid)
            raise

    def _set_umask(self, umask):
        if umask != None:
            try:
                os.umask(umask)
            except:
                _logger.error("%s: failed to set umask to %s", self.label, umask)

    def print_clf(self, fmt, *args):
        if self.cobalt_log_file:
            try:
                print >>self.cobalt_log_file, fmt % args
            except:
                _logger.error("%s: unable to write to cobaltlog file %s", self.label, self.pg.cobalt_log_file, exc_info=True)

    def do_first(self):
        '''
        Set important bits for cobalt jobs and redirect files as needed.
        '''

        BasePreexec.do_first(self)

        try:
            self.cobalt_log_file = open(self.pg.cobalt_log_file, "a")
        except:
            _logger.error("%s: unable to open cobaltlog file %s", self.label, self.pg.cobalt_log_file, exc_info=True)

        try:
            # only root can set the supplementary groups, so that must be done before the effective uid is changed
            self._set_supplementary_groups(self.pg.user)
            self._set_uid_gid(self.pg.user)
        except:
            _logger.error("%s: failed to set user information; terminating task", self.label, exc_info=True)
            os._exit(255)

        self._set_umask(self.pg.umask)

        try:
            self.stdin = self._open_input(self.pg.stdin, "stdin")
            if self.stdin:
                os.dup2(self.stdin.fileno(), sys.__stdin__.fileno())
                self.stdin.close()
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stdin to file %s: %s", self.label, self.pg.stdin, e)
            self.print_clf("ERROR: unable to redirect stdin to file %s: %s", self.pg.stdin, e)
        try:
            self.stdout = self._open_output(self.pg.stdout, "%s.output" % (self.pg.jobid,), "stdout")
            if self.stdout:
                os.dup2(self.stdout.fileno(), sys.__stdout__.fileno())
                self.stdout.close()
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stdout to file %s: %s", self.label, self.pg.stdout, e)
            self.print_clf("ERROR: unable to redirect stdout to file %s: %s", self.pg.stdout, e)
        try:
            self.stderr = self._open_output(self.pg.stderr, "%s.error" % (self.pg.jobid,), "stderr")
            # skip redirection of stderr until the end so that log messages are still send to the component's stderr
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stderr to file %s: %s", self.label, self.pg.stderr, e)
            self.print_clf("%s: an error occurred while redirecting stderr to file %s: %s", self.label, self.pg.stderr, e)
        if self.stdout:
            self.print_clf("Info: stdout sent to %s", self.stdout.name)
        if self.stderr:
            self.print_clf("Info: stderr sent to %s", self.stderr.name)
        if self.stdout or self.stderr:
            self.print_clf("")

    def do_last(self):
        self.print_clf("Command: %s\n", self.cmd_str)
        self.print_clf("Environment:")
        if self.env:
            env = self.env
        else:
            env = os.environ
        for key in env:
            self.print_clf("%s=%s", key, env[key])
        self.print_clf("")

        try:
            if self.stderr:
                os.dup2(self.stderr.fileno(), sys.__stderr__.fileno())
                self.stderr.close()
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stderr to file %s: %s", self.label, self.pg.stderr, e)
            self.print_clf("ERROR: unable to redirect stderr to file %s: %s", self.pg.stderr, e)

        try:
            self.cobalt_log_file.close()
        except:
            pass

        BasePreexec.do_last(self)


class PGForker (BaseForker):
    
    """Component for starting script jobs"""
    
    # name = __name__.split('.')[-1]
    # implementation = name

    def __init__ (self, *args, **kwargs):
        """Initialize a new BG mpirun forker.
        
        All arguments are passed to the base forker constructor.
        """
        BaseForker.__init__(self, *args, **kwargs)
        
        global _logger
        _logger = self.logger

    def __getstate__(self):
        return BaseForker.__getstate__(self)

    def __setstate__(self, state):
        BaseForker.__setstate__(self, state)

        global _logger
        _logger = self.logger

    def _add_cobalt_env_vars(self, child, postfork_env):
        #COBALT_JOBID and COBALT_RESID are special and must be passed to
        #the mpirun environment.
        postfork_env['COBALT_JOBID'] = str(child.pg.jobid)
        if child.pg.resid != None:
            postfork_env['COBALT_RESID'] = str(child.pg.resid)

    def _fork(self, child, data):
        child.pg = ProcessGroup(data)
        child.ignore_output = True
        try:
            child.pg.partition = child.pg.location[0]
        except IndexError:
            _logger.error("%s: no partition was specified", child.label)
            raise
