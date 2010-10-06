#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(ScriptManager)
    except KeyboardInterrupt:
        sys.exit(1)
