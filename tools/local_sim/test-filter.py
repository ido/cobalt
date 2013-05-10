#!/usr/bin/env python

import sys

print >>sys.stderr, sys.argv[0], "running"
for a in sys.argv:
    print >>sys.stderr, a

sys.exit(1)
