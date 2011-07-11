#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.user_script_forker import UserScriptForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(UserScriptForker, single_threaded=True, state_name="user_script_forker")
    except KeyboardInterrupt:
        sys.exit(1)
