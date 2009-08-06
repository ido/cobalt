#!/usr/bin/env python

import sys
import os
import optparse
import Cobalt
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':
    p = optparse.OptionParser()
    
    p.add_option("--stop", action="store_true", dest="stop", help="stop scheduling jobs")
    p.add_option("--start", action="store_true", dest="start", help="resume scheduling jobs")
    p.add_option("--reread-policy", action="store_true", dest="reread", help="reread the utility function definition file")
    p.add_option("--savestate", dest="savestate", help="write the current state to the specified file")
    p.add_option("--adjust-score", action="store_true", dest="adjust", help="<jobid> <jobid> [+,-- -]score")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args()
    
    try:
        sched = Cobalt.Proxy.ComponentProxy("scheduler")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to scheduler"
        sys.exit(1)

    if opt.stop:
        sched.disable()
    elif opt.start:
        sched.enable()
    elif opt.reread:
        try:
            Cobalt.Proxy.ComponentProxy("queue-manager").define_user_utility_functions()
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
    elif opt.adjust:
        if len(args) < 2:
            print >> sys.stderr, "must specify at least one jobid and a score adjustment"
            sys.exit(1)
        jobids = args[:-1]
        for i in range(len(jobids)):
            if jobids[i] == '*':
                continue
            try:
                jobids[i] = int(jobids[i])
            except:
                print >> sys.stderr, "jobid must be an integer, found '%s'" % jobids[i]
                sys.exit(1)
    
        specs = [{'jobid':jobid} for jobid in jobids]
        
        try:
            new_score = args[-1]
            float(new_score)
        except:
            print >> sys.stderr, "numeric argument expected for score adjustment, found '%s'" % args[-1]
            sys.exit(1) 
        
        try:
            response = Cobalt.Proxy.ComponentProxy("queue-manager").adjust_job_scores(specs, new_score)
        except:
            print >> sys.stderr, "Failed to connect to queue manager"
            raise
            sys.exit(1)

        if not response:
            print "no jobs matched"
        else:
            print "updating scores for jobs:",
            for id in response:
                print id,  

