#!/usr/bin/env python

'''This script removes reservations'''
__revision__ = '$Id$'
__version__ = '$Version$'

import getpass
import getopt, sys
import xmlrpclib

from Cobalt.Proxy import ComponentProxy, ComponentLookupError

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

    if not args:
        print "releaseres [--version] -p <partition> name"
        raise SystemExit, 1

    try:
        scheduler = ComponentProxy("scheduler", defer=False)
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1

    # Check if reservation exists
    try:
        result = scheduler.get_reservations([{'name':args[0]}])
    except xmlrpclib.Fault, flt:
        if flt.faultCode==1:
            print "Error communicating with queue manager"
            sys.exit(1)

    if not result:
        print "Reservation '%s' not found" % args[0]
        raise SystemExit, 1

    user = getpass.getuser()
    try:
        result = scheduler.del_reservations([{'name':args[0]}])
    except xmlrpclib.Fault, flt:
        if flt.faultCode==1:
            print "Error communicating with queue manager"
            sys.exit(1)

    print "Released reservation '%s', matched on %d partitions" % \
          (args[0], len(result))
