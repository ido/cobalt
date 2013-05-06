#!/usr/bin/env python
"""
Nodelist 

Usage: %prog
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS: None

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = 'TBD'
__version__ = 'TBD'

def main():
    """
    qmove main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # read the cobalt config files
    client_utils.read_config()

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

    if not parser.no_args():
        client_utils.logger.info("No arguments needed")
    
    impl = client_utils.get_implementation()

    # make sure we're on a cluster-system
    if "cluster_system" != impl:
        client_utils.logger.error("nodelist is only supported on cluster systems.  Try partlist instead.")
        sys.exit(0)

    system = client_utils.client_data.system_manager()

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

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
