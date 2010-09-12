#!/usr/bin/env python -W ignore::DeprecationWarning

__revision__ = '$Revision$'

import sys

from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(TimingServiceLocator, register=False)
    except KeyboardInterrupt:
        sys.exit(1)
