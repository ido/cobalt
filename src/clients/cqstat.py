#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import math
import os
import re
import sys
import time
import types
import ConfigParser
import socket

import Cobalt
import Cobalt.Logging
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

__helpmsg__ = "Usage: cqstat [-d] [-f] [-l] [--sort <fields>] [--header <fields>] [--reverse] <jobid> <jobid>\n" + \
              "       cqstat [-d] -q <queue> <queue>\n" + \
              "       cqstat [--version]"


def human_format(x):
    # return x
    units = ['  ', ' K', ' M', ' G', ' T', ' P']
    dividend = 1000.0
    count = 0
    stuff = x

    while True:
        if stuff < dividend:
            return "%5.1f%s" % (max(stuff, 0.1), units[count])

        count += 1
        if count >= len(units):
            return "%5.1f%s" % (max(stuff, 0.1), units[-1])

        stuff = stuff / dividend
        
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
            uniq = uniq[1:]
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
        sys.exit(0)
    if '-h' in sys.argv or '--help' in sys.argv:
        print __helpmsg__
        sys.exit(0)

    options = {'d':'debug', 'f':'full', 'l':'long', 'version':'version',
               'q':'q', 'reverse':'reverse'}
    doptions = {'header':'header', 'sort':'sort'}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)

    # check for custom header, first in cobalt.conf, env, then in --header
    custom_header = None
    custom_header_full = None
    try:
        CP = ConfigParser.ConfigParser()
        CP.read(Cobalt.CONFIG_FILES)
        custom_header = CP.get('cqm', 'cqstat_header').split(':')
    except:
        pass
        
    try:
        custom_header_full = CP.get('cqm', 'cqstat_header_full').split(':')
    except:
        pass
    if 'QSTAT_HEADER' in os.environ.keys():
        custom_header = os.environ['QSTAT_HEADER'].split(':')
    elif 'CQSTAT_HEADER' in os.environ.keys():
        custom_header = os.environ['CQSTAT_HEADER'].split(':')
    if 'QSTAT_HEADER_FULL' in os.environ.keys():
        custom_header_full = os.environ['QSTAT_HEADER_FULL'].split(':')
    elif 'CQSTAT_HEADER_FULL' in os.environ.keys():
        custom_header_full = os.environ['CQSTAT_HEADER_FULL'].split(':')
    if opts['header']:
        custom_header = opts['header'].split(':')

    level = 30
    if opts['debug']:
        level = 10

    if opts['version']:
        print "cqstat %s" % __revision__
        sys.exit(0)
        
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
                      'Preemptable', 'Queue', 'StartTime', 'Index']
    long_header    = ['JobID', 'JobName', 'User', 'WallTime', 'QueuedTime',
                      'RunTime', 'Nodes', 'State', 'Location', 'Mode', 'Procs',
                      'Preemptable', 'User_Hold', 'Admin_Hold', 'Queue',
                      'StartTime', 'Index', 'SubmitTime', 'Path', 'OutputDir',
                      'Envs', 'Command', 'Args', 'Kernel', 'KernelOptions',
                      'Project', 'Dependencies', 'short_state', 'Notify', 'Score']
    header = None
    query_dependencies = {'QueuedTime':['SubmitTime', 'StartTime'], 'RunTime':['StartTime']}

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(2)

    if opts['q']:  # querying for queues
        query = [{'name':qname, 'users':'*', 
                  'mintime':'*', 'maxtime':'*', 'maxrunning':'*',
                  'maxqueued':'*', 'maxusernodes':'*',
                  'totalnodes':'*', 'state':'*', 'priority':'*'} for qname in names]
        header = ['Name', 'State', 'Users', 'MinTime', 'MaxTime',
                  'MaxRunning', 'MaxQueued', 'MaxUserNodes',
                  'TotalNodes', 'Priority']
        response = cqm.get_queues(query)
    else:
        if opts['full'] and opts['long']:
            header = long_header
        elif opts['full'] and custom_header_full:
            header = custom_header_full
        elif opts['full'] and not opts['long']:
            header = full_header
        elif custom_header:
            header = custom_header
        else:
            header = default_header

        # build query from long_header (all fields) and fetch response
        try:
            query = []
            for n in names:
                if n=='*':
                    query.append({'tag':'job', 'jobid':n})
                else:
                    query.append({'tag':'job', 'jobid':int(n)})
        except ValueError:
            print "jobids must be integers"
            sys.exit(2)
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
        
    if len(args) and not response:
        sys.exit(1)

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
            t = int(float(j['walltime']))
            h = int(math.floor(t/60))
            t -= (h * 60)
            j['walltime'] = "%02d:%02d:00" % (h, t)
            # jobid
            j['jobid'] = jobidfmt % j['jobid']
            # location
            if isinstance(j['location'], types.ListType) and len(j['location']) > 1:
                j['location'] = mergelist(j['location'])
            elif isinstance(j['location'], types.ListType) and len(j['location']) == 1:
                j['location'] = j['location'][0]
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
            
            # make the SubmitTime readable by humans
            j['submittime'] = time.ctime(float(j['submittime']))

        # any header that was not present in the query response has value set to '-'
        output = [[j.get(x, '-') for x in [y.lower() for y in header]]
                  for j in response]

    field = opts['sort'] or "JobID"
    fields = [f.lower() for f in field.split(":")]
    lower_case_header = [str(h).lower() for h in header]
    idxes = []
    for f in fields:
        try:
            idx = lower_case_header.index(f)
            idxes.append(idx)
        except ValueError:
            pass
    if not idxes:
        idxes.append(0)

    def _my_cmp(left, right):
        for idx in idxes:
            try:
                val = cmp(float(left[idx]), float(right[idx]))
            except:
                val = cmp(left[idx], right[idx])
            if val == 0:
                continue
            else:
                return val
    
        return 0
    
    output.sort(_my_cmp)
    
    if opts['reverse']:
        output.reverse()
    
    if "short_state" in lower_case_header:
        idx = lower_case_header.index("short_state")
        header[idx] = "S"
    
    if "score" in lower_case_header:
        idx = lower_case_header.index("score")
        for line in output:
            line[idx] = human_format(float(line[idx]))
        
    
    if opts['long']:
        Cobalt.Util.print_vertical([tuple(x) for x in [header] + output])
    else:
        Cobalt.Util.print_tabular([tuple(x) for x in [header] + output])
