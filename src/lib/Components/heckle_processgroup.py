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
        print "The environment variables at this point are: %s" % spec['env']
        try:
            temp_env = spec['env']['data']
            del(spec['env']['data'])
            spec['env'].update(temp_env)
        except:
            pass
        try:     #  Checking for Fakebuild
            spec['fakebuild'] = spec['env']['fakebuild']
            del spec['env']['fakebuild']
        except:
            spec['fakebuild']=False
        self.env = spec['env']
        # Write nodefile
        self.nodefile = tempfile.mkstemp()
        print "\n\n\n\n\nNodefile is: %s\n\n\n\n\n" % self.nodefile[1]
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
        
    
    
    def __repr__(self):
        """
        Printout Representation of the Class
        """
        logstr = "ProcessGroup:__repr__"
        indict = self.__dict__
        printstr = ""
        printstr += logstr + "Values: ["
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
    
    
    
    def signal(self, signame="SIGINT"):
        """
        Do something with this process group depending on the signal
        """
        logstr = "ProcessGroup:signal:"
        LOGGER.debug( logstr + "%s:%s" % ( self.jobid, signame) )
        try:
            if self.local_id:
                ComponentProxy( "forker" ).signal( self.local_id, signame )
        except OSError as ose:
            LOGGER.exception( logstr + "failure for PG %s: %s" \
                                      % (self.id, err))
    
    
    def wait(self):
        """
        Sets the PG state to 'terminated' if done
        """
        logstr = "ProcessGroup:wait:"
        LOGGER.debug( logstr + "process group %s" % self.jobid )
        if "local_id" in self.__dict__.keys():
            LOGGER.debug( logstr + "Local ID for head node found at %s" % self.local_id )
            exit_status = ComponentProxy( "forker" ).get_status( self.local_id )
            if exit_status:
                exit_status = exit_status['exit_status']
                LOGGER.debug( logstr + "Process %s terminated: %s" 
                              % (self.jobid, exit_status) )
                #exit_status = exit_status >> 8
                # Remove temporary file with node locations
                #os.remove(self.nodefile[1])
                self.exit_status = exit_status
                # Do something if exit status is non-zero
    
    def start(self):
        """
        Starts the process group by:
        1.  Precompiling the data set for the job
        2.  Calling the forker with the job data
        3.  Saving the local_id from the forker
        ###  Still not sure about this, future work here...
        """
        #try:
        data = self.prefork()
        local_id = ComponentProxy("forker").fork(data)
        print "****************************************************"
        print "                  Local ID is %s" % local_id
        print "****************************************************"
        self.local_id = local_id


    def prefork (self):
        """
        Prepares the MPIRUN qualities for the Start function
        * Defines the running environment
        * Defines user and group info
        * Sets up the command line to run the cobalt launcher program
        """
        logstr = "ProcessGroup:prefork:"
        LOGGER.debug(logstr)
        print logstr + "Current State is: %s" % self
        ret = {}
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
        #self.nodefile = "/var/tmp/cobalt.%s" % self.jobid
        self.env["COBALT_NODEFILE"] = self.nodefile
        self.env["COBALT_JOBID"] = self.jobid
        for val in self.env:
            self.env[val] = str( self.env[val] )
        ret['environment'] = self.env
        ret["cmd" ] = self.executable
        LOGGER.debug( logstr + "Command dict is %s\n\n\n" % ret)
        return ret

