#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.bg_runjob_forker import BGRunjobForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BGRunjobForker, single_threaded=True, state_name="bg_runjob_forker")
    except KeyboardInterrupt:
        sys.exit(1)
