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
from Cobalt.Components.simulator import Simulator
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

REMOTE_QUEUE_MANAGER = "cluster-queue-manager"

WALLTIME_AWARE_CONS = False

MACHINE_ID = 0
MACHINE_NAME = "Intrepid"
MAXINT = 2021072587
MIDPLANE_SIZE = 512
DEFAULT_VICINITY = 60
DEFAULT_COSCHEDULE_SCHEME = 0

logging.basicConfig()
logger = logging.getLogger('Qsim')
TOTAL_NODES = 40960

OPT_RULE = "A1"  # A0, A1, A2, A3, A4, NORMAL, EVEN
RECOVERYOPT = 2 # by default, the failed job is sent back to the rear of the queue
CHECKPOINT = False  #not used in this version
MTTR = 3600   #time to repair partition(in sec), a failed partition will be available again in MTTR seconds,
SET_event = set(['I', 'Q', 'S', 'E', 'F', 'R'])

PRINT_SCREEN = True

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
    
    print line
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


def tune_workload(specs, frac=1, anchor=0):
    '''tune workload heavier or lighter, and adjust the start time to anchor'''
  
    def _subtimecmp(spec1, spec2):
        return cmp(spec1.get('submittime'), spec2.get('submittime'))
    specs.sort(_subtimecmp)
        
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

def qsim_quit():
    print "pid=", os.getpid()
    os.kill(os.getpid(), signal.SIGINT)
    
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
                            "nodes","runtime", "start_time", "end_time",
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
        self.state = spec.get("state", "invisible")
        self.system_state = ''
        self.starttime = 0
        #self.arrival_time = 0
        #self.failure_time = 0
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
            
    
class BGQsim(Simulator):
    '''Cobalt Queue Simulator for cluster systems'''
    
    implementation = "bqsim"
    name = "queue-manager"
    alias = "system"
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        
        Simulator.__init__(self, *args, **kwargs)
         
        #initialize partitions
        self.sleep_interval = kwargs.get("sleep_interval", 0)
        
        self.fraction = kwargs.get("BG_Fraction", 1)
        self.sim_start = kwargs.get("bg_trace_start", 0)
        self.sim_end = kwargs.get("bg_trace_end", sys.maxint)
        self.anchor = kwargs.get("Anchor", 0)
        
        #self.coscheduling = kwargs.get("coscheduling", False)
        self.mate_vicinity = kwargs.get("vicinity", DEFAULT_VICINITY)
        self.cosched_scheme = kwargs.get("coscheduling", None)
        if self.cosched_scheme in ["hold", "yield"]:
            self.coscheduling = True
        else:
            self.coscheduling = False
        
        self.mate_qtime_pairs = []
        
        #key=local job id, value=remote mated job id
        self.mate_job_dict = {}
        #key = jobid, value = nodelist  ['part-or-node-name','part-or-node-name' ]
        self.job_hold_dict = {}  
        
        self.givingup_job_list = []
        
        self.cluster_job_trace =  kwargs.get("cjob", None)        
        
        if self.coscheduling:
            #test whether cqsim is up by checking cluster job trace argument (cjob) 
            
            if self.cluster_job_trace:
                self.mate_qtime_pairs = self.init_mate_qtime_pair(self.cluster_job_trace)
            else:
                self.coscheduling = False
                self.mate_queue_manager = None
        
        partnames = self._partitions.keys()
        self.init_partition(partnames)
        self.inhibit_small_partitions()
        self.part_size_list = []
     
        for part in self.partitions.itervalues():
            if int(part.size) not in self.part_size_list:
                if part.size >= MIDPLANE_SIZE:
                    self.part_size_list.append(int(part.size))
        self.part_size_list.sort()
        #print self.part_size_list
        
        self.workload_file =  kwargs.get("bgjob")
        self.output_log = kwargs.get("outputlog")
        
        self.event_manager = ComponentProxy("event-manager")
        
        self.predict_scheme = kwargs.get("predict", False)
        
        if self.predict_scheme:
            self.walltime_prediction = True
            self.predict_queue = bool(int(self.predict_scheme[0]))
            self.predict_backfill = bool(int(self.predict_scheme[1]))
            self.predict_running = bool(int(self.predict_scheme[2]))
        else:
            self.walltime_prediction = False
            self.predict_queue = False
            self.predict_backfill = False
            self.predict_running = False
            
        #print "walltime_prediction =", self.walltime_prediction   
        histm_alive = False
        try:
            histm_alive = ComponentProxy("history-manager").is_alive()
        except:
            #self.logger.error("failed to connect to histm component", exc_info=True)
            histm_alive = False
        
        if histm_alive:
            self.history_manager = ComponentProxy("history-manager")
        else:
            self.walltime_prediction = False
            
        self.time_stamps = [('I', '0', 0, {})]
        self.cur_time_index = 0
        self.queues = SimQueueDict(policy=None)
        
#        self.invisible_job_dict = {}   # for jobs not submitted, {jobid:job_instance}
        self.unsubmitted_job_spec_dict = {}   #{jobid: jobspec}

        self.num_running = 0
        self.num_waiting = 0
        self.num_busy = 0
        self.num_end = 0
        self.total_job = 0
        
        self.init_queues()
        
        if self.coscheduling:
            self.init_mate_job_dict()
        
        for k, v in self.mate_job_dict.iteritems():
            print "%s:%s" % (k, v)

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
        local_components["system"] = self
        
        #initialize capacity loss
        self.capacity_loss = 0
                
        #starting job(id)s at current time stamp. used for calculating capacity loss
        self.starting_jobs = []
        
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}
                        
        self.define_builtin_utility_functions()
        self.define_user_utility_functions()
    
        self.rack_matrix = []
        self.reset_rack_matrix()
        
        #configure walltime-aware spatial scheduling schemes
        self.walltime_aware_cons = False
        self.walltime_aware_aggr = False
        self.wass_scheme = kwargs.get("wass", None) 
        
        if self.wass_scheme == "both":
            self.walltime_aware_cons = True
            self.walltime_aware_aggr = True
        elif self.wass_scheme == "cons":
            self.walltime_aware_cons = True
        elif self.wass_scheme == "aggr":
            self.walltime_aware_aggr = True
            
        if self.wass_scheme:
            print "walltime aware job allocation enabled, scheme = ", self.wass_scheme
        
        if self.walltime_prediction:
            print "walltime prediction enabled, scheme = ", self.predict_scheme
            
        if self.coscheduling:
            print "co-scheduling enabled, scheme = ", self.cosched_scheme
            
        if self.fraction != 1:
            print "job arrival intervals adjusted, fraction = ", self.fraction
        
        if not self.cluster_job_trace:
            Var = raw_input("press any Enter to continue...")
                
        print "Simulation starts:"
    
    def _get_queuing_jobs(self):
        return [job for job in self.queues.get_jobs([{'is_runnable':True}])]
    queuing_jobs = property(_get_queuing_jobs)
    
    def _get_running_jobs(self):
        return [job for job in self.queues.get_jobs([{'has_resources':True}])]
    running_jobs = property(_get_running_jobs)
        
    def init_mate_qtime_pair(self, mate_job_trace):
        '''initialize mate job dict'''
        jobfile = open(mate_job_trace, 'r')
        
        qtime_pairs = []
        
        for line in jobfile:
            line = line.strip('\n')
            line = line.strip('\r')
            if line[0].isdigit():
                #pbs-style trace
                firstparse = line.split(';')
                if firstparse[1] == 'Q':
                    qtime = date_to_sec(firstparse[0])
                    jobid = int(firstparse[2])
                    qtime_pairs.append((qtime, jobid))
            else:
                #alternative trace
                first_parse = line.split(';')
                tempdict = {}
                for item in first_parse:
                    tup = item.partition('=')
                    if tup[0] == 'qtime':
                        qtime = date_to_sec(tup[2], "%Y-%m-%d %H:%M:%S")
                    if tup[0] == 'jobid':
                        jobid = tup[2]
                if jobid and qtime:
                        qtime_pairs.append((qtime, jobid))
                    
        return qtime_pairs
    
    def find_mate_id(self, qtime, threshold):
    
        mate_subtime = 0
        ret_id = 0
        for pair in self.mate_qtime_pairs:
            if pair[0] > qtime:
                mate_subtime = pair[0]
                mate_id = pair[1]
                break

        if mate_subtime > 0:
            if mate_subtime - float(qtime) < threshold:
               ret_id = mate_id
        return ret_id
    
    def init_mate_job_dict(self):
        '''init mate job dictionary'''
        
        temp_dict = {} #remote_id:local_id
        
        for id, spec in self.unsubmitted_job_spec_dict.iteritems():
            id = int(id)
            submit_time = spec.get('submittime')
            mate_id = self.find_mate_id(submit_time, self.mate_vicinity)
            if mate_id > 0:
                #self.mate_job_dict[spec['jobid']] = int(mateid)
                if temp_dict.has_key(mate_id):
                    tmp = temp_dict[mate_id]
                    if id > tmp:
                        temp_dict[mate_id] = id
                else:
                    temp_dict[mate_id] = id
        #reserve dict to local_id:remote_id to guarantee one-to-one match
        self.mate_job_dict = dict((v, k) for k, v in temp_dict.iteritems())
        
    def is_finished(self):
        return self.finished
    is_finished = exposed(is_finished)
    
    def get_current_time(self):
        '''this function overrides get_current_time() in bgsched, bg_base_system, and cluster_base_system'''
        return  self.event_manager.get_current_time()
    
    def get_current_time_sec(self):
        return  self.event_manager.get_current_time()
    
    def get_current_time_date(self):
        return self.event_manager.get_current_date_time()
    
    def get_mate_job_dict(self):
        return self.mate_job_dict
    get_mate_job_dict = exposed(get_mate_job_dict)

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
    
    def inhibit_small_partitions(self):
        '''set all partition less than 512 nodes not schedulable and functional'''
        namelist = []
        for partition in self._partitions.itervalues():
            if partition.size < MIDPLANE_SIZE:
                namelist.append(partition.name)
        func = self.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in namelist],
                {'scheduled':False})
        apply(func, args)

    def init_queues(self):
        '''parses the work load log file, initializes queues and sorted time 
        stamp list'''
        
        print "Initializing jobs, one moment please..."
        
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
                if act_run_time <= 0:
                    continue
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
                message = "%s;E;%s;queue=%s qtime=%s Resource_List.nodect=%s Resource_List.walltime=%s start=%s end=%f exec_host=%s runtime=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], spec['nodes'], log_walltime, spec['start_time'], 
                 round(float(spec['end_time']), 1), ":".join(spec['location']),
                 spec['runtime'])
            else:
                print "invalid event type, type=", eventtype
                return
        self.pbslog.LogMessage(message)
        
    def get_live_job_by_id(self, jobid):
        '''get waiting or running job instance by jobid'''
        job = None
        joblist = self.queues.get_jobs([{'jobid':int(jobid)}])
        if joblist:
            job = joblist[0]
        return job
    
    def update_job_states(self, specs, updates):
        '''update the state of the jobs associated to the current time stamp'''
        
        jobid = self.event_manager.get_current_event_job()
        
        ids_str = str(self.event_manager.get_current_event_job())
        
        ids = ids_str.split(':')
        cur_event = self.event_manager.get_current_event_type()
        #print "current event=", cur_event, " ", ids
        for Id in ids:
            
            if cur_event == "Q":  # Job (Id) is submitted
                tempspec = self.unsubmitted_job_spec_dict.get(Id, None)
                
                if tempspec == None:
                    continue
                
                tempspec['state'] = "queued"   #invisible -> queued
                tempspec['is_runnable'] = True   #False -> True
                
#                self.unsubmitted_job_spec_dict[Id]['state'] = "queued"
#                self.unsubmitted_job_spec_dict[Id]['is_runnable'] = "True"
                
                self.queues.add_jobs([tempspec])
                self.num_waiting += 1
                
                self.log_job_event("Q", self.get_current_time_date(), tempspec)
                
                #del self.unsubmitted_job_spec_dict[Id]

            elif cur_event=="E":  # Job (Id) is completed
                completed_job = self.get_live_job_by_id(Id)
                
                if completed_job == None:
                    continue
                
                #release partition
                for partition in completed_job.location:
                    self.release_partition(partition)
                
                partsize = int(self._partitions[partition].size)
                self.num_busy -= partsize
                                
                #log the job end event
                jobspec = completed_job.to_rx()
                #print "end jobspec=", jobspec
                if jobspec['end_time']:
                    end = float(jobspec['end_time'])
                else:
                    end = 0
                end_datetime = sec_to_date(end)   
                self.log_job_event("E", end_datetime, jobspec)
                
#                self.unsubmitted_job_spec_dict[Id]['state'] = "ended"
#                self.unsubmitted_job_spec_dict[Id]['is_runnable'] = "False"
#                self.unsubmitted_job_spec_dict[Id]['has_resource'] = "False"
                
                #delete the job instance from self.queues
                self.queues.del_jobs([{'jobid':int(Id)}])
                self.num_running -= 1
                self.num_end += 1
        
        if not self.cluster_job_trace:
            os.system('clear')
            self.print_screen(cur_event)
                
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
    
    def get_jobs(self, specs):
        '''get a list of jobs, each time triggers time stamp increment and job
        states update'''

        jobs = []
        
        if self.event_manager.get_go_next():
            del self.givingup_job_list[:]
            
            self.update_job_states(specs, {})
            
            self.compute_utility_scores()

        self.event_manager.set_go_next(True)
        
        jobs = self.queues.get_jobs([{'tag':"job"}])
        
        if self.givingup_job_list:
            jobs = [job for job in jobs if job.jobid not in self.givingup_job_list]
  
        return jobs
    get_jobs = exposed(query(get_jobs))
    
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
    
    def equal_partition(self, nodeno1, nodeno2):
        proper_partsize1 = 0
        proper_partsize2 = 1        
        for psize in self.part_size_list:
            if psize >= nodeno1:
                proper_partsize1 = psize
                break
        for psize in self.part_size_list:
            if psize >= nodeno2:
                proper_partsize2 = psize
                break
        if proper_partsize1 == proper_partsize2:
            return True
        else:
            return False
    
    def run_matched_job(self, jobid, partition):
        '''implementation of aggresive scheme in sc10 submission'''
  
        #get neighbor partition (list) for running
        partlist = []
        nbpart = self.get_neighbor_by_partition(partition)
        if nbpart:
            nb_partition = self._partitions[nbpart]
            if nb_partition.state != "idle":
                #self.dbglog.LogMessage("return point 1")
                return None
        else:
            #self.dbglog.LogMessage("return point 2")
            return None
        partlist.append(nbpart)
                
        #find a job in the queue whose length matches the top-queue job
        topjob = self._get_job_by_id(jobid)
        
        base_length = float(topjob.walltime)
        #print "job %d base_length=%s" % (jobid, base_length)
        base_nodes = int(topjob.nodes)
        
        min_diff = MAXINT
        matched_job = None
        msg = "queueing jobs=%s" % ([job.jobid for job in self.queuing_jobs])
        #self.dbglog.LogMessage(msg)
        
        for job in self.queuing_jobs:
            #self.dbglog.LogMessage("job.nodes=%s, base_nodes=%s" % (job.nodes, base_nodes))
            
            if self.equal_partition(int(job.nodes), base_nodes):
                length = float(job.walltime)
                #self.dbglog.LogMessage("length=%s, base_length=%s" % (length, base_length))
                if length > base_length:
                    continue
                diff = abs(base_length - length)
                #print "diff=", diff
                #self.dbglog.LogMessage("diff=%s" % (diff))
                if diff < min_diff:
                    min_diff = diff
                    matched_job = job
        
        if matched_job == None:
            pass
            #self.dbglog.LogMessage("return point 3")
        else:
            self.dbglog.LogMessage(matched_job.jobid)
                    
        #run the matched job on the neiborbor partition
        if matched_job and partlist:
            self.start_job([{'tag':'job', 'jobid':matched_job.jobid}], {'location':partlist})
            msg = "job=%s, partition=%s, mached_job=%s, matched_partitions=%s" % (jobid, partition, matched_job.jobid, partlist)
            self.dbglog.LogMessage(msg)
        
        return 1
   
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
                    
                #to be inserted co-scheduling handling code
                else:
                    pass
            
            if action == "start":
                #print "BQSIM-normal start job %s on nodes %s" % (spec['jobid'], nodelist)
                self.start_job([spec], {'location': nodelist})
            elif action == "hold":
                #print "try to hold job %s on location %s" % (local_job_id, nodelist)
                tempjob = self.hold_job([spec], {'location': nodelist})
            elif action == "start_both":
                #print "start both mated jobs %s and %s" % (local_job_id, mate_job_id)
                self.start_job([spec], {'location': nodelist})
                ComponentProxy(REMOTE_QUEUE_MANAGER).run_holded_job([{'jobid':mate_job_id}])
            elif action == "start_both_or_give_up":
                #print "BQSIM: In order to run local job %s, try to run mate job %s" % (local_job_id, mate_job_id)
                try:
                    mate_job_can_run = ComponentProxy(REMOTE_QUEUE_MANAGER).try_to_run_mate_job(mate_job_id)
                except:
                    self.logger.error("failed to connect to remote queue-manager component!")
                    mate_job_can_run = False
                if mate_job_can_run:
                    #now that mate has been started, start local job
                    #print "-------------bqim: mate_job %s can run, start local job %s" % (mate_job_id, local_job_id)
                    self.start_job([spec], {'location': nodelist})
                    #print "local started ", spec.get('jobid')
                    
                    dbgmsg += " ###start both"
                    
                else:
                    #print "bqsim mate_job %s cannot run, job %s gives up" % (mate_job_id, local_job_id)
                    self.givingup_job_list.append(spec.get('jobid'))  #int
                    #self.release_allocated_nodes(nodelist)                    
                    
                    dbgmsg += "  --give up run local"
                self.dbglog.LogMessage(dbgmsg)
                #time.sleep(1)
                
            if self.walltime_aware_aggr:
                self.run_matched_job(spec['jobid'], nodelist[0])
                    
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
        jobs include the given mate job, return True else return False.  _jobid : int
        '''
        #print "entered bqsim.try_to_run_mate_job, jobid=", _jobid
            
        mate_job_started = False
        
        #start all the jobs that can run
        gohead = True
        while gohead:
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
            
            #print "queue order=", [item['jobid'] for item in job_location_args]
            
            best_partition_dict = self.find_job_location(job_location_args, end_times)
            
            if best_partition_dict:
                #print "best_partition_dict=", best_partition_dict
                
                for canrun_jobid in best_partition_dict:
                    nodelist = best_partition_dict[canrun_jobid]
                    
                    if str(_jobid) == canrun_jobid:
                        mate_job_started = True
                            
                    self.start_job([{'tag':"job", 'jobid':int(canrun_jobid)}], {'location':nodelist})
                    #print "bqsim.try_to_run_mate, start job jobid ", canrun_jobid 
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
        start_holded = False
        for spec in specs:
            if self.job_hold_dict.has_key(spec['jobid']):
                start_holded = True
                  
        partitions = updates['location']
        for partition in partitions:
            if not start_holded:
                self.reserve_partition(partition)
            partsize = int(self._partitions[partition].size)
            self.num_busy += partsize
            
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
        partitions = updates['location']
        for partition in partitions:
            self.reserve_partition(partition)
            partsize = int(self._partitions[partition].size)
                    
        for spec in specs:
            self.job_hold_dict[spec['jobid']] = partitions 
                    
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

        updates.update(newattr)
    
        return updates
    
    def compute_utility_scores (self):
        utility_scores = []
        current_time = time.time()
            
        for job in self.queues.get_jobs([{'is_runnable':True}]):    
            utility_name = self.queues[job.queue].policy
            args = {'queued_time':current_time - float(job.submittime), 
                    'wall_time': 60*float(job.walltime),    
                    'wall_time_p':  60*float(job.walltime_p), ##  *AdjEst*
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
            '''WFP'''
            if self.predict_queue:
                wall_time_sched = wall_time_p
            else:
                wall_time_sched = wall_time
                            
            val = ( queued_time / wall_time_sched)**3 * (size/64.0)
            
            return val
        
        def high_prio():
            val = 1.0
            return val
    
        self.builtin_utility_functions["default"] = default
        self.builtin_utility_functions["high_prio"] = high_prio
        
    def get_neighbor_by_partition(self, partname):
        '''get the neighbor partition by given partition name.
          note: this functionality is specific to intrepid partition naming and for partition size smaller than 4k'''
        nbpart = ""
        partition = self._partitions[partname]
        partsize = partition.size
        if partsize == 512:  #e.g. ANL-R12-M0-512  --> ANL-R12-M1-512
            nbpart = "%s%s%s" % (partname[0:9], 1-int(partname[9]), partname[10:])  #reverse the midplane
        elif partsize == 1024:  #e.g.  ANL-R12-1024 --> ANL-R13-1024
            rackno = int(partname[6])
            if rackno % 2 == 0:  #even
                nbrackno = rackno + 1
            else:
                nbrackno = rackno - 1
            nbpart = "%s%s%s" % (partname[0:6], nbrackno, partname[7:])    #find the neighbor rack
        elif partsize == 2048:  #e.g. ANL-R12-R13-2048 --> ANL-R14-R15-2048
            rackno1 = int(partname[6])
            rackno2 = int(partname[10])
            if rackno1 % 4 == 0:  #0, 4 ...
                nbrackno1 = rackno1 + 2
                nbrackno2 = rackno2 + 2
            else:  #2, 6
                nbrackno1 = rackno1 - 2
                nbrackno2 = rackno2 - 2
            nbpart = "%s%s%s%s%s" % (partname[0:6], nbrackno1, partname[7:10], nbrackno2, partname[11:])
        elif partsize == 4096:  #e.g. ANL-R10-R13-4096 --> ANL-R14-R17-4096
            rackno1 = int(partname[6])
            rackno2 = int(partname[10])
            if rackno1 == 0: 
                nbrackno1 = rackno1 + 4
                nbrackno2 = rackno2 + 4
            elif rackno1 == 4:
                nbrackno1 = rackno1 - 4
                nbrackno2 = rackno2 - 4
            nbpart = "%s%s%s%s%s" % (partname[0:6], nbrackno1, partname[7:10], nbrackno2, partname[11:])
        return nbpart
    
    def get_running_job_by_partition(self, partname):
        '''return a running job given the partition name'''
        partition = self._partitions[partname]
        if partition.state == "idle":
            return None               
        for rjob in self.running_jobs:
            partitions = rjob.location
            if partname in partitions:
                return rjob
        return None
        
    def _find_job_location(self, args, drain_partitions=set(), backfilling=False):
        jobid = args['jobid']
        nodes = args['nodes']
        queue = args['queue']
        utility_score = args['utility_score']
        walltime = args['walltime']
        walltime_p = args['walltime_p']  #*AdjEst* 
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])
        
        best_score = sys.maxint
        best_partition = None
        
        available_partitions = set()
        
        requested_location = None
        if args['attrs'].has_key("location"):
            requested_location = args['attrs']['location']
               
        if required:
            # whittle down the list of required partitions to the ones of the proper size
            # this is a lot like the stuff in _build_locations_cache, but unfortunately, 
            # reservation queues aren't assigned like real queues, so that code doesn't find
            # these
            for p_name in required:
                available_partitions.add(self.cached_partitions[p_name])
                available_partitions.update(self.cached_partitions[p_name]._children)

            possible = set()
            for p in available_partitions:            
                possible.add(p.size)
                
            desired_size = 64
            job_nodes = int(nodes)
            for psize in sorted(possible):
                if psize >= job_nodes:
                    desired_size = psize
                    break
            
            for p in available_partitions.copy():
                if p.size != desired_size:
                    available_partitions.remove(p)
                elif p.name in self._not_functional_set:
                    available_partitions.remove(p)
                elif requested_location and p.name != requested_location:
                    available_partitions.remove(p)
        else:
            for p in self.possible_locations(nodes, queue):
                skip = False
                for bad_name in forbidden:
                    if p.name == bad_name or bad_name in p.children or bad_name in p.parents:
                        skip = True
                        break
                if not skip:
                    if (not requested_location) or (p.name == requested_location):
                        available_partitions.add(p)
        
        available_partitions -= drain_partitions
        now = self.get_current_time()
        best_partition_list = []
        
        for partition in available_partitions:
            # if the job needs more time than the partition currently has available, look elsewhere    
            if self.predict_backfill:
                runtime_estimate = float(walltime_p)   # *Adj_Est*
            else:
                runtime_estimate = float(walltime)
            
            if backfilling:
                if 60*runtime_estimate > (partition.backfill_time - now):
                    continue
                
            if partition.state == "idle":
                # let's check the impact on partitions that would become blocked
                score = 0
                for p in partition.parents:
                    if self.cached_partitions[p].state == "idle" and self.cached_partitions[p].scheduled:
                        score += 1
                
                # the lower the score, the fewer new partitions will be blocked by this selection
                if score < best_score:
                    best_score = score
                    best_partition = partition
                    
                    best_partition_list[:] = []
                    best_partition_list.append(partition)
                #record equavalent partitions that have same best score
                elif score == best_score:
                    best_partition_list.append(partition)
        
        if self.walltime_aware_cons and len(best_partition_list) > 1:
            #print "best_partition_list=", [part.name for part in best_partition_list]
            #walltime aware job allocation (conservative)         
            least_diff = MAXINT
            for partition in best_partition_list:
                nbpart = self.get_neighbor_by_partition(partition.name)
                if nbpart:
                    nbjob = self.get_running_job_by_partition(nbpart)
                    if nbjob:
                        nbjob_remain_length = nbjob.starttime + 60*float(nbjob.walltime) - self.get_current_time_sec()
                        diff = abs(60*float(walltime) - nbjob_remain_length)
                        if diff < least_diff:
                            least_diff = diff
                            best_partition = partition
                        msg = "jobid=%s, partition=%s, neighbor part=%s, neighbor job=%s, diff=%s" % (jobid, partition.name, nbpart, nbjob.jobid, diff)
                        self.dbglog.LogMessage(msg)
            msg = "------------job %s allocated to best_partition %s-------------" % (jobid,  best_partition.name)
            self.dbglog.LogMessage(msg)
                            
        if best_partition:
            return {jobid: [best_partition.name]}

    def find_job_location(self, arg_list, end_times):
        best_partition_dict = {}
        
        if self.bridge_in_error:
            return {}
        
        self.cached_partitions = self.partitions

        # build the cached_partitions structure first
        self._build_locations_cache()

        # first, figure out backfilling cutoffs per partition (which we'll also use for picking which partition to drain)
        job_end_times = {}
        for item in end_times:
            job_end_times[item[0][0]] = item[1]
            
        now = self.get_current_time()
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
        
        for job in arg_list:
            partition_name = self._find_job_location(job, drain_partitions)
            if partition_name:
                best_partition_dict.update(partition_name)
                break
            
            location = self._find_drain_partition(job)
            if location is not None:
                for p_name in location.parents:
                    drain_partitions.add(self.cached_partitions[p_name])
                for p_name in location.children:
                    drain_partitions.add(self.cached_partitions[p_name])
                    self.cached_partitions[p_name].draining = True
                drain_partitions.add(location)
                #self.logger.info("job %s is draining %s" % (winning_job['jobid'], location.name))
                location.draining = True
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_partition_dict:
            
            # arg_list.sort(self._walltimecmp)

            for args in arg_list:
                partition_name = self._find_job_location(args, backfilling=True)
                if partition_name:
                    self.logger.info("backfilling job %s" % args['jobid'])
                    best_partition_dict.update(partition_name)
                    break

        return best_partition_dict
    find_job_location = locking(exposed(find_job_location))

    #display stuff
    
    def get_midplanes_by_state(self, status):
        idle_midplane_list = []
                
        for partition in self._partitions.itervalues():
            if partition.size == MIDPLANE_SIZE:
                if partition.state == status:
                    idle_midplane_list.append(partition.name)
                
        return idle_midplane_list        

    def show_resource(self):
        '''print rack_matrix'''
        
        self.mark_matrix()
        
        for row in self.rack_matrix:
            for rack in row:
                if rack[0] == 1:
                    print "*",
                elif rack[0] == 0:
                    print GREENS + 'X' + ENDC,
            print '\r'
            for rack in row:
                if rack[1] == 1:
                    print "*",
                elif rack[1] == 0:
                    print GREENS + 'X' + ENDC,
            print '\r'
             
    def mark_matrix(self):
        idle_midplanes = self.get_midplanes_by_state('idle')
        self.reset_rack_matrix()
        for name in idle_midplanes:  #sample name for a midplane:  ANL-R15-M0-512
            row = int(name[5])
            col = int(name[6])
            M = int(name[9])
            self.rack_matrix[row][col][M] = 1
            
    def reset_rack_matrix(self):
        self.rack_matrix = [
                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
            ]
        #self.rack_matrix = [[[0,0] for i in range(8)] for j in range(5)]
    
    def print_screen(self, cur_event=""):
        '''print screen, show number of waiting jobs, running jobs, busy_nodes%'''
        
        #os.system('clear')
        
        print "Blue Gene"
        
        if PRINT_SCREEN == False:
            print "simulation in progress, please wait"
            return            
        
        current_datetime = self.event_manager.get_current_date_time()
        print "%s %s" % (current_datetime, cur_event)
        
        self.show_resource()
         
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
        
        midplanes = self.num_busy / 512
        print "number of busy midplanes: ", midplanes
        print "system utilization: ", float(self.num_busy) / 40960.0
        busy_midplane_bar = GREENS
        
        i = 0
        while i < midplanes:
            busy_midplane_bar += "x"
            i += 1
        for j in range(i, 80):
            busy_midplane_bar += "-"
        busy_midplane_bar += ENDC
        busy_midplane_bar += REDS
        busy_midplane_bar += "|"
        busy_midplane_bar += ENDC
        print busy_midplane_bar
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
        print "\n\n"
            
    #coscheduling stuff
    def get_mate_job_status_bqsim(self, jobid):
        '''return mate job status, remote function, invoked by remote component'''
        #local_job = self.get_live_job_by_id(jobid)
        ret_dict = {'jobid':jobid}
        ret_dict['status'] = self.get_coschedule_status(jobid)
        return ret_dict
    get_mate_job_status_bqsim = exposed(get_mate_job_status_bqsim)
    
    def get_mate_jobs_status_local(self, remote_jobid):
        '''return mate job status, invoked by local functions'''
        status_dict = {}
        try:
            status_dict = ComponentProxy(REMOTE_QUEUE_MANAGER).get_mate_job_status_cqsim(remote_jobid)
        except:
            self.logger.error("failed to connect to remote cluster queue-manager component!")
        return status_dict
    
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
    
    def reserve_partition (self, name, size=None):
        """Reserve a partition and block all related partitions.
        
        Arguments:
        name -- name of the partition to reserve
        size -- size of the process group reserving the partition (optional)
        """
        
        try:
            partition = self.partitions[name]
        except KeyError:
            self.logger.error("reserve_partition(%r, %r) [does not exist]" % (name, size))
            return False
#        if partition.state != "allocated":
#            self.logger.error("reserve_partition(%r, %r) [%s]" % (name, size, partition.state))
#            return False
        if not partition.functional:
            self.logger.error("reserve_partition(%r, %r) [not functional]" % (name, size))
        if size is not None and size > partition.size:
            self.logger.error("reserve_partition(%r, %r) [size mismatch]" % (name, size))
            return False

        self._partitions_lock.acquire()
        try:
            partition.state = "busy"
            partition.reserved_until = False
        except:
            self.logger.error("error in reserve_partition", exc_info=True)
        self._partitions_lock.release()
        # explicitly call this, since the above "busy" is instantaneously available
        self.update_partition_state()
        
        self.logger.info("reserve_partition(%r, %r)" % (name, size))
        return True
    reserve_partition = exposed(reserve_partition)
             