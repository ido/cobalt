#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.base import run_component

def main ():
    script_manager = ScriptManager()
    run_component(script_manager)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
