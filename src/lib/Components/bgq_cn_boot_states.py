'''State classes for BGQ Compute node booting.

'''

import pybgsched
import logging
import time
from Cobalt.BaseTriremeState import BaseTriremeState

_logger = logging.getLogger()

def _initiate_boot(context):
    '''Initiate the boot. If problems are encountered, then return a BootFailed state, otherwise, return a BootInitiating state.

    '''
    _logger.info("initiating boot")
    try:
        pybgsched.Block.initiateBoot(context.subblock_parent)
    except RuntimeError:
        #fail the boot
        _logger.warning("%s/%s: Unable to boot block %s due to RuntimeError. Aborting job startup.", context.user, context.job_id,
                context.subblock_parent)
        context.status_string.append("%s/%s: Unable to boot block %s due to RuntimeError. Aborting job startup." % (context.user,
            context.job_id, context.subblock_parent))
        return BootFailed(context)
    except Exception:
        _logger.critical("%s/%s: Unexpected exception recieved during job boot on %s.  Aborting job startup.", context.user,
                context.job_id, context.subblock_parent)
        context.status_string.append("%s/%s: Unexpected exception recieved during job boot on %s.  Aborting job startup." % \
                (context.user, context.job_id, context.subblock_parent))
        return BootFailed(context)
    else:
        _logger.info("%s/%s: Initiating boot at location %s.", context.user, context.job_id, context.subblock_parent)
        context.status_string.append("%s/%s: Initiating boot at location %s." % (context.user,
            context.job_id, context.subblock_parent))
        return BootInitiating(context)

def get_compute_block(block, extended_info=False):
    '''We do this a lot, this is just to make the information call more readable.

    block -- a string containing the block name
    extended_info -- Default: False.  If set to true, pulls extended info for the
        block like hardware information.

    '''
    block_location_filter = pybgsched.BlockFilter()
    block_location_filter.setName(block)
    retloc = None
    if extended_info:
        block_location_filter.setExtendedInfo(True)
    try:
        retloc = pybgsched.getBlocks(block_location_filter)[0]
    except IndexError:
        _logger.critical("Booting Block %s not found in the control system!", block)
    return retloc

class BootPending(BaseTriremeState):
    '''A boot has been requested.  This state handles boot initiation.
    Errors contacting the control system at this point are considered fatal for the boot.
    Depending on when this occurs, it may also be fatal to the requesting job.

    '''
    _short_string = 'pending'

    def __init__(self, context):
        super(BootPending, self).__init__(context)
        self._destination_states = frozenset([BootPending, BootInitiating, BootComplete, BootFailed])

    def progress(self):
        #Make sure we have the lock for this resource, set user and start booting.
        label = "%s/%s" % (self.context.user, self.context.job_id)
        if self.context.under_resource_reservation():
            #we can continue the boot, we're not out of time.
            try:
                compute_block = get_compute_block(self.context.subblock_parent)
                pybgsched.Block.addUser(self.context.subblock_parent, self.context.user)
            except RuntimeError:
                #control system connection has blown.  This boot may as well be dead.
                self.context.status_string.append("%s: Unable to retrieve control system data for block %s. Aborting job." %\
                        (label, self.context.subblock_parent))
                return BootFailed(self.context)
            try:
                #Unlike BG/P where kernel options are passed in to mpirun we have to set them as a part of the block here.
                if self.context.block.current_kernel_options == '' or self.context.block.current_kernel_options is None:
                    #Workaround for not accepting null-strings.  Should be fixed by IBM later.
                    self.context.block.current_kernel_options = ' '
                if (self.context.block.current_kernel_options != compute_block.getBootOptions() and
                    self.context.block.current_kernel_options is not None):
                    #only write to the database if we have a change
                    if len(self.context.block.current_kernel_options) > 256: #control system size limit.
                        self.context.status_string.append("%s: ERROR: kernel options: [%s] longer than 256 characters",
                                label, self.context.block.current_kernel_options)
                        return BootFailed(self.context)
                    compute_block.setBootOptions(self.context.block.current_kernel_options)
                    compute_block.update()
            except RuntimeError:
                self.context.status_string("%s: Unable to set kernel options on block.  Aborting job.")
                return BootFailed(self.context)
            if self.context.block.block_type == 'pseudoblock':
                #we have to boot a subblock job. If already booted, this is complete.
                block_status = compute_block.getStatus()
                if block_status in [pybgsched.Block.Allocated, pybgsched.Block.Booting]:
                    #Boot in progress: move to initiating
                    return BootInitiating(self.context)
                elif block_status == pybgsched.Block.Initialized:
                    if compute_block.getAction() == pybgsched.Action._None:
                        compute_block.addUser(self.context.subblock_parent, self.context.user)
                        self.context.status_string.append("%s: Block %s for location %s already booted." \
                                "  Boot Complete from pending." % (label, self.context.subblock_parent, self.context.block_id))
                        return BootComplete(self.context)
                    else: #we're going to have to wait for this block to free and reboot the block.
                        _logger.info("%s: trying to start on freeing block %s. waiting until free.", label,
                            self.context.subblock_parent)
                        return self
            return _initiate_boot(self.context)
        else:
            self.context.status_string.append("%s: the internal reservation on %s expired; job has been terminated" % \
                    (label, self.context.subblock_parent))
            return BootFailed(self.context)
        raise RuntimeError, "Unable to return a valid state"

class BootInitiating(BaseTriremeState):
    '''Check to determine if our boot is still continuing or has completed.
    Problems contacting the control system at this point are considered fatal to the ongoing boot.

    '''
    _short_string = 'initiating'

    def __init__(self, context):
        super(BootInitiating, self).__init__(context)
        self._destination_states = frozenset([BootInitiating, BootComplete, BootFailed, BootRebooting])

    def progress(self):
        '''check up on groups that are waiting to start up.

        '''
        # Make sure we still have the reservation, otherise allow cleanup to clear the block
        if not self.context.under_resource_reservation():
            self.context.status_string.append("%s/%s: the internal reservation on %s expired; job has been terminated" % \
                    (self.context.user, self.context.job_id, self.context.subblock_parent))
            return BootFailed(self.context)

        boot_block = get_compute_block(self.context.subblock_parent)
        if boot_block is None:
            _logger.error('Unable to find block.  Failing boot!.')
            return BootFailed(self.context)
        block_status = boot_block.getStatus()
        if block_status == pybgsched.Block.Initialized:
            if boot_block.getAction() == pybgsched.Action.Free:
                _logger.warning("%s/%s: Block for pending boot on %s freeing. Attempting reboot.", self.context.user, self.context.job_id,
                    self.context.subblock_parent)
                return BootRebooting(self.context)
            else:
                self.context.status_string.append("%s/%s: Block %s for location %s successfully booted (Initiating). " % \
                    (self.context.user, self.context.job_id, self.context.subblock_parent, self.context.block.name))
                return BootComplete(self.context)
        elif block_status in [pybgsched.Block.Free, pybgsched.Block.Terminating]:
            #may have had an inopportune free, go ahead and make this and try and reboot.
            _logger.warning("%s/%s: Block for pending boot on %s freeing. Attempting reboot.", self.context.user, self.context.job_id,
                    self.context.subblock_parent)
            return BootRebooting(self.context)
        #allocated and booting states on the block means we stay in this state
        return self

class BootComplete(BaseTriremeState):

    _short_string = 'complete'

    def __init__(self, context):
        super(BootComplete, self).__init__(context)
        self._destination_states = frozenset([BootComplete])
        self.context.reap_timeout_end = None
        if self.context.reap_timeout is not None:
            self.context.reap_timeout_end = int(self.context.reap_timeout) + int(time.time())
        self.context.force_clean = False

    def progress(self):
        '''Boot has completed, wait until the boot is acknowledged and reaped.

        '''
        if self.context.reap_timeout is not None and int(time.time()) > self.context.reap_timeout_end:
            self.context.force_clean = True
        return self

class BootFailed(BaseTriremeState):
    _short_string = 'failed'

    def __init__(self, context):
        super(BootFailed, self).__init__(context)
        self._destination_states = frozenset([BootFailed])
        self.context.reap_timeout_end = None
        if self.context.reap_timeout is not None:
            self.context.reap_timeout_end = int(self.context.reap_timeout) + int(time.time())
        self.context.force_clean = False

    def progress(self):
        '''Boot has failed.  Messages have been logged.  Wait for reaping.

        '''
        if self.context.reap_timeout is not None and int(time.time()) > self.context.reap_timeout_end:
            self.context.force_clean = True
        return self

class BootRebooting(BaseTriremeState):
    _short_string = 'rebooting'

    def __init__(self, context):
        super(BootRebooting, self).__init__(context)
        self._destination_states = frozenset([BootRebooting, BootPending, BootInitiating, BootComplete, BootFailed])

    def progress(self):
        '''Block found in state that requires reboot.  Increment reboot counter, and check if we have already failed.

        '''
        #Do we still have the resource?
        if not self.context.under_resource_reservation():
            self.context.status_string.append("%s/%s: the internal reservation on %s expired; job has been terminated" % \
                    (self.context.user, self.context.job_id, self.context.subblock_parent))
            return BootFailed(self.context)
        #Check to see if we have any reboots left, if so, wait until free(?) Then go to pending.
        #If we find that our block is in a booting state already, then go along with the reboot in progress.
        if self.context.max_reboot_attempts != None and self.context.reboot_attempts >= self.context.max_reboot_attempts:
            self.context.status_string.append("%s/%s: Boot terminated on %s: too many reboot attempts." % (self.context.user,
                self.context.job_id, self.context.subblock_parent))
            return BootFailed(self.context)
        try:
            reboot_block = get_compute_block(self.context.subblock_parent)
        except Exception as e:
            _logger.critical("%s/%s: Unable to contact control system for block information.", self.context.user,
                    self.context.job_id, exc_info=True)
            return self
        block_status = reboot_block.getStatus()
        if block_status == pybgsched.Block.Free:
            self.context.status_string.append("%s/%s: Block %s free, retrying boot." % (self.context.user,
                self.context.job_id, self.context.subblock_parent))
            self.context.reboot_attempts += 1
            return BootPending(self.context)
        elif block_status in [pybgsched.Block.Allocated, pybgsched.Block.Booting]:
            #block has already started a reboot.  This can happen esaily with subblocks.
            self.context.status_string.append("%s/%s: Block %s now booting. Waiting for boot completion." % (self.context.user,
                self.context.job_id, self.context.subblock_parent))
            self.context.reboot_attempts += 1
            return BootInitiating(self.context)
        elif block_status == pybgsched.Block.Initialized and reboot_block.getAction() != pybgsched.Action.Free:
            #The block is apparently in a normal booted state, also shows up in subblock jobs.
            self.context.status_string.append("%s/%s: Block %s found booted.  Boot complete." % (self.context.user,
                self.context.job_id, self.context.subblock_parent))
            self.context.reboot_attempts += 1
            return BootComplete(self.context)
        return self

