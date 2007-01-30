#!/usr/bin/env python

'''This script removes reservations'''
__revision__ = '$Id$'
__version__ = '$Version$'

import getopt, sys
import Cobalt.Proxy

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "releaseres %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', [])
    except getopt.GetoptError, msg:
        print msg
        print "releaseres [--version] -p <partition> name"
        raise SystemExit, 1

    scheduler = Cobalt.Proxy.scheduler()
    if opts:
        spec = [{'tag':'partition', 'name':opts[0][1]}]
    else:
        spec = [{'tag':'partition', 'name':'*'}]
    print "Released reservation %s, matched on %d partitions" % \
          (args[0], len(scheduler.DelReservation(spec, args[0])))

    
