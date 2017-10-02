#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.bg_runjob_forker import BGRunjobForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGRunjobForker, single_threaded=True, state_name="bg_runjob_forker")
    except KeyboardInterrupt:
        sys.exit(1)
