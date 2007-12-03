"""Cobalt Libraries"""

__revision__ = '$Revision$'

__all__ = ['bridge', 'bgl_rm_api', 'Components', 'Data',
           'Logging', 'Proxy', 'Util']

# global config file specification
# making this a tuple rather than a list makes it
# a value, rather than a mutable object, and prevents
# shared object-state ugliness
CONFIG_FILES = ("/etc/cobalt.conf", )
