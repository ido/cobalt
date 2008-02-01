"""Cobalt Libraries"""

__revision__ = '$Revision$'

__all__ = ['bridge', 'bgl_rm_api', 'Components', 'Data',
           'Logging', 'Proxy', 'Util']

import sys

# global config file specification
# making this a tuple rather than a list makes it
# a value, rather than a mutable object, and prevents
# shared object-state ugliness
if '-C' in sys.argv:
    CONFIG_FILES = (sys.argv[sys.argv.index('-C') + 1], )
else:
    CONFIG_FILES = ("/etc/cobalt.conf", )
