#!/usr/bin/env python

'''slp provides the service location protocol'''
__revision__ = '$Revision$'

from select import select, error as selecterror
from time import time
from xmlrpclib import Fault
import getopt
import sys

from Cobalt.Data import Data, DataSet
from Cobalt.Component import Component

import Cobalt.Logging

class Location(Data):
    '''Location class for service assertions'''

    def __init__(self, data):
        Data.__init__(self, data)

    def renew(self):
        '''Reassert service'''
        self.set('stamp', time())

    def expired(self):
        '''Detect expired service'''
        return (time() - self.get('stamp')) > 300

class Slp(Component, DataSet):
    '''slp provides a simple service location protocol implementation'''
    __name__ = 'service-location'
    __implementation__ = 'slp'
    __srvtimeout___ = 180
    __object__ = Location
    async_funcs = ['timeout_services']

    def __init__(self, setup):
        Component.__init__(self, setup)
        DataSet.__init__(self)
        self.register_function(self.assert_service, "AssertService")
        self.register_function(self.lookup_service, "LookupService")
        self.register_function(self.deassert_service, "DeassertService")

    def assert_service(self, address, data):
        '''Assert service with slp'''
        # first try to assert existing services
        retval = self.Get([data], lambda service, args:service.renew())
        if not retval:
            self.logger.info("Adding new service %s at %s" % (data['name'], data['url']))
            retval = self.Add([data])
        return retval

    def lookup_service(self, address, service):
        '''Lookup a service in the slp'''
        retval = self.Get(service)
        if not retval:
            raise Fault(11, "No Matching Service")
        return retval

    def deassert_service(self, address, spec):
        '''Remove service registration'''
        retval = self.Del(spec, lambda item,dummy:self.logger.info("Removed service %s at %s" %
                                                                   (item.get('name'), item.get('url'))))
        if not retval:
            raise Fault(11, "No Matching Service")
        return retval

    def timeout_services(self):
        '''Remove services that havent asserted in __svctimeout__'''
        for srv in [service for service in self.data if service.expired()]:
            self.logger.info("Flushing registration for component %s" % (srv.get('name')))
            self.data.remove(srv)

if __name__ == '__main__':
    try:
        (opts, arg) = getopt.getopt(sys.argv[1:], 'C:D:')
    except getopt.GetoptError, msg:
        print "%s\nUsage:\nslp.py [-D pidfile] [-C config file]" % (msg)
        raise SystemExit, 1

    configfile = ""
    daemon = False
    for item in opts:
        if item[0] == '-C':
            configfile = item[1]
        elif item[0] == '-D':
            daemon = item[1]
    if not configfile:
        configfile = '/etc/cobalt.conf'

    ssetup = {'debug':False, 'configfile':configfile, 'daemon':daemon}
    server = Slp(ssetup)
    Cobalt.Logging.setup_logging('slp', level=0)
    server.serve_forever()

