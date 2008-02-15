#!/usr/bin/env python

'''Cobalt Queue Status'''
__revision__ = '$Revision: 406 $'
__version__ = '$Version$'

import math, os, re, sys, time, types, ConfigParser
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqstat %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0


    jobid = None

    names = ["*"]

    long_header    = ['JobID', 'JobName', 'User', 'WallTime', 'QueuedTime',
                      'RunTime', 'Nodes', 'State', 'Location', 'Mode', 'Procs',
                      'Queue', 'StartTime', 'Index', 'SubmitTime', 'Path',
                      'OutputDir', 'Envs', 'Command', 'Args', 'Kernel', 'KernelOptions',
                      'Project', 'errorpath', 'outputpath', 'inputfile' ]

    query_dependencies = {'QueuedTime':['SubmitTime', 'StartTime'], 'RunTime':['StartTime']}

    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1

    header = long_header

    # build query from long_header (all fields) and fetch response
    query = [{'tag':'job', 'jobid':'*'}]
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
    response = cqm.GetJobs(query)

    def my_cmp(left, right):
        return cmp(int(left['jobid']), int(right['jobid']))

    response.sort(my_cmp)

    if response:
        maxjoblen = max([len(item.get('jobid')) for item in response])
        jobidfmt = "%%%ss" % maxjoblen
    # calculate derived values
    for j in response:
        print "cqadm -j %s" % j['jobid']
        command = "cqsub "
        command += "-q %s " % j['queue']
        command += "-C %s " % j['outputdir']

        outputpath = j.get('outputpath')
        if outputpath:
            jobname = os.path.basename(outputpath).split('.output')[0]
            if jobname != j['jobid'].split()[0]:
                j['jobname'] = jobname
        if j.has_key('jobname'):
            command += "-O %s " % j['jobname']

        envs = j.get('envs', False)
        if envs:
            j['envs'] = ':'.join([str(x) + '=' + str(y) for x, y in j['envs'].iteritems()])
            command += "-e %s " % j['envs']

        if j.get('kernel', 'default') != "default":
            command += "-k %s " % j['kernel']

        if j.has_key('kerneloptions'):
            command += "-K %s " % j['kerneloptions']

        if j.has_key('errorpath'):
            command += "-E %s " % j['errorpath']
        if j.has_key('outputpath'):
            command += "-o %s " % j['outputpath']
        if j.has_key('inputfile'):
            command += "-i %s " % j['inputfile']

        command += "-t %s " % j['walltime']
        command += "-n %s " % j['nodes']

        if j['state'] == "hold":
            command += "-h "

        command += "-c %s " % j['procs']
        command += "-m %s " % j['mode']
        command += "%s " % j['command']
        command += "%s " % ' '.join(j['args'])

        print "su %s %s" % (j['user'], command)


