#!/usr/bin/env python
# -*- coding: utf-8 -*-

__revision__ = '$Revision: $'

import sys
from Cobalt.Components.base import run_component
from Cobalt.Components.heckle_forker import HeckleForker

if __name__ == "__main__":
    try:
        run_component(HeckleForker, single_threaded=True)
    except KeyboardInterrupt:
        sys.exit(1)
