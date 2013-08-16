#!/usr/bin/env python


from os import environ
from sys import stderr, stdout, argv, exit
from time import sleep
from random import randrange
import optparse


class AnyOptionParser(optparse.OptionParser):

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                optparse.OptionParser._process_args(self,largs,rargs,values)
            except (optparse.BadOptionError,optparse.AmbiguousOptionError), e:
                largs.append(e.opt_str)

def parse_options():

    parser = AnyOptionParser()

    parser.add_option("--fail", dest="exit_status", action="store", type="int")
    parser.add_option("--timeout", "-t", dest="timeout", action="store", type="int")


    opts, args = parser.parse_args(argv)

    return opts, args

if __name__ == '__main__':


    opts,args = parse_options()

    timeout = None
    if opts.timeout != None:
        timeout = opts.timeout
    print "timeout =", timeout

    exit_status = 0 #so we can make flags for non-zero statuses later.
    if opts.exit_status != None:
        exit_status = opts.exit_status

    print "exit_status =", exit_status

    print >> stdout, "Stdout: CHECK!"
    print >> stderr, '#' * 80
    print >> stderr, "Args:\n", "\n".join(argv)
    print >> stderr, '#' * 80
    print >> stderr, "Envs:\n", "\n".join(["%s=%s" %(key, val) for key, val in environ.iteritems()])

    #drop other diagnostics here
    if timeout != None:
        run_time = timeout
    else:
        run_time = randrange(90, 150)
    print "Starting simulator_run for %s seconds." % run_time
    sleep(run_time)
    print "run completed successfully!"

    if exit_status == 0:
        print >> stderr, "Exiting with status 0."
        exit(0)
    else:
        print >> stderr, "Like the Not-an-exit exit, I Fail!"
        print >> stderr, "Exiting with status %d." % opts.exit_status
        exit(opts.exit_status)

