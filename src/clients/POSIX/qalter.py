#!/usr/bin/env python

'''Cobalt qalter command'''
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
Usage: qalter [-d] [-v] -A <project name> -t <time in minutes> 
              -e <error file path> -o <output file path> 
              -n <number of nodes> -h --proccount <processor count> 
              -M <email address> --mode <mode co/vn> <jobid1> <jobid2> """

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version', 'h':'held'}
    doptions = {'n':'nodecount', 't':'time', 'A':'project', 'mode':'mode',
                'proccount':'proccount', 
                'M':'notify', 'e':'error', 'o':'output'}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)
    # need to filter here for all args
    if opts['version']:
        print "qalter %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 1

    if len(sys.argv) < 2:
        print helpmsg
        raise SystemExit, 1
 
    # setup logging
    level = 30
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('qalter', to_syslog=False, level=level)
    logger = logging.getLogger('qalter')

    CP = ConfigParser.ConfigParser()
    CP.read(['/etc/cobalt.conf'])

    user = pwd.getpwuid(os.getuid())[0]
    for i in range(len(args)):
        try:
            args[i] = int(args[i])
        except:
            logger.error("jobid must be an integer")
            raise SystemExit, 1
    spec = [{'tag':'job', 'user':user, 'jobid':jobid} for jobid in args]
    updates = {}
    nc = 0
    if opts['nodecount']:
        try:
            nc = int(opts['nodecount'])
        except:
            logger.error("non-integer node count specified")
            raise SystemExit, 1

        try:
            sys_size = int(CP.get('cqm', 'size'))
        except:
            sys_size = 1024
        if not 0 < nc <= sys_size:
            logger.error("node count out of realistic range")
            raise SystemExit, 1
        updates['nodes'] = opts['nodecount']
    # ensure time is actually in minutes
    if opts['time']:
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
            totaltime = sum([mults[index] * float(units[index]) for index in range(len(units))])
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
        updates['walltime'] = opts['time']

    try:
        sys_type = CP.get('cqm', 'bgtype')
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
            raise SystemExit, 1
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
                raise SystemExit, 1
        else:
            opts['proccount'] = opts['nodecount']
        updates['procs'] = opts['proccount']
    if opts['proccount']:
        try:
            int(opts['proccount'])
        except:
            logger.error("non-integer node count specified")
            raise SystemExit, 1
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
        updates.update({'state':'user hold'})

    try:
        filters = CP.get('cqm', 'filters').split(':')
    except ConfigParser.NoOptionError:
        filters = []
    for filt in filters:
        processfilter(filt, updates)

    try:
        cqm = ComponentProxy("queue-manager")
        response = cqm.set_jobs(spec, updates)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    except xmlrpclib.Fault, flt:
        response = []
        if flt.faultCode == 30:
            print flt.faultString
            raise SystemExit, 1
    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs or queues")
    else:
        Cobalt.Logging.logging.debug(response)


