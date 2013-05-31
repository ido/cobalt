#!/usr/bin/env python
"""
Cobalt qdel command

Usage: %prog [options] <jobid1> [ ... <jobidN>]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import time
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 345 $'
__version__ = '$Version$'

QUEMGR = client_utils.QUEMGR

def main():
    """
    qdel main
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

    user = client_utils.getuid()

    # Set required default values: None

    parser.parse_it() # parse the command line

    jobids = client_utils.validate_jobid_args(parser)
    jobs   = [{'tag':'job', 'user':user, 'jobid':jobid} for jobid in jobids]

    deleted_jobs = client_utils.component_call(QUEMGR, True, 'del_jobs', (jobs, False, user))
    time.sleep(1)
    if deleted_jobs:
        data = [('JobID','User')] + [(job.get('jobid'), job.get('user')) for job in deleted_jobs]
        client_utils.logger.info("      Deleted Jobs")
        client_utils.print_tabular(data)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)

