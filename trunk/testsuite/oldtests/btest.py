#!/usr/bin/env python
'''This script is a regression test of brooklyn'''

import Cobalt.Proxy

class testor:
    def __init__(self):
        self.sim = Cobalt.Proxy.simulator()

    def same(self):
        print "Running same partition test:",
        status = self.sim.ReservePartition('R000_J214-32', 16)
        if not status:
            print "FAILURE"
            print "Failed to reserve partition"
            return False
        status = self.sim.ReservePartition('R000_J214-32', 16)
        self.sim.ReleasePartition('R000_J214-32')
        if not status:
            print "SUCCESS"
            return True

    def toosmall(self):
        print "Running job too big test:",
        status = self.sim.ReservePartition('R000_J214-32', 76)
        if not status:
            print "SUCCESS"
            return True
        else:
            self.sim.ReleasePartition('R000_J214-32')
            print "FAILURE"
            return False

    def overlap(self):
        print "Running overlapping partition test:",
        status = self.sim.ReservePartition('R000_J214-32', 16)
        if not status:
            print "FAILURE"
            print "Failed to reserve partition"
            return False
        status = self.sim.ReservePartition('R000_J214-64', 16)
        self.sim.ReleasePartition('R000_J214-32')
        if not status:
            print "SUCCESS"
            return True
        else:
            self.sim.ReleasePartition('R000_J214-64')
            print "FAILURE"
            return False

    def runall(self):
        for test in [self.same, self.toosmall, self.overlap]:
            test()

if __name__ == '__main__':
    t = testor()
    t.runall()
