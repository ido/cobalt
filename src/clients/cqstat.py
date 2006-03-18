#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision$'

import getopt, math, sys, time
from datetime import datetime
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

def getElapsedTime(start, end):
    """
    returns hh:mm:ss elapsed time string from start and end timestamps
    """
    runtime = datetime.fromtimestamp( end ) - \
                 datetime.fromtimestamp( start )
    minutes, seconds = divmod(runtime.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return ( "%02d:%02d:%02d" % (hours, minutes, seconds) )

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'df', ['version'])
    except getopt.GetoptError, msg:
        print "Usage: cqstat [--version] [-d] [-f jobid]"
        print msg
        raise SystemExit, 1
    level = 30
    if '-d' in sys.argv:
        level = 10

    if '--version' in sys.argv:
        print "cqstat %s" % __revision__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('cqstat', to_syslog=False, level=level)

    jobid = None

    if len(args) > 0:
        jobid = args[0]

    if jobid:
        jobid_tosend = jobid
    else:
        jobid_tosend = "*"

    cqm = Cobalt.Proxy.queue_manager()
    query = [{'tag':'job', 'user':'*', 'walltime':'*', 'nodes':'*', 'state':'*', 'jobid':'*', 'location':'*'}]
    if '-f' in sys.argv:
        query[0].update({"mode":'*', 'procs':'*', 'queue':'*', 'starttime':'*'})
    jobs = cqm.GetJobs(query)

    header = [['JobID', 'User', 'WallTime', 'Nodes', 'State', 'Location']]
    if '-f' in sys.argv:
        header[0] += ['Mode', 'Procs', 'Queue', 'StartTime']

    output = [[job.get(x) for x in [y.lower() for y in header[0]]] for job in jobs]
    # add headers not used in query
    if '-f' in sys.argv:
        header[0].insert( header[0].index('WallTime') + 1, 'RunTime' )

    if output:
        maxjoblen = max([len(item[0]) for item in output])
        jobidfmt = "%%%ss" % maxjoblen
    # next we cook walltime
    for i in xrange(len(output)):
        t = int(output[i][2].split('.')[0])
        h = int(math.floor(t/60))
        t -= (h * 60)
        output[i][2] = "%02d:%02d:00" % (h, t)
        output[i][0] = jobidfmt % output[i][0]
        if '-f' in sys.argv:
            if output[i][9] == '-1' or output[i][9] == 'BUG' or output[i][9] == None:
                output[i][9] = 'N/A'   # StartTime
                output[i].insert( header[0].index('RunTime'), 'N/A' )  # RunTime
            else:
                output[i].insert( header[0].index('RunTime'),
                                  getElapsedTime( float(output[i][9]), time.time()) )
                output[i][10] = time.strftime("%m/%d/%y %T", time.localtime(float(output[i][10])))

    output.sort()
    Cobalt.Util.print_tabular([tuple(x) for x in header + output])
