#!/usr/bin/env python

'''Process manager for the breadboard'''
__revision__ = '$Revision$'

import atexit
import logging
import os
import pwd
import signal
import sys
import tempfile
import time
import ConfigParser

import Cobalt
import Cobalt.Component
import Cobalt.Data
import Cobalt.Logging

import FTB
from ctypes import *

class ProcessGroup(Cobalt.Data.Data):
    '''Run a process on a bb system'''
    def __init__(self, data, pgid):
        data['tag'] = 'process-group'
        Cobalt.Data.Data.__init__(self, data)
        self.log = logging.getLogger('pg')
        self.set('pgid', pgid)
        self.set('state', 'initializing')
        try:
            userid, groupid = pwd.getpwnam(self.get('user', ""))[2:4]
        except KeyError:
            raise ProcessGroupCreationError, "user/group"
        if self.get('outputfile', False):
            self.outlog = self.get('outputfile')
        else:
            self.outlog = tempfile.mktemp()            
        if self.get('errorfile', False):
            self.errlog = self.get('errorfile')
        else:
            self.errlog = tempfile.mktemp()

        self.pid = os.fork()
        if not self.pid:
            program = self.get('executable')
            self.t = tempfile.NamedTemporaryFile()
            self.t.write("\n".join(self.get('location').split(':')) + '\n')
            self.t.flush()
            # create a nodefile in /tmp
            os.environ['COBALT_NODEFILE'] = self.t.name
            try:
                os.setgid(groupid)
                os.setuid(userid)
            except OSError:
                self.log.error("Failed to change userid/groupid for PG %s" % (self.get("pgid")))
                sys.exit(0)
            try:
                err = open(self.errlog, 'a')
                os.chmod(self.errlog, 0600)
                os.dup2(err.fileno(), sys.__stderr__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stderr file %s. Stderr will be lost" % (self.get('jobid'), self.get('user'), self.errlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stderr will be lost" % (self.get('jobid'), self.get('user'), self.errlog))
            try:
                out = open(self.outlog, 'a')
                os.chmod(self.outlog, 0600)
                os.dup2(out.fileno(), sys.__stdout__.fileno())
            except IOError:
                self.log.error("Job %s/%s: Failed to open stdout file %s. Stdout will be lost" % (self.get('jobid'), self.get('user'), self.outlog))
            except OSError:
                self.log.error("Job %s/%s: Failed to chmod or dup2 file %s. Stdout will be lost" % (self.get('jobid'), self.get('user'), self.errlog))
            os.execl(self.get('executable'), self.get('executable'))

    def FinishProcess(self, status):
        '''Handle cleanup for exited process'''
        # process has already been waited on
        self.set('state', 'finished')
        self.log.info("Job %s/%s: ProcessGroup %s Finished with exit code %d. pid %s" % \
                      (self.get('jobid'), self.get('user'), self.get('pgid'),
                       int(status)/256, self.pid))
        os.system("/usr/bin/bbfree %s" % \
                  (node for node in self.get('location').split(':')))

    def Signal(self, signame):
        '''Send a signal to a process group'''
        try:
            os.kill(self.pid, getattr(signal, signame))
        except OSError, error:
            self.log.error("Signal failure for pgid %s:%s" % (self.get('pgid'), error.strerror))
        return 0

class BBProcessManager(Cobalt.Component.Component, Cobalt.Data.DataSet):
    '''The BGProcessManager supports the BG/L process execution model'''
    __implementation__ = 'bbpm'
    __name__ = 'process-manager'
    __object__ = ProcessGroup
    __id__ = Cobalt.Data.IncrID()
    async_funcs = ['assert_location', 'manage_children', 'get_FTB_events']

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
        properties = FTB.component_properties(0x02, 0x200000000 | 0x15, \
                                              'bbpm', 1, 20)
        FTB.libftb.FTB_Init(byref(properties))
        mask = FTB.event_mask(0xffffffff, 0xffffffff, 0xffffffff,
                              0xffffffffffffffff)
        FTB.libftb.FTB_Reg_catch_polling(byref(mask))
    
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

    def get_FTB_events(self):
        ret = 0
        evt = FTB.event_inst()
        while not ret:
            ret = FTB.libftb.FTB_Catch(byref(evt))
            if ret == 0:
                print 'caught event id %d, name %s' % (evt.event_id, evt.name)
    def start_shutdown(self, signum, frame):
        '''Shutdown on unexpected signals'''
        Cobalt.Component.Component.start_shutdown(self, signum, frame)
        FTB.libftb.FTB_Finalize()

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
        print "%s\nUsage:\nbbpm.py [-d] [-C config file] [-D <pidfile>]" % (msg)
        sys.exit(1)
    try:
        daemon = [item[1] for item in opts if item[0] == '-D'][0]
    except:
        daemon = False
    if len([item for item in opts if item[0] == '-d']):
        dlevel=logging.DEBUG
    else:
        dlevel=logging.INFO
    Cobalt.Logging.setup_logging('bbpm', level=dlevel)
    s = BBProcessManager({'configfile':Cobalt.CONFIG_FILES, 'daemon':daemon})
    s.serve_forever()
