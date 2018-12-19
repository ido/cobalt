#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

from Cobalt.Components.cluster_simulator import Simulator
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(Simulator, state_name="cluster_simulator")
    except KeyboardInterrupt:
        pass
