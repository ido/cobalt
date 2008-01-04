#!/usr/bin/env python
# $Id$

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component

try:
    system = BGSystem()
    run_component(system, register=True)
except KeyboardInterrupt:
    pass
