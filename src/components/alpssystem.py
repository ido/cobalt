#!/usr/bin/env python
# $Id$

from Cobalt.Components.system.CraySystem import CraySystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(CraySystem, register=True, state_name="alpssystem")
    except KeyboardInterrupt:
        pass
