#!/usr/bin/env python

'''Cobalt queue release'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time
import xmlrpclib
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

usehelp = "Usage:\nqrls [--version] <jobid> <jobid>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "qrls %s" % __revision__
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
    Cobalt.Logging.setup_logging('qrls', to_syslog=False, level=level)
    logger = Cobalt.Logging.logging.getLogger('qrls')
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
        
    check_specs = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':'*'} for jobid in args]

    try:
        check_response = cqm.get_jobs(check_specs)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1

    jobs_existed = [j.get('jobid') for j in check_response]
    update_specs = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':"*", 'is_active':"*"} for jobid in jobs_existed]
    updates = {'user_hold':False}

    try:
        update_response = cqm.set_jobs(update_specs, updates)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1

    jobs_found = [j.get('jobid') for j in update_response]
    jobs_not_found = list(set(args).difference(set(jobs_existed)))
    jobs_completed = [j.get('jobid') for j in update_response if j.get('has_completed')] + \
        list(set(jobs_existed).difference(set(jobs_found)))
    jobs_had_hold = [j.get('jobid') for j in check_response if j.get('user_hold') and j.get('jobid') in jobs_found]
    jobs_active = [j.get('jobid') for j in update_response if j.get('is_active')]
    jobs_no_hold = list(set(jobs_found).difference(set(jobs_had_hold)))
    jobs_no_pending_hold = list(set(jobs_no_hold).intersection(set(jobs_active)))
    unknown_failures = [j.get('jobid') for j in update_response if j.get('user_hold') and
        j.get('jobid') not in jobs_completed + jobs_no_pending_hold + jobs_active]
    new_releases = [j.get('jobid') for j in update_response if not j.get('user_hold') and j.get('jobid') in jobs_had_hold]
    failed_releases = list(set(args).difference(set(new_releases)))

    if not check_response and not update_response:
        print "   No jobs found."
        logger.error("Failed to match any jobs")
    else:
        logger.debug("Response: %s" % (update_response,))

    if len(failed_releases) > 0:
        print "   Failed to remove user hold on jobs: "
        for jobid in failed_releases:
            if jobid in jobs_not_found:
                print "      job %d not found" % (jobid,)
            elif jobid in jobs_completed:
                print "      job %d has already completed" % (jobid,)
            elif jobid in jobs_no_pending_hold:
                print "      job %d is already active and does not have a pending 'user hold'" % (jobid,)
            elif jobid in jobs_active:
                print "      job %d is already active" % (jobid,)
            elif jobid in jobs_no_hold:
                print "      job %d does not have a 'user hold'" % (jobid,)
            elif jobid in unknown_failures:
                print "      job %d encountered an unexpected problem while attempting to release the 'user hold'" % (jobid,)
            else:
                assert False, "job %d not properly categorized" % (jobid,)

    if len(new_releases) > 0:
        print "   Removed user hold on jobs: "
        for jobid in new_releases:
            print "      %d" % (jobid,)
