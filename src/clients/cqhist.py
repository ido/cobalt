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
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

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
    parser.add_option( "-l", "--alldetails", default=False,
                       action="store_true", dest="alldetails",
                       help="show all job details" )

    parser.add_option( "-d", "--debug", default=False,
                       action="store_true", dest="debugging",
                       help="show debugging information" )

    # Get the options
    (options, args) = parser.parse_args()

    # default headers used for querying job history and output
    long_header = ("EndTime", "JobID", "User",
                   "WallTime", "QueuedTime", "RunTime",
                   "Queue",
                   "Procs", "Mode", "Location",
                   "Kernel", "Account", "Exit")
    header =      ("EndTime", "JobID", "User", "Queue",
                   "Procs", "Mode",
                   "RunTime",
                   "Exit")
    # -------------------------------------------------------------------------
    #
    # Execution
    #
    # -------------------------------------------------------------------------
    
    #
    # Get all of the jobs, directly accessing log files
    #
    query = dict()
    for item in long_header:
        query.update({item.lower():'*'})
#     try:
#         cqm = ComponentProxy("queue-manager", defer=False)
#         jobs = cqm.get_history([query])
#     except (ComponentLookupError):
#     print "Trouble connecting to queue manager, falling back to log files"
    cqp = cqparse.CobaltLogParser()
    cqp.perform_default_parse()
    jobs = cqp.q_get([query])

    jobs = [j.to_rx() for j in jobs]

    #
    # Get the statistics
    #
    if not options.noheader:
        print "Cobalt queue history (%i jobs):" % (len(jobs))

    #
    # Filter the jobs using the specified selection criteria
    #
    if options.username:
        jobs = [ job for job in jobs if job['user'] == options.username ]
    if options.queue:
        jobs = [ job for job in jobs if job['queue'] == options.queue ]

    # Now, sort the jobs
    js = [ (job['endtime'], job) for job in jobs ]
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
            print "%-19s %7s %-8s %-8s %10s %-8s %-10s %5s %4s %18s %6s %8s %4s" % long_header
        else:
            print "%s" % ( "-" * 78 )
            print "%-19s %7s %-8s %-10s %5s %4s %-8s %4s" % header
    

    # Print the job lines
    for job in jobs:
        if options.alldetails:

#             if job['queuetime'] > job['usertime']:
#                 wait_flag = "*"
#             else:
#                 wait_flag = " "
            wait_flag = " "
            print "%(endtime)19s %(jobid)7lu %(user)-8s %(walltime)-8s %(queuedtime)-10s %(runtime)-8s %(queue)-10s %(procs)5s %(mode)4s %(location)18s %(kernel)-6s %(account)8s %(exit)4s" % job
        else:
            output = [job.get(x, '-') for x in [y.lower() for y in header]]
            print "%(endtime)19s %(jobid)7lu %(user)-8s %(queue)-10s %(procs)5s %(mode)4s %(runtime)-8s %(exit)4s" % job
