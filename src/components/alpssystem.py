#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
# $Id$

from Cobalt.Components.system.CraySystem import CraySystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(CraySystem, register=True, state_name="alpssystem")
    except KeyboardInterrupt:
        pass
