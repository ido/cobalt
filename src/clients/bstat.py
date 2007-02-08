#!/usr/bin/env python

import Cobalt.Proxy

if __name__ == '__main__':
    sim = Cobalt.Proxy.simulator()
    data = sim.GetState()
    data.sort()
    if data:
        fmt = "%14s | %s | %s"
        print fmt % ("Partition"," Used", "Blocked")
        print "================================"
        for line in data:
            print fmt % tuple(line)
