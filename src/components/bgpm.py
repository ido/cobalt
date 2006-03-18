#!/usr/bin/env python

'''Process manager for Blue Gene/L systems'''
__revision__ = '$Revision: 1.21 $'

import atexit, logging, os, pwd, signal, sys, tempfile, time
import ConfigParser, Cobalt.Component, Cobalt.Data, Cobalt.Logging

'''bgpm api:
CreateProcessGroup({user: 'user', executable:'executable', args:['arg1', 'arg2'], location:['location'],
                     env={'key':'val'}, errfile:'/errfile', outfile:'/outfile', mode:'co|vn', size:'count', cwd:'cwd'})
                     '''

class ProcessGroupCreationError(Exception):
    '''ProcessGroupCreation Error is used when not enough information is specified'''
    pass

class ProcessGroup(Cobalt.Data.Data):
    '''The ProcessGroup class implements all stages of running parallel processes'''
    # read in config from cobalt.conf
    required_fields = ['user', 'executable', 'args', 'location', 'size', 'cwd']
    _configfields = ['mmcs_server_ip', 'db2_instance', 'bridge_config', 'mpirun', 'db2_properties', 'db2_connect']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('bgpm'):
        print '''"bgpm" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['bgpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1

    def __init__(self, data, pgid):
        data['tag'] = 'process-group'
        Cobalt.Data.Data.__init__(self, data)
        self.log = logging.getLogger('pg')
        self.set('pgid', pgid)
        self.set('state', 'initializing')
        if self.get('outputfile', False):
            self.outlog = self.get('outputfile')
        else:
            self.outlog = tempfile.mktemp()            
        if self.get('errorfile', False):
            self.errlog = self.get('errorfile')
        else:
            self.errlog = tempfile.mktemp()

        if not self.get('location', False):
            raise ProcessGroupCreationError, "location"
        partition = self.get('location')[0]
            
        try:
            userid, groupid = pwd.getpwnam(self.get('user'))[2:4]
        except KeyError:
            raise ProcessGroupCreationError, "user/group"

        self.pid = os.fork()
        if not self.pid:
            program = self.get('executable')
            cwd = self.get('cwd')
            pnum = str(self.get('size'))
            mode = self.get('mode', 'co')
            args = " ".join(self.get('args', []))
            # strip out BGLMPI_MAPPING until mpirun bug is fixed 
            mapfile = ''
            if self.get('env', {}).has_key('BGLMPI_MAPPING'):
                mapfile = self.get('env')['BGLMPI_MAPPING']
                del self.get('env')['BGLMPI_MAPPING']
            envs = " ".join(["%s=%s" % envdata for envdata in self.get('env', {}).iteritems()])
            atexit._atexit = []
            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                self.log.error("Failed to change userid/groupid for PG %s" % (self.get("pgid")))
                sys.exit(0)
            #system("/bgl/BlueLight/ppcfloor/bglsys/bin/db2profile > /dev/null 2>&1")
            os.system("%s > /dev/null 2>&1" % (self.config['db2_connect']))
            os.environ["DB_PROPERTY"] = self.config['db2_properties']
            os.environ["BRIDGE_CONFIG_FILE"] = self.config['bridge_config']
            os.environ["MMCS_SERVER_IP"] = self.config['mmcs_server_ip']
            os.environ["DB2INSTANCE"] = self.config['db2_instance']
            os.environ["LD_LIBRARY_PATH"] = "/u/bgdb2cli/sqllib/lib"
            null = open('/dev/null', 'r')
            os.dup2(null.fileno(), sys.__stdin__.fileno())
            cmd = (self.config['mpirun'], "mpirun", '-np', pnum, '-partition', partition,
                               '-mode', mode, '-cwd', cwd, '-exe', program)
            if args != '':
                cmd = cmd + ('-args', args)
            if envs != '':
                cmd = cmd + ('-env',  envs)
            if mapfile != '':
                cmd = cmd + ('-mapfile', mapfile)

            if '--notbgl' in sys.argv:
                cmd = (program, os.path.basename(program), args)

            self.log.error("User %s: Running %s" % (self.get('user'), " ".join(cmd)))
            try:
                err = open(self.errlog, 'w')
                os.chmod(self.errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Failed to open stderr file %s. Stderr will be lost" % (self.errlog))
            try:
                out = open(self.outlog, 'w')
                os.chmod(self.outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Failed to open stdout file %s. Stdout will be lost" % (self.outlog))
            apply(os.execl, cmd)
            sys.exit(0)
        else:
            self.set('state', 'running')
            self.log.info("ProcessGroup %s Started on partition %s. pid: %s" % (pgid,
                                                                                partition, self.pid))
            #AddEvent("process-manager", "process_start", pgid)

    def FinishProcess(self, status):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        self.set('state', 'finished')
        self.log.info("User %s: ProcessGroup %s Finshed. pid %s" % (self.get('user'),
                                                                    self.get('pgid'), self.pid))
        #AddEvent("process-manager", "process_end", self.element.get('pgid'))
        if not self.get('outputfile', False):
            self.set('output', open(self.outlog).read())
        if not self.get('errorfile', False):
            self.set('error', open(self.errlog).read())
        self.set('exit-status', {'BG/L':status})

    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(self.pid, getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.get('pgid'), error.strerror))

    def Kill(self):
        '''Kill Blue Gene job. This method is more vicious; it is processed through the bridge API
        Not Yet Implemented'''
        pass

class BGProcessManager(Cobalt.Component.Component, Cobalt.Data.DataSet):
    '''The BGProcessManager supports the BG/L process execution model'''
    __implementation__ = 'bgpm'
    __name__ = 'process-manager'
    __object__ = ProcessGroup
    __id__ = Cobalt.Data.IncrID()
    async_funcs = ['assert_location', 'manage_children']

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        Cobalt.Data.DataSet.__init__(self)
        self.ignore = []
        self.lastwait = 0
        # need to add handlers here
        self.register_function(self.create_processgroup, "CreateProcessGroup")
        self.register_function(self.get_processgroup, "GetProcessGroup")
        self.register_function(self.signal_processgroup, "SignalProcessGroup")
        self.register_function(self.wait_processgroup, "WaitProcessGroup")
        self.register_function(self.kill_processgroup, "KillProcessGroup")

    def manage_children(self):
        if (time.time() - self.lastwait) > 6:
            while True:
                try:
                    self.lastwait = time.time()
                    (pid, stat) = os.waitpid(-1, os.WNOHANG)
                except OSError:
                    break
                if pid == 0:
                    break
                pgrps = [pgrp for pgrp in self.data if pgrp.pid == pid]
                if len(pgrps) == 0:
                    self.logger.error("Failed to locate process group for pid %s" % (pid))
                elif len(pgrps) == 1:
                    pgrps[0].FinishProcess(stat)
                else:
                    self.logger.error("Got more than one match for pid %s" % (pid))

    def create_processgroup(self, address, data):
        '''Create new process group element'''
        return self.Add(data)

    def get_processgroup(self, address, data):
        '''query existing process group'''
        return self.Get(data)

    def wait_processgroup(self, address, data):
        '''Remove completed process group'''
        return self.Del(data)

    def signal_processgroup(self, address, data, sig):
        '''signal existing process group with specified signal'''
        pass
                    
    def kill_processgroup(self, address, data):
        '''kill existing process group'''
        pass
    
    def SigChildHand(self, sig, frame):
        '''Dont Handle SIGCHLDs'''
        pass
    
if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arg) = getopt(sys.argv[1:], 'dC:', ['daemon=', 'notbgl'])
    except GetoptError,msg:
        print "%s\nUsage:\nbgpm.py [-d] [-C config file] [--daemon <pidfile>] [--notbgl]" % (msg)
        raise SystemExit, 1
    Cobalt.Logging.setup_logging('bgpm', level=0)
    daemon = [item for item in opts if item[0] == '--daemon']
    ldebug = len([item for item in opts if item[0] == '-d'])
    if daemon:
        from sss.daemonize import daemonize
        daemonize(daemon[0][1])
    s = BGProcessManager({'configfile':'/etc/cobalt.conf'})
    s.serve_forever()
