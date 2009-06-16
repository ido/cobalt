#!/usr/bin/env python

'''Cobalt qalter command'''
__revision__ = '$Revision: 559 $'
__version__ = '$Version$'

import os
import sys
import pwd
import os.path
import xmlrpclib
import ConfigParser
import logging
import time
import math

import Cobalt
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

helpmsg = """
Usage: qalter [-d] [-v] -A <project name> -t <time in minutes> 
              -e <error file path> -o <output file path> 
              --dependencies <jobid1>:<jobid2>
              -n <number of nodes> -h --proccount <processor count> 
              -M <email address> --mode <mode co/vn> <jobid1> <jobid2> """

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version', 'h':'held'}
    doptions = {'n':'nodecount', 't':'time', 'A':'project', 'mode':'mode',
                'proccount':'proccount', 'dependencies':'dependencies', 
                'M':'notify', 'e':'error', 'o':'output'}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)
    # need to filter here for all args
    if opts['version']:
        print "qalter %s" % __revision__
        print "cobalt %s" % __version__
        sys.exit(1)

    if len(sys.argv) < 2:
        print helpmsg
        sys.exit(1)
 
    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('qalter', to_syslog=False, level=level)
    logger = logging.getLogger('qalter')

    CP = ConfigParser.ConfigParser()
    CP.read(Cobalt.CONFIG_FILES)

    user = pwd.getpwuid(os.getuid())[0]
    for i in range(len(args)):
        if args[i] == '*':
            continue
        try:
            args[i] = int(args[i])
        except:
            logger.error("jobid must be an integer")
            sys.exit(1)
    spec = [{'tag':'job', 'user':user, 'jobid':jobid, 'project':'*', 'notify':'*', 'walltime':'*', 'queue':'*', 'procs':'*',
             'nodes':'*', 'is_active':"*"} for jobid in args]
    updates = {}
    nc = 0
    if opts['nodecount']:
        try:
            nc = int(opts['nodecount'])
        except:
            logger.error("non-integer node count specified")
            sys.exit(1)

        try:
            sys_size = int(CP.get('system', 'size'))
        except:
            sys_size = 1024
        if not 0 < nc <= sys_size:
            logger.error("node count out of realistic range")
            sys.exit(1)
        updates['nodes'] = opts['nodecount']
    # ensure time is actually in minutes
    if opts['time']:
        if opts['time'][0] in [ '+', '-']:
            try:
                minutes = Cobalt.Util.get_time(opts['time'][1:])
            except Cobalt.Exceptions.TimeFormatError, e:
                print "invalid time specification: %s" % e.args[0]
                sys.exit(1)

            jobdata = None
            try:
                cqm = ComponentProxy("queue-manager", defer=False)
                jobdata = cqm.get_jobs(spec)
            except ComponentLookupError:
                print >> sys.stderr, "Failed to connect to queue manager"
                sys.exit(1)
            if not jobdata:
                print "Failed to match any jobs"
                sys.exit(1)

            if opts['time'][0] == '-':
                new_time = float(jobdata[0]['walltime']) - minutes
                if new_time <= 0:
                    print >> sys.stderr, "invalid wall time: ", new_time
                else:
                    updates['walltime'] = str(float(jobdata[0]['walltime']) - minutes)
            elif opts['time'][0] == '+': 
                updates['walltime'] = str(float(jobdata[0]['walltime']) + minutes)
        else:
            try:
                minutes = Cobalt.Util.get_time(opts['time'])
            except Cobalt.Exceptions.TimeFormatError, e:
                print "invalid time specification: %s" % e.args[0]
                sys.exit(1)
            
            updates['walltime'] = str(minutes)


    try:
        sys_type = CP.get('bgsystem', 'bgtype')
    except:
        sys_type = 'bgl'
    if sys_type == 'bgp':
        job_types = ['smp', 'co', 'dual', 'vn', 'script']
    else:
        job_types = ['co', 'vn', 'script']
        
    if opts['mode']:
        if opts['mode'] not in job_types:
            logger.error("Specifed mode '%s' not valid, valid modes are\n%s" % \
                  (opts['mode'], "\n".join(job_types)))
            sys.exit(1)
        if opts['mode'] == 'co' and sys_type == 'bgp':
            opts['mode'] = 'SMP'
        updates['mode'] = opts['mode']

    if opts['nodecount'] and not opts['proccount']:
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
        updates['procs'] = opts['proccount']
    if opts['proccount']:
        try:
            int(opts['proccount'])
        except:
            logger.error("non-integer node count specified")
            sys.exit(1)
        updates['procs'] = opts['proccount']

    if opts['project']:
        updates['project'] = opts['project']

    if opts['notify']:
        updates['notify'] = opts['notify']

    if opts['error']:
        updates.update({'errorpath': opts['error']})
    if opts['output']:
        updates.update({'outputpath': opts['output']})
    if opts['held']:
        updates.update({'user_hold':True})
    if opts['dependencies']:
        deps = opts['dependencies']
        if deps and deps.lower() != "none":
            deps = deps.split(":")
        else:
            deps = []

        updates.update({'all_dependencies': deps})

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
        jobdata = cqm.get_jobs(spec)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    except xmlrpclib.Fault, flt:
        print >> sys.stderr, flt.faultString
        sys.exit(1)

    if not jobdata:
        print "Failed to match any jobs"
        sys.exit(1)

    job_running = False
    for job in jobdata:
        if job['is_active']:
            job_running = True
            
    if job_running:
        if updates.has_key('procs'):
            print >> sys.stderr, "cannot change processor count of a running job"
        if updates.has_key('nodes'):
            print >> sys.stderr, "cannot change node count of a running job"
        if updates.has_key('walltime'):
            print >> sys.stderr, "cannot change wall time of a running job"
        if updates.has_key('mode'):
            print >> sys.stderr, "cannot change mode of a running job"
        if updates.has_key('errorpath'):
            print >> sys.stderr, "cannot change the error path of a running job"
        if updates.has_key('outputpath'):
            print >> sys.stderr, "cannot change the output path of a running job"
        sys.exit(1)
        
    response = False
    for jobinfo in jobdata:
        del jobinfo['is_active']
        original_spec = jobinfo.copy()
        jobinfo.update(updates)
        for filt in filters:
            Cobalt.Util.processfilter(filt, jobinfo)
        try:
            cqm.set_jobs([original_spec], jobinfo)
            response = True
        except xmlrpclib.Fault, flt:
            print >> sys.stderr, flt.faultString
            response = True

    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs or queues")
    else:
        Cobalt.Logging.logging.debug(response)


