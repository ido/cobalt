#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import sys

print >>sys.stderr, "This script is going to fail,\nbut that to be expected."
for a in sys.argv[1:]:
    print >>sys.stderr, a
sys.exit(13)
