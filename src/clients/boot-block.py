#!/usr/bin/env python

'''Prompt cobalt to boot a block on behalf of a user.

    Options:
    --block - Block to boot.  User must be authorized for the block.
    --reboot - If the block is not already free, free the block, and reboot it

'''

__version__ = '$Version$'
helpmsg = '''Instruct Cobalt's system component to boot a block on your behalf.'''

import optparse
import sys
import os
import pwd

from Cobalt.Util import sleep as cobalt_sleep
from Cobalt.Proxy import ComponentProxy
import pybgsched #only use read commands from this.  For reboot tracking.

AUTH_FAIL = 2
BAD_OPTION_FAIL = 3
GENERAL_FAIL = 1
SUCCESS = 0

def main():

    retval = SUCCESS

    parser = optparse.OptionParser(usage=helpmsg, version=__version__)
    parser.add_option('--block', action='store', dest='block', type='string', help='Name of block to boot.')
    parser.add_option('--reboot', action='store_true', dest='reboot', help='If the block is already booted, free the block and reboot.')
    parser.add_option('--free', action='store_true', dest='free', help='Free the block, if booted.  May not be combined with reboot')
    parser.add_option('--jobid', action='store', dest='jobid', help='Specify a cobalt jobid for this boot.')

    opts, args = parser.parse_args()

    if opts.free and opts.reboot:
        print >> sys.stderr, "ERROR: --free may not be specified with --reboot."
        return BAD_OPTION_FAIL

    user = pwd.getpwuid(os.getuid())[0]

    block = None
    if opts.block == None:
        try:
            block = os.environ['COBALT_PARTNAME']
        except KeyError:
            pass
        try:
            block = os.environ['COBALT_BLOCKNAME']
        except KeyError:
            pass
        if block == None:
            print >> sys.stderr, "ERROR: block not specified as option or in environment."
            return BAD_OPTION_FAIL
    else:
        block = opts.block

    jobid = None
    if opts.jobid == None:
        try:
            jobid = os.environ['COBALT_JOBID']
        except KeyError:
            print >> sys.stderr, "ERROR: Cobalt jobid not specified as option or in environment."
            return BAD_OPTION_FAIL
    else:
        jobid = opts.jobid
    #make sure this is an expected type
    jobid = int(jobid)

    #we have block, we have jobid, we have user, try and boot.
    system = ComponentProxy('system', defer=False)

    if opts.reboot or opts.free:
        #Start the free on the block
        #poke cobalt to kill all jobs on the resource as well.
        success = system.initiate_proxy_free(block, user, jobid)
        print "Block free on %s initiated." % (block,)
        if not success:
            print >> sys.stderr, "Free request for block %s failed authorization." % (block, )
            return AUTH_FAIL
        while (True):
            #wait for free.  If the user still has jobs running, this won't complete.
            #the proxy free should take care of this, though.
            if system.get_block_bgsched_status(block) == 'Free':
                print "Block %s successfully freed." % (block,)
                break

    if not opts.free:
        success = system.initiate_proxy_boot(block, user, jobid)
        if not success:
            print >> sys.stderr, "Boot request for block %s failed authorization." % (block, )
            return AUTH_FAIL
        #give the system component a moment to initiate the boot
        cobalt_sleep(3)
        #wait for block to boot
        failed = False
        while True:
            boot_id, status, status_strings = system.get_boot_statuses_and_strings(block)
            if status_strings != [] and status_strings != None:
                print "\n".join(status_strings)
            if status in ['complete', 'failed']:
                system.reap_boot(block)
                if status == 'failed':
                    failed = True
                break
            cobalt_sleep(1)
        if failed:
            print "Boot for locaiton %s failed."% (block,)
        else:
            print "Boot for locaiton %s complete."% (block,)
    return retval

if __name__ == '__main__':
    exit_status = main()
    sys.exit(exit_status)
