#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.alps_script_forker import ALPSScriptForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(ALPSScriptForker, single_threaded=True, state_name="alps_script_forker")
    except KeyboardInterrupt:
        sys.exit(1)
