#!/usr/bin/env python

'''Scheduler for BG/L'''
__revision__ = '$Revision$'

import copy, logging, sys, time, xmlrpclib, ConfigParser, re
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

if '--nodb2' not in sys.argv:
    import DB2

logger = logging.getLogger('bgsched')

comm = Cobalt.Proxy.CommDict()

def printSchedule(sched):
    print 40*'='
    for item in sched:
        print item[0].get('jobid'), item[1].get('name'), item[2]
    print 40*'='

def GenerateUtilMetric(schedule):
    '''Generate Utilization metric for a given provisional schedule'''
    # schedule is (job, partition, start)
    filled = sum([int(sched[0].get('nodes')) * int(sched[0].get('walltime')) for sched in schedule])
    span = max([(float(sched[2]) + float(sched[0].get('walltime'))) for sched in schedule]) - \
           min([float(sched[0]) for sched in schedule])
    # FIXME get dynamic system size
    size = 1024.0
    return filled / (span * size)

def GenerateRespMetric(schedule):
    '''Generate System Responsiveness Metric'''
    # FIXME figure out how to measure system responsiveness
    return 1.0

def GenerateSpanMetric(schedule):
    '''Generate Span Metric for schedule
    This is the length (time) of a schedule'''
    # schedule is (job, partition, start)
    return 1/ max([(float(sched[2]) + float(sched[0].get('walltime'))) for sched in schedule]) - \
           min([float(sched[2]) for sched in schedule])

def Evaluate(schedule):
    '''Calculate the schedule metric'''
    return GenerateSpanMetric(schedule)

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

class Event:
    '''events describe an event in terms of start and duration'''
    def __init__(self, start, duration, status, recurrence):
        self.start = start
        self.duration = duration
        self.status = status
        self.recurrence = recurrence

    def __cmp__(self, other):
        return cmp(self.start, other.start)

class timeData(Cobalt.Data.Data):
    '''timeData is a class that can generate event traces for temporal ops'''
    def __init__(self, element):
        Cobalt.Data.Data.__init__(self, element)

    def getEvents(self):
        '''Return Duration events for self'''
        return []

class Reservation(timeData):
    '''This class represents reservations'''
    def __init__(self, element):
        timeData.__init__(self, element)

    def getEvents(self):
        '''Reservations are hard events'''
        return [Event(self.get('start'), float(self.get('duration')), 'hard', 0)]
        
class ReservationSet(Cobalt.Data.DataSet):
    '''This class holds the reservations'''
    __object__ = Reservation

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)

    def ScanEvents(self):
        '''ScanEvents returns a list of events describing activity'''
        events = []
        for reservation in self:
            events += reservation.getEvents()
        return events

    def isFree(set, location, starttime, jobspec):
        '''Checks for actions that would conflict with the proposed time'''
        for res in set.data:
            # A conflict occurs if the user is not in the userlist,
            # and the job time overlaps with the reservation, and the
            # location is in the reservation
            if location.get('name') in res.get('location') and \
                   jobspec.get('user') not in res.get('user'):
                if float(res.get('start')) <= starttime <= \
                       float(res.get('start') + res.get('duration')):
                    # job starts during reservation
                    return False
                if float(res.get('start')) <= (starttime + float(jobspec.get('walltime'))) <= \
                       float(res.get('start') + res.get('duration')):
                    # job ends during reservation
                    return False
        return True

class Job(timeData):
    '''This class represents User Jobs'''
    def __init__(self, element):
        timeData.__init__(self, element)
        self.partition = 'none'
        self.status = 'idle'
        logger.info("Job %s/%s: Found new job" % (self.get('jobid'), self.get('user')))
        self.start = -1
        self.eid = -1

    def getEvents(self):
        '''Get events corresponding to this instance'''
        if self.start != -1:
            etype = 'soft'
            if self.status == 'planned':
                etype = 'hard'
            return [Event(self.start, float(self.get('walltime')), etype, 0)]
        else:
            return []

    def Plan(self, start, location, eid):
        '''Set a tenative start time'''
        if self.start == -1:
            self.start = start
            self.status = 'planned'
            self.location = location
            self.eid = eid
        else:
            logger.error("Job %s: Attempted to run multiple times" % (self.get('jobid')))

    def Unplan(self, eid=-1):
        '''Remove scheduled execution'''
        if (eid == -1) or (eid < self.eid):
            self.start = -1
            self.location = None
            self.status = 'idle'
            oldid = self.eid
            self.eid = -1
            return oldid

    def Overlapped(self, location, start, duration):
        '''Test if job overlaps with a given locale'''
        if self.start == -1:
            return False
        if location == self.location:
            if self.start <= start <= (self.start + self.get('duration')):
                return False
            if self.start <= (start + duration) <= (self.start + self.get('duration')):
                return False
        return True

cqmFailed = FailureMode("QM Connection")

class JobSet(Cobalt.Data.DataSet):
    '''JobSet holds all current submitted jobs'''
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
                oldjob = self.Get([{'tag':'job', 'jobid':current.get('jobid')}])
                if not oldjob:
                    # job is new
                    self.Add([current])
                    continue
                else:
                    old = oldjob[0]
                    # job is modified
                    for key in [key for key in current._attrib if
                                key not in ['tag', 'jobid']]:
                        if old.get(key) != current.get(key):
                            logger.info("Updating field %s for job %s" % (key, current.get('jobid')))
                            old.set(key, current.get(key))
	# find finished jobs
        for job in self:
            if job.get('jobid') not in active:
                logger.info("Job %s has completed" % (job.get("jobid")))
                self.Del([{'tag':'job', 'jobid':job.get('jobid')}])
        self.lastrun = time.time()

    def ScanEvents(self):
        '''Provide an event stream for all current jobs'''
        events = []
        for job in self:
            events += job.getEvents()
        return events

    def isFree(self, location, starttime, jobspec, family):
        '''Checks for overlapping running jobs'''
        for rjob in [job for job in self if job.status == 'running']:
            # a conflicting job is running and overlaps with the new job
            # on a partition related to location
            if rjob.get('location') in family:
                if not ((float(starttime) > float(rjob.get('starttime')) + float(rjob.get('walltime')))
                        or
                        ((float(starttime) + float(jobspec.get('walltime')) < float(rjob.get('starttime'))))):
                    return False
        return True

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

class Base(Cobalt.Data.Data):
    '''Base block datatype'''

    pass

class BaseSet(Cobalt.Data.DataSet):
    '''Defines a BG/L system'''
    __object__ = Base
    __ncdefs__ = {'J102':'N0', 'J104':'N1', 'J106':'N2', 'J108':'N3',
                  'J111':'N4', 'J113':'N5', 'J115':'N6', 'J117':'N7',
                  'J203':'N8', 'J205':'N9', 'J207':'NA', 'J209':'NB',
                  'J210':'NC', 'J212':'ND', 'J214':'NE', 'J216':'NF'}

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

    def __init__(self, racks, psetsize):
        Cobalt.Data.DataSet.__init__(self)
        self.racks = racks
        self.psetsize = psetsize
        self.buildMachine()

    def getIONodes(self):
        '''Get location of i/o nodes from db2'''
        if '--nodb2' not in sys.argv:
            db2 = DB2.connect(uid=self.config.get('db2uid'),
                              pwd=self.config.get('db2pwd'), dsn=self.config.get('db2dsn')).cursor()

            db2.execute("SELECT LOCATION,IPADDRESS FROM tbglippool")
            results = db2.fetchall()
            ioreturn = [(location.strip(), ip) for (location, ip) in results]
            db2.close()
        else:
        #sample for 1:32 system
            ioreturn = [('R00-M1-NA-I:J18-U01', '172.30.0.53'),
                        ('R00-M1-NA-I:J18-U11', '172.30.0.54'),
                        ('R00-M1-NB-I:J18-U01', '172.30.0.55'),
                        ('R00-M1-NB-I:J18-U11', '172.30.0.56'),
                        ('R00-M1-NC-I:J18-U01', '172.30.0.57'),
                        ('R00-M1-NC-I:J18-U11', '172.30.0.58'),
                        ('R00-M1-ND-I:J18-U01', '172.30.0.59'),
                        ('R00-M1-ND-I:J18-U11', '172.30.0.60'),
                        ('R00-M1-NE-I:J18-U01', '172.30.0.61'),
                        ('R00-M1-NE-I:J18-U11', '172.30.0.62'),
                        ('R00-M1-NF-I:J18-U01', '172.30.0.63'),
                        ('R00-M1-NF-I:J18-U11', '172.30.0.64'),
                        ('R00-M1-N9-I:J18-U11', '172.30.0.52'),
                        ('R00-M0-N1-I:J18-U11', '172.30.0.4'),
                        ('R00-M0-N2-I:J18-U01', '172.30.0.5'),
                        ('R00-M0-N2-I:J18-U11', '172.30.0.6'),
                        ('R00-M0-N3-I:J18-U01', '172.30.0.7'),
                        ('R00-M0-N3-I:J18-U11', '172.30.0.8'),
                        ('R00-M0-N4-I:J18-U01', '172.30.0.9'),
                        ('R00-M0-N4-I:J18-U11', '172.30.0.10'),
                        ('R00-M0-N5-I:J18-U01', '172.30.0.11'),
                        ('R00-M0-N5-I:J18-U11', '172.30.0.12'),
                        ('R00-M0-N6-I:J18-U01', '172.30.0.13'),
                        ('R00-M0-N6-I:J18-U11', '172.30.0.14'),
                        ('R00-M0-N7-I:J18-U01', '172.30.0.15'),
                        ('R00-M0-N7-I:J18-U11', '172.30.0.16'),
                        ('R00-M0-N8-I:J18-U01', '172.30.0.17'),
                        ('R00-M0-N8-I:J18-U11', '172.30.0.18'),
                        ('R00-M0-N9-I:J18-U01', '172.30.0.19'),
                        ('R00-M0-N9-I:J18-U11', '172.30.0.20'),
                        ('R00-M0-NA-I:J18-U01', '172.30.0.21'),
                        ('R00-M0-NA-I:J18-U11', '172.30.0.22'),
                        ('R00-M0-NB-I:J18-U01', '172.30.0.23'),
                        ('R00-M0-NB-I:J18-U11', '172.30.0.24'),
                        ('R00-M0-NC-I:J18-U01', '172.30.0.25'),
                        ('R00-M0-NC-I:J18-U11', '172.30.0.26'),
                        ('R00-M0-ND-I:J18-U01', '172.30.0.27'),
                        ('R00-M0-ND-I:J18-U11', '172.30.0.28'),
                        ('R00-M0-NE-I:J18-U01', '172.30.0.29'),
                        ('R00-M0-NE-I:J18-U11', '172.30.0.30'),
                        ('R00-M0-NF-I:J18-U01', '172.30.0.31'),
                        ('R00-M0-N0-I:J18-U01', '172.30.0.1'),
                        ('R00-M0-N0-I:J18-U11', '172.30.0.2'),
                        ('R00-M0-N1-I:J18-U01', '172.30.0.3'),
                        ('R00-M0-NF-I:J18-U11', '172.30.0.32'),
                        ('R00-M1-N0-I:J18-U01', '172.30.0.33'),
                        ('R00-M1-N0-I:J18-U11', '172.30.0.34'),
                        ('R00-M1-N1-I:J18-U01', '172.30.0.35'),
                        ('R00-M1-N1-I:J18-U11', '172.30.0.36'),
                        ('R00-M1-N2-I:J18-U01', '172.30.0.37'),
                        ('R00-M1-N2-I:J18-U11', '172.30.0.38'),
                        ('R00-M1-N3-I:J18-U01', '172.30.0.39'),
                        ('R00-M1-N3-I:J18-U11', '172.30.0.40'),
                        ('R00-M1-N4-I:J18-U01', '172.30.0.41'),
                        ('R00-M1-N4-I:J18-U11', '172.30.0.42'),
                        ('R00-M1-N5-I:J18-U01', '172.30.0.43'),
                        ('R00-M1-N5-I:J18-U11', '172.30.0.44'),
                        ('R00-M1-N6-I:J18-U01', '172.30.0.45'),
                        ('R00-M1-N6-I:J18-U11', '172.30.0.46'),
                        ('R00-M1-N7-I:J18-U01', '172.30.0.47'),
                        ('R00-M1-N7-I:J18-U11', '172.30.0.48'),
                        ('R00-M1-N8-I:J18-U01', '172.30.0.49'),
                        ('R00-M1-N8-I:J18-U11', '172.30.0.50'),
                        ('R00-M1-N9-I:J18-U01', '172.30.0.51')]

        ioreturn.sort()

        # if only using 1 ionode per ionode processor card, filter out
        # every other entry in ioreturn
        if self.psetsize in [32, 128]:
            for i in ioreturn:
                if 'U11' in i[0]:
                    #print 'deleting', i
                    ioreturn.remove(i)
            
        return [re.sub('-I', '', i[0]) for i in ioreturn]

    def buildMachine(self):
        '''build machine representation from racks and psetsize'''
        ionodes = self.getIONodes()
        total_ionodes = (1024/self.psetsize) * self.racks  #total ionodes
        total_midplanes = self.racks * 2
        iopermidplane = total_ionodes/total_midplanes
        print 'total_ionodes: %d\ntotal_midplanes: %d\niopermidplane: %d' % \
              (total_ionodes, total_midplanes, iopermidplane)
        print 'length of ionodes', len(ionodes)
        q = total_ionodes
        while q > 0:
            print 'self.psetsize/q', self.psetsize/q

            for x in range(0, total_ionodes, q):
                #print 'io extent=%d, starting ionode is %d' % (q, x)
                if q == total_ionodes:
                    #print 'defining whole machine block'
                    base_type = 'full'
                    topology = 'torus'
                elif q < total_ionodes and q > iopermidplane*2:
                    base_type = 'multirack'
                    topology = 'torus'
                elif q == iopermidplane*2:
                    #print 'defining rack', x / (iopermidplane*2)
                    base_type = 'rack'
                    topology = 'torus'
                elif q == iopermidplane:
                    #print 'defining R%d M%d' % (x / (iopermidplane*2), (x / iopermidplane) % 2)
                    base_type = 'midplane'
                    topology = 'torus'
                else:
                    #print 'defining R%d M%d N%d' % (x/(iopermidplane*2), (x / iopermidplane) % 2, x % (iopermidplane))
                    base_type = 'block'
                    topology = 'mesh'

                includedIOn = [ionodes[y] for y in range(x, x+q)]
                computeNodes = q * self.psetsize
                rack = '%02d' % (x / (iopermidplane*2))
                midplane = '%d' % ((x / iopermidplane) % 2)
                self.Add([{'tag':'base', 'type':base_type, 'rack':rack, 'midplane':midplane,
                          'ionodes':includedIOn, 'computenodes':'%d' % computeNodes, 'psets':'%d' % q,
                          'state':'idle', 'topology':topology}])
            q = q / 2
        return

    def getMidplaneIONodes(self, rack, midplane):
        '''returns the ionodes in the midplane specified'''
        io = self.Get([{'tag':'base', 'rack':rack, 'midplane':midplane, 'ionodes':'*'}])
        if io:
            return io[0].get('ionodes')
        else:
            return None

class PartitionSet(Cobalt.Data.DataSet):
    '''PartitionSet contains all partitions'''
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

    def __init__(self, racks, psetsize):
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
        self.qmconnect = FailureMode("QM Connection")
        #TODO read racks and pset size from conf file
        self.basemachine = BaseSet(racks, psetsize)

    def __getstate__(self):
        return {'data':copy.deepcopy(self.data)}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.qmconnect = FailureMode("QM Connection")
        if '--nodb2' not in sys.argv:
            import DB2
            self.db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'),
                                   dsn=self.config.get('db2dsn')).cursor()

    def Add(self, cdata, callback=None, cargs=()):
        '''if adding a partition, fetches the ionodes for it
        and adds them as a field'''
        for datum in cdata:
            print 'datum', datum
            if datum.get('tag') == 'partition':
                #todo: check if datum.has_key('name')
                # fetch ionodes from DB for partition
                pionodes = self.getPartIONodes(datum.get('name'))
                print 'pionodes are', pionodes

                # from the ionodes, fill in the rest of the attributes from the base block
                for block in self.basemachine:
                    if len(pionodes) == len([p for p in pionodes if p in block.get('ionodes')]) \
                    and len(pionodes) == len(block.get('ionodes')):
                        baseblock = block
                        print 'block matches', block.get('ionodes')
                [datum.update({x:baseblock._attrib[x]}) for x in baseblock._attrib \
                 if not datum.has_key(x) and x != 'stamp']
#                 datum['functional'] = False
#                 datum['scheduled'] = False
                #datum.tag = 'partition'
                Cobalt.Data.DataSet.Add(self, [datum], callback, cargs)

    def getPartIONodes(self, partname):
        '''retrieves the IOnodes for the specified partition'''
        if '--nodb2' in sys.argv:
            iodict = {'32wayN0':['R00-M0-N0:J18-U01'],
                      '32wayN1':['R00-M0-N1:J18-U01'],
                      '32wayN2':['R00-M0-N2:J18-U01'],
                      '32wayN3':['R00-M0-N3:J18-U01'],
                      '64wayN01':['R00-M0-N0:J18-U01','R00-M0-N1:J18-U01'],
                      '64wayN23':['R00-M0-N2:J18-U01','R00-M0-N3:J18-U01'],
                      '128wayN0123':['R00-M0-N0:J18-U01','R00-M0-N1:J18-U01',
                                     'R00-M0-N2:J18-U01','R00-M0-N3:J18-U01']}
            return iodict.get(partname, None)

        ionodes = []
        db2 = DB2.connect(uid=self.config.get('db2uid'),
                          pwd=self.config.get('db2pwd'), dsn=self.config.get('db2dsn')).cursor()
        
        # first get blocksize in nodes
        db2.execute("select size from BGLBLOCKSIZE where blockid='%s'" % partname)
        blocksize = db2.fetchall()
        print 'blocksize is', blocksize[0][0], 'nodes'

        if int(blocksize[0][0]) < 512:
            print "small block"
            #tBGLSMALLBLOCK (BLOCKID, POSINMACHINE, PSETNUM, IONODEPOS, IONODECARD, IONODECHIP, COMPNODEPOS, NUMCOMPUTE)
            db2.execute("select * from tBGLSMALLBLOCK where blockid='%s' order by ionodepos" % partname)
            result = db2.fetchall()
            for b in result:
                rack = b[1].strip()[1:3]
                midplane = b[1].strip()[-1]
                ionodes.append("R%s-M%s-%s:%s-%s" % (rack, midplane, self.basemachine.__ncdefs__[b[3].strip()],
                                                     b[4].strip(), b[5].strip()))
        else:  #match up rack and midplane(s)?
            db2.execute("select bpid from TBGLBPBLOCKMAP where blockid='%s'" % partname)
            result = db2.fetchall()
            for b in result:
                rack = b[0].strip()[1:3]
                midplane = b[0].strip()[-1]
                print "R%s-M%s" % (rack, midplane)
                #ionodes = self.getIONodes(rack, midplane)
        db2.close()
        return ionodes

    def getParents(self, block):
        '''returns parents of partition, based on ionodes'''
        parents = [p for p in self.data
                   if len(block.get('ionodes')) == len([q for q in p.get('ionodes') if q in block.get('ionodes')])
                   and block.get('ionodes') != p.get('ionodes')]
        return parents

    def getChildren(self, block):
        '''returns children of partition, based on ionodes'''
        cionodes = block.get('ionodes')
        csize = len(cionodes)

        children = []
        for b in self.data:
            if len(b.get('ionodes')) < csize and [x for x in b.get('ionodes') if x in cionodes]:
                children.append(b)
        return children

    def isFree(self, partname):
        '''checks if partition is active/enabled'''
        for part in self:
            if part.get('name') == partname and part.get('scheduled') and \
                   part.get('functional') and part.get('state') == 'idle':
                return True
        return False

    def ScanEvents(self):
        '''Return events corresponding with administrative actions for partitions'''
        # FIXME implement PartitionSet.ScanEvents()
        return []

class AdminAction(timeData):
    '''machine actions, should have a location for the action'''
    def __init__(self, element):
        timeData.__init__(self, element)

    def getEvents(self):
        '''All admin actions are hard events'''
        return [Event(float(self.get('start')), float(self.get('duration')), 'hard',
                      float(self.get('recurrence')))]

class AdminActionSet(Cobalt.Data.DataSet):
    '''Holds online/offline actions for the machine (partitions and the like)'''
    __object__ = AdminAction

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)

    def ScanEvents(self):
        '''Generic event-grabbing'''
        events = []
        for action in self:
            events += action.getEvents()
        return events

    def isFree(self, location, starttime, duration):
        '''Checks for actions that would conflict with the proposed time'''
        for action in self:
            if action.get('location') == location.get('name'):
                if not ((float(starttime) > float(action.get('start')) + float(action.get('duration')))
                        or
                        ((float(starttime) + float(duration) < float(action.get('start'))))):
                    return False
        return True

class BGSched(Cobalt.Component.Component):
    '''This scheduler implements a fifo policy'''
    __implementation__ = 'bgsched2'
    __name__ = 'proto-scheduler'
    __statefields__ = ['partitions', 'jobs', 'reservations', 'actions']
    __schedcycle__ = 10
    async_funcs = ['assert_location']

    def __init__(self, setup):
        self.partitions = PartitionSet(1, 32)
        self.jobs = JobSet()
        self.reservations = ReservationSet()
        self.actions = AdminActionSet()
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
        self.routinecounter = 0
        self.loopcounter = 0
        self.visitedschedules = []
        self.partialschedules = []

    def AddReservation(self, _, spec, name, user, start, duration):
        '''Add a reservation to matching partitions'''
        reservation = (name, user, start, duration)
        robj = self.partitions.Get(spec, callback=lambda x, y:x.get('reservations').append(reservation))
        self.InvalidatePlanned(robj[0].get('location'), start, duration)
        return robj

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

    def CanRun(self, jobspec, location, starttime, tentative):
        '''
        Checks if a job (jobspec) can run, against current state of system,
        and against the tentative job schedule
        jobspec - job info
        location - partition object
        starttime - time that job is intended to be started
        tentative - [(job, partition, start)]
        '''
        family = [location.get('name')] + [p.get('name') for p in self.partitions.getParents(location)] + \
                 [p.get('name') for p in self.partitions.getChildren(location)]
        # check location
        if not location.CanRun({'queue':jobspec.get('queue'), 'nodes':jobspec.get('nodes')}):
            return False
        if not self.actions.isFree(location, starttime, jobspec.get('walltime')):
            return False

        # TODO check runtime queue restrictions
        
        # check for overlapping reservations
        if not self.reservations.isFree(location, starttime, jobspec):
            return False
        # check for overlapping running jobs
        if not self.jobs.isFree(location, starttime, jobspec, family):
            return False
        # check for overlapping tentative jobs
        for ten in tentative:
            if ten[1].get('name') in family:
                if not ((float(starttime) >= float(ten[2]) + float(ten[0].get('walltime')))
                    or
                    ((float(starttime) + float(jobspec.get('walltime')) <= float(ten[2])))):
                    return False
        return True

    def InvalidatePlanned(self, location, start, duration):
        '''Unplan events that have been impacted by system events'''
        ids = [job.Unplan() for job in self.jobs if job.Overlaps(location, start, duration)]
        # invalidate all provisional events newer than oldest invalid one
        [job.Unplan(min(ids)) for job in self.jobs]

    def Schedule(self):
        '''Perform all periodic scheduling work'''
        self.jobs.Sync()
        # call the recursive checker to produce a list of options
        e_to_check = self.jobs.ScanEvents() + self.partitions.ScanEvents() + self.actions.ScanEvents()
        j_to_check = [j for j in self.jobs if j.get('state') == 'queued']

        (_, newschedule) = self.findBest(j_to_check, e_to_check, [])
        for (job, location, evt) in newschedule:
            job.Plan(location, evt.start)
            # FIXME need to make sure that job start requests happen at the right time

    def findBest(self, jobs, events, tentative, depth=0):
        '''find best schedule using DFS and our metrics'''
        # at leaf node, evaluate tentative schedule
        #print "J:", ', '.join([j.get('jobid') for j in jobs])
        #print "E:", [(e.start, e.duration) for e in events]
        #print "T:", ["%s->%s" % (t[0].get('jobid'), t[1].get('name')) for t in tentative]
        #raw_input()
        # find all possible run combos for job
        best_score = -1
        best_schedule = []
        # do a pointwise uniq on events
        uevt = []
        [uevt.append(item) for event in events for item in \
         [event.start, event.start + event.duration] if item not in uevt]
        uevt.sort()

        self.routinecounter += 1
        #print depth, ':', len([j for j in jobs]) * len(uevt) * len([p for p in self.partitions])
        print 'events to check', [uevt]
        for job, event, part in [(j, e, p) for j in jobs for e in uevt for p in self.partitions]:
            self.loopcounter += 1
            # check if schedule that led us to job has already been
            # visited in one form or another
            if tentative in self.partialschedules:
                print 'this %d-level schedule already found:' % len(tentative), 
                print 'pruning branch', ["%s,%s,%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in tentative] # + [(job, part, event)]]
                return None, []
            print depth, ": Checking ===>", "j%s" % job.get('jobid'), event, part.get('name'), "to", ["%s,%s,%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in tentative], '...',
            if self.CanRun(job, part, event, tentative):
                print 'canrun'
                #print depth, ": Adding ===>", "j%s" % job.get('jobid'), event, part.get('name'), "to", ["%s->%s@%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in tentative]
                # add to tentative, recurse with that job event added
                # remove job from potential jobs list
                ten = tentative[:]
                ten.append((job, part, event))
                ten.sort()

#                 for p in self.partialschedules:
#                     print 'partials', ["%s,%s,%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in p]

                #printSchedule(ten)
                njobs = [j for j in jobs if j != job]
                if not njobs:
                    # check if the schedule has already been visited
                    if ten in self.visitedschedules:
                        print 'Schedule already found, length', len(ten)
                        continue
                    self.visitedschedules.append(ten)
                    #print 'schedules visited', len(self.visitedschedules)
                    #print 'sched to eval is', ["%s->%s@%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in ten]
                    newschedule = ten
                    print 'running eval'
                    newscore = Evaluate(newschedule)
                    #print 'eval is', newscore
                else:
                    (newscore, newschedule) = \
                               self.findBest(njobs, events + \
                                             [Event(event, job.get('walltime'), 'hard', 0)], ten, depth = depth+1)
                if newscore != None and newscore > best_score:
                    best_score = newscore
                    best_schedule = newschedule

                # add ten to partialschedules on the way out
                if len(ten) > 1 and ten not in self.partialschedules:
                    print '%d : adding ten to partialschedules' % len(ten), ["%s,%s,%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in ten]
                    printSchedule(ten)
                    self.partialschedules.append(ten)

            else:
                print 'bad'
                
#         print 'partial schedules'
#         for s in self.partialschedules:
#             print ["%s->%s@%d" % (t[0].get('jobid'), t[1].get('name'), t[2]) for t in s]
        return (best_score, best_schedule)

    def StartJobs(self):
        '''Start jobs whose start time has passed'''
        pass

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (OPTS, ARGS) = getopt(sys.argv[1:], 'C:dD:t', ['nodb2'])
    except GetoptError, msg:
        print "%s\nUsage:\nbgsched.py [-t] [-C configfile] [-d] [-D <pidfile>] [--nodb2]" % (msg)
        raise SystemExit, 1
    try:
        DAEMON = [X[1] for X in OPTS if X[0] == '-D'][0]
    except:
        DAEMON = False
    if len([X for X in OPTS if X[0] == '-d']):
        DLEVEL = logging.DEBUG
    else:
        DLEVEL = logging.INFO
    Cobalt.Logging.setup_logging('bgsched', level=DLEVEL)
    SERVER = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':DAEMON})
    SERVER.serve_forever()
    

