#!/usr/bin/env python

import sys
import socket

from Cobalt.Proxy import *
from Cobalt.Exceptions import ComponentLookupError

state_markers = dict(
    idle = ("*", " ", " "),
    busy = (" ", "*", " "),
    blocked = (" ", " ", "*"),
)

def run ():
    system = ComponentProxy("system")
    specs = system.get_partitions([{'name':"*", 'state':"*"}])
    format = "%14s | %4s | %4s | %7s"
    print format % ("partition", "idle", "busy", "blocked")
    print "=" * 39
    for spec in specs:
        line = (spec['name'], ) + state_markers[spec['state']]
        print format % line


if __name__ == "__main__":
    try:
        run()
    except ComponentLookupError:
        print >> sys.stderr, "unable to locate the system"
        sys.exit(1)
    except socket.error:
        print >> sys.stderr, "problem communicating wiht the system"
        sys.exit(1)
