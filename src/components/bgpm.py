#!/usr/bin/env python

'''Process manager for Blue Gene/L systems'''
__revision__ = '$Revision$'

import atexit, logging, os, pwd, signal, sys, tempfile, time
import ConfigParser, Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy

"""bgpm api:
CreateProcessGroup({user: 'user', executable:'executable', args:['arg1', 'arg2'], location:['location'],
                     env={'key':'val'}, errfile:'/errfile', outfile:'/outfile', mode:'co|vn|smp|dual', size:'count', cwd:'cwd'})
                     """

class ProcessGroupCreationError(Exception):
    '''ProcessGroupCreation Error is used when not enough information is specified'''
    pass

class ProcessGroup(Cobalt.Data.Data):
    '''The ProcessGroup class implements all stages of running parallel processes'''
    def __init__(self, data, pgid):
        print 'bgpm got data', data
        data['tag'] = 'process-group'
        Cobalt.Data.Data.__init__(self, data)
        self.comms = Cobalt.Proxy.CommDict()
        self.log = logging.getLogger('pg')
        self.set('pgid', pgid)
        self.set('state', 'initializing')

        print 'bgpm going to startjob'
        result = self.comms['sys'].StartJob(data)
        #TODO sync from startjob to self
        print 'result was', result
        self.set('pid', result.get('pid'))
        self.pid = result.get('pid')
#        self.pid = os.fork()
#        if not self.pid:
#        self.log.info("Job %s/%s: Running %s" % (data.get('jobid'), data.get('user'), " ".join(cmd)))
#             apply(os.execl, cmd)
#            sys.exit(0)
#        else:
        self.set('state', 'running')
#         self.log.info("Job %s/%s: ProcessGroup %s Started on partition %s. pid: %s" % (self.get('jobid'), self.get('user'), pgid,
#                                                                                partition, self.pid))
        #AddEvent("process-manager", "process_start", pgid)

    def FinishProcess(self, status):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        self.set('state', 'finished')
        self.log.info("Job %s/%s: ProcessGroup %s Finished with exit code %d. pid %s" % \
                      (self.get('jobid'), self.get('user'), self.get('pgid'),
                       int(status)/256, self.pid))
        #AddEvent("process-manager", "process_end", self.element.get('pgid'))
        if not self.get('outputfile', False):
            self.set('output', open(self.outlog).read())
        if not self.get('errorfile', False):
            self.set('error', open(self.errlog).read())
        self.set('exit-status', {'BG/L':status})

    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(int(self.pid), getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.get('pgid'), error.strerror))
        return 0

    def Kill(self):
        '''Kill Blue Gene job. This method is more vicious; it is processed through the bridge API
        Not Yet Implemented'''
#         self.comms['system'].KillJob()

class BGProcessManager(Cobalt.Component.Component, Cobalt.Data.DataSet):
    '''The BGProcessManager supports the BG/L process execution model'''
    __implementation__ = 'bgpm'
    __name__ = 'process-manager'
    __object__ = ProcessGroup
    __id__ = Cobalt.Data.IncrID()
    async_funcs = ['assert_location', 'manage_children']
    comms = Cobalt.Proxy.CommDict()

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
        '''queries the system component with a list of process groups
        system component should check for the jobs using whatever mechanism
        it chooses (pid, PyBridge) and return those jobs that are running. Those
        that are not running, but still listed in self are called FinishProcess.
        (this loses the exit code)
        '''
        if (time.time() - self.lastwait) > 6:
            self.lastwait = time.time()
            result = self.comms['sys'].QueryJobs([pg.to_rx(pg._attrib) for pg in self.data])
            result_pgs = [pg.get('pgid') for pg in result]
            for pg in self:
                if pg.get('pgid') not in result_pgs:
                    pg.FinishProcess(0)
                    
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
        for pg in self.data:
            if pg.get('pgid') == data['pgid']:
                return pg.Signal(sig)
        # could not find pg, so return False
        return False

    def kill_processgroup(self, address, data):
        '''kill existing process group'''
        return self.signal_processgroup(address, data, 'SIGINT')
    
    def SigChildHand(self, sig, frame):
        '''Dont Handle SIGCHLDs'''
        pass
    
if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arg) = getopt(sys.argv[1:], 'dC:D:', ['notbgl'])
    except GetoptError,msg:
        print "%s\nUsage:\nbgpm.py [-d] [-C config file] [-D <pidfile>] [--notbgl]" % (msg)
        raise SystemExit, 1
    try:
        daemon = [item[1] for item in opts if item[0] == '-D'][0]
    except:
        daemon = False
    if len([item for item in opts if item[0] == '-d']):
        dlevel=logging.DEBUG
    else:
        dlevel=logging.INFO
    Cobalt.Logging.setup_logging('bgpm', level=dlevel)
    s = BGProcessManager({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    s.serve_forever()
