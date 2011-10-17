#!/usr/bin/env python

import sys
import cPickle
sys.path.append('/usr/sbin')
#import oldcqm as cqm
from cqm import BGJob, Timer, Logger, CommDict, JobSet, CQM

queue = cPickle.loads(open('/var/spool/cobalt/cqm').read())[0]

#print dir(queue), queue.data
#print "cqadm.py -j %s" % (int(queue.idalloc.id) + 1)

for je in queue:
    #je = job.element

    if 'outputpath' in je._attrib:
        #myoutputpath = je.get('outputdir') + '/' + je.get('jobid')
        myoutputpath = je.get('outputpath').split('.output')[0]
        cmd = '''cd %s; env PATH=%s su %s -c "cqsub -q %s -n %s -m %s -k %s -t %s -O %s ''' % \
              (je.get('outputdir'), je.get('path'), je.get('user'),
               je.get('queue'), je.get('nodes'), je.get('mode'),
               je.get('kernel'), je.get('walltime').split('.')[0], myoutputpath)
    else:
        cmd = '''cd %s; env PATH=%s su %s -c "cqsub -q %s -n %s -m %s -k %s -t %s ''' % \
              (je.get('outputdir'), je.get('path'), je.get('user'),
               je.get('queue'), je.get('nodes'), je.get('mode'),
               je.get('kernel'), je.get('walltime').split('.')[0])
    if je.get('procs') != None:
        cmd += " -c %s " % (je.get('procs'))
        
    cmd += je.get('command')
    cmd += " "
    cmd += ' '.join(je.get('args'))
    cmd += '"'
    print cmd
    print

