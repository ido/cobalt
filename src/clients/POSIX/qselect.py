#!/usr/bin/env python

'''Cobalt qselect command'''
__revision__ = '$Revision: 559 $'
__version__ = '$Version$'

import os, sys, pwd, os.path, popen2, xmlrpclib, ConfigParser, re, logging
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

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
        raise SystemExit, 1

    if len(sys.argv) < 2:
        print helpmsg
        raise SystemExit, 1

    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('qselect', to_syslog=False, level=level)
    logger = logging.getLogger('qselect')

    CP = ConfigParser.ConfigParser()
    CP.read(['/etc/cobalt.conf'])
    
    failed = False

    jobspec = {'tag':'job'}
    query = {}
    if opts['nodecount']:
        try:
            nc = int(opts['nodecount'])
        except:
            logger.error("non-integer node count specified")
            raise SystemExit, 1
        query['nodes'] = opts['nodecount']
    else:
        query['nodes'] = '*'

    # ensure time is actually in minutes
    if opts['time']:
        if opts['time'].count(':') > 0:
            # process as a time
            #print "assuming seconds are not included in %s" % opts['time']
            units = opts['time'].split(':')
            units.reverse()
            totaltime = 0
            mults = [0, 1, 60]
            if len(units) > 3:
                logger.error("time too large")
                raise SystemExit, 1
            totaltime = sum([mults[index] * float(units[index]) for index in range(len(units))])
            logger.error("submitting walltime=%s minutes" % str(totaltime))
            opts['time'] = str(totaltime)
        try:
            numtime = float(opts['time'])
        except:
            logger.error("invalid time specification")
            raise SystemExit, 1
        if numtime <= 0:
            logger.error("invalid time specification")
            raise SystemExit, 1
        query['walltime'] = opts['time']
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
        cqm = ComponentProxy("queue-manager")

        query['tag'] = 'job'
        query['jobid'] = '*'
        response = cqm.get_jobs([query])

    except ComponentLookupError:
        logger.error("Can't connect to the queue manager")
        raise SystemExit, 1
    #except:
        #$logger.error("Error querying jobs")
        #raise SystemExit, 1
    # log jobid to stdout

    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs")
    else:
        Cobalt.Logging.logging.debug(response)
        print "   The following jobs matched your query:"
        for job in response:
            print "      %d" % job.get('jobid')
