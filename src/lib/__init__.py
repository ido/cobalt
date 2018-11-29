# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""Cobalt Libraries"""

__revision__ = '$Revision: 1622 $'

__all__ = ['bridge', 'bgl_rm_api', 'Components', 'Data', 'DataTypes',
           'Exceptions', 'Logging', 'Proxy', 'QueueThread', 'Util']

import sys
import os

DEFAULT_CONFIG_FILES = ("/etc/cobalt.conf", )
DEFAULT_LOG_DIRECTORY = '/var/log/cobalt'

if '--config-files' in sys.argv:
    CONFIG_FILES = []
    try:
        while True:
            loc = sys.argv.index('--config-files')
            sys.argv.pop(loc)
            CONFIG_FILES.extend(sys.argv.pop(loc).split(":"))
            del loc
    except ValueError:
        pass
    CONFIG_FILES = tuple(CONFIG_FILES)
elif os.environ.has_key("COBALT_CONFIG_FILES"):
    CONFIG_FILES = tuple(os.environ["COBALT_CONFIG_FILES"].split(":"))
else:
    CONFIG_FILES = DEFAULT_CONFIG_FILES
