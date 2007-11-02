#!/usr/bin/env python

'''This script removes reservations'''
__revision__ = '$Id$'
__version__ = '$Version$'

import getpass
import getopt, sys
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

    try:
        scheduler = ComponentProxy("scheduler")
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1
    if opts:
        spec = [{'tag':'partition', 'name':opts[0][1]}]
    else:
        spec = [{'tag':'partition', 'name':'*'}]

    # Check if reservation exists
    result = scheduler.GetPartition([{'tag':'partition', 'name':'*', 'reservations':'*'}])
    parts = []  # member partitions
    for r in result:
        if args[0] in [x[0] for x in r.get('reservations')]:
            parts.append(r.get('name'))
    if not parts:
        print "Reservation '%s' not found" % args[0]
        raise SystemExit, 1

    # delete reservation from member partitions
    if opts:
        spec = [{'tag':'partition', 'name':opts[0][1]}]
    else:
        spec = [{'tag':'partition', 'name':p} for p in parts]
    user = getpass.getuser()
    result = scheduler.DelReservation(spec, args[0], user)
    print "Released reservation '%s', matched on %d partitions" % \
          (args[0], len(result))
