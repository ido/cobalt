#!/usr/bin/env python

import logging, sys, lxml.etree, operator, os, pwd, atexit, ConfigParser, tempfile, signal
from getopt import getopt, GetoptError
import Cobalt.Component, Cobalt.Logging, Cobalt.Data
logger = logging.getLogger('bgsched')

def checkpid(somepid):
    '''checks if the specified pid is still around'''
    process_list = os.popen('ps ax')
    pids = process_list.readlines()
    process_list.close()
    pidlist = [p.split()[0] for p in pids]
    if str(somepid) in pidlist:
        return True
    else:
        return False

class ProcessGroupCreationError(Exception):
    '''ProcessGroupCreation Error is used when not enough information is specified'''
    pass

class Partition (Cobalt.Data.Data):
    fields = Cobalt.Data.Data.fields.copy()
    fields.update(dict(
        scheduled = False,
        name = None,
        functional = False,
        queue = "default",
        state = "idle",
        size = None,
    ))

class PartitionSet (Cobalt.Data.DataSet):
    __object__ = Partition

class Brooklyn(Cobalt.Component.Component):
    '''Brooklyn is a bgl bridge simulator'''
    __implementation__ = 'brooklyn'
    __name__ = 'system'

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        self.log = logger
        self.partitions = {}        #dictionary of part:(parents, children, sizes, nodecards)
        self.partitioninfo = PartitionSet()
        self.nodecards = set()      #set of nodecard names
        self.nodecardinfo = {}      #nested dictionary for nodecard info
        self.readConfigFile(setup.get('partconfig'))
        self.used = []              #list of used partitions
        self.blocked = []           #list of blocked (overlapping) partitions
        self.usednodecards = set()  #set of used nodecard names

        self.config = ConfigParser.ConfigParser()
        self.config.read(setup.get('configfile'))
        
        self.register_function(self.GetMachineState, "GetState")
        self.register_function(self.GetMachineStateDB2, "GetDB2State")
        self.register_function(self.ReservePartition, "ReservePartition")
        self.register_function(self.ReleasePartition, "ReleasePartition")
        self.register_function(self.GetPartition, "GetPartition")
        self.register_function(self.ReserveNodecards, "ReserveNodecards")
        self.register_function(self.ReleaseNodecards, "ReleaseNodecards")
        self.register_function(self.StartJob, "StartJob")
        self.register_function(self.query_jobs, "QueryJobs")
        self.register_function(self.kill_job, "KillJob")


    def readConfigFile(self, path):
        '''reads hardware info from xml (partitions, nodecards)'''
        self.partitions = {}
        doc = lxml.etree.parse(path)
        rack = doc.getroot()
        parents = {}
        children = {}
        sizes = {}
        nodecards = {}
        
        racknodecards = rack.findall('.//Nodecard')
        for racknode in racknodecards:
            newname = "%s-%s" % (racknode.get('bpid'), racknode.get('id'))
            self.nodecardinfo[newname] = {'tag':'nodecard', 'bpid':racknode.get('bpid'),
                                          'id':racknode.get('id'), 'queue':'default'}
        rackpartitions = rack.findall('.//Partition')
        for rackpart in rackpartitions:
            self.partitioninfo.Add([{'tag':'partition', 'name':rackpart.get('name'),
                                     'queue':'default', 'scheduled':True,
                                     'functional':True, 'state':'idle',
                                     'size':rackpart.get('size')}])

        for partition in rack.findall('Partition'):
            parents[partition.get('name')] = []
            children[partition.get('name')] = [p.get('name') \
                                               for p in partition.findall('.//Partition')]
            nodecards[partition.get('name')] = set(["%s-%s" % (n.get('bpid'), n.get('id')) for n in partition.findall('.//Nodecard')])
            work = partition.findall('Partition')
            sizes[partition.get('name')] = int(partition.get('size'))
        while work:
            next = work.pop()
            work += next.findall('Partition')
            children[next.get('name')] = [p.get('name') \
                                          for p in next.findall('.//Partition')]
            nodecards[next.get('name')] = set(["%s-%s" % (n.get('bpid'), n.get('id')) for n in next.findall('.//Nodecard')])
            
            npar = next.getparent().get('name')
            parents[next.get('name')] = [npar] + parents[npar]
            sizes[next.get('name')] = int(next.get('size'))
        for part in parents:
            self.partitions[part] = (parents[part], children[part],
                                     sizes[part], nodecards[part])

        #build nodecard set() of names (duplicates are ignored)
        for part in self.partitions.values():
            self.nodecards.update(part[3])

    def GetMachineStateDB2(self, _):
        '''Return db2-like list of tuples describing state'''
        return [(name, name in self.used and 'I' or 'F') for name in self.partitions]

    def GetMachineState(self, _):
        '''returns hardware state (nodecards)'''
        result = []

        for nc in self.nodecards:
            if nc in self.usednodecards:
                state = 'used'
            else:
                state = 'idle'
            result.append({'tag':'nodecard', 'name':nc,
                           'bpid':self.nodecardinfo[nc]['bpid'],
                           'id':self.nodecardinfo[nc]['id'], 'state':state,
                           'queue':self.nodecardinfo[nc]['queue']})
        result.sort(key=operator.itemgetter('bpid', 'id'))

        return result

    def getorderedlist(self, nodelist, newsize, depth, result_list):
        '''searches for partition whose nodecards match groups of nodecards in nodelist
        nodelist is ordered list of nodecards in system
        newsize is the size of the stencil used to match partition nodecards
        result_list is where the partitions are appended in order
        '''
        for x in range(0, len(nodelist), newsize):
            search_nodes = nodelist[x:x+newsize]
            for p in self.partitions:
                if self.partitions[p][3] == set(search_nodes):
                    result_list.append(p)
                    self.partitioninfo.Get([{'tag':'partition', 'name':p}], lambda x,y: x.update(y), {'depth':depth})
                    if newsize > 1:
                        self.getorderedlist(nodelist[x:x+newsize], newsize/2, depth+1, result_list)

    def GetPartition(self, _, query):
        '''returns query like DataSet.Get'''
        nclist = sorted(list(self.nodecards))
        olist = []
        depth = 0
        self.getorderedlist(nclist, len(nclist), depth, olist)

        response = self.partitioninfo.Get(query)
        for part in response:
            if part.get('name') in self.used:
                part.update({'state':'busy'})
            elif part.get('name') in self.blocked:
                part.update({'state':'blocked'})
            else:
                part.update({'state':'idle'})

        # reorder response based on olist
        newlist = []
        for opart in olist:
            ordered_part = [p for p in response if p.get('name') == opart]
            if ordered_part:
                newlist.append(ordered_part[0])

        return newlist

    def GenBlocked(self):
        '''Generate the blocked table from the values of set self.usednodecards'''
        self.blocked = []
        if not self.usednodecards:
            return
        for partition in self.partitions:
            if self.partitions[partition][3] == self.usednodecards:
                print 'this is probably the partition being used', partition
                print self.used
            elif self.partitions[partition][3].issubset(self.usednodecards):
                self.blocked.append(partition)
            elif self.partitions[partition][3].issuperset(self.usednodecards):
                self.blocked.append(partition)

        logger.info("blocked partitions %s" % self.blocked)

    def ReservePartition(self, _, name, size):
        '''Reserve partition and block all related partitions'''
        if name not in self.partitions:
            logger.error("Tried to use nonexistent partition %s" % (name))
            return False
        if name in self.used:
            logger.error("Tried to use busy partition %s" % (name))
            return False
        if name in self.blocked:
            logger.error("Tried to use blocked partition %s" % (name))
            return False
        if size > self.partitions[name][2]:
            logger.error("Partition %s too small for job size %s" % (name, size))
            return False
        self.usednodecards.update(self.partitions[name][3])
        self.used.append(name)
        logger.info("After reservation:")
        print self.used
        print self.usednodecards
        self.GenBlocked()
        return True

    def ReserveNodecards(self, _, nodecards):
        '''Reserve group of nodecards'''
        for nc in nodecards:
            if nc not in self.nodecards:
                logger.error("Tried to use nonexistant nodecard %s" % (nc))
                return False
            if nc in self.usednodecards:
                logger.error("Tried to use busy nodecard %s" % (nc))
                return False
        # check with stencil for proper allocation
        ncsize = len(nodecards)
        possible_ncgroups = self.GetPossibleNodegroups(ncsize)
        if nodecards not in possible_ncgroups:
            logger.error("Tried to use non-contiguous group of nodecards %s" % nodecards)
            return False
        self.usednodecards.update(nodecards)
        logger.info("After reservation:")
        logger.info(tuple(self.usednodecards))
#         logger.info(self.used)
        self.GenBlocked()
        return True

    def GetPossibleNodegroups(self, group_size):
        '''returns list of possible groups of nodecards of size group_size'''
        nclist = list(self.nodecards)
        nclist.sort()
        if group_size > len(nclist):
            logger.error("Tried to use %d nodecards in a %d nodecard system" % (group_size, len(nclist)))
            return []
        possible_groups = []
        for x in range(0, len(nclist), group_size):
            possible_groups.append(nclist[x:x+group_size])
        return possible_groups

    def ReleaseNodecards(self, _, nclist):
        '''Release group of nodecards'''
        if not self.usednodecards.issuperset(nclist):
            logger.error("Tried to release some free nodecards: %s" % set(nclist).difference(self.usednodecards))
            return False
        else:
            self.usednodecards.difference_update(set(nclist))
            logger.info("After release:")
            if self.usednodecards:
                logger.info(list(self.usednodecards))
            else:
                logger.info(" Empty")
            self.GenBlocked()
            print "blocked: ", self.blocked
            return True

    def ReleasePartition(self, _, name):
        '''Release used partition'''
        if name not in self.used:
            logger.error("Tried to release free partition %s" % name)
            return False
        else:
            self.used.remove(name)
            for nc in self.partitions[name][3]:
                self.usednodecards.remove(nc)
            logger.info("After release:")
            if self.used:
                logger.info(self.used)
            else:
                logger.info(" Empty")
            self.GenBlocked()
            return True

    def StartJob(self, _, jobinfo):
        '''starts a job'''
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
                outlog = jobinfo.get('outputfile')
            else:
                outlog = tempfile.mktemp()            
            if jobinfo.get('errorfile', False):
                errlog = jobinfo.get('errorfile')
            else:
                errlog = tempfile.mktemp()

            #check for location to run
            if not jobinfo.get('location', False):
                raise ProcessGroupCreationError, "location"
            partition = jobinfo.get('location')[0]

            #check for valid user/group
            try:
                userid, groupid = pwd.getpwnam(jobinfo.get('user', ""))[2:4]
            except KeyError:
                raise ProcessGroupCreationError, "user/group"

            program = jobinfo.get('executable')
            cwd = jobinfo.get('cwd')
            pnum = str(jobinfo.get('size'))
            mode = jobinfo.get('mode', 'co')
            args = " ".join(jobinfo.get('args', []))
            inputfile = jobinfo.get('inputfile', '')
            kerneloptions = jobinfo.get('kerneloptions') or ''
            # strip out BGLMPI_MAPPING until mpirun bug is fixed 
            mapfile = ''
            if jobinfo.get('env', {}).has_key('BGLMPI_MAPPING'):
                mapfile = jobinfo.get('env')['BGLMPI_MAPPING']
                del jobinfo.get('env')['BGLMPI_MAPPING']
            envs = " ".join(["%s=%s" % envdata for envdata in (jobinfo['envs'] or {}).iteritems()])
            atexit._atexit = []

            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                logger.error("Failed to change userid/groupid for PG %s" % (jobinfo.get("pgid")))
                sys.exit(0)

            #os.system("%s > /dev/null 2>&1" % (self.config.get('bgpm', 'db2_connect')))
            os.environ["DB_PROPERTY"] = self.config.get('bgpm', 'db2_properties')
            os.environ["BRIDGE_CONFIG_FILE"] = self.config.get('bgpm', 'bridge_config')
            os.environ["MMCS_SERVER_IP"] = self.config.get('bgpm', 'mmcs_server_ip')
            os.environ["DB2INSTANCE"] = self.config.get('bgpm', 'db2_instance')
            os.environ["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
            os.environ["COBALT_JOBID"] = jobinfo.get('jobid')
            if inputfile:
                infile = open(inputfile, 'r')
                os.dup2(infile.fileno(), sys.__stdin__.fileno())
            else:
                null = open('/dev/null', 'r')
                os.dup2(null.fileno(), sys.__stdin__.fileno())
            cmd = (self.config.get('bgpm', 'mpirun'), os.path.basename(self.config.get('bgpm', 'mpirun')),
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
                err = open(errlog, 'a')
                os.chmod(errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), errlog))

            try:
                out = open(outlog, 'a')
                os.chmod(outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (jobinfo.get('jobid'), jobinfo.get('user'), errlog))

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

    def query_jobs(self, _, jobsinfo):
        '''queries jobs via pid or PyBridge
        returns those jobs that are running'''
        print 'brooklyn: got query for these pid', [job.get('pid') for job in jobsinfo]
        return [job for job in jobsinfo
                if checkpid(job.get('pid'))]

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


if __name__ == '__main__':
    try:
        (opts, arguments) = getopt(sys.argv[1:], 'C:D:dt:f:', [])
    except GetoptError, msg:
        print "%s\nUsage:\nbrooklyn.py [-t <topo>] [-f failures] [-C configfile] [-d] [-D <pidfile>]" % (msg)
        raise SystemExit, 1
    try:
        daemon = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        daemon = False
    if len([x for x in opts if x[0] == '-d']):
        dlevel = logging.DEBUG
    else:
        dlevel = logging.INFO
    Cobalt.Logging.setup_logging('bgsched', level=dlevel)
    server = Brooklyn({'configfile':'/etc/cobalt.conf', 'daemon':daemon,
                       'partconfig':'../../misc/partitions.xml',
                       'ncfile':'../../misc/nodecards.xml'})
    server.serve_forever()
    

