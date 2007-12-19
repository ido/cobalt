#!/usr/bin/env python

'''Cobalt qsub command'''

__revision__ = '$Revision$'
__version__ = '$Version$'

import os
import sys
import pwd
import os.path
import popen2
import xmlrpclib
import ConfigParser
import re
import logging

import Cobalt
import Cobalt.Logging
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError


def processfilter(cmdstr, jobdict):
    '''Run a filter on the job, passing in all job args and processing all output'''
    extra = []
    for key, value in jobdict.iteritems():
        if isinstance(value, list):
            extra.append('%s="%s"' % (key, ':'.join(value)))
        elif isinstance(value, dict):
            extra.append('%s="{%s}"' % (key, str(value)))
        else:
            extra.append('%s="%s"' % (key, value))
    rc, out, err = Cobalt.Util.runcommand(" ".join([cmdstr] + extra))
    if err:
        # strip \n from last line of stderr to make sure only
        # one \n is print'ed 
        err[-1] = err[-1].strip()
        # the lines in err already end in \n from readlines()
        print >>sys.stderr, ''.join(err)
    if rc != 0:
        print >>sys.stderr, "Filter %s failed" % (cmdstr)
        sys.exit(1)
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
             -K <kernel options> -O <outputprefix> -t time <in minutes>
             -E <error file path> -o <output file path> -i <input file path>
             -n <number of nodes> -h -c <processor count> -m <mode co/vn> <command> <args>
"""

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version', 'h':'held'}
    doptions = {'n':'nodecount', 't':'time', 'p':'project', 'm':'mode',
                'c':'proccount', 'C':'cwd', 'e':'env', 'k':'kernel',
                'K':'kerneloptions', 'q':'queue', 'O':'outputprefix',
                'p':'project', 'N':'notify', 'E':'error', 'o':'output',
                'i':'inputfile'}
    (opts, command) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)
    # need to filter here for all args
    if opts['version']:
        print "cqsub %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit(1)

    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cqsub', to_syslog=False, level=level)
    logger = logging.getLogger('cqsub')

    CP = ConfigParser.ConfigParser()
    CP.read(Cobalt.CONFIG_FILES)
    
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
        sys.exit(1)

    jobspec = {'tag':'job'}
    try:
        nc = int(opts['nodecount'])
    except:
        logger.error("Error: non-integer node count specified with -n option")
        sys.exit(1)

    if opts['kerneloptions']:
        jobspec['kerneloptions'] = opts['kerneloptions']

    try:
        sys_size = int(CP.get('cqm', 'size'))
    except:
        sys_size = 1024
    if not 0 < nc <= sys_size:
        logger.error("node count out of realistic range")
        sys.exit(1)
    if opts['cwd'] == False:
        opts['cwd'] = os.getcwd()
    if not os.path.isdir(opts['cwd']):
        logger.error("Error: dir '%s' is not a directory" % opts['cwd'])
        sys.exit(1)
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
            sys.exit(1)
        try:
            totaltime = sum([mults[index] * float(units[index]) for index in range(len(units))])
        except ValueError:
            logger.error("invalid time specification")
            sys.exit(1)
        logger.error("submitting walltime=%s minutes" % str(totaltime))
        opts['time'] = str(totaltime)
    try:
        numtime = float(opts['time'])
    except:
        logger.error("invalid time specification")
        sys.exit(1)
    if numtime <= 0:
        logger.error("invalid time specification")
        sys.exit(1)
    user = pwd.getpwuid(os.getuid())[0]
    if command[0][0] != '/':
        command[0] = opts['cwd'] + '/' + command[0]

    if not os.path.isfile(command[0]):
        logger.error("command %s not found, or is not a file" % command[0])
        sys.exit(1)

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
        sys.exit(1)
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
                sys.exit(1)
        else:
            opts['proccount'] = opts['nodecount']
    else:
        try:
            int(opts['proccount'])
        except:
            logger.error("Error: non-integer node count specified with -c option")
            sys.exit(1)

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
            sys.exit(1)
    if opts['output']:
        if not opts['output'].startswith('/'):
            jobspec.update({'outputpath':"%s/%s" % (opts['cwd'], opts['output'])})
        else:
            jobspec.update({'outputpath':opts['output']})
        if not os.path.isdir(jobspec.get('outputpath')):
            logger.error("directory %s does not exist" % jobspec.get('outputpath'))
            sys.exit(1)
    if opts['held']:
        jobspec.update({'state':'hold'})
    if opts['env']:
        jobspec['envs'] = {}
        key_value_pairs = [item.split('=', 1) for item in re.split(r':(?=\w+\b=)', opts['env'])]
        for kv in key_value_pairs:
            if len(kv) != 2:
                print "Improperly formatted argument to env : %r" % kv
                sys.exit(1)
        for key, value in key_value_pairs:
            jobspec['envs'].update({key:value})
    if opts['inputfile']:
        if not opts['inputfile'].startswith('/'):
            jobspec.update({'inputfile':"%s/%s" % (opts['cwd'], opts['inputfile'])})
        else:
            jobspec.update({'inputfile':opts['inputfile']})
        if not os.path.isfile(jobspec.get('inputfile')):
            logger.error("file %s not found, or is not a file" % jobspec.get('inputfile'))
            sys.exit(1)
    jobspec.update({'cwd':opts['cwd'], 'command':command[0], 'args':command[1:]})

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []
    for filt in filters:
        processfilter(filt, jobspec)

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
        job = cqm.add_jobs([jobspec])
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    except xmlrpclib.Fault, flt:
        if flt.faultCode == 31:
            logger.error("System draining. Try again later")
            sys.exit(1)
        elif flt.faultCode == 30:
            logger.error("Job submission failed because: \n%s\nCheck 'cqstat -q' and the cqstat manpage for more details." % flt.faultString)
            sys.exit(1)
        elif flt.faultCode == 1:
            logger.error("Job submission failed due to queue-manager failure")
            sys.exit(1)
        else:
            logger.error("Job submission failed")
            logger.error(flt)
            sys.exit(1)
    except:
        logger.error("Error submitting job")
        sys.exit(1)
    # log jobid to stdout
    if job:
        print job[0]['jobid']
    else:
        print "failed to create teh job.  maybe a queue isn't there"
