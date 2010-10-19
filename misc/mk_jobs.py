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
                      'Project', 'errorpath', 'outputpath', 'inputfile','all_dependencies', 'user_hold',
                      'admin_hold', 'satisfied_dependencies', 'user_list', 'score']

    query_dependencies = {'QueuedTime':['SubmitTime', 'StartTime'], 'RunTime':['StartTime']}

    try:
        cqm = Cobalt.Proxy.ComponentProxy("queue-manager", defer=False)
    except Cobalt.Exceptions.ComponentLookupError:
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
    response = cqm.get_jobs(query)

    next_job_id = cqm.get_next_id()

    def my_cmp(left, right):
        return cmp(int(left['jobid']), int(right['jobid']))

    response.sort(my_cmp)

    if response:
        maxjoblen = max([len(str(item.get('jobid'))) for item in response])
        jobidfmt = "%%%ss" % maxjoblen
    # calculate derived values
    for j in response:

        print "cqadm.py -j %s" % j['jobid']
        command = "cqsub "
        command += "-q %s " % j['queue']
        command += "-C %s " % j['outputdir']

        outputpath = j.get('outputpath')
        if outputpath:
            jobname = os.path.basename(outputpath).split('.output')[0]
            if jobname != str(j['jobid']):
                j['jobname'] = jobname
        if j.has_key('jobname') and (j['jobname'] != None):
            command += "-O %s " % j['jobname']

        envs = j.get('envs', False)
        if envs:
            j['envs'] = ':'.join([str(x) + '=' + str(y) for x, y in j['envs'].iteritems()])
            command += "-e %s " % j['envs']

        if j.has_key('project') and (j['project'] != None):
            command += "-p %s " % j['project']

        if (j.get('kernel', 'default') != "default"):
            command += "-k %s " % j['kernel']

        if j.has_key('kerneloptions') and (j['kerneloptions'] !=  None):
            command += "-K %s " % j['kerneloptions']

        if j.has_key('errorpath') and (j['errorpath'] != None):
            command += "-E %s " % j['errorpath']
        if j.has_key('outputpath') and (j['outputpath'] != None):
            command += "-o %s " % j['outputpath']
        if j.has_key('inputfile') and (j['inputfile'] != None):
            command += "-i %s " % j['inputfile']

        command += "-t %s " % int(float(j['walltime']))
        command += "-n %s " % j['nodes']

        if j['all_dependencies'] != []:
            command += "--dependencies %s " % ':'.join(s for s in j['all_dependencies'] if
                                                       s not in j['satisfied_dependencies'])   
    
        if j['user_list'] != []:
            command += "--run_users %s " % ':'.join(j['user_list'])

        if j['state'] == "user_hold":
            command += "-h "

        command += "-c %s " % j['procs']
        command += "-m %s " % j['mode']
        command += "%s" % j['command']
        if j['args'] != []:
            command += " %s" % ' '.join(j['args'])

        print "su %s -c \"%s\"" % (j['user'], command)

        if j['admin_hold']:
            print "cqadm --hold %s" % j['jobid']
                                                  
                                               
        print "schedctl --score=%s %s" % (j['score'], j['jobid'])
    print "cqadm -j %d" % next_job_id



