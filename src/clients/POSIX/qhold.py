#!/usr/bin/env python
"""
Cobalt qhold command

Usage: %prog [options] <jobid1> [ ... <jobidN> ]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import sys
from Cobalt import client_utils

__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

def main():
    """
    qhold main
    """
    client_utils.hold_release_command(__doc__,__revision__,__version__)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
