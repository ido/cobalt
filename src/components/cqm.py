#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

__revision__ = '$Revision: 1981 $'

import sys
from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.base import run_component

if __name__ == "__main__":

    try:
        run_component(QueueManager, register=True, state_name='cqm')
    except KeyboardInterrupt:
        sys.exit(1)
