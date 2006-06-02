#!/usr/bin/env python

'''Cobalt qsub command'''
__revision__ = '$Revision$'

import os, sys, pwd, os.path, xmlrpclib
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

helpmsg = "Usage: cqsub [-d] [-v] -p <project> -q <queue> -C " \
          + "<working directory> -e envvar1=value1:envvar2=value2" \
          + " -k <kernel profile> -O <outputprefix> -t time <in minutes>" \
          + " -n <number of nodes> -c <processor count> -m <mode co/vn> <command> <args>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqsub %s" % __revision__
        raise SystemExit, 0
    options = {'v':'verbose', 'd':'debug'}
    doptions = {'n':'nodecount', 't':'time', 'p':'project', 'm':'mode', 'c':'proccount', 'C':'cwd',
                'e':'env', 'k':'kernel', 'q':'queue', 'O':'outputprefix', 'p':'project'}
    (opts, command) = Cobalt.Util.dgetopt(sys.argv[1:], options, doptions, helpmsg)
    # need to filter here for all args
    level = 30
    if '-d' in sys.argv:
        level = 10
        
    failed = False
    needed = ['time', 'nodecount'] #, 'project']
    if [field for (field, value) in opts.iteritems() if not value and field in needed] or not command:
        for ofield in needed:
            if opts[ofield]:
                needed.remove(ofield)
        if command:
            print "Not all required arguments provided: %s needed" % (",".join(needed))
        else:
            print "Command required"
        print helpmsg
        raise SystemExit, 1

    jobspec = {'tag':'job'}
    try:
        nc = int(opts['nodecount'])
    except:
        print "non-integer node count specified"
        raise SystemExit, 1
    
    if not 0 < nc <= 1024:
        print "node count out of realistic range"
        raise SystemExit, 1
    if opts['cwd'] == False:
        opts['cwd'] = os.getcwd()
    # ensure time is actually in minutes
    if opts['time'].count(':') > 0:
        # process as a time
        #print "assuming seconds are not included in %s" % opts['time']
        units = opts['time'].split(':')
        units.reverse()
        totaltime = 0
        mults = [0, 1, 60]
        if len(units) > 3:
            print "time too large"
            raise SystemExit, 1
        totaltime = sum([mults[index] * float(units[index]) for index in range(len(units))])
        print "submitting walltime=%s minutes" % str(totaltime)
        opts['time'] = str(totaltime)
    if float(opts['time']) <= 0:
        print "invalid time specification"
        raise SystemExit, 1
    user = pwd.getpwuid(os.getuid())[0]
    if command[0][0] != '/':
        command[0] = opts['cwd'] + '/' + command[0]

    if not os.path.isfile( command[0] ):
        print "Warning: command", command[0], "not found, or is not a file"

    if not opts['mode']:
        opts['mode'] = 'co'
    for field in ['kernel', 'queue']:
        if not opts[field]:
            opts[field] = 'default'
    if not opts['proccount']:
        if opts.get('mode', 'co') == 'vn':
            # set procs to 2 x nodes
            opts['proccount'] = str(2 * int(opts['nodecount']))
        else:
            opts['proccount'] = opts['nodecount']
    else:
        try:
            int(opts['proccount'])
        except:
            print "non-integer node count specified"
            raise SystemExit, 1
    if opts['project']:
        jobspec['project'] = opts['project']

    jobspec.update({'user':user, 'outputdir':opts['cwd'], 'walltime':opts['time'], 'jobid':'*',
                    'path':os.environ['PATH'], 'mode':opts.get('mode', 'co'), 'kernel':opts['kernel'],
                    'queue':opts['queue'], 'procs':opts.get('proccount'), 'nodes':opts.get('nodecount')})
    if opts['outputprefix']:
        if opts['outputprefix'][0] == '/':
            jobspec.update({'outputpath':"%s.output" % (opts['outputprefix']),
                            'errorpath':"%s.error" % (opts['outputprefix'])})
        else:
            jobspec.update({'outputpath':"%s/%s.output" % (opts['cwd'], opts['outputprefix']),
                            'errorpath':"%s/%s.error" % (opts['cwd'], opts['outputprefix'])})
    if opts['env']:
        jobspec['envs'] = {}
        [jobspec['envs'].update({key:value}) for key, value
         in [item.split('=', 1) for item in opts['env'].split(':')]]
    jobspec.update({'command':command[0], 'args':command[1:]})

    Cobalt.Logging.setup_logging('cqsub', to_syslog=False, level=level)
    
    try:
        cqm = Cobalt.Proxy.queue_manager()
        job = cqm.AddJob(jobspec)
    except xmlrpclib.Fault, flt:
        if flt.faultCode == 31:
            print "System draining. Try again later"
            raise SystemExit, 1
    except:
        print "Error submitting job"
        raise SystemExit, 1
    print job[0]['jobid']
