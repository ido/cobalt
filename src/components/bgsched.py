#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision'

import copy, sys, time
import Cobalt.Component, Cobalt.Data, Cobalt.Proxy
import DB2

from elementtree.ElementTree import XML
from syslog import syslog, LOG_INFO, LOG_ERR
from ConfigParser import ConfigParser

sys.path.append('/soft/apps/rm-0.90/lib/python')
import DB2

class FailureMode(object):
    '''FailureModes are used to report (and supress) errors appropriately
    call Pass() on success and Fail() on error'''
    def __init__(self, name):
        self.name = name
        self.status = True

    def Pass(self):
        '''Check if status was previously failure and report OK status if needed'''
        if not self.status:
            syslog(LOG_ERR, "Failure %s cleared" % (self.name))
            self.status = True

    def Fail(self):
        '''Check if status was previously success and report failed status if needed'''
        if self.status:
            syslog(LOG_ERR, "Failure %s occured" % (self.name))
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
        if self.get('admin') != 'online':
            return False
        if job.element.get('queue') not in self.get('queue').split(':') + ['BUG']:
            #print "job", job.element.get('jobid'), 'queue'
            return False
        jobsize = int(job.element.get('nodes'))
        partsize = int(self.get('size'))
        if jobsize > partsize:
            #print "job", job.element.get('jobid'), 'size'
            return False
        if (((jobsize * 2) <= partsize) and (partsize != 32)):
            # job should be run on a smaller partition
            return False
        # add a little slack for job cleanup with reservation calculations
        wall = float(job.element.get('walltime')) + 5.0
        jdur = 60 * wall
        # all times are in seconds
        current = time.time()
        for reserv in self.findall('Reservation'):
            if job.element.get('user') in reserv.get('user', '').split(':'):
                continue
            start = float(reserv.get('start'))
            rdur = int(reserv.get('duration'))
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
        syslog(LOG_INFO, "Job %s/%s: Scheduling job %s on partition %s" % (
            job.element.get('jobid'), job.element.get('user'), job.element.get('jobid'),
            self.get('name')))
        self.job = job.element.get('jobid')
        self.set('state', 'busy')

    def Free(self):
        '''DeAllocate partition for current job'''
        syslog(LOG_INFO, "Job %s: Freeing partition %s" % (self.job, self.get('name')))
        self.job = 'none'
        self.set('state', 'idle')

    def AddReservation(self, args):
        '''Add a reservation for this partition'''
        reservation = Cobalt.Data.Data(args)
        if not args.has_key('name'):
            reservation.set('name', "%s.%s" % (self.get('name'), self.rcounter))
            self.rcounter += 1
        self._attrib['reservations'].append(reservation)

    def DelReservation(self, name):
        [self._attrib['reservations'].remove(reservation) for reservation in self._attrib['reservations'] if reservation.get('name') == name]

class Job(Cobalt.Data.Data):
    '''This class is represents User Jobs'''
    def __init__(self, element):
        Cobalt.Data.Data.__init__(self, element)
        self.partition = 'none'
        syslog(LOG_INFO, "Job %s/%s: Found new job" % (self.get('jobid'),
                                                       self.get('user')))

    def Place(self, partition):
        '''Build linkage to execution partition'''
        self.partition = partition.element.get('name')
        self.set('state', 'running')
        

class PartitionSet(Cobalt.Data.DataSet):
    __object__ = Partition

    _configfields = ['db2uid', 'db2dsn', 'db2pwd']
    _config = ConfigParser()
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
        self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                               dsn=self.config.get('db2dsn')).cursor()
        self.jobs = []
        self.qmconnect = FailureMode("QM Connection")

    def __getstate__(self):
        return {'data':copy.deepcopy(self.data), 'jobs':copy.deepcopy(self.jobs)}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.qmconnect = FailureMode("QM Connection")
        self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                               dsn=self.config.get('db2dsn')).cursor()

    def Schedule(self, jobs):
        '''Find new jobs, fit them on a partitions'''
        #print "scheduling"
        knownjobs = [job.element.get('jobid') for job in self.jobs]
        activejobs = [job.get('jobid') for job in jobs]
        finished = [jobid for jobid in knownjobs if jobid not in activejobs]
        #print "known", knownjobs, "active", activejobs, "finished", finished
        # add new jobs
        [self.jobs.append(Job(jobdata)) for jobdata in jobs if jobdata.get('jobid') not in knownjobs]
        # delete finished jobs
        [self.jobs.remove(job) for job in self.jobs if job.element.get('jobid') in finished]
        for (jobid, state, queue) in [(job.get('jobid'), job.get('state'), job.get('queue')) for job in jobs]:
            try:
                [currjob] = [job for job in self.jobs if job.element.get('jobid') == jobid]
            except:
                continue
            if ((currjob.element.get('queue') != queue) or (currjob.element.get('state') != state)):
                syslog(LOG_ERR, "Detected local state inconsistency for job %s. Fixing." % jobid)
                currjob.element.set('state', state)
                currjob.element.set('queue', queue)
        # free partitions with nonexistant jobs
        [partition.Free() for partition in self.data if partition.job not in activejobs + ['none']]
        # find idle partitions for new jobs
        candidates = [part for part in self.data if part.element.get('state') == 'idle' and
                      part.element.get('admin') == 'online']
        #print "initial candidates: ", [cand.element.get('name') for cand in candidates]
        # find idle jobs
        idlejobs = [job for job in self.jobs if job.element.get('state') == 'queued']
        #print "jobs:", self.jobs
        #print "idle jobs:", [idlej.element.get('jobid') for idlej in idlejobs]
        #print "not idle:", [(nidlej.element.get('jobid'), nidlej.element.get('state')) for nidlej in self.jobs if nidlej not in idlejobs]
        if candidates and idlejobs:
            #print "Actively checking"
            self.db2.execute("select blockid, status from bglblock;")
            results = self.db2.fetchall()
            db2data = {}
            [db2data.update({block.strip():status}) for (block, status) in results]
            #print "db2data:", db2data
            for part in [part for part in candidates if db2data[part.element.get('name')] != 'F']:
                foundlocation = [job for job in jobs if job.get('location') == part.element.get('name')]
                if foundlocation:
                    part.job = foundlocation[0].get('jobid')
                    part.element.set('state', 'busy')
                    syslog(LOG_ERR, "Found job %s on Partition %s. Manually setting state." % (foundlocation[0].get('jobid'), part.element.get('name')))
                else:
                    syslog(LOG_ERR, 'Partition %s in inconsistent state' % (part.element.get('name')))
                candidates.remove(part)
            #print "after db2 check"
            #print "candidates: ", [cand.element.get('name') for cand in candidates]
            partbyname = {}
            for part in self.data:
                partbyname[part.element.get('name')] = part
            # deps is recursive dep list / pdeps is single ref 
            deps = {}
            pdeps = {}
            for part in self.data:
                #print "Dep line", part.element.get('name'), part.element.get('deps')
                pdeps[part] = part.element.get('deps', '').split(':')
            [pdeps[key].remove('') for key in pdeps.keys() if '' in pdeps[key]]
            for part in pdeps.keys():
                traversed = []
                left = copy.deepcopy(pdeps[part])
                while left:
                    current = left.pop()
                    traversed.append(current)
                    [left.append(item) for item in pdeps[partbyname[current]] if item not in traversed]
                deps[part] = [partition for partition in self.data if partition.element.get('name') in traversed]
            # now we have deps for all partitions
            #print "After dep check"
            #print "Deps:"
            #for key in deps.keys():
            #    if deps[key]:
            #        print key.element.get('name'), [partdep.element.get('name') for partdep in deps[key]]
            contained = {}
            for part in candidates:
                contained[part] = [key for key, value in deps.iteritems() if part in value and key != part]
            #print "Contained:"
            #for part in contained.keys():
            #    print part.element.get('name'), [cpart.element.get('name') for cpart in contained[part]]
            # need to filter out dependency-used partitions
            candidates = [part for part in candidates if not [item for item in deps[part] if item not in candidates]]
            # need to filter out contained partitions
            candidates = [part for part in candidates if not [block for block in contained[part] if db2data.get(block.element.get('name'), 'F') != 'F']]
            # now candidates are only completely free blocks
            #print "candidates: ", [cand.element.get('name') for cand in candidates]
            potential = {}
            for job in idlejobs:
                potential[job] = [part for part in candidates if part.CanRun(job)]
                if not potential[job]:
                    del potential[job]
            return self.ImplementPolicy(potential, deps)
        else:
            return []

    def ImplementPolicy(self, potential, deps):
        '''Switch between queue policies'''
        qpotential = {}
        placements = []
        for job in potential.keys():
            if qpotential.has_key(job.element.get('queue')):
                qpotential[job.element.get('queue')][job] = potential[job]
            else:
                qpotential[job.element.get('queue')] = {job:potential[job]}
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
            potentialjobs = [int(key.element.get('jobid')) for key in potential.keys()]
            potentialjobs.sort()
            newjobid = str(potentialjobs[0])
            [newjob] = [job for job in potential.keys() if job.element.get('jobid') == newjobid]
            location = potential[newjob][0]
            location.PlaceJob(newjob)
            newjob.Place(location)
            placements.append((newjob.element.get('jobid'), location.element.get('name')))
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
        potential = qpotential[queue]
        for job in potential.keys():
            if float(job.get('walltime')) > 30:
                del potential[job]
        return self.PlaceFIFO(potential, deps)

    def PlaceScavenger(self, qpotential, queue, deps):
        '''A really stupid priority queueing mechanism that starves lo queue jobs if the high-queue has idle jobs'''
        live = [job.get('queue') for job in self.jobs if job.get('state') == 'queued']
        if live.count(queue) != len(live):
            return []
        return self.PlaceFIFO(qpotential[queue], deps)
                
class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'BGSched'
    __component__ = 'scheduler'
    __dispatch__ = {'events':'HandleEvent',
                    'GetPartition':'partitions.Get', 'AddPartition':'partitions.Add',
                    'DelPartition':'partitions.Del', 'AddReservation':'AddRes',
                    'DelReservation':'DelRes', 'Set':'Partition_Set'}
    __statefields__ = ['partitions']
    __schedcycle__ = 10
    __validate__ = False

    def __setup__(self):
        self.partitions = PartitionSet()
        self.jobs = []
        self.qmconnect = FailureMode("QM Connection")
        self.lastrun = 0

    def __progress__(self):
        since = time.time() - self.lastrun
        if since > self.__schedcycle__:
            self.RunQueue()
            self.lastrun = time.time()
        return 0
            
    def RunQueue(self):
        try:
            handle = self.comm.ClientInit('queue-manager')
        except:
            self.qmconnect.Fail()
            return 0
        self.qmconnect.Pass()
        self.comm.SendMessage(handle,
                              "<get-job><job nodes='*' location='*' user='*' jobid='*' state='*' walltime='*' queue='*'/></get-job>")
        jobs = self.comm.RecvMessage(handle)
        xjobs = XML(jobs)
        active = [job.get('jobid') for job in xjobs.findall(".//job")]
        for job in [j for j in self.jobs if j.get('jobid') not in active]:
            syslog(LOG_INFO, "Job %s/%s: gone from qm" % (job.get('jobid'),
                                                          job.get('user')))
            self.jobs.remove(job)
        # known is jobs that are already registered
        known = [job.get('jobid') for job in self.jobs]
        [partition.Free() for partition in self.partitions if partition.job not in known + ['none']]
        newjobs = [job for job in xjobs.findall('.//job') if job.get('jobid') not in known]
        self.jobs.extend([Job(job) for job in newjobs])
        placements = self.partitions.Schedule(xjobs.findall(".//job"))
        #print placements
        for (jobid, part) in placements:
            self.comm.SendMessage(handle,
                                  "<run-job nodelist='%s'><job jobid='%s'/></run-job>" %
                                  (part, jobid))
            self.comm.RecvMessage(handle)
        self.comm.ClientClose(handle)
        return 0

    def AddRes(self, xml, portinfo):
        '''Handler for addition of reservations'''
        return self.partitions.Get(xml, portinfo, self.AddRes_cb)

    def AddRes_cb(self, partition, args):
        '''Callback for reservation addition'''
        partition.AddReservation(args)
    
    def DelRes(self, xml, portinfo):
        '''Handler for reservation deletion'''
        return self.partitions.Get(xml, portinfo, self.DelRes_cb)

    def DelRes_cb(self, partition, args):
        '''Callback for reservation deletion'''
        partition.DelReservation(args['name'])

    def Partition_Set_cb(self, partition, args):
        '''Set partition fields callback'''
        partition.element.attrib.update(args)

    def Partition_Set(self, xml, portinfo):
        '''Set Partition Field'''
        return self.partitions.Get(xml, portinfo, self.Partition_Set_cb)

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arguments) = getopt(sys.argv[1:], 'C:d', ['daemon='])
    except GetoptError, msg:
        print "%s\nUsage:\nbgsched.py [-C configfile] [-d] [--daemon <pidfile>]" % (msg)
        raise SystemExit, 1
    daemon = [x[1] for x in opts if x[0] == '--daemon']
    debug = len([x for x in opts if x[0] == '-d'])
    if daemon:
        from sss.daemonize import daemonize
        daemonize(daemon[0])
    server = BGSched(debug=debug)
    server.ServeForever()
    

