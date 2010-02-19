"""Implementations of the forker component.

Classes:
BaseForker -- generic implementation

The forker component provides a single threaded component which can safely
fork new processes.

"""

import logging
import sys
import os
import signal
import socket
import time

import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, automatic


__all__ = [
    "BaseForker",
]


class Child(object):
    def __init__(self):
        self.pid = None
        self.exit_status = None
        self.signum = 0
        self.core_dump = False


class BaseForker (Component):
    
    """Generic implementation of the service-location component.
    
    Methods:
    fork -- takes a dictionary specifying parameters for the forked task (exposed)
    signal -- signal a child with the specified signame (exposed)
    active_list -- retrieve a list of children which are still running (exposed)
    get_status -- return a dictionary of status information for a finished process (exposed)
    wait -- wait on children and record their status (automatic)
    """
    
    name = "forker"
    
    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = logging.getLogger("Cobalt.Components.BaseForker")
    
    def __init__ (self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.children = {}

    
    def fork (self, data):
        """fork a child task
        
        Arguments:
        data -- a dictionary of information required while forking
        """
        child_pid = os.fork()
        if not child_pid:
            try:
                pg_id = data["id"]
                try:
                    os.setgid(data["groupid"])
                    os.setuid(data["userid"])
                except OSError:
                    self.logger.error("failed to change userid/groupid for process group %s" % (pg_id))
                    os._exit(1)
        
                if data["umask"] != None:
                    try:
                        os.umask(data["umask"])
                    except:
                        self.logger.error("Failed to set umask to %s" % data["umask"])

                for key, value in data["postfork_env"].iteritems():
                    os.environ[key] = value
                    
                atexit._atexit = []
        
                try:
                    stdin = open(data["stdin"], 'r')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("process group %s: error opening stdin file %s: %s (stdin will be /dev/null)" % (pg_id, data["stdin"], e))
                    stdin = open("/dev/null", 'r')
                os.dup2(stdin.fileno(), 0)
                
                try:
                    stdout = open(data["stdout"], 'a')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("process group %s: error opening stdout file %s: %s (stdout will be lost)" % (pg_id, data["stdout"], e))
                    stdout = open("/dev/null", 'a')
                os.dup2(stdout.fileno(), sys.__stdout__.fileno())
                
                try:
                    stderr = open(data["stderr"], 'a')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("process group %s: error opening stderr file %s: %s (stderr will be lost)" % (pg_id, data["stderr"], e))
                    stderr = open("/dev/null", 'a')
                os.dup2(stderr.fileno(), sys.__stderr__.fileno())
                
                cmd = data["cmd"]
                try:
                    cobalt_log_file = open(data["cobalt_log_file"], "a")
                    print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
                    print >> cobalt_log_file, "called with environment:\n"
                    for key in os.environ:
                        print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                    print >> cobalt_log_file, "\n"
                    cobalt_log_file.close()
                except:
                    self.logger.error("process group %s unable to open cobaltlog file %s" % \
                                 (pg_id, data["cobalt_log_file"]))
        
                os.execl(*cmd)
                
            except:
                self.logger.error("Unable to start job", exc_info=1)
                os._exit(1)
        else:
            kid = Child()
            kid.pid = child_pid
            self.children[child_pid] = kid

            return child_pid
    fork = exposed(fork)
    
    def signal (self, pid, signame, id):
        """Signal a child process.
        
        Arguments:
        pid -- pid of the child to signal
        signame -- signal name
        id -- id of the ProcessGroup (only used for logging)
        """
        try:
            os.kill(int(pid), getattr(signal, signame))
        except OSError, e:
            self.logger.error("signal failure for process group %s: %s" % (id, e))

    signal = exposed(signal)
    
    def active_list (self):
        """Retrieve the list of running child processes.
        """
        ret = []
        for kid in self.children.itervalues():
            if kid.exit_status is None:
                ret.append(kid.pid)
                
        return ret
    active_list = exposed(active_list)
    
    def get_status (self, pid):
        """Signal a child process.
        
        Arguments:
        pid -- pid of the child to signal
        """

        if self.children.has_key(pid):
            dead = self.children[pid]
            if dead.exit_status is not None:
                del self.children[pid]
                return dead.__dict__
            
        return None
    get_status = exposed(get_status)


    def wait(self):
        """Call os.waitpid to status of dead processes.
        """
        while True:
            self.logger.error("i am waiting")
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError: # there are no child processes
                break
            # this is how waitpid + WNOHANG reports things are running
            # but not yet dead
            if pid == 0:
                break
            signum = 0
            core_dump = False
            if os.WIFEXITED(status):
                status = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                signum = os.WTERMSIG(status)
                if os.WCOREDUMP(status):
                    core_dump = True
            else:
                break
            
            self.logger.error("%s died with status %s", pid, status)
            for each in self.children.itervalues():
                if each.pid == pid:
                    if signum == 0:
                        each.exit_status = status
                    else:
                        each.exit_status = 128 + signum
                        each.core_dump = core_dump
                        each.signum = signum
    wait = automatic(wait)