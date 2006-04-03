#!/usr/bin/env python

from os import unlink, dup2, execl, stat, waitpid, WNOHANG
from popen2 import Popen4
from select import error as selecterror
from signal import signal, SIGCHLD, SIG_DFL
import sys
from sys import exit
from string import split, strip
from syslog import syslog, LOG_INFO, LOG_ERR, LOG_LOCAL0, openlog
from tempfile import mktemp
from time import time, sleep
from select import select
from base64 import encodestring

from elementtree.ElementTree import Element, XML, tostring

from sss.restriction import Data, DataSet, ID
from sss.server import Server, AddEvent
from sss.ssslib import ConnectError

mpdpath='/usr/mpi/bin'
outputspool='/tmp'

class ProcessGroup(Data):
    '''ProcessGroup is a subclassed sss.restriction.Data object that implements mpd process groups'''
    def __init__(self,element, pgid):
        Data.__init__(self,element)
        self.element.tag = "process-group"
        self.element.attrib['pgid'] = pgid
        self.element.attrib['state'] = 'running'
        self.mpdpid = None
        for attr in ['outfile','errfile','mpdfile','exitfile']:
            setattr(self,attr,mktemp())
        self.MPIStart()
    
    def MPIStart(self):
        '''MPIStart starts the execution of the process group'''
        self.element.attrib['state'] = 'running'
        syslog(LOG_INFO,"PGid %s Started"%(self.element.attrib['pgid']))
        try:
            AddEvent('process-manager','process_start',self.element.attrib['pgid'])
        except:
            syslog(LOG_ERR, "Error sending process_start for pgid %s"%(self.element.attrib['pgid']))
        # Dump out xml file
        self.element.tag = "create-process-group"
        self.element.attrib['exit_codes_filename'] = self.exitfile
        # add check='yes' to hs
        for node in self.element.findall('host-spec'):
            node.attrib['check'] = 'yes'
        open(self.mpdfile,'w').write(tostring(self.Fetch()))
        # Then fix all values
        self.element.tag = "process-group"
        for node in self.element.findall('host-spec'):
            del node.attrib['check']
        syslog(LOG_INFO, "running :%s:"%("%s/mpdrun.py -f %s "%(mpdpath,self.mpdfile)))
        pid=fork()
        if pid:
            syslog(LOG_INFO, "Got pid %s for pgid %s"%(pid, self.attr['pgid']))
            self.mpdpid=pid
        else:
            null=open('/dev/null','r')
            out=open(self.outfile,'w')
            err=open(self.errfile,'w')
            dup2(null.fileno(),sys.__stdin__.fileno())
            dup2(out.fileno(),sys.__stdout__.fileno())
            dup2(err.fileno(),sys.__stderr__.fileno())
            execl("%s/mpdrun.py"%(mpdpath), 'mpdrun','-f', self.mpdfile)

    def MPIFinish(self):
        '''MPIFinish cleans up after the execution of mpdrun has completed'''
        output = Element("output")
        err = Element("error")
        output.text = encodestring(open(self.outfile).read())
        err.text = encodestring(open(self.errfile).read())
        self.element.attrib['encoding'] = 'base64'
        es = Element("exit-status")
        try:
            map(lambda x:es.append(x), XML(open(self.exitfile).read()).findall('exit-code'))
        except IOError:
            syslog(LOG_ERR, "Failed to read exit status file for pgid %s"%(self.element.attrib['pgid']))
        except:
            syslog(LOG_ERR, "Exit Status exit parse failure for pgid %s"%(self.element.attrib['pgid']))
        self.element.append(output)
        self.element.append(err)
        self.element.append(es)
        for file in ['outfile','errfile','mpdfile','exitfile']:
            try:
                unlink(getattr(self,file))
            except:
                syslog(LOG_ERR, "Failed to unlink %s: %s"%(file,getattr(self,file)))
        syslog(LOG_INFO,"PGid %s Exited"%(self.element.attrib['pgid']))
        try:
            AddEvent('process-manager','process_end',self.element.attrib['pgid'])
        except:
            syslog(LOG_ERR, "Error sending process_end for pgid %s"%(self.element.attrib['pgid']))
        # Send out completion
        self.element.attrib['state'] = "finished"

        
    def Signal(self, signal, scope):
        pid = fork()
        if pid:
            return pid
        syslog(LOG_INFO,"PGid %s signaled with %s"%(self.element.attrib['pgid'],signal))
        if scope == 'single':
            s = '-s'
        else:
            s = '-g'
        execl("%s/mpdsigjob.py"%(mpdpath), "mpdsigjob", signal, '-a', self.element.attrib['pgid'], s)

    def MPDKill(self):
        pid = fork()
        if pid:
            return pid
        syslog(LOG_INFO,"PGid %s killed"%(self.element.attrib['pgid']))
        execl("%s/mpdkilljob.py"%(mpdpath), "mpdkilljob", '-a', self.element.attrib['pgid'])

    def Fetch(self,spec=None):
        data = Data.Fetch(self,spec)
        if self.element.attrib['state'] == 'running':
            if self.element.findall('process'):
                old = signal(SIGCHLD, SIG_DFL)
                mp=Popen4("%s/mpdlistjobs -a %s -sss"%(mpdpath,self.pgid))
                mp.wait()
                out=mp.fromchild.readlines()
                for (host,pid,session) in map(split,map(strip,out)):
                    data.append(Element("process", host=host, pid=pid, session=session))
                signal(SIGCHLD, old)
        return data

class mpd(Server):
    __implementation__ = 'mpdpm'
    __component__ = 'process-manager'
    __timeout__ = 0.5
    __statefields__ = ['pg']
    __dispatch__ = {'kill-process-group':'XKillPG',
                    'wait-process-group':'pg.Del',
                    'create-process-group':'AddPG',
                    'signal-process-group':'XSigPG',
                    'get-process-group-info':'pg.Get'}
    
    def __setup__(self):
        self.pg = DataSet("process-groups", "process-group", ProcessGroup, ID(), True)
        self.returns = []
        self.ignore = []
        try:
            stat("%s/mpdrun.py"%(mpdpath))
        except OSError:
            openlog('mpdpm',0,LOG_LOCAL0)
            syslog(LOG_ERR, "Error finding mpd. exiting")
            exit(1)

    def AddPG(self, xml, (peer, port)):
        '''This is needed since the pm syntax isnt quite restriction-like'''
        pg = ProcessGroup(xml, str(self.pg.idalloc.get()))
        self.pg.data.append(pg)
        return pg.Fetch(xml)

    def XSigPG(self, xml, (peer,port)):
        return self.pg.Get(xml, (peer,port), self.SigPG)

    def SigPG(self, pg, args):
        self.ignore.append(pg.Signal(args['signal'], args.get('scope', 'single')))

    def XKillPG(self, xml, (peer,port)):
        return self.pg.Get(xml, (peer,port), self.KillPG)

    def KillPG(self,pg, args):
        self.ignore.append(pg.MPDKill())

    def __progress__(self):
        num = 0
        try:
            (pid,stat) = waitpid(-1,WNOHANG)
            if pid != 0:
                self.returns.append((pid,stat))
        except OSError, e:
            if e.errno != 10:
                syslog(LOG_ERR, "Waitpid failed with %s"%(e))
        while self.returns:
            (pid,stat) = self.returns.pop()
            if pid in self.ignore:
                self.ignore.remove(pid)
                continue
            pg = [ x for x in self.pg if x.mpdpid == pid ]
            if len(pg) == 1:
                pg[0].MPIFinish()
                num += 1
            elif len(pg) == 0:
                syslog(LOG_ERR, "Got sigchld for unknown pid %s"%(pid))
        return num

    def SigChildHand(self,sig,frame):
            pass

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    from os import fork
    from sys import argv,exit
    try:
        (opts,args)=getopt(argv[1:],'dm:',['daemon='])
    except GetoptError,msg:
        print "%s\nUsage:\nmpdpm.py [-d] [-m <path to mpd> ] [--daemon <pidfile>]"%(msg)
        exit(1)
    daemon=filter(lambda x:(x[0] == '--daemon'),opts)
    mpath=filter(lambda x:(x[0] == '-m'),opts)
    ldebug=len(filter(lambda x:(x[0] == '-d'),opts))
    if mpath:
        mpdpath=mpath[0][1]
    if daemon:
        from sss.daemonize import daemonize
        daemonize(daemon[0][1])
    s=mpd(debug=ldebug)
    s.ServeForever()
