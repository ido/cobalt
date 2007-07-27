#!/usr/bin/env python
# $Id$

'''Cobalt System Component'''
__revision__ = '$Revision$'

from optparse import OptionParser

import logging, random, sys, ConfigParser, xmlrpclib, pwd, atexit, os
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util
import Cobalt.bridge

logger = logging.getLogger('bgsystem')

class BridgeData(Cobalt.Data.Data):
    '''A Data object that ties into another object, like something
    returned from the bridge module
    '''
    obj = None
    
    def get(self, field, default=None):
        '''return attribute from either self or self.obj,
        preferring self.obj
        '''
        if self.obj and field in self.obj.__attrinfo__:
            return getattr(self.obj, field)
        else:
            return Cobalt.Data.Data.get(self, field, default)

    def set(self, field, value):
        '''set attribute in either self of self.obj,
        preferring self.obj
        '''
        if self.obj and field in self.obj.__attrinfo__:
            setattr(self.obj, field, value)
        else:
            Cobalt.Data.Data.set(self, field, value)

    def to_rx(self, spec):
        '''return transmittable version of instance, sans ctype stuff
        that cannot be marshalled
        '''
        rxval = {'tag':self.tag}
        for field in [field for field in spec.keys() if field != 'tag' and
                      self._attrib.has_key(field) and
                      not isinstance(self.get(field), Cobalt.bridge.c_void_p) and
                      not isinstance(self.get(field), Cobalt.bridge.c_char_p)]:
            rxval[field] = self.get(field)
        return rxval

    def setObject(self, newobject):
        '''sets the backing bridge object, and updates self._attrib'''
        self.obj = newobject
        for attr in type(newobject).__attrinfo__.keys():
            if attr not in self._attrib:
                self._attrib.update({attr:None})

class BridgeDataSet(Cobalt.Data.DataSet):
    '''a collection of data objects that reference the bridge'''
    bridge_objects = {} #indexed by object.id

    def __init__(self, bridge_list):
        '''calls DataSet init, then builds dictionary of bridge objects'''
        Cobalt.Data.DataSet.__init__(self)
        for datum in bridge_list:
            self.bridge_objects.update({datum.id:datum})
        
    def Get(self, cdata, callback=None, cargs=()):
        '''DataSet.Get which reloads any bridge objects that may
        have been modified via the callback
        TODO: the result returned does not contain the updates from cargs
        '''
        result = Cobalt.Data.DataSet.Get(self, cdata, callback, cargs)
        if callback and cargs:
            for part in result:
                self.bridge_objects[part.get('name')].reload()
        return result

    def sync_bridge_refs(self, somedata):
        #TODO: why did I do this?
        '''reloads all the partition.obj -> bridge.Partition references'''
        local_objects = {}  # local object lookup (to avoid nxn looping)
        for datum in self:
            local_objects.update({datum.get('name'):datum})
        for datum in somedata:
            if datum.get('name') in self.bridge_objects.keys():
                local_objects[datum.get('name')].setObject(self.bridge_objects[datum.get('name')])

class BaseBlock(BridgeData):
    '''BG/L block (nodecard)'''
    pass

class BaseSystem(BridgeDataSet):
    '''Defines a BG/L system'''
    __object__ = BaseBlock

    def __init__(self):
        '''build list of bridge nodecard objects'''
        Cobalt.Data.DataSet.__init__(self)

        bg = Cobalt.bridge.BG()
        nodecardlist = []
        for bp in bg.basePartitions:
            for nc in bp.nodecards:
                self.bridge_objects.update({"%s-%s" % (bp.id, nc.id):nc})

        # initializes self with nodecard blocks
        
        self.buildBlocks()

    def buildBlocks(self):
        '''populate basesystem with nodecard blocks'''
        bg = Cobalt.bridge.BG()
        query = []
        for bp in bg.basePartitions:
            for nc in bp.nodecards:
                query.append({'tag':'block', 'state':'idle', 'queue':False,
                              'name':"%s-%s" % (bp.id, nc.id)})
        self.Add(query)
#         print query

class Partition(BridgeData):
    '''BG/L partition'''
    pass

class PartitionSet(BridgeDataSet):
    '''set of partitions'''
    __object__ = Partition

    def __init__(self):
        # using partlist for the backing bridge data
        BridgeDataSet.__init__(self, Cobalt.bridge.PartList())
#         self.partitions = Cobalt.bridge.PartList()
#         for part in self.partitions:
#             self.bridge_objects.update({part.id:part})
        self.populatePartitions()

    def refresh(self):
        '''refreshes partitions from bridge'''
        #TODO add new partition if partition in bridge not in self
        #TODO deal with partition in self but not in bridge (disable?)
        self.partitions.__freepartlist__()
#         self.partitions.__init__()
        # try using rm_get_partition
        self.partitions.reload()
        self.sync_bridge_refs(self)

    def populatePartitions(self):
        '''Populate the partition set with partitions from bridge api'''
        logger.info("populating partitions")
        
        query = []
        for part in self.partitions:
            print 'part is', part.id
            nodecards = ["%s-%s" % (nc.basepart, nc.id) \
                         for nc in part.nodecards]
#             print 'before sort', nodecards
#             nodecards.sort()
#             print 'after sort', nodecards
            query.append({'tag':'partition', 'name':part.id,
                          'nodes':len(nodecards)*32,
                          'nodecards':nodecards})
        result = self.Add(query)

        self.sync_bridge_refs(self)
        
    def get_more_deps(self, depdict, check_size, parent):

        print 'get_more_deps, check_size', check_size
        while check_size > 1:
            for p in [part for part in self if part.get('nodes') == check_size]:
                ischild = True
                for n in p.get('nodecards'):
                    if n not in parent.get('nodecards'):
                        ischild = False
                if ischild:
                    
                    print p.get('name'), p.get('nodes')
                    depdict.update({p.get('name'):{}})
                    self.get_more_deps(depdict[p.get('name')], check_size/2, p)
            return
        return

    def getDeps(self):
        '''generate dependencies between partitions'''
        bg = Cobalt.bridge.BG()
        bpsize = bg.BPsize['X']*bg.BPsize['Y']*bg.BPsize['Z']
        machine_size = bpsize*bg.BPnum
        print 'machine is %d nodes' % machine_size
        full_partitions = [p for p in self if p.get('nodes') == machine_size]
#         print 'full partition is', full_partition[0]._attrib
        depdict = {}
        check_size = machine_size

#         print type(check_size), [part.get('nodes') for part in self.data if part.get('nodes') == check_size]
        for part in full_partitions:
            self.get_more_deps(depdict, check_size, part)

        return depdict

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
        self.log = logging.getLogger('sys')
        self.register_function(self.start_job, "StartJob")
        self.register_function(self.query_jobs, "QueryJobs")
        self.register_function(self.kill_job, "KillJob")
        self.register_function(self.query_part, "GetPartition")
        self.register_function(self.full_partition_info, "FullPartitionInfo")

        logger.info('getting partitions')
        self.partitions = PartitionSet()

    def start_job(self, _, jobinfo):
        '''starts a job
        daemonizes the mpirun process, passing the mpirun pid back to the
        parent process via a pipe'''

#         self.log.info("Job %s/%s: Running %s" % (jobinfo.get('jobid'), jobinfo.get('user'), " ".join(cmd)))

        # make pipe for daemon mpirun to talk to bgsystem
        newpipe_r, newpipe_w = os.pipe()

        pid = os.fork()
        print 'pid is', pid
        if not pid:
            os.close(newpipe_r)
            os.setsid()
            pid2 = os.fork()
            if pid2 != 0:
                newpipe_w = os.fdopen(newpipe_w, 'w')
                newpipe_w.write(str(pid2))
                newpipe_w.close()
                os._exit(0)

            #start daemonized child
            os.close(newpipe_w)

            #setup output and error files
            if jobinfo.get('outputfile', False):
                self.outlog = jobinfo.get('outputfile')
            else:
                self.outlog = tempfile.mktemp()            
            if jobinfo.get('errorfile', False):
                self.errlog = jobinfo.get('errorfile')
            else:
                self.errlog = tempfile.mktemp()

            #check for location to run
            if not jobinfo.get('location', False):
                raise ProcessGroupCreationError, "location"
            partition = jobinfo.get('location')[0]

            #check for valid user/group
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

            try:
                apply(os.execl, cmd)
            except Exception, e:
                print 'got exception when trying to exec mpirun', e
                raise SystemExit, 1

            sys.exit(0)

        else:
            #parent process reads daemon child's pid through pipe
            os.close(newpipe_w)
            newpipe_r = os.fdopen(newpipe_r, 'r')
            childpid = newpipe_r.read()
            newpipe_r.close()
            rc = os.waitpid(pid, 0)  #wait for 1st fork'ed child to quit
            self.log.info('rc from waitpid was (%d, %d)' % rc)
            jobinfo['pid'] = childpid
            return jobinfo

    def kill_job(self, _, jobinfo):
        '''kills a job using via signal to pid'''
        # status_t jm_signal_job(db_job_id_t jid, rm_signal_t signal);
        print 'bgsystem got a kill_job call'
        pid = jobinfo.get('pid')
        signame = 'SIGINT'
        try:
            os.kill(int(pid), getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pid %s:%s" % (pid, error.strerror))
        return 0
#         signal = bgl_rm_api.rm_signal_t(15)
#         jobid = jobinfo.get('dbjobid')
#         bridge.jm_signal_job(jobid, signal)

    def query_jobs(self, _, jobsinfo):
        '''queries jobs via pid or PyBridge
        returns those jobs that are running'''
        return [job for job in jobsinfo
                if self.checkpid(job.get('pid'))]

    def checkpid(self, somepid):
        '''checks if the specified pid is still around'''
        ps = os.popen('ps ax')
        pids = ps.readlines()
        ps.close()
        pidlist = [p.split()[0] for p in pids]
        if str(somepid) in pidlist:
            return True
        else:
            return False

    def query_part(self, _, partinfo):
        '''queries partitions for status info'''
        return self.partitions.Get(partinfo)

    def full_partition_info(self, _):
        '''returns nested partition relation dictionary,
        and another dictionary of all partition attributes
        '''
        partition_relations = self.partitions.getDeps()

        return (partition_relations, [part.to_rx(part._attrib)
                                      for part in self.partitions])

if __name__ == '__main__':
    # setup option parsing
    parser = OptionParser()
    parser.add_option("-d", dest="debug", action="store_true", default=False,
                      help="Turn on debugging output")
    parser.add_option("-D", "--daemon", dest="daemon", default=False,
                      metavar="<pidfile>",
                      help="Run component as a daemon")
    (opts, args) = parser.parse_args()

#     newbase = BaseSystem()
#     for nc in newbase:
#         print nc._attrib

    __daemon__ = opts.daemon
    __dlevel__ = logging.INFO
    if opts.debug:
        __dlevel__ = logging.DEBUG
    Cobalt.Logging.setup_logging('bgsystem', level = __dlevel__, to_syslog=False)
    logger = logging.getLogger('bgsystem')
    __server__ = System({'configfile':'/etc/cobalt.conf', 'daemon':__daemon__})
    __server__.serve_forever()
