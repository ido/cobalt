#!/usr/bin/env python

'''query the slp daemon for component location information'''
__revision__ = '$Revision$'
__version__ = '$Version$'

from Cobalt.Util import print_tabular

import sys
import time
import xmlrpclib
import socket

import Cobalt.Logging
from Cobalt.Proxy import ComponentProxy, ComponentLookupError


if __name__ == '__main__':
    
    if '--version' in sys.argv:
        print "slpstat %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit()
    
    if '-d' in sys.argv:
        level = 10
    else:
        level = 20
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=level)
    
    try:
        slp = Cobalt.Proxy.ComponentProxy("service-location", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "unable to find service-location"
        sys.exit(1)
    try:
        services = slp.get_services([{'tag':'service', 'name':'*', 'stamp':'*', 'location':'*'}])
    except socket.error, e:
        print >> sys.stderr, "unable to connect to service-locator (%s)" % (e)
        sys.exit(1)
    except xmlrpclib.Fault, e:
        print >> sys.stderr, "RPC fault (%s)" % (e)
        sys.exit(1)
    
    if services:
        header = [('Name', 'Location', 'Update Time')]
        output = [
            (
                service['name'],
                service['location'],
                time.strftime("%c", time.localtime(service['stamp']))
            )
            for service in services
        ]
        print_tabular(header + [tuple(item) for item in output])
    else:
        print "no services registered"
