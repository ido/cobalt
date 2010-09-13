#!/usr/bin/env python
# -*- coding: utf-8 -*-

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.heckle_sched import HeckleSched
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(HeckleSched, state_name='bgsched')
    except KeyboardInterrupt:
        sys.exit(1)
