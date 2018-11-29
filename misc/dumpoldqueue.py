#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import sys
import cPickle
sys.path.append('/usr/sbin')
from oldcqm import BGJob, Timer

queue = cPickle.loads(open('/var/spool/sss/cqm').read())[0]

print "cqadm.py -j %s" % (int(queue.idalloc.id) + 1)

for job in queue:
    je = job.element
    cmd = '''cd %s; env PATH=%s su %s -c "cqsub -q %s -n %s -m %s -k %s -t %s -O %s ''' % \
          (je.get('outputdir'), je.get('path'), je.get('user'), je.get('queue'),
           je.get('nodes'), je.get('mode'), je.get('kernel'), je.get('walltime'),
           je.get('outputdir'))
    if je.get('count') != None:
        cmd += " -c %s" % (je.get('count'))
    cmd += job.element.find('command').get('bin')
    cmd += " "
    cmd += job.element.find('command').get('args')
    cmd += '"'
    print cmd

