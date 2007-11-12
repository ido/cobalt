#!/usr/bin/env python
# $Id$

from Cobalt.Components.bgsystem import System
from Cobalt.Components.base import run_component

try:
    system = System()
    run_component(system, register=True)
except KeyboardInterrupt:
    pass
