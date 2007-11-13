#!/usr/bin/env python

'''Cobalt qsub command'''
__revision__ = '$Revision: 559 $'
__version__ = '$Version$'

import os, sys, pwd, os.path, popen2, xmlrpclib, ConfigParser, re, logging
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError


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
    rc, out, err = Cobalt.Util.runcommand(" ".join([cmdstr] + extra))
    if err:
        # strip \n from last line of stderr to make sure only
        # one \n is print'ed 
        err[-1] = err[-1].strip()
        # the lines in err already end in \n from readlines()
        print >>sys.stderr, ''.join(err)
    if rc != 0:
        print >>sys.stderr, "Filter %s failed" % (cmdstr)
        raise SystemExit, 1
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
Usage: qsub [-d] [-v] -A <project name> -q <queue> --cwd <working directory>
             --env envvar1=value1:envvar2=value2 --kernel <kernel profile>
             -K <kernel options> -O <outputprefix> -t time <in minutes>
             -e <error file path> -o <output file path> -i <input file path>
             -n <number of nodes> -h --proccount <processor count> 
             --mode <mode co/vn> <command> <args>
"""

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version', 'h':'held'}
    doptions = {'n':'nodecount', 't':'time', 'A':'project', 'mode':'mode',
                'proccount':'proccount', 'cwd':'cwd', 'env':'env', 'kernel':'kernel',
                'K':'kerneloptions', 'q':'queue', 'O':'outputprefix',
                'A':'project', 'M':'notify', 'e':'error', 'o':'output',
                'i':'inputfile'}
    (opts, command) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)
    # need to filter here for all args
    if opts['version']:
        print "qsub %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 1

    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('qsub', to_syslog=False, level=level)
    logger = logging.getLogger('qsub')

    CP = ConfigParser.ConfigParser()
    CP.read(['/etc/cobalt.conf'])
    
    failed = False
    needed = ['time', 'nodecount'] #, 'project']
    if [field for (field, value) in opts.iteritems() if not value and field in needed] or not command:
        for ofield in needed:
            if opts[ofield]:
                needed.remove(ofield)
        if command:
            logger.error("Not all required arguments provided: %s needed" % (",".join(needed)))
        else:
            logger.error("Command required")
        logger.error(helpmsg)
        raise SystemExit, 1

    jobspec = {'tag':'job'}
    try:
        nc = int(opts['nodecount'])
    except:
        logger.error("Error: non-integer node count specified with -n option")
        raise SystemExit, 1

    if opts['kerneloptions']:
        jobspec['kerneloptions'] = opts['kerneloptions']

    try:
        sys_size = int(CP.get('cqm', 'size'))
    except:
        sys_size = 1024
    if not 0 < nc <= sys_size:
        logger.error("node count out of realistic range")
        raise SystemExit, 1
    if opts['cwd'] == False:
        opts['cwd'] = os.getcwd()
    if not os.path.isdir(opts['cwd']):
        logger.error("Error: dir '%s' is not a directory" % opts['cwd'])
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
            logger.error("time too large")
            raise SystemExit, 1
        try:
            totaltime = sum([mults[index] * float(units[index]) for index in range(len(units))])
        except ValueError:
            logger.error("invalid time specification")
            raise SystemExit, 1
        logger.error("submitting walltime=%s minutes" % str(totaltime))
        opts['time'] = str(totaltime)
    try:
        numtime = float(opts['time'])
    except:
        logger.error("invalid time specification")
        raise SystemExit, 1
    if numtime <= 0:
        logger.error("invalid time specification")
        raise SystemExit, 1
    user = pwd.getpwuid(os.getuid())[0]
    if command[0][0] != '/':
        command[0] = opts['cwd'] + '/' + command[0]

    if not os.path.isfile(command[0]):
        logger.error("command %s not found, or is not a file" % command[0])
        raise SystemExit, 1

    try:
        sys_type = CP.get('cqm', 'bgtype')
    except:
        sys_type = 'bgl'
    if sys_type == 'bgp':
        job_types = ['smp', 'co', 'dual', 'vn', 'script']
    else:
        job_types = ['co', 'vn', 'script']
        
    if not opts['mode']:
        opts['mode'] = 'co'
    elif opts['mode'] not in job_types:
        logger.error("Specifed mode '%s' not valid, valid modes are\n%s" % \
              (opts['mode'], "\n".join(job_types)))
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
                logger.error("Unknown bgtype %s" % (sys_type))
                raise SystemExit, 1
        else:
            opts['proccount'] = opts['nodecount']
    else:
        try:
            int(opts['proccount'])
        except:
            logger.error("Error: non-integer node count specified with -c option")
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
        if not opts['error'].startswith('/'):
            jobspec.update({'errorpath':"%s/%s" % (opts['cwd'], opts['error'])})
        else:
            jobspec.update({'errorpath':opts['error']})
        if not os.path.isdir(jobspec.get('errorpath')):
            logger.error("directory %s does not exist" % jobspec.get('errorpath'))
            raise SystemExit, 1
    if opts['output']:
        if not opts['output'].startswith('/'):
            jobspec.update({'outputpath':"%s/%s" % (opts['cwd'], opts['output'])})
        else:
            jobspec.update({'outputpath':opts['output']})
        if not os.path.isdir(jobspec.get('outputpath')):
            logger.error("directory %s does not exist" % jobspec.get('outputpath'))
            raise SystemExit, 1
    if opts['held']:
        jobspec.update({'state':'user hold'})
    if opts['env']:
        jobspec['envs'] = {}
        key_value_pairs = [item.split('=', 1) for item in re.split(r':(?=\w+\b=)', opts['env'])]
        for kv in key_value_pairs:
            if len(kv) != 2:
                print "Improperly formatted argument to env : %r" % kv
                raise SystemExit, 1
        for key, value in key_value_pairs:
            jobspec['envs'].update({key:value})
    if opts['inputfile']:
        if not opts['inputfile'].startswith('/'):
            jobspec.update({'inputfile':"%s/%s" % (opts['cwd'], opts['inputfile'])})
        else:
            jobspec.update({'inputfile':opts['inputfile']})
        if not os.path.isfile(jobspec.get('inputfile')):
            logger.error("file %s not found, or is not a file" % jobspec.get('inputfile'))
            raise SystemExit, 1
    jobspec.update({'cwd':opts['cwd'], 'command':command[0], 'args':command[1:]})

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []
    for filt in filters:
        processfilter(filt, jobspec)

    try:
        cqm = ComponentProxy("queue-manager")
        job = cqm.add_jobs([jobspec])
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    except xmlrpclib.Fault, flt:
        if flt.faultCode == 31:
            logger.error("System draining. Try again later")
            raise SystemExit, 1
        elif flt.faultCode == 30:
            logger.error("Job submission failed because: \n%s\nCheck 'qstat -q' and the qstat manpage for more details." % flt.faultString)
            raise SystemExit, 1
        elif flt.faultCode == 1:
            logger.error("Job submission failed due to queue-manager failure")
            raise SystemExit, 1
        else:
            logger.error("Job submission failed")
            logger.error(flt)
            raise SystemExit, 1
    except:
        logger.error("Error submitting job")
        raise SystemExit, 1
    # log jobid to stdout
    if job:
        print job[0]['jobid']
    else:
        print "failed to create teh job.  maybe a queue isn't there"
