#!/usr/bin/env python

'''Cobalt Queue Simulator library'''

import sys
import time
import ConfigParser

import Cobalt
import Cobalt.Util
import Cobalt.Cqparse

from Cobalt.Data import Data, DataList
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Components.base import Component, exposed, query, automatic
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.simulator import Simulator

default_workload_file = "/nfs/mcs-homes15/wtang/workspace/wl-20080530"

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

class Job (Data):
    '''Job for simulation'''
        
    _config = ConfigParser.ConfigParser()

    fields = Data.fields + ["jobid", "submittime", "queue", "walltime",
                            "nodes","runtime", "start_time", "end_time",
                            "location", "state", "is_visible", "args"]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = 'job'
        #following 6 fields are initialized at beginning of simulation
        self.jobid = int(spec.get("jobid"))
        self.queue = spec.get("queue", "default")
        
        self.submittime = spec.get("submittime")   #in seconds
        
        self.walltime = spec.get("walltime")   #in minutes
        
        self.nodes = spec.get("nodes", 0)
        self.runtime = spec.get("runtime", 0)
        
        self.start_time = spec.get('start_time', '0')
        self.end_time = spec.get('end_time', '0')
        self.state = spec.get("state", "invisible")
        self.is_visible = False
        self.args = []
        self.location = ''

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
        
    def get_joblist(self):
        '''return the job list'''
        return self.jobs
  
class SimQueueDict(QueueDict):
    '''Queue Dict class for simulating, extended from cqm.QueueDict'''
    item_cls = SimQueue
    key = "name"
 
    def add_jobs(self, specs, callback=None, cargs={}):
        '''add jobs to queues, if specified queue not exist, create one''' 
        queue_names = self.keys()
        for spec in specs:
            if spec['queue'] not in queue_names:
                self.add_queues([{"name":spec['queue']}])
                queue_names.append(spec['queue'])
               
        results = []
         # add the jobs to the appropriate JobList
        for spec in specs:
            results += self[spec['queue']].jobs.q_add([spec], callback, cargs)
            
        return results
 
         
class Qsimulator(Simulator):
    '''Cobalt Queue Simulator'''
    
    implementation = "qsim"
    name = "queue-manager"
    alias = Simulator.name
        
    def __init__(self, *args, **kwargs):
        Simulator.__init__(self, *args, **kwargs)
        self.queues = SimQueueDict()
        self.time_stamps = [0]
        self.cur_time_index = 0
        self.workload_file = kwargs.get("workload_file", default_workload_file)
        self.init_queues()
        partnames = self._partitions.keys()
        self.init_partition(partnames)
    
    def register_alias(self):
        '''register alternate name for the Qsimulator, by registering in slp
        with another name for the same location. in this case 'system' is the 
        alternate name'''
        try:
            slp = Cobalt.Proxy.ComponentProxy("service-location", defer=False)
        except ComponentLookupError:
            print >> sys.stderr, "unable to find service-location"
            sys.exit(1)
        svc_location = slp.locate(self.name)
        if svc_location:
            slp.register(self.alias, svc_location)
    register_alias = automatic(register_alias, 30)
    
    def init_partition(self, namelist):
        args = ([{'tag':'partition', 'name':partname, 'size':"*", 'functional':False,
                  'scheduled':False, 'queue':'default', 'deps':[]} for partname in namelist],)
        func = self.add_partitions
        apply(func, args)
        
    def get_current_time(self):
        '''get current time in date format'''
        return self.time_stamps[self.cur_time_index]
    
    def get_current_time_stamp(self):
        '''get current time stamp index'''
        return self.cur_time_index

    def time_increment(self):
        '''the current time stamp increments by 1'''
        if self.cur_time_index  < len(self.time_stamps) -1:
            self.cur_time_index += 1
            print str(self.get_current_time()) + \
            " time stamp incremented by 1, current time stamp: " + \
            str(self.cur_time_index)
        else:
            print str(self.get_current_time()) +\
            " Warning: reached maximum time stamp: " +\
            str(self.cur_time_index)
        return self.cur_time_index
   
    def init_queues(self):
        '''parses the work load log file, initializes queues and sorted time 
        stamp list'''
        
        raw_jobs = parse_work_load(self.workload_file)
        specs = []
        
        for key in raw_jobs:
            spec = {}
            tmp = raw_jobs[key]
            
            spec['jobid'] = tmp.get('jobid')
            spec['queue'] = tmp.get('queue')
            
            #convert submittime from "%m/%d/%Y %H:%M:%S" to Unix time sec
            format_sub_time = tmp.get('submittime')
            if format_sub_time:
                t_tuple = time.strptime(format_sub_time, "%m/%d/%Y %H:%M:%S")
                spec['submittime'] = time.mktime(t_tuple)                
            else:
                spec['submittime'] = '0'
                
            #convert walltime from 'hh:mm:ss' to float of minutes
            format_walltime = tmp.get('Resource_List.walltime')
            if format_walltime:
                segs = format_walltime.split(':')
                spec['walltime'] = str(int(segs[0])*60 + int(segs[1]) + \
                                       float(segs[2])/60)
            else:  #raw walltime is none
                spec['walltime'] = '0'
            
            spec['nodes'] = tmp.get('Resource_List.nodect')
            if tmp.get('start') and tmp.get('end'): 
                spec['runtime'] = float(tmp.get('end'))-float(tmp.get('start'))
            
            spec['state'] = 'invisible'
            spec['start_time'] = '0'
            spec['end_time'] = '0'
            
            #add the submit time into the interested time stamps list
            if format_sub_time:
                self.time_stamps.append(format_sub_time)
            #add the job spec to the spec list
            specs.append(spec)
            
        self.time_stamps.sort()
        self.add_jobs(specs)
      
        return 0
    
    def get_new_state(self, jobspec):
        '''return the new state updates of a specific job at specific time 
        stamp, including invisible->queued, running->ended'''
        updates = {}
        curstate = jobspec['state']
        newstate = curstate
        job_id = jobspec['jobid']
   
        #change time of format "%m/%d/%Y %H:%M:%S" to Unix time sec
        cur_tuple = time.strptime(self.get_current_time(), "%m/%d/%Y %H:%M:%S")
        current_time_sec = time.mktime(cur_tuple)
        submit_time_sec = float(jobspec['submittime'])
        if submit_time_sec == 0:  #the never submitted job
            return updates
                        
        if jobspec['end_time']:
            end = float(jobspec['end_time'])
        else:
            end = 0
        
        #make state change, handle invisible->queued, running->ended
        if curstate == 'invisible':
            if  current_time_sec >= submit_time_sec:
                newstate = 'queued'
                updates['is_visible'] = True
        elif curstate == 'running':
            if current_time_sec > end:  #job finished
                newstate = 'ended'
                partitions = jobspec['location'].split(':')
                for partition in partitions:
                    self.release_partition(partition)
                
        if not jobspec['state'] == newstate:
            print self.get_current_time(), "state change, job", job_id, \
             ":", curstate, "->", newstate
            updates['state'] = newstate
        
        return updates               
    
    def run_job_updates(self, jobspec):
        ''' return the state updates (including state queued -> running, 
        setting the start_time, end_time)'''
        updates = {}
        if not jobspec['state'] == 'queued':
            return updates
        t_tuple = time.strptime(self.get_current_time(), "%m/%d/%Y %H:%M:%S")
        current_time_sec = time.mktime(t_tuple)
        start = current_time_sec
        end = current_time_sec + float(jobspec['runtime'])
        updates['start_time'] = start
        updates['end_time'] = end
        updates['state'] = 'running'
        print self.get_current_time(), "state change, job", jobspec['jobid'], \
             ":", jobspec['state'], "->", updates['state']
        return updates
    
    def update_job_states(self, specs, updates):
        '''update the job state field when time stamp increments'''
        def _update_job_states(job, newattr):
            '''callback function to update job states'''
            temp = job.to_rx()
            newattr = self.get_new_state(temp)
            temp.update(newattr)
            job.update(newattr)
        return self.queues.get_jobs(specs, _update_job_states, updates)
                
    def start_job(self, specs, updates):
        '''update the job state and start_time and end_time when cqadm --run
        is issued to a group of jobs'''
        partitions = updates['location'].split(':')
        for partition in partitions:
            self.reserve_partition(partition)
        def _start_job(job, newattr):
            '''callback function to update job start/end time'''
            temp = job.to_rx()
            newattr.update(self.run_job_updates(temp))
            temp.update(newattr)
            job.update(newattr)
        return self.queues.get_jobs(specs, _start_job, updates)
    
    def add_jobs(self, specs):
        '''Add a job, currently for unit test only'''
        response = self.queues.add_jobs(specs)
        return response
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs(self, specs):
        '''get a list of jobs, each time triggers time stamp increment and job
        states update'''
        self.time_increment()
        self.update_job_states(specs, {})
        for spec in specs:
            spec['state'] = 'queued'
        return self.queues.get_jobs(specs)
    get_jobs = exposed(query(get_jobs))
    
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
            self.start_job(specs, {'location': ":".join(nodelist)})
        return self.queues.get_jobs([{'jobid':"*", 'state':"running"}])
    run_jobs = exposed(query(run_jobs))