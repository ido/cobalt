'''BGQ IO Block representation

Track the hardware associated with the block as well as
what compute blocks are currently using this block.

This is a hashable object, suitable for use with sets

'''
import Cobalt.Data
import pybgsched
import logging
import Cobalt.Util

_logger = logging.getLogger()

class IOBlock(Cobalt.Data.Data):
    '''BlueGene/Q IO Block'''

    fields = Cobalt.Data.Data.fields + ['name', 'state', 'status', 'io_drawers', 'io_links', 'connected_compute_blocks',
            'autoreboot']

    def __init__(self, spec):
        '''
        Initialize the IO Block

        spec should include:
        name - the control-system name for the block
        io_drawers - list of relevant IODrawers involved in the IOBlock
        io_links - list of IOLinks used by this IO block
        status - Current control system status of the block
        state - Cobalt state of the block (default "idle")

        '''
        super(IOBlock, self).__init__(spec)
        spec = spec.copy()
        self.name = spec.pop('name', None)
        self.status = spec.pop('status', 'Free') #control system status
        self.state = spec.pop('state', 'idle')
        self.size = spec.pop('size', ) #size in nodes
        self.io_drawers = set(spec.pop('io_drawers', []))
        self.io_nodes = set(spec.pop('io_nodes', []))
        self.block_computes_for_reboot = False
        self.ions_in_soft_failure = False
        self.autoreboot = False
        self.current_kernel = Cobalt.Util.get_config_option('bgsystem', 'ion_default_kernel', 'default')
        self.current_kernel_options = Cobalt.Util.get_config_option('bgsystem', 'ion_default_kernel_options', ' ')

    io_drawer_list = property(lambda self: list(self.io_drawers))
    io_node_list = property(lambda self: list(self.io_nodes))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<IOBlock name=%s>" % self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_state_for_update(self, io_hardware, bridge_io_block):
        '''return one of the following state strings:
        idle -- all hardware reported as available, block in Free status
        allocated -- all hardware reported as available, block in non-Free status
        idle-degraded -- some hardware unavailable, but block can be used, block in Free status
        allocated-degraded -- some hardware unavailable, but block can be used, block in non-Free status
        offline -- all hardware for the block is reported as offline
        blocked -- The block has IONs that are in-use by another IO Block.  This block may or may not be controled by Cobalt.

        NOTE: this does not actually set the state, only fetches what it should be.  This does not side-effect the io block itself

        '''
        #the theory here is that we get a list of states, a list of blocks and then do a bulk update.
        error_string = ''
        bad_ion_found = False
        bad_io_drawer_found = False
        any_live_hardware = False
        hardware_in_use = False
        for io_drawer_name in self.io_drawers:
            cached_drawer = io_hardware.getIODrawer(io_drawer_name)
            if cached_drawer.getState() != pybgsched.Hardware.Available:
                error_string = 'degraded (%s): %s' % (cached_drawer.getStateString(), io_drawer_name)
                bad_io_drawer_found = True
            ions = pybgsched.SWIG_vector_to_list(cached_drawer.getIONodes())
            for ion in ions:
                if ion.getState() != pybgsched.Hardware.Available:
                    error_string = 'degraded (%s): %s' % (ion.getStateString(), ion.getLocation())
                    bad_ion_found = True
                elif not any_live_hardware:
                    any_live_hardware = True
                if (not hardware_in_use and ion.isInUse() and (ion.getIOBlockName() != self.name) and
                        (ion.getLocation() in self.io_nodes)):
                    hardware_in_use = True
                    error_string = 'blocked (%s)' % ion.getIOBlockName()

        block_free = (bridge_io_block.getStatus() == pybgsched.Block.Free)

        if not any_live_hardware:
            retstate = 'offline'
        elif block_free:
            retstate = 'idle'
        else:
            retstate = 'allocated'

        if (bad_ion_found or bad_io_drawer_found) and not hardware_in_use:
            retstate = "-".join([retstate, error_string])
        elif hardware_in_use:
            retstate = error_string

        return retstate

    def clear_to_reboot(self):
        '''Requires pybgsched to be up and working.  We need to get the current connected compute blocks.

        '''
        #connected_computes is really a C++ vector type of strings.  Access using the C++ methods.  --PMR
        connected_computes = pybgsched.IOBlock.getConnectedComputeBlocks(self.name)
        return connected_computes.size() == 0


    def update_bridge_status(self, io_hardware, bridge_io_block):
        '''update the status that is being reported by the bridge. This resets the cached control system state and also clears the
        reboot flag and notes if we have any ions in a software failure in this block.

        '''
        self.status = bridge_io_block.getStatusString()
        if (self.block_computes_for_reboot and
            bridge_io_block.getStatus != pybgsched.IOBlock.Initialized and
            bridge_io_block.getAction() != pybgsched.IOBlock.Free):
            self.block_computes_for_reboot = False
        #check io nodes and make sure that we shouldn't be about to reboot
        self.ions_in_soft_failure = False
        for ion in self.io_nodes:
            self.ions_in_soft_failure = io_hardware.getIONode(ion).getState() == pybgsched.Hardware.SoftwareFailure
            if self.ions_in_soft_failure:
                break

class IOBlockDict (Cobalt.Data.DataDict):
    """Default container for blocks.

    Keyed by block name.
    """

    item_cls = IOBlock
    key = "name"



