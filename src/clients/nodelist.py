#!/usr/bin/env python
"""
Nodelist 

Usage: %prog
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS: None

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-b','--list_details',action='store_true', dest='list_details', help='list detalied information for specified nodes'
'--noheader',dest='noheader',action='store_true',help='disable display of header information'

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = 'TBD'
__version__ = 'TBD'

SYSMGR = client_utils.SYSMGR

def main():
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args>
        [ cb_debug        , () ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    # Set required default values: None

    parser.parse_it() # parse the command line
    opt = parser.options
    args = parser.args

    #if not parser.no_args():
    #    client_utils.logger.error("No arguments needed")

    impl = client_utils.component_call(SYSMGR, False, 'get_implementation', ())

    # make sure we're on a cluster-system
    if impl not in ['cluster_system', 'alps_system']:
        client_utils.logger.error("nodelist is only supported on cluster systems.  Try partlist instead.")
        sys.exit(0)

    if impl == 'alps_system':
        if opt.list_details:
            # get list from arguments.  Currently assuing a comma separated,
            # hyphen-condensed nodelist
            client_utils.print_node_details(args)
        else:
            client_utils.print_node_list()
        return



    header, output = client_utils.cluster_display_node_info()
    if parser.options.noheader is not None:
        client_utils.printTabular(header + output, with_header_info=False)
    else:
        client_utils.printTabular(header + output)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
