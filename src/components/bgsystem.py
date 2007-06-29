#!/usr/bin/env python
# $Id$

'''Cobalt System Component'''
__revision__ = '$Revision$'

from optparse import OptionParser

import logging, random, sys, ConfigParser, xmlrpclib, pwd, atexit, os
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util
#import Cobalt.bridge

logger = logging.getLogger('bgsystem')

class System(Cobalt.Component.Component):
    __implementation__ = 'bgsys'
    __name__ = 'system'
    __statefields__ = []
    async_funcs = ['assert_location']

    # read in config from cobalt.conf
    required_fields = ['user', 'executable', 'args', 'location', 'size', 'cwd']
    _configfields = ['mmcs_server_ip', 'db2_instance', 'bridge_config', 'mpirun', 'db2_properties', 'db2_connect']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('bgpm'):
        print '''"system" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['bgpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        self.comms = Cobalt.Proxy.CommDict()
        self.register_function(self.start_job, "StartJob")
#        self.register_function(self.query_job, "QueryJob")
        self.register_function(self.query_part, "QueryPartition")

    def start_job(self, _, jobinfo):
        '''starts a job'''

        print 'jobinfo', jobinfo
        print 'pid before fork is', os.getpid()
        pid = os.fork()
        print 'pid is', pid
        if not pid:
            print 'i am child, with pid', os.getpid(), os.getppid()
            if jobinfo.get('outputfile', False):
                self.outlog = jobinfo.get('outputfile')
            else:
                self.outlog = tempfile.mktemp()            
            if jobinfo.get('errorfile', False):
                self.errlog = jobinfo.get('errorfile')
            else:
                self.errlog = tempfile.mktemp()

            if not jobinfo.get('location', False):
                raise ProcessGroupCreationError, "location"
            partition = jobinfo.get('location')[0]

            try:
                userid, groupid = pwd.getpwnam(jobinfo.get('user'))[2:4]
            except KeyError:
                raise ProcessGroupCreationError, "user/group"

            program = jobinfo.get('executable')
            cwd = jobinfo.get('cwd')
            pnum = str(jobinfo.get('size'))
            mode = jobinfo.get('mode', 'co')
            args = " ".join(jobinfo.get('args', []))
            inputfile = jobinfo.get('inputfile', '')
            kerneloptions = jobinfo.get('kerneloptions', '')
            # strip out BGLMPI_MAPPING until mpirun bug is fixed 
            mapfile = ''
            if jobinfo.get('env', {}).has_key('BGLMPI_MAPPING'):
                mapfile = jobinfo.get('env')['BGLMPI_MAPPING']
                del jobinfo.get('env')['BGLMPI_MAPPING']
            envs = " ".join(["%s=%s" % envdata for envdata in jobinfo.get('envs', {}).iteritems()])
            atexit._atexit = []

            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                logger.error("Failed to change userid/groupid for PG %s" % (jobinfo.get("pgid")))
                sys.exit(0)

            #os.system("%s > /dev/null 2>&1" % (self.config['db2_connect']))
            os.environ["DB_PROPERTY"] = self.config['db2_properties']
            os.environ["BRIDGE_CONFIG_FILE"] = self.config['bridge_config']
            os.environ["MMCS_SERVER_IP"] = self.config['mmcs_server_ip']
            os.environ["DB2INSTANCE"] = self.config['db2_instance']
            os.environ["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
            os.environ["COBALT_JOBID"] = jobinfo.get('jobid')
            if inputfile != '':
                infile = open(inputfile, 'r')
                os.dup2(infile.fileno(), sys.__stdin__.fileno())
            else:
                null = open('/dev/null', 'r')
                os.dup2(null.fileno(), sys.__stdin__.fileno())
            cmd = (self.config['mpirun'], os.path.basename(self.config['mpirun']),
                   '-np', pnum, '-partition', partition,
                   '-mode', mode, '-cwd', cwd, '-exe', program)
            if args != '':
                cmd = cmd + ('-args', args)
            if envs != '':
                cmd = cmd + ('-env',  envs)
            if kerneloptions != '':
                cmd = cmd + ('-kernel_options', kerneloptions)
            if mapfile != '':
                cmd = cmd + ('-mapfile', mapfile)

            print 'going to daemonize...',
            #daemonize thy self...then set stdout/err
            Cobalt.Component.daemonize('/dev/null')

            try:
                err = open(self.errlog, 'a')
                os.chmod(self.errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), self.errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), self.errlog))

            try:
                out = open(self.outlog, 'a')
                os.chmod(self.outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), self.outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), self.errlog))

            print 'daemonized?'
            print 'going to run cmd', cmd
            try:
                apply(os.execl, cmd)
            except Exception, e:
                print 'got exception', e
            sys.exit(0)

        else:
            print 'parent: is this the child?', pid
            return pid
            

    def kill_job(self, _, jobinfo):
        '''kills a job using PyBridge or Allocator API'''
        # status_t jm_signal_job(db_job_id_t jid, rm_signal_t signal);
        signal = bgl_rm_api.rm_signal_t(15)
        jobid = jobinfo.get('dbjobid')
        bridge.jm_signal_job(jobid, signal)
    
    def query_part(self, _, partinfo):
        '''queries partitions for status info'''
        pass

if __name__ == '__main__':
    # setup option parsing
    parser = OptionParser()
    parser.add_option("-d", dest="debug", action="store_true", default=False,
                      help="Turn on debugging output")
    parser.add_option("-D", "--daemon", dest="daemon", default=False,
                      metavar="<pidfile>",
                      help="Run component as a daemon")
    (opts, args) = parser.parse_args()

    __daemon__ = opts.daemon
    __dlevel__ = logging.INFO
    if opts.debug:
        __dlevel__ = logging.DEBUG
    Cobalt.Logging.setup_logging('bgsystem', level = __dlevel__)
    logger = logging.getLogger('bgsystem')
    __server__ = System({'configfile':'/etc/cobalt.conf', 'daemon':__daemon__})
    __server__.serve_forever()
