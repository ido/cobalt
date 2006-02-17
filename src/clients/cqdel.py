#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = '$Revision$'

import os, pwd, sys, time
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqdel %s" % __revision__
    if len(sys.argv) < 2:
        print "Usage: cqdel -f <jobid>"
        raise SystemExit, 1
    level = 30
    if '-d' in sys.argv:
        level = 10
    user = pwd.getpwuid(os.getuid())[0]
    Cobalt.Logging.setup_logging('cqdel', to_syslog=False, level=level)
    cqm = Cobalt.Proxy.queue_manager()
    spec = [{'tag':'job', 'user':user, 'jobid':sys.argv[-1]}]
    jobs = cqm.DelJobs(spec)
    time.sleep(1)
    print jobs
    if jobs:
        data = [('JobID','User')] + [(job.get('jobid'), job.get('user')) for job in jobs]
        print "      Deleted Jobs"
        Cobalt.Util.print_tabular(data)
    else:
        print "cqdel: Job %s not found" % sys.argv[-1]

