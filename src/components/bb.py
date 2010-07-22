#!/usr/bin/env python

from Cobalt.Components.bb import BBSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BBSystem, register=True)
    except KeyboardInterrupt:
        SystemExit(1)
