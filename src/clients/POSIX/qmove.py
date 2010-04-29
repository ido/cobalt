#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time, xmlrpclib
import ConfigParser
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

usehelp = "Usage:\nqmove <queue name> <jobid> <jobid>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "qmove %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    if len(sys.argv) < 2:
        print usehelp
        raise SystemExit, 1
    try:
        queue = sys.argv[1]
        opts, args = getopt.getopt(sys.argv[2:], 'f')
    except getopt.GetoptError, gerr:
        print gerr
        print usehelp
        raise SystemExit, 1
    if len(args) < 1:
        print usehelp
        raise SystemExit, 1
    level = 30
    if '-d' in sys.argv:
        level = 10
    user = pwd.getpwuid(os.getuid())[0]
    Cobalt.Logging.setup_logging('qmove', to_syslog=False, level=level)
    logger = Cobalt.Logging.logging.getLogger('qmove')
    
    CP = ConfigParser.ConfigParser()
    CP.read(Cobalt.CONFIG_FILES)

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)

    for i in range(len(args)):
        if args[i] == '*':
            continue
        try:
            args[i] = int(args[i])
        except:
            logger.error("jobid must be an integer")
            raise SystemExit, 1
        
    spec = [{'tag':'job', 'user':user, 'jobid':jobid, 'project':'*', 'notify':'*',
             'walltime':'*', 'queue':'*', 'procs':'*', 'nodes':'*'} for jobid in args]

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []

    try:
        jobdata = cqm.get_jobs(spec)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1

    if not jobdata:
        print "Failed to match any jobs"
        sys.exit(1)

    response = []
    for jobinfo in jobdata:
        original_spec = jobinfo.copy()
        jobinfo.update({'queue': queue})
        for filt in filters:
            Cobalt.Util.processfilter(filt, jobinfo)
        try:
            [job] = cqm.set_jobs([original_spec], jobinfo)
            response.append("moved job %d to queue '%s'" % (job.get('jobid'), job.get('queue')))
        except xmlrpclib.Fault, flt:
            response.append(flt.faultString)

    if not response:
        logger.error("Failed to match any jobs or queues")
    else:
        logger.debug(response)
        for line in response:
            print line