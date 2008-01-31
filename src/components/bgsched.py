#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys
import cPickle as pickle

from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import run_component

def main ():
    try:
        scheduler = pickle.load(open('/var/spool/cobalt/bgsched'))
    except:
        print >> sys.stderr, "failed to restore state, creating new bgsched object"
        scheduler = BGSched()
    run_component(scheduler)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
