#!/usr/bin/env python -W ignore::DeprecationWarning

'''Cobalt qselect command'''
__revision__ = '$Revision: 559 $'
__version__ = '$Version$'

import os
import sys
import pwd
import os.path
import xmlrpclib
import ConfigParser
import re
import logging

import Cobalt
import Cobalt.Logging
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

helpmsg = """
Usage: qselect [-d] [-v] -A <project name> -q <queue> -n <number of nodes> 
               -t <time in minutes> -h <hold types> --mode <mode co/vn>
"""

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version'}
    doptions = {'n':'nodecount', 't':'time', 'A':'project', 'mode':'mode',
                'q':'queue', 'h':'held'}
    (opts, command) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)

    # need to filter here for all args
    if opts['version']:
        print "qselect %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit(1)

    if len(sys.argv) < 2:
        print helpmsg
        sys.exit(1)

    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('qselect', to_syslog=False, level=level)
    logger = logging.getLogger('qselect')

    CP = ConfigParser.ConfigParser()
    CP.read(Cobalt.CONFIG_FILES)
    
    failed = False

    jobspec = {'tag':'job'}
    query = {}
    if opts['nodecount']:
        try:
            nc = int(opts['nodecount'])
        except:
            logger.error("non-integer node count specified")
            sys.exit(1)
        query['nodes'] = opts['nodecount']
    else:
        query['nodes'] = '*'

    # ensure time is actually in minutes
    if opts['time']:
        try:
            minutes = Cobalt.Util.get_time(opts['time'])
        except Cobalt.Exceptions.TimeFormatError, e:
            print "invalid time specification: %s" % e.args[0]
            sys.exit(1)
        query['walltime'] = str(minutes)
    else:
        query['walltime'] = '*'

    user = pwd.getpwuid(os.getuid())[0]

    if opts['mode']:
        query['mode'] = opts['mode']
    else:
        query['mode'] = '*'

    if opts['project'] is not False:
        query['project'] = opts['project']
    else:
        query['project'] = '*'

    if opts['held']:
        query['state'] = opts['held']
    else:
        query['state'] = '*'
    
    if opts['queue']:
        query['queue'] = opts['queue']
    else:
        query['queue'] = '*'

    try:
        cqm = ComponentProxy("queue-manager", defer=False)

        query['tag'] = 'job'
        query['jobid'] = '*'
        response = cqm.get_jobs([query])

    except ComponentLookupError:
        logger.error("Can't connect to the queue manager")
        sys.exit(1)
    #except:
        #$logger.error("Error querying jobs")
        #sys.exit(1)
    # log jobid to stdout

    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs")
    else:
        Cobalt.Logging.logging.debug(response)
        print "   The following jobs matched your query:"
        for job in response:
            print "      %d" % job.get('jobid')
