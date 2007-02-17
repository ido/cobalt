#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import math, os, re, sys, time, types
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

__helpmsg__ = "Usage: cqstat [-d] [-f] [-l] <jobid> <jobid>\n" + \
              "       cqstat [-d] -q <queue> <queue>\n" + \
              "       cqstat [--version]"

def get_elapsed_time(starttime, endtime):
    """
    returns hh:mm:ss elapsed time string from start and end timestamps
    """
    runtime = endtime - starttime
    minutes, seconds = divmod(runtime, 60)
    hours, minutes = divmod(minutes, 60)
    return ( "%02d:%02d:%02d" % (hours, minutes, seconds) )

def mergelist(locations):
    '''create a set of dashed-ranges from a node list'''
    uniq = []
    reg = re.compile('(\D+)(\d+)')
    [uniq.append(loc) for loc in locations if loc not in uniq]
    uniq.sort()
    retl = [[reg.match(uniq[0]).group(2)]]
    prefix = reg.match(uniq[0]).group(1)
    uniq = uniq[1:]
    while uniq:
        newnum = reg.match(uniq[0]).group(2)
        block = [item for item in retl if (int(item[0]) == int(newnum) + 1) 
                 or (int(item[-1]) == int(newnum) -1)]
        if block:
            block[0].append(newnum)
            block[0].sort()
        else:
            retl.append([newnum])
            uniq = uniq[1:]
    retnl = []
    for item in retl:
        if len(item) > 1:
            retnl.append("[%s%s-%s]" % (prefix, item[0], item[-1]))
        else:
            retnl.append("%s%s" % (prefix, item[0]))
    return ','.join(retnl)

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqstat %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    if '-h' in sys.argv or '--help' in sys.argv:
        print __helpmsg__
        raise SystemExit, 1

    options = {'d':'debug', 'f':'full', 'l':'long', 'version':'version',
               'q':'q'}
    doptions = {}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)
    level = 30
    if opts['debug']:
        level = 10

    if opts['version']:
        print "cqstat %s" % __revision__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('cqstat', to_syslog=False, level=level)

    jobid = None

    if len(args) > 0:
        names = args
    else:
        names = ["*"]

    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1

    if opts['q']:
        query = [{'tag':'queue', 'name':qname, 'users':'*', 
                  'mintime':'*', 'maxtime':'*', 'maxrunning':'*',
                  'maxqueued':'*', 'maxusernodes':'*',
                  'totalnodes':'*', 'state':'*'} for qname in names]
        header = [['Name', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                   'MaxQueued', 'MaxUserNodes', 'TotalNodes', 'State']]
        response = cqm.GetQueues(query)
    else:
        query = [{'tag':'job', 'user':'*', 'walltime':'*', 'nodes':'*',
                  'state':'*', 'jobid':jid, 'location':'*'} for jid in names]
        if opts['full']:
            for q in query:
                q.update({'mode':'*', 'procs':'*', 'queue':'*',
                          'starttime':'*', 'outputpath':'*', 'submittime':'*'
                          })
                if opts['long']:
                    q.update({'path':'*', 'outputdir':'*',
                              'envs':'*', 'command':'*', 'args':'*',
                              'kernel':'*', 'index':'*'})

            header = [['JobID', 'OutputPath', 'User', 'WallTime', 'QueuedTime',
                       'RunTime',
                       'Nodes', 'State', 'Location', 'Mode', 'Procs', 'Queue',
                       'StartTime', 'Index']]
            if opts['long']:
                header[0] += ['SubmitTime', 'Path', 'OutputDir', 'Envs', 'Command', 'Args', 'Kernel']
        else:
            header = [['JobID', 'User', 'WallTime', 'Nodes', 'State', 'Location']]
        response = cqm.GetJobs(query)

    if opts['q']:
        for q in response:
            if q.get('maxtime','*') != '*':
                q['maxtime'] = "%02d:%02d:00" % (divmod(int(q['maxtime']), 60))
            if q.get('mintime', '*') != '*':
                q['mintime'] = "%02d:%02d:00" % (divmod(int(q['mintime']), 60))
        output = [[q.get(x, '*') for x in [y.lower() for y in header[0]]] for q in response]
    else:
        if response:
            maxjoblen = max([len(item.get('jobid')) for item in response])
            jobidfmt = "%%%ss" % maxjoblen
        # next we cook walltime
        for j in response:
            t = int(j['walltime'].split('.')[0])
            h = int(math.floor(t/60))
            t -= (h * 60)
            j['walltime'] = "%02d:%02d:00" % (h, t)
            j['jobid'] = jobidfmt % j['jobid']
            if isinstance(j['location'], types.ListType) and len(j['location']) > 1:
                j['location'] = mergelist(j['location'])
            if opts['full']:
                if j.get('starttime') in ('-1', 'BUG', None):
                    j['starttime'] = 'N/A'   # StartTime
                    j['runtime'] = 'N/A'     # RunTime
                    j['queuedtime'] = get_elapsed_time(float(j['submittime']), time.time())
                else:
                    j['runtime'] = get_elapsed_time( float(j['starttime']), time.time())
                    j['queuedtime'] = get_elapsed_time(float(j['submittime']), float(j['starttime']))
                    j['starttime'] = time.strftime("%m/%d/%y %T", time.localtime(float(j['starttime'])))

                outputpath = j.get('outputpath')
                if outputpath == None:
                    j['outputpath'] = "-"
                else:
                    jobname = os.path.basename(outputpath).split('.output')[0]
                    if jobname != j['jobid'].split()[0]:
                        j['outputpath'] = jobname
                    else:
                        j['outputpath'] = "-"

                if opts['long']:
                    envs = j.get('envs', False)
                    if not envs:
                        j.update({'envs':''})
                    else:
                        j['envs'] = ' '.join([str(x) + '=' + str(y) for x, y in j['envs'].iteritems()])
                    j['args'] = ' '.join(j['args'])
                    j.update({'submittime':time.strftime("%m/%d/%y %T", time.localtime(float(j['submittime'])))})

        output = [[j.get(x) for x in [y.lower() for y in header[0]]]
                  for j in response]
        if opts['full']:
            # change column names
            header[0][ header[0].index('OutputPath') ] = "JobName"

    output.sort()
    if opts['long']:
        Cobalt.Util.print_vertical([tuple(x) for x in header + output])
    else:
        Cobalt.Util.print_tabular([tuple(x) for x in header + output])
