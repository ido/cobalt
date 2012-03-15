#!/usr/bin/env python

from Cobalt.Components.bgqsystem import BGSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGSystem, state_name='bgqsystem')
    except KeyboardInterrupt:
        pass
