#!/usr/bin/env python
"""
Change used reservation

Usage: %prog [--version | --help | --debug]  <reservation name(s)>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug
from Cobalt.arg_parser import ArgParse
import time
import math

__revision__ = '$Id: releaseres.py 1361 2008-08-08 16:22:14Z buettner $'
__version__ = '$Version$'

SCHMGR = client_utils.SCHMGR

def update_start_time(spec, user_name):
    """
    will update the start time for the clyclic reservation
    """
    start = spec['start']
    duration = spec['duration']
    cycle = float(spec['cycle'])
    now = time.time()
    periods = math.floor((now - start)/cycle)

    if(periods < 0):
        start += cycle
    elif(now - start) % cycle < duration:
        start += (periods + 1) * cycle
    else:
        start += (periods + 2) * cycle

    updates = {'start':start}

    client_utils.component_call(SCHMGR, False, 'set_reservations', ([{'name':spec['name']}], updates, user_name))
    newstart = time.strftime("%c", time.localtime(start))
    client_utils.logger.info("Setting new start time for for reservation '%s': %s", spec['name'], newstart)

def main():
    """
    userres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [( cb_debug, ())]

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
    spec = [{'name': rname, 'users':"*", 'start':'*', 'cycle':'*', 'duration':'*'} for rname in args]
    result = client_utils.component_call(SCHMGR, False, 'get_reservations', (spec,))

    if len(result) and len(result) != len(args):
        client_utils.logger.error("Reservation subset matched")
    elif not result:
        client_utils.logger.error("No Reservations matched")
        sys.exit(1)

    user_name = client_utils.getuid()
    
    for spec in result:
        if not spec['users'] or user_name not in spec['users'].split(":"):
            client_utils.logger.error("You are not a user of reservation '%s' and so cannot alter it.", spec['name'])
            continue

        if spec['cycle']:
            updates = update_start_time(spec, user_name)
        else:
            client_utils.component_call(SCHMGR, False, 'del_reservations', ([{'name':spec['name']}], user_name))
            client_utils.logger.info("Releasing reservation '%s'", spec['name'])

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)

