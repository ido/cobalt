#!/usr/bin/env python

__revision__ = '$Revision: $'

from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import run_component

try:
    scheduler = BGSched()
    run_component(scheduler)
except KeyboardInterrupt:
    pass
