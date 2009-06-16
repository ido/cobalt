"""Cobalt Libraries"""

__revision__ = '$Revision$'

__all__ = ['bridge', 'bgl_rm_api', 'Components', 'Data', 'Exceptions',
           'Logging', 'Proxy', 'Util']

import sys
import os

DEFAULT_CONFIG_FILES = ("/etc/cobalt.conf", )
DEFAULT_LOG_DIRECTORY = '/var/log/cobalt'

if '-C' in sys.argv:
    CONFIG_FILES = (sys.argv[sys.argv.index('-C') + 1], )
elif os.environ.has_key("COBALT_CONFIG_FILE"):
    CONFIG_FILES = (os.environ["COBALT_CONFIG_FILE"], )
else:
    CONFIG_FILES = DEFAULT_CONFIG_FILES
