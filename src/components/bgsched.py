#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision'

import copy, logging, sys, time, xmlrpclib, ConfigParser
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy

if '--notbgl' not in sys.argv:
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

class Partition(Cobalt.Data.Data):
    '''Partitions are allocatable chunks of the machine'''
    def __init__(self, element):
        Cobalt.Data.Data.__init__(self, element)
        self.set('state', 'idle')
        self.set('reservations', [])
        self.job = 'none'
        self.rcounter = 1

    #def __cmp__(self, other):
    #    return int(self.get('size')).__cmp__(int(other.element.get('size')))

    def CanRun(self, job):
        '''Check that job can run on partition with reservation constraints'''
        if not self.get("scheduled") or not self.get('functional'):
            return False
        if job.get('queue') not in self.get('queue'):
            #print "job", job.element.get('jobid'), 'queue'
            return False
        jobsize = int(job.get('nodes'))
        if jobsize > self.get('size'):
            #print "job", job.element.get('jobid'), 'size'
            return False
        if (((jobsize * 2) <= self.get('size')) and (self.get('size') != 32)):
            # job should be run on a smaller partition
            return False
        # add a little slack for job cleanup with reservation calculations
        wall = float(job.get('walltime')) + 5.0
        jdur = 60 * wall
        # all times are in seconds
        current = time.time()
        for (rname, user, start, rdur) in self.get('reservations'):
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

class Job(Cobalt.Data.Data):
    '''This class is represents User Jobs'''
    def __init__(self, element):
        Cobalt.Data.Data.__init__(self, element)
        self.partition = 'none'
        logger.info("Job %s/%s: Found new job" % (self.get('jobid'),
                                                       self.get('user')))

    def Place(self, partition):
        '''Build linkage to execution partition'''
        self.partition = partition.get('name')
        self.set('state', 'running')

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
    qpolicy = {'default':'PlaceFIFO', 'short':'PlaceShort', 'scavenger':'PlaceScavenger'}

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        if '--notbgl' not in sys.argv:
            self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                                   dsn=self.config.get('db2dsn')).cursor()
        self.jobs = []
        self.qmconnect = FailureMode("QM Connection")

    def __getstate__(self):
        return {'data':copy.deepcopy(self.data), 'jobs':copy.deepcopy(self.jobs)}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.qmconnect = FailureMode("QM Connection")
        if '--notbgl' not in sys.argv:
            self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                                   dsn=self.config.get('db2dsn')).cursor()

    def Schedule(self, jobs):
        '''Find new jobs, fit them on a partitions'''
        knownjobs = [job.get('jobid') for job in self.jobs]
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
        # find idle partitions for new jobs
        candidates = [part for part in self.data if part.get('state') == 'idle' and
                      part.get('functional') and part.get('scheduled')]
        print "initial candidates: ", [cand.get('name') for cand in candidates]
        # find idle jobs
        idlejobs = [job for job in self.jobs if job.get('state') == 'queued']
        #print "jobs:", self.jobs
        if candidates and idlejobs:
            #print "Actively checking"
            if '--notbgl' not in sys.argv:
                self.db2.execute("select blockid, status from bglblock;")
                results = self.db2.fetchall()
                db2data = {}
                [db2data.update({block.strip():status}) for (block, status) in results]
                print "db2data:", db2data
                for part in [part for part in candidates if db2data[part.get('name')] != 'F']:
                    foundlocation = [job for job in jobs if job.get('location') == part.get('name')]
                    if foundlocation:
                        part.job = foundlocation[0].get('jobid')
                        part.set('state', 'busy')
                        logger.error("Found job %s on Partition %s. Manually setting state." % (foundlocation[0].get('jobid'), part.get('name')))
                    else:
                        logger.error('Partition %s in inconsistent state' % (part.get('name')))
                    candidates.remove(part)
            #print "after db2 check"
            print "candidates: ", [cand.get('name') for cand in candidates]
            partbyname = {}
            for part in self.data:
                partbyname[part.get('name')] = part
            # deps is recursive dep list / pdeps is single ref 
            deps = {}
            pdeps = {}
            for part in self.data:
                #print "Dep line", part.get('name'), part.get('deps')
                pdeps[part] = part.get('deps')
            [pdeps[key].remove('') for key in pdeps.keys() if '' in pdeps[key]]
            for part in pdeps.keys():
                traversed = []
                left = copy.deepcopy(pdeps[part])
                while left:
                    current = left.pop()
                    traversed.append(current)
                    [left.append(item) for item in pdeps[partbyname[current]] if item not in traversed]
                deps[part] = [partition for partition in self.data if partition.get('name') in traversed]
            # now we have deps for all partitions
            #print "After dep check"
            #print "Deps:"
            #for key in deps.keys():
            #    if deps[key]:
            #        print key.element.get('name'), [partdep.element.get('name') for partdep in deps[key]]
            contained = {}
            for part in candidates:
                contained[part] = [key for key, value in deps.iteritems() if part in value and key != part]
            deactivate = []
            # kill for deps already in use
            candidates = [part for part in candidates
                          if not [item for item in deps[part] if item.get('state') != 'idle']]
            print "cand1", candidates
            # need to filter out contained partitions
            if '--notbgl' not in sys.argv:
                candidates = [part for part in candidates if not [block for block in contained[part] if db2data.get(block.get('name'), 'F') != 'F' and block.get('functional') and block.get('state') == 'idle']]
                print "cand2", candidates
            # now candidates are only completely free blocks
            #print "candidates: ", [cand.element.get('name') for cand in candidates]
            potential = {}
            for job in idlejobs:
                potential[job] = [part for part in candidates if part.CanRun(job)]
                if not potential[job]:
                    del potential[job]
            print "Potential", potential, deps
            return self.ImplementPolicy(potential, deps)
        else:
            return []

    def ImplementPolicy(self, potential, deps):
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
            placements += qfunc(qpotential, queue, deps)
        return placements

    def PlaceFIFO(self, qpotential, queue, deps):
        '''Return a set of placements that patch a basic FIFO+backfill policy'''
        placements = []
        potential = qpotential[queue]
        while potential:
            #print "potential"
            #for key, value in potential.iteritems():
            #    print key.element.get('jobid'), [part.element.get('name') for part in value]
            potentialjobs = [int(key.get('jobid')) for key in potential.keys()]
            potentialjobs.sort()
            newjobid = str(potentialjobs[0])
            [newjob] = [job for job in potential.keys() if job.get('jobid') == newjobid]
            location = potential[newjob][0]
            location.PlaceJob(newjob)
            newjob.Place(location)
            placements.append((newjob.get('jobid'), location.get('name')))
            del potential[newjob]
            # now we need to remove location (and all partitions containing it) from potential lists
            #print "removing locations:", [x.element.get('name') for x in [location] + deps[location]]
            # remove entries in potential for all contained partitions
            for block in [location] + deps[location]:
                [potential[job].remove(block) for job, places in potential.iteritems() if block in places]
            # remove entries in potential for all partitions containing location
            for block in [block for block, bdeps in deps.iteritems() if location in bdeps]:
                [potential[job].remove(block) for job, places in potential.iteritems() if block in places]
            for job in potential.keys():
                if not potential[job]:
                    del potential[job]
        return placements

    def PlaceShort(self, qpotential, queue, deps):
        '''Policy for short queue. Limited to jobs 30 mins or less'''
        potential = qpotential
        for job in potential[queue].keys():
            if float(job.get('walltime')) > 30:
                del potential[queue][job]
        return self.PlaceFIFO(potential, queue, deps)

    def PlaceScavenger(self, qpotential, queue, deps):
        '''A really stupid priority queueing mechanism that starves lo queue jobs if the high-queue has idle jobs'''
        live = [job.get('queue') for job in self.jobs if job.get('state') == 'queued']
        if live.count(queue) != len(live):
            return []
        return self.PlaceFIFO(qpotential[queue], deps)
                
class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched'
    __name__ = 'scheduler'
    __statefields__ = ['partitions']
    __schedcycle__ = 10
    async_funcs = ['assert_location', 'RunQueue']

    def __init__(self, setup):
        self.partitions = PartitionSet()
        Cobalt.Component.Component.__init__(self, setup)
        self.jobs = []
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

    def AddReservation(self, address, spec, name, user, start, duration):
        '''Add a reservation to matching partitions'''
        reservation = (name, user, start, duration)
        return self.partitions.Get(spec, callback=lambda x, y:x.get('reservations').append(reservation))

    def ReleaseReservation(self, address, spec, name):
        '''Release specified reservation'''
        return self.partitions.Get(spec, callback=lambda x, y:[x.get('reservations').remove(rsv)
                                                              for rsv in x.get('reservations') if rsv[0] == name])

    def RunQueue(self):
        since = time.time() - self.lastrun
        if since < self.__schedcycle__:
            return
        try:
            jobs = comm['qm'].GetJobs([{'tag':'job', 'nodes':'*', 'location':'*', 'jobid':'*', 'state':'*',
                                      'walltime':'*', 'queue':'*', 'user':'*'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        except:
            self.logger.error("Unexpected fault during queue fetch", exc_info=1)
            return 0
        self.qmconnect.Pass()
        active = [job.get('jobid') for job in jobs]
        for job in [j for j in self.jobs if j.get('jobid') not in active]:
            logger.info("Job %s/%s: gone from qm" % (job.get('jobid'), job.get('user')))
            self.jobs.remove(job)
        # known is jobs that are already registered
        known = [job.get('jobid') for job in self.jobs]
        [partition.Free() for partition in self.partitions if partition.job not in known + ['none']]
        newjobs = [job for job in jobs if job.get('jobid') not in known]
        self.jobs.extend([Job(job) for job in newjobs])
        placements = self.partitions.Schedule(jobs)
        #print placements
        for (jobid, part) in placements:
            try:
                comm['qm'].RunJobs([{'tag':'job', 'jobid':jobid}], [part])
            except:
                logger.error("failed to connect to the queue manager to run job %s" % (jobid))
        self.lastrun = time.time()

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arguments) = getopt(sys.argv[1:], 'C:dD:', ['notbgl'])
    except GetoptError, msg:
        print "%s\nUsage:\nbgsched.py [-C configfile] [-d] [-D <pidfile>] [--notbgl]" % (msg)
        raise SystemExit, 1
    try:
        daemon = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        daemon = False
    debug = len([x for x in opts if x[0] == '-d'])
    Cobalt.Logging.setup_logging('bgsched', level=20)
    server = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    server.serve_forever()
    

