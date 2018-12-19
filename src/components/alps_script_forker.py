#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
'''Launcher for alps_script_forkers.  If we are running multiple on a node,
this will spawn the actual forkers as subprocesses.

'''
__revision__ = '$Revision: $'

import sys

from Cobalt.Components.alps_script_forker import ALPSScriptForker
from Cobalt.Components.base import run_component
#from Cobalt.Util import init_cobalt_config, get_config_option

if __name__ == "__main__":
    # state_name = 'alps_script_forker'
    # if '--name' in sys.argv:
    #     state_name = sys.argv[sys.argv.index('--name') + 1]
    seq_num = 0
    if '--seq' in sys.argv:
        seq_num = sys.argv[sys.argv.index('--seq') + 1]
        sys.argv.remove('--seq')
        sys.argv.remove(seq_num)
        seq_num = int(seq_num)
    try:
        run_component(ALPSScriptForker, single_threaded=True,
                aug_comp_name=True, state_name_match_component=True,
                seq_num=seq_num)
    except KeyboardInterrupt:
        sys.exit(1)
