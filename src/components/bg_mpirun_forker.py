#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.bg_mpirun_forker import BGMpirunForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGMpirunForker, single_threaded=True, state_name="bg_mpirun_forker")
    except KeyboardInterrupt:
        sys.exit(1)
