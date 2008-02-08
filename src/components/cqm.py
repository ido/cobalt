#!/usr/bin/env python

__revision__ = '$Revision$'

import cPickle as pickle
import sys
from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.base import run_component, state_file_location

def main ():
    state_file = state_file_location() + "/cqm"
    try:
        cqm = pickle.load(open(state_file))
    except:
        print >> sys.stderr, "failed to restore state, creating new cqm object"
        cqm = QueueManager()
    cqm.statefile = state_file
    run_component(cqm, register=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
