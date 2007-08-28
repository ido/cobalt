#!/usr/bin/env python

import pprint
import sys, re, ConfigParser
import DB2
import Cobalt.Data

class Base(Cobalt.Data.Data):
    '''Base block datatype'''

    pass

class BaseSet(Cobalt.Data.DataSet):
    '''Defines a BG/L system'''
    __object__ = Base
    __ncdefs__ = {'J102':'N0', 'J104':'N1', 'J106':'N2', 'J108':'N3',
                  'J111':'N4', 'J113':'N5', 'J115':'N6', 'J117':'N7',
                  'J203':'N8', 'J205':'N9', 'J207':'NA', 'J209':'NB',
                  'J210':'NC', 'J212':'ND', 'J214':'NE', 'J216':'NF'}

    _configfields = ['db2uid', 'db2dsn', 'db2pwd']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('bgsched'):
        print '''"bgsched" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['bgsched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1

    def __init__(self, racks, psetsize):
        Cobalt.Data.DataSet.__init__(self)
        self.racks = racks
        self.psetsize = psetsize
        self.buildMachine()

    def getIONodes(self):
        '''Get location of i/o nodes from db2'''
        if '--nodb2' not in sys.argv:
            db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'), dsn=self.config.get('db2dsn')).cursor()

            db2.execute("SELECT LOCATION,IPADDRESS FROM tbglippool")
            results = db2.fetchall()
            ioreturn = [(location.strip(),ip) for (location, ip) in results]
            db2.close()
        else:
        #sample for 1:32 system
            ioreturn = [('R00-M1-NA-I:J18-U01', '172.30.0.53'),
                        ('R00-M1-NA-I:J18-U11', '172.30.0.54'),
                        ('R00-M1-NB-I:J18-U01', '172.30.0.55'),
                        ('R00-M1-NB-I:J18-U11', '172.30.0.56'),
                        ('R00-M1-NC-I:J18-U01', '172.30.0.57'),
                        ('R00-M1-NC-I:J18-U11', '172.30.0.58'),
                        ('R00-M1-ND-I:J18-U01', '172.30.0.59'),
                        ('R00-M1-ND-I:J18-U11', '172.30.0.60'),
                        ('R00-M1-NE-I:J18-U01', '172.30.0.61'),
                        ('R00-M1-NE-I:J18-U11', '172.30.0.62'),
                        ('R00-M1-NF-I:J18-U01', '172.30.0.63'),
                        ('R00-M1-NF-I:J18-U11', '172.30.0.64'),
                        ('R00-M1-N9-I:J18-U11', '172.30.0.52'),
                        ('R00-M0-N1-I:J18-U11', '172.30.0.4'),
                        ('R00-M0-N2-I:J18-U01', '172.30.0.5'),
                        ('R00-M0-N2-I:J18-U11', '172.30.0.6'),
                        ('R00-M0-N3-I:J18-U01', '172.30.0.7'),
                        ('R00-M0-N3-I:J18-U11', '172.30.0.8'),
                        ('R00-M0-N4-I:J18-U01', '172.30.0.9'),
                        ('R00-M0-N4-I:J18-U11', '172.30.0.10'),
                        ('R00-M0-N5-I:J18-U01', '172.30.0.11'),
                        ('R00-M0-N5-I:J18-U11', '172.30.0.12'),
                        ('R00-M0-N6-I:J18-U01', '172.30.0.13'),
                        ('R00-M0-N6-I:J18-U11', '172.30.0.14'),
                        ('R00-M0-N7-I:J18-U01', '172.30.0.15'),
                        ('R00-M0-N7-I:J18-U11', '172.30.0.16'),
                        ('R00-M0-N8-I:J18-U01', '172.30.0.17'),
                        ('R00-M0-N8-I:J18-U11', '172.30.0.18'),
                        ('R00-M0-N9-I:J18-U01', '172.30.0.19'),
                        ('R00-M0-N9-I:J18-U11', '172.30.0.20'),
                        ('R00-M0-NA-I:J18-U01', '172.30.0.21'),
                        ('R00-M0-NA-I:J18-U11', '172.30.0.22'),
                        ('R00-M0-NB-I:J18-U01', '172.30.0.23'),
                        ('R00-M0-NB-I:J18-U11', '172.30.0.24'),
                        ('R00-M0-NC-I:J18-U01', '172.30.0.25'),
                        ('R00-M0-NC-I:J18-U11', '172.30.0.26'),
                        ('R00-M0-ND-I:J18-U01', '172.30.0.27'),
                        ('R00-M0-ND-I:J18-U11', '172.30.0.28'),
                        ('R00-M0-NE-I:J18-U01', '172.30.0.29'),
                        ('R00-M0-NE-I:J18-U11', '172.30.0.30'),
                        ('R00-M0-NF-I:J18-U01', '172.30.0.31'),
                        ('R00-M0-N0-I:J18-U01', '172.30.0.1'),
                        ('R00-M0-N0-I:J18-U11', '172.30.0.2'),
                        ('R00-M0-N1-I:J18-U01', '172.30.0.3'),
                        ('R00-M0-NF-I:J18-U11', '172.30.0.32'),
                        ('R00-M1-N0-I:J18-U01', '172.30.0.33'),
                        ('R00-M1-N0-I:J18-U11', '172.30.0.34'),
                        ('R00-M1-N1-I:J18-U01', '172.30.0.35'),
                        ('R00-M1-N1-I:J18-U11', '172.30.0.36'),
                        ('R00-M1-N2-I:J18-U01', '172.30.0.37'),
                        ('R00-M1-N2-I:J18-U11', '172.30.0.38'),
                        ('R00-M1-N3-I:J18-U01', '172.30.0.39'),
                        ('R00-M1-N3-I:J18-U11', '172.30.0.40'),
                        ('R00-M1-N4-I:J18-U01', '172.30.0.41'),
                        ('R00-M1-N4-I:J18-U11', '172.30.0.42'),
                        ('R00-M1-N5-I:J18-U01', '172.30.0.43'),
                        ('R00-M1-N5-I:J18-U11', '172.30.0.44'),
                        ('R00-M1-N6-I:J18-U01', '172.30.0.45'),
                        ('R00-M1-N6-I:J18-U11', '172.30.0.46'),
                        ('R00-M1-N7-I:J18-U01', '172.30.0.47'),
                        ('R00-M1-N7-I:J18-U11', '172.30.0.48'),
                        ('R00-M1-N8-I:J18-U01', '172.30.0.49'),
                        ('R00-M1-N8-I:J18-U11', '172.30.0.50'),
                        ('R00-M1-N9-I:J18-U01', '172.30.0.51')]

        ioreturn.sort()

        # if only using 1 ionode per ionode processor card, filter out
        # every other entry in ioreturn
        if self.psetsize in [32, 128]:
            for x in ioreturn:
                if 'U11' in x[0]:
                    #print 'deleting', x
                    ioreturn.remove(x)
            
        return [re.sub('-I', '', x[0]) for x in ioreturn]

    def buildMachine(self):
        '''build machine representation from racks and psetsize'''
        ionodes = self.getIONodes()
        total_ionodes = (1024/self.psetsize) * self.racks  #total ionodes
        total_midplanes = self.racks * 2
        iopermidplane = total_ionodes/total_midplanes
        print 'total_ionodes: %d\ntotal_midplanes: %d\niopermidplane: %d' % (total_ionodes, total_midplanes, iopermidplane)
        print 'length of ionodes', len(ionodes)
        q = total_ionodes
        while q > 0:
            print 'self.psetsize/q', self.psetsize/q

            for x in range(0, total_ionodes, q):
                #print 'io extent=%d, starting ionode is %d' % (q, x)
                if q == total_ionodes:
                    #print 'defining whole machine block'
                    base_type = 'full'
                    topology = 'torus'
                elif q < total_ionodes and q > iopermidplane*2:
                    base_type = 'multirack'
                    topology = 'torus'
                elif q == iopermidplane*2:
                    #print 'defining rack', x / (iopermidplane*2)
                    base_type = 'rack'
                    topology = 'torus'
                elif q == iopermidplane:
                    #print 'defining R%d M%d' % (x / (iopermidplane*2), (x / iopermidplane) % 2)
                    base_type = 'midplane'
                    topology = 'torus'
                else:
                    #print 'defining R%d M%d N%d' % (x / (iopermidplane*2), (x / iopermidplane) % 2, x % (iopermidplane))
                    base_type = 'block'
                    topology = 'mesh'

                includedIOn = [ionodes[y] for y in range(x, x+q)]
                computeNodes = q * self.psetsize
                start_ionode = x
                rack = '%02d' % (x / (iopermidplane*2))
                midplane = '%d' % ((x / iopermidplane) % 2)
                self.Add([{'tag':'base', 'type':base_type, 'rack':rack, 'midplane':midplane,
                          'ionodes':includedIOn, 'computenodes':'%d' % computeNodes, 'psets':'%d' % q,
                          'state':'idle', 'topology':topology}])
            q = q / 2
        return

    def getMidplaneIONodes(self, rack, midplane):
        '''returns the ionodes in the midplane specified'''
        io = self.Get([{'tag':'base', 'rack':rack, 'midplane':midplane, 'ionodes':'*'}])
        if io:
            return io[0].get('ionodes')
        else:
            return None
        
class PartitionSet(Cobalt.Data.DataSet):
    '''dummy partitionset'''
    def __init__(self, racks, psetsize):
        Cobalt.Data.DataSet.__init__(self)
        #TODO read racks and pset size from conf file
        self.basemachine = BaseSet(racks, psetsize)

    def Add(self, cdata):
        '''if adding a partition, fetches the ionodes for it
        and adds them as a field'''
        for datum in cdata:
            print 'datum', datum
            if datum.get('tag') == 'partition':
                #todo: check if datum.has_key('name')
                # fetch ionodes from DB for partition
                pionodes = self.getPartIONodes(datum.get('name'))
                print 'pionodes are', pionodes

                # from the ionodes, fill in the rest of the attributes from the base block
                for block in self.basemachine:
                    if len(pionodes) == len([x for x in pionodes if x in block.get('ionodes')]) and len(pionodes) == len(block.get('ionodes')):
                        baseblock = block
                        print 'block matches', block.get('ionodes')
                for field in baseblock.fields:
                    if not datum.has_key(field) and field != 'stamp':
                        datum.update({field:baseblock.get(field)})
                #datum.tag = 'partition'
                Cobalt.Data.DataSet.Add(self, [datum])

    def getPartIONodes(self, partname):
        '''retrieves the IOnodes for the specified partition'''
        if '--nodb2' in sys.argv:
            iodict = {'32wayN0':['R00-M0-N0:J18-U01'],
                      '32wayN1':['R00-M0-N1:J18-U01'],
                      '32wayN2':['R00-M0-N2:J18-U01'],
                      '32wayN3':['R00-M0-N3:J18-U01'],
                      '64wayN01':['R00-M0-N0:J18-U01','R00-M0-N1:J18-U01'],
                      '64wayN23':['R00-M0-N2:J18-U01','R00-M0-N3:J18-U01'],
                      '128wayN0123':['R00-M0-N0:J18-U01','R00-M0-N1:J18-U01',
                                     'R00-M0-N2:J18-U01','R00-M0-N3:J18-U01']}
            return iodict.get(partname, None)

        ionodes = []
        db2 = DB2.connect(uid=self.config.get('db2uid'), pwd=self.config.get('db2pwd'), dsn=self.config.get('db2dsn')).cursor()
        
        # first get blocksize in nodes
        db2.execute("select size from BGLBLOCKSIZE where blockid='%s'" % partname)
        blocksize = db2.fetchall()
        print 'blocksize is', blocksize[0][0], 'nodes'

        if int(blocksize[0][0]) < 512:
            print "small block"
            #tBGLSMALLBLOCK (BLOCKID, POSINMACHINE, PSETNUM, IONODEPOS, IONODECARD, IONODECHIP, COMPNODEPOS, NUMCOMPUTE)
            db2.execute("select * from tBGLSMALLBLOCK where blockid='%s' order by ionodepos" % partname)
            result = db2.fetchall()
            for b in result:
                rack = b[1].strip()[1:3]
                midplane = b[1].strip()[-1]
                ionodes.append("R%s-M%s-%s:%s-%s" % (rack, midplane, self.__ncdefs__[b[3].strip()],
                                                     b[4].strip(), b[5].strip()))
        else:  #match up rack and midplane(s)?
            db2.execute("select bpid from TBGLBPBLOCKMAP where blockid='%s'" % partname)
            result = db2.fetchall()
            for b in result:
                rack = b[0].strip()[1:3]
                midplane = b[0].strip()[-1]
                print "R%s-M%s" % (rack, midplane)
                #ionodes = self.getIONodes(rack, midplane)
        db2.close()
        return ionodes

    def getParents(self, block):
        '''returns parents of partition, based on ionodes'''
        parents = [x for x in self.data
                   if len(block.get('ionodes')) == len([q for q in x.get('ionodes') if q in block.get('ionodes')])
                   and block.get('ionodes') != x.get('ionodes')]
        return parents

    def getChildren(self, block):
        '''returns children of partition, based on ionodes'''
        cionodes = block.get('ionodes')
        csize = len(cionodes)

        children = []
        for b in self.data:
            if len(b.get('ionodes')) < csize and [x for x in b.get('ionodes') if x in cionodes]:
                children.append(b)
        return children

if __name__ == '__main__':
    newpartset = PartitionSet(1, 32)
    
    newpartset.Add([{'tag':'partition', 'name':x} for x in ['32wayN0', '32wayN1', '32wayN2', '32wayN3', '64wayN01', '64wayN23', '128wayN0123']])
    
    machine = newpartset.Get([{'tag':'partition', 'psets':'*', 'startnc':'*', 'rack':'*', 'midplane':'*',
                               'ionodes':'*', 'computenodes':'*', 'type':'*', 'topology':'*', 'state':'*', 'name':'*'}])
    pprint.pprint(machine)
    
    for part in newpartset:
        print part.get('name'), [x.get('name') for x in newpartset.getChildren(part)], [x.get('name') for x in newpartset.getParents(part)]
