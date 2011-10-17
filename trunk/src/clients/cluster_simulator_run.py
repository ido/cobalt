#!/usr/bin/env python


from os import environ
from sys import stderr, stdout, argv, exit
from time import sleep
from random import randrange
import getopt


def parse_options():


    opts, args = getopt.gnu_getopt(argv, "", ["fail=", "timeout="])

    print opts
    #parser = optparse.OptionParser()

    #parser.add_option("--fail", dest="exit_status", action="store", type="int")
    #parser.add_option("--timeout", "-t", dest="timeout", action="store", type="int")
    #print argv[1:] 
    
    #ret_tup = parser.parse_args(argv[2:])

    return opts, args

if __name__ == '__main__':


    #$opts,args = parse_options()
    

    exit_status = 0 #so we can make flags for non-zero statuses later.
    timeout = None
    
    print >> stdout, "Stdout: CHECK!"
    print >> stderr, '#' * 80
    print >> stderr, "Args:\n", "\n".join(argv)
    print >> stderr, '#' * 80
    print >> stderr, "Envs:\n", "\n".join(["%s=%s" %(key, val) for key, val in environ.iteritems()])

    #drop other diagnostics here
    if timeout == None:
        run_time = randrange(90, 150)
    else:
        run_time = opts.timeout
    print "Starting simulator_run for %s seconds." % run_time
    sleep(run_time)
    print "run completed successfully!"


    exit(0)
    
    if exit_status == None:
        print >> stderr, "Exiting with status 0."
        exit(0)
    else:
        print >> stderr, "Like the Not-an-exit exit, I Fail!"
        print >> stderr, "Exiting with status %d." % opts.exit_status
        exit(opts.exit_status)

