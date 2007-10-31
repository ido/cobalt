#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging
import math
import sys
import time
import Cobalt.Logging, Cobalt.Util

from Cobalt.Data import Data, ForeignData, ForeignDataDict
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

import Cobalt.SchedulerPolicies

logger = logging.getLogger('Cobalt.Components.BGSched')


class Reservation (Data):
    
    """Cobalt scheduler reservation."""
    
    fields = Data.fields.copy()
    fields.update(dict(
        tag = "reservation",
        name = None,
        start = None,
        duration = None,
        cycle = None,
        users = None,
        partitions = None,
    ))
    
    required_fields = ["name", "start", "duration"]
    
    def __init__ (self, *args, **kwargs):
        Data.__init__(self, *args, **kwargs)
        if self.partitions is None:
            self.partitions = []
        if self.users is None:
            self.users = []
    
    def overlaps(self, location, start, duration):
        '''check job overlap with reservations'''
        if start + duration < self.start:
            return False
        

        if self.cycle and duration >= self.cycle:
            return True

        my_stop = self.start + self.duration
        print "my_stop : " + `my_stop`
        if location is not None and location not in self.locations:
            print "here"
            return False
        if self.start <= start < my_stop:
            return True
        elif self.start <= (start + duration) < my_stop:
            return True
        if not self.cycle:
            return False
        
        # 3 cases, front, back and complete coverage of a cycle
        cstart = (start - self.start) % self.cycle
        cend = (start + duration - self.start) % self.cycle
        print "[%d, %d)" % (cstart, cend)
        if cstart < self.duration:
            return True
        if cend < self.duration:
            return True
        if cstart > cend:
            return True
        
        return False


class ReservationDict (Cobalt.Data.DataDict):
    
    item_cls = Reservation
    key = "name"
    
    def q_add (self, *args, **kwargs):
        reservations = Cobalt.Data.DataDict.q_add(self, *args, **kwargs)
        qm = ComponentProxy("queue-manager")
        queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        for reservation in reservations:
            reservation_queue = "R.%s" % reservation.name
            if reservation_queue not in queues:
                try:
                    qm.add_queues([{'name':reservation_queue, 'state':"running", 'users':reservation.users}])
                except Exception, e:
                    logger.error("unable to add reservation queue %s (%s)" % (reservation_queue, e))
                else:
                    logger.info("added reservation queue %s" % reservation_queue)
    
    def q_del (self, *args, **kwargs):
        reservations = Cobalt.Data.DataDict.q_del(self, *args, **kwargs)
        qm = ComponentProxy('queue-manager')
        queues = [spec['name'] for spec in cqm.GetQueues([{'name':"*"}])]
        for reservation in reservations:
            reservation_queue = "R.%s" % reservation.name
            if reservation_queue in queues:
                try:
                    qm.set_queues([{'name':reservation_queue}], {'state':"dead"})
                except Exception, e:
                    logger.error("problem disabling reservation queue (%s)" % e)
                else:
                    logger.info("reservation queue %s disabled" % reservation_queue)


class Partition (ForeignData):
    """Partitions are allocatable chunks of the machine"""
    
    fields = Data.fields.copy()
    fields.update(dict(
        queue = None,
        name = None,
        nodecards = None,
        scheduled = None,
        functional = None,
        size = None,
        parents = None,
        children = None,
    ))
    
    def CanRun (self, job):
        """Check that job can run on partition with reservation constraints"""
        basic = self.scheduled and self.functional
        queue = job.queue.startswith('R.') or \
                job.queue in self.queue.split(':')
        jsize = int(job.nodes) # should this be 'size' instead?
        psize = int(self.size)
        size = (psize >= jsize) and ((psize == 32) or (jsize > psize/2))
        if not (basic and size):
            return False
        return queue


class PartitionDict (ForeignDataDict):
    item_cls = Partition
    __failname__ = 'System Connection'
    __function__ = ComponentProxy("system").get_partitions
    __fields__ = ['name', 'queue', 'nodecards', 'scheduled', 'functional', 'size', 'parents', 'children']
    key = 'name'

    def GetOverlaps(self, partnames):
        ncs = []
        for part in partnames:
            [ncs.append(nc) for nc in part.nodecards if nc not in ncs]
        ret = []
        for part in self:
            if [nc for nc in part.nodecards if nc in ncs]:
                ret.append(part)
        return ret


class Job (ForeignData):
    
    """A cobalt job."""
    
    fields = Data.fields.copy()
    fields.update(dict(
        nodes = None,
        location = None,
        jobid = None,
        state = None,
        index = None,
        walltime = None,
        queue = None,
        user = None,
    ))
    
    def __init__ (self, spec):
        Cobalt.Data.ForeignData.__init__(self, spec)
        self.partition = "none"
        logger.info("Job %s/%s: Found job" % (self.jobid, self.user))

def fifocmp (job1, job2):
    """Compare 2 jobs for first-in, first-out."""
    
    def fifo_value (job):
        return job.index or job.id
    
    return cmp(fifo_value(job1), fifo_value(job2))


class JobDict(ForeignDataDict):
    item_cls = Job
    key = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection")
    __function__ = ComponentProxy("queue-manager").get_jobs
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user']

class Queue(ForeignData):
    fields = Data.fields.copy()
    fields.update(dict(
        name = None,
        state = None,
        policy = None,
    ))

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
    
    def add_reservations (self, specs):
        return self.reservations.q_add(specs)
    add_reservation = exposed(query(add_reservations))

    def del_reservations (self, specs):
        return self.reservations.q_del(specs)
    del_reservations = exposed(query(del_reservations))

    def get_reservations (self, specs):
        return self.reservations.q_get(specs)
    get_reservations = exposed(query(get_reservations))

    #def SetReservation(self, *args):
    #    return self.reservations.Get(*args,
    #                                 callback = \
    #                                 lambda r, na:r.update(na))
    #SetReservation = exposed(SetReservation)

    #def SyncData(self):
    #    for item in [self.jobs, self.queues, self.partitions]:
    #        item.Sync()
    #        if not item.__oserror__.status:
    #            self.logger.error(item.__class__.__name__ + " unable to sync")
    #SyncData = automatic(SyncData)

    def schedule_jobs (self):
        
        if not (self.partitions.__oserror__.status and self.queues.__oserror__.status and self.jobs.__oserror__.status):
            self.logger.error("foreign data scynchronization failed: disabling scheduling")
            return
        
        active_queues = []
        for queue in self.queues.itervalues():
            if queue.name.startswith("R."):
                if self.reservations.q_get([{'name':queue.name[2:]}]):
                    active_queues.append(queue)
            else:
                if queue.state == "running":
                    active_queues.append(queue)
        
        active_jobs = self.jobs.q_get([{'state':"queued", 'queue':queue.name} for queue in active_queues])
        
        #############################################
        # FIXME need to check reservation conflict
        #       somewhere in this function
        #############################################
        
        viable = active_jobs[:]
        viable.sort(fifocmp)
        potential = {}
        for job in viable[:]:
            tmp_list = [partition for partition in self.partitions.itervalues() if partition.CanRun(job)]
            
            if tmp_list:
                potential[job.jobid] = tmp_list
            else:
                viable.remove(job)
        
        for queue in self.queues.itervalues():
            q.policy.Prepare(viable, potential)
        
        placements = []
        for job in viable:
            # do something sensible when TidyPlacements yanked a job out from under us
            if not potential.has_key(job.jobid):
                continue
            queue = self.queues[job.queue]
            place = queue.policy.PlaceJob(job, potential)
            if place:
                del potential[job.jobid]
                self.TidyPlacements(potential, place[1])
                placements.append(place)
        
        self.run_jobs(placements)
    schedule_jobs = automatic(schedule_jobs)

    def TidyPlacements(self, potential, newlocation):
        '''Remove any potential spots that overlap with newlocation'''
        print "new location: %r" % newlocation
        print "   %r" % newlocation.parents
        print "   %r" % newlocation.children
        cleanup = []
        for job in potential.keys():
            for location in potential[job][:]:
                if location.name==newlocation.name or location.name in newlocation.parents or location.name in newlocation.children:
                    potential[job].remove(location)
            if not potential[job]:
                del potential[job]

#        for job in cleanup:
#            del potential[job]

    def run_jobs (self, placements):
        """Connect to cqm and run jobs."""
        
        try:
            cqm = ComponentProxy("queue-manager")
        except ComponentLookupError:
            self.logger.error("failed to connect to queue manager")
            return
        
        for placement in placements:
            job = placement[0]
            location = placement[1].name
            cqm.run_jobs([{'tag':"job", 'jobid':job.jobid}], [location])
