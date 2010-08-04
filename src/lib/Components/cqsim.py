#!/usr/bin/env python

'''Cobalt Queue Simulator (for Blue Gene systems) library'''

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

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from datetime import datetime

import Cobalt
import Cobalt.Cqparse
import Cobalt.Util

from Cobalt.Components.base import exposed, query, automatic, locking
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.cluster_base_system import ClusterBaseSystem
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

REMOTE_QUEUE_MANAGER = "queue-manager"

MACHINE_ID = 1
MACHINE_NAME = "EUREKA"

logging.basicConfig()
logger = logging.getLogger('Qsim')

SET_event = set(['I', 'Q', 'S', 'E', 'F', 'R'])

REDS = '\033[95m'
YELLOWS = '\033[93m'
BLUES = '\033[94m'
GREENS = '\033[92m'
ENDC = '\033[0m'

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('cqm'):
    print '''"cqm" section missing from cobalt config file'''
    sys.exit(1)

def get_histm_config(option, default):
    try:
        value = config.get('histm', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

prediction_scheme = get_histm_config("prediction_scheme", "paired")  # ["project", "user", "combine        # *AdjEst*

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

def parseline_alt(line):
    '''parse a line from alternative format'''
    def len2 (_input):
        _input = str(_input)
        if len(_input) == 1:
            return "0" + _input
        else:
            return _input
    
    temp= {}
    splits = line.split(';')
        
    for item in splits:
        tup = item.partition('=')
        temp[tup[0]] = tup[2]
    
    fmtdate = temp['qtime']
    submittime_sec = date_to_sec(fmtdate, "%Y-%m-%d %H:%M:%S")
    submittime_date = sec_to_date(submittime_sec)
    temp['submittime'] = submittime_date
    start_date = temp['start']
    start_sec = date_to_sec(start_date, "%Y-%m-%d %H:%M:%S")
    temp['start'] = start_sec
    end_date = temp['end']
    end_sec = date_to_sec(end_date, "%Y-%m-%d %H:%M:%S")
    temp['end'] = end_sec
    walltime_sec = temp['Resource_List.walltime']
    wall_time = int(float(walltime_sec) / 60) 
    walltime_minutes = len2(wall_time % 60)
    walltime_hours = len2(wall_time // 60)
    fmt_walltime = "%s:%s:00" % (walltime_hours, walltime_minutes)
    temp['Resource_List.walltime'] = fmt_walltime

    return temp

def parse_work_load(filename):
    '''parse the whole work load file, return a raw job dictionary''' 
    temp = {'jobid':'*', 'submittime':'*', 'queue':'*', 
            'Resource_List.walltime':'*','nodes':'*', 'runtime':'*'}
    # raw_job_dict = { '<jobid>':temp, '<jobid2>':temp2, ...}
    raw_job_dict = {}
    wlf = open(filename, 'r')
    for line in wlf:
        line = line.strip('\n')
        line = line.strip('\r')
        if line[0].isdigit():
            temp = parseline(line)
        else:
            temp = parseline_alt(line)
        jobid = temp['jobid']
        #new job id encountered, add a new entry for this job
        if not raw_job_dict.has_key(jobid):
            raw_job_dict[jobid] = temp
        else:  #not a new job id, update the existing entry
            raw_job_dict[jobid].update(temp)
            
    return raw_job_dict

def _subtimecmp(spec1, spec2):
        return cmp(spec1.get('submittime'), spec2.get('submittime'))

def tune_workload(specs, frac=1, anchor=0):
    '''tune workload heavier or lighter, and adjust the start time to anchor. specs should be sorted by submission time'''

    #calc intervals (the first job's interval=0, the i_th interval is sub_i - sub_{i-1}
    lastsubtime = 0
    for spec in specs:
        if (lastsubtime==0):
            interval = 0
        else:
            interval = spec['submittime'] - lastsubtime
        lastsubtime =  spec['submittime']
        spec['interval'] = interval
    
    #if anchor is specified, set the first job submission time to anchor
    if anchor:
        specs[0]['submittime'] = anchor
    else:
        pass
        
    last_newsubtime = specs[0].get('submittime')    
    for spec in specs:
        interval = spec['interval']
        newsubtime = last_newsubtime + frac * interval
        spec['submittime'] = newsubtime
        spec['interval'] = frac * interval
        last_newsubtime = newsubtime
    
def sec_to_date(sec, dateformat="%m/%d/%Y %H:%M:%S"):
    tmp = datetime.fromtimestamp(sec)
    fmtdate = tmp.strftime(dateformat)
    return fmtdate    
                      
def date_to_sec(fmtdate, dateformat="%m/%d/%Y %H:%M:%S"):
    t_tuple = time.strptime(fmtdate, dateformat)
    sec = time.mktime(t_tuple)
    return sec

def get_bgsched_config(option, default):
    try:
        value = config.get('bgsched', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

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
    first_subtime: unix second, float, the time that the job sumibitted for the first time
    enque_time: the time the job start waiting in queue, used by scheduler?
    recovering: indicating that the job was failed in the process of recovering
    '''
    
    fields = Data.fields + ["jobid", "submittime", "queue", "walltime",
                            "nodes","runtime", "start_time", "end_time", "hold_time", "yield_time"
                            "failure_time", "location", "state", "is_visible", 
                            "args",
                            "user",
                            "system_state",
                            "starttime",
                            "project",
                            "is_runnable",
                            "is_active",
                            "has_resources",
                            "attr",
                            "score",
                            "remain_time",    
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
        self.walltime_p = spec.get("walltime_p") #  *AdjEst* 
        self.user = spec.get("user", "unknown")
        self.project = spec.get("project", "unknown")
        self.nodes = spec.get("nodes", 0)
        self.runtime = spec.get("runtime", 0)
        self.remain_time = float(self.runtime)       
        self.start_time = spec.get('start_time', '0')
        self.end_time = spec.get('end_time', '0')
        self.hold_time = spec.get('hold_time', 0)  #the time the job starts holding (coscheduling only)
        self.yield_time = spec.get('yield_time', 0) #the time the job first yields (coscheduling only)
        self.state = spec.get("state", "invisible")
        self.system_state = ''
        self.starttime = 0
        self.has_resources = False
        self.is_runnable = spec.get("is_runnable", False)
        self.is_visible = False
        self.score = float(spec.get("score", 0.0))
        self.attrs = spec.get("attrs", {})
        self.args = []
        self.progress = 0
        #self.checkpoint = 1
        self.recovering = False
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
        self.add_queues([{"name":"default", "policy":"default"}])         
 
    def add_jobs(self, specs, callback=None, cargs={}):
        '''add jobs to queues, if specified queue not exist, create one''' 
        queue_names = self.keys()
        
        for spec in specs:
            if spec['queue'] not in queue_names:
                spec['queue'] = "default"
   
#               self.add_queues([{"name":spec['queue'], "policy":self.policy}])
#               queue_names.append(spec['queue'])
               
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
            
        if not os.path.isdir(self.logdir):
            os.system('mkdir %s' % self.logdir)        
            
        #determine log filename
        if name:
            filename = "%s/%s-qsim-%s.log" % (self.logdir, MACHINE_NAME, name)
        else:
            self.date = time.localtime()[:3]
            date_string = "%s_%02d_%02d" % self.date
            filename = "%s/%s-qsim-%s.log" % (self.logdir, MACHINE_NAME, date_string)    
        
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
            
    
class ClusterQsim(ClusterBaseSystem):
    '''Cobalt Queue Simulator for cluster systems'''
    
    implementation = "cqsim"
    name = "cluster-queue-manager"
    alias = "cluster-system"
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        
        ClusterBaseSystem.__init__(self, *args, **kwargs)
                
        self.sleep_interval = kwargs.get("sleep_interval", 0)
        
        self.fraction = kwargs.get("cluster_fraction", 1)
        self.sim_start = kwargs.get("c_trace_start", 0)
        self.sim_end = kwargs.get("c_trace_end", sys.maxint)
        self.anchor = kwargs.get("anchor", 0)
        
        self.workload_file =  kwargs.get("cjob")
        self.output_log = kwargs.get("outputlog")
        self.bgjob = kwargs.get("bgjob")
        
        self.event_manager = ComponentProxy("event-manager")
      
        walltime_prediction = get_histm_config("walltime_prediction", False)   # *AdjEst*
        print "walltime_prediction=", walltime_prediction
        if walltime_prediction in ["True", "true"]:
            self.walltime_prediction = True
        else:
            self.walltime_prediction = False
            
        self.time_stamps = [('I', '0', 0, {})]
        self.cur_time_index = 0
        self.queues = SimQueueDict(policy=None)
        
 #       self.invisible_job_dict = {}   # for jobs not submitted, {jobid:job_instance}
        self.unsubmitted_job_spec_dict = {}   #{jobid: jobspec}

        self.num_running = 0
        self.num_waiting = 0
        self.num_busy = 0
        self.num_end = 0
        self.total_job = 0
        self.total_nodes = len(self.all_nodes)
                
        self.init_queues()

        #initialize PBS-style logger
        self.pbslog = PBSlogger(self.output_log)
        
        #initialize debug logger
        if self.output_log:
            self.dbglog = PBSlogger(self.output_log+"-debug")
        else:
            self.dbglog = PBSlogger(".debug")
        
        #finish tag
        self.finished = False
        
        #register local alias "system" for this component
        local_components["cluster-system"] = self
        
        #initialize capacity loss
        self.capacity_loss = 0
                
        #starting job(id)s at current time stamp. used for calculating capacity loss
        self.starting_jobs = []
        
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}
                        
        self.define_builtin_utility_functions()
        self.define_user_utility_functions()
        
        _cosched_scheme = kwargs.get("coscheduling", (0,0))
        self.cosched_scheme = _cosched_scheme[1]
        self.cosched_scheme_remote = _cosched_scheme[0]
        
        valid_cosched_schemes = ["hold", "yield"]
        
        if self.cosched_scheme in valid_cosched_schemes and self.cosched_scheme_remote in valid_cosched_schemes:
            self.coscheduling = True
        else:
            self.coscheduling = False
        
        if self.coscheduling:
            bg_mate_dict = ComponentProxy(REMOTE_QUEUE_MANAGER).get_mate_job_dict()
            self.job_hold_dict = {}
            self.mate_job_dict = dict((v,k) for k, v in bg_mate_dict.iteritems())
            matejobs = len(self.mate_job_dict.keys())
            proportion = float(matejobs) / self.total_job
            print "number mate job pairs: %s, proportion in cluster jobs: %s%%" \
            % (len(self.mate_job_dict.keys()), round(proportion *100, 1) ) 
        else:
            self.mate_job_dict = {}
            
        #record yield jobs's first yielding time, for calculating the extra waiting time
        self.yielding_job_dict = {}
        
        #record yield job ids. update dynamically
        self.yielding_job_list = []
        
        if self.coscheduling:
            print "co-scheduling enabled, local scheme=%s, remote scheme=%s" % (self.cosched_scheme, self.cosched_scheme_remote)
  
        Var = raw_input("press any Enter to continue...")
                
        print "Simulation starts:"
        
            
    def init_mate_job_dict(self):
        '''initialize mate job dict'''
        pass
    
    def is_finished(self):
        return self.finished
    is_finished = exposed(is_finished)
    
    def get_current_time(self):
        '''this function overrid the get_current_time in bgsched, bg_base_system, and cluster_base_system'''
        return  self.event_manager.get_current_time()
    
    def get_current_time_sec(self):
        return  self.event_manager.get_current_time()
    
    def get_current_time_date(self):
        return self.event_manager.get_current_date_time()

    def time_increment(self):
        '''the current time stamp increments by 1'''
        self.event_manager.clock_increment()
       
    def insert_time_stamp(self, timestamp, type, info):
        '''insert time stamps in the same order'''
        if type not in SET_event:
            print "invalid event type,", type
            return
        
        evspec = {}
        evspec['jobid'] = info.get('jobid', 0)
        evspec['type'] = type
        evspec['datetime'] = sec_to_date(timestamp)
        evspec['unixtime'] = timestamp
        evspec['machine'] = MACHINE_ID
        
        self.event_manager.add_event(evspec)
        
    def init_queues(self):
        '''parses the work load log file, initializes queues and sorted time 
        stamp list'''
        
        print "Initializing cluster jobs, one moment please..."
        
        raw_jobs = parse_work_load(self.workload_file)
        specs = []
        
        tag = 0
        for key in raw_jobs:
            spec = {}
            tmp = raw_jobs[key]
            
            spec['jobid'] = tmp.get('jobid')
            spec['queue'] = tmp.get('queue')
            
            #convert submittime from "%m/%d/%Y %H:%M:%S" to Unix time sec
            format_sub_time = tmp.get('submittime')
            if format_sub_time:
                qtime = date_to_sec(format_sub_time)
                if qtime < self.sim_start or qtime > self.sim_end:
                    continue        
                spec['submittime'] = qtime
                #spec['submittime'] = float(tmp.get('qtime'))
                spec['first_subtime'] = spec['submittime']  #set the first submit time                
            else:
                continue
                
            spec['user'] = tmp.get('user')
            spec['project'] = tmp.get('account')
                
            #convert walltime from 'hh:mm:ss' to float of minutes
            format_walltime = tmp.get('Resource_List.walltime')
            spec['walltime'] = 0
            if format_walltime:
                segs = format_walltime.split(':')
                walltime_minuntes = int(segs[0])*60 + int(segs[1])
                spec['walltime'] = str(int(segs[0])*60 + int(segs[1]))
            else:  #invalid job entry, discard
                continue
            
            if tmp.get('start') and tmp.get('end'):
                act_run_time = float(tmp.get('end')) - float(tmp.get('start'))
                if act_run_time / (float(spec['walltime'])*60) > 1.1:
                    act_run_time = float(spec['walltime'])*60
                spec['runtime'] = str(round(act_run_time, 1))
            else:
                continue
                
            if tmp.get('Resource_List.nodect'):
                spec['nodes'] = tmp.get('Resource_List.nodect')
                if int(spec['nodes']) == 40960:
                    continue                    
            else:  #invalid job entry, discard
                continue
            
            if self.walltime_prediction: #*AdjEst*  
                ap = self.get_walltime_Ap(spec)
                spec['walltime_p'] = int(spec['walltime']) * ap
            else:
                spec['walltime_p'] = int(spec['walltime'])
             
            spec['state'] = 'invisible'
            spec['start_time'] = '0'
            spec['end_time'] = '0'
            spec['queue'] = "default"
            spec['has_resources'] = False
            spec['is_runnable'] = False
            
            #add the job spec to the spec list            
            specs.append(spec)

        specs.sort(_subtimecmp)
                
        #adjust workload density and simulation start time
        if self.fraction != 1 or self.anchor !=0 :
            tune_workload(specs, self.fraction, self.anchor)
            print "workload adjusted: "
            print "first job submitted:", sec_to_date(specs[0].get('submittime'))
            print "last job submitted:", sec_to_date(specs[len(specs)-1].get('submittime'))
        
        self.total_job = len(specs)
        print "total job number:", self.total_job
        
        #self.add_jobs(specs)
       
        self.unsubmitted_job_spec_dict = self.init_unsubmitted_dict(specs)
        
                        
        self.event_manager.add_init_events(specs, MACHINE_ID)

        return 0
    
    def init_unsubmitted_dict(self, specs):
        #jobdict = {}
        specdict = {}
        for spec in specs:
            jobid = str(spec['jobid'])
            #new_job = Job(spec)
            #jobdict[jobid] = new_job
            specdict[jobid] = spec
        return specdict
    
    def get_walltime_Ap(self, spec):  #*AdjEst*
        '''get walltime adjusting parameter from history manager component'''
        
        projectname = spec.get('project')
        username = spec.get('user')
        if prediction_scheme == "paired":
            return self.history_manager.get_Ap_by_keypair(username, projectname)
        
        Ap_proj = self.history_manager.get_Ap('project', projectname)
        
        Ap_user = self.history_manager.get_Ap('user', username)
         
        if prediction_scheme == "project":
            return Ap_proj
        elif prediction_scheme == "user":
            print "Ap_user==========", Ap_user
            return Ap_user
        elif prediction_scheme == "combined":
            return (Ap_proj + Ap_user) / 2
        else:
            return self.history_manager.get_Ap_by_keypair(username, projectname)
            
    def log_job_event(self, eventtype, timestamp, spec):
        '''log job events(Queue,Start,End) to PBS-style log'''
        def len2 (_input):
            _input = str(_input)
            if len(_input) == 1:
                return "0" + _input
            else:
                return _input
        if eventtype == 'Q':  #submitted(queued) for the first time
            message = "%s;Q;%s;queue=%s" % (timestamp, spec['jobid'], spec['queue'])
        elif eventtype == 'R':  #resume running after failure recovery
            message = "%s;R;%s" % (timestamp, ":".join(spec['location']))
        else:
            wall_time = spec['walltime']
            walltime_minutes = len2(int(float(wall_time)) % 60)
            walltime_hours = len2(int(float(wall_time)) // 60)
            log_walltime = "%s:%s:00" % (walltime_hours, walltime_minutes)
            if eventtype == 'S':  #start running 
                message = "%s;S;%s;queue=%s qtime=%s Resource_List.nodect=%s Resource_List.walltime=%s start=%s exec_host=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, spec['start_time'], ":".join(spec['location']))
            elif eventtype == 'H':  #hold some resource  
                message = "%s;H;%s;queue=%s qtime=%s Resource_List.nodect=%s Resource_List.walltime=%s exec_host=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, ":".join(spec['location']))
            elif eventtype == 'E':  #end
                if spec['hold_time'] == 0:
                    holding_time = 0
                else:
                    holding_time = spec['start_time'] - spec['hold_time']
                first_yielding = self.yielding_job_dict.get(int(spec['jobid']), 0)
                if first_yielding > 0:
                    yielding_time = spec['start_time'] - first_yielding
                else:
                    yielding_time = 0
                message = "%s;E;%s;queue=%s qtime=%s Resource_List.nodect=%s Resource_List.walltime=%s start=%s end=%f exec_host=%s runtime=%s hold=%s yield=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], spec['nodes'], log_walltime, spec['start_time'], 
                 round(float(spec['end_time']), 1), ":".join(spec['location']),
                 spec['runtime'], holding_time, yielding_time)
            else:
                print "---invalid event type, type=", eventtype
                return
        self.pbslog.LogMessage(message)
        
    def get_live_job_by_id(self, jobid):
        '''get waiting or running job instance by jobid'''
        job = None
        joblist = self.queues.get_jobs([{'jobid':int(jobid)}])
        if joblist:
            job = joblist[0]
        return job
        
    def get_jobs(self, specs):
        '''get a list of jobs, each time triggers time stamp increment and job
        states update'''

        jobs = []
        
        if self.event_manager.get_go_next():
            del self.yielding_job_list[:]
            
            self.update_job_states(specs, {})
            
            self.compute_utility_scores()

        self.event_manager.set_go_next(True)
        
        jobs = self.queues.get_jobs([{'tag':"job"}])
        
#        print "ret_job1=", [job.jobid for job in jobs if job.is_runnable == True]
        
        #exclude jobs that give up turns (for waiting their mate jobs)
        if self.yielding_job_list:
            jobs = [job for job in jobs if job.jobid not in self.yielding_job_list]

        return jobs
    get_jobs = exposed(query(get_jobs))
    
    def update_job_states(self, specs, updates):
        '''update the state of the jobs associated to the current time stamp'''
        
        jobid = self.event_manager.get_current_event_job()
        
        ids_str = str(self.event_manager.get_current_event_job())
        
        ids = ids_str.split(':')
        cur_event = self.event_manager.get_current_event_type()
        #print "current event=", cur_event, " ", ids
        for Id in ids:
            
            if cur_event == "Q":  # Job (Id) is submitted
                tempspec = self.unsubmitted_job_spec_dict[Id]
                
                tempspec['state'] = "queued"   #invisible -> queued
                tempspec['is_runnable'] = True   #False -> True
                
                self.queues.add_jobs([tempspec])
                self.num_waiting += 1
                
                self.log_job_event("Q", self.get_current_time_date(), tempspec)
                
                del self.unsubmitted_job_spec_dict[Id]

            elif cur_event=="E":  # Job (Id) is completed
                
                joblist = self.queues.get_jobs([{'jobid':int(Id)}])
                
                if joblist:
                    completed_job = joblist[0]
                else:
                    return 0
                #log the job end event
                jobspec = completed_job.to_rx()
                #print "end jobspec=", jobspec
                if jobspec['end_time']:
                    end = float(jobspec['end_time'])
                else:
                    end = 0
                end_datetime = sec_to_date(end)   
                self.log_job_event("E", end_datetime, jobspec)
                #free nodes
                self.nodes_up(completed_job.location)
                self.num_busy -= len(completed_job.location)
                
                #delete the job instance from self.queues
                self.queues.del_jobs([{'jobid':int(Id)}])
                self.num_running -= 1
                self.num_end += 1
                
#        if not self.bgjob:
#            os.system('clear')
#            self.print_screen(cur_event)

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

        #print self.get_current_time_date(), "run job state change, job", jobspec['jobid'], \
        #     ":", jobspec['state'], "->", updates['state']
             
        #determine whether the job is going to fail before completion
        location = newattr['location']
        duration = jobspec['remain_time']
        
        end = start + duration
        updates['end_time'] = end
        self.insert_time_stamp(end, "E", {'jobid':jobspec['jobid']})
        
        updates.update(newattr)
    
        return updates
     
    def add_jobs(self, specs):
        '''Add a job'''
        response = self.queues.add_jobs(specs)
        return response
    add_jobs = exposed(query(add_jobs))
        
    def current_idle_node(self):
        '''number of idle nodes'''
        idle_nodes = 0
        midplanes = self.get_all_idle_midplanes()
        idle_nodes = 512 * len(midplanes)
        return idle_nodes
    
    def current_cycle_capacity_loss(self):
        loss  = 0
        current_time = self.get_current_time_sec()
        next_time = self.get_next_time_sec()
        print "current_time=", current_time
        print "next_time=", next_time
        time_length = next_time - current_time
        idle_node = self.current_idle_node()
        loss = time_length * idle_node
        return loss
    
    def total_capacity_loss_rate(self):
        last_stamp = len(self.time_stamps) - 1
        total_period_sec = self.time_stamps[last_stamp] [2] - self.time_stamps[1][2]
        total_NH = TOTAL_NODES *  (total_period_sec / 3600)
            
        print "total_nodehours=", total_NH
        print "total loss capcity (node*hour)=", self.capacity_loss / 3600
        
        loss_rate = self.capacity_loss /  (total_NH * 3600)
        
        print "capacity loss rate=", loss_rate
        return loss_rate        
    
    def _get_job_by_id(self, jobid):
        jobs = self.queues.get_jobs([{'jobid':jobid}])
        if len(jobs) == 1:
            return jobs[0]
        else:
            return None
   
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
        end_time, invoked by bgsched'''
        #print "run job ", specs, " on nodes", nodelist
        if specs == None:
            return 0
        
        for spec in specs:
            
            action = "start"
            
            dbgmsg = ""
            
            if self.coscheduling:
                local_job_id = spec.get('jobid') #int
                #check whether there is a mate job
                
                mate_job_id = self.mate_job_dict.get(local_job_id, 0)

                #if mate job exists, get the status of the mate job
                if mate_job_id > 0:
                    remote_status = self.get_mate_jobs_status_local(mate_job_id).get('status', "unknown")
                    dbgmsg += "local=%s;mate=%s;mate_status=%s" % (local_job_id, mate_job_id, remote_status)
                    
                    if remote_status in ["queuing", "unsubmitted"]:
                        if self.cosched_scheme == "hold": # hold resource if mate cannot run, favoring job
                            action = "hold"
                        if self.cosched_scheme == "yield": # give up if mate cannot run, favoring sys utilization
                            action = "start_both_or_give_up"                        
                    if remote_status == "holding":
                        action = "start_both"
                    
                    #self.dbglog.LogMessage(dbgmsg)
                #to be inserted co-scheduling handling code
                else:
                    pass
            
            if action == "start":
                #print "CQSIM-normal: start job %s on nodes %s" % (spec['jobid'], nodelist)
                self.start_job([spec], {'location': nodelist})
            elif action == "hold":
                #print "try to hold job %s on location %s" % (local_job_id, nodelist)
                mate_job_can_run = False
                if self.cosched_scheme_remote == "yield":
                    #if remote scheme is 'yield', try to invoke a scheduling iteration to see if remote yielded job can run now
                    try:
                        mate_job_can_run = ComponentProxy(REMOTE_QUEUE_MANAGER).try_to_run_mate_job(mate_job_id)
                    except:
                        self.logger.error("failed to connect to remote queue-manager component!")
                else:
                    #if remote scheme is 'hold', the remote mate definitely can not run at this point because its status is not "holding"
                    pass
                
                if mate_job_can_run:
                    #now that mate has been started, start local job
                    self.start_job([spec], {'location': nodelist})
                    dbgmsg += " ###start both"
                else:
                    self.hold_job([spec], {'location': nodelist})
            elif action == "start_both":
                #print "start both mated jobs %s and %s" % (local_job_id, mate_job_id)
                self.start_job([spec], {'location': nodelist})
                ComponentProxy(REMOTE_QUEUE_MANAGER).run_holded_job([{'jobid':mate_job_id}])
            elif action == "start_both_or_give_up":
                mate_job_can_run = False
                               
                if self.cosched_scheme_remote == "yield":
                    #if remote scheme is 'yield', try to invoke a scheduling iteration to see if remote yielded job can run now
                    try:
                        mate_job_can_run = ComponentProxy(REMOTE_QUEUE_MANAGER).try_to_run_mate_job(mate_job_id)
                    except:
                        self.logger.error("failed to connect to remote queue-manager component!")
                else:
                    #if remote scheme is 'hold', the remote mate definitely can not run at this point because its status is not "holding"
                    pass
                        
                if mate_job_can_run:
                    #now that mate has been started, start local job
                    self.start_job([spec], {'location': nodelist})
                    dbgmsg += " ###start both"
                else:
                    #mate job cannot run, give up the turn. mark the job as yielding.
                    job_id = spec.get('jobid')
                    self.yielding_job_list.append(job_id)  #int
                    #record the first time this job yields
                    if not self.yielding_job_dict.has_key(job_id):
                        self.yielding_job_dict[job_id] = self.get_current_time_sec()
                        self.dbglog.LogMessage("%s: job %s first yield" % (self.get_current_time_date(), job_id))
                                    
        #set tag false, enable scheduling another job at the same time
        self.event_manager.set_go_next(False)
        #self.print_screen()
                
        return len(specs)
    run_jobs = exposed(run_jobs)
    
        # order the jobs with biggest utility first
    def utilitycmp(self, job1, job2):
        return -cmp(job1.score, job2.score)
    
    def try_to_run_mate_job(self, _jobid):
        '''try to run mate job, start all the jobs that can run. If the started
        jobs include the given mate job, return True else return False.
        '''
        mate_job_started = False
        
        #start all the jobs that can run
        while True:
            running_jobs = [job for job in self.queues.get_jobs([{'has_resources':True}])]
            
            end_times = []
            
            now = self.get_current_time_sec()
        
            for job in running_jobs:
                end_time = max(float(job.starttime) + 60 * float(job.walltime), now + 5*60)
                end_times.append([job.location, end_time])
  
            
            active_jobs = [job for job in self.queues.get_jobs([{'is_runnable':True}])] #waiting jobs
            active_jobs.sort(self.utilitycmp)
                   
            job_location_args = []
            for job in active_jobs:
                if not job.jobid == _jobid and self.mate_job_dict.get(job.jobid, 0) > 0:
                    #if a job other than given job (_jobid) has mate, skip it.
                    continue
                
                job_location_args.append({'jobid': str(job.jobid),
                                          'nodes': job.nodes,
                                          'queue': job.queue,
                                          'forbidden': [],
                                          'utility_score': job.score,
                                          'walltime': job.walltime,
                                          'walltime_p': job.walltime_p,  #*AdjEst*
                                          'attrs': job.attrs,
                 } )
            
            
            if len(job_location_args) == 0:
                break
            
            #print "cqsim queue order=", [item['jobid'] for item in job_location_args]
            
            best_partition_dict = self.find_job_location(job_location_args, end_times)
            
            if best_partition_dict:
                #print "best_partition_dict=", best_partition_dict
                
                for canrun_jobid in best_partition_dict:
                    nodelist = best_partition_dict[canrun_jobid]
                    
                    if str(_jobid) == canrun_jobid:
                        mate_job_started = True
                       
                    self.start_job([{'tag':"job", 'jobid':int(canrun_jobid)}], {'location':nodelist})
                    #print "bqsim.try_to_run_mate, start job jobid ", canrun_jobid 
                     
                    #insert a new end time
                    started_job = self.get_live_job_by_id(canrun_jobid)
                    new_end_time = max(now + 60 * float(started_job.walltime), now + 5*60)                    
                    end_times.append([started_job.location, new_end_time])
            else:
                break
                                  
        return mate_job_started
    try_to_run_mate_job = exposed(try_to_run_mate_job)
    
    def run_holded_job(self, specs):
        '''start holded job'''
        for spec in specs:
            jobid = spec.get('jobid')
            nodelist = self.job_hold_dict.get(jobid, None)
            if nodelist == None:
                #print "cannot find holded resources"
                return
            #print "start holded job %s on location %s" % (spec['jobid'], nodelist)
            self.start_job([spec], {'location':nodelist})
            del self.job_hold_dict[jobid]
            
    run_holded_job = exposed(run_holded_job)
    
    def start_job(self, specs, updates):
        '''update the job state and start_time and end_time when cqadm --run
        is issued to a group of jobs'''
        
        nodelist = updates['location']
              
        self.nodes_down(nodelist)
        
        self.num_busy += len(nodelist)
            
        self.num_running += 1
        self.num_waiting -= 1
                    
        def _start_job(job, newattr):
            '''callback function to update job start/end time'''
            temp = job.to_rx()
            newattr = self.run_job_updates(temp, newattr)
            temp.update(newattr)
            job.update(newattr)
            self.log_job_event('S', self.get_current_time_date(), temp)
        
        return self.queues.get_jobs(specs, _start_job, updates)

    def hold_job(self, specs, updates):
        '''hold a job. a holded job is not started but hold some resources that can run itself in the future
        once its mate job in a remote system can be started immediatly'''
        
        nodelist = updates['location']
        
        self.nodes_down(nodelist)
        
        for spec in specs:
            self.job_hold_dict[spec['jobid']] = nodelist 
        
        def _hold_job(job, newattr):
            '''callback function to update job start/end time'''
            temp = job.to_rx()
            newattr = self.hold_job_updates(temp, newattr)
            temp.update(newattr)
            job.update(newattr)
            self.log_job_event('H', self.get_current_time_date(), temp)
        
        return self.queues.get_jobs(specs, _hold_job, updates)
    
    def hold_job_updates(self, jobspec, newattr):
        ''' return the state updates (including state queued -> running, 
        setting the start_time, end_time)'''
        updates = {}
        
        updates['is_runnable'] = False
        updates['has_resources'] = False
        updates['state'] = "holding"
        updates['hold_time'] = self.get_current_time_sec()

        updates.update(newattr)
    
        return updates
    
    def compute_utility_scores (self):
        utility_scores = []
        current_time = time.time()
            
        for job in self.queues.get_jobs([{'is_runnable':True}]):    
            utility_name = self.queues[job.queue].policy
            args = {'queued_time':current_time - float(job.submittime), 
                    'wall_time': 60*float(job.walltime_p),    #  *AdjEst*
                    'size': float(job.nodes),
                    'user_name': job.user,
                    'project': job.project,
                    'queue_priority': int(self.queues[job.queue].priority),
                    #'machine_size': max_nodes,
                    'jobid': int(job.jobid),
                    'score': job.score,
                    'recovering': job.recovering,
                    'state': job.state,
                    }
            try:
                if utility_name in self.builtin_utility_functions:
                    utility_func = self.builtin_utility_functions[utility_name]
                else:
                    utility_func = self.user_utility_functions[utility_name]
                utility_func.func_globals.update(args)
                score = utility_func()
            except KeyError:
                # do something sensible when the requested utility function doesn't exist
                # probably go back to the "default" one
                
                # and if we get here, try to fix it and throw away this scheduling iteration
                self.logger.error("cannot find utility function '%s' named by queue '%s'" % (utility_name, job.queue))
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
            except:
                # do something sensible when the requested utility function explodes
                # probably go back to the "default" one
                # and if we get here, try to fix it and throw away this scheduling iteration
                self.logger.error("error while executing utility function '%s' named by queue '%s'" % (utility_name, job.queue), \
                    exc_info=True)
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
            
            try:
                job.score += score
            except:
                self.logger.error("utility function '%s' named by queue '%s' returned a non-number" % (utility_name, job.queue), \
                    exc_info=True)
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
    
    def define_user_utility_functions(self):
        self.logger.info("building user utility functions")
        self.user_utility_functions.clear()
        filename = os.path.expandvars(get_bgsched_config("utility_file", ""))
        try:
            f = open(filename)
        except:
            #self.logger.error("Can't read utility function definitions from file %s" % get_bgsched_config("utility_file", ""))
            return
        
        str = f.read()
        
        try:
            code = compile(str, filename, 'exec')
        except:
            self.logger.error("Problem compiling utility function definitions.", exc_info=True)
            return
        
        globals = {'math':math, 'time':time}
        locals = {}
        try:
            exec code in globals, locals
        except:
            self.logger.error("Problem executing utility function definitions.", exc_info=True)
            
        for thing in locals.values():
            if type(thing) is types.FunctionType:
                if thing.func_name in self.builtin_utility_functions:
                    self.logger.error("Attempting to overwrite builtin utility function '%s'.  User version discarded." % \
                        thing.func_name)
                else:
                    self.user_utility_functions[thing.func_name] = thing
    define_user_utility_functions = exposed(define_user_utility_functions)
    
    def define_builtin_utility_functions(self):
        self.logger.info("building builtin utility functions")
        self.builtin_utility_functions.clear()
        
        # I think this duplicates cobalt's old scheduling policy
        # higher queue priorities win, with jobid being the tie breaker
        def default0():
            val = queue_priority + 0.1
            return val
        
        def default1():
            '''FCFS'''
            val = queued_time
            return val
        
        def default():
            '''WFP, supporting coordinated job recovery'''
                        
            wall_time_sec = wall_time*60
                            
            val = ( queued_time / wall_time_sec)**3 * (size/64.0)
            
            return val
    
        def high_prio():
            val = 1.0
            return val
    
        self.builtin_utility_functions["default"] = default
        self.builtin_utility_functions["high_prio"] = high_prio
        
    def find_job_location(self, arg_list, end_times):
        best_location_dict = {}
        winner = arg_list[0]
               # first time through, try for starting jobs based on utility scores
        for args in arg_list:
            location_data = self._find_job_location(args)
            if location_data:
                best_location_dict.update(location_data)
                break
            
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_location_dict:
            job_end_times = {}
            total = 0
            for item in sorted(end_times, cmp=self._backfill_cmp):
                total += len(item[0])
                job_end_times[total] = item[1]
    
            needed = int(winner['nodes']) - len(self._get_available_nodes(winner))
            now = self.get_current_time() ##different from super function
            backfill_cutoff = 0
            for num in sorted(job_end_times):
                if needed <= num:
                    backfill_cutoff = job_end_times[num] - now

            for args in arg_list:
                if 60*float(args['walltime']) > backfill_cutoff:
                    continue
                
                location_data = self._find_job_location(args)
                if location_data:
                    best_location_dict.update(location_data)
                    self.logger.info("backfilling job %s" % args['jobid'])
                    break

#!!!following two lines must be commented for coscheduling feature because giving up may occur. when
# a job is found location but give up to run, the nodes can't be updated to running status.
        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
#        for location_list in best_location_dict.itervalues():
#            self.running_nodes.update(location_list)

        return best_location_dict
    find_job_location = exposed(find_job_location)

    #display stuff
    
    
    def print_screen(self, cur_event=""):
        '''print screen, show number of waiting jobs, running jobs, busy_nodes%'''
        
        print "Cluster" 
        
        current_datetime = self.event_manager.get_current_date_time()
        print "%s %s" % (current_datetime, cur_event)
        
        print "number of waiting jobs: ", self.num_waiting
        
        waiting_job_bar = REDS
        for i in range(self.num_waiting):
            waiting_job_bar += "*"
        waiting_job_bar += ENDC
            
        print waiting_job_bar
        
        print "number of running jobs: ", self.num_running
        
        running_job_bar = BLUES
        for i in range(self.num_running):
            running_job_bar += "+"
        running_job_bar += ENDC
        print running_job_bar
        
        print "number of busy nodes: ", self.num_busy
        print "system utilization: ", float(self.num_busy) / self.total_nodes
        busy_node_bar = GREENS
        
        i = 0
        while i < self.num_busy:
            busy_node_bar += "x"
            i += 1
        for j in range(i, self.total_nodes):
            busy_node_bar += "-"
        busy_node_bar += ENDC
        busy_node_bar += REDS
        busy_node_bar += "|"
        busy_node_bar += ENDC
        print busy_node_bar
        print "completed jobs/total jobs:  %s/%s" % (self.num_end, self.total_job)
        
        progress = 100 * self.num_end / self.total_job
        
        progress_bar = ""
        i = 0
        while i < progress:
            progress_bar += "="
            i += 1
        for j in range(i, 100):
            progress_bar += "-"
        progress_bar += "|"
        print progress_bar
        if self.sleep_interval:
            time.sleep(self.sleep_interval)

    #coscheduling stuff
    def get_mate_job_status_cqsim(self, jobid):
        '''return mate job status, remote function, invoked by remote component'''
        ret_dict = {'jobid':jobid}
        
        ret_dict['status'] = self.get_coschedule_status(jobid)

        return ret_dict
    get_mate_job_status_cqsim = exposed(get_mate_job_status_cqsim)
    
    def get_mate_jobs_status_local(self, remote_jobid):
        '''return mate job status, invoked by local functions'''
        status_dict = {}
        try:
            status_dict = ComponentProxy(REMOTE_QUEUE_MANAGER).get_mate_job_status_bqsim(remote_jobid)
        except:
            self.logger.error("failed to connect to remote queue-manager component!")
            status_dict = {'status':'notconnected'}
        return status_dict
    
    def test_can_run(self, jobid):
        '''test whether a job can start immediately, specifically in following cases:
          1. highest utility score and resource is available
          2. not with top priority but can start in non-drained partition when top-priority job is draining
          3. can be backfilled
        '''
        return False
    
    def get_coschedule_status(self, jobid):
        '''return job status regarding coscheduling, 
           input: jobid
           output: listed as follows:
            1. "queuing"
            2. "holding"
            3. "unsubmitted"
            4. "running"
            5. "ended"
        '''
        ret_status = "unknown"
        job = self.get_live_job_by_id(jobid)
        if job:  #queuing or running
            has_resources = job.has_resources
            is_runnable = job.is_runnable
            if is_runnable and not has_resources:
                ret_status = "queuing"
            if not is_runnable and has_resources:
                ret_status = "running"
            if not is_runnable and not has_resources:
                ret_status = "holding"
        else:  #unsubmitted or ended
            if self.unsubmitted_job_spec_dict.has_key(str(jobid)):
                ret_status = "unsubmitted"
            else:
                ret_status = "unknown"  #ended or no such job
                del self.mate_job_dict[jobid]
        return ret_status
    
    def print_post_screen(self):
        '''post screen after simulation completes'''
        print self.yielding_job_dict
    print_post_screen = exposed(print_post_screen)
