'''Breadboard Component'''

import time, logging, lxml.etree, fcntl, os, pwd, signal, sys, tempfile, atexit 
import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, query, automatic
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ProcessGroupCreationError, NodeAllocationError

__all__ = ['BBSystem', 'ProcessGroup']

REPO = "/var/lib/bcfg2/"

class ProcessGroup(Data):
    '''Run a process on a bb system'''
    fields = Data.fields + ['user', 'args', 'env', 'executable', 'size', 'cwd', 
              'location', 'nodes', 'outputfile', 'errorfile', 'id', 'state']
    required = ['user', 'executable', 'location']
    def __init__(self, data):
        Data.__init__(self, data)
        self.log = logging.getLogger('pg')
        self.state = 'initializing'
        self.id = data['id']
        self.pgid = data['id']
        self.exit_status = None
        self.user = data['user']
        self.executable = data['executable']
        if data['outputfile']:
            self.outlog = data['outputfile']
        else:
            self.outlog = tempfile.mktemp()
        if data['errorfile']:
            self.errlog = data['errorfile']
        else:
            self.errlog = tempfile.mktemp()
        if data['args']:
            self.args = [self.executable] + data['args']
        else:
            self.args = [self.executable]
        if data['env']:
            self.env = os.environ
            for k, v in data['env'].iteritems():
                self.env[k] = v
        else:
            self.env = os.environ
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            raise ProcessGroupCreationError, "user/group"
        self.location = data['location']
        self.pid = os.fork()
        if not self.pid:
            program = self.executable
            self.t = tempfile.NamedTemporaryFile()
            self.t.write("\n".join(self.location) + '\n')
            self.t.flush()
            # create a nodefile in /tmp
            os.environ['COBALT_NODEFILE'] = self.t.name
            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                self.log.error("Failed to change userid/groupid for PG %s" % 
                               (self.pgid))
                sys.exit(0)
            try:
                err = open(self.errlog, 'a')
                os.chmod(self.errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % 
                               (self.pgid, self.user, self.errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" %
                               (self.pgid, self.user, self.errlog))
            try:
                out = open(self.outlog, 'a')
                os.chmod(self.outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" %
                              (self.pgid, self.user, self.outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" %
                              (self.pgid, self.user, self.errlog))
            except:
                self.log.error("unknown error", exc_info=1)
            self.state = "running"
            try:
                os.execve(self.executable, self.args, self.env)
            except:
                self.log.error("Failed to execute script %s" % self.executable)

    def FinishProcess(self, status):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        self.state = "finished"
        self.exit_status = int(status)/256
        self.log.info("Job %s/%s: ProcessGroup %s Finished with exit code %d. pid %s" % \
                      (self.pgid, self.user, self.pgid,
                       self.exit_status, self.pid))
        bb_path = REPO + "BB/bb.xml"
        bb_file = open(bb_path, 'r+')
        # acquire lock on bb.xml
        start = time.time()
        while time.time() - start < 5:
            try:
                fcntl.lockf(bb_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                self.logger.error("Unable to acquire lock on metadata")
                continue
            else:
                break
        bb_tree = lxml.etree.parse(bb_file)
        root = bb_tree.getroot()
        for node in self.location:
            root.xpath(".//Node[@name='%s']" % node)[0].attrib['state'] = "free"
        bb_tree.write(bb_path)
        fcntl.lockf(bb_file.fileno(), fcntl.LOCK_UN)
        bb_file.close()

    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(self.pid, getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.pgid, error.strerror))
        return 0


class BBSystem(Component):
    '''BBSystem Component Class'''
    name = 'bbsystem'
    logger = logging.getLogger("Cobalt.Components.BBSystem")
    pgid = 0
    
    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.proc_groups = DataList()
        self.proc_groups.item_cls =  ProcessGroup
    
    def allocate(self, num_nodes):
        '''Return list of free nodes from bb.xml'''
        bb_path = REPO + "BB/bb.xml"
        bb_file = open(bb_path, 'r+')
        bb_tree = lxml.etree.parse(bb_file)
        self.logger.info("Searching for %d nodes" % num_nodes)
        # acquire lock on bb.xml
        start = time.time()
        while time.time() - start < 5:
            try:
                fcntl.lockf(bb_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                self.logger.error("Unable to acquire lock on metadata")
                continue
            else:
                break
        # find free nodes
        root = bb_tree.getroot()
        free = root.xpath(".//Node[@state='free']")
        if len(free) < num_nodes:
            self.logger.error("Not enough nodes.")
            raise NodeAllocationError
        free = free[:num_nodes]
        for node in free:
            node.attrib['state'] = "used"
        nodes = [node.attrib['name'] for node in free]
        bb_tree.write(bb_path)
        fcntl.lockf(bb_file.fileno(), fcntl.LOCK_UN)
        bb_file.close()
        self.logger.info("Allocating: " + ','.join(nodes))
        return nodes
        
    def create_processgroup(self, data):
        '''Create new process group element'''
        data['location'] = self.allocate(data['nodes'])
        data['id'] = self.pgid
        self.pgid += 1
        return [item.to_rx() for item in self.proc_groups.q_add([data])]
    create_processgroup = exposed(create_processgroup)

    def get_processgroup(self, data):
        '''query existing process group'''
        return [item.to_rx() for item in self.proc_groups.q_get([data])]
    get_processgroup = exposed(get_processgroup)

    def wait_processgroup(self, data):
        '''Remove completed process group'''
        return [itme.to_rx() for item in self.proc_groups.q_del([data])]
    wait_processgroup = exposed(wait_processgroup)

    def signal_processgroup(self, data, sig):
        '''signal existing process group with specified signal'''
        for pg in self.proc_groups:
            if pg.pgid == data['id']:
                return pg.Signal(sig)
        # could not find pg, so return False
        return False
    signal_processgroup = exposed(signal_processgroup)

    def kill_processgroup(self, data):
        '''kill existing process group'''
        return self.signal_processgroup(address, data, 'SIGINT')
    kill_processgroup = exposed(kill_processgroup)

    def wait_for_completion(self):
        '''Watch pid's for completed pg'''
        for pg in self.proc_groups:
            if pg.state != 'finished':
                exit_stat = os.waitpid(pg.pid, 0)
                pg.FinishProcess(exit_stat[1])
    wait_for_completion = automatic(wait_for_completion, 2)
