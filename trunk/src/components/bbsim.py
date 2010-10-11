#!/usr/bin/env python

from Cobalt.Components.bbsim import BBSimulator
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BBSimulator, register=True)
    except KeyboardInterrupt:
        SystemExit(1)
