#!/usr/bin/env python

'''Some base definitions for Qsim'''

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
SET_event = set(['I', 'Q', 'S', 'E', 'F', 'R', 'U'])

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
    
    temp= {}
    splits = line.split(';')
        
    for item in splits:
        tup = item.partition('=')
        temp[tup[0]] = tup[2]
    
    fmtdate = temp['qtime']
    submittime_sec = date_to_sec(fmtdate, "%Y-%m-%d %H:%M:%S")
    submittime_date = sec_to_date(submittime_sec)
    temp['submittime'] = submittime_date

    if temp.has_key('start') and temp.has_key('end'):
        start_date = temp['start']
        start_sec = date_to_sec(start_date, "%Y-%m-%d %H:%M:%S")
        temp['start'] = start_sec
        end_date = temp['end']
        end_sec = date_to_sec(end_date, "%Y-%m-%d %H:%M:%S")
        temp['end'] = end_sec

    walltime_sec = temp['Resource_List.walltime']  #sec in log
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


def subtimecmp(spec1, spec2):
    return cmp(spec1.get('submittime'), spec2.get('submittime'))
        
def tune_workload(specs, frac=1, anchor=0):
    '''tune workload heavier or lighter, and adjust the start time to anchor, specs should be sorted by submission time'''
  
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
                            "nodes","runtime", "start_time", "end_time", "last_hold", "hold_time", "first_yield",
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
        self.last_hold = spec.get('last_hold', 0) # #the time (unix sec) the job starts a latest holding (coscheduling only)
        self.hold_time = 0 #the time period during which the job is holding (coscheduling only)
        self.yield_time = spec.get('first_yield', 0) #the time the job first yields (coscheduling only)
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
        self.location = spec.get('location', '')  #original location read from job trace, used for job reservation

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
            
class Qsim():
    '''Cobalt Queue Simulator (base class)'''
    
    implementation = "qsim"
    name = "queue-manager"
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        pass        
