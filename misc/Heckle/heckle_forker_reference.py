#!/usr/bin/env python
# -*- coding: utf-8 -*-

__revision__ = '$Revision: $'

import sys
sys.path.append("/usr/lib/python2.6/site-packages")
print sys.path
from Cobalt.Components.base import run_component
from Cobalt.Components.heckle_forker import HeckleForker

if __name__ == "__main__":
    try:
        run_component(HeckleForker, single_threaded=True)
    except KeyboardInterrupt:
        sys.exit(1)
