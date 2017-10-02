#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
# $Id$

import sys

from Cobalt.Components.cluster_system import ClusterSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(ClusterSystem, register=True, state_name="cluster_system")
    except KeyboardInterrupt:
        sys.exit(1)
