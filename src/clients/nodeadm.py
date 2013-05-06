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
'-l','--list',action='store_true', dest='list', help='list node states'

"""
import logging
import math
import sys
import time
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = ''
__version__ = ''

def validate_args(parser):
    """
    Validate nodeadm arguments. 
    """
    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)

    if parser.no_args() and not parser.options.list:
        client_utils.logger.error("No arguments provided")
        parser.parser.print_help()
        sys.exit(1)
    
    if opt_count == 0:
        client_utils.logger.error("Need at least one option")
        parser.parser.print_help()
        sys.exit(1)

    impl = client_utils.get_implementation()

    # make sure we're on a cluster-system
    if "cluster_system" != impl:
        client_utils.logger.error("nodeadm is only supported on cluster systems.  Try partlist instead.")
        sys.exit(0)

    optc = 0
    errmsg = '' # init error msessage to empty string
    # Check mutually exclusive options
    if opt_count > 1:
        if parser.options.down != None: 
            errmsg += ' down'
            optc += 1
        if parser.options.up != None: 
            errmsg += ' up'
            optc += 1
        if parser.options.list != None: 
            errmsg += ' queue'
            optc += 1
        if parser.options.list != None: 
            errmsg += ' list'
            optc += 1

    if optc > 1:
        errmsg = 'Option combinations not allowed with: %s option(s)' % errmsg[1:].replace(' ',', ')
        client_utils.logger.error(errmsg)
        sys.exit(1)

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
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    whoami = client_utils.getuid()
    parser.parse_it() # parse the command line

    validate_args(parser)

    opt  = parser.options
    args = parser.args

    system = client_utils.client_data.system_manager(False)

    if opt.down:
        delta = system.nodes_down(args, whoami)
        client_utils.logger.info("nodes marked down:")
        for d in delta:
            client_utils.logger.info("   %s" % d)
        client_utils.logger.info("")
        client_utils.logger.info("unknown nodes:")
        for a in args:
            if a not in delta:
                client_utils.logger.info("   %s" % a)
    
    elif opt.up:
        delta = system.nodes_up(args, whoami)
        client_utils.logger.info("nodes marked up:")
        for d in delta:
            client_utils.logger.info("   %s" % d)
        client_utils.logger.info('')
        client_utils.logger.info("nodes that weren't in the down list:")
        for a in args:
            if a not in delta:
                client_utils.logger.info("   %s" %a)
    
    elif opt.list:
        status = system.get_node_status()
        queue_data = system.get_queue_assignments()

        header = [['Host', 'Queue', 'State']]
        #build output list
        output = []
        for t in status:
            host_name = t[0]
            status = t[1]
            queues = []
            for q in queue_data:
                if host_name in queue_data[q]:
                    queues.append(q) 
            output.append([host_name, ":".join(queues), status])
            
        client_utils.printTabular(header + output)

    elif opt.queue:
        data = system.set_queue_assignments(opt.queue, args, whoami)
        client_utils.logger.info(data)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
