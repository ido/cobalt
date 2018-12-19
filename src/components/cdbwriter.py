#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

__revision__ = '$Revision: 1 $'

import sys
from Cobalt.Components.DBWriter.cdbwriter import MessageQueue
from Cobalt.Components.base import run_component

if __name__ == "__main__":

    try:
        run_component(MessageQueue, register=True, state_name='cdbwriter')
    except KeyboardInterrupt:
        sys.exit(1)
