#!/usr/bin/env python

from Cobalt.Components.cluster_simulator import Simulator
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(Simulator)
    except KeyboardInterrupt:
        pass
