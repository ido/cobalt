#!/usr/bin/env python
"""
Cobalt Queue Status

Usage: %prog [options] <jobids1> ... <jobidsN>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn non communication debugging',callback=cb_debug
'-f','--full',dest='full',help='show more verbose information',action='store_true'
'-l','--long',dest='long',help='show job info in vertical format',action='store_true'
'-Q',dest='Q',help='show queues and properties',action='store_true'
'--reverse',dest='reverse',help='show output in reverse',action='store_true'

Option with values:

'--header',dest='header',type='string',help='specify custom header',callback=cb_split
'--sort',dest='sort',type='string',help='sort output by specified attribute',callback=cb_split
'-u','--user',dest='user',type='string',help='Specify username'

"""
import math
import os
import sys
import time
import types
import logging
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_split

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 406 $'
__version__ = '$Version$'

QUEMGR = client_utils.QUEMGR

def human_format(x):
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

def get_output_for_queues(parser,hinfo):
    """
    get the queues info for the specified queues
    """

    names = parser.args if not parser.no_args() else ['*']

    query = [{'name':qname,'users':'*','groups':'*','mintime':'*','maxtime':'*','maxrunning':'*','maxqueued':'*','maxusernodes':'*',
              'maxnodehours':'*','totalnodes':'*','state':'*'} for qname in names]
    response = client_utils.component_call(QUEMGR, True, 'get_queues', (query,))

    if not parser.no_args() and not response:
        sys.exit(1)

    for q in response:
        if q['maxtime'] is not None:
            q['maxtime'] = "%02d:%02d:00" % (divmod(int(q['maxtime']), 60))
        if q['mintime'] is not None:
            q['mintime'] = "%02d:%02d:00" % (divmod(int(q['mintime']), 60))

    output = [[q[x] for x in [y.lower() for y in hinfo.header]] for q in response]

    return output

def get_output_for_jobs(parser,hinfo,queues):
    """
    get jobs from specified jobids
    """
    names              = parser.args if not parser.no_args() else ['*']
    user_name          = parser.options.user if parser.options.user != None else '*'
    query_dependencies = {'QueuedTime':
                              ['SubmitTime','StartTime'],'RunTime':['StartTime'],'TimeRemaining':['WallTime','StartTime']}

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
        client_utils.logger.error("%s is not a valid jobid or queue name" % n)
        sys.exit(1)
    for q in query:
        for h in hinfo.long_header:
            if h == 'JobName':
                q.update({'jobname':'*'})
            elif h not in ['JobID', 'Queue']:
                q.update({h.lower():'*'})
            if h in query_dependencies:
                for x in query_dependencies[h]:
                    if x not in hinfo.header:
                        q.update({x.lower():'*'})
        q["user"] = user_name

    response = client_utils.component_call(QUEMGR, False, 'get_jobs', (query,))

    if not parser.no_args() and not response:
        sys.exit(1)

    if response:
        maxjoblen = max([len(str(item.get('jobid'))) for item in response])
        jobidfmt = "%%%ss" % maxjoblen
    # calculate derived values
    for j in response:
        # walltime
        walltime_secs = int(j['walltime']) * 60
        t = int(float(j['walltime']))
        h = int(math.floor(t/60))
        t -= (h * 60)
        j['walltime'] = "%02d:%02d:00" % (h, t)
        # jobid
        j['jobid'] = jobidfmt % j['jobid']
        # location
        if isinstance(j['location'], types.ListType) and len(j['location']) > 1:
            j['location'] = client_utils.merge_nodelist(j['location'])
        elif isinstance(j['location'], types.ListType) and len(j['location']) == 1:
            j['location'] = j['location'][0]
        # queuedtime
        if j.get('starttime') in ('-1', 'BUG', 'N/A', None):
            j['queuedtime'] = client_utils.get_elapsed_time(float(j.get('submittime')), time.time())
        else:
            j['queuedtime'] = client_utils.get_elapsed_time(float(j.get('submittime')), float(j['starttime']))
        # runtime
        if j.get('starttime') in ('-1', 'BUG', 'N/A', None):
            j['runtime'] = 'N/A'
        else:
            currtime = time.time()
            j['runtime'] = client_utils.get_elapsed_time( float(j['starttime']), time.time())
        # starttime
        if j.get('starttime') in ('-1', 'BUG', None):
            j['starttime'] = 'N/A'
        else:
            orig_starttime = float(j['starttime'])
            j['starttime'] = client_utils.sec_to_str(float(j['starttime']))
        # timeremaining
        if j.get('starttime') in ['-1', 'BUG', 'N/A' ,None]:
            j['timeremaining'] = 'N/A'
        else:
            time_remaining = walltime_secs - (currtime - orig_starttime)
            if time_remaining < 0:
                j['timeremaining'] = '00:00:00'
            else:
                s = int(time_remaining) % 60
                m = (int(time_remaining) % 3600) / 60
                h = int(time_remaining) / 3600
                j['timeremaining'] = "%02d:%02d:%02d" % (h, m, s)
        # jobname
        outputpath = j.get('outputpath')
        jobname    = j.get('jobname')
        # envs
        if j['envs'] is None:
            j.update({'envs':''})
        else:
            j['envs'] = ' '.join([str(x) + '=' + str(y) for x, y in j['envs'].iteritems()])
        # args
        j['args'] = ' '.join(j['args'])

        # make the SubmitTime readable by humans
        j['submittime'] = client_utils.sec_to_str(float(j['submittime']))

        j['outputpath'] = outputpath
        j['errorpath'] = j.get('errorpath')
        j['user_list'] = ':'.join(j['user_list'])

        if j['geometry'] != None:
            j['geometry'] = "x".join([str(i) for i in j['geometry']])
        else:
            j['geometry'] = 'Any'
    # any header that was not present in the query response has value set to '-'
    output = [[j.get(x, '-') for x in [y.lower() for y in hinfo.header]]
              for j in response]

    return output

def process_the_output(output,parser,hinfo):
    """
    process the qstat output
    """
    fields            = ['score'] if parser.options.sort == None else [f.lower() for f in parser.options.sort]
    lower_case_header = [str(h).lower() for h in hinfo.header]
    idxes             = []
    
    for f in fields:
        try:
            idx = lower_case_header.index(f)
            idxes.append(idx)
        except:
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

    if parser.options.reverse != None:
        output.reverse()
    
    if "short_state" in lower_case_header:
        idx = lower_case_header.index("short_state")
        hinfo.header[idx] = "S"

    if "score" in lower_case_header:
        idx = lower_case_header.index("score")
        for line in output:
            line[idx] = human_format(float(line[idx]))

    if parser.options.long != None:
        client_utils.print_vertical([tuple(x) for x in [hinfo.header] + output])
    else:
        client_utils.print_tabular([tuple(x) for x in [hinfo.header] + output])


def main():
    """
    qstat main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    delim = ':'

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)
    parser.parse_it() # parse the command line

    # Get the header instance 
    hinfo = client_utils.header_info(parser)

    # Get the queues for job ids
    queues = client_utils.component_call(QUEMGR, True, 'get_queues', ([{'name':'*','state':'*'}],))

    #  if Q option specified then get the info for the specified queues 
    if parser.options.Q != None:

        output = get_output_for_queues(parser,hinfo)

    else:

        # build query from long_header (all fields) and fetch response        
        output = get_output_for_jobs(parser,hinfo,queues)

    process_the_output(output,parser,hinfo)
            
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
