#!/usr/bin/env python -W ignore::DeprecationWarning

__revision__ = '$Revision: 1 $'

import sys
from Cobalt.Components.DBWriter.cdbwriter import MessageQueue
from Cobalt.Components.base import run_component

if __name__ == "__main__":

    try:
        run_component(MessageQueue, register=True, state_name='cdbwriter')
    except KeyboardInterrupt:
        sys.exit(1)
