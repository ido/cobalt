#!/usr/bin/env python

'''This script simulates the standard bridge mpirun for brooklyn'''

import sys, Cobalt.Proxy, time, math

if __name__ == '__main__':
    for flag in ['-partition', '-np', '-mode']:
        if flag not in sys.argv[1:]:
            print "ERROR: %s is a required flag" % (flag)
            raise SystemExit, 1
    partition = sys.argv[sys.argv.index('-partition') + 1]
    mode = sys.argv[sys.argv.index('-mode') + 1]
    size = sys.argv[sys.argv.index('-np') + 1]
    if mode == 'vn':
        size = int(math.ceil(float(size) / 2))
    brooklyn = Cobalt.Proxy.simulator()
    stat = brooklyn.ReservePartition(partition, size)
    if not stat:
        print "Failed to run process on partition"
        raise SystemExit, 1
    try:
        time.sleep(0.90 * float(sys.argv[-1]))
    except:
        pass
    brooklyn.ReleasePartition(partition)
    
