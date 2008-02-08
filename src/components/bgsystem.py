#!/usr/bin/env python
# $Id$

import cPickle as pickle
import sys

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component, state_file_location

def main ():
    state_file = state_file_location() + "/bgsystem"
    try:
        system = pickle.load(open(state_file))
    except:
        print >> sys.stderr, "failed to restore state, creating new bgsystem object"
        system = BGSystem()
    system.statefile = state_file
    run_component(system, register=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
