#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Heckle System Object Component
Represents, holds, operates upon, and manipulates the 
resources of the machines themselves.
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

from time import sleep

from Cobalt.DataTypes.heckle_temp_ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.Components.heckle_resource import Attribute, Resource, ResourceDict, Glossary
from Cobalt.Components.base import Component, automatic, exposed, query
from Cobalt.Exceptions import JobValidationError

from Cobalt.Components.heckle_processgroup import *

from heckle.lib.util import createSessionInstance

from Cobalt.Components.heckle_lib import *

import threading



__all__ = ["HeckleSystem"]


logger = logging.getLogger(__name__)


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
          logger.debug( "heckle: System: init ... %s ... &&&&&&&&&&&&&&&&&&&&&&&&&&&&&  I am here as well &&&&&&&&&&&&&&&&&&&&&&&&&" % threading.current_thread().getName() )
          Component.__init__(self, *args, **kwargs)
          self.process_groups = ProcessGroupDict()
          self.process_groups.item_cls = HeckleProcessGroup
          self.resources = ResourceDict()
          self.queue_assignments["default"] = self.resources.keys()
          print "\n\n\n\n"
          print "Queue assignments are: %s" % self.queue_assignments
     
     
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
               printstr+= str(element) +"::" + str(self.process_groups[element]) + ", "
          return printstr
     
     
     #####################
     # Main set of methods
     #####################
     def add_process_groups(self, specs):
          """
          Allocate nodes and add the list of those allocated to the PGDict
          specs is a list of dictionaries
          Each dictionary contains the specifications for all the nodes in the process group
          """
          #Debug - Take out to really rebuild
          ####    Need to check the environment variable for fakebuild
          try:
               specs[0]['fakebuild'] = specs[0]['env']['fakebuild']
               del specs[0]['env']['fakebuild']
          except:
               pass
          print "Heckle System:  add_process_groups: <<<<<<<<<<<<<<<<<<          OK< Debug< This< :  %s" % specs
          HICCUP= Heckle_Interface()
          #try:
          reservation = HICCUP.make_reservation( **(specs[0]) )
          heckle_res_id = reservation.id
          uid = specs[0]['user']
          logger.debug( "Heckle System: heckle_res_id = %i" % heckle_res_id )
          specs[0]['heckle_res_id']=heckle_res_id
          return self.process_groups.q_add(specs, lambda x, _:self._start_pg(x, heckle_res_id = heckle_res_id, uid=uid))
          #except Exception as hec_except:
               ## could do something here about problems
               ##    1)  Kill job, then resubmit job w/o node name(s)
               ##         Would require access to cqadm via api
               ##    2)  Put job / node in fail state
               ##    3)  Simply fail
               #raise Exception("Heckle System Object: add_process_groups: %s" % hec_except)
     add_process_groups = exposed(query(add_process_groups))
     
     
     def get_process_groups(self, specs):
          """Get a list of existing allocations"""
          #logger.debug( "Heckle System: get_process_groups" )
          self._wait()
          return self.process_groups.q_get(specs)
     get_process_groups = exposed(query(get_process_groups))
     
     
     def signal_process_groups(self, specs, sig):
          """Free the specified process group (set of allocated nodes)"""
          logger.debug( "Heckle System: signal_process_groups: Specs are %s, sig is %s" % (specs, sig) )
          return self.process_groups.q_get(specs, lambda x, y:x.signal(y),
                                             sig)
     signal_process_groups = exposed(query(signal_process_groups))
     
     
     def wait_process_groups(self, specs):
          """Remove terminated process groups"""
          logger.debug( "Heckle System: wait_process_groups; specs are %s" % specs )
          return self.process_groups.q_del(specs, lambda x,
                                             _:self._release_resources(x))
     wait_process_groups = exposed(query(wait_process_groups))
     
     
     #########################################
     # Methods for dealing with Process Groups
     #########################################
     
     
     def _start_pg(self, pgp):
          """
          Populates the process group with its resources
               Gets node information for nodes in process group
               Updates those attributes
               Places nodes in the pinging nodes list, to see if they're built
          """
          logger.debug( "Heckle System: start_pg: PGP is %s" % pgp )
          nodelist = pgp.location
          #self.resource[nodelist]['action'] = action
          self.resource[nodelist]['mac'] = self.resource[nodelist]['mac'].replace("-",":")
          pgp.pinging_nodes.append(nodelist)
     add_process_groups = exposed(query(add_process_groups))
     
     
     def _check_builds_done(self):
          """
          Check to see if the nodes are done building
          Starts the process group if all nodes in them are done building
          """
          #logger.debug( "heckle: System: Check Build Done: Waiting to Start..." )
          #sleep(20)
          retval = True
          pg_list = [x for x in self.process_groups.itervalues() if (len(x.pinging_nodes) > 0)]
          self.resources.update()
          for pgp in pg_list:
               for nodename in pgp.pinging_nodes:
                    teststr = self.resources[nodename]['bootstate']
                    if  teststr == "COMPLETED":
                         logger.debug( "heckle: System: Check Build Done: Removing node %s...%i pinging nodes left" % (nodename, len(pgp.pinging_nodes)-1) )
                         pgp.pinging_nodes.remove(nodename)
                    elif teststr in ["BOOTING", "", ""]:
                         logger.debug( "Heckle System: Check Build Done: Node %s not done yet." % nodename)
                    elif teststr == "UNALLOCATED":
                         raise Exception("HIC_SO: _check_builds_done: Node says, 'UNALLOCATED'.  Possible build error, or system timed out.")
                    elif teststr == "CRITFAIL":
                         raise Exception("HIC_SO: _check_builds_done: Node says, 'CRITFAIL'.  It timed out while building.")
                         #####################
                         ####      Need to figure a better way to fail gracefully on this one...
                         #####################
                    elif teststr == "READY":
                         raise Exception("HIC_SO: _check_builds_done: Node says, 'READY'.  The Heckle Reservation is already ready already, skipping pinging.")
               if len(pgp.pinging_nodes) == 0:
                    logger.debug( "Heckle System: Check Build Done: No Pinging Nodes left, Start PG Running.")
                    pgp.start()
               else:
                    retval = False
          return retval
     _check_builds_done = automatic(_check_builds_done)
     
     
     def _wait(self):
          """
          Calls the process group container's wait() method
          """
          #logger.debug( "Heckle System: wait" )
          for pgp in self.process_groups.itervalues():
               pgp.wait()
     _wait = automatic(_wait)
     
     
     def _release_resources(self, pgp):
          """
          Releases all the Heckle nodes, unreserving them
          """
          logger.debug( "Heckle System: Release %s" % pgp.location )
          #self.resources[pgp.location]['action']='Free'
          HICCUP= Heckle_Interface()
          HICCUP.free_reserved_node( uid = pgp.uid, node_list=pgp.location )
          self.resources.free( nodes=pgp.location )
     
     
     def get_resources(self, specs={}):
          """
          Returns a list of names for all the resources (nodes) which match the given specs.
          """
          logger.debug( "Heckle System: Get Resources, specs are %s" % specs )
          ##################################
          ###  Look at this as a future change
          ##################################
          specs['current reservation'] = 9999999
          specs['allocatable'] = 'True'
          res_list = self.resources >= specs
          logger.debug( "Heckle System: Get Resources, resources are %s" % res_list )
          return res_list
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
          logger.debug( "Heckle System: Validate Job: Specs are %s" % spec )
          try:
               checklist = spec['attrs']
          except:
               checklist = {}
          #del(checklist['action'])
          try:
               nodecount = spec['nodecount']
          except:
               nodecount = 1
          glossary = self.resources.glossary
          dnelist = []   # for attributes which do not exist in glossary
          badlist = []   # for attributes in glossary which do not exist
          ##################################
          ###  Look at this as a future change
          ###  Think:  Refresh Resources Info
          ##################################
          #1st step:  Are there enough nodes at all?
          if nodecount >= self.resources.node_count():
               pass
          else:
               raise Exception( "Validate Job: Not enough nodes; Requested %s, only have %s in the system." % ( nodecount, self.resources.nodecount() ) )
          for att in checklist:
               val = checklist[att]
               try:
                    if val in glossary[att]:
                         pass
                    else:
                         badlist.append("%s:%s"%(att, val)) # Bad attribute
               except:
                    dnelist.append(att) #Attribute does not exist
               checklist['current reservation'] = 9999999
               checklist['allocatable'] = 'True'
               retlist = self.resources >= checklist
               retcount = len(retlist)
               goodlen = retcount >= nodecount
               if goodlen and not badlist and not dnelist:
                    return spec         #Good Job!
               else:
                    retstr = "Validate Job: "
                    if badlist or dnelist:
                         if badlist:
                              restr += "No value for attribute: %s" % badlist
                         if dnelist:
                              retstr += "Attributes Do Not Exist: %s" % dnelist
                    else:
                         retstr += "Need %s nodes, only have %s nodes:  %s" % (nodecount, retcount, retlist)
                    raise Exception( retstr )
          return spec
     validate_job = exposed(validate_job)
     
     
     def verify_locations(self, location_list):
          """
          Makes sure a location list is valid
          location list is a list of fully qualified strings of node names
          ex:  nodename.mcs.anl.gov
          """
          logger.debug("heckle: System: Validate Job: Verify Locations")
          return location_list in self.resources.glossary
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
          logger.debug("heckle: System: find_job_location" )
          locations = {}
          def jobsort(job):
               """Used to sort job list by utility score"""
               return job["utility_score"]
          job_location_args.sort(key=jobsort)          
          #Try to match jobs to nodes which can run them
          for job in job_location_args:
               if "attrs" not in job or job["attrs"] is None:
                    attrs = {}
               else:
                    attrs = job['attrs']
               attrs['current reservation'] = 9999999
               attrs['allocatable'] = 'True'
               nodecount = int(job['nodes'])
               print "Job is %s" % job
               #############################
               ###  Look at this as point of change
               ###  Think:  For node in unreserved nodes
               ###            Choose node from list
               ###            Remove node from unreserved nodes
               #############################
               print "Free Nodes is %s" % self.resources.getfreenodes()
               nodelist = ( self.resources >= attrs )    # Get Matching Node
               print "Nodelist at this stage is %s" % nodelist
#               if len(nodelist) >= nodecount:
               print "Nodecount = %s" % nodecount
               retlist = nodelist[:nodecount]
               self.resources.allocate(retlist)
               print "Remaining nodelist is %s" % retlist
#               else:
#                    raise Exception ("Something, Not Enough matching Nodes Available")
               locations[job["jobid"]]=retlist
               print "Locations is now: %s" % locations
          logger.info("heckle: find_job_location: locations are %s" % locations )
          return locations
     find_job_location = exposed(find_job_location)
     
     
     def find_queue_equivalence_classes(self, reservation_dict, active_queue_names):
        """
        Finds equivalent queues
        An equivalent queue is a queue which can run upon the same partition(s)
        For now, with one partition (everything!) this is irrelevant.
        Returns: equiv= [{'reservations': [], 'queues': ['default']}]
        """
        logger.debug("Heckle System: find queue equivalence classes" )
        equiv = []
        #print "Reservation_Dict is: %s" % reservation_dict
        #print "Active_queue_names is %s" % active_queue_names
        #print "Queue assignments are: %s" % self.queue_assignments
        for queue in self.queue_assignments:
            # skip queues that aren't running
            if not queue in active_queue_names:
                continue
            found_a_match = False
            print "Heckle Queue is %s" % queue
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
          nodelist = self.resources.Glossary.nodelist
          logger.debug("Heckle System: get_partitions: raw is are: %s" % locations )
          logger.debug("Heckle System: get_partitions: vals are: %s" % locs )
          if locations in nodelist:
               return locations
          else:
               raise Exception("heckle: System: get_partition: Bad Locations: %s " % badlocations)
     get_partitions = exposed(get_partitions)
     
     
     
     
     
     
     
     
     
     
     
     
