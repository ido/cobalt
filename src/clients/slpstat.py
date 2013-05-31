#!/usr/bin/env python
"""
query the slp daemon for component location information

Usage: %prog [options] <queue name> <jobid1> [... <jobidN>]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import logging
import time
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 1221 $'
__version__ = '$Version$'

SLPMGR = client_utils.SLPMGR


def main():
    """
    slpstat main
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

    # Set required default values: None

    parser.parse_it() # parse the command line

    if not parser.no_args():
        client_utils.logger.error('No arguments needed')

    services = client_utils.component_call(SLPMGR, False, 'get_services', 
                                           ([{'tag':'service', 'name':'*', 'stamp':'*', 'location':'*'}],))

    if services:
        header = [('Name', 'Location', 'Update Time')]
        output = [ (service['name'],
                    service['location'],
                    time.strftime("%c", time.localtime(service['stamp'])))
                   for service in services ]
        client_utils.print_tabular(header + [tuple(item) for item in output])
    else:
        client_utils.logger.info("no services registered")

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)


