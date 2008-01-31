#!/usr/bin/env python

"""Process manager for Blue Gene/L systems"""

__revision__ = '$Revision$'

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
