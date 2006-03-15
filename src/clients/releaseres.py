#!/usr/bin/env python

'''This script removes reservations'''
__revision__ = '$Id$'

import getopt, sys
import Cobalt.Proxy

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', [])
    except getopt.GetoptError, msg:
        print msg
        print "releaseres -p <partition> name"
        raise SystemExit, 1

    scheduler = Cobalt.Proxy.scheduler()
    if opts:
        spec = [{'tag':'partition', 'name':opts[0][1]}]
    else:
        spec = [{'tag':'partition', 'name':'*'}]
    print scheduler.DelReservation(spec, name)

    
