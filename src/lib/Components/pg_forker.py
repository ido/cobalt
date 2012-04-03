import grp
import logging
import os
import pwd
import sys

import Cobalt
import Cobalt.Components.base_forker
BaseForker = Cobalt.Components.base_forker.BaseForker
BaseChild = Cobalt.Components.base_forker.BaseChild
get_forker_config = Cobalt.Components.base_forker.get_forker_config
import Cobalt.DataTypes.ProcessGroup
ProcessGroup = Cobalt.DataTypes.ProcessGroup.ProcessGroup
import Cobalt.Util
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string

__all__ = [
    "PGForker",
    "PGChild",
]

_logger = logging.getLogger(__name__.split('.')[-1])

_scratch_dir = get_forker_config("scratch_dir", None)
if get_forker_config("ignore_setgroup_errors", "false") in ["true", "True", "TRUE", "1"]:
    _ignore_setgroup_errors = True
else:
    _ignore_setgroup_errors = False


class PGChild (BaseChild):
    '''Class for handling pre-exec tasks for a job.
    Initilaization takes a job-data object.  This allows id's to be set 
    properly and other bookkeeping tasks to be correctly set.

    '''

    def __init__(self, id = None, **kwargs):
        BaseChild.__init__(self, id=id, **kwargs)

        try:
            self.pg = ProcessGroup(kwargs['data'])
        except KeyError:
            _logger.error("process group data not provided to PGChild constructor")
            raise

        self.cwd = self.pg.cwd
        self.umask = self.pg.umask
        self.cobalt_log_filename = self.pg.cobalt_log_file

        self.cmd_string = None

    def __getstate__(self):
        state = {}
        state.update(BaseChild.__getstate__(self))
        # BaseChild.__getstate__ copies __dict__ and thus automatically acquires what PGChild needs
        return state

    def __setstate__(self, state):
        BaseChild.__setstate__(self, state)

    def _open_input(self, filename, desc):
        in_file = None
        try:
            try:
                in_file = open(filename or "/dev/null", 'r')
            except (IOError, OSError, TypeError), e:
                _logger.error("%s: unable to open %s file %s; redirecting to /dev/null: %s", self.label, desc, filename, e)
                self.print_clf_error("unable to open %s file %s; redirecting to /dev/null: %s", desc, filename, e)
                in_file = open("/dev/null", 'r')
        except Exception, e:
                _logger.error("%s: an unexpected exception occurred while opening %s file %s: %s", self.label, desc, filename, e)
                self.print_clf_error("an unexpected exception occurred while opening %s file %s: %s", desc, filename, e)
        return in_file
    
    def _open_output(self, filename, scratch_filename, desc):
        out_file = None
        try:
            try:
                out_file = open(filename, 'a')
            except (IOError, OSError, TypeError), e:
                _logger.error("%s: error opening %s file %s: %s", self.label, desc, filename, e)
                self.print_clf_error("error opening %s file %s: %s", desc, filename, e)
                output_to_devnull = False
                if _scratch_dir:
                    try:
                        fn = os.path.join(_scratch_dir, scratch_filename)
                    except Exception, e:
                        _logger.error("%s: unable to construct path to scratch file", self.label)
                        self.print_clf_error("unable to construct path to scratch file")
                        output_to_devnull = True
                    else:
                        try:
                            out_file = open(fn, 'a')
                            _logger.warning("%s: sending %s to scratch_dir %s", self.label, desc, fn)
                            self.print_clf_warning("sending %s to scratch_dir %s", desc, fn)
                        except Exception, e:
                            _logger.error("%s: unable to open secondary %s file %s: %s", self.label, desc, fn, e)
                            self.print_clf_error("unable to open secondary %s file %s: %s", desc, fn, e)
                            output_to_devnull = True
                else:
                    _logger.warning("%s: set the scratch_dir option in the [forker] section of cobalt.conf to salvage %s",
                        self.label, desc)
                    output_to_devnull = True
    
                if output_to_devnull:
                    out_file = open("/dev/null", 'a')
                    _logger.warning("%s: sending %s to /dev/null", self.label, desc)
                    self.print_clf_warning("sending %s to /dev/null", desc)
        except Exception, e:
            _logger.error("%s: an unexpected exception occurred while opening %s file %s: %s", self.label, desc, filename, e)
            self.print_clf_error("an unexpected exception occurred while opening %s file %s: %s", desc, filename, e)
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

        self._open_clf(uid=uid, gid=gid)

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

    def preexec_first(self):
        '''
        Set important bits for cobalt jobs and redirect files as needed.
        '''

        BaseChild.preexec_first(self)

        try:
            # only root can set the supplementary groups, so that must be done before the effective uid is changed
            self._set_supplementary_groups(self.pg.user)
            self._set_uid_gid(self.pg.user)
        except:
            _logger.error("%s: failed to set user and group information; terminating task", self.label)
            self.print_clf_error("failed to set the process' user and group information")
            raise

        try:
            self.stdin_file = self._open_input(self.pg.stdin, "stdin")
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stdin to file %s: %s", self.label, self.pg.stdin, e)
            self.print_clf_error("unable to redirect stdin from file %s: %s", self.pg.stdin, e)
        try:
            self.stdout_file = self._open_output(self.pg.stdout, "%s.output" % (self.pg.jobid,), "stdout")
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stdout to file %s: %s", self.label, self.pg.stdout, e)
            self.print_clf_error("unable to redirect stdout to file %s: %s", self.pg.stdout, e)
        try:
            self.stderr_file = self._open_output(self.pg.stderr, "%s.error" % (self.pg.jobid,), "stderr")
        except Exception, e:
            _logger.error("%s: an error occurred while redirecting stderr to file %s: %s", self.label, self.pg.stderr, e)
            self.print_clf_error("unable to redirect stderr to file %s: %s", self.pg.stderr, e)

    def preexec_last(self):
        # COBALT_JOBID and COBALT_RESID are special and must be part of the mpirun environment and the environment of any script
        # invoking mpirun.  they are added to the environment last so any values provided by the user are overwritten
        self.env['COBALT_JOBID'] = str(self.pg.jobid)
        if self.pg.resid != None:
            self.env['COBALT_RESID'] = str(self.pg.resid)

        self.print_clf("")
        self.print_clf("Command: %s", self.cmd_string or convert_argv_to_quoted_command_string(self.args))
        self.print_clf("")
        self.print_clf("Environment:")
        for key in self.env:
            self.print_clf("%s=%s", key, self.env[key])
        self.print_clf("")

        BaseChild.preexec_last(self)


class PGForker (BaseForker):
    
    """Component for starting script jobs"""
    
    # name = __name__.split('.')[-1]
    # implementation = name

    def __init__ (self, *args, **kwargs):
        """Initialize a new BG mpirun forker.
        
        All arguments are passed to the base forker constructor.
        """
        global _logger
        _logger = self.logger

        BaseForker.__init__(self, *args, **kwargs)
        
    def __getstate__(self):
        state = {}
        state.update(BaseForker.__getstate__(self))
        return state

    def __setstate__(self, state):
        global _logger
        _logger = self.logger

        BaseForker.__setstate__(self, state)

