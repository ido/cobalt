#!/usr/bin/env python

"""
Delete Cobalt Scheduler Reservation(s)

Usage: %prog [--version | --help | --debug] <reservation name>
version: "%prog " + __revision__ + , Cobalt  + __version__


OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug
from Cobalt.arg_parser import ArgParse

__revision__ = '$Id: releaseres.py 2146 2011-04-29 16:19:22Z richp $'
__version__ = '$Version$'

SCHMGR = client_utils.SCHMGR

def main():
    """
    releaseres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [(cb_debug, ())]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    parser.parse_it() # parse the command line
    args = parser.args

    if parser.no_args():
        client_utils.print_usage(parser)
        sys.exit(1)

    # Check if reservation exists
    spec = [{'name': arg,'partitions': '*'} for arg in args]
    result = client_utils.component_call(SCHMGR, False, 'get_reservations', (spec,))

    if len(result) and len(result) != len(args):
        client_utils.logger.error("Reservation subset matched")
    elif not result:
        client_utils.logger.error("No Reservations matched")
        sys.exit(1)

    result = client_utils.component_call(SCHMGR, False, 'release_reservations', (spec, client_utils.getuid()))
    for resinfo in result:
        partitions = resinfo['partitions'].split(':')
        client_utils.logger.info("Released reservation '%s' for partitions: %s", resinfo['name'], str(partitions))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
