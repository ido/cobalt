#!/usr/bin/env python

__revision__ = '$Revision: $'

from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.base import run_component

try:
    script_manager = ScriptManager()
    run_component(script_manager)
except KeyboardInterrupt:
    pass
