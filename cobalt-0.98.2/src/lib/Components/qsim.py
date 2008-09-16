#!/usr/bin/env python

'''Cobalt Queue Simulator library'''

import ConfigParser
import logging
import math
import os
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

from Cobalt.Components.base import Component, exposed, query, automatic
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.simulator import Simulator
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

MIDPLANE_SIZE = 512
default_SCALE = 2000000
default_SHAPE = 0.9 
default_SENSITIVITY = 0.7
default_SPECIFICITY = 0.9
default_FAILURE_LOG = "failure.lists"
logger = logging.getLogger('Qsim')

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
    '''Job for simulation'''
        
    #_config = ConfigParser.ConfigParser()

    fields = Data.fields + ["jobid", "submittime", "queue", "walltime",
                            "nodes","runtime", "start_time", "end_time",
                            "failure_time", "location", "state", "is_visible",
                            "args"]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = 'job'
        #following fields are initialized at beginning of simulation
        self.jobid = int(spec.get("jobid"))
        self.queue = spec.get("queue", "default")
        
        self.submittime = spec.get("submittime")   #in seconds
        
        self.walltime = spec.get("walltime")   #in minutes
        
        self.nodes = spec.get("nodes", 0)
        self.runtime = spec.get("runtime", 0)
        
        self.start_time = spec.get('start_time', '0')
        self.end_time = spec.get('end_time', '0')
        self.state = spec.get("state", "invisible")
        self.failure_time = 0
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
        self.state = 'running'
        self.tag = 'queue'
        
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

class PBSlogger:
    '''Logger to generate PBS-style event log'''

    def __init__(self, name):
        #get log directory
        CP = ConfigParser.ConfigParser()
        CP.read(Cobalt.CONFIG_FILES)
        try:
            self.logdir = CP.get('cqm', 'log_dir')
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
   
        #get command line parameters
        self.FAILURE_FREE = True
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
        if self.fault_aware:
            self.SENSITIVITY = float(kwargs.get('sensitivity'))
            if self.SENSITIVITY == 0:
                self.SENSITIVITY = default_SENSITIVITY
            self.SPECIFICITY = float(kwargs.get('specificity'))
            if self.SPECIFICITY == 0:
                self.SPECIFICITY = default_SPECIFICITY
        
        if self.failure_log or self.weibull:
            self.FAILURE_FREE = False
        
        #initialize time stamps and job queues
        self.time_stamps = [0]
        self.cur_time_index = 0
        self.queues = SimQueueDict()
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
        
    def get_current_time(self):
        '''get current time in date format'''
        return self.time_stamps[self.cur_time_index]
    
    def get_current_time_stamp(self):
        '''get current time stamp index'''
        return self.cur_time_index
    get_current_time_stamp = exposed(get_current_time_stamp)

    def time_increment(self):
        '''the current time stamp increments by 1'''
        if self.cur_time_index  < len(self.time_stamps) - 1:
            self.cur_time_index += 1
            print str(self.get_current_time()) + \
            " time stamp incremented by 1, current time stamp: " + \
            str(self.cur_time_index)
        else:
            print str(self.get_current_time()) +\
            " Reached maximum time stamp: %s, simulating finished! " \
             %  (str(self.cur_time_index))
            self.finished = True
            self.pbslog.closeLog()
            qsim_quit()  #simulation completed, exit!!!
        return self.cur_time_index
   
    def init_queues(self):
        '''parses the work load log file, initializes queues and sorted time 
        stamp list'''
        
        raw_jobs = parse_work_load(self.workload_file)
        specs = []
        
        for key in raw_jobs:
            spec = {'valid':True}
            tmp = raw_jobs[key]
            
            spec['jobid'] = tmp.get('jobid')
            spec['queue'] = tmp.get('queue')
            
            #convert submittime from "%m/%d/%Y %H:%M:%S" to Unix time sec
            format_sub_time = tmp.get('submittime')
            if format_sub_time:
                spec['submittime'] = date_to_sec(format_sub_time)                
            else:
                spec['valid'] = False
                
            #convert walltime from 'hh:mm:ss' to float of minutes
            format_walltime = tmp.get('Resource_List.walltime')
            if format_walltime:
                segs = format_walltime.split(':')
                spec['walltime'] = str(int(segs[0])*60 + int(segs[1]))
            else:  #invalid job entry, discard
                spec['valid'] = False
            
            if tmp.get('Resource_List.nodect'):
                spec['nodes'] = tmp.get('Resource_List.nodect')
            else:  #invalid job entry, discard
                spec['valid'] = False
            
            if tmp.get('start') and tmp.get('end'):
                act_run_time = float(tmp.get('end')) - float(tmp.get('start'))
                spec['runtime'] = str(round(act_run_time, 1))
            else:
                spec['valid'] = False
            
            spec['state'] = 'invisible'
            spec['start_time'] = '0'
            spec['end_time'] = '0'
            
            #add the job spec to the spec list
            if spec['valid'] == True:
                specs.append(spec)
                if not self.time_stamps.__contains__(format_sub_time):
                    self.insert_time_stamp(format_sub_time)
            
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
        if eventtype == 'Q':
            message = "%s;Q;%d;queue=%s" % (timestamp, spec['jobid'], spec['queue'])
        else:
            wall_time = spec['walltime']
            walltime_minutes = len2(int(float(wall_time)) % 60)
            walltime_hours = len2(int(float(wall_time)) // 60)
            log_walltime = "%s:%s:00" % (walltime_hours, walltime_minutes)
            if eventtype == 'S':
                message = "%s;S;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s start=%s exec_host=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, spec['start_time'], spec['location'])
            elif eventtype == 'E':
                message = "%s;E;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s start=%s end=%f exec_host=%s runtime=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], spec['nodes'], log_walltime, spec['start_time'], 
                 round(float(spec['end_time']), 1), spec['location'], 
                 spec['runtime'])
            elif eventtype == 'F':
                failtime =  round(float(spec['failure_time']) - float(spec['start_time']), 1)
                message = "%s;F;%d;queue=%s qtime=%s Resource_List.ncpus=%s Resource_List.walltime=%s exec_host=%s start=%s failtime=%s complete=%f" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], 
                 spec['nodes'], log_walltime, spec['location'], spec['start_time'], 
                 failtime, round(failtime / float(spec['runtime']), 2)
                )
            else:
                print "invalid event type, type=", type
                return
        self.pbslog.LogMessage(message)
                
    def get_new_state(self, jobspec):
        '''return the new state updates of a specific job at specific time 
        stamp, including invisible->queued, running->ended'''
        
        updates = {}
        curstate = jobspec['state']
        newstate = curstate
        job_id = jobspec['jobid']
   
        submit_time_sec = float(jobspec['submittime'])
        if submit_time_sec == 0:  #the never submitted job
            return updates
        else:
            submit_datetime = sec_to_date(submit_time_sec)
                        
        if jobspec['end_time']:
            end = float(jobspec['end_time'])
        else:
            end = 0
        end_datetime = sec_to_date(end)
        
        if jobspec['failure_time']:
            fail = float(jobspec['failure_time'])
        else:
            fail = 0
        failure_datetime = sec_to_date(fail)
        
        #make state change
        if curstate == 'running':
            #job fails, resubmit
            if failure_datetime == self.get_current_time():
                newstate = 'queued'
                updates['failure_time'] = 0
                partitions = jobspec['location'].split(':')
                for partition in partitions:
                    self.release_partition(partition)
                self.log_job_event('F', failure_datetime, jobspec)
                print self.get_current_time(), " job %d failed at %s!!" % (job_id, jobspec['location'])
            #job completes
            elif end_datetime == self.get_current_time():
                newstate = 'ended'
                updates['is_visible'] = False                                                                                                   
                self.log_job_event('E', end_datetime, jobspec)
                partitions = jobspec['location'].split(':')
                for partition in partitions:
                    self.release_partition(partition)
                self.queues.del_jobs([{'jobid':job_id}])
            
        elif curstate == 'invisible':
            if  submit_datetime == self.get_current_time():
                newstate = 'queued'
                updates['is_visible'] = True
                self.log_job_event('Q', self.get_current_time(), jobspec)
                
        if not jobspec['state'] == newstate:
            print self.get_current_time(), "state change, job", job_id, \
             ":", curstate, "->", newstate
            updates['state'] = newstate
        
        return updates               
    
    def insert_time_stamp(self, new_time):
        '''insert time stamps in the same order'''
        pos = len(self.time_stamps)
        while new_time < self.time_stamps[pos-1]:
            pos = pos -1
        self.time_stamps.insert(pos, new_time)
     
    def run_job_updates(self, jobspec, newattr):
        ''' return the state updates (including state queued -> running, 
        setting the start_time, end_time)'''
        updates = {}
        if not jobspec['state'] == 'queued':
            return updates
        
        start = date_to_sec(self.get_current_time())
        updates['start_time'] = start
        
        updates['state'] = 'running'
        print self.get_current_time(), "state change, job", jobspec['jobid'], \
             ":", jobspec['state'], "->", updates['state']
             
        #determine whether the job is going to fail before completion
        location = newattr['location']
        duration = float(jobspec['runtime'])
        nearest_failure = self.get_next_failure(location, start, duration)
        if (nearest_failure):
            updates['failure_time'] = date_to_sec(nearest_failure)
            new_time_stamp = nearest_failure
        else:  # will complete
            end = start + duration
            updates['end_time'] = end
            new_time_stamp = sec_to_date(end)
            
        #insert new time stamp for job end or failure
        self.insert_time_stamp(new_time_stamp)
        
        updates.update(newattr)
      
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
        if self.increment_tag:
            self.time_increment()
        self.increment_tag = True
        self.update_job_states(specs, {})
        for spec in specs:
            spec['is_visible'] = True
        jobs = self.queues.get_jobs(specs)
        return jobs
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
            #set tag false, enable scheduling another job at the same time
            self.increment_tag = False
        return self.queues.get_jobs([{'jobid':"*", 'state':"running"}])
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
                                       
        closest_fail_sec = sys.maxint
        partitions = location.split(':')
        
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
                        
        if closest_fail_sec == sys.maxint:
            next_failure_date = None
        else:
            job_end_sec = now + duration
            if closest_fail_sec < job_end_sec:
                next_failure_date = sec_to_date(closest_fail_sec)
            else:
                next_failure_date = None
                
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
        start = self.time_stamps[1]
        end = self.time_stamps[len(self.time_stamps)-1]
        
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
        if (next_fail):
            return self.SENSITIVITY
        else:
            return 1 - self.SPECIFICITY
    get_failure_chance = exposed(get_failure_chance)
    