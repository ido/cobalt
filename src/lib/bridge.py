from ctypes import CDLL, cast, byref, c_void_p, c_int, c_char_p, POINTER, pointer, Structure

__all__ = [
    "set_serial", "get_serial",
    "BlueGene", "BasePartition", "NodeCard", "NodeCardList", "Switch",
    "Wire", "Port", "PartitionList", "Partition", "JobList", "Job",
]

try:
    bridge = CDLL("libbglbridge.so")
    systype = 'bgl'
except OSError:
    bridge = CDLL("libbgpbridge.so")
    systype = 'bgp'
libc = CDLL("libc.so.6")

status_t = c_int

def free_value (cdata):
    value = cdata.value
    libc.free(cdata)
    return value

def check_status (status, **kwargs):
    if status == 0:
        return status
    
    exceptions = kwargs.get("exceptions")
    if exceptions is None:
        exceptions = (
            PartitionNotFound, JobNotFound, BasePartitionNotFound,
            SwitchNotFound, JobAlreadyDefined, ConnectionError,
            InternalError, InvalidInput, IncompatibleState,
            InconsistentData
        )
    default = kwargs.get("default")
    if default is None:
        default = BridgeException
    
    for exception in exceptions:
        if status == exception.status:
            raise exception()
    raise BridgeException("encountered unexpected status: %i" % status)

rm_element_t = c_void_p
rm_component_id_t = c_char_p

bridge.rm_get_data.argtypes = [rm_element_t, c_int, c_void_p]
bridge.rm_get_data.restype = check_status


class BridgeException (Exception):
    
    """An exception caused by the c bridge library."""

class PartitionNotFound (BridgeException):
    
    status = -1


class JobNotFound (BridgeException):
    
    status = -2


class BasePartitionNotFound (BridgeException):
    
    status = -3


class SwitchNotFound (BridgeException):
    
    status = -4


class JobAlreadyDefined (BridgeException):
    
    status = -5


class ConnectionError (BridgeException):
    
    status = -10


class InternalError (BridgeException):
    
    status = -11


class InvalidInput (BridgeException):
    
    status = -12


class IncompatibleState (BridgeException):
    
    status = -13


class InconsistentData (BridgeException):
    
    status = -14


class Resource (object):
    
    def __init__ (self, element_pointer, **kwargs):
        self._as_parameter_ = element_pointer
        self._free = kwargs.get("free")
    
    def _get_data (self, field, ctype):
        data = ctype()
        bridge.rm_get_data(self, field, byref(data))
        return data


class ElementGenerator (object):
    
    def __init__ (self, container, cls, numfield, firstfield, nextfield):
        self._container = container
        self._cls = cls
        self._numfield = numfield
        self._firstfield = firstfield
        self._nextfield = nextfield
            
    def __len__ (self):
        return self._container._get_data(self._numfield, c_int).value

    def __iter__ (self):
        for x in xrange(len(self)):
            if x == 0:
                yield self._cls(self._container._get_data(self._firstfield, self._cls._ctype))
            else:
                yield self._cls(self._container._get_data(self._nextfield, self._cls._ctype))

    def __getitem__ (self, index):
        return list(self)[index]

rm_serial_t = rm_component_id_t
bridge.rm_set_serial.argtypes = [rm_serial_t]
bridge.rm_set_serial.restype = check_status

def set_serial (serial):
    bridge.rm_set_serial(rm_serial_t(serial))

bridge.rm_get_serial.argtypes = []
bridge.rm_get_serial.restype = check_status

def get_serial ():
    serial = rm_serial_t()
    bridge.rm_get_serial(byref(serial))
    return serial.value


##
# Blue Gene system

class rm_BGL_t (Structure):
    _fields_ = []

class rm_size3D_t (Structure):
    _fields_ = [('X', c_int), ('Y', c_int), ('Z', c_int)]

bridge.rm_get_BGL.argtypes = [POINTER(POINTER(rm_BGL_t))]
bridge.rm_get_BGL.restype = check_status

bridge.rm_free_BGL.argtypes = [POINTER(rm_BGL_t)]
bridge.rm_free_BGL.restype = check_status

if systype == 'bgl':
    RM_BPsize = 0
    RM_Msize = 1
    RM_BPNum = 2
    RM_FirstBP = 3
    RM_NextBP = 4
    RM_SwitchNum = 5
    RM_FirstSwitch = 6
    RM_NextSwitch = 7
    RM_WireNum = 8
    RM_FirstWire = 9
    RM_NextWire = 10
elif systype == 'bgp':
    RM_BPsize = 1000
    RM_Msize = 1001
    RM_BPNum = 1002
    RM_FirstBP = 1003
    RM_NextBP = 1004
    RM_SwitchNum = 1005
    RM_FirstSwitch = 1006
    RM_NextSwitch = 1007
    RM_WireNum = 1008
    RM_FirstWire = 1009
    RM_NextWire = 1010

def to_size_tuple (c_data):
    return (c_data.X, c_data.Y, c_data.Z)

class BlueGene (Resource):
    
    """The Blue Gene object represents the Blue Gene system.
    
    This object can be used to retrieve information and status for other
    components in the system, such as base partitions, node cards, I/O nodes,
    switches, wires, and ports.
    
    example:
    >>> set_serial("BGL") # informs the bridge of which machine to reference
    >>> bgl = BlueGene.by_serial() # get the machine
    
    properties:
    base_partitions -- generates BasePartition objects from the machine
    switches -- generates Switch objects from the machine
    wires -- generates Wire objects from the machine
    base_partition_size -- 3D size as a tuple (X, Y, Z)
    machine_size -- 3D size as a tuple (X, Y, Z)
    """
    
    _ctype = POINTER(rm_BGL_t)
    
    @classmethod
    def by_serial (cls):
        """Retrieve a BlueGene object based on the global serial id."""
        element_pointer = cls._ctype()
        bridge.rm_get_BGL(byref(element_pointer))
        return cls(element_pointer, free=True)
    
    def __init__ (self, element_pointer, **kwargs):
        """Create a BlueGene object based on existing memory.
        
        arguments:
        element_pointer -- memory address for machine in bridge
        """
        Resource.__init__(self, element_pointer, **kwargs)
        self.base_partitions = ElementGenerator(self, BasePartition, RM_BPNum, RM_FirstBP, RM_NextBP)
        self.switches = ElementGenerator(self, Switch, RM_SwitchNum, RM_FirstSwitch, RM_NextSwitch)
        self.wires = ElementGenerator(self, Wire, RM_WireNum, RM_FirstWire, RM_NextWire)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_BGL(self)
    
    def _get_base_partition_size (self):
        size = self._get_data(RM_BPsize, rm_size3D_t)
        return to_size_tuple(size)
    
    base_partition_size = property(_get_base_partition_size,
        doc="The size of a base partition (in c-nodes) in each dimension.")
    
    def _get_machine_size (self):
        size = self._get_data(RM_Msize, rm_size3D_t)
        return to_size_tuple(size)
    
    machine_size = property(_get_machine_size,
        doc="The size of the machine in base partition units.")


##
# Partition

class rm_partition_t (Structure):
    _fields_ = []

pm_partition_id_t = c_char_p
rm_partition_state_t = c_int
rm_partition_state_values = ("RM_PARTITION_FREE", "RM_PARTITION_CONFIGURING", "RM_PARTITION_READY", "RM_PARTITION_BUSY", "RM_PARTITION_DEALLOCATING", "RM_PARTITION_ERROR", "RM_PARTITION_NAV")
rm_connection_type_t = c_int
rm_connection_type_values = ("RM_MESH", "RM_TORUS", "RM_NAV")
rm_partition_mode_t = c_int
rm_partition_mode_values = ("RM_PARTITION_COPROCESSOR_MODE", "RM_PARTITION_VIRTUAL_NODE_MODE")

bridge.rm_get_partition.argtypes = [pm_partition_id_t, POINTER(POINTER(rm_partition_t))]
bridge.rm_get_partition.restype = check_status

bridge.rm_free_partition.argtypes = [POINTER(rm_partition_t)]
bridge.rm_free_partition.restype = check_status

if systype == 'bgl':
    RM_PartitionID = 39
    RM_PartitionState = 40
    RM_PartitionConnection = 41
    RM_PartitionUserName = 42
    RM_PartitionBPNum = 43
    RM_PartitionFirstBP = 44
    RM_PartitionNextBP = 45
    RM_PartitionSwitchNum = 46
    RM_PartitionFirstSwitch = 47
    RM_PartitionNextSwitch = 48
    RM_PartitionMloaderImg = 49
    RM_PartitionBlrtsImg = 50
    RM_PartitionLinuxImg = 51
    RM_PartitionRamdiskImg = 52
    RM_PartitionOptions = 53
    RM_PartitionMode = 54
    RM_PartitionDescription = 55
    RM_PartitionSmall = 56
    RM_PartitionNodeCardNum = 57
    RM_PartitionFirstNodeCard = 58
    RM_PartitionNextNodeCard = 59
    RM_PartitionPsetsPerBP = 60
    RM_PartitionUsersNum = 61
    RM_PartitionFirstUser = 62
    RM_PartitionNextUser = 63
elif systype == 'bgp':
    RM_PartitionID = 10000
    RM_PartitionState = 10001
    RM_PartitionConnection = 10003
    RM_PartitionUserName = 10008
    RM_PartitionBPNum = 10013
    RM_PartitionFirstBP = 10014
    RM_PartitionNextBP = 10015
    RM_PartitionSwitchNum = 10016
    RM_PartitionFirstSwitch = 10017
    RM_PartitionNextSwitch = 10018
    RM_PartitionMloaderImg = 10010
    RM_PartitionOptions = 10009
    RM_PartitionDescription = 10004
    RM_PartitionSmall = 10005
    RM_PartitionNodeCardNum = 10019
    RM_PartitionFirstNodeCard = 10020
    RM_PartitionNextNodeCard = 10021
    RM_PartitionPsetsPerBP = 10006
    RM_PartitionUsersNum = 10022
    RM_PartitionFirstUser = 10017
    RM_PartitionNextUser = 10018

class Partition (Resource):
    
    _ctype = POINTER(rm_partition_t)
    
    @classmethod
    def by_id (cls, id):
        element_pointer = cls._ctype()
        bridge.rm_get_partition(pm_partition_id_t(id), byref(element_pointer))
        return cls(element_pointer, free=True)
    
    def __init__ (self, element_pointer, **kwargs):
        Resource.__init__(self, element_pointer, **kwargs)
        self.base_partitions = ElementGenerator(self, BasePartition, RM_PartitionBPNum, RM_PartitionFirstBP, RM_PartitionNextBP)
        self.switches = ElementGenerator(self, Switch, RM_PartitionSwitchNum, RM_PartitionFirstSwitch, RM_PartitionNextSwitch)
        
        self._node_cards = ElementGenerator(self, NodeCard, RM_PartitionNodeCardNum, RM_PartitionFirstNodeCard, RM_PartitionNextNodeCard)
        # self.users = ElementGenerator(self, PartitionUsers, RM_PartitionUsersNum, RM_PartitionFirstUser, RM_PartitionNextUser)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_partition(self)
    
    def _get_node_cards (self):
        if self.small:
            return self._node_cards
        else:
            return self._get_base_partition_node_cards()
    
    node_cards = property(_get_node_cards)
    
    def _get_base_partition_node_cards (self):
        for base_partition in self.base_partitions:
            for node_card in NodeCardList.by_base_partition(base_partition):
                yield node_card
    
    def _get_id (self):
        id = self._get_data(RM_PartitionID, pm_partition_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_data(RM_PartitionState, rm_partition_state_t)
        return rm_partition_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_connection (self):
        connection_type = self._get_data(RM_PartitionConnection, rm_connection_type_t)
        return rm_connection_type_values[connection_type.value]
    
    connection = property(_get_connection)
    
    def _get_user_name (self):
        name = self._get_data(RM_PartitionUserName, c_char_p)
        return free_value(name)
    
    user_name = property(_get_user_name)
    
    def _get_machine_loader_image (self):
        image = self._get_data(RM_PartitionMloaderImg, c_char_p)
        return free_value(image)
    
    machine_loader_image = property(_get_machine_loader_image)
    
    def _get_compute_node_kernel_image (self):
        image = self._get_data(RM_PartitionBlrtsImg, c_char_p)
        return free_value(image)

    if systype == 'bgl':
        compute_node_kernel_image = property(_get_compute_node_kernel_image)
    
    def _get_io_node_kernel_image (self):
        image = self._get_data(RM_PartitionLinuxImg, c_char_p)
        return image.value

    if systype == 'bgl':
        io_node_kernel_image = property(_get_io_node_kernel_image)
    
    def _get_ramdisk_image (self):
        image = self._get_data(RM_PartitionRamdiskImg, c_char_p)
        return free_value(image)

    if systype == 'bgl':
        ramdisk_image = property(_get_ramdisk_image)
    
    def _get_description (self):
        description = self._get_data(RM_PartitionDescription, c_char_p)
        return free_value(description)
    
    description = property(_get_description)
    
    def _get_small (self):
        small = self._get_data(RM_PartitionSmall, c_int)
        return small.value != 0
    
    small = property(_get_small)
    
    def _get_psets_per_base_partition (self):
        psets = self._get_data(RM_PartitionPsetsPerBP, c_int)
        return psets.value
    
    psets_per_base_partition = property(_get_psets_per_base_partition)
    
    def _get_options (self):
        options = self._get_data(RM_PartitionOptions, c_char_p)
        return options.value
    
    options = property(_get_options)
    
    def _get_mode (self):
        mode = self._get_data(RM_PartitionMode, rm_partition_mode_t)
        return rm_partition_mode_values[mode.value]

    if systype == 'bgl':
        mode = property(_get_mode)


##
# Base Partition

class rm_BP_t (Structure):
    _fields_ = []

rm_bp_id_t = rm_component_id_t
rm_BP_state_t = c_int
rm_BP_state_values = ("RM_BP_UP", "RM_BP_DOWN", "RM_BP_MISSING", "RM_BP_ERROR", "RM_BP_NAV")
rm_BP_computenode_memory_t = c_int
rm_BP_computenode_memory_values = ("RM_BP_COMPUTENODE_MEMORY_256M", "RM_BP_COMPUTENODE_MEMORY_512M", "RM_BP_COMPUTENODE_MEMORY_1G", "RM_BP_COMPUTENODE_MEMORY_2G", "RM_BP_COMPUTENODE_MEMORY_4G", "RM_BP_COMPUTENODE_MEMORY_NAV")

class rm_location_t (Structure):
    _fields_ = [('X', c_int), ('Y', c_int), ('Z', c_int)]

if systype == 'bgl':
    RM_BPID = 11
    RM_BPState = 12
    RM_BPLoc = 13
    RM_BPPartID = 14
    RM_BPPartState = 15
    RM_BPSDB = 16
    RM_BPSD = 17
    # Revision 2
    RM_BPComputeNodeMemory = 93
elif systype == 'bgp':
    RM_BPID = 2000
    RM_BPState = 2001
    RM_BPLoc = 2003
    RM_BPPartID = 2004
    RM_BPPartState = 2005
    RM_BPSDB = 2007
    RM_BPSD = 2008
    RM_BPComputeNodeMemory = 2009
    
bridge.rm_free_BP.argtypes = [POINTER(rm_BP_t)]
bridge.rm_free_BP.restype = check_status

class BasePartition (Resource):
    
    _ctype = POINTER(rm_BP_t)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_BP(self)
    
    def _get_id (self):
        id = self._get_data(RM_BPID, rm_bp_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_data(RM_BPState, rm_BP_state_t)
        return rm_BP_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_location (self):
        location = self._get_data(RM_BPLoc, rm_location_t)
        return (location.X, location.Y, location.Z)
    
    location = property(_get_location)
    
    def _get_partition_id (self):
        partition_id = self._get_data(RM_BPPartID, pm_partition_id_t)
        return free_value(partition_id)
    
    partition_id = property(_get_partition_id)
    
    def _get_partition_state (self):
        state = self._get_data(RM_BPPartState, rm_partition_state_t)
        return rm_partition_state_values[state.value]
    
    partition_state = property(_get_partition_state)
    
    def _get_part_of_small (self):
        sdb = self._get_data(RM_BPSDB, c_int)
        return sdb.value != 0
    
    part_of_small = property(_get_part_of_small)
    
    def _get_divided_into_small (self):
        sd = self._get_data(RM_BPSD, c_int)
        return sd.value != 0
    
    divided_into_small = property(_get_divided_into_small)
    
    def _get_compute_node_memory (self):
        memory = self._get_data(RM_BPComputeNodeMemory, rm_BP_computenode_memory_t)
        return rm_BP_computenode_memory_values[memory.value]
    
    compute_node_memory = property(_get_compute_node_memory)


class rm_nodecard_t (Structure):
    _fields_ = []

rm_nodecard_id_t = rm_component_id_t
rm_quarter_t = c_int
rm_quarter_values = ("RM_Q1", "RM_Q2", "RM_Q3", "RM_Q4", "RM_Q_NAV")
rm_nodecard_state_t = c_int
rm_nodecard_state_values = ("RM_NODECARD_UP", "RM_NODECARD_DOWN", "RM_NODECARD_MISSING", "RM_NODECARD_ERROR", "RM_NODECARD_NAV")

if systype == 'bgl':
    RM_NodeCardID = 18
    RM_NodeCardQuarter = 19
    RM_NodeCardState = 20
    RM_NodeCardIONodes = 21
    RM_NodeCardPartID = 22
    RM_NodeCardPartState = 23
elif systype == 'bgp':
    RM_NodeCardID = 4000
    RM_NodeCardQuarter = 4001
    RM_NodeCardState = 4002
    RM_NodeCardIONodes = 4004
    RM_NodeCardPartID = 4005
    RM_NodeCardPartState = 4006

bridge.rm_free_nodecard.argtypes = [POINTER(rm_nodecard_t)]
bridge.rm_free_nodecard.restype = check_status

class NodeCard (Resource):
    
    _ctype = POINTER(rm_nodecard_t)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_nodecard(self)
    
    def _get_id (self):
        id = self._get_data(RM_NodeCardID, rm_nodecard_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_quarter (self):
        quarter = self._get_data(RM_NodeCardQuarter, rm_quarter_t)
        return rm_querter_values[quarter.value]
    
    quarter = property(_get_quarter)
    
    def _get_state (self):
        state = self._get_data(RM_NodeCardState, rm_nodecard_state_t)
        return rm_nodecard_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_io_nodes (self):
        io_nodes = self._get_data(RM_NodeCardIONodes, c_int)
        return io_nodes.value
    
    io_nodes = property(_get_io_nodes)
    
    def _get_partition_id (self):
        partition_id = self._get_data(RM_NodeCardPartID, pm_partition_id_t)
        return free_value(partition_id)
    
    partition_id = property(_get_partition_id)
    
    def _get_partition_state (self):
        state = self._get_data(RM_NodeCardPartState, rm_partition_state_t)
        return rm_partition_state_values[state.value]
    
    partition_state = property(_get_partition_state)


class rm_nodecard_list_t (Structure):
    _fields_ = []

bridge.rm_get_nodecards.argtypes = [rm_bp_id_t, POINTER(POINTER(rm_nodecard_list_t))]
bridge.rm_get_nodecards.restype = check_status

if systype == 'bgl':
    RM_NodeCardListSize = 86
    RM_NodeCardListFirst = 87
    RM_NodeCardListNext = 88
elif systype == 'bgp':
    RM_NodeCardListSize = 3000
    RM_NodeCardListFirst = 3001
    RM_NodeCardListNext = 3002

bridge.rm_free_nodecard_list.argtypes = [POINTER(rm_nodecard_list_t)]
bridge.rm_free_nodecard_list.restype = check_status

class NodeCardList (Resource, ElementGenerator):
    
    _ctype = POINTER(rm_nodecard_list_t)
    
    @classmethod
    def by_base_partition (cls, base_partition):
        try:
            base_partition_id = base_partition.id # accepts a BasePartition...
        except AttributeError:
            base_partition_id = base_partition # or a bpid
        element_pointer = cls._ctype()
        bridge.rm_get_nodecards(c_char_p(base_partition_id), byref(element_pointer))
        return cls(element_pointer, free=True)
    
    def __init__ (self, element_pointer, **kwargs):
        Resource.__init__(self, element_pointer, **kwargs)
        ElementGenerator.__init__(self, self, NodeCard, RM_NodeCardListSize, RM_NodeCardListFirst, RM_NodeCardListNext)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_nodecard_list(self)
    
    def __repr__ (self):
        return "<%s %i>" % (self.__class__.__name__, len(self))


class rm_switch_t (Structure):
    _fields_ = []

rm_switch_id_t = rm_component_id_t
rm_switch_state_t = c_int
rm_switch_state_values = ("RM_SWITCH_UP", "RM_SWITCH_DOWN", "RM_SWITCH_MISSING", "RM_SWITCH_ERROR", "RM_SWITCH_NAV")
rm_dimension_t = c_int
rm_dimension_values = ("RM_DIM_X", "RM_DIM_Y", "RM_DIM_Z")

if systype == 'bgl':
    RM_SwitchID = 24
    RM_SwitchBPID = 25
    RM_SwitchState = 26
    RM_SwitchDim = 27
    RM_SwitchFirstConnection = 28
    RM_SwitchNextConnection = 29
    RM_SwitchConnNum = 30
elif systype == 'bgp':
    RM_SwitchID = 6000
    RM_SwitchBPID = 6001
    RM_SwitchState = 6002
    RM_SwitchDim = 6004
    RM_SwitchFirstConnection = 6006
    RM_SwitchNextConnection = 6007
    RM_SwitchConnNum = 6005
    
bridge.rm_free_switch.argtypes = [POINTER(rm_switch_t)]
bridge.rm_free_switch.restype = check_status

class Switch (Resource):
    
    _ctype = POINTER(rm_switch_t)
    
    def __init__ (self, element_pointer, **kwargs):
        Resource.__init__(self, element_pointer, **kwargs)
        # self.connections = ElementGenerator(self, ?...) # requires a connection object, and implementation of class-level ctype
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_switch(self)
    
    def _get_id (self):
        id = self._get_data(RM_SwitchID, rm_switch_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_base_partition_id (self):
        id = self._get_data(RM_SwitchBPID, rm_bp_id_t)
        return free_value(id)
    
    base_partition_id = property(_get_base_partition_id)
    
    def _get_state (self):
        state = self._get_data(RM_SwitchState, rm_switch_state_t)
        return rm_switch_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_dimension (self):
        dimension = self._get_data(RM_SwitchDim, rm_dimension_t)
        return rm_dimension_values[dimension.value]
    
    dimension = property(_get_dimension)


class rm_wire_t (Structure):
    _fields_ = []

rm_wire_id_t = rm_component_id_t
rm_wire_state_t = c_int
rm_wire_state_values = ("UP", "DOWN")

if systype == 'bgl':
    RM_WireID = 31
    RM_WireState = 32
    RM_WireFromPort = 33
    RM_WireToPort = 34
    RM_WirePartID = 35
    RM_WirePartState = 36
elif systype == 'bgp':
    RM_WireID = 7000
    RM_WireState = 7001
    RM_WireFromPort = 7002
    RM_WireToPort = 7003
    RM_WirePartID = 7004
    RM_WirePartState = 7005

class Wire (Resource):
    
    _ctype = POINTER(rm_wire_t)
    
    def _get_id (self):
        id = self._get_data(RM_WireID, rm_wire_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_data(RM_WireState, rm_wire_state_t)
        return rm_wire_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_from_port (self):
        port = self._get_data(RM_WireFromPort, rm_element_t)
        return Port(port)
    
    from_port = property(_get_from_port)
    
    def _get_to_port (self):
        port = self._get_data(RM_WireToPort, rm_element_t)
        return Port(port)
    
    to_port = property(_get_to_port)
    
    def _get_partition_id (self):
        id = self._get_data(RM_WirePartID, pm_partition_id_t)
        return free_value(id)
    
    partition_id = property(_get_partition_id)
    
    def _get_partition_state (self):
        state = self._get_data(RM_WirePartState, rm_partition_state_t)
        return rm_partition_state_values[state.value]
    
    partition_state = property(_get_partition_state)


class rm_port_t (Structure):
    _fields_ = []

rm_port_id_t = c_int

if systype == 'bgl':
    RM_PortComponentID = 37
    RM_PortID = 38
elif systype == 'bgp':
    RM_PortComponentID = 8000
    RM_PortID = 8001
    
class Port (Resource):
    
    _ctype = POINTER(rm_port_t)
    
    def __repr__ (self):
        return "<%s %i>" % (self.__class__.__name__, self.id)
    
    def _get_component_id (self):
        id = self._get_data(RM_PortComponentID, rm_component_id_t)
        return free_value(id)
    
    component_id = property(_get_component_id)
    
    def _get_id (self):
        id = self._get_data(RM_PortID, rm_port_id_t)
        return id.value
    
    id = property(_get_id)


class rm_partition_list_t (Structure):
    _fields_ = []

if systype == 'bgl':
    RM_PartListSize = 80
    RM_PartListFirstPart = 81
    RM_PartListNextPart = 82
elif systype == 'bgp':
    RM_PartListSize = 9000
    RM_PartListFirstPart = 9001
    RM_PartListNextPart = 9002

PARTITION_FREE_FLAG = 0x1
PARTITION_CONFIGURING_FLAG = 0x2
PARTITION_READY_FLAG = 0x4
PARTITION_BUSY_FLAG = 0x8
PARTITION_DEALLOCATING_FLAG = 0x10
PARTITION_ERROR_FLAG = 0x20
PARTITION_ALL_FLAG = 0xFF

bridge.rm_get_partitions.argtypes = [rm_partition_state_t, POINTER(POINTER(rm_partition_list_t))]
bridge.rm_get_partitions.restype = check_status

bridge.rm_get_partitions_info.argtypes = [rm_partition_state_t, POINTER(POINTER(rm_partition_list_t))]
bridge.rm_get_partitions_info.restype = check_status

bridge.rm_free_partition_list.argtypes = [POINTER(rm_partition_t)]
bridge.rm_free_partition_list.restype = check_status

class PartitionList (Resource, ElementGenerator):
    
    _ctype = POINTER(rm_partition_list_t)
    
    @classmethod
    def by_filter (cls, filter=PARTITION_ALL_FLAG):
        element_pointer = cls._ctype()
        bridge.rm_get_partitions(c_int(filter), byref(element_pointer))
        return cls(element_pointer, free=True)
    
    @classmethod
    def info_by_filter (cls, filter=PARTITION_ALL_FLAG):
        element_pointer = cls._ctype()
        bridge.rm_get_partitions_info(c_int(filter), byref(element_pointer))
        return cls(element_pointer, free=True)

    def __init__ (self, element_pointer, **kwargs):
        Resource.__init__(self, element_pointer, **kwargs)
        ElementGenerator.__init__(self, self, Partition, RM_PartListSize, RM_PartListFirstPart, RM_PartListNextPart)


class rm_job_list_t (Structure):
    _fields_ = []

rm_job_state_flag_t = c_int
bridge.rm_get_jobs.argtypes = [rm_job_state_flag_t, POINTER(POINTER(rm_job_list_t))]
bridge.rm_get_jobs.restype = check_status

if systype == 'bgl':
    RM_JobListSize = 83
    RM_JobListFirstJob = 84
    RM_JobListNextJob = 85
elif systype == 'bgp':
    RM_JobListSize = 11000
    RM_JobListFirstJob = 11001
    RM_JobListNextJob = 11002

bridge.rm_free_job_list.argtypes = [POINTER(rm_job_list_t)]
bridge.rm_free_job_list.restype = check_status

class JobList (Resource, ElementGenerator):
    
    _ctype = POINTER(rm_job_list_t)
    
    @classmethod
    def by_flag (cls, flag):
        element_pointer = cls._ctype()
        bridge.rm_get_jobs(c_int(flag), byref(element_pointer))
        return cls(pointer, free=True)
    
    def __init__ (self, element_pointer, **kwargs):
        Resource.__init__(self, element_pointer, **kwargs)
        ElementGenerator.__init__(self, self, Job, RM_JobListSize, RM_JobListFirstJob, RM_JobListNextJob)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_job_list(self)


class rm_job_t (Structure):
    _fields_ = []

rm_job_id_t = c_char_p
db_job_id_t = c_int
rm_job_state_t = c_int
rm_job_state_values = ("RM_JOB_IDLE", "RM_JOB_STARTING", "RM_JOB_RUNNING", "RM_JOB_TERMINATED", "RM_JOB_KILLED", "RM_JOB_ERROR", "RM_JOB_DYING", "RM_JOB_DEBUG", "RM_JOB_LOAD", "RM_JOB_LOADED", "RM_JOB_BEGIN", "RM_JOB_ATTACH", "RM_JOB_NAV")
rm_job_mode_t = c_int
rm_job_mode_values = ("RM_COPROCESSOR_MODE", "RM_VIRTUAL_NODE_MODE")
rm_job_strace_t = c_int
rm_job_stdin_info_t = c_int
rm_job_stdout_info_t = c_int
rm_job_stderr_info_t = c_int
rm_job_runtime_t = c_int
rm_job_computenodes_used_t = c_int
rm_job_exitstatus_t = c_int

if systype == 'bgl':
    RM_JobState = 64
    RM_JobExecutable = 65
    RM_JobID = 66
    RM_JobPartitionID = 67
    RM_JobUserName = 68
    RM_JobDBJobID = 69
    RM_JobOutFile = 70
    RM_JobInFile = 71
    RM_JobErrFile = 72
    RM_JobOutDir = 73
    RM_JobErrText = 74
    RM_JobArgs = 75
    RM_JobEnvs = 76
    RM_JobInHist = 77
    RM_JobExitStatus = 78
    RM_JobMode = 79
    # Revision 2
    RM_JobStrace = 89
    RM_JobStdinInfo = 90
    RM_JobStdoutInfo = 91
    RM_JobStderrInfo = 92
    # Revision 3
    RM_JobStartTime = 94
    RM_JobEndTime = 95
    RM_JobRunTime = 96
    RM_JobComputeNodesUsed = 97
elif systype == 'bgp':
    RM_JobState = 12002
    RM_JobExecutable = 12004
    RM_JobID = 12000
    RM_JobPartitionID = 12001
    RM_JobUserName = 12005
    RM_JobDBJobID = 12006
    RM_JobOutFile = 12007
    RM_JobErrFile = 12008
    RM_JobOutDir = 12009
    RM_JobErrText = 12010
    RM_JobArgs = 12011
    RM_JobEnvs = 12012
    RM_JobInHist = 12013
    RM_JobExitStatus = 12020
    RM_JobMode = 12014
    RM_JobStrace = 12015
    RM_JobStartTime = 12016
    RM_JobEndTime = 12017
    RM_JobRunTime = 12018
    RM_JobComputeNodesUsed = 12019

bridge.rm_get_job.argtypes = [db_job_id_t, POINTER(POINTER(rm_job_t))]
bridge.rm_get_job.restype = check_status

bridge.rm_free_job.argtypes = [POINTER(rm_job_t)]
bridge.rm_free_job.restype = check_status

class Job (Resource):
    
    _ctype = POINTER(rm_job_t)
    
    def __del__ (self):
        if self._free:
            bridge.rm_free_job(self)
    
    def _get_id (self):
        id = self._get_data(RM_JobID, rm_job_id_t)
        return free_value(id)
    
    id = property(_get_id)
    
    def _get_partition_id (self):
        id = self._get_data(RM_JobPartitionID, pm_partition_id_t)
        return free_value(id)
    
    partition_id = property(_get_partition_id)
    
    def _get_state (self):
        state = self._get_data(RM_JobState, rm_job_state_t)
        return rm_job_state_values[state.value]
    
    state = property(_get_state)
    
    def _get_executable (self):
        executable = self._get_data(RM_JobExecutable, c_char_p)
        return free_value(executable)
    
    executable = property(_get_executable)
    
    def _get_user_name (self):
        user_name = self._get_data(RM_JobUserName, c_char_p)
        return free_value(user_name)
    
    user_name = property(_get_user_name)
    
    def _get_db_id (self):
        id = self._get_data(RM_JobDBJobID, db_job_id_t)
        return id.value
    
    id = property(_get_db_id)
    
    def _get_outfile (self):
        outfile = self._get_data(RM_JobOutFile, c_char_p)
        return free_value(outfile)
    
    outfile = property(_get_outfile)
    
    def _get_infile (self):
        # deprecated. add a DeprecationWarning
        infile = self._get_data(RM_JobInFile, c_char_p)
        return free_value(infile)

    if systype == 'bgl':
        infile = property(_get_infile)
    
    def _get_errfile (self):
        errfile = self._get_data(RM_JobErrFile, c_char_p)
        return free_value(errfile)
    
    errfile = property(_get_errfile)
    
    def _get_outdir (self):
        outdir = self._get_data(RM_JobOutDir, c_char_p)
        return free_value(outdir)
    
    outdir = property(_get_outdir)
    
    def _get_errtext (self):
        errtext = self._get_data(RM_JobErrText, c_char_p)
        return free_value(errtext)
    
    errtext = property(_get_errtext)
    
    def _get_args (self):
        args = self._get_data(RM_JobArgs, c_char_p)
        return free_value(args)
    
    args = property(_get_args)
    
    def _get_envs (self):
        envs = self._get_data(RM_JobEnvs, c_char_p)
        return free_value(envs)
    
    envs = property(_get_envs)
    
    def _get_in_history (self):
        in_history = self._get_data(RM_JobInHist, c_int)
        return in_history.value != 0
    
    in_history = property(_get_in_history)
    
    def _get_mode (self):
        mode = self._get_data(RM_JobMode, rm_job_mode_t)
        return rm_job_mode_values[mode.value]
    
    mode = property(_get_mode)
    
    def _get_strace (self):
        strace = self._get_data(RM_JobStrace, rm_job_strace_t)
        return strace.value
    
    strace = property(_get_strace)
    
    def _get_stdin_info (self):
        stdin_info = self._get_data(RM_JobStdinInfo, rm_job_stdin_info_t)
        return stdin_info.value

    if systype == 'bgl':
        stdin_info = property(_get_stdin_info)
    
    def _get_stdout_info (self):
        stdout_info = self._get_data(RM_JobStdoutInfo, rm_job_stdout_info_t)
        return stdout_info.value

    if systype == 'bgl':
        stdout_info = property(_get_stdout_info)
    
    def _get_stderr_info (self):
        stderr_info = self._get_data(RM_JobStderrInfo, rm_job_stderr_info_t)
        return stderr_info.value

    if systype == 'bgl':
        stderr_info = property(_get_stderr_info)
    
    def _get_starttime (self):
        starttime = self._get_data(RM_JobStartTime, c_char_p)
        return free_value(starttime)
    
    starttime = property(_get_starttime)
    
    def _get_endtime (self):
        endtime = self._get_data(RM_JobEndTime, c_char_p)
        return free_value(endtime)
    
    endtime = property(_get_endtime)
    
    def _get_runtime (self):
        runtime = self._get_data(RM_JobRunTime, rm_job_runtime_t)
        return runtime.value
    
    runtime = property(_get_runtime)
    
    def _get_compute_nodes_used (self):
        compute_nodes_used = self._get_data(RM_JobComputeNodesUsed, rm_job_computenodes_used_t)
        return compute_nodes_used.value
    
    compute_nodes_used = property(_get_compute_nodes_used)
    
    def _get_exit_status (self):
        exit_status = self._get_data(RM_JobExitStatus, rm_job_exitstatus_t)
        return exit_status.value
    
    exit_status = property(_get_exit_status)
