#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time, xmlrpclib
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

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
        
    spec = [{'tag':'job', 'user':user, 'jobid':jobid} for jobid in args]

    try:
        response = cqm.move_jobs(spec, queue)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1

    if not response:
        logger.error("Failed to match any jobs or queues")
    else:
        logger.debug(response)
        print "   Moved Jobs to queue: " + queue
        for job in response:
            print "      %d" % job.get('jobid')

