#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.system_script_forker import SystemScriptForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(SystemScriptForker, single_threaded=True, state_name="system_script_forker")
    except KeyboardInterrupt:
        sys.exit(1)
