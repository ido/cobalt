#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import math, os, re, sys, time, types, ConfigParser, socket
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

__helpmsg__ = "Usage: cqstat [-d] [-f] [-l] [--header] <jobid> <jobid>\n" + \
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
    doptions = {'header':'header'}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)

    # check for custom header, first in cobalt.conf, env, then in --header
    custom_header = None
    try:
        CP = ConfigParser.ConfigParser()
        CP.read(['/etc/cobalt.conf'])
        custom_header = CP.get('cqm', 'cqstat_header').split(':')
    except:
        pass
    if 'CQSTAT_HEADER' in os.environ.keys():
        custom_header = os.environ['CQSTAT_HEADER'].split(':')
    if opts['header']:
        custom_header = opts['header'].split(':')

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

    # define headers, long_header is used to query the queue-manager
    default_header = ['JobID', 'User', 'WallTime', 'Nodes', 'State', 'Location']
    full_header    = ['JobID', 'JobName', 'User', 'WallTime', 'QueuedTime',
                      'RunTime', 'Nodes', 'State', 'Location', 'Mode', 'Procs',
                      'Queue', 'StartTime', 'Index']
    long_header    = ['JobID', 'JobName', 'User', 'WallTime', 'QueuedTime',
                      'RunTime', 'Nodes', 'State', 'Location', 'Mode', 'Procs',
                      'Queue', 'StartTime', 'Index', 'SubmitTime', 'Path',
                      'OutputDir', 'Envs', 'Command', 'Args', 'Kernel', 'KernelOptions',
                      'Project']
    header = None
    query_dependencies = {'QueuedTime':['SubmitTime', 'StartTime'], 'RunTime':['StartTime']}

    try:
        cqm = ComponentProxy("queue-manager")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)

    if opts['q']:  # querying for queues
        query = [{'tag':'queue', 'name':qname, 'users':'*', 
                  'mintime':'*', 'maxtime':'*', 'maxrunning':'*',
                  'maxqueued':'*', 'maxusernodes':'*',
                  'totalnodes':'*', 'state':'*'} for qname in names]
        header = ['Name', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                  'MaxQueued', 'MaxUserNodes', 'TotalNodes', 'State']
        response = cqm.get_queues(query)
    else:
        if opts['full'] and not opts['long']:
            header = full_header
        elif opts['full'] and opts['long']:
            header = long_header
        elif custom_header:
            header = custom_header
        else:
            header = default_header

        # build query from long_header (all fields) and fetch response
        query = [{'tag':'job', 'jobid':n} for n in names]
        for q in query:
            for h in long_header:
                if h == 'JobName':
                    q.update({'outputpath':'*'})
                elif h != 'JobID':
                    q.update({h.lower():'*'})
                if h in query_dependencies.keys():
                    for x in query_dependencies[h]:
                        if x not in header:
                            q.update({x.lower():'*'})
        response = cqm.get_jobs(query)

    if opts['q']:
        for q in response:
            if q['maxtime'] is not None:
                q['maxtime'] = "%02d:%02d:00" % (divmod(int(q['maxtime']), 60))
            if q['mintime'] is not None:
                q['mintime'] = "%02d:%02d:00" % (divmod(int(q['mintime']), 60))
        output = [[q[x] for x in [y.lower() for y in header]] for q in response]
    else:
        if response:
            maxjoblen = max([len(str(item.get('jobid'))) for item in response])
            jobidfmt = "%%%ss" % maxjoblen
        # calculate derived values
        for j in response:
            # walltime
            t = int(j['walltime'].split('.')[0])
            h = int(math.floor(t/60))
            t -= (h * 60)
            j['walltime'] = "%02d:%02d:00" % (h, t)
            # jobid
            j['jobid'] = jobidfmt % j['jobid']
            # location
            if isinstance(j['location'], types.ListType) and len(j['location']) > 1:
                j['location'] = mergelist(j['location'])
            # queuedtime
            if j.get('starttime') in ('-1', 'BUG', 'N/A', None):
                j['queuedtime'] = get_elapsed_time(float(j.get('submittime')), time.time())
            else:
                j['queuedtime'] = get_elapsed_time(float(j.get('submittime')), float(j['starttime']))
            # runtime
            if j.get('starttime') in ('-1', 'BUG', 'N/A', None):
                j['runtime'] = 'N/A'
            else:
                j['runtime'] = get_elapsed_time( float(j['starttime']), time.time())
            # starttime
            if j.get('starttime') in ('-1', 'BUG', None):
                j['starttime'] = 'N/A'
            else:
                j['starttime'] = time.strftime("%m/%d/%y %T", time.localtime(float(j['starttime'])))
            # jobname
            outputpath = j.get('outputpath')
            if outputpath:
                jobname = os.path.basename(outputpath).split('.output')[0]
                if jobname != j['jobid'].split()[0]:
                    j['jobname'] = jobname
            # envs
            if j['envs'] is None:
                j.update({'envs':''})
            else:
                j['envs'] = ' '.join([str(x) + '=' + str(y) for x, y in j['envs'].iteritems()])
            # args
            j['args'] = ' '.join(j['args'])

        # any header that was not present in the query response has value set to '-'
        output = [[j.get(x, '-') for x in [y.lower() for y in header]]
                  for j in response]

    output.sort()
    if opts['long']:
        Cobalt.Util.print_vertical([tuple(x) for x in [header] + output])
    else:
        Cobalt.Util.print_tabular([tuple(x) for x in [header] + output])
