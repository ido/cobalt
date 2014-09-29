#!/usr/bin/env python
"""
Prompt cobalt to boot a block on behalf of a user.

Usage: %prog [options]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'--block', dest='block', type='string', help='Name of block to boot.'
'--reboot', action='store_true', dest='reboot', help='If the block is already booted, free the block and reboot.'
'--free', action='store_true', dest='free', help='Free the block, if booted.  May not be combined with reboot'
'--jobid', dest='jobid', type='int', help='Specify a cobalt jobid for this boot.',callback=cb_gtzero

"""
import logging
import sys
import os
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_gtzero

from Cobalt.arg_parser import ArgParse

from Cobalt.Util import init_cobalt_config

__revision__ = 'TBD'
__version__  = '$Version$'

AUTH_FAIL       = 2
BAD_OPTION_FAIL = 3
GENERAL_FAIL    = 1
SUCCESS         = 0

SYSMGR = client_utils.SYSMGR

def main():
    """
    get-bootable-blocks main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args>
        [ cb_debug        , () ],
        [ cb_gtzero       , (True,) ] ] # return int

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    user = client_utils.getuid()

    parser.parse_it() # parse the command line
    opts   = parser.options

    if not parser.no_args():
        client_utils.logger.info('No arguments needed')

    if opts.free and opts.reboot:
        client_utils.logger.error("ERROR: --free may not be specified with --reboot.")
        sys.exit(BAD_OPTION_FAIL)

    block = opts.block
    if block == None:
        try:
            block = os.environ['COBALT_PARTNAME']
        except KeyError:
            pass
        try:
            block = os.environ['COBALT_BLOCKNAME']
        except KeyError:
            pass
        if block == None:
            client_utils.logger.error("ERROR: block not specified as option or in environment.")
            sys.exit(BAD_OPTION_FAIL)

    jobid = opts.jobid
    if jobid == None:
        try:
            jobid = int(os.environ['COBALT_JOBID'])
        except KeyError:
            client_utils.logger.error("ERROR: Cobalt jobid not specified as option or in environment.")
            sys.exit(BAD_OPTION_FAIL)

    if opts.reboot or opts.free:
        #Start the free on the block
        #poke cobalt to kill all jobs on the resource as well.
        success = client_utils.component_call(SYSMGR, False, 'initiate_proxy_free', (block, user, jobid))
        client_utils.logger.info("Block free on %s initiated." % (block,))
        if not success:
            client_utils.logger.error("Free request for block %s failed authorization." % (block, ))
            sys.exit(AUTH_FAIL)
        while (True):
            #wait for free.  If the user still has jobs running, this won't complete.
            #the proxy free should take care of this, though.
            if client_utils.component_call(SYSMGR, False, 'get_block_bgsched_status', (block,)) == 'Free':
                client_utils.logger.info("Block %s successfully freed." % (block,))
                break

    if not opts.free:
        #This returns important error codes. Pass this back up through main.
        return client_utils.boot_block(block, user, jobid)

if __name__ == '__main__':
    try:
        retval = main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
    sys.exit(retval)
