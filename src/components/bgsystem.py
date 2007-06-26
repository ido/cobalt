#!/usr/bin/env python
# $Id$

'''Cobalt System Component'''
__revision__ = '$Revision$'

from optparse import OptionParser

import logging, random, sys, ConfigParser, xmlrpclib
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

logger = logging.getLogger('bgsystem')

class System(Cobalt.Component.Component):
    __implementation__ = 'bgsys'
    __name__ = 'system'
    __statefields__ = [] #['projects']
    async_funcs = ['assert_location']

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        self.comms = Cobalt.Proxy.CommDict()
        self.register_function(self.start_job, "StartJob")
        self.register_function(self.query_part, "QueryPartition")

    def start_job(self, _, jobinfo):
        '''checks jobinfo against the allocation DB'''
        pass
    
    def query_part(self, _, jobinfo):
        '''updates allocation DB with job runtime'''
        pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", dest="debug", action="store_true", default=False,
                      help="Turn on debugging output")
    parser.add_option("-D", "--daemon", dest="daemon", default=False,
                      metavar="<pidfile>",
                      help="Run component as a daemon")
    (opts, args) = parser.parse_args()

    __daemon__ = opts.daemon
    __dlevel__ = logging.INFO
    if opts.debug:
        __dlevel__ = logging.DEBUG
    Cobalt.Logging.setup_logging('bgsystem', level = __dlevel__)
    logger = logging.getLogger('bgsystem')
    __server__ = System({'configfile':'/etc/cobalt.conf', 'daemon':__daemon__})
    __server__.serve_forever()
