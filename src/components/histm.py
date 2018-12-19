#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import sys
from Cobalt.Components.histm import HistoryManager
from Cobalt.Components.base import run_component

__helpmsg__ = "Usage: histm [-j <jobinfo_file> -d <last_days> -d <least_item> -i <update_interval (in sec)>]"

if __name__ == "__main__":
    
    options = {}
    doptions = {'j':'jobinfo_file', 'd':'last_days', 'n':'least_item',
                'i':'update_interval'}
    
    try:
        run_component(HistoryManager, register=True, state_name='histm')
    except KeyboardInterrupt:
        sys.exit(1)
