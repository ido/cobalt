#!/usr/bin/env python
"""
Return a space delimited list of names that a user can boot within their job.
Block names are sent to standard output in a space delimited list.

Usage: %prog [options] <block location>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'--size',dest='query_size', type='int', help='Constrain blocks to a particular nodecount',callback=cb_gtzero
'--geometry',dest='geo_list', type='string', help='Constrain blocks to a particular geometry',callback=cb_bgq_geo

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_gtzero, cb_bgq_geo

from Cobalt.arg_parser import ArgParse

__revision__ = 'TBD'
__version__ = 'TBD'

SYSMGR = client_utils.SYSMGR

def main():
    """
    get-bootable-blocks main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args>
        [ cb_debug        , () ],
        [ cb_gtzero       , (True,) ], # return int
        [ cb_bgq_geo      , () ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)
    parser.parse_it() # parse the command line
    opts   = parser.options
    args   = parser.args

    if parser.no_args():
        client_utils.print_usage(parser)
        sys.exit(1)

    block_loc   = args[0]
    idle_blocks = client_utils.component_call(SYSMGR, False, 'get_idle_blocks', (block_loc, opts.query_size, opts.geo_list))
    client_utils.logger.info("\n".join(idle_blocks))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
