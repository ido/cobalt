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

class FailureMode(object):
    '''FailureModes are used to report (and supress) errors appropriately
    call Pass() on success and Fail() on error'''
    def __init__(self, name):
        self.name = name
        self.status = True

    def Pass(self):
        '''Check if status was previously failure and report OK status if needed'''
        if not self.status:
            logger.error("Failure %s cleared" % (self.name))
            self.status = True

    def Fail(self):
        '''Check if status was previously success and report failed status if needed'''
        if self.status:
            logger.error("Failure %s occured" % (self.name))
            self.status = False

def filterByLength(potential, length):
    '''Filter out all potential placements for jobs longer than length'''
    if length == -1:
        return
    for job in potential.keys():
        if float(job.get('walltime')) > float(length):
            del potential[job]

class ForeignData(Cobalt.Data.Data):
    def Sync(self, data):
        upd = [(k, v) for (k, v) in data.iteritems() \
               if k != 'tag' and self.get(k) != v]
        if upd:
            logger.info("Resetting job %s parameters %s" % \
                        (self.get('jobid'), ':'.join([u[0] for u in upd])))
            for (k, v) in upd:
                self.set(k, v)

class ForeignDataSet(Cobalt.Data.DataSet):
    def Sync(self):
        try:
            func = getattr(comm[__osource__[0]], __osource__[1])
            data = func(__osource__[2])
        except xmlrpclib.Fault:
            self.__oserror__.Fail()
            return
        except:
            self.logger.error("Unexpected fault during data sync",
                              exc_info=1)
            return
        self.__oserror__.Pass()
        exists = [item.get(self.__oidfield__) for item in self]
        active = [item.get(self.__oidfield__) for item in data]
        syncd = dict([(item.get(self.__oidfield__), item) \
                      for item in self \
                      if item.get(self.__oidfield__) in active])
        done = [item for item in exists if item not in active]
        new_o = [item for item in data \
                 if item.get(self.__oidfield__) not in exists]
        # remove finished jobs
        [self.data.remove(item) for item in self \
         if item.get(self.__oidfield__) in done]
        # create new jobs
        [self.data.append(self.__object__(data)) for data in new_o]
        # sync existing jobs
        for item in [item for item in self \
                     if item.get(self.__oidfield__) in syncd]:
            item.Sync(syncd[item.get(self.__oidfield__)])

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

class Partition(Cobalt.Data.Data):
    '''Partitions are allocatable chunks of the machine'''
    def CanRun(self, job):
        '''Check that job can run on partition with reservation constraints'''
        basic = self.get('scheduled') and self.get('functional')
        queue = job.get('queue') in self.get('queue').split(':')
        jqueue = job.get('queue')
        jsize = int(job.get('nodes')) # should this be 'size' instead?
        psize = int(self.get('size'))
        size = ((psize >= jsize) and ((psize == 32) or (jsize > psize/2)))
        if not (basic and size):
            return False
        # add a slack for job cleanup with reservation calculations
        wall = float(job.get('walltime')) + 5.0
        jdur = 60 * wall
        # all times are in seconds
        current = time.time()
        rstates = []
        for (rname, ruser, start, rdur) in self.get('reservations'):
            if current < start:
                # reservation has not started
                if start < (current + jdur):
                    return False
            elif current > (start + rdur):
                # reservation has finished
                continue
            else:
                # reservation is active
                rstates.append(jqueue == ('R.%s' % (rname))
                               and job.get('user') in ruser.split(':'))
        if rstates:
            return False not in rstates
        else:
            return queue
        return True


class Job(ForeignData):
    '''This class represents User Jobs'''
    def __init__(self, element):
        ForeignData.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.get('jobid'),
                                                  self.get('user')))

class JobSet(Cobalt.Data.DataSet):
    __object__ = Job
    __oidfield__ = 'jobid'
    __oserror__ = FailureMode("QM Connection")
    __osource__ = ('qm', 'GetJobs',
                   [{'tag':'job', 'nodes':'*', 'location':'*',
                     'jobid':'*', 'state':'*', 'index':'*',
                     'walltime':'*', 'queue':'*', 'user':'*'}]

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        self.qmconnect = FailureMode("QM Connection")

    def Run(self, jobid, location):
        pass

class Queue(ForeignData):
    pass

class QueueSet(ForeignDataSet):
    __object__ = Queue
    __oidfield__ = 'name'
    __oserror__ = FailureMode("QM Connection")
    __osource__ = ('qm', 'GetQueues', [{'tag':'queue', 'name':'*'}]

class PartitionSet(Cobalt.Data.DataSet):
    __object__ = Partition

    _configfields = ['db2uid', 'db2dsn', 'db2pwd']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('bgsched'):
        print '''"bgsched" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['bgsched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1
    if not _config._sections.has_key('bgsched-queue'):
        print '''bgsched-queue section missing from config file'''
        raise SystemExit, 1
    qconfig = _config._sections['bgsched-queue']
    qpolicy = {'default':'PlaceFIFO', 'scavenger':'PlaceScavenger',
               'high-prio':'PlaceSpruce'}

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        if '--nodb2' not in sys.argv:
            try:
                import DB2
                conn = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                                   dsn=self.config.get('db2dsn'))
                self.db2 = conn.cursor()
            except:
                print "Failed to connect to DB2"
                raise SystemExit, 1
        self.jobs = []
        self.qmconnect = FailureMode("QM Connection")

    def __getstate__(self):
        return {'data':copy.deepcopy(self.data), 'jobs':copy.deepcopy(self.jobs)}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.qmconnect = FailureMode("QM Connection")
        if '--nodb2' not in sys.argv:
            import DB2
            self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                                   dsn=self.config.get('db2dsn')).cursor()

    def NewSchedule(self):
        # self.jobs contains jobs
        # self queues contains queues
        # self.reservations contains reservations
        # self.resources contains resources
        pass

    def Schedule(self, jobs):
        candidates = [part for part in self.data \
                      if part.get('state') == 'idle' and
                      part.get('functional') and part.get('scheduled')]
        # find idle jobs
        idlejobs = [job for job in self.jobs if job.get('state') == 'queued']
        # filter for dead queus
        # FIXME use self.queues methods to determine live queues
        idlejobs = [job for job in idlejobs if job.get('queue') not \
                    in [q.get('name') for q in stopped_queues + dead_queues]]

            # now we get dependency info
            depsrc = [part.to_rx({'tag':'partition', 'name':'*', 'deps':'*'}) for part in self.data]
            depinfo = Cobalt.Util.buildRackTopology(depsrc)

            # kill for deps already in use
            # deps must be idle, and functional

            # first, get busy partition names
            busy_part_names = [part.get('name') for part in self.data if not part.isIdle() and
                               part.get('functional')]
            candidates = [part for part in candidates
                          if not [item for item in depinfo[part.get('name')][1] if item in busy_part_names]]

            logger.debug("cand1 %s" % ([part.get('name') for part in candidates]))
            # need to filter out contained partitions
            candidates = [part for part in candidates
                          if not [block for block in depinfo[part.get('name')][0]
                                  if block in busy_part_names]]

            logger.debug("cand2 %s" % ([part.get('name') for part in candidates]))
            # now candidates are only completely free blocks
            potential = {}
            for job in idlejobs:
                potential[job] = [part for part in candidates if part.CanRun(job)]
                if not potential[job]:
                    del potential[job]
            return self.ImplementPolicy(potential, depinfo)
        else:
            return []

    def QueueCMP(self, q1, q2):
        if self.qpol.get(q1, 'default') == 'high-prio':
            return -1
        if self.qpol.get(q2, 'default') == 'high-prio':
            return 1
        return 0

    def ImplementPolicy(self, potential, depinfo):
        '''Switch between queue policies'''
        qpotential = {}
        placements = []
        for job in potential:
            if qpotential.has_key(job.get('queue')):
                qpotential[job.get('queue')][job] = potential[job]
            else:
                qpotential[job.get('queue')] = {job:potential[job]}
        self.qpol = {}
        # get queue policies
        try:
            qps = comm['qm'].GetQueues([{'tag':'queue',
                                         'name':'*', 'policy':'*'}])
            self.qmconnect.Pass()
        except:
            self.qmconnect.Fail()
            return []
        # if None, set default
        for qinfo in qps:
            if qinfo.get('policy', None) != None:
                self.qpol[qinfo['name']] = qinfo['policy']
            else:
                self.qpol[qinfo['name']] = 'default'
        queues = self.qpol.keys()
        queues.sort(self.QueueCMP)
        for queue in queues:
            if queue not in qpotential:
                qpotential[queue] = {}
            qp = self.qpolicy.get(self.qpol[queue], 'default')
            qfunc = getattr(self, qp, 'default')
                            
            # need to remove partitions, included and containing,
            # for newly used partitions
            # for all jobs in qpotential
            filterByTopology(placements, depinfo, qpotential[queue])
            newplace = qfunc(qpotential, queue, depinfo)
            placements += newplace
        return placements

    def PlaceFIFO(self, qpotential, queue, depinfo):
        '''Return a set of placements that patch a basic FIFO+backfill policy'''
        placements = []
        potential = qpotential[queue]
        # update queuestate from cqm once per Schedule cycle
        try:
            queuestate = comm['qm'].GetJobs([{'tag':'job', 'jobid':'*', 'index':'*',
                                              'state':'*', 'nodes':'*',
                                              'queue':'*', 'user':'*'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        self.qmconnect.Pass()
        while potential:
            # get lowest jobid and place on first available partition
            jobs = potential.keys()
            jobs.sort(fifocmp)
            newjob = jobs[0]
            
            # filter here for runtime restrictions
            try:
                comm['qm'].CanRun(queuestate, newjob._attrib)
            except xmlrpclib.Fault, flt:
                if flt.faultCode == 30:
                    logger.debug('Job %s/%s cannot run in queue because %s' %
                                 (newjob.get('jobid'), newjob.get('user'), flt.faultString))
                    del potential[newjob]
                    continue
                else:
                    self.qmconnect.Fail()
                    return 0
            self.qmconnect.Pass()
            logger.debug('Job %s/%s accepted to run' % (newjob.get('jobid'), newjob.get('user')))
            location = potential[newjob][0]
            location.PlaceJob(newjob)
            newjob.Place(location)
            # update local state of job for use in this schedule cycle
            for j in queuestate:
                if j.get('jobid') == newjob.get('jobid') and j.get('queue') == newjob.get('queue'):
                    j.update({'state':'running'})
            placements.append((newjob.get('jobid'), location.get('name')))
            del potential[newjob]

            # now we need to remove location (and dependencies and all
            # partitions containing it) from potential lists
            filterByTopology(placements, depinfo, potential)
        return placements

    def PlaceScavenger(self, qpotential, queue, depinfo):
        '''A really stupid priority queueing mechanism that starves lo queue jobs if the high-queue has idle jobs'''
        live = [job.get('queue') for job in self.jobs if job.get('state') == 'queued']
        if live.count(queue) != len(live):
            return []
        return self.PlaceFIFO(qpotential[queue], depinfo)

    def PlaceSpruce(self, qpotential, queue, depinfo):
        '''Defer other jobs which spruce queue has idle jobs'''
        idle = [job for job in self.jobs if job.get('queue') == queue \
                  and job.get('state') == 'queued']
        p = self.PlaceFIFO(qpotential, queue, depinfo)
        if len(p) != len(idle):
            # we have idle jobs, so defer others
            for q in qpotential:
                qpotential[q] = {}
        return p
                
class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched'
    __name__ = 'scheduler'
    #__statefields__ = ['partitions', 'jobs']
    __statefields__ = ['partitions']
    __schedcycle__ = 10
    async_funcs = ['assert_location', 'RunQueue',
                   'RemoveOldReservations', 'ResQueueSync']

    def __init__(self, setup):
        self.partitions = PartitionSet()
        self.jobs = []
        Cobalt.Component.Component.__init__(self, setup)
        self.executed = []
        self.qmconnect = FailureMode("QM Connection")
        self.lastrun = 0
        self.register_function(lambda  address,
                               data:self.partitions.Get(data),
                               "GetPartition")
        self.register_function(lambda  address,
                               data:self.partitions.Add(data),
                               "AddPartition")
        self.register_function(lambda  address,
                               data:self.partitions.Del(data),
                               "DelPartition")
        self.register_function(lambda address, data, updates:
                               self.partitions.Get(data, lambda part, newattr:part.update(newattr), updates),
                               'Set')  
        self.register_function(self.AddReservation, "AddReservation")
        self.register_function(self.ReleaseReservation, "DelReservation")
        self.register_function(self.SetReservation, "SetReservation")

    def SupressDuplicates(self, provisional):
        '''Prevent duplicate job start requests from being generated'''
        locations = [pro[1] for pro in provisional]
        for (jobid, location) in provisional:
            if jobid in self.executed:
                logger.error("Tried to execute job %s multiple times" % (jobid))
                provisional.remove((jobid, location))
                [partition.Free() for partition in self.partitions if partition.get('name') == location]
            elif locations.count(location) > 1:
                logger.error("Tried to use the same partition multiple times")
                provisional.remove((jobid, location))
                locations.remove(location)
            else:
                self.executed.append(jobid)
            
    def RunQueue(self):
        '''Process changes to the cqm queue'''
        since = time.time() - self.lastrun
        if since < self.__schedcycle__:
            return
        try:
            jobs = comm['qm'].GetJobs([{'tag':'job', 'nodes':'*', 'location':'*',
                                        'jobid':'*', 'state':'*', 'index':'*',
                                        'walltime':'*', 'queue':'*', 'user':'*'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        except:
            self.logger.error("Unexpected fault during queue fetch", exc_info=1)
            return 0
        self.qmconnect.Pass()
        active = [job.get('jobid') for job in jobs]
        logger.debug("RunQueue: active jobs %s" % active)
        for job in [j for j in self.jobs if j.get('jobid') not in active]:
            logger.info("Job %s/%s: gone from qm" % (job.get('jobid'), job.get('user')))
            self.jobs.remove(job)
        # known is jobs that are already registered
        known = [job.get('jobid') for job in self.jobs]
        [partition.Free() for partition in self.partitions if partition.job not in known + ['none']]
        newjobs = [job for job in jobs if job.get('jobid') not in known]
        logger.debug('RunQueue: newjobs %s' % newjobs)
        self.jobs.extend([Job(job) for job in newjobs])
        logger.debug('RunQueue: after extend to Job %s' % self.jobs)
        placements = self.partitions.Schedule(jobs)
        if '-t' not in sys.argv:
            self.SupressDuplicates(placements)
            for (jobid, part) in placements:
                try:
                    comm['qm'].RunJobs([{'tag':'job', 'jobid':jobid}], [part])
                    pass
                except:
                    logger.error("failed to connect to the queue manager to run job %s" % (jobid))
        else:
            print "Jobs would be placed on:", placements
        self.lastrun = time.time()

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
    

