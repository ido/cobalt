#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys
import cPickle as pickle

from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import run_component, state_file_location

def main ():
    state_file = state_file_location() + "/bgsched"
    try:
        scheduler = pickle.load(open(state_file))
    except:
        print >> sys.stderr, "failed to restore state, creating new bgsched object"
        scheduler = BGSched()
    scheduler.statefile = state_file
    run_component(scheduler)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
