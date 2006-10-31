#!/usr/bin/env python

import time, sys
sys.argv.append('--nodb2')

import psyco
psyco.full()

from bgsched2 import BGSched, Event, printSchedule


bs = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':False})
# jobs = JobSet()
# partitions = PartitionSet(1, 32)
# resv = ReservationSet()

bs.jobs.Add([{'tag':'job', 'nodes':'32', 'location':None, 'jobid':'1',
              'state':'queued', 'walltime':20, 'queue':'default',
              'user':'desai'},
             {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'2',
              'state':'queued', 'walltime':15, 'queue':'default',
              'user':'voran'},
             {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'3',
              'state':'queued', 'walltime':10, 'queue':'default',
              'user':'nobody'},
#              {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'4',
#               'state':'queued', 'walltime':40, 'queue':'default',
#               'user':'nobody'},
#              {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'5',
#               'state':'queued', 'walltime':10, 'queue':'default',
#               'user':'nobody'},
#              {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'6',
#               'state':'queued', 'walltime':43, 'queue':'default',
#               'user':'joe'}
             ])

# bs.reservations.Add([{'tag':'reservation', 'user':['nobody'], 'start':0,
#                       'duration':150, 'location':['32wayN0'], 'recurrence':0}])
# print bs.reservations.ScanEvents()

bs.partitions.Add([{'tag':'partition', 'name':x, 'size':y, 'functional':True, 'scheduled':True, 'queue':'default'} for x, y in [('32wayN0', '32'), ('32wayN1', '32')]])

# bs.partitions.Add([{'tag':'partition', 'name':x, 'size':y, 'functional':False, 'scheduled':False, 'queue':'default'} for x, y in [('32wayN2', '32'), ('32wayN3', '32')]])

e_to_check = bs.jobs.ScanEvents() + [Event(0, 0, 'hard', 0)] #bs.reservations.ScanEvents() #+ [Event(0, 0, 'hard', 0)]

t1 = time.time()
theschedule = bs.findBest([j for j in bs.jobs], e_to_check, [])
t2 = time.time()
print 'took %.3f seconds to find schedule' % (t2-t1)
print 'count', bs.routinecounter, bs.loopcounter

# print 'visited schedules\n'
# for v in bs.visitedschedules:
#     printSchedule(v)
# print
# print 'partial schedules\n'
# for p in bs.partialschedules:
#     printSchedule(p)

print 'schedule:'
print 'score: %s' % theschedule[0]
for job, location, tstep in theschedule[1]:
    print "Running job %s on partition %s at timestep %s for %s seconds" % \
          (job.get('jobid'), location.get('name'), tstep, job.get('walltime'))

# Reservations work
# Partition status works
# FIXME need to test partition cascading
