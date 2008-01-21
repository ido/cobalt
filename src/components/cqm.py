#!/usr/bin/env python

__revision__ = '$Revision$'

import cPickle

from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.base import run_component

try:
    try:
        cqm = cPickle.load(open('/var/spool/cobalt/cqm'))
    except:
        print "failed to restore state, creating new cqm object"
        cqm = QueueManager()
    run_component(cqm, register=True)
except KeyboardInterrupt:
    pass
