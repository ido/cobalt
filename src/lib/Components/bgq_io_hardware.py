'''IBM BG/Q IO hardware cobalt representation definitions.

'''

class IODrawer(object):
    """Represnetation of a BGQ IODrawer

    """
    def __init__(self, name, state='Available'):
        self.id = name
        self.name = name
        self.state = state
        self.ionodes = []
        self.io_blocks = []
        self.used_by = '' #IOBlock using this

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<IODrawer id=%s/>" % self.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def update_io_drawer_state(self, updater_callback):
        '''Use callback function, that takes an IONode to set the current state.'''
        self.state = updater_callback(self)

class IONode(object):
    '''Cobalt representation of a BGQ IO Node

    '''
    def __init__(self, name, state='Available'):
        self.id = name
        self.name = name
        self.rebooting = False
        self.io_blocks = []
        self.state = state
        self.nodes_serviced = []
        self.used_by = '' #IOBlock currently using this hardware

    def __str__(self):
        return self.state

    def __repr__(self):
        return "<IONode id=%s/>" % self.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def add_serviced_node(self, compute_node_id):
        '''Add a node to the list of compute nodes serviced by this node.  This is max 2.

        '''
        if len(self.nodes_serviced == 2):
            raise ValueError("Already have two compute nodes associated with this ION")
        self.nodes_serviced.append(compute_node_id)

    def update_io_node_state(self, updater_callback):
        '''Use callback function, that takes an IONode to set the current state.'''
        self.state = updater_callback(self)

