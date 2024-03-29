#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""
Cobalt qmove command

Usage: %prog [options] <queue name> <jobid1> [... <jobidN>]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug
from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 559 $' # TBC may go away.
__version__ = '$Version$'

QUEMGR = client_utils.QUEMGR

def validate_args(parser,user):
    """
    Validate qmove arguments.
    """
    if len(parser.args) < 2:
        client_utils.print_usage(parser)
        sys.exit(1)

    # get jobids from the argument list
    jobids = client_utils.get_jobids(parser.args[1:])

    jobs = [{'tag':'job', 'user':user, 'jobid':jobid, 'project':'*', 'notify':'*',
        'walltime':'*', 'queue':'*', 'procs':'*', 'nodes':'*', 'attrs':'*'} for jobid in jobids]
    queue = parser.args[0]
    return queue, jobs

def main():
    """
    qmove main
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

    queue,jobs = validate_args(parser,user)
    filters    = client_utils.get_filters()
    jobdata    = client_utils.component_call(QUEMGR, False, 'get_jobs', (jobs,))

    response = []
    hold_msg = []
    # move jobs to queue
    for job in jobdata:
        orig_job = job.copy()
        # keep orig job's attrs.  If this gets reset (which the filter can do) this will cause the find for the set operation to
        # fail. '*' will grab any here.
        orig_job['attrs'] = '*'
        job.update({'queue':queue})
        client_utils.process_filters(filters, job)
        # FIXME: Need a better aggregate operation, this really should be one remote call.
        [j] = client_utils.component_call(QUEMGR, False, 'set_jobs', ([orig_job], job, user))
        response.append("moved job %s to queue '%s'" % (j.get('jobid'), j.get('queue')))
        for resp in [j]:
            if 'message' in resp and resp['message'] is not None:
                if 'jobid' in resp and resp['jobid'] is not None:
                    hold_msg.append("%s: %s" % (resp['jobid'], resp['message']))
    if not response:
        client_utils.logger.error("Failed to match any jobs or queues")
    else:
        for line in response:
            client_utils.logger.info(line)
        for msg in hold_msg:
            client_utils.logger.info(msg)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)

