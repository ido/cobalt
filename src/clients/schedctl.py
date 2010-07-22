#!/usr/bin/env python

import sys
import os
import optparse
import Cobalt
import getpass
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':
    p = optparse.OptionParser()
    
    p.add_option("--stop", action="store_true", dest="stop", help="stop scheduling jobs")
    p.add_option("--start", action="store_true", dest="start", help="resume scheduling jobs")
    p.add_option("--reread-policy", action="store_true", dest="reread", help="reread the utility function definition file")
    p.add_option("--savestate", dest="savestate", help="write the current state to the specified file")
    p.add_option("--score", dest="adjust", type="string", help="<jobid> <jobid> adjust the scores of the arguments")
    p.add_option("--inherit", dest="dep_frac", type="float", help="<jobid> <jobid> control the fraction of the score inherited by jobs which depend on the arguments")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    whoami = getpass.getuser()
    opt, args = p.parse_args()
    
    try:
        sched = Cobalt.Proxy.ComponentProxy("scheduler")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to scheduler"
        sys.exit(1)

    if opt.stop:
        sched.disable(whoami)
    elif opt.start:
        sched.enable(whoami)
    elif opt.reread:
        try:
            Cobalt.Proxy.ComponentProxy("queue-manager").define_user_utility_functions(whoami)
        except:
            print >> sys.stderr, "Failed to connect to queue manager"
            sys.exit(1)
    elif opt.savestate:
        try:
            directory = os.path.dirname(opt.savestate)
            if not os.path.exists(directory):
                print >> sys.stderr, "directory %s does not exist" % directory
                sys.exit(1)
            response = sched.save(opt.savestate)
        except Exception, e:
            print e
            sys.exit(1)
        else:
            print response

            
    # everything below here should operate on <jobid> arguments
    if not args:
        print >> sys.stderr, "must specify at least one jobid"
        sys.exit(1)
    for i in range(len(args)):
        if args[i] == '*':
            continue
        try:
            args[i] = int(args[i])
        except:
            print >> sys.stderr, "jobid must be an integer, found '%s'" % args[i]
            sys.exit(1)
    
    if opt.adjust:
        specs = [{'jobid':jobid} for jobid in args]
        
        try:
            new_score = opt.adjust
            float(new_score)
        except:
            print >> sys.stderr, "numeric argument expected for score adjustment, found '%s'" % opt.adjust
            sys.exit(1) 
        
        try:
            response = Cobalt.Proxy.ComponentProxy("queue-manager").adjust_job_scores(specs, new_score, whoami)
        except:
            print >> sys.stderr, "Failed to connect to queue manager"
            raise
            sys.exit(1)

        if not response:
            print "no jobs matched"
        else:
            dumb = [str(id) for id in response]
            print "updating scores for jobs: %s" % ", ".join(dumb)

    if opt.dep_frac:
        specs = [{'jobid':jobid} for jobid in args]
        
        try:
            response = Cobalt.Proxy.ComponentProxy("queue-manager").set_jobs(specs, {"dep_frac": opt.dep_frac}, whoami)
        except:
            print >> sys.stderr, "Failed to connect to queue manager"
            raise
            sys.exit(1)

        if not response:
            print "no jobs matched"
        else:
            dumb = [str(r["jobid"]) for r in response]
            print "updating inheritance fraction for jobs: %s" % ", ".join(dumb)
