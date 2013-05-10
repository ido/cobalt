#!/usr/bin/env python

import sys

print >>sys.stderr, "This script is going to fail,\nbut that to be expected."
for a in sys.argv[1:]:
    print >>sys.stderr, a
sys.exit(13)
