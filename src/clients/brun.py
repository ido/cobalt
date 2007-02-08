#!/usr/bin/env python

'''This script simulates the standard bridge mpirun for brooklyn'''

import sys, Cobalt.Proxy, time

if __name__ == '__main__':
    if '-partition' not in sys.argv[1:]:
        print "ERROR: -partition is a required flag"
        raise SystemExit, 1
    partition = sys.argv[sys.argv.index('-partition') + 1]
    brooklyn = Cobalt.Proxy.simulator()
    stat = brooklyn.ReservePartition(partition)
    if not stat:
        print "Failed to run process on partition"
        raise SystemExit, 1
    try:
        time.sleep(0.90 * float(sys.argv[-1]))
    except:
        pass
    brooklyn.ReleasePartition(partition)
    
