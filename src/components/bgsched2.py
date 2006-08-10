#!/usr/bin/env python

'''Scheduler for BG/L'''
__revision__ = '$Revision$'

import copy, logging, sys, time, xmlrpclib, ConfigParser
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

if '--nodb2' not in sys.argv:
    import DB2

logger = logging.getLogger('bgsched')

comm = Cobalt.Proxy.CommDict()

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

class event:
    '''events describe an event in terms of start and duration'''
    def __init__(self, start, duration, status):
        self.start = start
        self.duration = duration
        self.status = status

class timeData(Cobalt.Data.Data):
    '''timeData is a class that can generate event traces for temporal ops'''
    def __init__(self, element):
        Cobalt.Data.Data.__init__(self, element)

    def getEvents(self):
        '''Return Duration events for self'''
        return []

class Job(timeData):
    '''This class represents User Jobs'''
    def __init__(self, element):
        timeData.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.get('jobid'),
                                                       self.get('user')))
        self.start = -1

    def getEvents(self):
        if self.start != -1:
            etype = 'soft'
            if self.status == 'planned':
                etype = 'hard'
            return [event(self.start, float(self.get('duration')), etype)]
        else:
            return []

    def planRun(self, start):
        if self.start == -1:
            self.start = start
            self.status = 'planned'
        else:
            logger.error("Job %s: Attempted to run multiple times" % (self.get('jobid')))

cqmFailed = FailureMode()

class JobSet(Cobalt.Data.DataSet):
    __object__ = Job
    __syncrate__ = 60
    alljobq = [{'tag':'job', 'nodes':'*', 'location':'*', 'jobid':'*', 'state':'*',
		'walltime':'*', 'queue':'*', 'user':'*'}]

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        self.lastrun = -1

    def Sync(self):
        '''Synchronize with current queue state'''
        since = time.time() - self.lastrun
        if since < self.__syncrate__:
            return
        try:
            jobs = comm['qm'].GetJobs(self.alljobq)
        except xmlrpclib.Fault:
            cqmFailed.Fail()
            return 0
        except:
            logger.error("Unexpected fault during queue fetch", exc_info=1)
            return 0
        cqmFailed.Pass()
        active = [job.get('jobid') for job in jobs]
        for current in jobs:
            if self.Get([current]):
                # job is already registered and matches
                continue
            else:
                if not self.Get([{'tag':'job', 'jobid':current.get('jobid')}]):
                    # job is new
                    self.Add([current])
                    continue
                # job is modified
		# sync data here
                pass
	# find finished jobs
        for job in self:
            if job.get('jobid') not in active:
                logger.info("Job %s has completed" % (job.get("jobid")))
                self.Del([{'tag':'job', 'jobid':job.get('jobid')}])
        self.lastrun = time.time()

class Partition(timeData):
    '''Partitions are allocatable chunks of the machine'''
    def __init__(self, element):
        timeData.__init__(self, element)
        self.set('state', 'idle')
        self.set('reservations', [])
        self.job = 'none'
        self.rcounter = 1
        self.set('db2', 'XX')

    def isIdle(self):
        '''Return True if partition is idle'''
        if '--nodb2' not in sys.argv:
            return self.get('state') == 'idle' and self.get('db2') == 'F'
        else:
            return self.get('state') == 'idle'

    def CanRun(self, job):
        '''Check that job can run on partition with reservation constraints'''
        basic = self.get('scheduled') and self.get('functional')
        queue = job.get('queue') in self.get('queue').split(':')
        jsize = int(job.get('nodes')) # should this be 'size' instead?
        psize = int(self.get('size'))
        size = ((psize >= jsize) and ((psize == 32) or (jsize > psize/2)))
        if not (basic and queue and size):
            return False
        # add a little slack for job cleanup with reservation calculations
        wall = float(job.get('walltime')) + 5.0
        jdur = 60 * wall
        # all times are in seconds
        current = time.time()
        for (_, user, start, rdur) in self.get('reservations'):
            if job.get('user') in user:
                continue
            if current < start:
                # reservation has not started
                if start < (current + jdur):
                    return False
            elif current > (start + rdur):
                # reservation has finished
                continue
            else:
                # reservation is active
                return False
        return True

    def PlaceJob(self, job):
        '''Allocate this partition for Job'''
        logger.info("Job %s/%s: Scheduling job %s on partition %s" % (
            job.get('jobid'), job.get('user'), job.get('jobid'),
            self.get('name')))
        self.job = job.get('jobid')
        self.set('state', 'busy')

    def Free(self):
        '''DeAllocate partition for current job'''
        logger.info("Job %s: Freeing partition %s" % (self.job, self.get('name')))
        self.job = 'none'
        self.set('state', 'idle')

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
    qpolicy = {'default':'PlaceFIFO', 'scavenger':'PlaceScavenger'}

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

    def Schedule(self, jobs):
        '''Find new jobs, fit them on a partitions'''
        knownjobs = [job.get('jobid') for job in self.jobs]
        logger.debug('Schedule: knownjobs %s' % knownjobs)
        activejobs = [job.get('jobid') for job in jobs]
        finished = [jobid for jobid in knownjobs if jobid not in activejobs]
        #print "known", knownjobs, "active", activejobs, "finished", finished
        # add new jobs
        #print jobs
        [self.jobs.append(Job(jobdata)) for jobdata in jobs if jobdata.get('jobid') not in knownjobs]
        # delete finished jobs
        [self.jobs.remove(job) for job in self.jobs if job.get('jobid') in finished]
        for (jobid, state, queue) in [(job.get('jobid'), job.get('state'), job.get('queue')) for job in jobs]:
            try:
                [currjob] = [job for job in self.jobs if job.get('jobid') == jobid]
            except:
                continue
            if ((currjob.get('queue') != queue) or (currjob.get('state') != state)):
                logger.error("Detected local state inconsistency for job %s. Fixing." % jobid)
                currjob.set('state', state)
                currjob.set('queue', queue)
        # free partitions with nonexistant jobs
        [partition.Free() for partition in self.data if partition.job not in activejobs + ['none']]
        # find idle partitions for new jobs (idle, functional, and scheduled)
        candidates = [part for part in self.data if part.get('state') == 'idle' and
                      part.get('functional') and part.get('scheduled')]
        # find idle jobs
        idlejobs = [job for job in self.jobs if job.get('state') == 'queued']
        # filter for stopped and dead queues
        try:
            stopped_queues = comm['qm'].GetQueues([{'tag':'queue', 'name':'*', 'state':'stopped'}])
            dead_queues = comm['qm'].GetQueues([{'tag':'queue', 'name':'*', 'state':'dead'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        self.qmconnect.Pass()
        logger.debug('stopped queues %s' % stopped_queues)
        idlejobs = [job for job in idlejobs if job.get('queue') not in [q.get('name') for q in stopped_queues + dead_queues]]

        #print "jobs:", self.jobs
        if candidates and idlejobs:
            logger.debug("initial candidates: %s" % ([cand.get('name') for cand in candidates]))
            #print "Actively checking"
            if '--nodb2' not in sys.argv:
                self.db2.execute("select blockid, status from bglblock;")
                results = self.db2.fetchall()
                for (pname, state) in results:
                    partname = pname.strip()
                    partinfo = [part for part in self.data if part.get('name') == partname]
                    if partinfo:
                        partinfo[0].set('db2', state)

                for partition in [part for part in self.data if part.get('db2', 'XXX') == 'XXX']:
                    logger.error("DB2 has no state for partition %s" % (partition.get('name')))

                # check for discrepancies between candidates and db2
                for part in [part for part in candidates if part.get('db2') != 'F']:
                    foundlocation = [job for job in jobs if job.get('location') == part.get('name')]
                    if foundlocation:
                        part.job = foundlocation[0].get('jobid')
                        part.set('state', 'busy')
                        logger.error("Found job %s on Partition %s. Manually setting state." % \
                                     (foundlocation[0].get('jobid'), part.get('name')))
                    else:
                        logger.error('Partition %s in inconsistent state' % (part.get('name')))
                    candidates.remove(part)
            #print "after db2 check"

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

    def ImplementPolicy(self, potential, depinfo):
        '''Switch between queue policies'''
        qpotential = {}
        placements = []
        for job in potential.keys():
            if qpotential.has_key(job.get('queue')):
                qpotential[job.get('queue')][job] = potential[job]
            else:
                qpotential[job.get('queue')] = {job:potential[job]}
        for queue in qpotential.keys():
            qfunc = getattr(self, self.qpolicy.get(self.qconfig.get(queue, 'default'), 'default'))
            placements += qfunc(qpotential, queue, depinfo)
        return placements

    def PlaceFIFO(self, qpotential, queue, depinfo):
        '''Return a set of placements that patch a basic FIFO+backfill policy'''
        placements = []
        potential = qpotential[queue]
        # update queuestate from cqm once per Schedule cycle
        try:
            queuestate = comm['qm'].GetJobs([{'tag':'job', 'jobid':'*',
                                              'state':'*', 'nodes':'*',
                                              'queue':'*', 'user':'*'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        self.qmconnect.Pass()
        while potential:

            # get lowest jobid and place on first available partition
            potentialjobs = [int(key.get('jobid')) for key in potential.keys()]
            potentialjobs.sort()
            newjobid = str(potentialjobs[0])
            [newjob] = [job for job in potential.keys() if job.get('jobid') == newjobid]
            
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

            # remove entries in potential for all related partitions
            related = [part for part in depinfo[location.get('name')][0] + depinfo[location.get('name')][1]]
            for block in [location.get('name')] + related:
                for job, places in potential.iteritems():
                    if block in [p.get('name') for p in places]:
                        potential[job].remove([b for b in potential[job] if b.get('name')==block][0])

            for job in potential.keys():
                if not potential[job]:
                    del potential[job]
        return placements

    def PlaceScavenger(self, qpotential, queue, depinfo):
        '''A really stupid priority queueing mechanism that starves lo queue jobs if the high-queue has idle jobs'''
        live = [job.get('queue') for job in self.jobs if job.get('state') == 'queued']
        if live.count(queue) != len(live):
            return []
        return self.PlaceFIFO(qpotential[queue], depinfo)
                
class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched'
    __name__ = 'scheduler'
    __statefields__ = ['partitions', 'jobs']
    __schedcycle__ = 10
    async_funcs = ['assert_location', 'RunQueue']

    def __init__(self, setup):
        self.partitions = PartitionSet()
        self.jobs = JobSet()
        Cobalt.Component.Component.__init__(self, setup)
        self.executed = []
        self.qmconnect = FailureMode("QM Connection")
        self.lastrun = 0
        self.register_function(lambda  address, data:self.partitions.Get(data), "GetPartition")
        self.register_function(lambda  address, data:self.partitions.Add(data), "AddPartition")
        self.register_function(lambda  address, data:self.partitions.Del(data), "DelPartition")
        self.register_function(lambda address, data, updates:
                               self.partitions.Get(data, lambda part, newattr:part.update(newattr), updates),
                               'Set')  
        self.register_function(self.AddReservation, "AddReservation")
        self.register_function(self.ReleaseReservation, "DelReservation")

    def AddReservation(self, _, spec, name, user, start, duration):
        '''Add a reservation to matching partitions'''
        reservation = (name, user, start, duration)
        return self.partitions.Get(spec, callback=lambda x, y:x.get('reservations').append(reservation))

    def ReleaseReservation(self, _, spec, name):
        '''Release specified reservation'''
        return self.partitions.Get(spec, callback=lambda x, y:[x.get('reservations').remove(rsv)
                                                              for rsv in x.get('reservations') if rsv[0] == name])

    def SupressDuplicates(self, provisional):
        '''Prevent duplicate job start requests from being generated'''
        for (jobid, location) in provisional:
            if jobid in self.executed:
                logger.error("Tried to execute job %s multiple times" % (jobid))
                provisional.remove((jobid, location))
                [partition.Free() for partition in self.partitions if partition.get('name') == location]
            else:
                self.executed.append(jobid)

    def CanRun(self, nodes, duration, queue, user, location, starttime):
         '''
         nodes - size of job
         duration - walltime of job
         queue - 
         user - 
         location - 
         starttime - time that job is intended to be started
         '''
         # check location
         if not self.partitions.isFree(location, starttime, duration):
             return False
         # check queues
         
         # check reservations
         
         # check jobs
         running_jobs = [job for job in self.jobs if job.status == 'running']
         for rjob in running_jobs:
             if rjob.get('location') == location or \
                rjob.get('location') in self.partitions.GetParents(location) or \
                rjob.location in self.partitions.GetChildren(location):
                 #if range(starttime, starttime+duration) overlaps with range(rjob.get('starttime'), rjob.get('starttime')+rjob.get('duration')
                     return False

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (OPTS, ARGS) = getopt(sys.argv[1:], 'C:dD:t', ['nodb2'])
    except GetoptError, msg:
        print "%s\nUsage:\nbgsched.py [-t] [-C configfile] [-d] [-D <pidfile>] [--nodb2]" % (msg)
        raise SystemExit, 1
    try:
        DAEMON = [x[1] for x in OPTS if x[0] == '-D'][0]
    except:
        DAEMON = False
    if len([x for x in opts if x[0] == '-d']):
        DLEVEL = logging.DEBUG
    else:
        DLEVEL = logging.INFO
    Cobalt.Logging.setup_logging('bgsched', level=DLEVEL)
    SERVER = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':DAEMON})
    SERVER.serve_forever()
    

