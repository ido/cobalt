#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

from Cobalt.Components.bb import BBSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BBSystem, register=True)
    except KeyboardInterrupt:
        SystemExit(1)
