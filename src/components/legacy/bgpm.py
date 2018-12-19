#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

"""Process manager for Blue Gene/L systems"""

__revision__ = '$Revision: 1100 $'

import sys

from Cobalt.Components.cpm import ProcessManager
from Cobalt.Components.base import run_component

def main ():
    cpm = ProcessManager()
    run_component(cpm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
