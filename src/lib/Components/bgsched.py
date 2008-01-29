#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging
import time
try:
    set()
except:
    from sets import Set as set

import Cobalt.Logging, Cobalt.Util
from Cobalt.Data import Data, DataDict, ForeignData, ForeignDataDict, DataCreationError
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

import Cobalt.SchedulerPolicies

logger = logging.getLogger("Cobalt.Components.scheduler")


class Reservation (Data):
    
    """Cobalt scheduler reservation."""
    
    fields = Data.fields + [
        "tag", "name", "start", "duration", "cycle", "users", "partitions",
        "active", "queue", 
    ]
    
    required_fields = ["name", "start", "duration"]
    
    def __init__ (self, spec):
        Data.__init__(self, spec)
        self.tag = spec.get("tag", "reservation")
        self.duration = spec.get("duration")
        self.cycle = spec.get("cycle")
        self.users = spec.get("users", "")
        self.createdQueue = False
        self.partitions = spec.get("partitions", "")
        try:
            self.name = spec.get("name")
        except:
            raise DataCreationError("required key name missing")
        self.queue = spec.get("queue", "R.%s" % self.name)
        try:
            self.start = spec.get("start")
        except:
            raise DataCreationError("required key start missing")
        
    def _get_active(self):
        return self.is_active()
    
    active = property(_get_active)
    
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
            return True
        elif self.start <= (start + duration) < my_stop:
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
            job_end = time.time() + 60 * float(job.walltime)
            if not self.cycle:
                res_end = self.start + self.duration
                if job_end < res_end:
                    return True
                else:
                    return False
            else:
                if 60 * float(job.walltime) > self.duration:
                    return False
                
                if ((job_end - self.start) % self.cycle) < self.duration:
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

        reservations = Cobalt.Data.DataDict.q_add(self, *args, **kwargs)        
        for reservation in reservations:
            if reservation.queue not in queues:
                try:
                    qm.add_queues([{'name':reservation.queue, 'state':"running",
                                    'users':reservation.users}])
                except Exception, e:
                    logger.error("unable to add reservation queue %s (%s)" % \
                                 (reservation.queue, e))
                else:
                    logger.info("added reservation queue %s" % (reservation.queue))
            else:
                try:
                    qm.set_queues([{'name':reservation.queue}],
                                  {'state':"running", 'users':reservation.users})
                except Exception, e:
                    logger.error("unable to update reservation queue %s (%s)" % \
                                 (reservation.queue, e))
                else:
                    reservation.createdQueue = True
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
        "queue", "name", "nodecards", "scheduled", "functional", "size", "parents", "children", "state"
    ]

    def __init__(self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.queue = spec.pop("queue", None)
        self.name = spec.pop("name", None)
        self.nodecards = spec.pop("nodecards", None)
        self.scheduled = spec.pop("scheduled", None)
        self.functional = spec.pop("functional", None)
        self.size = spec.pop("size", None)
        self.parents = spec.pop("parents", None)
        self.children = spec.pop("children", None)
        self.state = spec.pop("state", None)
        
        
    def _can_run (self, job):
        """Check that job can run on partition with reservation constraints"""
        basic = self.scheduled and self.functional
        jsize = int(job.nodes) # should this be 'size' instead?
        psize = int(self.size)
        size = (psize >= jsize) and ((psize == 32) or (jsize > psize/2))
        if not (basic and size):
            return False
        else:
            return True


class PartitionDict (ForeignDataDict):
    item_cls = Partition
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (partition)")
    __failname__ = 'System Connection'
    __function__ = ComponentProxy("system").get_partitions
    __fields__ = ['name', 'queue', 'nodecards', 'scheduled', 'functional', 'size', 'parents', 'children', 'state']
    key = 'name'

    def can_run(self, target_partition, job):
        if target_partition.state != "idle":
            return False
        for part in self.itervalues():
            if not part.functional:
                if target_partition.name in part.children or target_partition.name in part.parents:
                    return False
        
        return target_partition._can_run(job)
                

class Job (ForeignData):
    
    """A cobalt job."""
    
    fields = ForeignData.fields + [
        "nodes", "location", "jobid", "state", "index", "walltime", "queue", "user",
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
        
        logger.info("Job %s/%s: Found job" % (self.jobid, self.user))

def fifocmp (job1, job2):
    """Compare 2 jobs for first-in, first-out."""
    
    def fifo_value (job):
        return job.index or job.jobid
    
    return cmp(fifo_value(job1), fifo_value(job2))


class JobDict(ForeignDataDict):
    item_cls = Job
    key = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (job)")
    __function__ = ComponentProxy("queue-manager").get_jobs
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user']

class Queue(ForeignData):
    fields = ForeignData.fields + [
        "name", "state", "policy"
    ]

    def __init__(self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.name = spec.pop("name", None)
        self.state = spec.pop("state", None)
        self.policy = spec.pop("policy", None)
        
        

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
    __fields__ = ['name', 'state', 'policy']

    def Sync(self):
        qp = [(q.name, q.policy) for q in self.itervalues()]
        Cobalt.Data.ForeignDataDict.Sync(self)
        [q.LoadPolicy() for q in self.itervalues() \
         if (q.name, q.policy) not in qp]


class BGSched (Component):
    
    implementation = "bgsched"
    name = "scheduler"
    logger = logging.getLogger("Cobalt.Components.scheduler")
    
    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.reservations = ReservationDict()
        self.queues = QueueDict()
        self.jobs = JobDict()
        self.partitions = PartitionDict()
        self.assigned_partitions = {}
        self.sched_info = {}
        self.started_jobs = {}
    
    def __getstate__(self):
        return {'reservations':self.reservations, 'version':1}
    
    def __setstate__(self, state):
        self.reservations = state['reservations']
        
        self.queues = QueueDict()
        self.jobs = JobDict()
        self.partitions = PartitionDict()
        self.assigned_partitions = {}
        self.sched_info = {}
        self.started_jobs = {}

        
    def save_me(self):
        Component.save(self, '/var/spool/cobalt/bgsched')
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

    #def SetReservation(self, *args):
    #    return self.reservations.Get(*args,
    #                                 callback = \
    #                                 lambda r, na:r.update(na))
    #SetReservation = exposed(SetReservation)

    def sync_data(self):
        for item in [self.jobs, self.queues, self.partitions]:
            try:
                item.Sync()
            except ComponentLookupError:
                # the ForeignDataDicts already include FailureMode stuff
                pass
    sync_data = automatic(sync_data)

    def _run_reservation_jobs (self, available_partitions, res_queues):
        temp_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue} for queue in res_queues])
        active_jobs = []
        for j in temp_jobs:
            if not self.started_jobs.has_key(j.jobid):
                active_jobs.append(j)

        active_jobs.sort(fifocmp)
            
        for job in active_jobs:
            cur_res = self.reservations[job.queue[2:]]
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
                
                # let's run this thing!
                self._start_job(job, partition)
                return


    def _start_job(self, job, partition):
        cqm = ComponentProxy("queue-manager")
        
        try:
            print "trying to start job %d on partition %s" % (job.jobid, partition.name)
            cqm.run_jobs([{'tag':"job", 'jobid':job.jobid}], [partition.name])
        except ComponentLookupError:
            self.logger.error("failed to connect to queue manager")
            return

        self.assigned_partitions[partition.name] = time.time()
        self.started_jobs[job.jobid] = time.time()

        

    def schedule_jobs (self):
        '''look at the queued jobs, and decide which ones to start'''
        
        # if we're missing information, don't bother trying to schedule jobs
        if not (self.partitions.__oserror__.status and self.queues.__oserror__.status and self.jobs.__oserror__.status):
            self.logger.error("foreign data scynchronization failed: disabling scheduling")
            return
        
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
        res_queues = set(item.queue for item \
                         in self.reservations.q_get([{'queue':'*'}]))
        for queue in self.queues.itervalues():
            if queue.name not in res_queues and queue.state == 'running':
                active_queues.append(queue)
        
        # handle the reservation jobs that might be ready to go
        self._run_reservation_jobs(available_partitions, res_queues)
        
        temp_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue.name} for queue in active_queues])
        active_jobs = []
        for j in temp_jobs:
            if not self.started_jobs.has_key(j.jobid):
                active_jobs.append(j)
                
        active_jobs.sort(fifocmp)
        
        # this is the bit that actually picks which job to run
        for job in active_jobs:
            for partition in available_partitions:
                # check if the current partition is linked to the job's queue
                if job.queue not in partition.queue.split(':'):
                    continue
                    
                if self.partitions.can_run(partition, job):
                    really_okay = True
                    for res in self.reservations.itervalues():
                        # if the proposed job overlaps an active reservation, don't run it
                        if res.overlaps(partition, time.time(), 60 * float(job.walltime)):
                            really_okay = False
                            self.sched_info[job.jobid] = "overlaps reservation '%s'" % res.name
                            break
                            
                    if really_okay:
                        # let's run this thing!
                        self._start_job(job, partition)
                        return

    schedule_jobs = automatic(schedule_jobs)

    
    def get_sched_info(self):
        """Get information about why jobs aren't running."""
        ret = {}
        for k in self.sched_info:
            ret[str(k)] = self.sched_info[k]
        return ret
    get_sched_info = exposed(get_sched_info)
