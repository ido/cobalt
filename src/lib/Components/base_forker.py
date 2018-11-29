# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
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
import time
import subprocess
from ConfigParser import NoOptionError, NoSectionError

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

from Cobalt.Util import init_cobalt_config, get_config_option

__all__ = [
    "BaseForker",
    "BaseChild"
]

_logger = logging.getLogger(__name__.split('.')[-1])

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
init_cobalt_config()

# Number of bytes to attempt to read at once from stdout.  Excpect some large
# values due to large Cray system states/statuses.
PIPE_BUFSIZE = int(get_config_option('forker', ' pipe_buffsize', 16777216))

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

        #Pipe handling for parent piping stdin/stdout
        self.pipe_child_stdin = None
        self.pipe_child_stdout = None
        self.pipe_read = None
        self.pipe_write = None
        self.stdin_string = kwargs.get('stdin_string', None) #string to send
        self.use_stdout_string = kwargs.get('stdout_string', False)
        self.stdout_string = ''
        self.stdout_fd_gone = False

        self.complete = False
        self.lost_child = False
        self.exit_status = None
        self.signum = 0
        self.core_dump = False

        if kwargs.has_key('log_filename'):
            self.cobalt_log_filename = kwargs['log_filename']
        else:
            self.cobalt_log_filename = None
        self._cobalt_log_file = None
        self._cobalt_log_failed = False
        self._cobalt_log_reporting_errors = False
        self._cobalt_log_have_blank_line = False
        # cgroup control
        self.use_cgroups = False
        self.cgclassify_path = '/usr/bin/cgclassify'
        self.cgclassify_args = None
        self.cgroup_failure_fatal = False
        self._set_cgroup_config('forker')


    def _set_cgroup_config(self, section):
        '''Read and set cgroup configuration for the forker instance from config file

        Args:
            section - section of cobalt config file to use.  Other subclasses may
                      call this with different sections to override the configuration

        Returns:
                None

        Side Effects:
            Sets use_cgexec, cgexec_path, and cgexec_args for this instance.

        Notes:
            * Override goes from forker to forker.implementation to forker.name.  More specific wins.
            * This gets called on both child init and will be reset for childeren on re-initialization from a statefile.

        '''
        #set defaults in forker section.  forker.NAME sections override this behavior

        new_use_cgroups = get_config_option(section, 'use_cgroups', None)
        new_cgroup_failure_fatal = get_config_option(section, 'cgroup_failure_fatal', None)
        new_cgclassify_path = get_config_option(section, 'cgclassify_path', None)
        new_cgclassify_args = get_config_option(section, 'cgclassify_args', None)
        if new_use_cgroups is not None:
            self.use_cgroups = new_use_cgroups.lower() in Cobalt.Util.config_true_values
        if new_cgroup_failure_fatal is not None:
            self.cgroup_failure_fatal = new_cgroup_failure_fatal.lower() in Cobalt.Util.config_true_values
        if new_cgclassify_path is not None:
            self.cgclassify_path = new_cgclassify_path
        if new_cgclassify_args is not None:
            self.cgclassify_args = new_cgclassify_args
            self.cgclassify_args = self.cgclassify_args.split(' ') #Nothing we're passing has spaces we need to link back up
        return

    def _log_cgroup_info(self):
        _logger.debug('Cgroup configuration: use_cgroup: %s\ncgclassify_path: %s\ncgclassify_args: %s\ncgroup_failure_fatal: %s',
                self.use_cgroups, self.cgclassify_path, self.cgclassify_args, self.cgroup_failure_fatal)
        return

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
        self.use_stdout_string = state.get('stdout_string', False)
        self.stdin_string = state.get('stdin_string', None)
        self.stdout_string = state.get('stdout_string', '')
        if not self.complete:
            self.lost_child = True
            self.return_output = False
            self.complete = True
        self._set_cgroup_config('forker')

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
        d['stdout_string'] = self.stdout_string
        return d

    def _open_clf(self):
        if not self._cobalt_log_file and self.cobalt_log_filename and not self._cobalt_log_failed:
            if os.geteuid() == 0:
                return
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

    def print_clf_info(self, fmt, *args):
        self.print_clf("Info: " + fmt, *args)

    def print_clf_warning(self, fmt, *args):
        self.print_clf("WARNING: " + fmt, *args, error=True)

    def print_clf_error(self, fmt, *args):
        self.print_clf("ERROR: " + fmt, *args, error=True)

    def print_clf(self, fmt, *args, **kwargs):
        t = Cobalt.Util.sec_to_str(time.time()) + ' '
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
                _msg = t + (fmt % args)
                print >>self._cobalt_log_file, _msg
                if fmt != "":
                    self._cobalt_log_have_blank_line = False
            except (IOError, OSError), e:
                _logger.error("%s: unable to write to cobaltlog file %s: %s", self.label, self.cobalt_log_filename, e)
                self._cobalt_log_failed = True
            except:
                _logger.error("%s: unable to write to cobaltlog file %s", self.label, self.cobalt_log_filename, exc_info=True)
                self._cobalt_log_failed = True

    def preexec_first(self):
        '''Configuration changes that should happen early in process life.
        If we are being used for a forker that executes setuid/setgid operations,
        this is the point where we're still root.

        Args:
            None

        Returns:
            None

        Notes:
            Current version sets cgroups if cgroups are enabled, sets the process sid
            and the umask.

        '''
        try:
            os.setsid()
            _logger.debug("%s: session id set to %s", self.label, os.getsid(os.getpid()))
        except Exception, e:
            _logger.error("%s: setting the process group and session id failed: %s", self.label, e)
            raise

        if self.umask != None:
            try:
                _logger.debug("%s: setting umask to %s", self.label, self.umask)
                os.umask(self.umask)
            except:
                _logger.error("%s: failed to set umask to %s", self.label, self.umask)
                self._umask_failed = True

        # Migrate this process (and all it's child processes) to an admin-specified cgroup
        if self.use_cgroups:
            cgroup_args = [self.cgclassify_path]
            cgroup_args.extend(self.cgclassify_args)
            cgroup_args.append(str(os.getpid())) # going as a string to the command line.
            _logger.info('%s: setting cgroup with "%s"', self.label, " ".join(cgroup_args))
            try:
                cgclassify = subprocess.Popen(cgroup_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                _logger.error("%s: unexpected error executing cgclassify with parameters: %s", self.label, cgroup_args,
                        exc_info=True)
                if self.cgroup_failure_fatal:
                    _logger.error("%s: cgroup failure fatal flag set: terminating task", self.label)
                    raise
            else:
                stdout, stderr = cgclassify.communicate(None)
                if cgclassify.returncode != 0:
                    _logger.error("%s: cgclassify failed with status: %s", self.label, cgclassify.returncode)
                    _logger.error("%s: cgclassify stdout: %s", self.label, stdout)
                    _logger.error("%s: cgclassify stderr: %s", self.label, stderr)
                    if self.cgroup_failure_fatal:
                        _logger.error("%s: cgroup failure fatal flag set: terminating task", self.label)
                        raise RuntimeError('%s: Unable to set cgroup with cgclassify' % self.label)
                else:
                    _logger.info('%s: cgclassify successful', self.label)

    def preexec_last(self):
        if self.stdin_string is not None:
            self.pipe_read = self.pipe_child_stdin[0]
            os.close(self.pipe_child_stdin[1])
        if self.use_stdout_string:
            self.pipe_write = self.pipe_child_stdout[1]
            os.close(self.pipe_child_stdout[0])

        if hasattr(self, '_umask_failed'):
            self.print_clf_error("failed to set umask to %s", self.umask)

        if self.cwd:
            try:
                _logger.debug("%s: setting current working directory to %s", self.label, self.cwd)
                os.chdir(self.cwd)
            except OSError, e:
                _logger.error("%s: unable to change to the current working directory to \"%s\"", self.label, self.cwd)
                self.print_clf_error("unable to change to the current working directory to \"%s\"; terminating job", self.cwd)
                raise
        if self.stdin_file and self.stdin_string is None:
            _logger.debug("%s: redirecting stdin", self.label)
            try:
                os.dup2(self.stdin_file.fileno(), sys.__stdin__.fileno())
                self.stdin_file.close()
            except Exception, e:
                _logger.error("%s: unable to redirect file %s to stdin: %s", self.label, self.stdin_file.name, e)
                self.print_clf_error("unable to redirect file %s to stdin: %s", self.stdin_file.name, e)
                self.stdin_file = None
        elif self.stdin_string is not None:
            #receive stdin from parent.
            _logger.debug('%s: Redirecting stdin to string', self.label)
            try:
                fcntl.fcntl(self.pipe_read, fcntl.F_SETFL, not os.O_NONBLOCK)
                os.dup2(self.pipe_read, sys.__stdin__.fileno())
                _logger.debug('%s: flags are: %s', self.label,
                        fcntl.fcntl(sys.__stdin__.fileno(), fcntl.F_GETFL))
            except Exception as exc:
                _logger.error("%s unable to redirect stdin to pipe: %s",
                        self.label, exc, exc_info=True)
            finally:
                self.close_read_pipe()
        if self.stdin_string is None and self.pipe_read is not None:
            #close for one-sided case
            self.close_read_pipe()

        if self.stdout_file and (not self.use_stdout_string):
            _logger.debug("%s: redirecting stdout", self.label)
            try:
                os.dup2(self.stdout_file.fileno(), sys.__stdout__.fileno())
                self.stdout_file.close()
            except Exception, e:
                _logger.error("%s: unable to redirect stdout to file %s: %s", self.label, self.stdout_file.name, e)
                self.print_clf_error("unable to redirect stdout to file %s: %s", self.stdout_file.name, e)
                self.stdout_file = None
        elif self.use_stdout_string:
            _logger.debug('%s: Redirecting stdout to pipe', self.label)
            try:
                os.dup2(self.pipe_write, sys.__stdout__.fileno())
            except Exception as exc:
                _logger.error("%s unable to redirect stdout to pipe: %s",
                        self.label, exc, exc_info=True)
            finally:
                self.close_write_pipe()
        if not self.use_stdout_string and self.pipe_write is not None:
            #close for one-sided case
            self.close_write_pipe()

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

    def parent_postfork(self):
        '''Take actions required after fork in parent.'''
        if self.use_stdout_string:

            self.pipe_read = self.pipe_child_stdout[0]
            os.close(self.pipe_child_stdout[1])
            #set stdout reader to nonblocking
            fcntl.fcntl(self.pipe_read, fcntl.F_SETFL, os.O_NONBLOCK)
        if self.stdin_string is not None:
            self.pipe_write = self.pipe_child_stdin[1]
            os.close(self.pipe_child_stdin[0])

        #fcntl.fcntl(self.pipe_write, fcntl.F_SETFL, os.O_NONBLOCK)
        if self.stdin_string is not None:
            #pipe opened as a part of start prior to fork call.
            written = 0
            while (written < len(self.stdin_string)):
                try:
                    written += os.write(self.pipe_write, self.stdin_string[written:])
                except (OSError, IOError) as exc:
                    if exc.errno in [errno.EAGAIN, errno.EWOULDBLOCK,
                            errno.EINTR]:
                        # I expect this to happen, especially if we end up using
                        # O_NONBLOCKING.  Don't make noise, just continue.
                        # Is the return for os.write well-defined at this point?
                        pass
                    elif exc.errno in [errno.EPIPE]:
                        _logger.warning("%s: Broken pipe recieved while writing to stdin", self.label)
                    else:
                        _logger.critical("%s Unexpected IOError recieved while writing to child stdin.",
                                self.label, exc_info=True)
        self.close_write_pipe()
        if not self.use_stdout_string:
            #leave this side open if we're going to read from the child later.
            self.close_read_pipe()
        return

    def _close_pipe_and_check(self, pipe):
        '''Close the fd's tied to a pipe to this child.
        Gracefully handle errors.

        '''
        retry = True
        while(retry):
            retry = False
            try:
                os.close(pipe)
            except (IOError, OSError) as exc:
                if exc.errno == errno.EBADF:
                    _logger.warning('%s: Tried to close a pipe twice.',
                            self.label)
                elif exc.errno == errno.EINTR:
                    _logger.warning('%s: Close interrupted by system call.',
                            self.label)
                    retry = True
                elif exc.errno == errno.EIO:
                    _logger.warning('%s: IO Error while closing pipe.',
                            self.label)
                else:
                    raise
            finally:
                pipe = None

    def close_read_pipe(self):
        '''close the read side of the pipe to this child'''
        if self.pipe_read is not None:
            self._close_pipe_and_check(self.pipe_read)

    def close_write_pipe(self):
        '''close the write side of the pipe to this child'''
        if self.pipe_write is not None:
            self._close_pipe_and_check(self.pipe_write)

    def start(self):

        if self.stdin_string is not None:
            _logger.debug("%s: setting stdin pipe", self.label)
            try:
                #self.pipe_read, self.pipe_write = os.pipe()
                self.pipe_child_stdin = os.pipe()
            except (OSError, IOError) as exc:
                if exc.errno in [errno.EFAULT, errno.EINVAL, errno.EMFILE,
                        errno.ENFILE]:
                    #we flat-out cannot make this pipe happen.  Log failure and
                    #abort startup.  Not sure if this should  be a higher
                    #logging level.
                    _logger.critical("%s: FATAL: FIFO creation failed with error: %s",
                            self.label, errno.errorcode[exc.errno])
        if self.use_stdout_string:
            _logger.debug("%s: setting stdout pipe", self.label)
            try:
                #self.pipe_read, self.pipe_write = os.pipe()
                self.pipe_child_stdout = os.pipe()
            except (OSError, IOError) as exc:
                if exc.errno in [errno.EFAULT, errno.EINVAL, errno.EMFILE,
                        errno.ENFILE]:
                    #we flat-out cannot make this pipe happen.  Log failure and
                    #abort startup.  Not sure if this should  be a higher
                    #logging level.
                    _logger.critical("%s: FATAL: FIFO creation failed with error: %s",
                            self.label, errno.errorcode[exc.errno])

        _logger.debug("%s: forking process", self.label)
        try:
            gc_enabled = gc.isenabled()
            gc.disable()
            try:
                self.pid = os.fork()
            except OSError, e:
                _logger.error("%s: fork failed: %s", self.label, e.strerror)
                self.close_read_pipe()
                self.close_write_pipe()
                raise
        finally:
            if gc_enabled:
                gc.enable()
        if self.pid != 0:
            self.parent_postfork()
            return

        _logger.info("%s: child process %s created to run '%s'", self.label, os.getpid(), self.args[0])

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
        if self.pid != None:
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
        else:
            _logger.info("%s: unable to send signal %s to dead process", self.label, signame)


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
        for child in self.children.values():
            _logger.debug("Child found: %s", child.id)

    def __save_me(self):
        '''Periodically save off a statefile.'''
        Component.save(self)
    __save_me = automatic(__save_me, float(get_forker_config('save_me_interval', 10)))

    def fork(self, args, tag=None, label=None, env=None, preexec_data=None,
            runid=None, stdin_string=None, stdout_string=False,
            stderr_string=False):
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
        stdin_string -- a string to send to the forked child's stdin at startup.
        stdout_string -- store stdout as a string in child data.
        stderr_string -- store stderr as a string in the child data.  If used
                         stdout_string, both outputs will be interleaved.
        returns the forker id of the child process object.

        """

        _logger.debug("fork called with args of %s", " ".join(args))

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
                child = self.child_cls(label_prefix=label, tag=tag, args=args,
                        env=env, runid=runid, data=preexec_data,
                        stdin_string=stdin_string, stdout_string=stdout_string, forker_name=self.name)
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
                for c in self.children.itervalues():
                    if c.pid == child.pid:
                        if self.marked_for_death.has_key(c.id):
                            del self.marked_for_death[c.id]
                        c.pid = None
                self.children[child.id] = child
                if child.runid is not None:
                    self.active_runids.append(runid)
                return child.id
            else:
                return None
        except Exception, e:
            _logger.error("%s: failed due to an unexpected exception: %s", label, e, exc_info=True)
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
            _logger.error("%s: %s is not a valid signal name; child not signaled", child_id, signame)
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

    def _read_stdout_pipe(self, child_pids=None):
        '''Read messages from our children that are using redirected stdout to
        string pipes.

        Args:
            child_pids: An optional list of child_pids to fetch information for.
            Default: None.

        Returns:
            None

        Side Effects:
            Updates the output string buffer for running children from the child
            process' stdout.

        '''
        if child_pids is None:
            children = self.children.itervalues()
        else:
            children = [child for child in self.children.itervalues()
                        if child.pid in child_pids]

        for child in children:
            if child.use_stdout_string and child.exit_status is None:
                while True:
                    try:
                        child_str = os.read(child.pipe_read, PIPE_BUFSIZE)
                    except (OSError, IOError) as exc:
                        if exc.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
                            #read would block.  Don't block and continue.
                            break
                        elif exc.errno in [errno.EBADF, errno.EINVAL, errno.EPIPE]:
                            _logger.error("%s: Error reading stdout from child pipe.",
                                    child.label, exc_info=True)
                            break
                        elif exc.errno in [errno.EINTR]:
                            #Try again
                            continue
                        else:
                            _logger.error("%s: Error reading stdout from child pipe: [%s] %s",
                                    child.label, errno.errorcode[exc.errno],
                                    exc.strerror, exc_info=True)
                    else:
                        if child_str == '':
                            break #we're done
                        child.stdout_string += child_str

    def _wait(self):
        """Call os.waitpid to status of dead processes.

        """
        self._read_stdout_pipe()
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
                    if child.use_stdout_string:
                        # need to do a final read for anything remaining
                        # post-exit, then close the fd.
                        self._read_stdout_pipe([child.pid])
                        child.close_read_pipe()
                    child.exit_status = exit_status
                    child.core_dump = core_dump
                    child.signum = signum
                    child.pid = None
                    child.complete = True
                    if self.marked_for_death.has_key(child.id):
                        del self.marked_for_death[child.id]
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
            elif child.death_timer.has_expired:
                try:
                    child.signal(signal.SIGKILL)
                except OSError, e:
                    if e.errno == errno.ESRCH:
                        del self.marked_for_death[child_id]
                else:
                    child.death_timer.max_time = child.death_timer.elapsed_time + self.DEATH_TIMEOUT

    _wait = automatic(_wait, float(get_forker_config('wait_interval', 10.0)))


# if __name__ == "__main__":

    # import time
    # print "Initiating forker unit tests"
    # test_count = IncrID()
    # with open("CHANGES") as test_in:
        # test_str = "#".join(test_in)
    # forker = BaseForker()
    # forker.child_cls = BaseChild
    # child_id = forker.fork(['/usr/bin/grep', '.*'], stdin_string=test_str,
            # stdout_string=True)

    # complete = False
    # child = None
    # while(not complete):
        # forker._wait()
        # children = forker.get_children(child_ids=[child_id])
        # child = children[0]
        # if child['complete']:
            # print child['stdout_string']
        # complete = child['complete']
        # time.sleep(1)
    # forker.cleanup_children([child_id])

#    init_pid = forker.fork("/bin/ls", runid=1)
#    print test_count.next(),":", "forked process with pid %s" % init_pid
#    assert (init_pid == 1), "init_id wrong"
#    pid_2 = forker.fork("/bin/ls", runid=2)
#    assert (pid_2 == 2), "pid_2 wrong"
#    print test_count.next(),":", "forked process with pid %s" % pid_2
#    pid_3 = forker.fork("/bin/ls", runid=1)
#    print test_count.next(),":", "forked process with pid %s" % pid_3
#
#    print forker.active_runids
#    print forker.children
#    forker.child_cleanup([init_pid, pid_2, pid_3])
#
#    print forker.active_runids
#    print forker.children
#    pid_4 = forker.fork("/bin/ls", runid=1)
#    pid_5 = forker.fork("/bin/ls")
#    print pid_4
#    forker.child_cleanup([pid_4])
#
