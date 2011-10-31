#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Heckle Cobalt Interface component reference

...I don't really know what this does...


"""

from Cobalt.Components.heckle_system import HeckleSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(HeckleSystem, register=True)
    except KeyboardInterrupt:
        SystemExit(1)
