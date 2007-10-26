#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging, math, sys, time
import Cobalt.Logging, Cobalt.Util

from Cobalt.Data import Data, ForeignData, ForeignDataDict
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

import Cobalt.SchedulerPolicies

logger = logging.getLogger('Cobalt.Components.BGSched')

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

class Partition(ForeignData):
    '''Partitions are allocatable chunks of the machine'''
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

class PartitionDict(ForeignDataDict):
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

class Job(ForeignData):
    '''This class represents User Jobs'''
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

    def __init__(self, element):
        Cobalt.Data.ForeignData.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.jobid, self.user))

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

class BGSched(Component):
    '''This scheduler implements a fifo policy'''
    implementation = 'bgsched'
    name = 'scheduler'
    __statefields__ = ['reservations']
    __schedcycle__ = 10
    
    logger = logging.getLogger("Cobalt.Components.BGSched")


    def __init__(self, *args, **kwargs):
        self.jobs = JobDict()
        self.queues = QueueDict()
        self.reservations = ReservationSet()
        self.resources = PartitionDict()
        Component.__init__(self, *args, **kwargs)
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

#    def SetReservation(self, *args):
#        return self.reservations.Get(*args,
#                                     callback = \
#                                     lambda r, na:r.update(na))
#    SetReservation = exposed(SetReservation)

    def SyncData(self):
        for item in [self.jobs, self.queues, self.resources]:
            item.Sync()
            if not item.__oserror__.status:
                self.logger.error(item.__class__.__name__ + " unable to sync")
    SyncData = automatic(SyncData)

    def Schedule(self):
        # self queues contains queues
        if not (self.resources.__oserror__.status and self.queues.__oserror__.status and self.jobs.__oserror__.status):
            self.logger.error("foreign data scynchronization failed: disabling scheduling")
            return
        activeq = []
        for q in self.queues.itervalues():
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
        activej = [j for j in self.jobs.itervalues() if j.get('queue') in activeq \
                   and j.get('state') == 'queued']
        print "activej:", activej

        #############################################
        # FIXME need to check reservation conflict
        #       somewhere in this function
        #############################################
        
        viable = activej[:]
        viable.sort(fifocmp)
        potential = {}
        dead_to_me = []
        for job in viable[:]:
            tmp_list = []
            [tmp_list.append(partition) for partition \
             in self.resources.itervalues() if partition.CanRun(job)]
            
            if tmp_list:
                potential[job.jobid] = tmp_list
            else:
                viable.remove(job)
            
        placements = []
        # call all queue policies
        [q.policy.Prepare(viable, potential) for q in self.queues.itervalues()]
        # place all viable jobs
        for job in viable:
            # do something sensible when TidyPlacements yanked a job out from under us
            if not potential.has_key(job.jobid):
                continue
            QP = self.queues[job.get('queue')].policy
            place = QP.PlaceJob(job, potential)
            if place:
                # clean up that job placement
                del potential[job.jobid]
                # tidy other placements
                self.TidyPlacements(potential, place[1])
                placements.append(place)
        self.RunJobs(placements)
    Schedule = automatic(Schedule)

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

    def RunJobs(self, placements):
        '''Connect to cqm and run jobs'''
        # FIXME
        print "trying to run a job"
        print "    ", repr(placements)
        
        try:
            cqm = ComponentProxy("queue-manager")
        except ComponentLookupError:
            print >> sys.stderr, "Failed to connect to queue manager"
            sys.exit(1)
        
        for p in placements:
            job = p[0]
            location = p[1].name
            print "location --> " + location
            
            spec = {'tag':"job", 'jobid':job.jobid}
            cqm.run_jobs([spec], [location])
        
        

    
