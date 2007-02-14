#!/usr/bin/env python

'''Cobalt queue history command'''
__revision__ = '$Revision$'
__version__ = '$Version$'

#
# cqhist.py
# Extended Cobalt queue history
#
# Matthew Woitaszek
# 21 November 2006
#
# Portions of this file are based on the existing Cobalt qhist script developed
# by Argonne National Laboratory. Special thanks to Theron Voran for his
# assistance!
#

#
# This script prints Cobalt job history.
#

# Python imports
import sys
from optparse import OptionParser

# Application imports
import Cobalt.Cqparse as cqparse

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqhist %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    # -------------------------------------------------------------------
    #
    # Option Processing
    #
    # -------------------------------------------------------------------

    description = "Cobalt Queue History"
    usage = "usage: %prog [<options>]"
    parser = OptionParser(usage=usage, description=description)

    # Query selection options
    parser.add_option( "-u", "--user", default=None,
                       action="store", type="string", dest="username",
                       help="display only jobs from this user" )
    parser.add_option( "-q", "--queue", default=None,
                       action="store", type="string", dest="queue",
                       help="display only jobs from this queue" )


    # Output length
    parser.add_option( "-n", "--rows", default=20,
                       action="store", type="int", dest="lines",
                       help="output only the last LINES lines [default: %default]" )
    parser.add_option( "", "--noheader", default=False,
                       action="store_true", dest="noheader",
                       help="suppress all headers" )

    # Output options
    parser.add_option( "-a", "--alldetails", default=False,
                       action="store_true", dest="alldetails",
                       help="show all job details" )

    # Get the options
    (options, args) = parser.parse_args()

    # -------------------------------------------------------------------------
    #
    # Execution
    #
    # -------------------------------------------------------------------------
    
    #
    # Get all of the jobs
    #
    cqp = cqparse.CobaltLogParser()
    cqp.perform_default_parse()
    jobs = [ x for x in cqp.finished_jobs() ]

    #
    # Get the statistics
    #
    print "Cobalt queue history (%i jobs):" % (len(jobs))

    #
    # Filter the jobs using the specified selection criteria
    #
    if options.username:
        jobs = [ job for job in jobs if job.username == options.username ]
    if options.queue:
        jobs = [ job for job in jobs if job.queue == options.queue ]

    # Now, sort the jobs
    js = [ (job.finish_time, job) for job in jobs ]
    js.sort()
    jobs = [ job[1] for job in js ]

    # Finally, truncate the results  
    if options.lines:
        jobs = jobs[-abs(options.lines):]

    #
    # Print the standard output
    #

    # Print the header
    if not options.noheader:
        if options.alldetails:
            print "%-19s %7s %-10s %-8s %5s %4s %5s %18s %9s  %9s %8s %6s" % (
                "Termination Time", "Job ID", "Queue", "User",
                "ncpus", "mode", "nodes",
                "partition", "queuetime",
                "walltime", "cpuh", "Exit" )
        else:
            print "%s" % ( "-" * 78 )
            print "%-19s %6s %-10s %-8s %5s %4s %5s %8s %6s" % (
                "Termination Time", "Job ID", "Queue", "User",
                "ncpus", "mode", "nodes", "Walltime", "Exit")

    # Print the job lines
    for job in jobs:
        if options.alldetails:
            if job.queuetime > job.usertime:
                wait_flag = "*"
            else:
                wait_flag = " "

            print "%19s %7i %-10s %-8s %5i %4s %5i %18s %9s%s %9s %8.2f %6s" % (
                job.finish_time, job.jobid, job.queue, job.username,
                job.processors, job.mode, job.partition_size,
                job.partition, job.queuetime_formatted, wait_flag,
                job.usertime_formatted,
                job.partition_size * job.usertime / 3600, job.exitcode)        
        else:
            print "%19s %6i %-10s %-8s %5i %4s %5i %8s %6s" % (
                job.finish_time, job.jobid, job.queue, job.username,
                job.processors, job.mode, job.partition_size, 
                job.usertime_formatted, job.exitcode )

