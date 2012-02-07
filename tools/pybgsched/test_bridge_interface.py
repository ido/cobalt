#!/usr/bin/python

import pybgsched
from nose.tools import raises

class TestStartup(object):

    def test_init(self):
        
        pybgsched.init("/home/richp/bg.properties")
        return

    def test_refreshConfiguration(self):
        
        pybgsched.init("/home/richp/bg.properties")
        ret = pybgsched.refreshConfiguration()
        assert ret, "Configuration refresh failed."
    
    @raises(IOError)
    def test_bad_init(self):
        pybgsched.init("bad_file")
        return


class TestCore(object):


    pybgsched.init("/home/richp/bg.properties")
    zero_coords_4 = pybgsched.Coordinates(0,0,0,0)
    zero_coords_5 = pybgsched.Coordinates(0,0,0,0,0)
    
    def test_getComputeHardware(self):
        h = pybgsched.getComputeHardware()
        assert h != None, 'pybgsched.getComputeHardware() returned None.'
        assert isinstance(h, pybgsched.ComputeHardware),\
                'getComputeHardware returned improper class.  Reports as %s' % type(h)
        return

    def test_getMachineSize(self):
        machineSize = pybgsched.Coordinates(1,1,2,2)
        c = pybgsched.getMachineSize()
        assert machineSize == c, 'getMachineSize returned wrong size.'
        return

    def test_getMidplaneCooridnates(self):
        c = pybgsched.getMidplaneCoordinates('R00-M0')
        assert self.zero_coords_4 == c, 'Midplane R00-M0 returned bad coords.'

    def test_getNodeBoards(self):
        nbv = pybgsched.getNodeBoards('R00-M0')
        assert len(nbv) == 16, "Improper number of NodeBoards returned." 
        for i in range(0,len(nbv)):
            assert nbv[i].getLocation() == 'R00-M0-N%02d' % i, \
                    "Improper NodeBoard locations being returned."
        return

    def test_getNode(self):
        nv = pybgsched.getNodes('R00-M0-N00')
        assert len(nv) == 32, "Improper number of Nodes returned"
        for i in range(0,len(nv)):
            assert nv[i].getLocation() == 'R00-M0-N00-J%02d' % i, \
                    "Improper Node locations being returned."
        return

    def test_getIOLinks(self):
        lv = pybgsched.getIOLinks('R00-M0')
        assert len(lv) == 8, "Improper number of IOLinks returned." 
        for i in range(0, len(lv)):
            target = 'R00-M0-N%02d-J%02d' % (i/2*4, 6 + i%2 * 5)
            assert lv[i].getLocation() == target, \
                    "Improper Node locations being returned. Expected %s got %s" % (target, lv[i].getLocation())
        return

class TestNodeBoard(object):
    pass

class TestNode(object):
    pass

class TestIOLinks(object):
    pass

class TestMidplane(object):
    pass
