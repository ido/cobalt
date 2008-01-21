#!/usr/bin/env python

__revision__ = '$Revision: $'

import cPickle

from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import run_component

try:
    try:
        scheduler = cPickle.load(open('/var/spool/cobalt/bgsched'))
    except:
        print "failed to restore state, creating new bgsched object"
        scheduler = BGSched()

    run_component(scheduler)
except KeyboardInterrupt:
    pass
