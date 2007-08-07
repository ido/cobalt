#!/usr/bin/env python

import logging, sys, lxml.etree, operator
from xml.etree import ElementTree as ET
from getopt import getopt, GetoptError
import Cobalt.Component, Cobalt.Logging
logger = logging.getLogger('bgsched')

class Brooklyn(Cobalt.Component.Component):
    '''Brooklyn is a bgl bridge simulator'''
    __implementation__ = 'brooklyn'
    __name__ = 'simulator'

    def __init__(self, setup):
        Cobalt.Component.Component.__init__(self, setup)
        self.partitions = {}
        self.nodecards = set()
        self.readConfigFile(setup.get('partconfig'))
#         self.readNodeCardConfigFile(setup.get('ncfile'))
        self.used = []
        self.blocked = []
        self.usednodecards = set()
        self.register_function(self.GetMachineState, "GetState")
        self.register_function(self.GetMachineStateDB2, "GetDB2State")
        self.register_function(self.ReservePartition, "ReservePartition")
        self.register_function(self.ReleasePartition, "ReleasePartition")
        self.register_function(self.GetPartition, "GetPartition")
        self.register_function(self.ReserveNodecards, "ReserveNodecards")
        self.register_function(self.ReleaseNodecards, "ReleaseNodecards")

    def readConfigFile(self, path):
        self.partitions = {}
        doc = lxml.etree.parse(path)
        rack = doc.getroot()
        parents = {}
        children = {}
        sizes = {}
        nodecards = {}
        print rack.findall('Partition')
        for partition in rack.findall('Partition'):
            parents[partition.get('name')] = []
            children[partition.get('name')] = [p.get('name') \
                                               for p in partition.findall('.//Partition')]
            print 'children for %s are' % partition.get('name'), children[partition.get('name')]
            nodecards[partition.get('name')] = set([n.get('name') for n in partition.findall('.//Nodecard')])
            work = partition.findall('Partition')
            sizes[partition.get('name')] = int(partition.get('size'))
        while work:
            next = work.pop()
            work += next.findall('Partition')
            children[next.get('name')] = [p.get('name') \
                                          for p in next.findall('.//Partition')]
            nodecards[next.get('name')] = set([n.get('name') for n in next.findall('.//Nodecard')])
            
            npar = next.getparent().get('name')
            parents[next.get('name')] = [npar] + parents[npar]
            sizes[next.get('name')] = int(next.get('size'))
        for part in parents:
            self.partitions[part] = (parents[part], children[part], sizes[part], nodecards[part])

        for p in self.partitions.values():
            self.nodecards.update(p[3])

        print self.nodecards
#     def readNodeCardConfigFile(self, path):
#         '''reads node cards from xml'''
#         self.nodecards = {}
#         print 'parsing', path
#         doc = ET.parse(path)
#         rack = doc.getroot()
#         for basepart in rack:
#             for nodecard in basepart:
#                 nodecard.attrib.update({'basepart':basepart.get('id')})
#                 self.nodecards.update({'%s-%s' % (basepart.get('id'), nodecard.get('id')):nodecard.attrib})
        
#         print self.nodecards
#         for x in self.nodecards:
#             print x, self.nodecards[x]

    def GetMachineStateDB2(self, conn):
        '''Return db2-like list of tuples describing state'''
        return [(name, self.used[name]) for name in self.partitions]

#     def GetMachineState(self, conn):
#         '''Return an overall description of machine state'''
#         return [(part, part in self.used, part in self.blocked) for \
#                 part in self.partitions]

    def GetMachineState(self, _):
        '''simulates DataSet get'''
        result = []
        print 'self.usednodecards', self.usednodecards, self.nodecards
        for nc in self.nodecards:
            if nc in self.usednodecards:
                state = 'used'
            else:
                state = 'idle'
            result.append({'tag':'nodecard', 'name':nc, 'state':state})
        result.sort(key=operator.itemgetter('name'))
        print result
        return result

    def GetPartition(self, _, query):
        pass

    def GenBlocked(self):
        '''Generate the blocked table from the values of set self.usednodecards'''
        self.blocked = []
        if not self.usednodecards:
            return
        for partition in self.partitions:
            print self.partitions[partition][3]
            if self.partitions[partition][3] == self.usednodecards:
                print 'this is the partition being used', partition
                print self.used
            elif self.partitions[partition][3].issubset(self.usednodecards):
                print 'partition %s is subset of busy nodecards %s' % (partition, self.usednodecards)
                self.blocked.append(partition)
            elif self.partitions[partition][3].issuperset(self.usednodecards):
                print 'partition %s is superset of busy nodecards %s' % (partition, self.usednodecards)
                self.blocked.append(partition)
            else:
                print 'partition %s is not super or sub' % partition

        logger.info("blocked partitions %s" % self.blocked)

#         for partition in [p for p in self.partitions if p in self.used]:
#             for relative in self.partitions[partition][0] \
#                     + self.partitions[partition][1]:
#                 self.blocked.append(relative)

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
        '''returns list of possible groups of that size'''
        nclist = list(self.nodecards)
        nclist.sort()
        print self.nodecards, nclist
        if group_size > len(nclist):
            logger.error("Tried to use %d nodecards in a %d nodecard system" % (group_size, len(nclist)))
            return []
        possible_groups = []
        stencil_size = len(nclist)/group_size
        for x in range(0, len(nclist), group_size):
            possible_groups.append(nclist[x:x+group_size])
        return possible_groups

    def ReleaseNodecards(self, _, nclist):
        '''Release group of nodecards'''
        if not self.usednodecards.issuperset(nclist):
            logger.error("Tried to release some free nodecards %s" % nclist)
            return False
        else:
            self.usednodecards.difference_update(set(nclist))
            logger.info("After release:")
            if self.usednodecards:
                logger.info(list(self.usednodecards))
            else:
                logger.info(" Empty")
            self.GenBlocked()
            return True

    def ReleasePartition(self, conn, name):
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
    

