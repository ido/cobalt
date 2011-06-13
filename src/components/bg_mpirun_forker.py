#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.bg_mpirun_forker import BGMpirunForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGMpirunForker, single_threaded=True, state_name="bg_mpirun_forker")
    except KeyboardInterrupt:
        sys.exit(1)
