#!/usr/bin/env python
# $Id$

import cPickle

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component

try:
    try:
        system = cPickle.load(open('/var/spool/cobalt/bgsystem'))
    except:
        print "failed to restore state, creating new bgsystem object"
        system = BGSystem()

    run_component(system, register=True)
except KeyboardInterrupt:
    pass
