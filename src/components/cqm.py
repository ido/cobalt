#!/usr/bin/env python

__revision__ = '$Revision$'

import cPickle as pickle
import sys
from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.base import run_component

def main ():
    try:
        cqm = pickle.load(open('/var/spool/cobalt/cqm'))
    except:
        print >> sys.stderr, "failed to restore state, creating new cqm object"
        cqm = QueueManager()
    run_component(cqm, register=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
