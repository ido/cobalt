#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
# -*- coding: utf-8 -*-

__revision__ = '$Revision: $'

import sys
from Cobalt.Components.base import run_component
from Cobalt.Components.heckle_forker import HeckleForker

if __name__ == "__main__":
    try:
        run_component(HeckleForker, single_threaded=True)
    except KeyboardInterrupt:
        sys.exit(1)
