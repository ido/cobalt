#!/usr/bin/env python

from Cobalt.Components.gravina import BGSystem
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGSystem, state_name='gravina',
                      cls_kwargs={'config_file':'bgq_simulator.xml'})
    except KeyboardInterrupt:
        pass
