#!/usr/bin/env python

'''HappyNSM implements a node state manager with diagnostic capabilities'''
__revision__ = '$Revision$'

from os import environ, getuid, fork, close
from pwd import getpwuid
from signal import signal, SIGINT
from select import select
from syslog import syslog, LOG_INFO, LOG_ERR
from cPickle import dumps, loads
from elementtree.ElementTree import Element, SubElement, tostring, XML
from time import strftime, localtime
import re

from sss.server import BufferedPipe, MsgError, EventReceiver
from sss.ssslib import comm_lib
from sss.restriction import DataSet, Data

class NodeState(Data):
    '''NodeStates track client states'''
    def UpdateNST(self, arglist):
        for test in self.element.getchildren():
            if test.get("test") == arglist["test"]:
                self.element.remove(test)
            self.element.append(Element("testresult", test=arglist["test"],
                                        status=arglist["status"], output=arglist["output"]))
        self.element.set("adminstate", "online")
        for test in self.element.getchildren():
            if test.get("status")!="0":
                self.element.set("adminstate", "offline")
        return

class happynsm(EventReceiver):
    '''Diagnostic node state manager'''
    __component__ = 'node-state-manager'
    __implementation__ = 'happynsm'
    __statefields__ = ['nsdata']
    __dispatch__ = {   'get-node-state':'nsdata.Get',
                       'set-node-state':'XSet',
                       'add-node-state':'nsdata.Add',
                       'del-node-state':'nsdata.Del',
                       'update-node-state':'nsdata.UpdateNST',
                       'diagnose':'Diagnose',
                       'events':'HandleEvent'}
    __validate__ = 0

    def __setup__(self):
        self.__subscriptions__ = [('process-manager', 'process_end', '**')]
        self.pgids = []
        self.nsdata = DataSet('node-states', 'node-state', NodeState, None, False)
        self.readConf('/etc/happynsm.conf')

    def readConf(self, filename):
        '''Read Configuration File'''
        try:
            for data in open(filename, 'r').readlines():
                (var, value) = data.split('=')
                value = value.strip()
                setattr(self, var, value.split(','))
        except IOError, e:
            print "Unable to open the happynsm.conf file: ", e

    def XSet(self, xml, (peer, port)):
        self.changed_nodes = {}
        result = self.nsdata.Get(xml, (peer, port), self.Set)
        self.evt.WriteMessage(dumps(self.changed_nodes.keys()))
        return result

    def Set(self, item, attrib):
        for x in attrib.keys():
            if item.attr[x] != attrib[x]:
                item.attr[x] = attrib[x]
                self.changed_nodes[item.attr['node']] = 1

    def HandleEvent(self, xml, (peer, port)):
        '''process events from the event manager'''
        for event in xml.findall('event'):
            (c, m, d) = tuple([event.attrib[field] for field in ['component', 'msg', 'data']])
            if c == 'process-manager':
                if m == 'process_end':
                    for (x, y, (peer, port)) in self.pgids:
                        if d == x:
                            self.recvDiagnosis(x, y, (peer, port))
                            self.pgids.remove((x, y, (peer, port)))
        return Element('event-ok')

    def Diagnose(self, xml, (peer, port)):
        '''run diagnostics on nodes'''
        nodes = xml.attrib['node'].strip()
        nodelist = nodes.split(',')
        tests = xml.attrib['test'].strip()
        testlist = tests.split(',')
        #make this more advanced, support better description of nodes
        #if there is a nodename duplicated

        for testname in testlist:
            for executable in getattr(self, testname):
                self.sendMPDMessage(executable, nodelist, (peer, port)) 
        return Element('event-ok')
   
    def recvDiagnosis(self, pgid, executable, (peer, port)):
        test = executable.split("/")[len(executable.split("/"))-1].split(" ")[0].strip()
        comm = comm_lib(debug='-d' in argv)
        msg = XML("<wait-process-group><process-group pgid='%s' submitter='*'><output/><exit-status><exit-code host='*' pid='*' rank='*' status='*'/></exit-status></process-group></wait-process-group>"%(pgid))
        pm = comm.ClientInit('process-manager')
        comm.SendMessage(pm, tostring(msg))
        ack = comm.RecvMessage(pm)
        comm.ClientClose(pm)
        try:
            xmlack = XML(ack)
            xmlexitcodes =  xmlack.find("process-group").find("exit-status").findall("exit-code")
            output = xmlack.find("process-group").findtext("output")
            syslog(LOG_INFO, "Got exit-info for pgid %s recieved successfully."%(pgid))
        except:
            print "there was an error reciving exit-codes from the Process Manager"
            return "<event-failed />"

        listoutput =  re.split('(\d+:)', output)
        del listoutput[0]
        corroutput = zip([listoutput[x] for x in range(0, len(listoutput), 2)],
                         [listoutput[x] for x in range(1, len(listoutput), 2)])

        noderes = {}
        for node in xmlexitcodes:
            outputlines = ""
            for (x, y) in corroutput:
                if node.get("rank") + ":" == x:
                    outputlines += y + "\n"

        noderes[node] = Element("testresult", host=node.get("host"), test=test, status=node.get("status"), output=outputlines)

        xml = Element("get-node-state")
        for node in noderes.keys():
            xml.append(Element("node-state", adminstate="*", host=node.get("host"), state="*"))
        nodestates = self.nsdata.Get(xml, (peer, port))
        for node in noderes.keys():
            try:
                nodestate = [nds for nds in nodestates.findall('node-state') if nds.get('host') == noderes[node].get('host')]
            except:
                syslog(LOG_ERR, "Failed to get node-state event")
                return
             
        if nodestate != []:
            self.nsdata.Get(XML('''<update-node-state test="%s" status="%s" output="%s"><node-state adminstate="*" host="%s" state="*"/></update-node-state>''' % (noderes[node].get("test"), noderes[node].get("status"), noderes[node].get("output"), noderes[node].get("host"))), (peer, port), lambda x, y:x.UpdateNST(y))

        else:
            syslog(LOG_ERR, "Failed to send state-changed event")
        return

    def sendMPDMessage(self, executable, nodelist, (peer, port)):
        #Simply, this creates, sends, and gets output from the Process Manager. 
        numprocs   = str(len(nodelist))
        submitter = getpwuid(getuid())[0]

        path = environ['PATH']
        cwd = environ['PWD']
        msg = Element("create-process-group", pgid='*', submitter=submitter, totalprocs=numprocs, output='label')
        ps = Element("process-spec", user=submitter, path=path, cwd=cwd)
        ps.attrib['exec'] = executable
        msg.append(ps)
        #host spec
        nodetext = ''
        for node in nodelist:
            nodetext = nodetext + node + '\n'
        hs = Element("host-spec", check='yes')
        hs.text = nodetext
        msg.append(hs)

        comm = comm_lib(debug='-d' in argv)
        process_manager = comm.ClientInit('process-manager')
        comm.SendMessage(process_manager, tostring(msg))
        ack = comm.RecvMessage(process_manager)
        comm.ClientClose(process_manager)
        r = XML(ack)
        pgid = r.attrib.get('pgid', None)
        self.pgids.append((pgid, executable, (peer, port)))
        #add this pgid to acceptable pgids list
        if not pgid:
            syslog(LOG_ERR, "Failed to recieve PGID")
            return
        else:
            syslog(LOG_INFO, "Got PGID %s\nwaiting for event data" % (pgid))
        return
   
    def ChildSigHand(self, signum, frame):
        raise SystemExit, 0
    
    def __setupChildren__(self):
        self.evt = BufferedPipe()
        self.pipes.append(self.evt)
        pid = fork()
        if pid == 0:
            signal(SIGINT, self.ChildSigHand)
            self.readsockets = [self.evt.r]
            self.socketdispatch = {self.evt.r:self.ProcessChanges_cb}
            self.ServeForever()
        else:
            close(self.evt.r)
            return [pid]

    def ProcessChanges_cb(self, pipe, inl=None):
        '''Read changes from pipe and create events for them'''
        while 1:
            try:
                (infd, out, x) = select([pipe], [], [], 5)
                # Catch and disregard the traceback on child process exit
            except:
                pass
            if infd != []:
                self.evt.ReadMessages()

            while self.evt.buffer:
                try:
                    changed_nodes = loads(self.evt.ReadMessage())
                except MsgError:
                    break
      
                # Send state changed message
                doc = Element('add-event')
                for node in changed_nodes:
                    SubElement(doc, 'event', component=self.__component__, 
                               msg='state-changed', data=node, 
                               time=strftime("%c",localtime()))
                if len(doc) > 0:
                    try:
                        c = comm_lib()
                        h = c.ClientInit('event-manager')
                        c.SendMessage(h, tostring(doc))
                        c.RecvMessage(h)
                        c.ClientClose(h)
                    except:
                        syslog(LOG_ERR, "Failed to send state-changed event")
      
                del doc

if __name__ == '__main__':
    from getopt import getopt, GetoptError
    from sys import argv
    try:
        (opts, args) = getopt(argv[1:], 'd', ['daemon='])
    except GetoptError, msg:
        print "%s\nUsage:\nnsm.py [-d] [--daemon <pidfile>]" % (msg)
        raise SystemExit, 1
    daemon = [item for item in opts if item[0] == '--daemon']
    ldebug = len([item for item in opts if item[0] == '-d'])
    if daemon:
        from sss.daemonize import daemonize
        daemonize(daemon[0][1])
    server = happynsm(debug=ldebug)
    server.ServeForever()
