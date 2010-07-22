#!/usr/bin/env python

__revision__ = '$Revision: $'

import sys

from Cobalt.Components.base_forker import BaseForker
from Cobalt.Components.base import run_component

if __name__ == "__main__":
    try:
        run_component(BaseForker, single_threaded=True)
    except KeyboardInterrupt:
        sys.exit(1)
