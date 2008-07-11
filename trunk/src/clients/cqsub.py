#!/usr/bin/env python

'''Cobalt qsub command'''

__revision__ = '$Revision$'
__version__ = '$Version$'

import os
import sys
import pwd
import os.path
import popen2
import stat
import xmlrpclib
import ConfigParser
import re
import logging

import Cobalt
Cobalt.CONFIG_FILES = Cobalt.DEFAULT_CONFIG_FILES
import Cobalt.Logging
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import QueueError, ComponentLookupError


helpmsg = """
Usage: cqsub [-d] [-v] -p <project> -q <queue> -C <working directory>
             --dependencies <jobid1>:<jobid2>
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
                'i':'inputfile', 'dependencies':'dependencies', 'F':'forcenoval'}
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
    if opts['kerneloptions']:
        jobspec['kerneloptions'] = opts['kerneloptions']

    if opts['cwd'] == False:
        opts['cwd'] = os.getcwd()
    if not os.path.isdir(opts['cwd']):
        logger.error("Error: dir '%s' is not a directory" % opts['cwd'])
        sys.exit(1)
    # ensure time is actually in minutes
    try:
        minutes = Cobalt.Util.get_time(opts['time'])
    except Cobalt.Exceptions.TimeFormatError, e:
        logger.error("invalid time specification: %s" % e.message)
        sys.exit(1)
    opts['time'] = str(minutes)
    user = pwd.getpwuid(os.getuid())[0]
    if command[0][0] != '/':
        command[0] = opts['cwd'] + '/' + command[0]

    if not os.path.isfile(command[0]):
        logger.error("command %s not found, or is not a file" % command[0])
        sys.exit(1)

    for field in ['kernel', 'queue']:
        if not opts[field]:
            opts[field] = 'default'
    if not opts['mode']:
        opts['mode'] = 'co'
    elif opts['mode'] == 'script':
        script_mode = os.stat(command[0])[stat.ST_MODE]
        if not (script_mode & stat.S_IXUSR or \
                script_mode & stat.S_IXGRP or script_mode & stat.S_IXOTH):
            logger.error("Script %s is not executable" % command[0])
            sys.exit(1)

    try:
        system = ComponentProxy("system", defer=False)
        opts = system.validate_job(opts)
    except xmlrpclib.Fault, flt:
        logger.error("Job failed to validate: %s" % (flt.faultString))
        if not opts['forcenoval']:
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
        if not os.path.isdir(os.path.dirname(jobspec.get('errorpath'))):
            logger.error("directory %s does not exist" % jobspec.get('errorpath'))
            sys.exit(1)
    if opts['output']:
        if not opts['output'].startswith('/'):
            jobspec.update({'outputpath':"%s/%s" % (opts['cwd'], opts['output'])})
        else:
            jobspec.update({'outputpath':opts['output']})
        if not os.path.isdir(os.path.dirname(jobspec.get('outputpath'))):
            logger.error("directory %s does not exist" % jobspec.get('outputpath'))
            sys.exit(1)
    if opts['held']:
        jobspec.update({'user_state':'hold'})
    if opts['env']:
        if sys.argv.count('-e') - command.count('-e') > 1:
            logger.error("Use of multiple -e options is not supported. Specify multiple environment variables with -e FOO=1:BAR=2")
            raise SystemExit(1)
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

    if opts['dependencies']:
        jobspec['all_dependencies'] = opts['dependencies']
    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []
    for filt in filters:
        Cobalt.Util.processfilter(filt, jobspec)

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
        job = cqm.add_jobs([jobspec])
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    except xmlrpclib.Fault, flt:
        if flt.faultCode == QueueError.fault_code:
            logger.error(flt.faultString)
            sys.exit(1)
        else:
            logger.error("Job submission failed")
            print repr(flt.faultCode)
            print repr(QueueError.fault_code)
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
