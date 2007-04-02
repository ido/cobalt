#!/usr/bin/env python

'''Cobalt qsub command'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import os, sys, pwd, os.path, popen2, xmlrpclib, ConfigParser, re
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

def runcommand(cmd):
    '''Execute command, returning rc, stdout, stderr'''
    cmdp = popen2.Popen3(cmd, True)
    out = []
    err = []
    status = cmdp.wait()
    out += cmdp.fromchild.readlines()
    err += cmdp.childerr.readlines()
    return (status, out, err)

def processfilter(cmdstr, jobdict):
    '''Run a filter on the job, passing in all job args and processing all output'''
    extra = []
    for key, value in jobdict.iteritems():
        if isinstance(value, list):
            extra.append("%s=%s" % (key, ':'.join(value)))
        elif isinstance(value, dict):
            extra.append("%s={%s}" % (key, str(value)))
        else:
            extra.append("%s=%s" % (key, value))
    rc, out, err = runcommand(" ".join([cmdstr] + extra))
    if err:
        print '\n'.join(err)
    if rc != 0:
        print "Filter %s failed" % (cmdstr)
        raise SystemExit, 0
    if out:
        for line in out:
            key, value = line.strip().split('=', 1)
            if key not in jobdict.keys():
                jobdict[key] = value
            elif isinstance(jobdict[key], list):
                jobdict[key] = value.split(':')
            elif isinstance(jobdict[key], dict):
                jobdict[key].update(eval(value))
            else:
                jobdict[key] = value

helpmsg = """
Usage: cqsub [-d] [-v] -p <project> -q <queue> -C <working directory>
             -e envvar1=value1:envvar2=value2 -k <kernel profile>
             -O <outputprefix> -t time <in minutes> -E <error file path>
             -o <output file path> -i <input file path> -n <number of nodes>
             -c <processor count> -m <mode co/vn> <command> <args>
"""

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version'}
    doptions = {'n':'nodecount', 't':'time', 'p':'project', 'm':'mode', 'c':'proccount', 'C':'cwd',
                'e':'env', 'k':'kernel', 'q':'queue', 'O':'outputprefix', 'p':'project', 'N':'notify',
                'E':'error', 'o':'output', 'i':'inputfile'}
    (opts, command) = Cobalt.Util.dgetopt_long(sys.argv[1:], options, doptions, helpmsg)
    # need to filter here for all args
    if opts['version']:
        print "cqsub %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    level = 30
    if '-d' in sys.argv:
        level = 10
    CP = ConfigParser.ConfigParser()
    CP.read(['/etc/cobalt.conf'])
        
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

    try:
        sys_size = int(CP.get('cqm', 'size'))
    except:
        sys_size = 1024
    if not 0 < nc <= sys_size:
        print "node count out of realistic range"
        raise SystemExit, 1
    if opts['cwd'] == False:
        opts['cwd'] = os.getcwd()
    if not os.path.isdir(opts['cwd']):
        print "Error: dir '" + opts['cwd'] + "' is not a directory"
        raise SystemExit, 1
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
    try:
        numtime = float(opts['time'])
    except:
        print "invalid time specification"
        raise SystemExit, 1
    if numtime <= 0:
        print "invalid time specification"
        raise SystemExit, 1
    user = pwd.getpwuid(os.getuid())[0]
    if command[0][0] != '/':
        command[0] = opts['cwd'] + '/' + command[0]

    if not os.path.isfile(command[0]):
        print "command", command[0], "not found, or is not a file"
        raise SystemExit, 1

    try:
        sys_type = CP.get('cqm', 'bgtype')
    except:
        sys_type = 'bgl'
    if sys_type == 'bgp':
        job_types = ['smp', 'co', 'dual', 'vn']
    else:
        job_types = ['co', 'vn']
        
    if not opts['mode']:
        opts['mode'] = 'co'
    elif opts['mode'] not in job_types:
        print "Specifed mode '%s' not valid, valid modes are\%s" % \
              (opts['mode'], "\n".join(job_types))
        raise SystemExit, 1
    if opts['mode'] == 'co' and sys_type == 'bgp':
        opts['mode'] = 'SMP'
    for field in ['kernel', 'queue']:
        if not opts[field]:
            opts[field] = 'default'
    if not opts['proccount']:
        if opts.get('mode', 'co') == 'vn':
            # set procs to 2 x nodes
            if sys_type == 'bgl':
                opts['proccount'] = str(2 * int(opts['nodecount']))
            elif sys_type == 'bgp':
                opts['proccount'] = str(4 * int(opts['nodecount']))
            else:
                print "Unknown bgtype %s" % (sys_type)
                raise SystemExit, 1
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

    if opts['notify']:
        jobspec['notify'] = opts['notify']

    jobspec.update({'user':user, 'outputdir':opts['cwd'], 'walltime':opts['time'],
                    'jobid':'*', 'path':os.environ['PATH'], 'mode':opts.get('mode', 'co'),
                    'kernel':opts['kernel'], 'queue':opts['queue'],
                    'procs':opts.get('proccount'), 'nodes':opts.get('nodecount')})
    if opts['outputprefix']:
        if opts['outputprefix'][0] == '/':
            jobspec.update({'outputpath':"%s.output" % (opts['outputprefix']),
                            'errorpath':"%s.error" % (opts['outputprefix'])})
        else:
            jobspec.update({'outputpath':"%s/%s.output" % (opts['cwd'],
                                                           opts['outputprefix']),
                            'errorpath':"%s/%s.error" % (opts['cwd'], opts['outputprefix'])})
    if opts['error']:
        jobspec.update({'errorpath': opts['error']})
    if opts['output']:
        jobspec.update({'outputpath': opts['output']})
    if opts['env']:
        jobspec['envs'] = {}
        [jobspec['envs'].update({key:value}) for key, value
         in [item.split('=', 1) for item in re.split(r':(?=\w+\b=)', opts['env'])]]
    if opts['inputfile']:
        if not opts['inputfile'].startswith('/'):
            jobspec.update({'inputfile':"%s/%s" % (opts['cwd'], opts['inputfile'])})
        else:
            jobspec.update({'inputfile':opts['inputfile']})
        if not os.path.isfile(jobspec.get('inputfile')):
            print "file", jobspec.get('inputfile'), "not found, or is not a file"
            raise SystemExit, 1
    jobspec.update({'command':command[0], 'args':command[1:]})

    Cobalt.Logging.setup_logging('cqsub', to_syslog=False, level=level)

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []
    for filt in filters:
        processfilter(filt, jobspec)
    
    try:
        cqm = Cobalt.Proxy.queue_manager()

        # check if job can run in queue as specified
        response = cqm.CanQueue(jobspec)

        # try adding job to queue_manager
        job = cqm.AddJob(jobspec)

    except Cobalt.Proxy.CobaltComponentError:
        print "Can't connect to the queue manager"
        raise SystemExit, 1
    except xmlrpclib.Fault, flt:
        if flt.faultCode == 31:
            print "System draining. Try again later"
            raise SystemExit, 1
        elif flt.faultCode == 30:
            print "Job submission failed because: \n%s\nCheck 'cqstat -q' and the cqstat manpage for more details." % flt.faultString
            raise SystemExit, 1
        elif flt.faultCode == 1:
            print "Job submission failed due to queue-manager failure"
            raise SystemExit, 1
        else:
            print "Job submission failed"
            print flt
            raise SystemExit, 1
    except:
        print "Error submitting job"
        raise SystemExit, 1
    print job[0]['jobid']
