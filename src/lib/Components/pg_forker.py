import grp
import os
import pwd
import sys
import Cobalt.DataTypes.ProcessGroup
ProcessGroup = Cobalt.DataTypes.ProcessGroup.ProcessGroup
import Cobalt.Components.base_forker
BaseForker = Cobalt.Components.base_forker.BaseForker
get_forker_config = Cobalt.Components.base_forker.get_forker_config

_scratch_dir = get_forker_config("scratch_dir", None)
if get_forker_config("ignore_setgroup_errors", "false") in ["true", "True", "TRUE", "1"]:
    _ignore_setgroup_errors = True
else:
    _ignore_setgroup_errors = False

class PGPreexec(object):
    '''Class for handling pre-exec tasks for a job.
    Initilaization takes a job-data object.  This allows id's to be set 
    properly and other bookkeeping tasks to be correctly set.

    '''

    def __init__(self, cmd_str, child, logger):
        self.cmd_str = cmd_str
        self.logger = logger
        self.pg = child.pg
        # self.label = "%s/%s" % (pg.jobid, pg.id)
        self.label = child.label

    def _open_input(self, filename, desc):
        in_file = None
        try:
            try:
                in_file = open(filename or "/dev/null", 'r')
            except (IOError, OSError, TypeError), e:
                self.logger.error("%s: error opening %s file %s; redirecting to /dev/null: %s", self.label, desc, filename, e)
                in_file = open("/dev/null", 'r')
        except Exception, e:
                self.logger.error("%s: an unexpected error occurred while opening input file %s: %s", self.label, filename, e)
        return in_file
    
    def _open_output(self, filename, scratch_filename, desc):
        out_file = None
        try:
            try:
                out_file = open(filename, 'a')
            except (IOError, OSError, TypeError), e:
                self.logger.error("%s: error opening %s file %s: %s", self.label, desc, filename, e)
                output_to_devnull = False
                if _scratch_dir:
                    try:
                        fn = os.path.join(_scratch_dir, scratch_filename)
                    except Exception, e:
                        self.logger.error("%s: unable to construct path to scratch file", self.label)
                        output_to_devnull = True
                    else:
                        try:
                            self.logger.error("%s: sending %s to scratch_dir %s", self.label, desc, fn)
                        except Exception, e:
                            self.logger.error("%s: error opening %s file %s: %s", self.label, desc, fn, e)
                            out_file = open(fn, 'a')
                            output_to_devnull = True
                else:
                    self.logger.error(
                        "%s: set the scratch_dir option in the [forker] section of cobalt.conf to salvage %s",
                        self.label, desc)
                    output_to_devnull = True
    
                if output_to_devnull:
                    out_file = open("/dev/null", 'a')
                    self.logger.error("%s: sending %s to /dev/null", self.label, desc)
        except Exception, e:
            self.logger.error("%s: an unexpected error occurred while opening output file %s: %s", self.label, filename, e)
        return out_file

    def _set_supplementary_groups(self, username):
        supplementary_group_ids = []
        for g in grp.getgrall():
            if username in g.gr_mem:
                supplementary_group_ids.append(g.gr_gid)
        try:
            os.setgroups([])
            os.setgroups(groups)
        except:
            self.logger.error("%s: failed to set supplementary groups for user %s", self.label, username)
            if not _ignore_setgroup_errors:
                raise

    def _set_uid_gid(self, username):
        try:
            uid, gid = pwd.getpwnam(username)[2:4]
        except KeyError:
            self.logger.error("%s: failed to get uid/gid for user %s", self.label, username)
            raise
        try:
            os.setgid(gid)
        except OSError:
            self.logger.error("%s: failed to change group id to %d", self.label, gid)
            raise
        try:
            os.setuid(uid)
        except OSError:
            self.logger.error("%s: failed to change user id to %d", self.label, uid)
            raise

    def _set_umask(self, umask):
        if umask != None:
            try:
                os.umask(umask)
            except:
                self.logger.error("%s: failed to set umask to %s", self.label, umask)

    def __call__(self):
        '''
        Set important bits for cobalt jobs and redirect files as needed.
        '''
        pg = self.pg
        label = self.label

        try:
            try:
                # only root can set the supplementary groups, so that must be done before the effective uid is changed
                self._set_supplementary_groups(pg.user)
                self._set_uid_gid(pg.user)
            except:
                self.logger.error("%s: failed to set user information; terminating task", self.label, exc_info=True)
                os._exit(1)

            self._set_umask(pg.umask)

            try:
                stdin = self._open_input(pg.stdin, "stdin")
                if stdin:
                    os.dup2(stdin.fileno(), sys.__stdin__.fileno())
            except Exception, e:
                self.logger.error("%s: an error occurred while redirecting stdin to file %s: %s", label, pg.stdin, e)
            try:
                stdout = self._open_output(pg.stdout, "%s.output" % (pg.jobid,), "stdout")
                if stdout:
                    os.dup2(stdout.fileno(), sys.__stdout__.fileno())
            except Exception, e:
                self.logger.error("%s: an error occurred while redirecting stdout to file %s: %s", label, pg.stdout, e)
            try:
                stderr = self._open_output(pg.stderr, "%s.error" % (pg.jobid,), "stderr")
                if stderr:
                    os.dup2(stderr.fileno(), sys.__stderr__.fileno())
            except Exception, e:
                self.logger.error("%s: an error occurred while redirecting stderr to file %s: %s", label, pg.stderr, e)

            try:
                cobalt_log_file = open(pg.cobalt_log_file, "a")
                if stdout == None or stdout.name != pg.stdout:
                    print >> cobalt_log_file, "failed to open %s" % (pg.stdout,)
                    if stdout != None:
                        print >> cobalt_log_file, "stdout sent to %s\n" % (stdout.name,)
                if stderr == None or stderr.name != pg.stderr:
                    print >> cobalt_log_file, "failed to open %s" % (pg.stderr,)
                    if stderr != None:
                        print >> cobalt_log_file, "stderr sent to %s\n" % (stderr.name,)
                print >> cobalt_log_file, "%s\n" % (self.cmd_str,)
                print >> cobalt_log_file, "called with environment:\n"
                for key in os.environ:
                    print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                print >> cobalt_log_file, "\n"
                cobalt_log_file.close()
            except:
                self.logger.error("%s: unable to open cobaltlog file %s", label, pg.cobalt_log_file, exc_info=True)
        except:
            self.logger.error("%s: Unhandled exception in PGPreexec.")
            raise


class PGForker (BaseForker):
    
    """Component for starting script jobs"""
    
    name = "pg_forker"
    # implementation = "generic"

    def __init__ (self, *args, **kwargs):
        """Initialize a new BG mpirun forker.
        
        All arguments are passed to the base forker constructor.
        """
        BaseForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return BaseForker.__getstate__(self)

    def __setstate__(self, state):
        BaseForker.__setstate__(self, state)

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
            self.logger.error("%s: no partition was specified", child.label)
            raise
