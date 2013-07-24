'''States for IO node booting on the BlueGene/Q

'''
import logging
import pybgsched
from Cobalt.BaseTriremeState import BaseTriremeState


_logger = logging.getLogger()


def _get_io_block(io_block, extended_info=False):
    '''We do this a lot, this is just to make the information call more readable.

    block -- a string containing the block name
    extended_info -- Default: False.  If set to true, pulls extended info for the
        block like hardware information.

    '''
    block_location_filter = pybgsched.IOBlockFilter()
    block_location_filter.setName(io_block)
    if extended_info:
        block_location_filter.setExtendedInfo(True)
    return pybgsched.getIOBlocks(block_location_filter)[0]


def _fetch_io_block(io_block_name):
    io_block = None
    try:
        io_block = _get_io_block(io_block_name)
    except RuntimeError:
        #Control system is out to lunch, this boot is failing.  Hard.
        _logger.critical("Unable to retrieve control system data for block %s.", io_block_name)
    return io_block


class IOBootPending(BaseTriremeState):
    '''A boot has been requested.  This state handles boot initiation.
    Errors contacting the control system at this point are considered fatal for the boot.
    Depending on when this occurs, it may also be fatal to the requesting job.

    '''
    _short_string = 'pending'

    def __init__(self, context):
        super(IOBootPending, self).__init__(context)
        self._destination_states = frozenset([IOBootPending, IOBootInitiating, IOBootFailed])

    def progress(self):
        label = "%s/%s" % (self.context.user, self.context.job_id)
        io_block = _fetch_io_block(self.context.io_block_name)
        if io_block == None:
            _logger.critical('Control system error duing boot intiation, failing boot for block %s', self.context.io_block_name)
            return IOBootFailed(self.context)

        block_status = io_block.getStatus()

        if block_status == pybgsched.IOBlock.Free and io_block.getAction() == pybgsched.Action._None:
            try:
                # Initialize the ion_kernel options in the control system
                if self.context.ion_kerneloptions == '' or self.context.ion_kerneloptions is None:
                    #Workaround for not accepting null-strings.  Should be fixed by IBM later.
                    self.context.ion_kerneloptions = ' '
                if (self.context.ion_kerneloptions != io_block.getBootOptions() and
                    self.context.ion_kerneloptions is not None):
                    #only write to the database if we have a change
                    if len(self.context.ion_kerneloptions) > 256: #control system size limit.
                        self.context.status_string.append("%s: ERROR: kernel options: [%s] longer than 256 characters",
                                label, self.context.ion_kerneloptions)
                        return IOBootFailed(self.context)
                    io_block.setBootOptions(self.context.ion_kerneloptions)
                    io_block.update()
            except RuntimeError:
                #if we don't have enough access to the control system to do this, this boot is going to completely fail now.
                self.context.status_string("%s: Unable to set kernel options on block.  Aborting job.")
                return IOBootFailed(self.context)
            # Unlike compute blocks, we can and do boot IO Blocks with non-functional hardware.  If we see any, log that there is
            # down hardware at boot-time.
            unavailable_resources = pybgsched.StringVector() #here for interface purposes, but subsumed by unavailableIONodes
            unavailable_io_nodes = pybgsched.StringVector()
            try:
                pybgsched.IOBlock.initiateBoot(self.context.io_block_name, True, unavailable_resources, unavailable_io_nodes)
                _logger.info("IOBlock %s: Boot initiated.", self.context.io_block_name)
            except RuntimeError:
                _logger.info("Error encountered while booting IOBlock %s. Boot failing.", self.context.io_block_name)
                return IOBootFailed(self.context)
            except Exception:
                _logger.critical("%s: Unexpected exception recieved during ION boot block %s.  Aborting job startup.",
                        label, self.context.io_block_name, exc_info=True)
                return IOBootFailed(self.context)
            if unavailable_io_nodes.size() != 0:
                _logger.warning("IOBlock %s: Some nodes not available on booted block: %s", self.context.io_block_name,
                        " ".join([ion for ion in unavailable_io_nodes]))
            return IOBootInitiating(self.context)
        else:
            #we can only boot a free block.  Otherwise this is an error
            #Unless this is a kernel reboot, wait for the block to transition to the free state instead.
            if not self.context.pending_kernel_reboot:
                _logger.error("Attempted to boot IOBlock %s in non-free status or pending action.  Boot Failed." % \
                        (self.context.io_block_name ))
                return IOBootFailed(self.context)
        return self

class IOBootInitiating(BaseTriremeState):
    '''Track a boot that has been initiated and progress to completed or failed as appropriate.

    '''
    _short_string = 'initiating'

    def __init__(self, context):
        super(IOBootInitiating, self).__init__(context)
        self._destination_states = frozenset([IOBootInitiating, IOBootComplete, IOBootFailed])
        return

    def progress(self):
        io_block = _fetch_io_block(self.context.io_block_name)
        if io_block == None:
            #I'm not entirely sure that failure is the right thing to do in this case, but it is a safe option. Is it better to just
            #stay in initiating? --PMR
            _logger.critical('Control system error duing boot intiation, failing boot for block %s', self.context.io_block_name)
            return IOBootFailed(self.context)

        block_status = io_block.getStatus()
        if block_status == pybgsched.IOBlock.Initialized and io_block.getAction() == pybgsched.Action._None:
            _logger.info('IOBlock %s: Block booting complete', self.context.io_block_name)
            return IOBootComplete(self.context)
        elif (block_status in [pybgsched.IOBlock.Allocated, pybgsched.IOBlock.Booting] or
                (block_status == pybgsched.IOBlock.Free and io_block.getAction() == pybgsched.Action.Boot)):
            return self
        else:
            #The boot is terminating or the block has already been freed.  Both would be the result of a failed boot.
            _logger.error('IOBlock %s: Block booting failed.', self.context.io_block_name)
            return IOBootFailed(self.context)

class IOBootComplete(BaseTriremeState):
    '''Note that a boot has completed and is eligible for reaping by the booter.  This state must be acknowledged prior to the boot
    instance being reaped and cleaned up.

    '''
    _short_string = 'complete'

    def __init__(self, context):
        super(IOBootComplete, self).__init__(context)
        self._destination_states = frozenset([IOBootComplete])
        return

    def progress(self):
        return self

class IOBootFailed(BaseTriremeState):
    '''Terminal state to indicate that a boot has failed.  This boot should be reaped after dumping error messages.

    '''
    _short_string = 'failed'

    def __init__(self, context):
        super(IOBootFailed, self).__init__(context)
        self._destination_states = frozenset([IOBootFailed])
        return

    def progress(self):
        return self
