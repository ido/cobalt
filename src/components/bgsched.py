#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import copy, logging, sys, time, xmlrpclib, ConfigParser
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

logger = logging.getLogger('bgsched')

comm = Cobalt.Proxy.CommDict()

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

class Reservation(Cobalt.Data.Data):
    '''Reservation\nHas attributes:\nname, start, stop, cycle, users, resources'''
    def Overlaps(self, location, start, duration):
        '''check job overlap with reservations'''
        if location not in self.get('locations'):
            return False
        if self.get('start') <= start <= self.get('stop'):
            return True
        elif self.get('start') <= (start + duration) <= self.get('stop'):
            return True
        if self.get('cycle') == 0:
            return False
        # 3 cases, front, back and complete coverage of a cycle
        cstart = math.floor((start - self.get('start')) / self.get('cycle'))
        if cstart <= start <= (cstart + self.get('duration')):
            return True
        cend = math.floor(((start + duration) - self.get('start')) / self.get('cycle'))
        if cend <= (start + duration) <= (cend + self.get('duration')):
            return True
        if duration >= self.get('cycle'):
            return True
        return False

    def IsActive(self, stime=False):
        if not stime:
            stime = time.time()
        if self.get('start') <= stime <= self.get('stop'):
            return True

    def FilterPlacements(self, placements, resources):
        '''Filter placements not allowed by reservation'''
        overlaps = resources.GetOverlaps(self.get('location'))
        now = time.time()
        # filter overlapping jobs not in reservation
        for job in placements:
            if job.get('queue').startswith("R.%s" % self.get("name")):
                if job.get('user') not in self.get('users'):
                    del placements[job]
                    continue
                placements[job] = [location for location in \
                                   placements[job] if location in \
                                   self.get('location')]
            for location in placements[job][:]:
                if location in overlaps:
                    if self.Overlaps(location, now,
                                     job.get('duration')):
                        placements[job].remove(location)
        if not self.IsActive():
            # filter jobs in Rqueue if not active
            if "R.%s" % self.get('name') in placements.keys():
                del placements["R.%" % self.get('name')]

class ReservationSet(Cobalt.Data.DataSet):
    __object__ = Reservation

    def CreateRQueue(self, reserv):
        queues = comm['qm'].GetQueues([{'tag':'queue', 'name':'*'}])
        qnames = [q['name'] for q in queues]
        if "R.%s" % reserv.get('name') not in qnames:
            logger.info("Adding reservation queue R.%s" % \
                        (reserv.get('name')))
            spec = [{'tag':'queue', 'name': 'R.%s' % \
                     (reserv.get('name'))}]
            attrs = {'state':'running', 'users': reserv.get('users')}
                try:
                    comm['qm'].AddQueue(spec)
                    comm['qm'].SetQueues(spec, attrs)
                except Exception, e:
                    logger.error("Queue setup for %s failed: %s" \
                                 % ("R.%s" % reserv.get('name'), e))

    def DeleteRQueue(self, reserv):
        queues = comm['qm'].GetQueues([{'tag':'queue', 'name':'*'}])
        qnames = [q['name'] for q in queues]
        rqn = "R.%s" % reserv.get("name")
        if rqn in qnames:
            logger.info("Disabling Rqueue %s" % (qn))
            try:
                response = comm['qm'].SetQueues([{'tag':'queue',
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
        basic = self.get('scheduled') and self.get('functional')
        queue = job.get('queue').startswith('R.') or \
                job.get('queue') in self.get('queue').split(':')
        jsize = int(job.get('nodes')) # should this be 'size' instead?
        psize = int(self.get('size'))
        size = (psize >= jsize) and ((psize == 32) or (jsize > psize/2))
        if not (basic and size):
            return False
        return queue

class PartitionSet(Cobalt.Data.DataSet):
    __object__ = Partition
    __failname__ = 'System Connection'
    __osource__ = ('system', 'GetBlah', ['name', 'queue', 'nodecards'])
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
        ForeignData.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.get('jobid'),
                                                  self.get('user')))

class JobSet(Cobalt.Data.ForeignDataSet):
    __object__ = Job
    __unique__ = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection")
    __osource__ = ('qm', 'GetJobs',
                   ['nodes', 'location', 'jobid', 'state', 'index',
                    'walltime', 'queue', 'user'])

    def Run(self, jobid, location):
        # FIXME implement
        pass

class Queue(Cobalt.Data.ForeignData):
    pass

class QueueSet(Cobalt.Data.ForeignDataSet):
    __object__ = Queue
    __unique__ = 'name'
    __osource__ = ('qm', 'GetQueues', ['name', 'status', 'policy']

class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched'
    __name__ = 'scheduler'
    __statefields__ = ['reservations']
    __schedcycle__ = 10
    async_funcs = ['assert_location', 'RunQueue',
                   'RemoveOldReservations', 'ResQueueSync']

    def __init__(self, setup):
        self.jobs = JobSet()
        self.queues = QueueSet()
        self.reservations = ReservationSet()
        self.resources = PartitionSet()
        Cobalt.Component.Component.__init__(self, setup)
        self.executed = []
        self.lastrun = 0
        self.register_function(self.reservations.Add, "AddReservation")
        self.register_function(self.reservations.Del, "DelReservation")
        self.register_function(
            lambda a,d,u: \
            self.reservations.Get(d, lambda r, na:r.update(na), u), 
            "SetReservation")

    def SyncData(self):
        for item in [self.resources, self.queues, self.jobs]:
            item.Sync()

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
        # need to perform search
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

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arguments) = getopt(sys.argv[1:], 'C:dD:t', ['nodb2'])
    except GetoptError, msg:
        print "%s\nUsage:\nbgsched.py [-t] [-C configfile] [-d] [-D <pidfile>] [--nodb2]" % (msg)
        raise SystemExit, 1
    try:
        daemon = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        daemon = False
    if len([x for x in opts if x[0] == '-d']):
        dlevel = logging.DEBUG
    else:
        dlevel = logging.INFO
    Cobalt.Logging.setup_logging('bgsched', level=dlevel)
    server = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    server.serve_forever()
    

