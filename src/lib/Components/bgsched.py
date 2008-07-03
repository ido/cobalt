#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging
import sys
import time
import math
import types
import ConfigParser
try:
    set()
except:
    from sets import Set as set

import Cobalt.Logging, Cobalt.Util
from Cobalt.Data import Data, DataDict, ForeignData, ForeignDataDict
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ReservationError, DataCreationError, ComponentLookupError
import xmlrpclib

import Cobalt.SchedulerPolicies

logger = logging.getLogger("Cobalt.Components.scheduler")

SLOP_TIME = 180
DEFAULT_RESERVATION_POLICY = "default"

class Reservation (Data):
    
    """Cobalt scheduler reservation."""
    
    fields = Data.fields + [
        "tag", "name", "start", "duration", "cycle", "users", "partitions",
        "active", "queue", 
    ]
    
    required = ["name", "start", "duration"]
    
    def __init__ (self, spec):
        Data.__init__(self, spec)
        self.tag = spec.get("tag", "reservation")
        self.cycle = spec.get("cycle")
        self.users = spec.get("users", "")
        self.createdQueue = False
        self.partitions = spec.get("partitions", "")
        self.name = spec['name']
        self.start = spec['start']
        self.queue = spec.get("queue", "R.%s" % self.name)
        self.duration = spec.get("duration")
        
    def _get_active(self):
        return self.is_active()
    
    active = property(_get_active)
    
    def update (self, spec):
        if spec.has_key("users"):
            qm = ComponentProxy("queue-manager")
            try:
                qm.set_queues([{'name':self.queue,}], {'users':spec['users']})
            except ComponentLookupError:
                logger.error("unable to contact queue manager when updating reservation users")
                raise
        # try the above first -- if we can't contact the queue-manager, don't update the users
        Data.update(self, spec)

    
    def overlaps(self, partition, start, duration):
        '''check job overlap with reservations'''
        if start + duration < self.start:
            return False

        part_list = self.partitions.split(":")
        no_overlap = True
        for part_name in part_list:
            if part_name==partition.name or part_name in partition.children or part_name in partition.parents:
                no_overlap = False
                break
        if no_overlap:
            return False

        if self.cycle and duration >= self.cycle:
            return True

        my_stop = self.start + self.duration
        if self.start <= start < my_stop:
            # Job starts within reservation 
            return True
        elif self.start <= (start + duration) < my_stop:
            # Job ends within reservation 
            return True
        elif start < self.start and (start + duration) >= my_stop:
            # Job starts before and ends after reservation
            return True
        if not self.cycle:
            return False
        
        # 3 cases, front, back and complete coverage of a cycle
        cstart = (start - self.start) % self.cycle
        cend = (start + duration - self.start) % self.cycle
        if cstart < self.duration:
            return True
        if cend < self.duration:
            return True
        if cstart > cend:
            return True
        
        return False

    def job_within_reservation(self, job):
        if not self.is_active():
            return False
        
        if job.queue == self.queue:
            job_end = time.time() + 60 * float(job.walltime) + SLOP_TIME
            if not self.cycle:
                res_end = self.start + self.duration
                if job_end < res_end:
                    return True
                else:
                    return False
            else:
                if 60 * float(job.walltime) + SLOP_TIME > self.duration:
                    return False
                
                relative_start = (time.time() - self.start) % self.cycle
                relative_end = relative_start + 60 * float(job.walltime) + SLOP_TIME
                if relative_end < self.duration:
                    return True
                else:
                    return False
        else:
            return False

    
    def is_active(self, stime=False):
        if not stime:
            stime = time.time()
            
        if stime < self.start:
            return False
        
        if self.cycle:
            now = (stime - self.start) % self.cycle
        else:
            now = stime - self.start    
        if now <= self.duration:
            return True

    def is_over(self):
        # reservations with a cycle time are never "over"
        if self.cycle:
            return False
        
        stime = time.time()
        if (self.start + self.duration) <= stime:
            return True
        else:
            return False
        
        

class ReservationDict (DataDict):
    
    item_cls = Reservation
    key = "name"
    
    def q_add (self, *args, **kwargs):
        qm = ComponentProxy("queue-manager")
        try:
            queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        except ComponentLookupError:
            logger.error("unable to contact queue manager when adding reservation")
            raise
        
        try:
            reservations = Cobalt.Data.DataDict.q_add(self, *args, **kwargs)
        except KeyError, e:
            raise ReservationError("Error: a reservation named %s already exists" % e)
                
        for reservation in reservations:
            if reservation.queue not in queues:
                try:
                    print "adding reservation using policy:", DEFAULT_RESERVATION_POLICY
                    qm.add_queues([{'tag': "queue", 'name':reservation.queue, 'state':"running",
                                    'users':reservation.users, 'policy':DEFAULT_RESERVATION_POLICY}])
                except Exception, e:
                    logger.error("unable to add reservation queue %s (%s)" % \
                                 (reservation.queue, e))
                else:
                    reservation.createdQueue = True
                    logger.info("added reservation queue %s" % (reservation.queue))
            else:
                try:
                    qm.set_queues([{'name':reservation.queue}],
                                  {'state':"running", 'users':reservation.users})
                except Exception, e:
                    logger.error("unable to update reservation queue %s (%s)" % \
                                 (reservation.queue, e))
                else:
                    logger.info("updated reservation queue %s" % reservation.queue)
    
        return reservations
        
    def q_del (self, *args, **kwargs):
        reservations = Cobalt.Data.DataDict.q_del(self, *args, **kwargs)
        qm = ComponentProxy('queue-manager')
        queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        spec = [{'name': reservation.queue} for reservation in reservations \
                if reservation.createdQueue and reservation.queue in queues and \
                not self.q_get([{'queue':reservation.queue}])]
        try:
            qm.set_queues(spec, {'state':"dead"})
        except Exception, e:
            logger.error("problem disabling reservation queue (%s)" % e)
        return reservations

class Partition (ForeignData):
    """Partitions are allocatable chunks of the machine"""
    
    fields = ForeignData.fields + [
        "queue", "name", "node_card_names", "scheduled", "functional", "size", "parents", "children", "state"
    ]

    def __init__(self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.queue = spec.pop("queue", None)
        self.name = spec.pop("name", None)
        self.node_card_names = spec.pop("node_card_names", None)
        self.scheduled = spec.pop("scheduled", None)
        self.functional = spec.pop("functional", None)
        self.size = spec.pop("size", None)
        self.parents = spec.pop("parents", None)
        self.children = spec.pop("children", None)
        self.state = spec.pop("state", None)
        
        
    def _can_run (self, job):
        """Check that job can run on partition with reservation constraints"""
        return self.scheduled and self.functional

class PartitionDict (ForeignDataDict):
    item_cls = Partition
    __oserror__ = Cobalt.Util.FailureMode("System Connection (partition)")
    __failname__ = 'System Connection'
    __function__ = ComponentProxy("system").get_partitions
    __fields__ = ['name', 'queue', 'node_card_names', 'scheduled', 'functional', 'size', 'parents', 'children', 'state']
    key = 'name'

    def can_run(self, target_partition, job):
        if target_partition.state != "idle":
            return False
        desired = sys.maxint
        for part in self.itervalues():
            if not part.functional:
                if target_partition.name in part.children or target_partition.name in part.parents:
                    return False
            else:
                if part.scheduled:
                    if int(job.nodes) <= int(part.size) < desired:
                        desired = int(part.size)
        return target_partition._can_run(job) and int(target_partition.size) == desired
                

class Job (ForeignData):
    
    """A cobalt job."""
    
    fields = ForeignData.fields + [
        "nodes", "location", "jobid", "state", "index", "walltime", "queue", "user", "submittime", 
        "system_state", "starttime", "project",
    ]
    
    def __init__ (self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.partition = "none"
        self.nodes = spec.pop("nodes", None)
        self.location = spec.pop("location", None)
        self.jobid = spec.pop("jobid", None)
        self.state = spec.pop("state", None)
        self.index = spec.pop("index", None)
        self.walltime = spec.pop("walltime", None)
        self.queue = spec.pop("queue", None)
        self.user = spec.pop("user", None)
        self.submittime = spec.pop("submittime", None)
        self.system_state = spec.pop("system_state", None)
        self.starttime = spec.pop("starttime", None)
        self.project = spec.pop("project", None)
        
        logger.info("Job %s/%s: Found job" % (self.jobid, self.user))

class JobDict(ForeignDataDict):
    item_cls = Job
    key = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (job)")
    __function__ = ComponentProxy("queue-manager").get_jobs
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user', 'submittime', 'system_state', 
                  'starttime', 'project' ]

class Queue(ForeignData):
    fields = ForeignData.fields + [
        "name", "state", "policy", "priority"
    ]

    def __init__(self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.name = spec.pop("name", None)
        self.state = spec.pop("state", None)
        self.policy = spec.pop("policy", None)
        self.priority = spec.pop("priority", 0)
        
        

    def LoadPolicy(self):
        '''Instantiate queue policy modules upon demand'''
        if self.policy not in Cobalt.SchedulerPolicies.names:
            logger.error("Cannot load policy %s for queue %s" % \
                         (self.policy, self.name))
        else:
            pclass = Cobalt.SchedulerPolicies.names[self.policy]
            self.policy = pclass(self.name)


class QueueDict(ForeignDataDict):
    item_cls = Queue
    key = 'name'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (queue)")
    __function__ = ComponentProxy("queue-manager").get_queues
    __fields__ = ['name', 'state', 'policy', 'priority']

#    def Sync(self):
#        qp = [(q.name, q.policy) for q in self.itervalues()]
#        Cobalt.Data.ForeignDataDict.Sync(self)
#        [q.LoadPolicy() for q in self.itervalues() \
#         if (q.name, q.policy) not in qp]


class BGSched (Component):
    
    implementation = "bgsched"
    name = "scheduler"
    logger = logging.getLogger("Cobalt.Components.scheduler")
    
    _configfields = ['utility_file']
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgsched'):
        print '''"bgsched" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['bgsched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file [bgsched] section: %s" % (" ".join(mfields))
        sys.exit(1)
    if config.get("default_reservation_policy"):
        global DEFAULT_RESERVATION_POLICY
        DEFAULT_RESERVATION_POLICY = config.get("default_reservation_policy")
    
    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.reservations = ReservationDict()
        self.queues = QueueDict()
        self.jobs = JobDict()
        self.partitions = PartitionDict()
        self.assigned_partitions = {}
        self.sched_info = {}
        self.started_jobs = {}
        self.sync_state = Cobalt.Util.FailureMode("Foreign Data Sync")
        self.active = True
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}
    
    def __getstate__(self):
        return {'reservations':self.reservations, 'version':1,
                'active':self.active}
    
    def __setstate__(self, state):
        self.reservations = state['reservations']
        if 'active' in state:
            self.active = state['active']
        else:
            self.active = True
        
        self.queues = QueueDict()
        self.jobs = JobDict()
        self.partitions = PartitionDict()
        self.assigned_partitions = {}
        self.sched_info = {}
        self.started_jobs = {}
        self.sync_state = Cobalt.Util.FailureMode("Foreign Data Sync")
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}

    # order the jobs with biggest utility first
    def utilitycmp(self, tuple1, tuple2):
        return -cmp(tuple1[1], tuple2[1])
    
    # order the jobs with the most walltime first
    def walltimecmp(self, tuple1, tuple2):
        return -cmp(float(tuple1[0].walltime), float(tuple2[0].walltime))
    
    def prioritycmp(self, job1, job2):
        """Compare 2 jobs first using queue priority and then first-in, first-out."""
        
        val = cmp(self.queues[job1.queue].priority, self.queues[job2.queue].priority)
        if val == 0:
            return self.fifocmp(job1, job2)
        else:
            # we want the higher priority first
            return -val
        
    def fifocmp (self, job1, job2):
        """Compare 2 jobs for first-in, first-out."""
        
        def fifo_value (job):
            if job.index is not None:
                return int(job.index)
            else:
                return job.jobid
            
        # Implement some simple variations on FIFO scheduling
        # within a particular queue, based on queue policy
        fifoval = cmp(fifo_value(job1), fifo_value(job2))
        if(job1.queue == job2.queue):
            qpolicy = self.queues[job1.queue].policy
            sizeval = cmp(int(job1.nodes), int(job2.nodes))
            wtimeval = cmp(int(job1.walltime), int(job2.walltime))
            if(qpolicy == 'largest-first' and sizeval):
                return -sizeval
            elif(qpolicy == 'smallest-first' and sizeval):
                return sizeval
            elif(qpolicy == 'longest-first' and wtimeval):
                return -wtimeval
            elif(qpolicy == 'shortest-first' and wtimeval):
                return wtimeval
            else:
                return fifoval
        else:
            return fifoval

        return cmp(fifo_value(job1), fifo_value(job2))

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    def add_reservations (self, specs):
        return self.reservations.q_add(specs)
    add_reservations = exposed(query(add_reservations))

    def del_reservations (self, specs):
        return self.reservations.q_del(specs)
    del_reservations = exposed(query(del_reservations))

    def get_reservations (self, specs):
        return self.reservations.q_get(specs)
    get_reservations = exposed(query(get_reservations))

    def set_reservations(self, specs, updates):
        def _set_reservations(res, newattr):
            res.update(newattr)
        return self.reservations.q_get(specs, _set_reservations, updates)
    set_reservations = exposed(query(set_reservations))

    def check_reservations(self):
        ret = ""
        reservations = self.reservations.values()
        for i in range(len(reservations)):
            for j in range(i+1, len(reservations)):
                # if at least one reservation is cyclic, we want *that* reservation to be the one getting its overlaps method called
                if reservations[i].cycle is not None:
                    res1 = reservations[i]
                    res2 = reservations[j]
                else:
                    res1 = reservations[j]
                    res2 = reservations[i]
                for p in res2.partitions.split(":"):
                    # we substract a little bit because the overlaps method isn't really meant to do this
                    # it will report warnings when one reservation starts at the same time another ends
                    if res1.overlaps(self.partitions[p], res2.start, res2.duration - 0.00001):
                        ret += "Warning: reservation '%s' overlaps reservation '%s'\n" % (res1.name, res2.name)

        return ret
    check_reservations = exposed(check_reservations)

    def sync_data(self):
        for item in [self.jobs, self.queues, self.partitions]:
            try:
                item.Sync()
            except (ComponentLookupError, xmlrpclib.Fault):
                # the ForeignDataDicts already include FailureMode stuff
                pass
    sync_data = automatic(sync_data)

    def _run_reservation_jobs (self, available_partitions, res_queues):
        temp_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue} for queue in res_queues])
        active_jobs = []
        for j in temp_jobs:
            if not self.started_jobs.has_key(j.jobid):
                active_jobs.append(j)

        utility_scores = self._compute_utility_scores(active_jobs, time.time())
        if not utility_scores:
            # if we've got no utility scores, either there were no active_jobs
            # or an error occurred -- either way, give up now
            return
        utility_scores.sort(self.utilitycmp)

        # this is the bit that actually picks which job to run
        for tup in utility_scores:
            job = tup[0]
            if tup[1] < utility_scores[0][2]:
                self.sched_info[utility_scores[0][0].jobid] += "\n     wants to block other jobs from starting"
                # this break is meant to take us to the explicit back filling mumbo-jumbo
                break
            
            best_score = sys.maxint
            best_partition = None
            
            for cur_res in self.reservations.values():
                if job.queue == cur_res.queue:
                    if not cur_res.job_within_reservation(job):
                        if cur_res.is_active():
                            self.sched_info[job.jobid] = "not enough time in reservation '%s' for job to finish" % cur_res.name
                        else:
                            self.sched_info[job.jobid] = "reservation '%s' is not active yet" % cur_res.name
                        continue
                    
                    for partition in available_partitions:
                        # check if the current partition is linked to the job's reservation
                        part_in_res = False
                        for part_name in cur_res.partitions.split(":"):
                            if not part_name in self.partitions:
                                self.logger.error("reservation '%s' refers to non-existant partition '%s'" % (cur_res.name, part_name))
                                continue
                            if not (partition.name==self.partitions[part_name].name or partition.name in self.partitions[part_name].children):
                                continue
                            # if we got here, then the partition is part of the reservation
                            part_in_res = True
                        
                        if not part_in_res:
                            continue
                            
                        if not self.partitions.can_run(partition, job):
                            continue
                        
                        # let's check the impact on partitions that would become blocked
                        score = 0
                        for p in partition.parents:
                            if self.partitions[p].state == "idle" and self.partitions[p].scheduled:
                                score += 1
                        
                        # the lower the score, the fewer new partitions will be blocked by this selection
                        if score < best_score:
                            best_score = score
                            best_partition = partition        
        
                    if best_partition is not None:
                        self._start_job(job, best_partition)
                        return

    def _start_job(self, job, partition):
        cqm = ComponentProxy("queue-manager")
        
        try:
            self.logger.info("trying to start job %d on partition %s" % (job.jobid, partition.name))
            cqm.run_jobs([{'tag':"job", 'jobid':job.jobid}], [partition.name])
        except ComponentLookupError:
            self.logger.error("failed to connect to queue manager")
            return

        self.assigned_partitions[partition.name] = time.time()
        self.started_jobs[job.jobid] = time.time()

    def _find_best_partition(self, job, available_partitions):
        best_score = sys.maxint
        best_partition = None
        for partition in available_partitions:
            # check if the current partition is linked to the job's queue
            if job.queue not in partition.queue.split(':'):
                continue
                
            if self.partitions.can_run(partition, job):
                really_okay = True
                for res in self.reservations.itervalues():
                    # if the proposed job overlaps an active reservation, don't run it
                    if res.overlaps(partition, time.time(), 60 * float(job.walltime) + SLOP_TIME):
                        really_okay = False
                        self.sched_info[job.jobid] = "overlaps reservation '%s'" % res.name
                        break
                        
                if really_okay:
                    # let's check the impact on partitions that would become blocked
                    score = 0
                    for p in partition.parents:
                        if self.partitions[p].state == "idle" and self.partitions[p].scheduled:
                            score += 1
                    
                    # the lower the score, the fewer new partitions will be blocked by this selection
                    if score < best_score:
                        best_score = score
                        best_partition = partition        

        return best_partition

    def _compute_utility_scores (self, active_jobs, current_time):
        utility_scores = []
        if not self.builtin_utility_functions:
            self.define_builtin_utility_functions()
            
        if not self.user_utility_functions:
            self.define_user_utility_functions()
            
        for job in active_jobs:
            utility_name = self.queues[job.queue].policy
            args = {'queued_time':current_time - float(job.submittime), 
                    'wall_time': float(job.walltime), 
                    'size': float(job.nodes),
                    'user_name': job.user,
                    'project': job.project,
                    'queue_priority': int(self.queues[job.queue].priority),
                    'machine_size': 40 * 1024 * 4,
                    'jobid': int(job.jobid),
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
                self.logger.error("error while executing utility function '%s' named by queue '%s'" % (utility_name, job.queue), exc_info=True)
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
            
            if type(score) is not types.TupleType:
                score = (score, 0)
            
            self.sched_info[job.jobid] = str(score)    
            utility_scores.append( (job, ) + score)
        return utility_scores

    def schedule_jobs (self):
        '''look at the queued jobs, and decide which ones to start'''

        if not self.active:
            return
        # if we're missing information, don't bother trying to schedule jobs
        if not (self.partitions.__oserror__.status and self.queues.__oserror__.status and self.jobs.__oserror__.status):
            self.sync_state.Fail()
            return
        self.sync_state.Pass()
        
        # clean up the assigned_partitions cached data, and the started_jobs cached data
        now = time.time()
        for part_name in self.assigned_partitions.keys():
            if (now - self.assigned_partitions[part_name]) > 5*60:
                del self.assigned_partitions[part_name]
        
        for job_name in self.started_jobs.keys():
            if (now - self.started_jobs[job_name]) > 60:
                del self.started_jobs[job_name]

        # cleanup the sched_info information if a job is no longer listed as "active"
        self.sched_info = {}
        
        # cleanup any reservations which have expired
        for res in self.reservations.values():
            if res.is_over():
                self.logger.info("reservation %s has ended; removing" % res.name)
                self.reservations.q_del([{'name': res.name}])
                
        scriptm = ComponentProxy("script-manager")
        
        try:
            script_locations = [job['location'][0] for job in scriptm.get_jobs([{'location':"*"}])]
        except ComponentLookupError:
            self.logger.error("failed to connect to script manager")
            return

        for name in script_locations:
            # once the partition can be found from the script manager, the scheduler doesn't need to keep track of it
            if self.assigned_partitions.has_key(name):
                del self.assigned_partitions[name]
                
        available_partitions = []
        for partition in self.partitions.itervalues():
            okay_to_add = True

            if partition.state != "idle":
                # if the system component finally knows that the partition isn't idle, we don't need to keep
                # track of it any longer
                if self.assigned_partitions.has_key(partition.name):
                    del self.assigned_partitions[partition.name]
                continue
            
            if partition.name in self.assigned_partitions:
                continue
            
            if partition.name in script_locations:
                continue

            # walk the various lists of partitions and see if the current partition belongs to the parents or children of 
            # a partition which is in use
            for key in set(self.assigned_partitions.keys() + script_locations):
                if partition.name in self.partitions[key].parents or partition.name in self.partitions[key].children:
                    okay_to_add = False
                    break
            
            if okay_to_add:
                available_partitions.append(partition)
        

        active_queues = []
        spruce_queues = []
        res_queues = set()
        for item in self.reservations.q_get([{'queue':'*'}]):
            if self.queues.has_key(item.queue):
                if self.queues[item.queue].state == 'running':
                    res_queues.add(item.queue)

        for queue in self.queues.itervalues():
            if queue.name not in res_queues and queue.state == 'running':
                if queue.policy == "high_prio":
                    spruce_queues.append(queue)
                else:
                    active_queues.append(queue)
        
        # handle the reservation jobs that might be ready to go
        self._run_reservation_jobs(available_partitions, res_queues)

        # figure out stuff about queue equivalence classes
        equiv = []
        for part in self.partitions.itervalues():
            if part.functional and part.scheduled:
                found_a_match = False
                for e in equiv:
                    if e['data'].intersection(part.node_card_names):
                        e['queues'].update(part.queue.split(":"))
                        e['data'].update(part.node_card_names)
                        found_a_match = True
                        break
                if not found_a_match:
                    equiv.append( { 'queues': set(part.queue.split(":")), 'data': set(part.node_card_names) } ) 
            
        # print "equiv: ", 
        # print equiv

        
        for eq_class in equiv:
            temp_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue.name} for queue in active_queues if queue.name in eq_class['queues']])
            active_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid):
                    active_jobs.append(j)
    
            temp_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue.name} for queue in spruce_queues if queue.name in eq_class['queues']])
            spruce_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid):
                    spruce_jobs.append(j)
    
            # if there are any pending jobs in high_prio queues, those are the only ones that can start
            if spruce_jobs:
                active_jobs = spruce_jobs
    
            utility_scores = self._compute_utility_scores(active_jobs, now)
            if not utility_scores:
                # if we've got no utility scores, either there were no active_jobs
                # or an error occurred -- either way, go on to the next equivalence class
                continue
            utility_scores.sort(self.utilitycmp)
    
            # this is the bit that actually picks which job to run
            for tup in utility_scores:
                job = tup[0]
                if tup[1] < utility_scores[0][2]:
                    self.sched_info[utility_scores[0][0].jobid] += "\n     wants to block other jobs from starting"
                    # this break is meant to take us to the explicit back filling mumbo-jumbo
                    break
    
                best_partition = self._find_best_partition(job, available_partitions)
                if best_partition is not None:
                    self._start_job(job, best_partition)
                    return
    
            # oh mercy
            # time for some explicit backfilling
            temp_jobs = [job for job in self.jobs.q_get([{'system_state':"running"}]) if job.queue in eq_class['queues']]
            end_times = []
            for job in temp_jobs:
                end_time = float(job.starttime) + 60 * float(job.walltime)
                end_times.append(end_time)
            
            for cur_res in self.reservations.values():
                skip = True
                for p_name in cur_res.partitions.split(":"):
                    if eq_class['data'].intersection(self.partitions[p_name].node_card_names):
                        skip = False
                        break
                if skip:
                    continue
                        
                if not cur_res.cycle:
                    end_time = float(cur_res.start) + float(cur_res.duration)
                else:
                    done_after = float(cur_res.duration) - ((now - float(cur_res.start)) % float(cur_res.cycle))
                    if done_after < 0:
                        done_after += cur_res.cycle
                    end_time = now + done_after
                end_times.append(end_time)
    
            if end_times:
                # add on an extra 2 minutes so that some jobs with the same walltime can start together 
                cut_off = min(end_times) - now + 120
            else:
                # if nothing is running, we can't technically "back fill" and there's just nothing to run
                # so we should examine the next equivalence class of queues
                continue
    
            utility_scores.sort(self.walltimecmp)
            
            for tup in utility_scores:
                job = tup[0]
                if 60*float(job.walltime) > cut_off:
                    continue
    
                best_partition = self._find_best_partition(job, available_partitions)
                if best_partition is not None:
                    self._start_job(job, best_partition)
                    self.logger.info("backfilling job %s" % job.jobid)
                    return


    schedule_jobs = automatic(schedule_jobs)

    
    def get_sched_info(self):
        """Get information about why jobs aren't running."""
        ret = {}
        for k in self.sched_info:
            ret[str(k)] = self.sched_info[k]
        return ret
    get_sched_info = exposed(get_sched_info)

    def enable(self):
        """Enable scheduling"""
        self.active = True
    enable = exposed(enable)

    def disable(self):
        """Disable scheduling"""
        self.active = False
    disable = exposed(disable)

    def define_user_utility_functions(self):
        self.logger.info("building user utility functions")
        self.user_utility_functions.clear()
        filename = self.config.get("utility_file")
        try:
            f = open(filename)
        except:
            self.logger.error("Can't read utility function definitions from file %s" % self.config.get("utility_file"))
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
                    self.logger.error("Attempting to overwrite builtin utility function '%s'.  User version discarded." % thing.func_name)
                else:
                    self.user_utility_functions[thing.func_name] = thing
    define_user_utility_functions = exposed(define_user_utility_functions)
            
    def define_builtin_utility_functions(self):
        self.logger.info("building builtin utility functions")
        self.builtin_utility_functions.clear()
        
        # I think this duplicates cobalt's old scheduling policy
        # higher queue priorities win, with jobid being the tie breaker
        def default():
            val = queue_priority + (1 - 1/jobid)
            return (val, 0)
    
        def high_prio():
            val = queued_time
            return (val, 0)
    
        self.builtin_utility_functions["default"] = default