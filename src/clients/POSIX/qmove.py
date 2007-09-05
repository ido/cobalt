#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time, xmlrpclib
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

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
    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1
    spec = [{'tag':'job', 'user':user, 'jobid':jobid} for jobid in args]
    updates = {}
    updates['queue'] = queue

    try:
        response = cqm.SetJobs(spec, updates)
    except xmlrpclib.Fault, flt:
        response = []
        if flt.faultCode == 30:
            print flt.faultString
            raise SystemExit, 1

    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs or queues")
    else:
        Cobalt.Logging.logging.debug(response)
        print "   Moved Jobs to queue: " + queue
        data = [(job.get('jobid'), job.get('user')) for job in response]
        for job in response:
            print "      " + job.get('jobid')

