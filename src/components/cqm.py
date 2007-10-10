#!/usr/bin/env python

__revision__ = '$Revision$'

from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.base import run_component

try:
    cqm = QueueManager()
    run_component(cqm, register=True)
except KeyboardInterrupt:
    pass
