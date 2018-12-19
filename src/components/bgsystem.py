#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
# $Id$

import sys

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGSystem, register=True, state_name='bgsystem')
    except KeyboardInterrupt:
        sys.exit(1)
