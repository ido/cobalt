#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = '$Revision$'

import getopt, os, pwd, sys, time
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

usehelp = "Usage:\ncqdel [-f] <jobid> <jobid>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqdel %s" % __revision__
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
    Cobalt.Logging.setup_logging('cqdel', to_syslog=False, level=level)
    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1
    spec = [{'tag':'job', 'user':user, 'jobid':jobid} for jobid in args]
    jobs = cqm.DelJobs(spec)
    time.sleep(1)
    print jobs
    if jobs:
        data = [('JobID','User')] + [(job.get('jobid'), job.get('user')) for job in jobs]
        print "      Deleted Jobs"
        Cobalt.Util.print_tabular(data)
    else:
        print "cqdel: Job %s not found" % sys.argv[-1]

