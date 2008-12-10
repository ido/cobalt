#!/usr/bin/env python
# $Id$

import sys

from Cobalt.Components.cluster_system import ClusterSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(ClusterSystem, register=True, cls_kwargs={'config_file':'cobalt.hostfile'})
    except KeyboardInterrupt:
        sys.exit(1)
