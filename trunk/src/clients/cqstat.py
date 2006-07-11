#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision$'

import getopt, math, sys, time, os
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

def get_elapsed_time(starttime, endtime):
    """
    returns hh:mm:ss elapsed time string from start and end timestamps
    """
    runtime = endtime - starttime
    minutes, seconds = divmod(runtime, 60)
    hours, minutes = divmod(minutes, 60)
    return ( "%02d:%02d:%02d" % (hours, minutes, seconds) )

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'dfq', ['version'])
    except getopt.GetoptError, msg:
        print "Usage: cqstat [--version] [-d] [-f jobid] [-q]"
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

    if '-q' in sys.argv:
        query = [{'tag':'queue', 'name':'*', 'users':'*', 
                  'mintime':'*', 'maxtime':'*', 'maxrunning':'*',
                  'maxqueued':'*', 'maxusernodes':'*',
                  'totalnodes':'*', 'state':'*'}]
        header = [['Name', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                   'MaxQueued', 'MaxUserNodes', 'TotalNodes', 'State']]
        response = cqm.GetQueues(query)
    else:
        query = [{'tag':'job', 'user':'*', 'walltime':'*', 'nodes':'*', 'state':'*', 'jobid':jobid_tosend, 'location':'*'}]
        if '-f' in sys.argv:
            query[0].update({'mode':'*', 'procs':'*', 'queue':'*', 'starttime':'*', 'outputpath':'*'})

            header = [['JobID', 'OutputPath', 'User', 'WallTime', 'RunTime', 'Nodes', 'State',
                       'Location', 'Mode', 'Procs', 'Queue', 'StartTime']]
        else:
            header = [['JobID', 'User', 'WallTime', 'Nodes', 'State', 'Location']]
        response = cqm.GetJobs(query)

    if '-q' in sys.argv:
        for q in response:
            if q.get('maxtime','*') != '*':
                q['maxtime'] = "%02d:%02d:00" % (divmod(int(q['maxtime']), 60))
            if q.get('mintime', '*') != '*':
                q['mintime'] = "%02d:%02d:00" % (divmod(int(q['mintime']), 60))
        output = [[q.get(x, '*') for x in [y.lower() for y in header[0]]] for q in response]
    else:
        output = [[job.get(x) for x in [y.lower() for y in header[0]]] for job in response]

        if output:
            maxjoblen = max([len(item[0]) for item in output])
            jobidfmt = "%%%ss" % maxjoblen
        # next we cook walltime
        for i in xrange(len(output)):
            t = int(output[i][ header[0].index('WallTime') ].split('.')[0])
            h = int(math.floor(t/60))
            t -= (h * 60)
            output[i][ header[0].index('WallTime') ] = "%02d:%02d:00" % (h, t)
            output[i][ header[0].index('JobID') ] = jobidfmt % output[i][ header[0].index('JobID') ]
            if '-f' in sys.argv:
                if output[i][ header[0].index('StartTime') ] in ('-1', 'BUG', None):
                    output[i][ header[0].index('StartTime') ] = 'N/A'   # StartTime
                    output[i][ header[0].index('RunTime') ] = 'N/A'     # RunTime
                else:
                    output[i][ header[0].index('RunTime') ] = \
                                      get_elapsed_time( float(output[i][ header[0].index('StartTime') ]), time.time())
                    output[i][ header[0].index('StartTime') ] = time.strftime("%m/%d/%y %T", \
                                                                              time.localtime(float(output[i][ header[0].index('StartTime') ])))
            if '-f' in sys.argv:
                outputpath = output[i][ header[0].index('OutputPath') ]

                if outputpath == None:
                    output[i][ header[0].index('OutputPath') ] = "-"
                else:
                    jobname = os.path.basename(outputpath).split('.output')[0]

                    if jobname != output[i][ header[0].index('JobID') ].split()[0]:
                        output[i][ header[0].index('OutputPath') ] = jobname
                    else:
                        output[i][ header[0].index('OutputPath') ] = "-"

        if '-f' in sys.argv:
            # change column names
            header[0][ header[0].index('OutputPath') ] = "JobName"

    output.sort()
    Cobalt.Util.print_tabular([tuple(x) for x in header + output])
