#!/usr/bin/env python

'''Cobalt Queue Simulator library'''

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
import urlparse

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from datetime import datetime

import Cobalt
import Cobalt.Cqparse
import Cobalt.Util

from Cobalt.Components.base import Component, exposed, query, automatic, locking
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.simulator import Simulator
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

MAXINT = 2021072587
MIDPLANE_SIZE = 512
default_SCALE = 2000000
default_SHAPE = 0.9 
default_SENSITIVITY = 0.7
default_SPECIFICITY = 0.9
default_FAILURE_LOG = "failure.lists"

logging.basicConfig()
logger = logging.getLogger('Qsim')

RECOVERYOPT = 1 # by default, the failed job is sent back to the rear of the queue
CHECKPOINT = False  #not used in this version
MTTR = 1200   #time to repair partition(in sec), a failed partition will be available again in MTTR seconds,
FRACTION = 1  #factor to tune workload, the times between job arrival will be multipled with FRACTION.(1 means no change.) 
SET_event = set(['I', 'Q', 'S', 'E', 'F', 'R'])
FAULTAWARE = False

def parseline(line):
    '''parse a line in work load file, return a temp
    dictionary with parsed fields in the line'''
    temp = {}
    firstparse = line.split(';')
    temp['EventType'] = firstparse[1]
    if temp['EventType'] == 'Q':
        temp['submittime'] = firstparse[0]
    temp['jobid'] = firstparse[2]
    substr = firstparse.pop()
    if len(substr) > 0:
        secondparse = substr.split(' ')
        for item in secondparse:
            tup = item.partition('=')
            if not temp.has_key(tup[0]):
                temp[tup[0]] = tup[2]
    return temp

def parse_work_load(filename):
    '''parse the whole work load file, return a raw job dictionary''' 
    temp = {'jobid':'*', 'submittime':'*', 'queue':'*', 
            'Resource_List.walltime':'*','nodes':'*', 'runtime':'*'}
    # raw_job_dict = { '<jobid>':temp, '<jobid2>':temp2, ...}
    raw_job_dict = {}
    wlf = open(filename, 'r')
    for line in wlf:
        if line[0].isdigit():
            line = line.strip('\n')
            temp = parseline(line)
            jobid = temp['jobid']
            #new job id encountered, add a new entry for this job
            if not raw_job_dict.has_key(jobid):
                raw_job_dict[jobid] = temp
            else:  #not a new job id, update the existing entry
                raw_job_dict[jobid].update(temp)
    return raw_job_dict

def tune_workload(specs, frac):
    '''tune workload heavier or lighter'''
    
    print "inside tune_workload"
    
    def _subtimecmp(spec1, spec2):
        return cmp(spec1.get('submittime'), spec2.get('submittime'))
    
    specs.sort(_subtimecmp)
        
    #calc mtbs
    lastsubtime = 0
    for spec in specs:
        if (lastsubtime==0):
            interval = 0
        else:
            interval = spec['submittime'] - lastsubtime
        lastsubtime =  spec['submittime']
        spec['interval'] = interval
    
     #tune workload heavy or light
    
    last_newsubtime = specs[0].get('submittime')
    i = 0
    for spec in specs:
        interval = spec['interval']
        newsubtime = last_newsubtime + frac* interval
        spec['submittime'] = newsubtime
        spec['interval'] = frac* interval
        last_newsubtime = newsubtime
        i += 1
    
    print "in adjust: last submit job=", specs[len(specs)-1].get('submittime')

def sec_to_date(sec, format="%m/%d/%Y %H:%M:%S"):
    tmp = datetime.fromtimestamp(sec)
    fmtdate = tmp.strftime(format)
    return fmtdate    
                      
def date_to_sec(fmtdate, format="%m/%d/%Y %H:%M:%S"):
    t_tuple = time.strptime(fmtdate, format)
    sec = time.mktime(t_tuple)
    return sec

def qsim_quit():
    print "pid=", os.getpid()
    os.kill(os.getpid(), signal.SIGINT)

class Job (Data):
    '''Job for simulation
    Job attribute description and type:
    jobid: int
    submittime:  unix second, float
    queue: queue name, string
    walltime: estimate runtime, minutes, string
    nodes: node number, string
    runtime: seconds, string
    remain_time: seconds, float
    start_time: unix second, float
    end_time: unix second, float
    failure_time: unix second, float
    location: list of string(partition name)
    state: ['invisible', 'running', 'queued', 'ended', 'pending']  string
    is_visible: true/false
    recovery_opt,     #0-4
    first_subtime: unix second, float, the time that the job sumibitted for the first time
    enque_time: the time the job start waiting in queue, used by scheduler?
    '''
    
    fields = Data.fields + ["jobid", "submittime", "queue", "walltime",
                            "nodes","runtime", "start_time", "end_time",
                            "failure_time", "location", "state", "is_visible", 
                            "args",
                            "system_state",
                            "starttime",
                            "project",
                            "is_runnable",
                            "is_active",
                            "has_resources",
                            #below are qsim specific fields
                            "remain_time",    
                            "recovery_opt",     #0-4
                            "arrival_time",
                            "enque_time",
                            "checkpoint",   #0,1
                            ]    

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = 'job'
        #following fields are initialized at beginning of simulation
        self.jobid = int(spec.get("jobid"))
        self.queue = spec.get("queue", "default")
        #self.queue = "default"
                
        self.submittime = spec.get("submittime")   #in seconds
        
        self.walltime = spec.get("walltime")   #in minutes
        
        self.nodes = spec.get("nodes", 0)
        self.runtime = spec.get("runtime", 0)
        self.remain_time = float(self.runtime)       
        self.start_time = spec.get('start_time', '0')
        self.end_time = spec.get('end_time', '0')
        self.state = spec.get("state", "invisible")
        self.system_state = ''
        self.starttime = 0
        self.arrival_time = 0
        self.failure_time = 0
        self.has_resources = False
        self.is_runnable = False
        self.is_visible = False
        self.args = []
        self.progress = 0
        self.recovery_opt = spec.get("recovery_opt", RECOVERYOPT)
        self.checkpoint = 1
        self.location = []

class JobList(DataList):
    '''the list of job objects'''
    item_cls = Job
    
    def __init__(self, _queue):
        self.queue = _queue 

class SimQueue (Queue):
    '''SimQueue object, extended from cqm.Queue, 
     the attribute jobs is qsim.JobList'''
    
    def __init__(self, spec):
        Queue.__init__(self, spec)
        self.jobs = JobList(self)
        self.state = 'running'
        self.tag = 'queue'
        
    def get_joblist(self):
        '''return the job list'''
        return self.jobs
  
class SimQueueDict(QueueDict):
    '''Queue Dict class for simulating, extended from cqm.QueueDict'''
    item_cls = SimQueue
    key = "name"

    def __init__(self, policy):
        QueueDict.__init__(self)
        self.policy = policy
        #create default queue
        self.add_queues([{"name":"default", "policy":self.policy}])         
 
    def add_jobs(self, specs, callback=None, cargs={}):
        '''add jobs to queues, if specified queue not exist, create one''' 
        queue_names = self.keys()
        for spec in specs:
            if spec['queue'] not in queue_names:
                self.add_queues([{"name":spec['queue'], "policy":self.policy}])
                queue_names.append(spec['queue'])
               
        results = []
         # add the jobs to the appropriate JobList
        for spec in specs:
            results += self[spec['queue']].jobs.q_add([spec], callback, cargs)
            
        return results

class PBSlogger:
    '''Logger to generate PBS-style event log'''

    def __init__(self, name):
        #get log directory
        CP = ConfigParser.ConfigParser()
        CP.read(Cobalt.CONFIG_FILES)
        try:
            self.logdir = os.path.expandvars(CP.get('cqm', 'log_dir'))
        except ConfigParser.NoOptionError:
            self.logdir = '.'
            
        #determine log filename
        if name:
            filename = "%s/qsim-%s.log" % (self.logdir, name)
        else:
            self.date = time.localtime()[:3]
            date_string = "%s_%02d_%02d" % self.date
            filename = "%s/qsim-%s.log" % (self.logdir, date_string)    
        
        self.logfile = open(filename, 'w')
        self.name = name

    def closeLog(self):
        self.logfile.close()

    def LogMessage(self, message):
        '''log message into pbs-style log'''
        try:
            self.logfile.write("%s\n" % (message))
            self.logfile.flush()
        except IOError, e:
            logger.error("PBSlogger failure : %s" % e)
    
class Qsimulator(Simulator):
    '''Cobalt Queue Simulator'''
    
    implementation = "qsim"
    name = "queue-manager"
    alias = Simulator.name

    def __init__(self, *args, **kwargs):
        
        print "kwargs= ",  kwargs
        
        #initialize partitions
        Simulator.__init__(self, *args, **kwargs)
        partnames = self._partitions.keys()
        self.init_partition(partnames)
        self.part_size_list = []
        for part in self.partitions.itervalues():
            if int(part.size) not in self.part_size_list:
                self.part_size_list.append(int(part.size))
        self.part_size_list.sort()
   
        #get command line parameters
        self.FAILURE_FREE = True
        self.FRACTION = kwargs.get("fraction", 1)
        self.workload_file =  kwargs.get("workload")
        self.output_log = kwargs.get("outputlog")
        self.failure_log = kwargs.get('failurelog')
        
        self.weibull = kwargs.get('weibull')
        if self.weibull:
            self.SCALE = float(kwargs.get('scale'))
            if self.SCALE == 0:
                self.SCALE = default_SCALE
            self.SHAPE = float(kwargs.get('shape'))
            if self.SHAPE == 0:
                self.SHAPE = default_SHAPE
        
        self.fault_aware = kwargs.get('faultaware')
        self.SENSITIVITY = default_SENSITIVITY
        self.SPECIFICITY = default_SPECIFICITY
        if self.fault_aware:
            self.SENSITIVITY = float(kwargs.get('sensitivity', default_SENSITIVITY))
            self.SPECIFICITY = float(kwargs.get('specificity', defalt_SPECIFICITY))
                
        if self.failure_log or self.weibull:
            self.FAILURE_FREE = False
        
        #initialize time stamps and job queues
        #time stamp format: ('EVENT', 'time_stamp_date', time_stamp_second, {'job_id':str(jobid), 'location':[partition1, partition2,...]})
        self.time_stamps = [('I', '0', 0, {})]
        self.cur_time_index = 0
        self.queues = SimQueueDict(policy=kwargs['policy'])
        self.init_queues()
        
        #initialize failures
        self.failure_dict = {}
        if not self.FAILURE_FREE:
            if self.failure_log:  
                #if specified failure log, use log trace failure
                self.inject_failures()
            elif self.weibull:
                #else MAKE failures by Weibull distribution
                self.make_failures()
        
        #initialize PBS-style logger
        self.pbslog = PBSlogger(self.output_log)
        
        #finish tag
        self.finished = False
        
        #tag for controlling time stamp increment
        self.increment_tag = True
        
        #register local alias "system" for this component
        local_components["system"] = self
        print "Simulation starts:"
             
    def register_alias(self):
        '''register alternate name for the Qsimulator, by registering in slp
        with another name for the same location. in this case 'system' is the
        alternate name'''
        try:
            slp = Cobalt.Proxy.ComponentProxy("service-location", defer=False)
        except ComponentLookupError:
            print >> sys.stderr, "unable to find service-location"
            qsim_quit()
        svc_location = slp.locate(self.name)
        if svc_location:
            slp.register(self.alias, svc_location)
    register_alias = automatic(register_alias, 30)
    
    def is_finished(self):
        return self.finished
    is_finished = exposed(is_finished)
    
    def init_partition(self, namelist):
        '''add all paritions and apply activate and enable'''
        func = self.add_partitions
        args = ([{'tag':'partition', 'name':partname, 'size':"*",
                  'functional':False, 'scheduled':False, 'queue':"*",
                  'deps':[]} for partname in namelist],)
        apply(func, args)
        
        func = self.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in namelist],
                {'scheduled':True, 'functional': True})
        apply(func, args)

        
    def get_current_time_event(self):
        return self.time_stamps[self.cur_time_index][0]
    
    def get_current_time(self):
        '''get current time in date format'''
        return self.time_stamps[self.cur_time_index][1]
    
    def get_current_time_sec(self):
        return self.time_stamps[self.cur_time_index][2]
    get_current_time_sec = exposed(get_current_time_sec)
        
    def get_current_time_job(self):
        ret = None
        if self.time_stamps[self.cur_time_index][3].has_key('jobid'):
            ret = self.time_stamps[self.cur_time_index][3]['jobid']
        return ret
    
    def get_current_time_partition(self):
        if self.get_current_time_event() in set(["R","S"]):
            return self.time_stamps[self.cur_time_index][3]['location']
        else:
            return None
    
    def get_current_time_stamp(self):
        '''get current time stamp index'''
        return self.cur_time_index
    get_current_time_stamp = exposed(get_current_time_stamp)
    
    def get_current_time_stamp_tuple(self):
        return  self.time_stamps[self.cur_time_index]

    def time_increment(self):
        '''the current time stamp increments by 1'''
        if self.cur_time_index < len(self.time_stamps) - 1:
            self.cur_time_index += 1
            print " "
            print str(self.get_current_time()) + \
            " Time stamp is incremented by 1, current time stamp: " + \
            str(self.cur_time_index)
        else:
            print str(self.get_current_time()) +\
            " Reached maximum time stamp: %s, simulating finished! " \
             %  (str(self.cur_time_index))
            self.finished = True
            self.pbslog.closeLog()
            qsim_quit()  #simulation completed, exit!!!
        return self.cur_time_index
       
    def insert_time_stamp(self, new_time_date, event, info):
        '''insert time stamps in the same order'''
        if event not in SET_event:
            print "invalid event type,", event
            return
        
        new_time_sec = date_to_sec(new_time_date)
        new_time_tuple = (event, new_time_date, new_time_sec, info)
                
        pos = len(self.time_stamps)
        
        while new_time_sec < self.time_stamps[pos-1][2]:
            pos = pos - 1
    
        self.time_stamps.insert(pos, new_time_tuple)
        #print "insert time stamp ", new_time_tuple, " at pos ", pos
        return pos
   
    def init_queues(self):
        '''parses the work load log file, initializes queues and sorted time 
        stamp list'''
        
        raw_jobs = parse_work_load(self.workload_file)
        specs = []
        
        tag = 0
        for key in raw_jobs:
            spec = {'valid':True}
            tmp = raw_jobs[key]
            
            spec['jobid'] = tmp.get('jobid')
            spec['queue'] = tmp.get('queue')
            
            #convert submittime from "%m/%d/%Y %H:%M:%S" to Unix time sec
            format_sub_time = tmp.get('submittime')
            if format_sub_time:
                spec['submittime'] = date_to_sec(format_sub_time)
                spec['first_subtime'] = spec['submittime']  #set the first submit time                
            else:
                spec['valid'] = False
                
            #convert walltime from 'hh:mm:ss' to float of minutes
            format_walltime = tmp.get('Resource_List.walltime')
            if format_walltime:
                segs = format_walltime.split(':')
                spec['walltime'] = str(int(segs[0])*60 + int(segs[1]))
            else:  #invalid job entry, discard
                spec['valid'] = False
            
            if tmp.get('start') and tmp.get('end'):
                act_run_time = float(tmp.get('end')) - float(tmp.get('start'))
                spec['runtime'] = str(round(act_run_time, 1))
            else:
                spec['valid'] = False
                
            if tmp.get('Resource_List.nodect'):
                spec['nodes'] = tmp.get('Resource_List.nodect')
            else:  #invalid job entry, discard
                spec['valid'] = False
            
            spec['state'] = 'invisible'
            spec['start_time'] = '0'
            spec['end_time'] = '0'
            
            #add the job spec to the spec list            
            if spec['valid'] == True:
                specs.append(spec)
                
        #adjust workload density
        if FRACTION != 1:
            tune_workload(specs, FRACTION)
            print "workload adjusted: last submit job=", specs[len(specs)-1].get('submittime')
        
        print "Initializing jobs and time stamps list, wait one moment... ..."
        for spec in specs:
            format_sub_time = sec_to_date(spec['submittime']) 
            if not self.time_stamps.__contains__(format_sub_time):
                    self.insert_time_stamp(format_sub_time, 'Q', {'jobid':str(spec['jobid'])})
        
        print "total job number:", len(specs)
        self.add_jobs(specs)

        return 0
    
    def log_job_event(self, eventtype, timestamp, spec):
        '''log job events(Queue,Start,End) to PBS-style log'''
        def len2 (_input):
            _input = str(_input)
            if len(_input) == 1:
                return "0" + _input
            else:
                return _input
        if eventtype == 'Q':  #submitted(queued) for the first time
            message = "%s;Q;%d;queue=%s" % (timestamp, spec['jobid'], spec['queue'])
        elif eventtype == 'R':  #resume running after failure recovery
            message = "%s;R;%s" % (timestamp, ":".join(spec['location']))
        else:
            wall_time = spec['walltime']
            walltime_minutes = len2(int(float(wall_time)) % 60)
            walltime_hours = len2(int(float(wall_time)) // 60)
            log_walltime = "%s:%s:00" % (walltime_hours, walltime_minutes)
            if eventtype == 'S':  #start running 
                message = "%s;S;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s start=%s exec_host=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, spec['start_time'], ":".join(spec['location']))
            elif eventtype == 'E':  #end
                message = "%s;E;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s start=%s end=%f exec_host=%s runtime=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], spec['nodes'], log_walltime, spec['start_time'], 
                 round(float(spec['end_time']), 1), ":".join(spec['location']),
                 spec['runtime'])
            elif eventtype == 'F':  #failure
                frag_runtime = round(float(spec['failure_time']) - float(spec['start_time']), 1)  #running time before failure(after the latest start)
                message = "%s;F;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s exec_host=%s start=%s frag_runtime=%s complete=%f" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, ":".join(spec['location']), spec['start_time'], 
                 frag_runtime, round(frag_runtime / float(spec['runtime']), 2)
                )
            elif eventtype == 'P':  #pending
                message = "%s;P;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s exec_host=%s start=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, ":".join(spec['location']), spec['start_time'], 
                )
                print "message=", message
            else:
                print "invalid event type, type=", type
                return
        self.pbslog.LogMessage(message)
                
    def get_new_states(self, jobspec):
        '''return the new state updates of a specific job at specific time 
        stamp, including invisible->queued, running->ended'''
        
        updates = {}
        curstate = jobspec['state']
        newstate = curstate
        job_id = jobspec['jobid']
       
        cur_event = self.get_current_time_event()
  
        #handle job submssion event       
        if cur_event == 'Q' and curstate == "invisible":
            newstate = "queued"
            updates['is_runnable'] = True
            updates['is_visible'] = True
            self.log_job_event('Q', self.get_current_time(), jobspec)
        
        #handle job completion event
        elif cur_event == 'E' and curstate == "running":
            newstate = "ended"
            updates['is_runnable'] = False
            updates['has_resources'] = False
            updates['is_visible'] = False
            
            #release partition immediately
            partitions = jobspec['location']
            for partition in partitions:
                self.release_partition(partition)
            self.queues.del_jobs([{'jobid':job_id}])
            
            #write to output log
            if jobspec['end_time']:
                end = float(jobspec['end_time'])
            else:
                end = 0
            end_datetime = sec_to_date(end)                                                                                                   
            self.log_job_event('E', end_datetime, jobspec)
        
        #handle job failure event        
        elif cur_event == 'F' and curstate == "running":
            print "entered failure handling"
  
            #release partition
            partitions = jobspec['location']
            for partition in partitions:
                print "partition %s start repairing" % (partition)
                self.start_repair_partition(partition)
             
            #write to output log 
            if jobspec['failure_time']:
                fail = float(jobspec['failure_time'])
            else:
                fail = 0
            failure_datetime = sec_to_date(fail)
            self.log_job_event('F', failure_datetime, jobspec)
            print self.get_current_time(), " job %d failed at %s!!" % (job_id, ":".join(jobspec['location']))
            
            rec_updates = self.recovery_mgr(jobspec)
            
            if not rec_updates == {}:
                updates.update(rec_updates)
                
            if updates.has_key('state'):
                newstate = updates['state']
                
            if CHECKPOINT:
                print "enter checkpoint handling****"
                #runtime before failed after latest start
                frag_runtime = float(jobspec['failure_time']) - float(jobspec['start_time'])
                updates['remain_time'] = jobspec['remain_time'] - frag_runtime
            
            updates['has_resources'] = False
               
        else:#other event
            pass
        
        if updates and not curstate == newstate:
            print self.get_current_time(), "state changed, job", job_id, \
             ":", curstate, "->", newstate
            updates['state'] = newstate
     
        return updates
    
    def update_job_states(self, specs, updates):
        '''update the state of the jobs associated to the current time stamp'''
        
        def _update_job_states(job, newattr):
            '''callback function to update job states'''
            temp = job.to_rx()
            newattr = self.get_new_states(temp)
            if newattr:
                temp.update(newattr)
                job.update(newattr)
                    
        ids_str = self.get_current_time_job()
        ids = ids_str.split(':')
        for id in ids:
            for spec in specs:
                spec['jobid'] = int(id)
            ret = self.queues.get_jobs(specs, _update_job_states, updates)
        return 0
     
    def run_job_updates(self, jobspec, newattr):
        ''' return the state updates (including state queued -> running, 
        setting the start_time, end_time)'''
        updates = {}
        
        #print "enter run_job_updates, jobspec=", jobspec
        
        start = self.get_current_time_sec()
        updates['start_time'] = start
        updates['starttime'] = start

        updates['state'] = 'running'
        updates['system_state'] = 'running'
        updates['is_runnable'] = False
        updates['has_resources'] = True

        print self.get_current_time(), "run job state change, job", jobspec['jobid'], \
             ":", jobspec['state'], "->", updates['state']
             
        #determine whether the job is going to fail before completion
        location = newattr['location']
        duration = jobspec['remain_time']
        #print "duration=", duration
        nearest_failure = self.get_next_failure(location, start, duration)
        if (nearest_failure):
            updates['failure_time'] = date_to_sec(nearest_failure)
            new_time_stamp = nearest_failure
            self.insert_time_stamp(new_time_stamp, 'F', {'jobid':str(jobspec['jobid'])})
        else:  # will complete
            end = start + duration
            updates['end_time'] = end
            new_time_stamp = sec_to_date(end)
            #print "new_time_stamp=", new_time_stamp
            self.insert_time_stamp(new_time_stamp, 'E', {'jobid':str(jobspec['jobid'])})
        
        updates.update(newattr)
    
        return updates
  
    def start_job(self, specs, updates):
        '''update the job state and start_time and end_time when cqadm --run
        is issued to a group of jobs'''
        partitions = updates['location']
        for partition in partitions:
            self.reserve_partition(partition)
            
        def _start_job(job, newattr):
            '''callback function to update job start/end time'''
            temp = job.to_rx()
            newattr = self.run_job_updates(temp, newattr)
            temp.update(newattr)
            job.update(newattr)
            self.log_job_event('S', self.get_current_time(), temp)
        return self.queues.get_jobs(specs, _start_job, updates)
    
    def add_jobs(self, specs):
        '''Add a job, currently for unit test only'''
        response = self.queues.add_jobs(specs)
        return response
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs(self, specs):
        '''get a list of jobs, each time triggers time stamp increment and job
        states update'''

        jobs = []
        if self.increment_tag:
            self.time_increment()
            eventtype = self.get_current_time_event()
            print "current event type====", eventtype
            if eventtype == "R":
                self.release_repaired_partition()
                
                #if the repaired job associated with some pending jobs, 
                #returen empty list to scheduler, in order to ensure the next 
                #time stamp will restart the pending job other than scheduling other jobs at this time stamp
                #this will avoid run multiple jobs on the same partition(once a bug, solved)
                if self.get_current_time_job():
                    return jobs
                    
            elif eventtype == "S":
                
                self.restart_pending_job() 
                return jobs
            
            else:
                self.update_job_states(specs, {})
            #self.update_job_states(specs, {})  #needchange : according to time stamp, update specific job's attribution
        
        if len(self.recovering_jobs) > 0:
            self.update_recovering_jobs({})
        
        self.increment_tag = True
        for spec in specs:
            spec['is_visible'] = True
            spec['jobid'] = "*"   # can't omitted, reset the spec['jobid'] assinged in update_job_states, (once a tricky bug, cost me nearly one day to find!)
        jobs = self.queues.get_jobs(specs)

        #make all job queue "default" so that the scheduler won't skip some jobs based on queue-partition relationship, only in simulation!
        for job in jobs:
            job.queue = "default"
            
#        print "running jobs=", [job.jobid for job in self.running_jobs]
#        print "queueing jobs=", [job.jobid for job in self.queuing_jobs]
#        print "return jobs=", len(jobs) 

        return jobs
    get_jobs = exposed(query(get_jobs))
    
    def update_recovering_jobs(self, updates):
        print "enter update_recovering_jobs()"
        
        def _update_recovering_jobs(job, newattr):
            '''callback function to update job states'''
            temp = job.to_rx()
            print "temp=", temp
            newattr = self.recovery_mgr(temp)
            print "update_recovering_jobs newattr=", newattr
            print "temp=", temp
            if newattr:
                temp.update(newattr)
                job.update(newattr)
                
        ids = [job.jobid for job in self.recovering_jobs]
        print "ids=", ids
        
        ret = self.queues.get_jobs([{'tag':"job", 'state': "recovering"}], _update_recovering_jobs, updates)
        return 0
    
    def _get_queuing_jobs(self):
        return self.queues.get_jobs([{'jobid':"*", 'state':"queued"}])
    queuing_jobs = property(_get_queuing_jobs)
    
    def _get_running_jobs(self):
        return self.queues.get_jobs([{'jobid':"*", 'state':"running"}])
    running_jobs = property(_get_running_jobs)
    
    def _get_recovering_jobs(self):
        return self.queues.get_jobs([{'jobid':"*", 'state':"recovering"}])
    recovering_jobs = property(_get_recovering_jobs)
    
    def _get_job_by_id(self, jobid):
        jobs = self.queues.get_jobs([{'jobid':jobid}])
        if len(jobs) == 1:
            return jobs[0]
        else:
            return None
   
    def get_recovering_jobs(self, specs):
        return self.recovering_jobs
    get_running_jobs = exposed(query(get_recovering_jobs))
           
    def add_queues(self, specs):
        '''add queues'''
        return self.queues.add_queues(specs)
    add_queues = exposed(query(add_queues))
    
    def get_queues(self, specs):
        '''get queues'''
        return self.queues.get_queues(specs)
    get_queues = exposed(query(get_queues))

    def run_jobs(self, specs, nodelist):
        '''run a queued job, by updating the job state, start_time and
        end_time'''
        print "run job specs=", specs, " on partion", nodelist
        if specs:
            self.start_job(specs, {'location': nodelist})
            #set tag false, enable scheduling another job at the same time
            self.increment_tag = False
        #print "current running jobs=", [job.jobid for job in self.running_jobs]
        return self.running_jobs
    run_jobs = exposed(query(run_jobs))
    
    
    def get_midplanes(self, partname):
        '''return a list of sub-partitions each contains 512-nodes(midplane)'''
        midplane_list = []
        partition = self._partitions[partname]
        
        if partition.size == MIDPLANE_SIZE:
            midplane_list.append(partname)
        elif partition.size > MIDPLANE_SIZE:
            children = partition.children
            for part in children:
                if self._partitions[part].size == MIDPLANE_SIZE:
                    midplane_list.append(part)
        else:
            parents = partition.parents
            for part in parents:
                if self._partitions[part].size == MIDPLANE_SIZE:
                    midplane_list.append(part)
                            
        return midplane_list 
    
    def get_next_failure(self, location, now, duration): 
        '''return the next(closest) failure moment according the partition failure list'''
        
        if (self.FAILURE_FREE):
            return None
        
        def _find_next_failure(partname, now):
            next = None
            failure_list = self.failure_dict[partname]
            if failure_list:
                for fail_time in failure_list:
                    if date_to_sec(fail_time) > now:
                        next = fail_time
                        break
            return next
                                       
        closest_fail_sec = MAXINT
        partitions = location

        midplanes = set()
        for partition in partitions:
            tmp_midplanes = self.get_midplanes(partition)
            for item in tmp_midplanes:
                if item not in midplanes:
                    midplanes.add(item)
                        
        for midplane in midplanes:
            next = _find_next_failure(midplane, now)
            if (next):
                next_sec = date_to_sec(next)
                if next_sec < closest_fail_sec:
                    closest_fail_sec =next_sec
        
                        
        if closest_fail_sec == MAXINT:
            next_failure_date = None
        else:
            job_end_sec = now + duration
            if closest_fail_sec < job_end_sec:
                next_failure_date = sec_to_date(closest_fail_sec)
            else:
                next_failure_date = None
                
        #print "next_failure_date=", next_failure_date
                
        return next_failure_date                 

    def will_job_fail(self, mtbf, nodes, hours):
        '''simulate static failure chance, [not used]'''
        return False
        print "mtbf=%d, nodes=%d, hours=%f" % (mtbf,nodes,hours)
        failure_chance = 1 - (1 - hours * 1.0/mtbf) ** nodes
        if failure_chance > 0.7 :
            failure_chance = 0.7
        random_num = random.random()
        print "failure chance=%f, random_num=%f" % (failure_chance, random_num)
        if random_num < failure_chance:
            return True
        else:
            return False
        
    def nodes_static(self):
        '''static the node requested by each job, [not used]'''
        jobs = self.queues.get_jobs([{'jobid':"*", 'queue':"*", 'nodes':"*"}])
        nodesdict = {}
        for job in jobs:
            nodes = int(job.nodes)
            nodesstr = nodes
            if (nodesdict.has_key(nodesstr)):
                nodesdict[nodesstr] =  nodesdict[nodesstr] + 1
            else:
                nodesdict[nodesstr] = 1
        keys = nodesdict.keys()
        keys.sort()
        for key in keys:
            print key, ":", nodesdict[key]
            
    def gen_failure_list(self, scale, shape, startdate, enddate):
        '''generate a synthetic failure time list based on weibull distribution
         and start/end date time'''
        failure_moments = []
        ttf_list = []
                
        start = date_to_sec(startdate)
        end = date_to_sec(enddate)
        
        cur_failure = start
        
        while True:
            ttf = random.weibullvariate(scale,shape)
            cur_failure += ttf
            if cur_failure < end:
                ttf_list.append(ttf)
                failure_moments.append(sec_to_date(cur_failure))
            else:
                break
        return failure_moments, ttf_list
    
    def make_failures(self):
        '''generate failure lists for each 512-nodes partition'''
        ttf_dict = {}
        start = self.time_stamps[1][1]
        end = self.time_stamps[len(self.time_stamps)-1][1]
        
        for partition in self._partitions.values():
            if partition.size == MIDPLANE_SIZE:
                fl, ttfs = self.gen_failure_list(self.SCALE, self.SHAPE, start, end)
                self.failure_dict[partition.name] = fl
                ttf_dict[partition.name] = ttfs
                        
        partnames = self.failure_dict.keys()
        partnames.sort()
        f = open(default_FAILURE_LOG, "w")
        total_f = 0
        mtbf = 0
        for part in partnames:
            f_list = self.failure_dict[part]
            print part, " ", f_list
            f.write("%s;%s\n" % (part, ";".join(f_list)))
            total_f +=  len(f_list)
            
            ttfs = ttf_dict[part]  
            if len(ttfs)==0:
                mtbf = 0
            else:
                total = 0
               
                for ttf in ttfs:
                    total += ttf
                    mtbf = total / len(ttfs)
        start_sec = date_to_sec(start)
        end_sec = date_to_sec(end)
        f.write("Total=%d\nMTBF=%f" % (total_f, (end_sec-start_sec)/(total_f*3600)))

        f.close()
        
    def inject_failures(self):
        '''parse failure trace log to make failure list for each 1-midplane partition'''
                
        raw_job_dict = {}
        partnames = set(self._partitions.keys())
        flog = open(self.failure_log, "r")
        self.failure_dict = {}
        for line in flog:
            print "line=", line
            line = line.strip('\n')
            parsedline = line.split(";")
            print "parsedline=", parsedline
            failure_list = []
            part = parsedline[0]
            if part in partnames:
                for i in range(1, len(parsedline)):
                    failure_moment = parsedline[i]
                    if len(failure_moment) == 0:
                        continue
                    failure_list.append(failure_moment)
                self.failure_dict[part] = failure_list
        partnames = self.failure_dict.keys()
        partnames.sort()
        for part in partnames:
            f_list = self.failure_dict[part]
            print part, " ", f_list   
        
    def get_failure_chance(self, location, duration):
        now = date_to_sec(self.get_current_time())
        next_fail = self.get_next_failure(location, now, duration)
        if (next_fail != None):
            return self.SENSITIVITY
        else:
            return 1 - self.SPECIFICITY
    get_failure_chance = exposed(get_failure_chance)
    
    def recovery_mgr(self, jobspec):
        """Recovery manager, this function can be extended to support various recovery options.
        at this version, the failed job is sent back to the rear of the queue. The extended code
        is ready and available at private code branch(wtang)."""
    
        updates = {}
        
        updates = self.handle_reque_rear(jobspec) 

        recovery_option = jobspec['recovery_opt']
        print "rec_opt=", recovery_option
        
        #if_else structure remains room for recovery option extending   
        if recovery_option == 1:
            #resubmit the job
            #resubmit the job, the submit time changed to NOW
            updates = self.handle_reque_rear(jobspec) 
        
        return updates

    def handle_reque_rear(self, jobspec):
        '''handle option 1 - resubmit the job to rear of waiting queue'''
        updates = {}
        updates['state'] = "queued"
        updates['start_time'] = 0
        updates['submittime'] = self.get_current_time_sec()
        return updates
        
    def start_repair_partition(self, partname):
        '''partition failed, assuming get repaired MTTR seconds later'''
        now = self.get_current_time_sec()
        time_to_repair = now + MTTR
        time_to_repair_date = sec_to_date(time_to_repair)
        self.insert_time_stamp(time_to_repair_date, "R", {'location':partname})
        
    def release_repaired_partition(self):
        '''enter release_repaired_partition() partition repaired'''
        partition = self.get_current_time_partition()
        if partition == None:
            return False
        self.release_partition(partition)
        print "partition %s gets repaired" % (partition)
        self.log_job_event('R', self.get_current_time(), {'location':partition})
        return True
    
    def restart_pending_job(self):
        '''restart jobs that pending for the nodes repair'''
        partname = self.get_current_time_partition()
        print "enter restart_pending_job() partname=", partname
        
        ids_str = self.get_current_time_job()
        ids = ids_str.split(':')
        jobspecs = []
        for id in ids:
            spec = {'tag':'job', 'jobid':int(id)}
            jobspecs.append(spec)
        print "restart pending job ", jobspecs, " on repaired partition ", partname
        self.run_jobs(jobspecs, [partname])
        

    def _find_job_location(self, args, drain_partitions=set(), backfilling=False):
        jobid = args['jobid']
        nodes = args['nodes']
        queue = args['queue']
        utility_score = args['utility_score']
        walltime = args['walltime']
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])

        best_score = sys.maxint
        best_partition = None
                
        available_partitions = set()
        if required:
            for p_name in required:
                available_partitions.add(self.cached_partitions[p_name])
                available_partitions.update(self.cached_partitions[p_name]._children)
        else:
            for p in self.cached_partitions.itervalues():
                skip = False
                for bad_name in forbidden:
                    if p.name==bad_name or bad_name in p.children or bad_name in p.parents:
                        skip = True
                        break
                if not skip:
                    available_partitions.add(p)
        
        available_partitions -= drain_partitions
        now = self.get_current_time_sec()
        
        for partition in available_partitions:
            # check if the current partition is linked to the job's queue (but if reservation locations were
            # passed in via the "required" argument, then we know it's all good)
#            if not required and queue not in partition.queue.split(':'):
#                continue
            
            # if the job needs more time than the partition currently has available, look elsewhere    
            if backfilling:
                if 60*float(walltime) > (partition.backfill_time - now):
                    continue
                
            if self.can_run(partition, nodes, self.cached_partitions):
                # let's check the impact on partitions that would become blocked
                #print "can run ", partition.name
                score = 0
                for p in partition.parents:
                    if self.cached_partitions[p].state == "idle" and self.cached_partitions[p].scheduled:
                        score += 1
                
                if (FAULTAWARE):
                    Pf = 0
                    Pf = self.get_failure_chance(partition.name, 60*float(walltime))
                    score += Pf
                
                # the lower the score, the fewer new partitions will be blocked by this selection
                if score < best_score:
                    best_score = score
                    best_partition = partition        

        if best_partition:
            #print "return bestpartition=",{jobid: [best_partition.name]}
            return {jobid: [best_partition.name]}
 
    def find_job_location(self, arg_list, end_times):
                
        best_partition_dict = {}
        
        if self.bridge_in_error:
            print "bridge_in_error"
            return {}
        
        self._partitions_lock.acquire()
        try:
            self.cached_partitions = copy.deepcopy(self.partitions)
        except Exception,e:
            print e
            self.logger.error("error in copy.deepcopy", exc_info=True)
            return {}
        finally:
            self._partitions_lock.release()

        # first, figure out backfilling cutoffs per partition (which we'll also use for picking which partition to drain)
        job_end_times = {}
        for item in end_times:
            job_end_times[item[0][0]] = item[1]
                    
        now = self.get_current_time_sec()
        for p in self.cached_partitions.itervalues():
            if p.state == "idle":
                p.backfill_time = now
            else:
                p.backfill_time = now + 5*60
            p.draining = False
        
        for p in self.cached_partitions.itervalues():    
            if p.name in job_end_times:
                if job_end_times[p.name] > p.backfill_time:
                    p.backfill_time = job_end_times[p.name]
                
                for parent_name in p.parents:
                    parent_partition = self.cached_partitions[parent_name]
                    if p.backfill_time > parent_partition.backfill_time:
                        parent_partition.backfill_time = p.backfill_time
        
        for p in self.cached_partitions.itervalues():
            if p.backfill_time == now:
                continue
            
            for child_name in p.children:
                child_partition = self.cached_partitions[child_name]
                if child_partition.backfill_time == now or child_partition.backfill_time > p.backfill_time:
                    child_partition.backfill_time = p.backfill_time
        
        # first time through, try for starting jobs based on utility scores
        drain_partitions = set()
        # the sets draining_jobs and cannot_start are for efficiency, not correctness
        draining_jobs = set()
        cannot_start = set()
        for idx in range(len(arg_list)):
            winning_job = arg_list[idx]
            for jj in range(idx, len(arg_list)):
                job = arg_list[jj]
                
                # this job isn't good enough!
                if job['utility_score'] < winning_job['threshold']:
                    break

                if job['jobid'] not in cannot_start:
                    partition_name = self._find_job_location(job, drain_partitions)
                    if partition_name:
                        best_partition_dict.update(partition_name)
                        break
                
                cannot_start.add(job['jobid'])
                
                # we already picked a drain location for the winning job
                if winning_job['jobid'] in draining_jobs:
                    continue

                location = self._find_drain_partition(winning_job)
                if location is not None:
                    for p_name in location.parents:
                        drain_partitions.add(self.cached_partitions[p_name])
                    for p_name in location.children:
                        drain_partitions.add(self.cached_partitions[p_name])
                        self.cached_partitions[p_name].draining = True
                    drain_partitions.add(location)
                    #self.logger.info("job %s is draining %s" % (winning_job['jobid'], location.name))
                    location.draining = True
                    draining_jobs.add(winning_job['jobid'])
            
            # at this time, we only want to try launching one job at a time
            if best_partition_dict:
                break
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_partition_dict:
            
            # arg_list.sort(self._walltimecmp)

            for args in arg_list:
                partition_name = self._find_job_location(args, backfilling=True)
                if partition_name:
                    self.logger.info("backfilling job %s" % args['jobid'])
                    best_partition_dict.update(partition_name)
                    break

        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
        #
        # also, this is the only part of finding a job location where we need to lock anything
        self._partitions_lock.acquire()
        try:
            for p in self.partitions.itervalues():
                # push the backfilling info from the local cache back to the real objects
                p.draining = self.cached_partitions[p.name].draining
                p.backfill_time = self.cached_partitions[p.name].backfill_time
                
            for partition_list in best_partition_dict.itervalues():
                part = self.partitions[partition_list[0]] 
                part.reserved_until = self.get_current_time_sec() + 5*60
                part.state = "starting job"
                for p in part._parents:
                    if p.state == "idle":
                        p.state = "blocked by starting job"
                for p in part._children:
                    if p.state == "idle":
                        p.state = "blocked by starting job"
        except:
            self.logger.error("error in find_job_location", exc_info=True)
        self._partitions_lock.release()
        
        #print "best_partition_dict=", best_partition_dict
        
        return best_partition_dict
    find_job_location = locking(exposed(find_job_location))
