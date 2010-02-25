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
import atexit

import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Data import IncrID



__all__ = [
    "BaseForker",
]


class Child(object):
    def __init__(self):
        self.id = None
        self.pid = None
        self.label = None
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
        self.id_gen = IncrID()

    
    def fork (self, data):
        """fork a child task
        
        Arguments:
        data -- a dictionary of information required while forking
        """
        label = "%s/%s" % (data["jobid"], data["id"])
        child_pid = os.fork()
        if not child_pid:
            try:
                # only root can call os.setgroups so we need to do this
                # before calling os.setuid
                try:
                    os.setgroups([])
                    os.setgroups(data["other_groups"])
                except:
                    self.logger.error("task %s: failed to set supplementary groups", label, exc_info=True)
 
                try:
                    os.setgid(data["primary_group"])
                    os.setuid(data["userid"])
                except OSError:
                    self.logger.error("task %s: failed to change userid/groupid", label)
                    os._exit(1)
                       
                if data["umask"] != None:
                    try:
                        os.umask(data["umask"])
                    except:
                        self.logger.error("task %s: failed to set umask to %s", 
                                label, data["umask"])

                for key, value in data["postfork_env"].iteritems():
                    os.environ[key] = value
                    
                atexit._atexit = []
        
                try:
                    stdin = open(data["stdin"] or "/dev/null", 'r')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("task %s: error opening stdin file %s: %s (stdin will be /dev/null)", label, data["stdin"], e)
                    stdin = open("/dev/null", 'r')
                os.dup2(stdin.fileno(), 0)
                
                try:
                    stdout = open(data["stdout"], 'a')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("task %s: error opening stdout file %s: %s (stdout will be lost)", label, data["stdout"], e)
                    stdout = open("/dev/null", 'a')
                os.dup2(stdout.fileno(), sys.__stdout__.fileno())
                
                try:
                    stderr = open(data["stderr"], 'a')
                except (IOError, OSError, TypeError), e:
                    self.logger.error("task %s: error opening stderr file %s: %s (stderr will be lost)", label, data["stderr"], e)
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
                    self.logger.error("task %s: unable to open cobaltlog file %s", 
                                 label, data["cobalt_log_file"])
        
                os.execl(*cmd)
                
            except:
                self.logger.error("task %s: unable to start", label, exc_info=1)
                os._exit(1)
        else:
            local_id = self.id_gen.next()
            kid = Child()
            kid.id = local_id
            kid.pid = child_pid
            kid.label = "%s/%s" % (label, local_id)
            self.children[local_id] = kid
            self.logger.info("task %s: forked", kid.label)
            return local_id
    fork = exposed(fork)
    
    def signal (self, local_id, signame):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        signame -- signal name
        """
        if not self.children.has_key(local_id):
            self.logger.error("signal found no child with id %s", local_id)
            return

        kid = self.children[local_id]
        self.logger.info("task %s: signaling %s", kid.label, signame)
        try:
            os.kill(kid.pid, getattr(signal, signame))
        except OSError, e:
            self.logger.error("task %s: signal failure", kid.label, e)

    signal = exposed(signal)
    
    def active_list (self):
        """Retrieve the list of running child processes.
        """
        ret = []
        for kid in self.children.itervalues():
            if kid.exit_status is None:
                ret.append(kid.id)
                
        return ret
    active_list = exposed(active_list)
    
    def get_status (self, local_id):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        """

        self.logger.info("status requested for task id %s", local_id)
        if self.children.has_key(local_id):
            dead = self.children[local_id]
            if dead.exit_status is not None:
                del self.children[local_id]
                self.logger.info("task %s: status returned", dead.label)
                return dead.__dict__
            else:
                self.logger.info("task %s: still running", dead.label)
        else:
            self.logger.info("task id %s: not found", local_id)
            
        return None
    get_status = exposed(get_status)


    def wait(self):
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
            signum = 0
            core_dump = False
            if os.WIFEXITED(status):
                status = os.WEXITSTATUS(status)
                if os.WIFSIGNALED(status):
                    signum = os.WTERMSIG(status)
                    if os.WCOREDUMP(status):
                        core_dump = True
            else:
                break
            
            if signum:
                self.logger.info("pid %s died with status %s and signal %s", pid, status, signum)
            else:
                self.logger.info("pid %s died with status %s", pid, status)
            for each in self.children.itervalues():
                if each.pid == pid:
                    self.logger.info("task %s: dead pid %s matches", each.label, pid)
                    if signum == 0:
                        each.exit_status = status
                    else:
                        each.exit_status = 128 + signum
                        each.core_dump = core_dump
                        each.signum = signum
    wait = automatic(wait)
