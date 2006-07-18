#!/usr/bin/env python

'''query the slp daemon for component location information'''
__revision__ = '0.96'

from Cobalt.Util import print_tabular

import sys, time, xmlrpclib
import Cobalt.Logging, Cobalt.Proxy

if __name__ == '__main__':
    level = 20
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=level)
    slp = Cobalt.Proxy.service_location()
    try:
        locations = slp.LookupService([{'tag':'location', 'name':'*', 'stamp':'*', 'url':'*'}])
    except xmlrpclib.Fault, flt:
        if flt.faultCode == 11:
            print "No services registered"
            raise SystemExit, 0
        else:
            print "Unknown Fault %s" % (flt.faultString)
            raise SystemExit, 1

    fields = ['name', 'url', 'stamp']
    header = [('Name', 'Location', 'Update Time')]
    output = [[item[field] for field in fields] for item in locations]
    
    for item in output:
        item[2] = time.strftime("%c", time.localtime(item[2]))

    print_tabular(header + [tuple(item) for item in output])

