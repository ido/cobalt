#!/usr/bin/env python

'''Cobalt queue converter script'''
__revision__ = '$Revision: $'

import sys, cPickle, shutils
sys.path.append('/usr/sbin')
from cqm import BGJob, Timer, Logger, CommDict, JobSet, CQM, QueueSet, Queue

if __name__ == '__main__':

    # make backup of old pickle
    shutils.copyfile('/var/spool/cobalt/cqm', '/var/spool/cobalt/cqm.save')

    queue = cPickle.loads(open('/var/spool/cobalt/cqm').read())[0]

    newqueueset = QueueSet()
    newqueueset.__id__.idnum = queue.__id__.idnum

    for je in queue:
        # create queue if doesn't exist
        if je.get('queue') not in [q.get('name') for q in newqueueset]:
            newqueueset.Add([{'tag':'queue', 'name':je.get('queue')}])

        # add job to queue
        je._attrib.update({'tag':'job'})

        # set job's jobid
        [thisqueue] = [q for q in newqueueset if q.get('name') == je.get('queue')]
        [response] = thisqueue.Add(je._attrib)
        [thisjob] = [j for j in thisqueue if j.get('jobid') == response.get('jobid')]
        thisjob.set('jobid', je.get('jobid'))

    savedata = tuple([newqueueset])
    cPickle.dump(savedata, open('/var/spool/cobalt/cqm', 'w'))
