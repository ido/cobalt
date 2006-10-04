#!/usr/bin/env python

import time, sys
sys.argv.append('--nodb2')

import psyco
psyco.full()

from bgsched2 import JobSet, PartitionSet, ReservationSet, Event, BGSched


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
            'user':'desai'},
           {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'4',
            'state':'queued', 'walltime':40, 'queue':'default',
            'user':'voran'},
           {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'5',
            'state':'queued', 'walltime':10, 'queue':'default',
            'user':'nobody'}])

bs.reservations.Add([{'tag':'reservation', 'user':['nobody'], 'start':0,
                      'duration':150, 'location':['32wayN0'], 'recurrence':0}])

bs.partitions.Add([{'tag':'partition', 'name':x, 'size':y, 'functional':True, 'scheduled':True, 'queue':'default'} for x,y in [('32wayN0', '32'), ('32wayN1', '32')]])

bs.partitions.Add([{'tag':'partition', 'name':x, 'size':y, 'functional':False, 'scheduled':False, 'queue':'default'} for x,y in [('32wayN2', '32'), ('32wayN3', '32')]])

e_to_check = bs.jobs.ScanEvents() + bs.reservations.ScanEvents()# + [Event(10, 12, 'hard', 0)]

theschedule = bs.findBest([j for j in bs.jobs], e_to_check, [])

print 'schedule:'
print 'score: %s' % theschedule[0]
for job, location, time in theschedule[1]:
    print "Running job %s on partition %s at timestep %s for %s seconds" % \
          (job.get('jobid'), location.get('name'), time, job.get('walltime'))

# Reservations work
# Partition status works
# FIXME need to test partition cascading
