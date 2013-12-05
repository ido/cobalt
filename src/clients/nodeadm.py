#!/usr/bin/env python
"""
nodeadm - Nodeadm is the administrative interface for cluster systems

Usage: %prog [-l] [--down part1 part2] [--up part1 part2]"
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'--down',dest='down',help='mark nodes as down',action='store_true'
'--up',dest='up',help='mark nodes as up (even if allocated)',action='store_true'
'--queue',action='store', dest='queue', help='set queue associations'
'-l','--list_nstates',action='store_true', dest='list_nstates', help='list the node states'

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug
import time
from Cobalt.arg_parser import ArgParse

__revision__ = ''
__version__ = ''

SYSMGR = client_utils.SYSMGR

def validate_args(parser):
    """
    Validate nodeadm arguments. 
    """
    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)

    if (parser.no_args() and not parser.options.list_nstates) or opt_count == 0:
        client_utils.print_usage(parser)
        sys.exit(1)

    impl = client_utils.component_call(SYSMGR, False, 'get_implementation', ())

    # make sure we're on a cluster-system
    if "cluster_system" != impl:
        client_utils.logger.error("nodeadm is only supported on cluster systems.  Try partlist instead.")
        sys.exit(0)

    # Check mutually exclusive options
    mutually_exclusive_option_lists = [['down', 'up', 'list_nstates', 'queue']]

    if opt_count > 1:
        client_utils.validate_conflicting_options(parser, mutually_exclusive_option_lists)

def main():
    """
    setres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args>
        [ cb_debug        , () ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    parser = ArgParse(opt_def, callbacks)

    whoami = client_utils.getuid()
    parser.parse_it() # parse the command line

    validate_args(parser)

    opt  = parser.options
    args = parser.args

    if opt.down:
        delta = client_utils.component_call(SYSMGR, False, 'nodes_down', (args, whoami))
        client_utils.logger.info("nodes marked down:")
        for d in delta:
            client_utils.logger.info("   %s" % d)
        client_utils.logger.info("")
        client_utils.logger.info("unknown nodes:")
        for a in args:
            if a not in delta:
                client_utils.logger.info("   %s" % a)

    elif opt.up:
        delta = client_utils.component_call(SYSMGR, False, 'nodes_up', (args, whoami))
        client_utils.logger.info("nodes marked up:")
        for d in delta:
            client_utils.logger.info("   %s" % d)
        client_utils.logger.info('')
        client_utils.logger.info("nodes that weren't in the down list:")
        for a in args:
            if a not in delta:
                client_utils.logger.info("   %s" %a)

    elif opt.list_nstates:
        header, output = client_utils.cluster_display_node_info()
        client_utils.printTabular(header + output)

    elif opt.queue:
        data = client_utils.component_call(SYSMGR, False, 'set_queue_assignments', (opt.queue, args, whoami))
        client_utils.logger.info(data)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
