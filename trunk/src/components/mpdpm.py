#!/usr/bin/env python

import logging, os, sys, tempfile, time, xml.dom.minidom
import ConfigParser, Cobalt.Component, Cobalt.Data, Cobalt.Logging

'''mpdpm api:
CreateProcessGroup({user: 'user', executable:'executable', args:['arg1', 'arg2'], location:['location'],
                     env = {'key':'val'}, errfile:'/errfile', outfile:'/outfile', mode:'co|vn', size:'count', cwd:'cwd'})
                     '''

class ProcessGroupCreationError(Exception):
    '''ProcessGroupCreation Error is used when not enough information is specified'''
    pass

class ProcessGroup(Cobalt.Data.Data):
    '''ProcessGroup is a subclassed sss.restriction.Data object that implements mpd process groups'''
    required_fields = ['pgid']
    _configfields = ['mpdpath', 'outputspool']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('mpdpm'):
        print '''"mpdpm" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['mpdpm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1

    def __init__(self, data, pgid):
        print "I am initializing a process group"
        self.log = logging.getLogger('pg')
        data['tag'] = 'process-group'
        data['pgid'] = pgid
        print "attempting to create data object"
        try:
            Cobalt.Data.Data.__init__(self, data)
        except:
            self.log.error("FAILED TO CREATE DATA OBJECT",exc_info=1)
        print "I created a data object"

        self.set('pgid', pgid)
        self.set('state', 'initializing')
        self.mpdpid = None
        self.mpdxml = xml.dom.minidom.Element('create-process-group')
        if self.get('outputfile', False):
            self.outlog = self.get('outputfile')
        else:
            self.outlog = tempfile.mktemp()            
        if self.get('errorfile', False):
            self.errlog = self.get('errorfile')
        else:
            self.errlog = tempfile.mktemp()            
        if self.get('mpdfile', False):
            self.mpdlog = self.get('mpdfile')
        else:
            self.mpdlog = tempfile.mktemp()            
        if self.get('exitfile', False):
            self.exitlog = self.get('exitfile')
        else:
            self.exitlog = tempfile.mktemp()
        print "I am going to start a process"
        self.ProcessStart()
    
    def ProcessStart(self):
        '''ProcessStart starts the execution of the process group'''
        self.set('state', 'running')
        self.log.info("PGid %s Started"%(self.get('pgid')))
        self.createMPDfile()
        self.log.info("running :%s:"%("%s/mpdrun.py -f %s "%(self.config['mpdpath'], self.mpdlog)))
        pid = os.fork()
        if pid:
            self.log.info("Got pid %s for pgid %s"%(pid, self.get('pgid')))
            self.mpdpid = pid
        else:
            null = open('/dev/null', 'r')
            out = open(self.outlog, 'w')
            err = open(self.errlog, 'w')
            os.dup2(null.fileno(), sys.__stdin__.fileno())
            os.dup2(out.fileno(), sys.__stdout__.fileno())
            os.dup2(err.fileno(), sys.__stderr__.fileno())
            os.execl("%s/mpdrun.py"%(self.config['mpdpath']), 'mpdrun', '-f', self.mpdlog)

    def createMPDfile(self):
        '''This functions pull the information out of the process object and creates
        an xml document that can be used by the mpdrun command'''
        self.mpdxml.setAttribute('exit_codes_filename', self.exitlog )
        self.mpdxml.setAttribute('output', "merged" )
        self.mpdxml.setAttribute('pgid', '%s'%self.get('pgid') )
        self.mpdxml.setAttribute('state', self.get('state') )
        self.mpdxml.setAttribute('submitter', self.get('user') )
        self.mpdxml.setAttribute('totalprocs', '%s'%self.get('size') )
        counter = 1
        #I need a process spec created( how did I forget )
        processxml = xml.dom.minidom.Element('process-spec')
        processxml.setAttribute('cwd', self.get('cwd'))
        processxml.setAttribute('exec', self.get('executable'))
        processxml.setAttribute('path', self.get('path', '/bin:/usr/bin:/usr/local/bin'))
        processxml.setAttribute('user', self.get('user'))
        for mpdarg in self.get('args'):
            tempxml = xml.dom.minidom.Element( 'arg' )
            tempxml.setAttribute( 'idx', '%s'%counter )
            tempxml.setAttribute( 'value', mpdarg )
            processxml.appendChild(tempxml)
            counter += 1
        for key, val in self.get('env', {}):
            tempxml = xml.dom.minidom.Element('env')
            tempxml.setAttribute( 'name', key )
            tempxml.setAttribute( 'value', val )
            processxml.appendChild(tempxml)
        self.mpdxml.appendChild(processxml)
        tempxml = xml.dom.minidom.Element('host-spec')
        tempxml.setAttribute('check', 'yes')
        tempdoc = xml.dom.minidom.Document()
        tempxml.appendChild(tempdoc.createTextNode("\n".join( self.get('location'))))

        self.mpdxml.appendChild(tempxml)
        open(self.mpdlog, 'w').write(self.mpdxml.toxml())
        
    def FinishProcess(self):
        '''FinishProcess cleans up after the execution of mpdrun has completed'''
        if not self.get('outputfile', False ):
            self.set('output', open(self.outlog).read())
        if not self.get('errorfile', False ):
            self.set('error', open(self.errlog).read())
        errorstates = {}
        try:
            for x in  xml.dom.minidom.parseString(open(self.exitlog).read()).getElementsByTagName('exit-code'):
                errorstates[x.getAttribute('rank')] = x.getAttribute('status')
        except IOError:
            self.log.info("Failed to read exit status file for pgid %s"%(self.get('pgid')))
        except:
            self.log.info("Exit Status exit parse failure for pgid %s"%(self.get('pgid')))

        self.set('exit-status', errorstates )
        self.log.info("PGid %s Exited"%(self.get('pgid')))
        self.set('state', "finished")
        
    def Signal(self, signal, scope):
        '''Signal used to signal the job process'''
        pid = os.fork()
        if pid:
            return pid
        self.log.info("PGid %s signaled with %s"%(self.get('pgid'), signal))
        if signal == 'SIGINT':
            self.log.info("PGid %s killed"%(self.get('pgid')))
            os.execl("%s/mpdkilljob.py"%(self.config['mpdpath']), "mpdkilljob", '-a', self.get('pgid'))            
        else:
            if scope == 'single':
                sopt = '-s'
            else:
                sopt = '-g'
            os.execl("%s/mpdsigjob.py"%(mpdpath), "mpdsigjob", signal, '-a', self.get('pgid'), sopt)


class MPDProcessManager(Cobalt.Component.Component, Cobalt.Data.DataSet):
    '''The MPD Process Manager Object'''
    __implementation__ = 'mpdpm'
    __name__ = 'process-manager'
    __object__ = ProcessGroup
    __id__ = Cobalt.Data.IncrID()
    async_funcs = ['assert_location', 'manage_children']
    
    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        Cobalt.Data.DataSet.__init__(self)
        self.ignore = []
        self.returns = []
        self.lastwait = 0
        # need to add handlers here
        self.register_function(self.create_processgroup, "CreateProcessGroup")
        self.register_function(self.get_processgroup, "GetProcessGroup")
        self.register_function(self.signal_processgroup, "SignalProcessGroup")
        self.register_function(self.wait_processgroup, "WaitProcessGroup")
        self.register_function(self.kill_processgroup, "KillProcessGroup")

    def manage_children(self):
        '''manage_children insures that all of the spawned processes are maintained and collected'''
        if (time.time() - self.lastwait) > 6:
            while True:
                try:
                    self.lastwait = time.time()
                    (pid, stat) = os.waitpid(-1, os.WNOHANG)
                except OSError:
                    break
                if pid == 0:
                    break
                pgrps = [pgrp for pgrp in self.data if pgrp.mpdpid == pid]
                if len(pgrps) == 0:
                    self.logger.error("Failed to locate process group for pid %s" % (pid))
                elif len(pgrps) == 1:
                    pgrps[0].FinishProcess()
                else:
                    self.logger.error("Got more than one match for pid %s" % (pid))

    def create_processgroup(self, address, data):
        '''Create new process group element'''
        print "I am creating a process group"
        return self.Add(data)

    def get_processgroup(self, address, data):
        '''query existing process group'''
        return self.Get(data)

    def wait_processgroup(self, address, data):
        '''Remove completed process group'''
        return self.Del(data)

    def signal_processgroup(self, address, data, sig):
        '''signal existing process group with specified signal'''
        for pgroup in self.data:
            if pgroup.get('pgid') == data['pgid']:
                return pgroup.Signal(sig)
        # could not find pg, so return None
        return None

    def kill_processgroup(self, address, data):
        '''kill existing process group'''
        return self.signal_processgroup(address, data, 'SIGINT')
    
    def SigChildHand(self, sig, frame):
        '''Dont Handle SIGCHLDs'''
        pass


if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        (opts, arg) = getopt(sys.argv[1:], 'dC:D:m:')
    except GetoptError, msg:
        print "%s\nUsage:\nmpdpm.py [-d] [-C config file] [-D <pidfile>] [-m </path/to/mpd> ]" % (msg)
        raise SystemExit, 1
    Cobalt.Logging.setup_logging('mpdpm', level = 0)
    try:
        daemon = [item[1] for item in opts if item[0] == '-D'][0]
    except:
        daemon = False
    try:
        mdppath = [item[1] for item in opts if item[0] == '-m'][0]
    except:
        mpdpath = False
    ldebug = len([item for item in opts if item[0] == '-d'])
    s = MPDProcessManager({'configfile':'/etc/cobalt.conf', 'daemon':daemon, 'mpdpath':mpdpath})
    s.serve_forever()
    
