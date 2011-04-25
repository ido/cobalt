#!/usr/bin/env python


from os import environ
from sys import stderr, stdout, argv, exit
from time import sleep
from random import randrange

if __name__ == '__main__':

    exit_status = 0 #so we can make flags for non-zero statuses later.

    print >> stderr, '#' * 80
    print >> stderr, "Args:\n", "\n".join(argv)
    print >> stderr, '#' * 80
    print >> stderr, "Envs:\n", "\n".join(["%s=%s" %(key, val) for key, val in environ.iteritems()])

    #drop other diagnostics here

    run_time = randrange(90, 150)
    print "Starting simulator_run for %s seconds." % run_time
    sleep(run_time)
    print "run completed successfully!"

    exit(exit_status)

