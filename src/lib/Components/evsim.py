#!/usr/bin/env python

'''Cobalt Event Simulator'''

import ConfigParser
import copy
import logging
import math
import os
import os.path
import random
import signal
import sys
import time
import inspect

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from datetime import datetime
import time

import Cobalt
import Cobalt.Cqparse
import Cobalt.Util
import Cobalt.Components.bgsched

from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.simulator import Simulator
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

logging.basicConfig()
logger = logging.getLogger('evsim')

no_of_machine = 2
INTREPID = 0
EUREKA = 1
BOTH = 2
UNHOLD_INTERVAL = 1200

SHOW_SCREEN_LOG = False

CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)
if CP.has_section('evsim') and CP.get("evsim", "no_of_machines"):
    no_of_machine = CP.get("evsim", "no_of_machines")
    
def sec_to_date(sec, dateformat="%m/%d/%Y %H:%M:%S"):
    tmp = datetime.fromtimestamp(sec)
    fmtdate = tmp.strftime(dateformat)
    return fmtdate    
                      
def date_to_sec(fmtdate, dateformat="%m/%d/%Y %H:%M:%S"):
    t_tuple = time.strptime(fmtdate, dateformat)
    sec = time.mktime(t_tuple)
    return sec

class Sim_bg_Sched (BGSched):
    
    def __init__(self, *args, **kwargs):
        BGSched.__init__(self, *args, **kwargs)
        
        self.get_current_time = ComponentProxy("event-manager").get_current_time
        
        predict_scheme = kwargs.get("predict", False)
        if predict_scheme:
            self.running_job_walltime_prediction = bool(int(predict_scheme[2]))
        else:
            self.running_job_walltime_prediction = False             
                
class Sim_Cluster_Sched (BGSched):
    
    def __init__(self, *args, **kwargs):
        BGSched.__init__(self, *args, **kwargs)
        self.get_current_time = ComponentProxy("event-manager").get_current_time
        self.COMP_QUEUE_MANAGER = "cluster-queue-manager"
        self.COMP_SYSTEM = "cluster-system"
        self.queues = Cobalt.Components.bgsched.QueueDict(self.COMP_QUEUE_MANAGER)
        self.jobs = Cobalt.Components.bgsched.JobDict(self.COMP_QUEUE_MANAGER)
        self.running_job_walltime_prediction = False
    
class SimEvent (Data):
    
    """A simulated event
    
    Attributes:
    machine -- 0, 1, 2 ... represent the system (e.g. Intrepid or Eureka) where the event occurs
    type -- I (init), Q (submit job), S (start job), E (end job),
    datetime -- the date time at which the event occurs
    unixtime -- the unix time form for datetime
    jobid -- the job id associated with the event
    location -- the location where the event occurs, represented by node list or partition list 
    """
    
    fields = Data.fields + [
        "machine", "type", "datetime", "unixtime",
        "jobid", "location", 
    ]
    
    def __init__ (self, spec):
        """Initialize a new partition."""
        Data.__init__(self, spec)
        spec = spec.copy()
        self.machine = spec.get("machine", 0)
        self.type = spec.get("type", "I")
        self.datetime = spec.get("datetime", None)
        self.unixtime = spec.get("unixtime", None)
        self.jobid = spec.get("jobid", 0)
        self.location = spec.get("location", {})
    
class EventSimulator(Component):
    """Event Simulator. Manages time stamps, events, and the advancing of the clock
        
    Definition of an event, which is a dictionary of following keys:
        machine -- 0, 1, 2 ... represent the system (e.g. Intrepid or Eureka) where the event occurs
        type -- I (init), Q (submit job), S (start job), E (end job),
        datetime -- the date time at which the event occurs
        unixtime -- the unix time form for datetime
        jobid -- the job id associated with the event
        location -- the location where the event occurs, represented by node list or partition list 
    """
    
    implementation = "evsim"
    name = "event-manager"
    
    def __init__(self, *args, **kwargs):
        
        Component.__init__(self, *args, **kwargs)
        self.event_list = [{'unixtime':0}]
        self.time_stamp = 0
        
        self.finished = False
                
        self.bgsched = Sim_bg_Sched(**kwargs)
        
        #inhibit coscheduling and cluster simulation feature before bgsched.py makes change
        #self.csched = Sim_Cluster_Sched()
        
        self.go_next = True
        
    def set_go_next(self, bool_value):
        self.go_next = bool_value
    set_go_next = exposed(set_go_next)
    
    def get_go_next(self,):
        return self.go_next
    get_go_next = exposed(get_go_next)
    
    def events_length(self):
        return len(self.event_list)
    
    def add_event(self, ev_spec):
        '''insert time stamps in the same order'''
        
        time_sec = ev_spec.get('unixtime')
        if time_sec == None:
            print "insert time stamp error: no unix time provided"
            return -1
        
        if not ev_spec.has_key('jobid'):
            ev_spec['jobid'] = 0
        if not ev_spec.has_key('location'):
            ev_spec['location'] = [] 
        
        pos  = self.events_length()
        
        while time_sec < self.event_list[pos-1].get('unixtime'):
            pos = pos - 1
            
        self.event_list.insert(pos, ev_spec)
        #print "insert time stamp ", ev_spec, " at pos ", pos
        return pos
    add_event = exposed(add_event)
    
    def get_time_span(self):
        '''return the whole time span'''
        starttime = self.event_list[1].get('unixtime')
        endtime = self.event_list[-1].get('unixtime')
        timespan = endtime - starttime
        return timespan
    get_time_span = exposed(get_time_span)       
    
    def get_current_time_stamp(self):
        '''return current time stamp'''
        return self.time_stamp
    
    def get_current_time(self):
        '''return current unix time'''
        return self.event_list[self.time_stamp].get('unixtime')
    get_current_time = exposed(get_current_time)
        
    def get_current_date_time(self):
        '''return current date time'''
        return self.event_list[self.time_stamp].get('datetime')
    get_current_date_time = exposed(get_current_date_time)
    
    def get_current_event_type(self):
        '''return current event type'''
        return self.event_list[self.time_stamp].get('type')
    get_current_event_type = exposed(get_current_event_type)
    
    def get_current_event_job(self):
        '''return current event job'''
        return self.event_list[self.time_stamp].get('jobid')
    get_current_event_job = exposed(get_current_event_job)
    
    def get_current_event_location(self):
        return self.event_list[self.time_stamp].get('location')
    get_current_event_location = exposed(get_current_event_location)
    
    def get_current_event_machine(self):
        '''return machine which the current event belongs to'''
        return self.event_list[self.time_stamp].get('machine')
        
    def get_current_event_all(self):
        '''return current event'''
        return self.event_list[self.time_stamp]
    
    def get_next_event_time_sec(self):
        '''return the next event time'''
        if self.time_stamp < len(self.event_list) - 1:
            return self.event_list[self.time_stamp + 1].get('unixtime')
        else:
            return self.get_current_time_date()
    get_next_event_time_sec = exposed(get_next_event_time_sec)
    
        
    def is_finished(self):
        return self.finished
    is_finished = exposed(is_finished)
    
    def clock_increment(self):
        '''the current time stamp increments by 1'''
        if self.time_stamp < len(self.event_list) - 1:
            self.time_stamp += 1
            if SHOW_SCREEN_LOG:
                print str(self.get_current_date_time()) + \
                "[%s]: Time stamp is incremented by 1, current time stamp: %s " % (self.implementation, self.time_stamp)
        else:
            self.finished = True
            
        return self.time_stamp
    clock_intrement = exposed(clock_increment)
   
    def add_init_events(self, jobspecs, machine_id):   ###EVSIM change here        
        """add initial submission events based on input jobs and machine id"""

        for jobspec in jobspecs:
            evspec = {}
            evspec['machine'] = machine_id
            evspec['type'] = "Q"
            evspec['unixtime'] = float(jobspec.get('submittime'))
            evspec['datetime'] = sec_to_date(float(jobspec.get('submittime')))
            evspec['jobid'] = jobspec.get('jobid')
            evspec['location'] = []
            self.add_event(evspec)

    add_init_events = exposed(add_init_events)
    
    def init_unhold_events(self, machine_id):
        """add unholding event"""
        if not self.event_list:
            return
            
        first_time_sec = self.event_list[1]['unixtime']
        last_time_sec = self.event_list[-1]['unixtime']
        
        unhold_point = first_time_sec + UNHOLD_INTERVAL + machine_id
        while unhold_point < last_time_sec:
            evspec = {}
            evspec['machine'] = machine_id
            evspec['type'] = "C"
            evspec['unixtime'] = unhold_point
            evspec['datetime'] = sec_to_date(unhold_point)
            self.add_event(evspec)
            
            unhold_point += UNHOLD_INTERVAL + machine_id
    init_unhold_events = exposed(init_unhold_events)        
    
    def print_events(self):
        print "total events:", len(self.event_list) 
        i = 0
        for event in self.event_list:
            print event
            i += 1
            if i == 25:
                break
    
    def event_driver(self):
        """core part that drives the clock"""
        
        if self.go_next:
            #only if the go_next tag is true will the clock be incremented. enable scheduler schedule multiple job at the same time stamp
            self.clock_increment()
             
        machine = self.get_current_event_machine()
#        print "[%s]: %s, machine=%s, event=%s, job=%s" % (
#                                            self.implementation,
#                                            self.get_current_date_time(), 
#                                            self.get_current_event_machine(), 
#                                            self.get_current_event_type(),
#                                            self.get_current_event_job(),
#                                            )

        if machine == INTREPID:
            self.bgsched.schedule_jobs()
        if machine == EUREKA:
            self.csched.schedule_jobs()
        
        if self.go_next:
            ComponentProxy("queue-manager").calc_loss_of_capacity()
            