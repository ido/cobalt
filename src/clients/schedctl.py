#!/usr/bin/env python

import sys
import Cobalt
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':
    try:
        sched = Cobalt.Proxy.ComponentProxy("scheduler")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to scheduler"
        sys.exit(1)

    if "--stop" in sys.argv:
        sched.disable()
    elif "--start" in sys.argv:
        sched.enable()
    elif "--reread-policy" in sys.argv:
        sched.define_user_utility_functions()
