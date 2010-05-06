#!/usr/bin/env python

'''Cobalt queue release'''
__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

import getopt, os, pwd, sys, time
import xmlrpclib
import Cobalt.Logging, Cobalt.Util
import optparse
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

usehelp = "Usage:\nqrls [--version] <jobid> <jobid>"

if __name__ == '__main__':
    p = optparse.OptionParser(usage="%prog [options] <jobid> <jobid>",
            description="Removes user_hold state set by qhold.  Can instead clear job dependencies by using the --dependencies flag.")
    
    p.add_option("-v", "--version", action="store_true", dest="version", help="show version information")
    p.add_option("-d", action="store_true", dest="debug", help="debug level logging")
    p.add_option("--dependencies", action="store_true", dest="deps", help="clear all job dependencies")
    
    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args()

    if opt.version:
        print "qrls %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit(0)
    
    if len(args) < 1:
        p.print_help()
        sys.exit(1)
    
    level = 30
    if opt.debug:
        level = 10
    user = pwd.getpwuid(os.getuid())[0]
    Cobalt.Logging.setup_logging('qrls', to_syslog=False, level=level)
    logger = Cobalt.Logging.logging.getLogger('qrls')
    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)

    all_jobs = set()
    for i in range(len(args)):
        if args[i] == '*':
            continue
        try:
            args[i] = int(args[i])
            all_jobs.add(args[i])
        except:
            logger.error("jobid must be an integer")
            sys.exit(1)
        
    check_specs = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':'*'} for jobid in args]

    try:
        check_response = cqm.get_jobs(check_specs)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1

    jobs_existed = [j.get('jobid') for j in check_response]
    all_jobs = all_jobs.union(set(jobs_existed))
    update_specs = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':"*", 'is_active':"*"} for jobid in jobs_existed]
    
    if opt.deps:
        updates = {'all_dependencies': []}
    else:
        updates = {'user_hold':False}

    try:
        update_response = cqm.set_jobs(update_specs, updates)
    except xmlrpclib.Fault, flt:
        print flt.faultString
        raise SystemExit, 1
    
    if opt.deps:
        print "   Removed dependencies from jobs: "
        for j in update_response:
            print "      %s" % j.get("jobid")
        sys.exit(0)

    jobs_found = [j.get('jobid') for j in update_response]
    jobs_not_found = list(all_jobs.difference(set(jobs_existed)))
    jobs_completed = [j.get('jobid') for j in update_response if j.get('has_completed')] + \
        list(set(jobs_existed).difference(set(jobs_found)))
    jobs_had_hold = [j.get('jobid') for j in check_response if j.get('user_hold') and j.get('jobid') in jobs_found]
    jobs_active = [j.get('jobid') for j in update_response if j.get('is_active')]
    jobs_no_hold = list(set(jobs_found).difference(set(jobs_had_hold)))
    jobs_no_pending_hold = list(set(jobs_no_hold).intersection(set(jobs_active)))
    unknown_failures = [j.get('jobid') for j in update_response if j.get('user_hold') and
        j.get('jobid') not in jobs_completed + jobs_no_pending_hold + jobs_active]
    new_releases = [j.get('jobid') for j in update_response if not j.get('user_hold') and j.get('jobid') in jobs_had_hold]
    failed_releases = list(all_jobs.difference(set(new_releases)))

    if not check_response and not update_response:
        print "   No jobs found."
        logger.error("Failed to match any jobs")
    else:
        logger.debug("Response: %s" % (update_response,))

    if len(failed_releases) > 0:
        print "   Failed to remove user hold on jobs: "
        for jobid in failed_releases:
            if jobid in jobs_not_found:
                print "      job %s not found" % (jobid,)
            elif jobid in jobs_completed:
                print "      job %s has already completed" % (jobid,)
            elif jobid in jobs_no_pending_hold:
                print "      job %s is already active and does not have a pending 'user hold'" % (jobid,)
            elif jobid in jobs_active:
                print "      job %s is already active" % (jobid,)
            elif jobid in jobs_no_hold:
                print "      job %s does not have a 'user hold'" % (jobid,)
            elif jobid in unknown_failures:
                print "      job %s encountered an unexpected problem while attempting to release the 'user hold'" % (jobid,)
            else:
                assert False, "job %s not properly categorized" % (jobid,)

    if len(new_releases) > 0:
        print "   Removed user hold on jobs: "
        for jobid in new_releases:
            print "      %s" % (jobid,)
