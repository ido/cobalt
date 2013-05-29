#!/usr/bin/env python
"""
Cobalt qselect command

Usage: %prog [options]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn non communication debugging',callback=cb_debug
'-v','--verbose',dest='verbose',help='not used',action='store_true'

Option with values:

'-h','--held',dest='state',type='string',help='Specify the state of the job'
'-n','--nodecount',dest='nodes',type='int',help='modify job node count for jobs in args',callback=cb_nodes
'-A','--project',dest='project',type='string',help='modify project name for jobs in args'
'-t','--time',dest='walltime',type='string',help='specify the runtime for the job - minutes or HH:MM:SS',callback=cb_time
'-q','--queue',dest='queue',type='string',help='select queue that the job resides'

The following optins are only valid on IBM BlueGene architecture platforms:

'--mode',dest='mode',type='string',help='specify the job mode (co/vn)'

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_nodes, cb_time

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 559 $' # TBC may go away.
__version__ = '$Version$'

QUEMGR = client_utils.QUEMGR

def main():
    """
    qselect main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    opts     = {} # old map
    opt2spec = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>           <cb args>
        [ cb_debug               , () ],
        [ cb_nodes               , (False,) ], # return string
        [ cb_time                , (False, False, False) ] ] # no delta time, return minutes, return string

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    # Set required default for the query:
    query = {'tag':'job','jobid':'*','nodes':'*','walltime':'*','mode':'*','project':'*','state':'*','queue':'*'}

    parser.parse_it() # parse the command line

    if not parser.no_args(): 
        client_utils.logger.error("qselect takes no arguments")
        sys.exit(1)

    client_utils.get_options(query,opts,opt2spec,parser)
    response  = client_utils.component_call(QUEMGR, False, 'get_jobs', ([query],))
    if not response:
        client_utils.logger.error("Failed to match any jobs")
    else:
        client_utils.logger.debug(response)
        client_utils.logger.info("   The following jobs matched your query:")
        for job in response:
            client_utils.logger.info("      %d" % job.get('jobid'))
        
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
