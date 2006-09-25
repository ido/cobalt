#!/usr/bin/env python

from bgsched2 import JobSet, PartitionSet, ReservationSet, Event, BGSched
import time, sys

sys.argv.append('--nodb2')

def findPossible(jobs, events, tentative, depth):
    '''find possible'''
    print depth, 'starting findPossible', [j.get('jobid') for j in jobs], \
          [(e.start,e.duration) for e in events], \
          [(j.get('jobid'), p.get('name'), e) for j,p,e in tentative]
    
    if not jobs:
        print depth, 'empty', [(j.get('jobid'), p.get('name'), e) for j,p,e in tentative]
        score = evaluate(tentative)
        return (score, tentative)
    
    for job,event,part in [(j,e,p) for j in jobs for e in events for p in partitions]:
        print depth, 'checking event (', event.start, event.duration, ')'
        for e in [event.start, event.start + event.duration]:
            # check start of event
            if True: #self.CanRun(job, part, e, tentative):
                # add to tentative
                # recurse with that job event added?
                ten = tentative[:]
                ten.append((job, part, e))
                tempjobs = jobs[:]
                tempjobs.remove(job)
                #print 'tempjobs', [j.get('jobid') for j in tempjobs]
                (newscore, newschedule) = findPossible(tempjobs, events + [Event(e, job.get('walltime'), 'hard', 0)], ten, depth+1)
                if newschedule_score > best_score:
                    best_score = newscore
                    best_schedule = newschedule

    return (best_score, best_schedule)
                    
    print depth, 'best was', best
    print depth, 'tentative schedule', [(j.get('jobid'), p.get('name'), e) for j,p,e in tentative]
    return best

bs = BGSched({'configfile':'/etc/cobalt.conf', 'daemon':False})
# jobs = JobSet()
# partitions = PartitionSet(1, 32)
# resv = ReservationSet()

bs.jobs.Add([{'tag':'job', 'nodes':'32', 'location':None, 'jobid':'1',
              'state':'queued', 'walltime':20, 'queue':'default',
              'user':'nobody'},
             {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'2',
              'state':'queued', 'walltime':15, 'queue':'default',
              'user':'nobody'}])
#           {'tag':'job', 'nodes':'32', 'location':None, 'jobid':'3',
#            'state':'queued', 'walltime':10, 'queue':'default',
#            'user':'nobody'}])

bs.reservations.Add([{'tag':'reservation', 'user':'nobody', 'start':0,
                      'duration':15, 'location':'32wayN0', 'recurrence':0}])

bs.partitions.Add([{'tag':'partition', 'name':x, 'size':y, 'functional':True, 'scheduled':True, 'queue':'default'} for x,y in [('32wayN0', '32')]])#, ('32wayN1', '32')]])

e_to_check = bs.jobs.ScanEvents() + bs.reservations.ScanEvents()# + [Event(10, 12, 'hard', 0)]

theschedule = bs.findBest([j for j in bs.jobs], e_to_check, [])

print 'schedule:'
print 'score: %s' % theschedule[0]
for job, location, time in theschedule[1]:
    print "Running job %s on partition %s at timestep %s for %s seconds" % \
          (job.get('jobid'), location.get('name'), time, job.get('walltime'))
