#!/usr/bin/env python

import logging, sys, lxml.etree
import Cobalt.Component, Cobalt.Logging
logger = logging.getLogger('bgsched')

class Brooklyn(Cobalt.Component.Component):
    '''Brooklyn is a bgl bridge simulator'''
    __implementation__ = 'brooklyn'
    __name__ = 'simulator'

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        self.partitions = {}
        self.readConfigFile('/home/desai/partitions.xml')
        self.used = []
        self.blocked = []
        self.register_function(self.GetMachineState, "GetState")
        self.register_function(self.GetMachineStateDB2, "GetDB2State")
        self.register_function(self.ReservePartition, "ReservePartition")
        self.register_function(self.ReleasePartition, "ReleasePartition")

    def readConfigFile(self, path):
        self.partitions = {}
        doc = lxml.etree.parse(path)
        rack = doc.getroot()
        parents = {}
        children = {}
        sizes = {}
        for partition in rack.findall('Partition'):
            parents[partition.get('name')] = []
            children[partition.get('name')] = [p.get('name') \
                                               for p in partition.findall('.//Partition')]
            work = partition.findall('Partition')
            sizes[partition.get('name')] = int(partition.get('size'))
        while work:
            next = work.pop()
            work += next.findall('Partition')
            children[next.get('name')] = [p.get('name') \
                                          for p in next.findall('.//Partition')]
            npar = next.getparent().get('name')
            parents[next.get('name')] = [npar] + parents[npar]
            sizes[next.get('name')] = int(next.get('size'))
        for part in parents:
            self.partitions[part] = (parents[part], children[part], sizes[part])

    def GetMachineStateDB2(self, conn):
        '''Return db2-like list of tuples describing state'''
        return [(name, self.used[name]) for name in self.partitions]

    def GetMachineState(self, conn):
        '''Return an overall description of machine state'''
        return [(part, part in self.used, part in self.blocked) for \
                part in self.partitions]

    def GenBlocked(self):
        '''Generate the blocked table from the values of self.used'''
        self.blocked = []
        for partition in [p for p in self.partitions if p in self.used]:
            for relative in self.partitions[partition][0] \
                    + self.partitions[partition][1]:
                self.blocked.append(relative)

    def ReservePartition(self, conn, name, size):
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
        self.used.append(name)
        logger.info("After reservation:")
        logger.info(self.used)
        self.GenBlocked()
        return True

    def ReleasePartition(self, conn, name):
        '''Release used partition'''
        if name not in self.used:
            logger.error("Tried to release free partition %s" % name)
            return False
        else:
            self.used.remove(name)
            logger.info("After release:")
            if self.used:
                logger.info(self.used)
            else:
                logger.info(" Empty")
            self.GenBlocked()
            return True

if __name__ == '__main__':
    from getopt import getopt, GetoptError
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
    server = Brooklyn({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    server.serve_forever()
    

