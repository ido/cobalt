#!/usr/bin/env python
# $Id$

import cPickle as pickle
import sys

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component

def main ():
    try:
        system = pickle.load(open('/var/spool/cobalt/bgsystem'))
    except:
        print >> sys.stderr, "failed to restore state, creating new bgsystem object"
        system = BGSystem()
    run_component(system, register=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
