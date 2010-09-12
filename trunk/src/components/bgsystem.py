#!/usr/bin/env python -W ignore::DeprecationWarning
# $Id$

import sys

from Cobalt.Components.bgsystem import BGSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGSystem, register=True, state_name='bgsystem')
    except KeyboardInterrupt:
        sys.exit(1)
