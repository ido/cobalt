#!/usr/bin/env python

import sys
import optparse
import Cobalt
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':
    p = optparse.OptionParser()
    
    p.add_option("--stop", action="store_true", dest="stop", help="stop scheduling jobs")
    p.add_option("--start", action="store_true", dest="start", help="resume scheduling jobs")
    p.add_option("--reread-policy", action="store_true", dest="reread", help="reread the utility function definition file")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args()
    
    try:
        sched = Cobalt.Proxy.ComponentProxy("scheduler")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to scheduler"
        sys.exit(1)

    if opt.stop:
        sched.disable()
    elif opt.start:
        sched.enable()
    elif opt.reread:
        sched.define_user_utility_functions()
