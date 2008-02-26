#!/usr/bin/env python

'''Cobalt queue hold'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

usehelp = "Usage:\nqhold [--version] <jobid> <jobid>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "qhold %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f')
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
    Cobalt.Logging.setup_logging('qhold', to_syslog=False, level=level)
    logger = Cobalt.Logging.logging.getLogger('qhold')
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
        
    spec = [{'tag':'job', 'user':user, 'jobid':jobid, 'state':'queued'} for jobid in args]
    check_state_spec = [{'tag':'job', 'user':user, 'jobid':jobid, 'state':'*'} for jobid in args]
    
    updates = {}
    updates['state'] = "user hold"

    try:
        check_state = [j for j in cqm.get_jobs(check_state_spec) if j.get('state') != 'queued']
        response = cqm.set_jobs(spec, updates)
    except xmlrpclib.Fault, flt:
        response = []
        if flt.faultCode == 30:
            print flt.faultString
            raise SystemExit, 1

    if not response and not check_state:
        logger.error("Failed to match any jobs or queues")
    else:
        logger.debug(response)
        if check_state:
            print "   Failed to place user hold on jobs: "
            for job in check_state:
                if job.get('state') == 'user hold':
                    print "      job %d already in state 'user hold'" % job.get('jobid')
                else:
                    print "      job %d cannot be moved from state '%s'" % (job.get('jobid'), job.get('state'))
            print
        if response:
            print "   Placed user hold on jobs: "
            for job in response:
                print "      %d" % job.get('jobid')
    
