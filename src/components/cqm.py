#!/usr/bin/env python

__revision__ = '$Revision$'

import sys
from Cobalt.Components.cqm import QueueManager, cleanup_database_writer
from Cobalt.Components.base import run_component

if __name__ == "__main__":

    try:
        run_component(QueueManager, register=True, state_name='cqm')
        cleanup_database_writer()
    except KeyboardInterrupt:
        sys.exit(1)
