#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging, math, sys, time
import Cobalt.Logging, Cobalt.Util

from Cobalt.Data import Data, DataList
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

import Cobalt.SchedulerPolicies

logger = logging.getLogger('bgsched')

def lazy_component_proxy (component_name, method_name):
    def call_method ():
        component = Cobalt.Proxy.ComponentProxy(component_name)
        method = getattr(component, method_name)
        return method()
    return call_method

def fifocmp(job1, job2):
    '''Compare 2 jobs for fifo mode'''
    if job1.get('index', False):
        j1 = int(job1.get('index'))
    else:
        j1 = int(job1.get('jobid'))
    if job2.get('index', False):
        j2 = int(job2.get('index'))
    else:
        j2 = int(job2.get('jobid'))
    return cmp(j1, j2)

class Reservation(Data):
    '''Reservation\nHas attributes:\nname, start, duration, cycle, users, locations'''
    fields = Data.fields.copy()
    fields.update(dict(
        tag = "reservation",
        name = None,
        start = None,
        duration = None,
        cycle = None,
        users = None,
        locations = None,
    ))
    def overlaps(self, location, start, duration):
        '''check job overlap with reservations'''
        if duration > self.cycle:
            return True

        my_stop = self.start + self.duration
        if location not in self.locations:
            return False
        if self.start <= start <= my_stop:
            return True
        elif self.start <= (start + duration) <= my_stop:
            return True
        if self.cycle == 0:
            return False
        
        # 3 cases, front, back and complete coverage of a cycle
        cstart = (start - self.start) % self.cycle
        cend = (start + duration - self.start) % self.cycle
        if cstart <= self.duration:
            return True
        if cend <= self.duration:
            return True
        if cstart > cend:
            return True
        
        return False

    def IsActive(self, stime=False):
        if not stime:
            stime = time.time()
        now = (stime - self.start) % self.cycle    
        if now <= self.duration:
            return True

    def FilterPlacements(self, placements, resources):
        '''Filter placements not allowed by reservation'''
        overlaps = resources.GetOverlaps(self.location)
        now = time.time()
        # filter overlapping jobs not in reservation
        for job in placements:
            if job.queue.startswith("R.%s" % self.name):
                if job.user not in self.users:
                    del placements[job]
                    continue
                placements[job] = [location for location in \
                                   placements[job] if location in \
                                   self.location]
            for location in placements[job][:]:
                if location in overlaps:
                    if self.Overlaps(location, now,
                                     job.get('duration')):
                        placements[job].remove(location)
        if not self.IsActive():
            # filter jobs in Rqueue if not active
            if "R.%s" % self.name in placements.keys():
                del placements["R.%" % self.name]

class ReservationSet(Cobalt.Data.DataSet):
    __object__ = Reservation

    def CreateRQueue(self, reserv):
        cqm = Cobalt.Proxy.ComponentProxy('queue-manager')
        queues = cqm.GetQueues([{'tag':'queue', 'name':'*'}])
        qnames = [q['name'] for q in queues]
        if "R.%s" % reserv.get('name') not in qnames:
            logger.info("Adding reservation queue R.%s" % \
                        (reserv.get('name')))
            spec = [{'tag':'queue', 'name': 'R.%s' % \
                     (reserv.get('name'))}]
            attrs = {'state':'running', 'users': reserv.get('users')}
            try:
                cqm.AddQueue(spec)
                cqm.SetQueues(spec, attrs)
            except Exception, e:
                logger.error("Queue setup for %s failed: %s" \
                             % ("R.%s" % reserv.get('name'), e))

    def DeleteRQueue(self, reserv):
        cqm = Cobalt.Proxy.ComponentProxy('queue-manager')
        queues = cqm.GetQueues([{'tag':'queue', 'name':'*'}])
        qnames = [q['name'] for q in queues]
        rqn = "R.%s" % reserv.get("name")
        if rqn in qnames:
            logger.info("Disabling Rqueue %s" % (rqn))
            try:
                response = cqm.SetQueues([{'tag':'queue',
                                           'name':rqn}],
                                         {'state':'dead'})
            except Exception, e:
                logger.error("Disable request failed: %s" % e)

    def Add(self, cdata, callback=None, cargs={}):
        Cobalt.Data.DataSet.Add(self, cdata, self.CreateRQueue, cargs)
        
    def Del(self, cdata, callback=None, cargs={}):
        Cobalt.Data.DataSet.Del(self, cdata, self.DeleteRQueue, cargs)

class Partition(Cobalt.Data.ForeignData):
    '''Partitions are allocatable chunks of the machine'''
    def CanRun(self, job):
        '''Check that job can run on partition with reservation constraints'''
        basic = self.scheduled and self.functional
        queue = job.queue.startswith('R.') or \
                job.queue in self.queue.split(':')
        jsize = int(job.nodes) # should this be 'size' instead?
        psize = int(self.size)
        size = (psize >= jsize) and ((psize == 32) or (jsize > psize/2))
        if not (basic and size):
            return False
        return queue

class PartitionSet(Cobalt.Data.ForeignDataSet):
    __object__ = Partition
    __failname__ = 'System Connection'
    __function__ = lazy_component_proxy('system', 'GetBlah')
    __fields__ = ['name', 'queue', 'nodecards']
    __unique__ = 'name'

    def GetOverlaps(self, partnames):
        ncs = []
        for part in partnames:
            [ncs.append(nc) for nc in part.nodecards if nc not in ncs]
        ret = []
        for part in self:
            if [nc for nc in part.nodecards if nc in ncs]:
                ret.append(part)
        return ret

class Job(Cobalt.Data.ForeignData):
    '''This class represents User Jobs'''
    def __init__(self, element):
        Cobalt.Data.ForeignData.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.jobid, self.user))

class JobSet(Cobalt.Data.ForeignDataSet):
    __object__ = Job
    __unique__ = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection")
    __function__ = lazy_component_proxy('queue-manager', 'GetJobs')
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user']

class Queue(Cobalt.Data.ForeignData):
    def LoadPolicy(self):
        '''Instantiate queue policy modules upon demand'''
        if self.policy not in Cobalt.SchedulerPolicies.names:
            logger.error("Cannot load policy %s for queue %s" % \
                         (self.policy, self.name))
        else:
            pclass = Cobalt.SchedulerPolicies.names[self.policy]
            self.policy = pclass()


class QueueSet(Cobalt.Data.ForeignDataSet):
    __object__ = Queue
    __unique__ = 'name'
    __function__ = lazy_component_proxy('queue-manager', 'GetQueues')
    __fields__ = ['name', 'status', 'policy']

    def Sync(self):
        qp = [(q.get('name'), q.get('policy')) for q in self]
        Cobalt.Data.ForeignDataSet.Sync()
        [q.LoadPolicy() for q in self \
         if (q.get('name'), q.get('policy')) not in qp]

class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched'
    __name__ = 'scheduler'
    __statefields__ = ['reservations']
    __schedcycle__ = 10

    def __init__(self, setup):
        self.jobs = JobSet()
        self.queues = QueueSet()
        self.reservations = ReservationSet()
        self.resources = PartitionSet()
        Cobalt.Component.Component.__init__(self, setup)
        self.executed = []
        self.lastrun = 0

    def AddReservation(self, *args):
        return self.reservations.Add(*args)
    AddReservation = exposed(AddReservation)

    def DelReservation(self, *args):
        return self.reservations.Del(*args)
    DelReservation = exposed(DelReservation)

    def GetReservation(self, *args):
        return self.reservations.Get(*args)
    GetReservation = exposed(GetReservation)

    def SetReservation(self, *args):
        return self.reservations.Get(*args,
                                     callback = \
                                     lambda r, na:r.update(na))
    SetReservation = exposed(SetReservation)

    def SyncData(self):
        for item in [self.resources, self.queues, self.jobs]:
            item.Sync()
    SyncData = automatic(SyncData)

    def Schedule(self):
        # self queues contains queues
        activeq = []
        for q in self.queues:
            if q.get('name').startswith('R.'):
                if True in \
                   [rm.Active() for rm in \
                    self.reservations.Match({'name':q.get('name')[2:]})]:
                    activeq.append(q.get('name'))
            else:
                if q.get('state') == 'running':
                    activeq.append(q.get('name'))
        print "activeq:", activeq
        # self.jobs contains jobs
        activej = [j for j in self.jobs if j.get('queue') in activeq \
                   and j.get('state') == 'queued']
        print "activej:", activej
        potential = {}
        # FIXME need to perform search
        # need to check reservation conflict
        # return self.ImplementPolicy(potential, depinfo)
        viable = []
        [viable.extend(queue.keys()) for queue in potential.values()]
        viable.sort(fifocmp)
        potential = {}
        for job in viable:
            potential[job] = []
            [potential[job].append(partition) for partition \
             in self.resources if partition.CanRun(job)]

        placements = []
        # call all queue policies
        [q.policy.Prepare(viable, potential) for q in self.queues]
        # place all viable jobs
        for job in viable:
            QP = self.queues[job.get('queue')].policy
            place = QP.PlaceJob(job, potential)
            if place:
                # clean up that job placement
                del potential[job.get('queue')][job.get('jobid')]
                # tidy other placements
                self.TidyPlacements(potential, place[1])
                placements.append(place)
        self.RunJobs(placements)
    Schedule = automatic(Schedule)

    def TidyPlacements(self, potential, newlocation):
        '''Remove any potential spots that overlap with newlocation'''
        nodecards = [res for res in self.resources \
                     if res.get('name') == newlocation][0].get('nodecards')
        overlap = [res.get('name') for res in self.resources \
                   if [nc for nc in res.get('nodecards') \
                       if nc in nodecards]]
        for queue in potential:
            for job, locations in queue.iteritems():
                [locations.remove(location) for location in locations \
                 if location in overlap]
                if not locations:
                    del queue[job]

    def RunJobs(self, placements):
        '''Connect to cqm and run jobs'''
        # FIXME
        pass

    
