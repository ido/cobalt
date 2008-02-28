#!/usr/bin/env python

import sys

if __name__ == '__main__':
    sched = Cobalt.Proxy.ComponentProxy("scheduler")
    if "--stop" in sys.argv:
        sched.disable()
    elif "--start" in sys.argv:
        sched.enable()
