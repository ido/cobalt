"""Cobalt Libraries"""

__revision__ = '$Revision$'

__all__ = ['bridge', 'bgl_rm_api', 'Components', 'Data',
           'Logging', 'Proxy', 'Util']

import sys

DEFAULT_CONFIG_FILES = ("/etc/cobalt.conf", )

if '-C' in sys.argv:
    CONFIG_FILES = (sys.argv[sys.argv.index('-C') + 1], )
else:
    CONFIG_FILES = DEFAULT_CONFIG_FILES
