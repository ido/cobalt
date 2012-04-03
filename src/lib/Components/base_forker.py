"""Implementations of the forker component.

Classes:
BaseForker -- generic implementation

The forker component provides a single threaded component which can safely
fork new processes.

"""

import copy
import errno
import fcntl
import gc
import logging
import os
import signal
import sys
import ConfigParser

import Cobalt
import Cobalt.Components.base
Component = Cobalt.Components.base.Component
exposed = Cobalt.Components.base.exposed
automatic = Cobalt.Components.base.automatic
import Cobalt.Data
IncrID = Cobalt.Data.IncrID
import Cobalt.Statistics
Statistics = Cobalt.Statistics.Statistics
import Cobalt.Util
sleep = Cobalt.Util.sleep
Timer = Cobalt.Util.Timer

__all__ = [
    "BaseForker",
    "BaseChild"
]

_logger = logging.getLogger(__name__.split('.')[-1])

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

def get_forker_config(option, default):
    try:
        value = config.get('forker', option)
    except Exception, e:
        if isinstance(e, ConfigParser.NoSectionError):
            _logger.info("[forker] section missing from cobalt.conf")
            value = default
        elif isinstance(e, ConfigParser.NoOptionError):
            value = default
        else:
            raise e
    return value


class BaseChild (object):
    '''Base class for child processes.'''

    id_gen = IncrID()

    def __init__(self, id=None, **kwargs):
        if id:
            self.id = id
        else:
            self.id = self.id_gen.next()
        if kwargs.has_key('args'):
            self.args = kwargs['args']
        else:
            self.args = None
        if kwargs.has_key('env'):
            self.env = kwargs['env']
        else:
            self.env = None
        if kwargs.has_key('tag'):
            self.tag = kwargs['tag']
        else:
            self.tag = None
        if kwargs.has_key('cwd'):
            self.cwd = kwargs['cwd']
        else:
            self.cwd = None
        if kwargs.has_key('umask'):
            self.umask = kwargs['umask']
        else:
            self.umask = None
        if kwargs.has_key('runid'):
            self.runid = kwargs['runid']
        else:
            self.runid = None
        if kwargs.has_key('label_prefix'):
            self.label = "%s/%s" % (kwargs['label_prefix'], self.id)
        else:
            self.label = "Child %s" % (self.id,)

        self.exe = None

        self.pid = None

        self.stdin_file = None
        self.stdout_file = None
        self.stdout_data = None
        self.stderr_file = None
        self.stderr_data = None
        self.return_output = False

        self.complete = False
        self.lost_child = False
        self.exit_status = None
        self.signum = 0
        self.core_dump = False
        self.termination_timer = None

        if kwargs.has_key('log_filename'):
            self.cobalt_log_filename = kwargs['log_filename']
        else:
            self.cobalt_log_filename = None
        self._cobalt_log_file = None
        self._cobalt_log_failed = False
        self._cobalt_log_reporting_errors = False
        self._cobalt_log_have_blank_line = False
    
    def __getstate__(self):
        '''
        Return the data to be pickled or copied (via copy.copy).  The standard I/O file objects are removed since they cannot be
        pickled.
        '''
        state = copy.copy(self.__dict__)
        state['base_forker_version'] = 2
        del state['stdin_file']
        del state['stdout_file']
        del state['stderr_file']
        del state['_cobalt_log_file']
        return state

    def __setstate__(self, state):
        '''
        Restore object using state return from __getstate__.  Since UNIX provides no mechanism to reattach to a child, the child
        is marked as lost if the component had not already been notified of the child's completion.  The standard I/O file
        objects are cleared since it was not possible to pickle them.
        '''
        if not state.has_key('base_forker_version') or state['base_forker_version'] < 2:
            raise Exception(("The state file for the %s component is incompatible with the current implementation.  Please " +
                "remove the state file and try again.") % (self.implementation,))
        self.__dict__.update(state)
        self.stdin_file = None
        self.stdout_file = None
        self.stderr_file = None
        self._cobalt_log_file = None
        self._cobalt_log_failed = False
        if not self.complete:
            self.lost_child = True
            self.return_output = False
            self.complete = True

    def export_state(self):
        d = {}
        d['id'] = self.id
        d['args'] = self.args
        d['env'] = self.env
        d['tag'] = self.tag
        d['runid'] = self.runid
        d['label'] = self.label
        if self.return_output:
            d['stdout'] = self.stdout_data
            d['stderr'] = self.stderr_data
        d['complete'] = self.complete
        d['lost_child'] = self.lost_child
        d['exit_status'] = self.exit_status
        d['signum'] = self.signum
        d['core_dump'] = self.core_dump
        return d

    def _open_clf(self, uid=None, gid=None):
        if not self._cobalt_log_file and self.cobalt_log_filename and not self._cobalt_log_failed:
            try:
                _logger.debug("%s: opening the cobaltlog file: %s", self.label, self.cobalt_log_filename)
                self._cobalt_log_file = open(self.cobalt_log_filename, "a", 1)
                try:
                    flags = fcntl.fcntl(self._cobalt_log_file.fileno(), fcntl.F_GETFD)
                    fcntl.fcntl(self._cobalt_log_file.fileno(), fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
                except OSError, e:
                    _logger.warning("%s: failed to set the close-on-exec flag for the cobaltlog file: fd=%s",
                        self.label, self._cobalt_log_file.fileno())
            except (IOError, OSError), e:
                _logger.error("%s: unable to open the cobaltlog file %s: %s", self.label, self.cobalt_log_filename, e)
                self._cobalt_log_failed = True
            except:
                _logger.error("%s: unable to open the cobaltlog file %s", self.label, self.cobalt_log_filename, exc_info=True)
                self._cobalt_log_failed = True

        if uid and gid:
            try:
                _logger.debug("%s: determining if uid and gid of the cobaltlog file need to be reset", self.label)
                clf_uid = -1
                clf_gid = -1
                proc_uid = os.geteuid()
                proc_gid = os.getegid()
                # if the specified user is different than the effective user of the current process, then set the file's user to
                # the one specified
                if uid != proc_uid:
                    clf_uid = uid
                # if specified group is different than the effective group of the current process and the directory containing
                # the cobaltlog file is not setgid, then set the file's group to the one specified
                if gid != proc_gid:
                    try:
                        cld_info = os.stat(os.path.dirname(self.cobalt_log_filename) or os.path.curdir)
                        if not cld_info.st_mode & 02000:
                            clf_gid = gid
                    except OSError:
                        _logger.warning("%s: failed to get info on the directory containing the cobaltlog file %s: %s",
                            self.label, os.path.dirname(self.cobalt_log_filename) or os.path.curdir, e)
                        pass
                if clf_uid > 0 or clf_gid > 0:
                    _logger.warning("%s: setting ownership of the cobaltlog file %s: uid=%s, gid=%s",
                        self.label, self.cobalt_log_filename, clf_uid, clf_gid)
                    os.fchown(self._cobalt_log_file.fileno(), clf_uid, clf_gid)
            except OSError, e:
                _logger.error("%s: failed to set ownership of the cobaltlog file %s: %s", self.label, self.cobalt_log_filename, e)
            except:
                _logger.error("%s: failed to set ownership of the cobaltlog file %s", self.label, self.cobalt_log_filename,
                    exc_info=True)
            

    def print_clf_info(self, fmt, *args):
        self.print_clf("Info: " + fmt, *args)
    
    def print_clf_warning(self, fmt, *args):
        self.print_clf("WARNING: " + fmt, *args, error=True)
    
    def print_clf_error(self, fmt, *args):
        self.print_clf("ERROR: " + fmt, *args, error=True)

    def print_clf(self, fmt, *args, **kwargs):
        if not self._cobalt_log_file:
            self._open_clf()
        if self._cobalt_log_file and not self._cobalt_log_failed:
            if fmt == "":
                self._cobalt_log_have_blank_line = True
            try:
                if kwargs.has_key('error') and kwargs['error']:
                    if not self._cobalt_log_reporting_errors:
                        if not self._cobalt_log_have_blank_line:
                            print >>self._cobalt_log_file, ""
                            self._cobalt_log_have_blank_line = True
                        self._cobalt_log_reporting_errors = True
                elif self._cobalt_log_reporting_errors:
                    if not self._cobalt_log_have_blank_line:
                        print >>self._cobalt_log_file, ""
                        self._cobalt_log_have_blank_line = True
                    self._cobalt_log_reporting_errors = False
                print >>self._cobalt_log_file, fmt % args
                if fmt != "":
                    self._cobalt_log_have_blank_line = False
            except (IOError, OSError), e:
                _logger.error("%s: unable to write to cobaltlog file %s: %s", self.label, self.cobalt_log_filename, e)
                self._cobalt_log_failed = True
            except:
                _logger.error("%s: unable to write to cobaltlog file %s", self.label, self.cobalt_log_filename, exc_info=True)
                self._cobalt_log_failed = True

    def preexec_first(self):
        try:
            os.setsid()
            _logger.debug("%s: session id set to %s", self.label, os.getsid(os.getpid()))
        except Exception, e:
            _logger.error("%s: setting the process group and session id failed: %s", self.label, e)
            raise

    def preexec_last(self):
        if self.cwd:
            try:
                _logger.debug("%s: setting current working directory to %s", self.label, self.cwd)
                os.chdir(self.cwd)
            except OSError, e:
                _logger.error("%s: unable to change to the current working directory to \"%s\"", self.label, self.cwd)
                self.print_clf_error("unable to change to the current working directory to \"%s\"; terminating job", self.cwd)
                raise

        if self.umask != None:
            try:
                _logger.debug("%s: setting umask to %s", self.label, self.umask)
                os.umask(self.umask)
            except:
                _logger.error("%s: failed to set umask to %s", self.label, self.umask)
                self.print_clf_error("failed to set umask to %s", self.umask)

        if self.stdin_file:
            _logger.debug("%s: redirecting stdin", self.label)
            try:
                os.dup2(self.stdin_file.fileno(), sys.__stdin__.fileno())
                self.stdin_file.close()
            except Exception, e:
                _logger.error("%s: unable to redirect file %s to stdin: %s", self.label, self.stdin_file.name, e)
                self.print_clf_error("unable to redirect file %s to stdin: %s", self.stdin_file.name, e)
                self.stdin_file = None
        if self.stdout_file:
            _logger.debug("%s: redirecting stdout", self.label)
            try:
                os.dup2(self.stdout_file.fileno(), sys.__stdout__.fileno())
                self.stdout_file.close()
            except Exception, e:
                _logger.error("%s: unable to redirect stdout to file %s: %s", self.label, self.stdout_file.name, e)
                self.print_clf_error("unable to redirect stdout to file %s: %s", self.stdout_file.name, e)
                self.stdout_file = None
        if self.stderr_file:
            try:
                # if we are about to redirect the stderr file descriptor currently used by a logging handler, then create a new
                # file object from a duplicate stderr descriptor and assign it to the logging handler.  we do this so that log
                # messages are still sent to the component's stderr.
                new_stderr_file = None
                for handler in _logger.handlers:
                    if isinstance(handler, logging.StreamHandler):
                        _logger.debug("%s: found logging handler using fd %s, stderr_fd=%s",
                             self.label, handler.stream.fileno(), sys.__stderr__.fileno())
                        if not handler.stream.fileno() == sys.__stderr__.fileno():
                            continue
                        if not new_stderr_file:
                            try:
                                _logger.debug("%s: dupping stderr fd for logging", self.label)
                                new_stderr_file = os.fdopen(os.dup(sys.__stderr__.fileno()), "a", 0)
                                flags = fcntl.fcntl(new_stderr_file.fileno(), fcntl.F_GETFD)
                                fcntl.fcntl(new_stderr_file.fileno(), fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
                            except OSError:
                                pass
                        if new_stderr_file:
                            handler.stream.flush()
                            handler.stream = new_stderr_file
                _logger.debug("%s: redirecting stderr", self.label)
                os.dup2(self.stderr_file.fileno(), sys.__stderr__.fileno())
                self.stderr_file.close()
            except Exception, e:
                _logger.error("%s: unable to redirect stderr to file %s: %s", self.label, self.stderr_file.name, e)
                self.print_clf_error("unable to redirect stderr to file %s: %s", self.stderr_file.name, e)
                self.stderr_file = None
        if self.stdin_file:
            self.print_clf_info("stdin received from %s", self.stdin_file.name)
        if self.stdout_file:
            self.print_clf_info("stdout sent to %s", self.stdout_file.name)
        if self.stderr_file:
            self.print_clf_info("stderr sent to %s", self.stderr_file.name)
        if self.stdout_file or self.stderr_file:
            self.print_clf("")

    def start(self):
        _logger.debug("%s: forking process", self.label)
        try:
            gc_enabled = gc.isenabled()
            gc.disable()
            try:
                self.pid = os.fork()
            except OSError, e:
                _logger.error("%s: fork failed: %s", self.label, e.strerror)
                raise
        finally:
            if gc_enabled:
                gc.enable()
        if self.pid != 0:
            return

        _logger.debug("%s: child process created: pid=%s", self.label, os.getpid())

        try:
            self.preexec_first()
            self.preexec_last()
        except:
            _logger.error("%s: pre-exec function failed; terminating job", self.label, exc_info = True)
            self.print_clf_error("forker's pre-exec methods failed; terminating job")
            os._exit(255)

        if not self.exe:
            self.exe = self.args[0]

        if self._cobalt_log_file:
            self._cobalt_log_file.flush()

        try:
            if self.env is None:
                os.execvp(self.exe, self.args)
            else:
                os.execvpe(self.exe, self.args, self.env)
        except Exception, e:
            msg = ": %s" % (str(e),)
        else:
            msg = ""
        _logger.error("%s: exec() failed to start process%s", self.label, msg)
        self.print_clf_error("exec() failed to start process%s", msg)
        if self._cobalt_log_file:
            self._cobalt_log_file.flush()
        os._exit(255)

    _signum_map = {}
    for s in signal.__dict__:
        if isinstance(s, str) and s[0:3] == 'SIG':
            _signum_map[signal.__dict__[s]] = s

    def signal(self, signum, pg=False):
        try:
            signame = self._signum_map[signum]
        except KeyError:
            signame = str(signum)
        try:
            if pg:
                _logger.info("%s: sending signal %s to process group %s", self.label, signame, self.pid)
                os.killpg(self.pid, signum)
            else:
                _logger.info("%s: sending signal %s to pid %s", self.label, signame, self.pid)
                os.kill(self.pid, signum)
        except OSError, e:
            _logger.error("%s: signal failure: %s", self.label, e)
            raise

            
class BaseForker (Component):
    
    """Generic implementation of the service-location component.
    
    Methods:
    fork -- takes a dictionary specifying parameters for the forked task (exposed)
    signal -- signal a child with the specified signame (exposed)
    active_list -- retrieve a list of children which are still running (exposed)
    get_status -- return a dictionary of status information for a finished process (exposed)
    wait -- wait on children and record their status (automatic)
    """
    
    # name = __name__.split('.')[-1]
    # implementation = name

    child_cls = None

    UNKNOWN_ERROR = 256
    DEATH_TIMEOUT = 300 # seconds
    
    __statefields__ = ['next_task_id', 'children']

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)

        global _logger
        _logger = self.logger

        self.children = {}
        self.active_runids = []
        self.marked_for_death = {}

    def __getstate__(self):
        state = {}
        state.update(Component.__getstate__(self))
        state.update({
                'base_forker_version': 2,
                'next_task_id': BaseChild.id_gen.idnum+1,
                'children': self.children,
                'active_runids': self.active_runids,
                'marked_for_death': self.marked_for_death})
        return state
   
    def __setstate__(self, state):
        Component.__setstate__(self, state)

        global _logger
        _logger = self.logger

        if not state.has_key('base_forker_version') or state['base_forker_version'] < 2:
            _logger.error("The state file for the %s component is incompatible with the current implementation.  Please " +
                "remove the state file and try again.", self.implementation)
            os._exit(1)

        BaseChild.id_gen = IncrID()
        BaseChild.id_gen.set(state['next_task_id'])
        if state.has_key('children'):
            self.children = state['children']
        else:
            self.children = []
        if state.has_key('active_runids'):
            self.active_runids = state['active_runids']
        else:
            self.active_runids = []
        if state.has_key('marked_for_death'):
            self.marked_for_death = state['marked_for_death']
        else:
            self.marked_for_death = {}

    def __save_me(self):
        '''Periodically save off a statefile.'''
        Component.save(self)
    __save_me = automatic(__save_me, float(get_forker_config('save_me_interval', 10)))
        
    def fork(self, args, tag=None, label=None, env=None, preexec_data=None, runid=None):
        """Fork a child task.  
        args -- A list of strings: the command and relevant arguments.
        tag -- a tag identifying the type of job, such as a script
        label -- a label for logger lines.  Somehthing like "<jobid>/<pgid>"
        env -- A mapping of environemnt variables to be included in the child's
        environment. 
        data -- user data to interpreted by a more specialized forker
        runid -- an indentifier generated by the client and used by forker to
        prevent starting a task multiple times during XML-RPC communication
        failure / retry scenarios.

        returns the forker id of the child process object.

        """

        _logger.info("fork called with args of %s", " ".join(args))

        try:
            #make sure that a job isn't retrying because the XML-RPC hung.
            if (runid != None) and (runid in self.active_runids):
                _logger.warning("%s: Attempting to start a task that is "\
                        "already running. Returning running child id." % label)
                for child,child_obj in self.children.iteritems():
                    if child_obj.runid == runid:
                        return child_obj.id 
    
            # os.environ silently calls putenv().  It also shallow-copies.
            # I'm checking here to make sure user-environments don't leak
            # back into forker's environment.  --PMR
            
            #only should do this for user jobs, we're not using this for
            #helper scripts.
            orig_env = copy.deepcopy(os.environ)
            child_env_dict = copy.deepcopy(os.environ.data)

            child = None
            try:
                child = self.child_cls(label_prefix=label, tag=tag, args=args, env=env, runid=runid, data=preexec_data)
            except:
                _logger.error("%s: failed to create child object; aborting fork", label, exc_info=True)
            else:
                try:
                    child.start()
                except:
                    _logger.error("%s: failed to start child process", child.label, exc_info=True)

            if orig_env != os.environ:
                _logger.error("forker environment changed during"
                        " task initialization.")

            if child is not None and child.pid is not None:
                self.children[child.id] = child
                if child.runid is not None:
                    self.active_runids.append(runid)
                return child.id
            else:
                return None
        except Exception, e:
            _logger.error("%s: failed due to an unexpected exception: %s", child.label, e, exc_info=True)
            raise

    fork = exposed(fork)
    
    def signal(self, child_id, signame):
        """
        Signal a child process.
        
        Arguments:
        child_id -- id of the child to signal
        signame -- signal name
        """
        if not self.children.has_key(child_id):
            _logger.error("Child %s: child not found; unable to signal", child_id)
            return

        try:
            signum = getattr(signal, signame)
        except AttributeError:
            _logger.error("%s: %s is not a valid signal name; child not signaled", child.label, signame)
            raise

        self.children[child_id].signal(signum)

    signal = exposed(signal)
    
    def get_children(self, tag=None, child_ids=None):
        """
        Retrieve a list of child processes. If a tag is supplied, return only the children with that tag.  If a set of child ids
        are supplied, then return only the children in that set.  If neither a tag nor a set of child ids are provided, then
        return all known children.

        """
        ret = []
        if child_ids is None:
            for child in self.children.itervalues():
                if tag is None or child.tag == tag:
                    ret.append(child.export_state())
        else:
            for child_id in child_ids:
                try:
                    child = self.children[child_id]
                except KeyError:
                    # the requested child no longer exists so make up a dummy child and mark it as lost
                    child = self.child_cls(child_id)
                    child.lost_child = True
                    child.tag = tag
                    child.complete = True
                if tag is None or child.tag == tag:
                    ret.append(child.export_state())
        return ret

    get_children = exposed(get_children)
   
    def cleanup_children(self, child_ids):
        '''Let the forker know that we are done with the child process data.
        and clean up.  Only call this if you have some sort of return code.
        Operates on a list of ids

        '''
        _logger.debug("cleaning up children: %s" % (" ".join([str(id) for id in child_ids]),))

        for child_id in child_ids:
            if not self.children.has_key(child_id):
                _logger.debug("Child %s: unable to cleanup nonexistent child", child_id)
                continue
         
            child = self.children[child_id]
            if not child.complete:
                self.marked_for_death[child.id] = child
            if self.children[child.id].runid is not None:
                try:
                    self.active_runids.remove(self.children[child_id].runid)
                except ValueError:
                    _logger.warning("%s: unable to remove child from the active runid list: runid %s was not present",
                        child.label, child.runid)
            del self.children[child_id]

    cleanup_children = exposed(cleanup_children)

    def _wait(self):
        """Call os.waitpid to status of dead processes.
        """
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError: # there are no child processes
                break
            # this is how waitpid + WNOHANG reports things are running
            # but not yet dead
            if pid == 0:
                break
            exit_status = None
            signum = 0
            core_dump = False
            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                signum = os.WTERMSIG(status)
                if os.WCOREDUMP(status):
                    core_dump = True
                exit_status = 128 + signum
                
            if exit_status is None:
                _logger.info("pid %s died but had no status", pid)
                break
            
            if signum:
                _logger.info("pid %s died with status %s and signal %s; coredump=%s", pid, exit_status, signum, core_dump)
            else:
                _logger.info("pid %s died with status %s", pid, exit_status)

            found = False
            for child in self.children.itervalues():
                if child.pid == pid:
                    _logger.info("task %s: dead pid %s matches child %s", child.label, pid, child.id)
                    child.exit_status = exit_status
                    child.core_dump = core_dump
                    child.signum = signum
                    child.complete = True
                    if child.return_output:
                        try:
                            if child.stdout_file:
                                _logger.info("task %s: reading stdout", child.label)
                                child.stdout_file.seek(0, 0)
                                child.stdout_data = [l.rstrip() for l in child.stdout_file.readlines()]
                                _logger.debug("task %s: stdout:\n%s", child.label, "\n".join(child.stdout_data))
                        except (OSError, IOError), e:
                            _logger.error("%s: unable to read stdout: %s", child.label, e)
                        try:
                            if child.stderr_file:
                                _logger.info("task %s: reading stderr", child.label)
                                child.stderr_file.seek(0, 0)
                                child.stderr_data = [l.rstrip() for l in child.stderr_file.readlines()]
                                _logger.debug("task %s: stderr:\n%s", child.label, "\n".join(child.stderr_data))
                        except (OSError, IOError), e:
                            _logger.error("%s: unable to read stderr: %s", child.label, e)
                    found = True
                    break
            if not found:
                _logger.warning("pid %s has no corresponding child object", pid)
                for child_id in self.marked_for_death.keys():
                    if self.marked_for_death[child_id].pid == pid:
                        _logger.info("pid %s found in marked for death list", pid)
                        del self.marked_for_death[child_id]
                        break
            
        # signal any children marked for death
        for child_id in self.marked_for_death.keys():
            child = self.marked_for_death[child_id]
            if not hasattr(child, 'death_timer'):
                try:
                    child.signal(signal.SIGTERM)
                except OSError, e:
                    if e.errno == errno.ESRCH:
                        del self.marked_for_death[child_id]
                else:
                    child.death_timer = Timer(self.DEATH_TIMEOUT)
                    child.death_timer.start()
            elif timer.has_expired():
                try:
                    child.signal(signal.SIGKILL)
                except OSError, e:
                    if e.errno == errno.ESRCH:
                        del self.marked_for_death[child_id]
                else:
                    child.death_timer.max_time = child.death_timer.elapsed_time + self.DEATH_TIMEOUT

    _wait = automatic(_wait, float(get_forker_config('wait_interval', 10)))


if __name__ == "__main__":

    print "Initiating forker unit tests"
    test_count = IncrID()
    
    forker = BaseForker()

    init_pid = forker.fork("/bin/ls", runid=1)
    print test_count.next(),":", "forked process with pid %s" % init_pid
    assert (init_pid == 1), "init_id wrong"
    pid_2 = forker.fork("/bin/ls", runid=2)
    assert (pid_2 == 2), "pid_2 wrong"
    print test_count.next(),":", "forked process with pid %s" % pid_2
    pid_3 = forker.fork("/bin/ls", runid=1)
    print test_count.next(),":", "forked process with pid %s" % pid_3

    print forker.active_runids
    print forker.children
    forker.child_cleanup([init_pid, pid_2, pid_3])

    print forker.active_runids
    print forker.children
    pid_4 = forker.fork("/bin/ls", runid=1)
    pid_5 = forker.fork("/bin/ls")
    print pid_4
    forker.child_cleanup([pid_4])

