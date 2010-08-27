#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementations of the forker component.

Classes:
BaseForker -- generic implementation

The forker component provides a single threaded component which can safely
fork new processes.

"""

import logging
import os
import sys
import signal
import socket
import time
import atexit
import ConfigParser
import shlex, subprocess


import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Data import IncrID


config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

# A default logger for the component is instantiated here.
module_logger = logging.getLogger("Cobalt.Components.BaseForker")

def get_forker_config(option, default):
    try:
        value = config.get('forker', option)
    except Exception, e:
        if isinstance(e, ConfigParser.NoSectionError):
            module_logger.info("[forker] section missing from cobalt.conf")
            value = default
        elif isinstance(e, ConfigParser.NoOptionError):
            value = default
        else:
            raise e
    return value


__all__ = [
    "HeckleForker",
]


class Child(object):
    def __init__(self):
        self.id = None
        self.pid = None
        self.label = None
        self.exit_status = None
        self.signum = 0
        self.core_dump = False


class HeckleForker (Component):
    
    """Generic implementation of the service-location component.
    
    Methods:
    fork -- takes a dictionary specifying parameters for the forked task (exposed)
    signal -- signal a child with the specified signame (exposed)
    active_list -- retrieve a list of children which are still running (exposed)
    get_status -- return a dictionary of status information for a finished process (exposed)
    wait -- wait on children and record their status (automatic)
    """
    
    name = "forker"
    implementation = "HeckleForker"
    
    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = module_logger
    
    def __init__ (self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.children = {}
        self.id_gen = IncrID()
     
     
    def fork (self, data):
          """
          Fork and Run a child task
          Arguments:
               data -- a dictionary of information required while forking
          """
          logstr = "Forker:Fork:"
          print logstr + "data is: %s" % data
          label = "%s/%s" % (data["jobid"], data["id"])
          child_pid = 0
          print "User ID is %s, pid is %s" % (os.getuid(), child_pid)
          child_pid = os.fork()
          if not child_pid:
               print "...and User ID is now %s, pid is now %s" % (os.getuid(), child_pid)
               self.logger.debug( logstr + "Parent / Script Start")
               os.setgroups([])
               os.setgroups(data["other_groups"])
               os.setgid(data["primary_group"])
               #os.setuid(data["userid"])
               print "post-set: uid is now %s" % os.getuid()
               atexit._atexit = []
               if data["umask"] != None:
                    try:
                         stdin = open(data["stdin"] or "/dev/null", 'r')
                    except (IOError, OSError, TypeError), e:
                         self.logger.error("task %s: error opening stdin file %s: %s (stdin will be /dev/null)", label, data["stdin"], e)
                         stdin = open("/dev/null", 'r')
               os.dup2(stdin.fileno(), 0)
               self.logger.debug( logstr + "1" )
               new_out = None
               try:
                    stdout = open(data["stdout"], 'a')
               except (IOError, OSError, TypeError), e:
                    self.logger.error("task %s: error opening stdout file %s: %s", label, data["stdout"], e)
                    output_to_devnull = False
                    try:
                         scratch_dir = get_forker_config("scratch_dir", None)
                         if scratch_dir:
                              new_out = os.path.join(scratch_dir, "%s.output" % data["jobid"])
                              self.logger.error("task %s: sending stdout to scratch_dir %s", label, new_out)
                              stdout = open(new_out, 'a')
                         else:
                              self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stdout")
                              output_to_devnull = True
                    except Exception, e:
                         output_to_devnull = True
                         self.logger.error("task %s: error opening stdout file %s: %s", label, new_out, e)
                    if output_to_devnull:
                         stdout = open("/dev/null", 'a')
                         new_out = "/dev/null"
                         self.logger.error("task %s: sending stdout to /dev/null", label)
               os.dup2(stdout.fileno(), sys.__stdout__.fileno())
               self.logger.debug( logstr + "2" )
               new_err = None
               try:
                    stderr = open(data["stderr"], 'a')
                    self.logger.debug( logstr + "2aaa" )
               except (IOError, OSError, TypeError), e:
                    self.logger.debug( logstr + "2aab" )
                    self.logger.error("task %s: error opening stderr file %s: %s", label, data["stderr"], e)
                    error_to_devnull = False
                    self.logger.debug( logstr + "2a" )
                    try:
                         scratch_dir = get_forker_config("scratch_dir", None)
                         self.logger.debug( logstr + "2a1")
                         if scratch_dir:
                              new_err = os.path.join(scratch_dir, "%s.error" % data["jobid"])
                              self.logger.error("task %s: sending stderr to scratch_dir %s", label, new_err)
                              stderr = open(new_err, 'a')
                         else:
                              self.logger.debug( logstr + "2a2" )
                              self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stderr")
                              error_to_devnull = True
                    except Exception, e:
                         self.logger.debug( logstr + "2a3" )
                         error_to_devnull = True
                         self.logger.error("task %s: error opening stderr file %s: %s", label, new_err, e)
                    self.logger.debug( logstr + "2b" )
                    if error_to_devnull:
                         stderr = open("/dev/null", 'a')
                         new_err = "/dev/null"
                         self.logger.error( logstr + "task %s: sending stderr to /dev/null", label)
               self.logger.debug( logstr + "2 Last!" )
               os.dup2(stderr.fileno(), sys.__stderr__.fileno())
               self.logger.debug( logstr + "3" )
               cmd = data["cmd"]
               environ = data["environment"]
               try:
                    cobalt_log_file = open(data["cobalt_log_file"], "a")
                    if new_out:
                         print >> cobalt_log_file, "failed to open %s" % data["stdout"]
                         print >> cobalt_log_file, "stdout sent to %s\n" % new_out
                    if new_err:
                         print >> cobalt_log_file, "failed to open %s" % data["stderr"]
                         print >> cobalt_log_file, "stderr sent to %s\n" % new_err
                    print >> cobalt_log_file, "command is %s" % cmd
                    print >> cobalt_log_file, "called with environment:\n"
                    for key in environ:
                         print >> cobalt_log_file, "%s=%s" % (key, environ[key])
                    print >> cobalt_log_file, "\n"
                    cobalt_log_file.close()
               except:
                    self.logger.error( logstr + "task %s: unable to open cobaltlog file %s", 
                              label, data["cobalt_log_file"])
               self.logger.debug( logstr + "4" )
               os.setuid( data['userid'] )
               self.logger.debug( logstr + "About to exec with %s" % cmd )
               os.execvpe(cmd, (cmd, ), environ)
               self.logger.debug( logstr + "Finished Execution" )
          else:
               self.logger.info( logstr + "Child / Remainder" )
               local_id = self.id_gen.next()
               kid = Child()
               kid.id = local_id
               kid.pid = child_pid
               kid.label = "%s/%s" % (label, local_id)
               self.children[local_id] = kid
               self.logger.info( logstr + "Parent:Task %s: forked with pid %s", kid.label, kid.pid)
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
        self.logger.info("task %s: sending %s to pid %s", kid.label, signame, kid.pid)
        try:
            os.kill(kid.pid, getattr(signal, signame))
        except OSError:
            self.logger.error("task %s: signal failure", kid.label, exc_info=True)

    signal = exposed(signal)
    
    def active_list (self):
        """Retrieve the list of running child processes.
        """
        ret = []
        for kid in self.children.itervalues():
            if kid.exit_status is None:
                ret.append(kid.id)
                
        logger.debug( "Active List still looks at %s" % ret )
        return ret
    active_list = exposed(active_list)
    
    def get_status (self, local_id):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        """
        logstr = "Forker:get_status:"
        self.logger.info( logstr + "current tasks are %s" % self.children.keys() )
        self.logger.info( logstr + "status requested for task id %s" % local_id )
        self.logger.info( logstr + "task pid is %s" % self.children[local_id].pid )
        if self.children.has_key(local_id):
            dead = self.children[local_id]
            if dead.exit_status is not None:
                #del self.children[local_id]
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
            exit_status = None
            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                signum = os.WTERMSIG(status)
                if os.WCOREDUMP(status):
                    core_dump = True
                exit_status = 128 + signum
                
            if exit_status is None:
                self.logger.info("pid %s died but had no status", pid)
                break
            
            if signum:
                self.logger.info("pid %s died with status %s and signal %s", pid, status, signum)
            else:
                self.logger.info("pid %s died with status %s", pid, status)
            for each in self.children.itervalues():
                if each.pid == pid:
                    self.logger.info("task %s: dead pid %s matches", each.label, pid)
                    each.exit_status = exit_status
                    each.core_dump = core_dump
                    each.signum = signum
    wait = automatic(wait)
