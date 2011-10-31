#!/usr/bin/env python

'''Cobalt Queue Simulator (for cluster systems) library'''

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
import random

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from datetime import datetime

import Cobalt
import Cobalt.Cqparse
import Cobalt.Util

from Cobalt.Components.qsim_base import *
from Cobalt.Components.base import exposed, query, automatic, locking
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.cluster_base_system import ClusterBaseSystem
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

REMOTE_QUEUE_MANAGER = "queue-manager"
MACHINE_ID = 1
MACHINE_NAME = "Eureka"
DEFAULT_VICINITY = 0
DEFAULT_MAX_HOLDING_SYS_UTIL = 0.6
SELF_UNHOLD_INTERVAL = 0
AT_LEAST_HOLD = 600
YIELD_THRESHOLD = 0
    
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
        self.output_log = MACHINE_NAME + "-" + kwargs.get("outputlog", "")
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
        
        self.cosched_scheme_tup = kwargs.get("coscheduling", (0,0))
        self.cosched_scheme = self.cosched_scheme_tup[1]
        self.cosched_scheme_remote = self.cosched_scheme_tup[0]
        self.mate_vicinity = kwargs.get("vicinity", 0)
        self.mate_ratio = kwargs.get("mate_ratio", 0)
        
        valid_cosched_schemes = ["hold", "yield"]
        
        if self.cosched_scheme in valid_cosched_schemes and self.cosched_scheme_remote in valid_cosched_schemes:
            self.coscheduling = True
        else:
            self.coscheduling = False
            
        if not kwargs.get("bgjob", None):
            self.coscheduling = False
            
        self.mate_job_dict = {}
            
        if self.coscheduling:
            self.jobid_qtime_pairs =  self.init_jobid_qtime_pairs()           
            try:
                self.remote_jobid_qtime_pairs = ComponentProxy(REMOTE_QUEUE_MANAGER).get_jobid_qtime_pairs()
            except:
                self.logger.error("fail to connect to remote queue-manager component!")
                self.coscheduling = False

            if self.mate_vicinity:
                print "start init mate job dict, vicinity=", self.mate_vicinity
                self.init_mate_job_dict_by_vicinity()
            elif self.mate_ratio:
                print "start init mate job dict, mate_ratio=", self.mate_ratio
                self.init_mate_job_dict_by_ratio(self.mate_ratio)
            else:
                self.logger.error("fail to initialize mate job dict!")
            
            matejobs = len(self.mate_job_dict.keys())
            proportion = float(matejobs) / self.total_job
       
        #recording holding job id and holden resource    
        self.job_hold_dict = {}
        
        #record holding job's holding time   jobid:first hold (sec)
        self.first_hold_time_dict = {} 
            
        #record yield jobs's first yielding time, for calculating the extra waiting time
        self.first_yield_hold_time_dict = {}
        
        #record yield job ids. update dynamically
        self.yielding_job_list = []
        
        if self.coscheduling:
            remote_mate_job_dict = dict((v,k) for k, v in self.mate_job_dict.iteritems())
            try:
                ComponentProxy(REMOTE_QUEUE_MANAGER).set_mate_job_dict(remote_mate_job_dict)
            except:
                self.logger.error("failed to connect to remote queue-manager component!")
                self.coscheduling = False
            print "number of mate job pairs: %s, proportion in cluster jobs: %s%%" \
            % (len(self.mate_job_dict.keys()), round(proportion *100, 1) )
            
        self.max_holding_sys_util = DEFAULT_MAX_HOLDING_SYS_UTIL
    
    def get_current_time(self):
        '''this function overrid the get_current_time in bgsched, bg_base_system, and cluster_base_system'''
        return  self.event_manager.get_current_time()
    
    def get_current_time_sec(self):
        return  self.event_manager.get_current_time()
    
    def get_current_time_date(self):
        return self.event_manager.get_current_date_time()

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
        
    def _get_queuing_jobs(self):
        return [job for job in self.queues.get_jobs([{'is_runnable':True}])]
    queuing_jobs = property(_get_queuing_jobs)
    
    def _get_running_jobs(self):
        return [job for job in self.queues.get_jobs([{'has_resources':True}])]
    running_jobs = property(_get_running_jobs)
        
    def add_queues(self, specs):
        '''add queues'''
        return self.queues.add_queues(specs)
    add_queues = exposed(query(add_queues))
    
    def get_queues(self, specs):
        '''get queues'''
        return self.queues.get_queues(specs)
    get_queues = exposed(query(get_queues))

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
                parts = format_walltime.split(',')
                days = 0
                if len(parts) > 1: #contain day:  1 day, 11:00:00
                    days = int(parts[0].split(' ')[0])
                    minutes_part = parts[1]
                else:
                    minutes_part = parts[0] 
                segs = minutes_part.split(':')
                walltime_minutes = int(segs[0])*60 + int(segs[1])
                total_walltime_minutes = walltime_minutes + days * 24 * 60
                spec['walltime'] = str(total_walltime_minutes)
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
                spec['walltime_p'] = float(spec['walltime']) * ap
            else:
                spec['walltime_p'] = float(spec['walltime'])
             
            spec['state'] = 'invisible'
            spec['start_time'] = '0'
            spec['end_time'] = '0'
            spec['queue'] = "default"
            spec['has_resources'] = False
            spec['is_runnable'] = False
            
            #add the job spec to the spec list            
            specs.append(spec)

        specs.sort(subtimecmp)
                
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
            elif eventtype == "U":  #unhold some resources  
                message = "%s;U;%s;host=%s" % \
                (timestamp, spec['jobid'], ":".join(spec['location']))
            elif eventtype == 'E':  #end
                first_yield_hold = self.first_yield_hold_time_dict.get(int(spec['jobid']), 0)
                if first_yield_hold > 0:
                    overhead = spec['start_time'] - first_yield_hold
                else:
                    overhead = 0
                message = "%s;E;%s;queue=%s qtime=%s Resource_List.nodect=%s Resource_List.walltime=%s start=%s end=%f exec_host=%s runtime=%s hold=%s overhead=%s" % \
                (timestamp, spec['jobid'], spec['queue'], spec['submittime'], spec['nodes'], log_walltime, spec['start_time'], 
                 round(float(spec['end_time']), 1), ":".join(spec['location']),
                 spec['runtime'], spec['hold_time'], overhead)
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
            
            cur_event = self.event_manager.get_current_event_type()
            
            
            if cur_event in ["Q", "E"]:
                self.update_job_states(specs, {}, cur_event)
            
            self.compute_utility_scores()
            
            #unhold holding job. MUST be after compute_utility_scores()    
            if cur_event == "U":
                cur_job = self.event_manager.get_current_event_job()
                
                if cur_job in self.job_hold_dict.keys():
                    self.unhold_job(cur_job)
                else:
                    #if the job not in job_hold_dict, do nothing. the job should have already started
                    return []
                
            if cur_event == "C":
                if self.job_hold_dict.keys():
                    self.unhold_all()
                            
        self.event_manager.set_go_next(True)
        
        jobs = self.queues.get_jobs([{'tag':"job"}])
        
        if self.yielding_job_list:
            jobs = [job for job in jobs if job.jobid not in self.yielding_job_list]
  
        return jobs
    get_jobs = exposed(query(get_jobs))
    
    def update_job_states(self, specs, updates, cur_event):
        '''update the state of the jobs associated to the current time stamp'''
          
        ids_str = str(self.event_manager.get_current_event_job())
        
        ids = ids_str.split(':')
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
        
        if jobspec['last_hold'] > 0:
            updates['hold_time'] = jobspec['hold_time'] + self.get_current_time_sec() - jobspec['last_hold']

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
                    dbgmsg1 = "local=%s;mate=%s;mate_status=%s" % (local_job_id, mate_job_id, remote_status)
                    self.dbglog.LogMessage(dbgmsg1)
                    
                    if remote_status in ["queuing", "unsubmitted"]:
                        if self.cosched_scheme == "hold": # hold resource if mate cannot run, favoring job
                            action = "start_both_or_hold"
                        if self.cosched_scheme == "yield": # give up if mate cannot run, favoring sys utilization
                            action = "start_both_or_yield"                        
                    if remote_status == "holding":
                        action = "start_both"
                    
                    #self.dbglog.LogMessage(dbgmsg)
                #to be inserted co-scheduling handling code
                else:
                    pass
            
            if action == "start":
                #print "CQSIM-normal: start job %s on nodes %s" % (spec['jobid'], nodelist)
                self.start_job([spec], {'location': nodelist})
            elif action == "start_both_or_hold":
                #print "try to hold job %s on location %s" % (local_job_id, nodelist)
                mate_job_can_run = False
                #try to invoke a scheduling iteration to see if remote yielding job can run now
                try:
                    mate_job_can_run = ComponentProxy(REMOTE_QUEUE_MANAGER).try_to_run_mate_job(mate_job_id)
                except:
                    self.logger.error("failed to connect to remote queue-manager component!")
               
                if mate_job_can_run:
                    #now that mate has been started, start local job
                    self.start_job([spec], {'location': nodelist})
                    dbgmsg += " ###start both"
                else:
                    self.hold_job(spec, {'location': nodelist})
            elif action == "start_both":
                #print "start both mated jobs %s and %s" % (local_job_id, mate_job_id)
                self.start_job([spec], {'location': nodelist})
                ComponentProxy(REMOTE_QUEUE_MANAGER).run_holding_job([{'jobid':mate_job_id}])
            elif action == "start_both_or_yield":
                mate_job_can_run = False
                               
                #try to invoke a scheduling iteration to see if remote yielding job can run now
                try:
                    mate_job_can_run = ComponentProxy(REMOTE_QUEUE_MANAGER).try_to_run_mate_job(mate_job_id)
                except:
                    self.logger.error("failed to connect to remote queue-manager component!")
                  
                if mate_job_can_run:
                    #now that mate has been started, start local job
                    self.start_job([spec], {'location': nodelist})
                    dbgmsg += " ###start both"
                else:
                    #mate job cannot run, give up the turn. mark the job as yielding.
                    job_id = spec.get('jobid')
                    self.yielding_job_list.append(job_id)  #int
                    #record the first time this job yields
                    if not self.first_yield_hold_time_dict.has_key(job_id):
                        self.first_yield_hold_time_dict[job_id] = self.get_current_time_sec()
                        self.dbglog.LogMessage("%s: job %s first yield" % (self.get_current_time_date(), job_id))
                                    
        #set tag false, enable scheduling another job at the same time
        self.event_manager.set_go_next(False)
        #self.print_screen()
                
        return len(specs)
    run_jobs = exposed(run_jobs)
        
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
    
        # order the jobs with biggest utility first
    def utilitycmp(self, job1, job2):
        return -cmp(job1.score, job2.score)
    
    def compute_utility_scores (self):
        utility_scores = []
        current_time = self.get_current_time_sec()
            
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


#####coscheduling stuff
    def init_jobid_qtime_pairs(self):
        '''initialize mate job dict'''
        jobid_qtime_pairs = []
        
        for id, spec in self.unsubmitted_job_spec_dict.iteritems():
            qtime = spec['submittime']
            jobid_qtime_pairs.append((qtime, int(id)))
            
        def _qtimecmp(tup1, tup2):
            return cmp(tup1[0], tup2[0])
        
        jobid_qtime_pairs.sort(_qtimecmp)
        
        return jobid_qtime_pairs


    def find_mate_id(self, qtime, threshold):
    
        mate_subtime = 0
        ret_id = 0
        last = (0,0)
        for pair in self.remote_jobid_qtime_pairs:
            if pair[0] > qtime:
                break
            last = pair
            
        mate_subtime = last[0]
        mate_id = last[1]

        if mate_subtime > 0:
            if float(qtime) - mate_subtime  < threshold:
               ret_id = mate_id
        return ret_id
    
    def init_mate_job_dict_by_vicinity(self):
        '''init mate job dictionary by vicinity'''
        
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
        #reserve dict to local_id:remote_id. (guarentee one-to-one)
        self.mate_job_dict = dict((local_id, remote_id) for remote_id, local_id in temp_dict.iteritems())
        
    def init_mate_job_dict_by_ratio(self, ratio):
        '''init mate job dictionary by specified ratio'''
        
        if ratio <= 0.5:
            step = int(1.0 / ratio)
            reverse_step = 1
        else:
            step = 1
            reverse_step = int(1.0/(1-ratio))
        
        print "step=", step
        print "reverse_step=", reverse_step
        
        i = 0
        temp_dict = {}
        for item in self.jobid_qtime_pairs:
            remote_item = self.remote_jobid_qtime_pairs[i]
            random_number = random.random()
            if step > 1:
                if i % step == 0:
                    temp_dict[item[1]] = remote_item[1]
            if reverse_step > 1:
                if i % reverse_step != 0:
                    temp_dict[item[1]] = remote_item[1]
            i += 1
        self.mate_job_dict = temp_dict            
        
    def get_mate_job_dict(self):
        return self.mate_job_dict
    get_mate_job_dict = exposed(get_mate_job_dict)

    def hold_job(self, spec, updates):
        '''hold a job. a holding job is not started but hold some resources that can run itself in the future
        once its mate job in a remote system can be started immediatly. Note, one time hold only one job'''
        
        def _hold_job(job, newattr):
            '''callback function to update job start/end time'''
            temp = job.to_rx()
            newattr = self.hold_job_updates(temp, newattr)
            temp.update(newattr)
            job.update(newattr)
            self.log_job_event('H', self.get_current_time_date(), temp)
        
        current_holden_nodes = 0
        for nodelist in self.job_hold_dict.values():
            current_holden_nodes += len(nodelist)
            
        nodelist = updates['location']

        job_id = spec['jobid']
        if current_holden_nodes + len(nodelist) < self.max_holding_sys_util * self.total_nodes:
            self.job_hold_dict[job_id] = nodelist
            
            if not self.first_hold_time_dict.has_key(job_id):
                self.first_hold_time_dict[job_id] = self.get_current_time_sec()
            
            self.nodes_down(nodelist)
            
            if not self.first_yield_hold_time_dict.has_key(job_id):
                self.first_yield_hold_time_dict[job_id] = self.get_current_time_sec()
            
            return self.queues.get_jobs([spec], _hold_job, updates)
        else:
            #if execeeding the maximum limite of holding nodes, the job will not hold but yield
            self.yielding_job_list.append(job_id)  #int
            #record the first time this job yields
            if not self.first_yield_hold_time_dict.has_key(job_id):
                self.first_yield_hold_time_dict[job_id] = self.get_current_time_sec()
                self.dbglog.LogMessage("%s: job %s first yield" % (self.get_current_time_date(), job_id))
            return 0
        
    def hold_job_updates(self, jobspec, newattr):
        ''' return the state updates (including state queued -> running, 
        setting the start_time, end_time)'''
        updates = {}
        
        updates['is_runnable'] = False
        updates['has_resources'] = False
        updates['state'] = "holding"
        updates['last_hold'] = self.get_current_time_sec()
        
        updates.update(newattr)
             
        if SELF_UNHOLD_INTERVAL > 0:
            release_time = self.get_current_time_sec() + SELF_UNHOLD_INTERVAL
            self.insert_time_stamp(release_time, "U", {'jobid':jobspec['jobid'], 'location':newattr['location']})
        
        return updates
    
    def unhold_job(self, jobid):
        '''if a job holds a partition longer than MAX_HOLD threshold, the job will release the partition and starts yielding'''
        nodelist = self.job_hold_dict.get(jobid)
        
        #release holden partitions
        if nodelist:
            self.nodes_up(nodelist)
        else:
            print "holding job %s not found in job_hold_dict: " % jobid
            
        def _unholding_job(job, newattr):
            '''callback function'''
            temp = job.to_rx()
            newattr = self.unholding_job_updates(temp, newattr)
            temp.update(newattr)
            job.update(newattr)
            self.log_job_event("U", self.get_current_time_date(), temp)
            
            del self.job_hold_dict[jobid]
            
        return self.queues.get_jobs([{'jobid':jobid}], _unholding_job, {'location':self.job_hold_dict.get(jobid, ["N"])})
                
    def unholding_job_updates(self, jobspec, newattr):
        '''unhold job'''
        updates = {}
        
        updates['is_runnable'] = True
        updates['has_resources'] = False
        updates['state'] = "queued"
        #set the job to lowest priority at this scheduling point. 
        #if no other job gets the nodes it released, the unholden job can hold those nodes again
        updates['score'] = 0
        
        updates['hold_time'] = jobspec['hold_time'] + self.get_current_time_sec() - jobspec['last_hold']
        
        updates['last_hold'] = 0  
                
        updates.update(newattr)
        
        return updates
    
    def unhold_all(self):
        '''unhold all jobs. periodically invoked to prevent deadlock'''
        for jobid in self.job_hold_dict.keys():
            job_hold_time = self.get_current_time_sec() - self.first_hold_time_dict[jobid]
            #if a job has holden at least 10 minutes, then periodically unhold it
            if job_hold_time >  AT_LEAST_HOLD:
                self.unhold_job(jobid)
    
    def try_to_run_mate_job(self, _jobid):
        '''try to run mate job, start all the jobs that can run. If the started
        jobs include the given mate job, return True else return False.  _jobid : int
        '''
        #if the job is not yielding, do not continue; no other job is possibly to be scheduled
        if _jobid not in self.yielding_job_list:
            return False
            
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
        
    def run_holding_job(self, specs):
        '''start holding job'''
        for spec in specs:
            jobid = spec.get('jobid')
            nodelist = self.job_hold_dict.get(jobid, None)
            if nodelist == None:
                #print "cannot find holding resources"
                return
            #print "start holding job %s on location %s" % (spec['jobid'], nodelist)
            self.start_job([spec], {'location':nodelist})
            del self.job_hold_dict[jobid]
            
    run_holding_job = exposed(run_holding_job)         

    #coscheduling stuff
    def get_mate_job_status(self, jobid):
        '''return mate job status, remote function, invoked by remote component'''
        ret_dict = {'jobid':jobid}
        
        ret_dict['status'] = self.get_coschedule_status(jobid)

        return ret_dict
    get_mate_job_status = exposed(get_mate_job_status)
    
    def get_mate_jobs_status_local(self, remote_jobid):
        '''return mate job status, invoked by local functions'''
        status_dict = {}
        try:
            status_dict = ComponentProxy(REMOTE_QUEUE_MANAGER).get_mate_job_status(remote_jobid)
        except:
            self.logger.error("failed to connect to remote queue-manager component!")
            status_dict = {'status':'notconnected'}
            self.dbglog.LogMessage("failed to connect to remote queue-manager component!")
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
                
        holding_jobs = len(self.job_hold_dict.keys())
        holden_nodes = 0
        for nodelist in self.job_hold_dict.values():
            nodes = len(nodelist)
            holden_nodes += nodes
                        
        print "number of running jobs: ", self.num_running
        running_job_bar = BLUES
        for i in range(self.num_running):
            running_job_bar += "+"
        running_job_bar += ENDC
        print running_job_bar
        
        
        print "number of holding jobs: ", holding_jobs
        print "number of holden nodes: ", holden_nodes 
        
        print "number of busy nodes: ", self.num_busy
        print "system utilization: ", float(self.num_busy) / self.total_nodes
        busy_node_bar = GREENS
        
        i = 0
        while i < self.num_busy:
            busy_node_bar += "x"
            i += 1
        j = 0
        busy_node_bar += ENDC
        busy_node_bar += YELLOWS
        while j < holden_nodes:
            busy_node_bar += '+'
            j += 1
            i += 1
        busy_node_bar += ENDC
        for k in range(i, self.total_nodes):
            busy_node_bar += "-"
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
        #print "waiting jobs: ", [(job.jobid, job.nodes) for job in self.queues.get_jobs([{'is_runnable':True}])]
        #print "holding jobs: ", self.job_hold_dict.keys()
        if self.sleep_interval:
            time.sleep(self.sleep_interval)
    
    def post_simulation_handling(self):
        '''post screen after simulation completes'''
        #print self.first_yield_hold_time_dict
        pass
    post_simulation_handling = exposed(post_simulation_handling)
