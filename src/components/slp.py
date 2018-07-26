#!/usr/bin/env python

__revision__ = '$Revision: 1981 $'

import sys

from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        #FIXME: we cannot register slp because of a problem with _register located in the property register.
        run_component(TimingServiceLocator, register=False, time_out=10.0)
    except KeyboardInterrupt:
        sys.exit(1)
