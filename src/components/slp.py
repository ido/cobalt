#!/usr/bin/env python

__revision__ = '$Revision$'

from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.base import run_component

try:
    slp = TimingServiceLocator()
    run_component(slp, register=False)
except KeyboardInterrupt:
    pass
