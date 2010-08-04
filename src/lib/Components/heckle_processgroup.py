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
import signal
import stat
import sys
import tempfile
import grp

import ConfigParser

from Cobalt.DataTypes.Resource import ResourceDict
from Cobalt.Exceptions import JobValidationError
from Cobalt.Proxy import ComponentProxy


from Cobalt.DataTypes.heckle_temp_ProcessGroup import ProcessGroup
from Cobalt.heckle_temp_Data import IncrID


try:
    from Cobalt.Components.heckle_lib2 import HeckleConnector
except:
    from heckle_lib2 import HeckleConnector


__all__ = ["HeckleProcessGroup"]


LOGGER = logging.getLogger(__name__)


class HeckleProcessGroup(ProcessGroup):
    """
    Process Group modified for Heckle-based Systems on Breadboard
    """
    
    def __init__(self, spec ):
        logstr = "ProcessGroup:__INIT__:"
        LOGGER.debug( logstr + "Spec is: %s " % spec )
        ProcessGroup.__init__(self, spec, LOGGER)
        hiccup = HeckleConnector()
        self.location = spec['location'][:]
        self.pinging_nodes = spec['location'][:]
        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n Location is: %s, %s, %s\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" % (self.location, self.pinging_nodes, spec['location'])
        # Set up process group attributes
        if not spec['kernel']:
            spec['kernel'] = "default"
        self.kernel = spec['kernel']
        self.user = self.uid = spec['user']
        self.resource_attributes = {}
        for loc in self.location:
            self.resource_attributes[loc] = hiccup.get_node_properties( loc )
        try:     #  Checking for Fakebuild
            spec['fakebuild'] = spec['env']['fakebuild']
            del spec['env']['fakebuild']
        except:
            spec['fakebuild']=False
        self.env = spec['env']
        # Write nodefile
        self.nodefile = tempfile.mkstemp()
        os.write(self.nodefile[0], " ".join(self.location))
        os.chmod(self.nodefile[1], stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP| \
        stat.S_IROTH)
        os.close(self.nodefile[0])
        # Make heckle reservation
        res_attrs = ['location', 'kernel', 'walltime', 'user', 'fakebuild'\
            , 'comment']
        res_args = {}
        for attr in spec:
            res_args[attr] = spec[attr]
        reservation = hiccup.make_reservation( res_args )
        self.heckle_res_id = reservation.id
        ###  Watch this line... not sure what it does...  Supposed to be in ProcessGroupDict
        self.id_gen = IncrID()
        
    
    
    def __repr__(self):
        """
        Printout Representation of the Class
        """
        indict = self.__dict__
        printstr = ""
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
        and pass through correct LOGGER
        """
        LOGGER.debug( "HeckleProcess Group: simulator_init")
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
        logstr = "ProcessGroup:_runjob:"
        startstr = "!  !  !  !  !  !  !  !  !  !  !  !  !  !  !  !  !  !\n"
        LOGGER.debug( startstr + startstr + logstr + "\n" + startstr + startstr )
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            LOGGER.exception( logstr + "Error getting userid/groupid for"\
                + " process group %s" % self.id)
            os._exit(1)
        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            LOGGER.exception( logstr + "Failed to set userid/groupid for"\
                + " process group %s" % self.id)
            os._exit(1)
        if self.umask != None:
            try:
                os.umask(self.umask)
            except OSError:
                LOGGER.exception( logstr + "Failed to set umask to %s" %\
                    self.umask)
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
            LOGGER.exception(( logstr + "Process Group %s: error opening "\
                + "stdout; file %s (stdout will be lost)") \
                % (self.id, self.stdout))
        try:
            stderr = open(self.stderr or tempfile.mktemp(), "a")
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
        except (IOError, OSError):
            LOGGER.exception(("Heckle Process Group: runjob: Process Group %s:"\
                + "error opening stderr, file %s (stderr will be lost)")
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
            LOGGER.error("Heckle Process Group: runjob: Job %s/%s: unable to"\
                " open cobalt log file %s" % (self.id, self.user, self.cobalt_log_file))
        try:
            os.execl(*cmd)
        except OSError:
            LOGGER.exception("Heckle Process Group: runjob: Job %s/%s: unable"\
                + " to execl the script" % (self.id, self.user) )
            os._exit(1)
        print "Done!  What now?"
    
    
    def signal(self, signame="SIGINT"):
        """
        Do something with this process group depending on the signal
        """
        for node in self.nodefile:
            print "Node is %s" % node
        LOGGER.debug( "Heckle Process Group: runjob: signal" )
        if self.head_pid and self.state != "terminated":
            try:
                os.kill(self.head_pid, getattr(signal, signame))
            except OSError, err:
                LOGGER.exception("Heckle Process Group: runjob: signal"\
                    + "failure for PG %s: %s"% (self.id, err))
        elif not self.head_pid and self.state != "terminated":
            if signame == "SIGINT" or signame == "SIGTERM" or \
                    signame == "SIGKILL":
                os.remove(self.nodefile[1])
                self.exit_status = 1
    
    
    def wait(self):
        """
        Sets the PG state to 'terminated' if done
        """
        LOGGER.debug( "Heckle Process Group: wait" )
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
        logstr = "ProcessGroup:prefork"
        LOGGER.debug(logstr)
        print logstr + "Current State is: %s" % self
        try:            # check for valid user/group
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            raise ProcessGroupCreationError("error getting uid/gid")
        supplementary_group_ids = []
        for gr in grp.getgrall():
            if self.user in gr.gr_mem:
                supplementary_group_ids.append(gr.gr_gid)
                ret["other_groups"] = supplementary_group_ids
        ret["userid"] = userid
        ret["primary_group"] = groupid
        ret["other_groups"] = []
        ret["umask"] = self.umask
        ret["stdin"] = self.stdin
        ret["stdout"] = self.stdout
        ret["stderr"] = self.stderr
        ret["id"] = self.id
        ret["jobid"] = self.jobid
        ret["cobalt_log_file"] = self.cobalt_log_file
        self.nodefile = "/var/tmp/cobalt.%s" % self.jobid
        self.env["COBALT_NODEFILE"] = self.nodefile
        self.env["COBALT_JOBID"] = self.jobid
        ret['environment'] = self.env
        ret["cmd" ] = self.executable
        LOGGER.debug( logstr + "Command dict is %s" % ret)
        return ret

