#!/usr/bin/env python

__revision__ = '$Revision$'

import sys

from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.base import run_component

def main ():
    slp = TimingServiceLocator()
    run_component(slp, register=False)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
