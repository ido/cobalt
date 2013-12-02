#!/usr/bin/env python

'''Cobalt queue converter script'''
__revision__ = '$Revision$'

__helpmsg__ ="""This script converts queue and job data to the 0.96.0 format, and is
intended to be run after installing 0.96.0. It takes no arguments, and
makes a backup copy of the old cqm data in
'/var/spool/cobalt/cqm.save' and saves the new cqm data in
'/var/spool/cobalt/cqm'.

If you installed cqm.py in a location other than '/usr/sbin', then you
will need to modify line 6 of this script to reflect the location of
cqm.py.

Make sure there are no jobs running in the queue before you run this
script."""

import sys, cPickle, shutil

if '-h' in sys.argv or '--help' in sys.argv:
    print __helpmsg__
    raise SystemExit, 1

sys.path.append('/usr/sbin')
try:
    from cqm import BGJob, Timer, Logger, CommDict, JobSet, CQM, QueueSet, Queue
except:
    print '''Cannot find cqm.py. Please specify the directory where cqm.py can
be found in line 20 of this script, or in your $PYTHONPATH.'''
    raise SystemExit, 1

if __name__ == '__main__':

    # make backup of old pickle
    shutil.copyfile('/var/spool/cobalt/cqm', '/var/spool/cobalt/cqm.save')

    queue = cPickle.loads(open('/var/spool/cobalt/cqm').read())[0]
    if isinstance(queue, QueueSet):
        print '''Error, already converted cqm to 0.96.0 format. Replace
/var/spool/cobalt/cqm with old cqm data to try conversion again.'''
        raise SystemExit, 1

    newqueueset = QueueSet()
    newqueueset.__id__.idnum = queue.__id__.idnum
    print 'Set next jobid to be %d' % (queue.__id__.idnum + 1)

    for je in queue:
        # create queue if doesn't exist
        if je.get('queue') not in [q.get('name') for q in newqueueset]:
            newqueueset.Add([{'tag':'queue', 'name':je.get('queue')}])
            print "Created '%s' queue" % je.get('queue')

        [thisqueue] = [q for q in newqueueset if q.get('name') == je.get('queue')]
        response = thisqueue.append(je)
        print "Added job %s/%s to the '%s' queue" % (je.get('jobid'), je.get('user'), thisqueue.get('name'))

    savedata = tuple([newqueueset])
    cPickle.dump(savedata, open('/var/spool/cobalt/cqm', 'w'))
