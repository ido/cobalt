#!/usr/bin/env python

'''Cobalt Queue Status'''

__revision__ = '$Revision: 406 $'
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

__helpmsg__ = "Usage: qstat [-d] [-f] [-l] [--sort <fields>] [--header <fields>] [--schedinfo] [<jobid|queue> ...]\n" + \
              "       qstat [-d] -Q <queue> <queue>\n" + \
              "       qstat [--version]"

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
        print "qstat %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit(0)
    if '-h' in sys.argv or '--help' in sys.argv:
        print __helpmsg__
        sys.exit(0)

    options = {'d':'debug', 'f':'full', 'l':'long', 'version':'version',
               'Q':'Q', 'schedinfo':'schedinfo'}
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
    if 'CQSTAT_HEADER' in os.environ.keys():
        custom_header = os.environ['CQSTAT_HEADER'].split(':')
    elif 'QSTAT_HEADER' in os.environ.keys():
        custom_header = os.environ['QSTAT_HEADER'].split(':')
    if 'CQSTAT_HEADER_FULL' in os.environ.keys():
        custom_header_full = os.environ['CQSTAT_HEADER_FULL'].split(':')
    elif 'QSTAT_HEADER_FULL' in os.environ.keys():
        custom_header_full = os.environ['QSTAT_HEADER_FULL'].split(':')
    if opts['header']:
        custom_header = opts['header'].split(':')

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(2)
    
    try:
        queues = cqm.get_queues([{'name':"*", 'state':"*"}])
    except:
        print >> sys.stderr, "Failed to get queue list from queue manager"
        sys.exit(2)

    level = 30
    if opts['debug']:
        level = 10

    if opts['version']:
        print "qstat %s" % __revision__
        sys.exit(0)
        
    if opts['schedinfo']:
        print "The most recent scheduling attempt reports:\n"
        try:
            sched = ComponentProxy("scheduler", defer=False)
        except:
            print >> sys.stderr, "Failed to contact scheduler"
            sys.exit(2)
        jobs = cqm.get_jobs([{'jobid':"*", 'queue':"*", 'system_state':"*", 'user_state':"*", 'dependencies':"*"}])
        sched_info = sched.get_sched_info()

        for job in jobs:
            if len(args) > 0:
                if str(job['jobid']) not in args:
                    continue
                
            print "job", job['jobid'], ":"
            print "    ",
            if job['system_state'] == 'running':
                print "the job is running"
            elif job['system_state'] == 'hold' or job['user_state'] == 'hold':
                print "the job has a hold on it"
            elif job['dependencies']:
                print "the job has dependencies:", job['dependencies']
            elif [q['state'] for q in queues if q['name']==job['queue']][0] != 'running':
                print "the queue '%s' isn't running" % job['queue']
            elif sched_info.has_key(str(job['jobid'])):
                print sched_info[str(job['jobid'])]
            elif job['queue'].startswith("R."):
                res_name = job['queue'][2:]
                res_list = sched.get_reservations([{'name':res_name, 'active':"*"}])
                if res_list and not res_list[0]['active']:
                    print "the reservation '%s' is not active" % res_name
                else:
                    print "the job is waiting in an active reservation '%s'" % res_name
                
            else:
                print "maybe the potential locations for the job are blocked or busy?"
            
        if len(args) and not jobs:
            sys.exit(1)
        else:
            sys.exit(0)
        
    Cobalt.Logging.setup_logging('qstat', to_syslog=False, level=level)

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
                      'Project', 'Dependencies', 'short_state']
    header = None
    query_dependencies = {'QueuedTime':['SubmitTime', 'StartTime'], 'RunTime':['StartTime']}

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(2)

    if opts['Q']:  # querying for queues
        query = [{'name':qname, 'users':'*', 
                  'mintime':'*', 'maxtime':'*', 'maxrunning':'*',
                  'maxqueued':'*', 'maxusernodes':'*',
                  'totalnodes':'*', 'state':'*'} for qname in names]
        header = ['Name', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                  'MaxQueued', 'MaxUserNodes', 'TotalNodes', 'State']
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
                    query.append({'tag':'job', 'jobid':n, 'queue':'*'})
                elif [q['name'] for q in queues if q['name'] == n]:
                    query.append({'tag':'job', 'queue':n, 'jobid':'*'})
                else:
                    query.append({'tag':'job', 'jobid':int(n), 'queue':'*'})
        except ValueError:
            print "%s is not a valid jobid or queue name" % n
            sys.exit(2)
        for q in query:
            for h in long_header:
                if h == 'JobName':
                    q.update({'outputpath':'*'})
                elif h not in ['JobID', 'Queue']:
                    q.update({h.lower():'*'})
                if h in query_dependencies.keys():
                    for x in query_dependencies[h]:
                        if x not in header:
                            q.update({x.lower():'*'})
        response = cqm.get_jobs(query)
        
    if len(args) and not response:
        sys.exit(1)

    if opts['Q']:
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
    idxes = []
    for f in fields:
        try:
            idx = [str(h).lower() for h in header].index(f)
            idxes.append(idx)
        except ValueError:
            pass
    if not idxes:
        idxes.append(0)

    def _my_cmp(left, right):
        for idx in idxes:
            val = cmp(left[idx], right[idx])
            if val == 0:
                continue
            else:
                return val
    
        return 0
    
    output.sort(_my_cmp)
    
    if "short_state" in header:
        idx = header.index("short_state")
        header[idx] = "S"
    
    if opts['long']:
        Cobalt.Util.print_vertical([tuple(x) for x in [header] + output])
    else:
        Cobalt.Util.print_tabular([tuple(x) for x in [header] + output])
