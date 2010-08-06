#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Heckle System Object Component
Represents, holds, operates upon, and manipulates the 
resources of the machines themselves.
"""
from types import ListType, StringType
import logging

from Cobalt.DataTypes.heckle_temp_ProcessGroup import ProcessGroupDict
from Cobalt.DataTypes.Resource import ResourceDict
from Cobalt.Components.base import Component, automatic, exposed, query
from Cobalt.Exceptions import JobValidationError

from Cobalt.Components.heckle_processgroup import HeckleProcessGroup


#from Cobalt.Components.heckle_lib import *
try:
    from Cobalt.Components.heckle_lib2 import HeckleConnector
except:
    from heckle_lib2 import HeckleConnector



__all__ = ["HeckleSystem"]


LOGGER = logging.getLogger(__name__)


class HeckleSystem(Component):
    """
    Cobalt System component for handling / interacting with Heckle resource manager
    
    External Methods:
        add_process_groups -- allocates nodes
        get_process_groups -- get process groups based on specs
        signal_process_groups -- signal a process group
        wait_process_groups -- removed process groups based on specs
        
    Internal Methods:
        __init__:
        _start_pg:
        _check_builds_done:
        _wait:
        _release_resources:
        get_resources:
        
    Queue Manager Methods:
        validate_job:
        verify_locations:
        find_job_locations:
        find_queue_equivalence_classes:
    """
        
    name = "system"
    implementation = "HeckleBreadboard"
    queue_assignments = {}

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.process_groups = ProcessGroupDict()
        self.process_groups.item_cls = HeckleProcessGroup
        self.queue_assignments["default"] = self.get_resources()
        self.hacky_forbidden_nodes = []   #This is a temporary fix for the forbidden nodes issue
    def __repr__(self):
        """
        printout representation of the class
        """
        indict = self.__dict__
        printstr = ""
        printstr += "Heckle System Object: Values"
        for element in indict:
            printstr += str(element) + "::"
            if indict[element] == None:
                printstr += "None, "
            else:
                printstr += str(indict[element]) + ", "
        printstr += "   Process Groups:"
        for element in self.process_groups:
            printstr += str(element) + "::" + \
            str(self.process_groups[element]) + ", "
        return printstr
    #####################
    # Main set of methods
    #####################
    def add_process_groups(self, specs):
        """
        This function takes the specs (a list of jobs) and initiates each job as
        a process group.
        The process group abstracts the actual job into an object, providing a 
        single point of control and interaction for all the nodes within that job.
        Each job is described by a dict.  Each dict contains:
            size:  
            kernel: a String, the name of the kernel image to load.
            executable: A string, the name of the command to execute upon the
                head node; this could be considered the actual job's file.
            stdin, stdout, stderr:  Three separate strings, each containing
                the file to use for standard communication with the job as it
                is running.  May be specified, or False.
            kerneloptions: A string containing various options for the kernel,
                or False.
            args: A list
            umask: An integer
            jobid: An integer
            cobalt_log_file: A string containing the log file to use in the
                initiation and running of the job itself.
            location:  List of strings of node / resource names
            env:  A dict of key:value strings, specifying the environment in
                which the job is to run on the node
            id: A number
            mode:
            nodect:
            cwd:  A string, specifying the current working directory in which
                to run the job on the node
            walltime:  Integer; the time, in minutes, allocated for the job
                to run on the node.
            user:  A string, the name of the user under which this job is to run.
        """
        logstr = "System:add_process_groups:"
        LOGGER.debug( logstr + "Specs are %s" % specs )
        return self.process_groups.q_add(specs)
    add_process_groups = exposed(query(add_process_groups))
    
    
    def get_process_groups(self, specs):
        """get a list of existing allocations"""
        LOGGER.debug( "System:get_process_groups: specs are %s" % specs )
        self._wait()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))
    
    
    def signal_process_groups(self, specs, sig):
        """Free the specified process group (set of allocated nodes)"""
        LOGGER.debug( 
        "System:signal_process_groups: Specs are %s, sig is %s"\
        % (specs, sig) )
        return self.process_groups.q_get(specs, lambda x, y:x.signal(y), sig)
    signal_process_groups = exposed(query(signal_process_groups))
    
    
    def wait_process_groups(self, specs):
        """Remove terminated process groups"""
        LOGGER.debug( "System:wait_process_groups; specs are %s" % specs )
        return self.process_groups.q_del(specs, lambda x, \
        _:self._release_resources(x))
    wait_process_groups = exposed(query(wait_process_groups))
    
    
    #########################################
    # Methods for dealing with Process Groups
    #########################################
    
    
    def _check_builds_done(self):
        """
        Check to see if the nodes are done building
        Starts the process group if all nodes in them are done building
        """
        #LOGGER.debug( "System:Check Build Done: Waiting to Start..." )
        #sleep(20)
        exstr = "System:check_build_done:"
        retval = True
        pg_list = [x for x in self.process_groups.itervalues()\
        if (len(x.pinging_nodes) > 0)]
        hiccup = HeckleConnector()
        for pgp in pg_list:
            for nodename in pgp.pinging_nodes:
                teststr = hiccup.get_node_bootstate(nodename)
                if teststr == "READY":
                    if 'fakebuild' in pgp.__dict__ and pgp.fakebuild:
                        pgp.pinging_nodes.remove(nodename)
                        LOGGER.debug( exstr + "Node %s done building; "\
                             + "%s pinging nodes left" %\
                             ( nodename, len(pgp.pinging_nodes)-1 ) )
                    else:
                        LOGGER.debug( exstr + "Node %s not done yet" %\
                                          nodename )
                if  teststr == "COMPLETED":
                    LOGGER.debug( exstr + 
                         "Removing node %s...%i pinging nodes left" \
                              % (nodename, len(pgp.pinging_nodes)-1) )
                    pgp.pinging_nodes.remove(nodename)
                elif teststr in ["BOOTING", "", ""]:
                    LOGGER.debug( exstr +
                    "Node %s not done yet." % nodename)
                elif teststr == "UNALLOCATED":
                    raise Exception( exstr +
        "Node 'UNALLOCATED'; Possible build error, or system timed out.")
                elif teststr == "CRITFAIL":
                    raise Exception( exstr +
                "Node says, 'CRITFAIL'.  It timed out while building.")
                #####################
                ####     Need to figure a better way to fail gracefully
                #####################
            if len(pgp.pinging_nodes) == 0:
                LOGGER.debug( 
    "System:Check Build Done: No Pinging Nodes left, Start PG %s Running." \
        % pgp.jobid)
                pgp.start()
            else:
                retval = False
        return retval
    _check_builds_done = automatic(_check_builds_done)
    
    
    def _wait(self):
        """
        Calls the process group container's wait() method
        """
        waitlen = len( self.process_groups.keys() )
        LOGGER.debug( "System:_wait:%s process groups." % waitlen )
        for pgp in self.process_groups.itervalues():
            pgp.wait()
    _wait = automatic(_wait)
    
    
    def _release_resources(self, pgp):
        """
        Releases all the Heckle nodes, unreserving them
        """
        LOGGER.debug( "System:release" )
        LOGGER.debug( "System:Locations are: %s" % pgp.location )
        hiccup = HeckleConnector()
        hiccup.free_reserved_node( uid = pgp.uid, node_list=pgp.location )
    
    
    def get_resources(self, specs=None ):
        """
        Returns a list of free resources (nodes) which match the given specs.
        Specs is a dict which describes a job
        """
        LOGGER.debug( "System:get Resources" )
        ##################################
        ###  Look at this as a future change
        ##################################
        hiccup = HeckleConnector()
        if not specs:
            return hiccup.node_list
        else:
            return hiccup.list_available_nodes( **specs )
    get_resources = exposed(query(get_resources))
    
    
    ##########################################################
    # Methods for interacting with scheduler and queue-manager
    ##########################################################
    
    
    def validate_job(self, spec):
        """
        Validates a job for submission
        -- will the job ever run under the current Heckle configuration?
        Steps:
            1)  Validate Kernel
            2)  Validate HW
            3)  Validate Job versus overall
        """
        LOGGER.debug( "System:Validate Job: Specs are %s" % spec )
        hiccup = HeckleConnector()
        try:
            kernel = spec['kernel']
            valid_kernel = hiccup.validkernel( kernel )
            if not valid_kernel:
                raise Exception("System:Validate Job: Bad Kernel")
        except:
            spec['kernel'] = 'default'
        try:
            valid_hw = hiccup.validhw( **spec['attrs'] )
            if not valid_hw:
                raise Exception(
                "System:Validate Job: Bad Hardware Specs: %s" % spec )
        except Exception as strec:
            raise Exception("System:Validate Job:  Validate Job: %s" % strec)
        #try:
            #valid_job = hiccup.validjob( **spec )
            #if not valid_job:
                #raise Exception(
                #"System: validate Job:  Never enough nodes")
        #except:
            #raise Exception("System: validate Job: Never enough nodes")
        return spec
    validate_job = exposed(validate_job)
    
    
    def verify_locations(self, location_list):
        """
        Makes sure a location list is valid
        location list is a list of fully qualified strings of node names
        ex:  nodename.mcs.anl.gov
        """
        LOGGER.debug("System:validate Job: Verify Locations")
        hiccup = HeckleConnector()
        heckle_set = set(hiccup.list_all_nodes())
        location_set = set(location_list)
        if heckle_set >= location_set:
            return location_list
        else:
            not_valid_list = list( location_set.difference( heckle_set ) )
            raise Exception(
    "System:VerifyLocations: Invalid location names: %s" % not_valid_list)
    verify_locations = exposed( verify_locations )
    
    
    def find_job_location(self, job_location_args, end_times):
        """
        Finds a group of not-busy nodes in which to run the job
        
        Arguments:
            job_location_args -- A list of dictionaries with info about the job
                jobid -- string identifier
                nodes -- int number of nodes
                queue -- string queue name
                required -- ??
                utility_score -- ??
                threshold -- ??
                walltime -- ??
                attrs -- dictionary of attributes to match against
            end_times -- supposed time the job will end
            
        Returns: Dictionary with list of nodes a job can run on, keyed by jobid
        """
        LOGGER.debug("System:find_job_location" )
        locations = {}
        def jobsort(job):
            """Used to sort job list by utility score"""
            return job["utility_score"]
        job_location_args.sort(key=jobsort)
        
        #Try to match jobs to nodes which can run them
        hiccup = HeckleConnector()
        for job in job_location_args:
            if "attrs" not in job or job["attrs"] is None:
                job["attrs"] = {}
            print "Job is %s" % job
            tempjob = job.copy()
            if 'forbidden' not in tempjob.keys():
                tempjob['forbidden'] = self.hacky_forbidden_nodes
            else:
                tempjob['forbidden'].update( self.hacky_forbidden_nodes )
            #############################
            ###  Look at this as point of change
            ###  Think:  For node in unreserved nodes
            ###            Choose node from list
            ###            Remove node from unreserved nodes
            #############################
            resources = hiccup.find_job_location(**job)  #get matching nodes
            if not resources:
                continue
            node_list = []
            # Build a list of appropriate nodes
            for node in resources:
                node_list.append(node)
                self.hacky_forbidden_nodes.append(node)
            locations[job["jobid"]] = node_list
        LOGGER.info("System:find_job_location: locations are %s" % locations )
        return locations
    find_job_location = exposed(find_job_location)
    
    
    def find_queue_equivalence_classes(self, reservation_dict, \
                                                        active_queue_names):
        """
        Finds equivalent queues
        An equivalent queue is a queue which can run upon the same partition(s)
        For now, with one partition (everything!) this is irrelevant.
        Returns: equiv= [{'reservations': [], 'queues': ['default']}]
        """
        #LOGGER.debug("System:find queue equivalence classes" )
        equiv = []
        #print "Reservation_Dict is: %s" % reservation_dict
        #print "Active_queue_names is %s" % active_queue_names
        #print "Queue assignments are: %s" % self.queue_assignments
        for queue in self.queue_assignments:
            # skip queues that aren't running
            if not queue in active_queue_names:
                continue
            found_a_match = False
            #print "Heckle Queue is %s" % queue
            for equ in equiv:
                print "Heckle Equ is %s" % equ
                if equ['data'].intersection(self.queue_assignments[queue]):
                    equ['queues'].add(queue)
                    equ['data'].update(self.queue_assignments[queue])
                    found_a_match = True
                    break
            if not found_a_match:
                equiv.append({'queues': set([queue]),
                                'data': set(self.queue_assignments[queue]),
                                'reservations': set()})
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for equ in real_equiv:
                if equ['queues'].intersection(eq_class['queues']):
                    equ['queues'].update(eq_class['queues'])
                    equ['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)
        equiv = real_equiv
        for eq_class in equiv:
            for res_name in reservation_dict:
                for host_name in reservation_dict[res_name].split(":"):
                    if host_name in eq_class['data']:
                        eq_class['reservations'].add(res_name)
            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
    
    
    def get_partitions(self, locations):
        """
        Work-around to get the cqadm to run a single job on this system
        PRE:  locations is a list of dict of strings of possible node names
        POST:  if good, return locations
                if not good, raise exception and list bad nodes
        """
        logstr = "System:get_partition: "
        hiccup = HeckleConnector()
        heckle_node_set = set(hiccup.list_all_nodes())
        locs = locations[0]['name']
        LOGGER.debug( logstr + "raw is are: %s" % locations )
        LOGGER.debug( logstr + "vals are: %s" % locs )
        if type(locs) == ListType:
            locset = set(locs)
            badlocations = locset.difference(heckle_node_set)
            if badlocations:
                raise Exception(
        logstr + "Bad Locations: %s " % list(badlocations) )
        elif type(locs) == StringType:
            if locs not in locations:
                raise Exception( logstr + "Bad Locations: %s" % locs)
        else:
            raise Exception( logstr + 
"location needs to be string or list of strings, you provided %s : %s" \
% ( type(locs), locs))
        return locations
    get_partitions = exposed(get_partitions)
    
    
