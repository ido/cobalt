#!/usr/bin/env python

"""Process manager for Blue Gene/L systems"""

__revision__ = '$Revision$'

from Cobalt.Components.cpm import ProcessManager
from Cobalt.Components.base import run_component

try:
    cpm = ProcessManager()
    run_component(cpm)
except KeyboardInterrupt:
    pass
