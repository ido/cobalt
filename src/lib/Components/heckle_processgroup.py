#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Heckle Component
"""

import atexit
import logging
import os
import os.path
import pwd
import sets
import signal
import stat
import sys
import tempfile
import grp

import ConfigParser

from time import sleep

from Cobalt.DataTypes.Resource import ResourceDict
from Cobalt.Components.base import Component, automatic, exposed, query
from Cobalt.Exceptions import JobValidationError
from Cobalt.Proxy import ComponentProxy


from Cobalt.DataTypes.heckle_temp_ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.heckle_temp_Data import IncrID
from Cobalt import CONFIG_FILES

import threading



__all__ = ["HeckleProcessGroup"]


logger = logging.getLogger(__name__)


class HeckleProcessGroup(ProcessGroup):
     """
     Process Group modified for Heckle-based Systems on Breadboard
     """
     
     _configfields = ['mpirun']
     _config = ConfigParser.ConfigParser()
     _config.read(CONFIG_FILES)
     if not _config._sections.has_key('bgpm'):
          print '''"bgpm" section missing from cobalt config file'''
          sys.exit(1)
     config = _config._sections['bgpm']
     mfields = [field for field in _configfields if not config.has_key(field)]
     if mfields:
          print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
          sys.exit(1)
     else:
          pass

     
     def __init__(self, spec ):
          logger.debug( "Heckle Process Group: init ... %s ... &&&&&&&&&&&&&&&&&&&&&&&&&&&&&  I am here!!! &&&&&&&&&&&&&&&&&&&&&&&&&" % threading.current_thread().getName() )
          logger.debug( "Heckle Process Group: Spec is: %s " % spec )
          ProcessGroup.__init__(self, spec, logger)
          
          if not self.kernel:
               self.kernel = "default"
          self.pinging_nodes = []
          self.nodefile = tempfile.mkstemp()
          
          print "Nodefile is: %s       &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" % type(self.nodefile)
          logger.debug( "Heckle Process Group: init: location is: %s" % self.location )
          self.resource_attributes = {}
          os.write(self.nodefile[0], " ".join(self.location))
          os.chmod(self.nodefile[1], stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|
                    stat.S_IROTH)
          ###
          ###  Watch this line... not sure what it does...  Supposed to be in ProcessGroupDict
          ###
          self.id_gen = IncrID()
          os.close(self.nodefile[0])
     
     
     def __repr__(self):
          """
          Printout Representation of the Class
          """
          indict = self.__dict__
          printstr = ""
          in_len = len(indict)
          printstr += "Heckle Process Group: Values: ["
          for element in indict:
               printstr += str(element) + "::" 
               if indict[element] == None:
                    printstr += "None"
               else:
                    printstr += str(indict[element])
               printstr += ", "
          printstr += "]"
          return printstr
     
     
     def simulator_init(self, spec, log):
          """
          Used by Simulator to be able to extend Process Group
          and pass through correct logger
          """
          logger.debug( "HeckleProcess Group: simulator_init")
          ProcessGroup.__init__(self, spec, log)
          if not self.kernel:
               self.kernel = "default"
          self.pinging_nodes = []
          self.nodefile = tempfile.mkstemp()
          os.write(self.nodefile[0], " ".join(self.location))
          os.close(self.nodefile[0])
     
     
     def _runjob(self):
        """
        Sets up the environment and execs to the executable script.
        """
        logger.debug( "Heckle Process Group:  run job")
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            logger.exception("Heckle Process Group: runjob: Error getting userid/groupid for process group %s"
                             % self.id)
            os._exit(1)
        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            logger.exception("Heckle Process Group: runjob: Failed to set userid/groupid for process group %s"
                             % self.id)
            os._exit(1)
        if self.umask != None:
            try:
                os.umask(self.umask)
            except OSError:
                logger.exception("Heckle Process Group: runjob: Failed to set umask to %s" % self.umask)
        for node in self.nodefile:
             print "Node is: %s" % node
        nodes_file_path = self.nodefile[1]
        os.environ["COBALT_NODEFILE"] = nodes_file_path
        for key, value in self.env.iteritems():
            os.environ[key] = value
        atexit._atexit = []
        stdin = open(self.stdin or "/dev/null", "r")
        os.dup2(stdin.fileno(), sys.__stdin__.fileno())
        try:
            stdout = open(self.stdout or tempfile.mktemp(), "a")
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
        except (IOError, OSError):
            logger.exception(("Heckle Process Group: runjob: Process Group %s: error opening stdout " +
                              "file %s (stdout will be lost)")
                             % (self.id, self.stdout))
        try:
            stderr = open(self.stderr or tempfile.mktemp(), "a")
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
        except (IOError, OSError):
            logger.exception(("Heckle Process Group: runjob: Process Group %s: error opening stderr " +
                              "file %s (stderr will be lost)")
                             % (self.id, self.stderr)) 
        cmd = (self.executable, self.executable)
        if self.args:
            cmd = cmd + (self.args)
        try:
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
            print >> cobalt_log_file, "called with environment:\n"
            for key in os.environ:
                print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
            print >> cobalt_log_file, "\n"
            cobalt_log_file.close()
        except IOError:
            logger.error("Heckle Process Group: runjob: Job %s/%s: unable to open cobalt log file %s"
                         % (self.id, self.user, self.cobalt_log_file))
        try:
            os.execl(*cmd)
        except OSError:
            logger.exception("Heckle Process Group: runjob: Job %s/%s: unable to execl the script"
                             % (self.id, self.user))
            os._exit(1)
        print "Done!  What now?"
     
     
     def signal(self, signame="SIGINT"):
        """
        Do something with this process group depending on the signal
        """
        for node in self.nodefile:
             print "Node is %s" % node
        logger.debug( "Heckle Process Group: runjob: signal" )
        if self.head_pid and self.state != "terminated":
            try:
                os.kill(self.head_pid, getattr(signal, signame))
            except OSError, err:
                logger.exception("Heckle Process Group: runjob: signal failure for PG %s: %s"
                                 % (self.id, err))
        elif not self.head_pid and self.state != "terminated":
            if signame == "SIGINT" or signame == "SIGTERM" or \
                    signame == "SIGKILL":
                os.remove(self.nodefile[1])
                self.exit_status = 1
     
     
     def wait(self):
        """
        Sets the PG state to 'terminated' if done
        """
        logger.debug( "Heckle Process Group: wait" )
        if self.head_pid:
            try:
                pid, status = os.waitpid(self.head_pid, os.WNOHANG)
            except OSError:
                return
            if self.head_pid == pid:
                # Child has terminated
                status = status >> 8
                # Remove temporary file with node locations
                os.remove(self.nodefile[1])
                self.exit_status = status
                # Do something if exit status is non-zero?
     
     
     def start(self):
          """
          Starts the process group by forking to _mpirun()
          ###
          ###  Still not sure about this, future work here...
          ###
          """
          #try:
          data = self.prefork()
          self.head_pid = ComponentProxy("forker").fork(data)


     def prefork (self):
          """
          Prepares the MPIRUN qualities for the Start function
          * Defines the running environment
          * Defines user and group info
          * Sets up the command line to run the cobalt launcher program
          """
          logger.debug("PreFork:")
          print "Current State is: %s" % self
          ret = {}
          # check for valid user/group
          try:
               userid, groupid = pwd.getpwnam(self.user)[2:4]
          except KeyError:
               raise ProcessGroupCreationError("error getting uid/gid")
          ret["userid"] = userid
          ret["primary_group"] = groupid
          ret["other_groups"] = []
          ret["umask"] = self.umask
          ret["stdin"] = self.stdin
          ret["stdout"] = self.stdout
          ret["stderr"] = self.stderr
          self.nodefile = "/var/tmp/cobalt.%s" % self.jobid
          # get supplementary groups
          supplementary_group_ids = []
          for g in grp.getgrall():
               if self.user in g.gr_mem:
                    supplementary_group_ids.append(g.gr_gid)
          ret["other_groups"] = supplementary_group_ids
          #Set Head Node
          try:
               rank0 = self.location[0].split(":")[0]
          except IndexError:
               raise ProcessGroupCreationError("no location")
          #cmd_string = "/usr/bin/cobalt-launcher.py --nf %s --jobid %s --cwd %s --exe %s" % (self.nodefile, self.jobid, self.cwd, self.executable)
          cmd_string = "/home/sthompso/cobalt-launcher.py --nf %s --jobid %s --cwd %s --exe %s" % (self.nodefile, self.jobid, self.cwd, self.executable)
          cmd = ("/usr/bin/ssh", "/usr/bin/ssh", rank0, cmd_string)
          ret["id"] = self.id
          ret["jobid"] = self.jobid
          ret["cobalt_log_file"] = self.cobalt_log_file
          ret["cmd" ] = cmd
          logger.debug("Command is %s" % ret)
          return ret

