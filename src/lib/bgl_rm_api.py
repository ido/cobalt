from ctypes import *

STRING = c_char_p

class enum(object):
    def __init__(self, fields):
        self.fields = fields
    def __call__(self, item):
        return self.fields[item.value]

# enum rm_port_id
RM_PortIDEnum = enum(['RM_PORT_PLUS_X', 'RM_PORT_MINUS_X',
                      'RM_PORT_PLUS_Y', 'RM_PORT_MINUS_Y',
                      'RM_PORT_PLUS_Z', 'RM_PORT_MINUS_Z',
                      'RM_PORT_S0', 'RM_PORT_S1', 'RM_PORT_S2',
                      'RM_PORT_S3', 'RM_PORT_S4', 'RM_PORT_S5',
                      'RM_PORT_NAV'])

# enum rm_BP_state
RM_BPStateEnum = enum(['RM_BP_UP', 'RM_BP_DOWN', 'RM_BP_MISSING',
                       'RM_BP_ERROR', 'RM_BP_NAV'])

# enum rm_switch_state
RM_SwitchStateEnum = enum(['RM_SWITCH_UP', 'RM_SWITCH_DOWN',
                           'RM_SWITCH_MISSING', 'RM_SWITCH_ERROR',
                           'RM_SWITCH_NAV'])

# enum rm_dimension
RM_DimensionEnum = enum(['RM_DIM_X', 'RM_DIM_Y', 'RM_DIM_Z', 'RM_DIM_NAV'])

# enum rm_wire_state
RM_WireStateEnum = enum(['RM_WIRE_UP', 'RM_WIRE_DOWN', 'RM_WIRE_MISSING',
                         'RM_WIRE_ERROR', 'RM_WIRE_NAV'])

# enum rm_partition_state
RM_PartitionStateEnum = enum( \
    ['RM_PARTITION_FREE', 'RM_PARTITION_CONFIGURING', 'RM_PARTITION_READY',
     'RM_PARTITION_BUSY', 'RM_PARTITION_DEALLOCATING', 'RM_PARTITION_ERROR',
     'RM_PARTITION_NAV'])

# enum rm_partition_mode
RM_PartitionModeEnum = enum(['RM_PARTITION_COPROCESSOR_MODE',
                             'RM_PARTITION_VIRTUAL_NODE_MODE'])

# enum rm_job_mode
RM_JobModeEnum = enum(['RM_COPROCESSOR_MODE', 'RM_VIRTUAL_NODE_MODE'])

# enum rm_job_state
RM_JobStateEnum = enum(['RM_JOB_IDLE', 'RM_JOB_STARTING', 'RM_JOB_RUNNING',
                        'RM_JOB_TERMINATED', 'RM_JOB_KILLED',
                        'RM_JOB_ERROR', 'RM_JOB_DYING', 'RM_JOB_DEBUG',
                        'RM_JOB_LOAD', 'RM_JOB_LOADED', 'RM_JOB_BEGIN',
                        'RM_JOB_ATTACH', 'RM_JOB_NAV'])

# enum rm_connection_type
RM_ConnectionTypeEnum = enum(['RM_MESH', 'RM_TORUS', 'RM_NAV'])
  
# enum rm_nodecard_state
RM_NodeCardStateEnum = enum(['RM_NODECARD_UP', 'RM_NODECARD_DOWN',
                             'RM_NODECARD_MISSING', 'RM_NODECARD_ERROR',
                             'RM_NODECARD_NAV'])

# enum rm_quarter
RM_QuarterEnum = enum(['RM_Q1', 'RM_Q2', 'RM_Q3', 'RM_Q4', 'RM_Q_NAV'])

# enum rm_BP_computenode_memory
RM_ComputenodeMemoryEnum = enum(['RM_BP_COMPUTENODE_MEMORY_256M',
                                 'RM_BP_COMPUTENODE_MEMORY_512M',
                                 'RM_BP_COMPUTENODE_MEMORY_1G',
                                 'RM_BP_COMPUTENODE_MEMORY_2G',
                                 'RM_BP_COMPUTENODE_MEMORY_4G',
                                 'RM_BP_COMPUTENODE_MEMORY_NAV'])

RM_BPLoc = 13
RM_JobStderrInfo = 92
JOB_NOT_FOUND = -2
RM_JobPartitionID = 67
RM_NodeCardID = 18
RM_MODIFY_BlrtsImg = 3
RM_NextSwitch = 7
RM_SwitchBPID = 25
RM_NodeCardPartState = 23
RM_PartitionFirstUser = 62
RM_JobExitStatus = 78
RM_JobRunTime = 96
RM_PartitionID = 39
JOB_ALREADY_DEFINED = -5
RM_BPSD = 17
RM_NextWire = 10
RM_PartitionConnection = 41
RM_PartitionNextBP = 45
RM_PortID = 38
RM_MODIFY_LinuxImg = 4
RM_PartListFirstPart = 81
SWITCH_NOT_FOUND = -4
RM_PartitionLinuxImg = 51
RM_PortComponentID = 37
RM_PartitionNodeCardNum = 57
RM_BPsize = 0
CONNECTION_ERROR = -10
RM_BPPartID = 14
RM_JobID = 66
RM_PartitionFirstSwitch = 47
RM_JobOutFile = 70
RM_JobOutDir = 73
RM_SwitchState = 26
RM_Msize = 1
RM_NodeCardListSize = 86
RM_PartitionOptions = 53
RM_WirePartID = 35
INTERNAL_ERROR = -11
RM_BPState = 12
RM_WirePartState = 36
RM_PartitionFirstBP = 44
INCOMPATIBLE_STATE = -13
RM_WireToPort = 34
RM_PartitionNextUser = 63
RM_SwitchNum = 5
RM_NodeCardPartID = 22
RM_JobStartTime = 94
RM_MODIFY_Options = 6
BP_NOT_FOUND = -3
RM_PartitionUsersNum = 61
RM_JobState = 64
RM_JobErrText = 74
RM_JobMode = 79
RM_WireState = 32
RM_JobComputeNodesUsed = 97
RM_PartListNextPart = 82
RM_NodeCardListFirst = 87
RM_PartitionMode = 54
RM_MODIFY_Owner = 0
RM_MODIFY_MloaderImg = 2
RM_PartitionFirstNodeCard = 58
RM_BPID = 11
RM_PartListSize = 80
RM_FirstSwitch = 6
INCONSISTENT_DATA = -14
RM_JobListSize = 83
RM_PartitionPsetsPerBP = 60
RM_JobExecutable = 65
RM_PartitionNextNodeCard = 59
RM_PartitionSmall = 56
RM_MODIFY_Description = 1
RM_SwitchConnNum = 30
RM_BPPartState = 15
RM_PartitionMloaderImg = 49
RM_WireFromPort = 33
RM_NodeCardListNext = 88
RM_SwitchFirstConnection = 28
RM_FirstBP = 3
RM_PartitionUserName = 42
RM_NodeCardQuarter = 19
RM_PartitionNextSwitch = 48
INVALID_INPUT = -12
RM_NextBP = 4
RM_JobEnvs = 76
RM_JobInHist = 77
RM_JobEndTime = 95
RM_JobStdoutInfo = 91
RM_PartitionBlrtsImg = 50
RM_JobStrace = 89
RM_JobArgs = 75
RM_FirstWire = 9
RM_BPNum = 2
RM_SwitchDim = 27
STATUS_OK = 0
RM_JobListNextJob = 85
RM_SwitchNextConnection = 29
RM_MODIFY_RamdiskImg = 5
RM_JobStdinInfo = 90
RM_NodeCardState = 20
RM_PartitionDescription = 55
RM_PartitionSwitchNum = 46
RM_WireNum = 8
RM_WireID = 31
PARTITION_NOT_FOUND = -1
RM_JobDBJobID = 69
RM_JobListFirstJob = 84
RM_JobUserName = 68
RM_PartitionState = 40
RM_SwitchID = 24
RM_NodeCardIONodes = 21
RM_PartitionBPNum = 43
RM_BPSDB = 16
RM_JobErrFile = 72
RM_BPComputeNodeMemory = 93
RM_JobInFile = 71
RM_PartitionRamdiskImg = 52
class MPIR_PROCDESC(Structure):
    pass
MPIR_PROCDESC._fields_ = [
    ('host_name', STRING),
    ('executable_name', STRING),
    ('pid', c_int),
]
rm_serial_t = STRING
rm_component_id_t = STRING
rm_switch_id_t = rm_component_id_t
rm_bp_id_t = rm_component_id_t
rm_wire_id_t = rm_component_id_t
rm_nodecard_id_t = rm_component_id_t
pm_partition_id_t = STRING
jm_job_id_t = STRING
db_job_id_t = c_int
rm_element_t = c_void_p
rm_partition_state_flag_t = c_int
rm_job_state_flag_t = c_int
rm_signal_t = c_int
rm_job_strace_t = c_int
rm_job_stdin_info_t = c_int
rm_job_stdout_info_t = c_int
rm_job_stderr_info_t = c_int
rm_job_runtime_t = c_int
rm_job_computenodes_used_t = c_int
rm_job_exitstatus_t = c_int
class rm_BGL(Structure):
    pass
rm_BGL._fields_ = [
]
rm_BGL_t = rm_BGL
class rm_port(Structure):
    pass
rm_port._fields_ = [
]
rm_port_t = rm_port
class rm_BP(Structure):
    pass
rm_BP_t = rm_BP
rm_BP._fields_ = [
]
class rm_switch(Structure):
    pass
rm_switch._fields_ = [
]
rm_switch_t = rm_switch
class rm_wire(Structure):
    pass
rm_wire_t = rm_wire
rm_wire._fields_ = [
]
class rm_nodecard(Structure):
    pass
rm_nodecard._fields_ = [
]
rm_nodecard_t = rm_nodecard
class rm_partition(Structure):
    pass
rm_partition._fields_ = [
]
rm_partition_t = rm_partition
class rm_job(Structure):
    pass
rm_job_t = rm_job
rm_job._fields_ = [
]
class rm_partition_list(Structure):
    pass
rm_partition_list_t = rm_partition_list
rm_partition_list._fields_ = [
]
class rm_job_list(Structure):
    pass
rm_job_list_t = rm_job_list
rm_job_list._fields_ = [
]
class rm_nodecard_list(Structure):
    pass
rm_nodecard_list_t = rm_nodecard_list
rm_nodecard_list._fields_ = [
]

# values for enumeration 'rm_port_id'
rm_port_id = c_int # enum

# values for enumeration 'rm_BP_state'
rm_BP_state = c_int # enum

# values for enumeration 'rm_switch_state'
rm_switch_state = c_int # enum

# values for enumeration 'rm_dimension'
rm_dimension = c_int # enum

# values for enumeration 'rm_wire_state'
rm_wire_state = c_int # enum

# values for enumeration 'rm_partition_state'
rm_partition_state = c_int # enum

# values for enumeration 'rm_partition_mode'
rm_partition_mode = c_int # enum

# values for enumeration 'rm_job_mode'
rm_job_mode = c_int # enum

# values for enumeration 'rm_job_state'
rm_job_state = c_int # enum

# values for enumeration 'rm_connection_type'
rm_connection_type = c_int # enum

# values for enumeration 'rm_nodecard_state'
rm_nodecard_state = c_int # enum

# values for enumeration 'rm_quarter'
rm_quarter = c_int # enum

# values for enumeration 'rm_BP_computenode_memory'
rm_BP_computenode_memory = c_int # enum
rm_port_id_t = rm_port_id
rm_BP_state_t = rm_BP_state
rm_switch_state_t = rm_switch_state
rm_dimension_t = rm_dimension
rm_wire_state_t = rm_wire_state
rm_partition_state_t = rm_partition_state
rm_job_state_t = rm_job_state
rm_connection_type_t = rm_connection_type
rm_partition_mode_t = rm_partition_mode
rm_job_mode_t = rm_job_mode
rm_nodecard_state_t = rm_nodecard_state
rm_quarter_t = rm_quarter
rm_BP_computenode_memory_t = rm_BP_computenode_memory

# values for enumeration 'rm_specification'
rm_specification = c_int # enum

# values for enumeration 'rm_modify_op'
rm_modify_op = c_int # enum
class rm_location_t(Structure):
    pass
rm_location_t._fields_ = [
    ('X', c_int),
    ('Y', c_int),
    ('Z', c_int),
]
class rm_size3D_t(Structure):
    pass
rm_size3D_t._fields_ = [
    ('X', c_int),
    ('Y', c_int),
    ('Z', c_int),
]
class rm_connection_t(Structure):
    pass
rm_connection_t._fields_ = [
    ('p1', rm_port_id_t),
    ('p2', rm_port_id_t),
    ('part_id', pm_partition_id_t),
    ('part_state', rm_partition_state_t),
]

# values for enumeration 'status'
status = c_int # enum
status_t = status
JOB_DYING_FLAG = 32 # Variable c_int
SN_LENGTH = 33 # Variable c_int
JOB_ALL_FLAG = 4095 # Variable c_int
JOB_STARTING_FLAG = 2 # Variable c_int
JOB_ATTACH_FLAG = 1024 # Variable c_int
PARTITION_ALL_FLAG = 255 # Variable c_int
PARTITION_BUSY_FLAG = 8 # Variable c_int
PARTITION_CONFIGURING_FLAG = 2 # Variable c_int
PARTITION_ERROR_FLAG = 32 # Variable c_int
JOB_DEBUG_FLAG = 64 # Variable c_int
JOB_LOADED_FLAG = 256 # Variable c_int
PARTITION_DEALLOCATING_FLAG = 16 # Variable c_int
MPIR_DEBUG_SPAWNED = 1 # Variable c_int
MPIR_DEBUG_ABORTING = 2 # Variable c_int
JOB_BEGIN_FLAG = 512 # Variable c_int
JOB_TERMINATED_FLAG = 8 # Variable c_int
JOB_KILLED_FLAG = 2048 # Variable c_int
JOB_IDLE_FLAG = 1 # Variable c_int
JOB_ERROR_FLAG = 16 # Variable c_int
PARTITION_READY_FLAG = 4 # Variable c_int
PARTITION_FREE_FLAG = 1 # Variable c_int
JOB_LOAD_FLAG = 128 # Variable c_int
JOB_RUNNING_FLAG = 4 # Variable c_int

__all__ = ['RM_PartitionPsetsPerBP', 'rm_port_id',
           'RM_PartitionOptions', 'RM_JobRunTime',
           'RM_PartListFirstPart', 'RM_JobExecutable',
           'RM_JobErrText', 'RM_PartitionFirstNodeCard',
           'rm_job_strace_t', 'JOB_STARTING_FLAG', 'RM_NextWire',
           'rm_partition_state_t',
           'rm_modify_op', 'rm_job_list_t',
           'RM_NodeCardPartState', 'RM_JobStateEnum',
           'JOB_DYING_FLAG', 'INCOMPATIBLE_STATE', 'rm_switch_t',
           'PARTITION_BUSY_FLAG', 'RM_SwitchNextConnection',
           'rm_connection_type_t', 
           'RM_JobListFirstJob', 'rm_partition_state', 'RM_SwitchNum',
           'RM_SwitchState', 
           'rm_job_state_t', 'rm_partition_list',
           'rm_port_t', 'rm_nodecard', 
           'RM_FirstSwitch', 'JOB_IDLE_FLAG',
           'RM_NodeCardID', 'rm_nodecard_list_t',
           'RM_PartitionDescription', 'RM_PartitionNextBP',
           'rm_BP_computenode_memory', 'RM_JobListSize',
           'rm_job_t', 'INCONSISTENT_DATA',
           'MPIR_DEBUG_ABORTING', 'rm_specification',
           'rm_partition_t', 'RM_NodeCardState',
           'RM_WireNum', 'RM_WireID', 'rm_nodecard_list',
           'RM_JobStartTime', 'status', 'rm_size3D_t',
           'rm_nodecard_state', 'RM_SwitchFirstConnection',
           'MPIR_PROCDESC', 'rm_job_state_flag_t', 'rm_dimension_t',
           'rm_port_id_t', 'RM_NodeCardListFirst',
           'rm_partition_state_flag_t', 'RM_JobMode', 'rm_wire_id_t', 
           'status_t', 'rm_port', 'JOB_LOAD_FLAG', 'RM_WireToPort',
           'JOB_NOT_FOUND', 'RM_JobErrFile', 'RM_Msize', 'RM_SwitchDim',
           'rm_BP_computenode_memory_t', 'rm_nodecard_id_t',
           'RM_JobDBJobID', 'RM_JobEndTime', 'rm_partition_list_t',
           'RM_PartitionBlrtsImg', 'rm_component_id_t', 'RM_BPPartState', 
           'rm_job_runtime_t', 'RM_MODIFY_MloaderImg', 'RM_SwitchID',
           'RM_PortComponentID', 'RM_PartitionNodeCardNum', 
           'rm_job_stdin_info_t', 'INTERNAL_ERROR', 'RM_PartitionFirstBP', 
           'INVALID_INPUT', 'RM_JobStderrInfo', 'rm_location_t', 
           'RM_PartitionMode', 'rm_connection_t', 'rm_partition_mode',
           'RM_JobComputeNodesUsed', 'RM_BPID', 'RM_JobState',
           'RM_PartitionSmall', 'RM_PartitionConnection', 
           'RM_JobStdinInfo', 'rm_job_mode', 'JOB_RUNNING_FLAG',
           'RM_PartitionState', 'RM_NodeCardPartID',
           'rm_job_exitstatus_t', 
           'RM_MODIFY_BlrtsImg', 'RM_NodeCardIONodes',
           'pm_partition_id_t', 'RM_PartitionLinuxImg',
           'rm_partition_mode_t', 'rm_BP', 'RM_MODIFY_Description',
           'rm_wire_state_t', 'RM_BPPartID', 'rm_quarter',
           'PARTITION_ERROR_FLAG', 'RM_JobArgs', 'RM_PortID',
           'JOB_ATTACH_FLAG', 'PARTITION_ALL_FLAG',
           'RM_JobOutFile', 'rm_switch_state_t', 'MPIR_DEBUG_SPAWNED',
           'RM_FirstWire', 'RM_NodeCardListNext', 'RM_BPState',
           'RM_PartitionMloaderImg',
           'rm_serial_t', 'rm_partition', 'SN_LENGTH',
           'RM_PartitionUsersNum', 'JOB_ERROR_FLAG',
           'SWITCH_NOT_FOUND', 'rm_switch', 'RM_JobPartitionID',
           'RM_NextSwitch', 'PARTITION_NOT_FOUND', 'RM_SwitchBPID',
           'RM_MODIFY_Owner', 'RM_WireState', 'RM_JobEnvs',
           'RM_BPNum', 'rm_job', 'JOB_BEGIN_FLAG',
           'RM_MODIFY_RamdiskImg', 'RM_FirstBP', 'rm_job_list',
           'RM_MODIFY_LinuxImg', 'JOB_KILLED_FLAG', 'rm_BGL_t',
           'RM_PartitionRamdiskImg', 'rm_BGL', 'RM_PartitionID',
           'RM_JobOutDir', 'RM_BPSD', 'JOB_LOADED_FLAG',
           'RM_WirePartState', 'PARTITION_READY_FLAG', 'rm_job_state',
           'rm_BP_state_t', 'RM_PartitionFirstSwitch', 'RM_WirePartID',
           'db_job_id_t', 'RM_JobUserName', 'RM_JobInHist',
           'RM_PartitionNextNodeCard', 'rm_job_stderr_info_t',
           'RM_PartitionNextUser', 'rm_nodecard_t', 'RM_PartListSize',
           'RM_PartListNextPart', 'CONNECTION_ERROR', 'rm_wire_state',
           'JOB_ALL_FLAG', 'rm_signal_t', 'RM_BPLoc',
           'RM_BPSDB', 'BP_NOT_FOUND', 'RM_JobStdoutInfo',
           'PARTITION_FREE_FLAG', 'RM_JobExitStatus', 'rm_element_t',
           'rm_BP_state', 'RM_BPsize', 'rm_switch_state',
           'RM_JobListNextJob', 'rm_quarter_t', 'RM_WireFromPort',
           'JOB_DEBUG_FLAG', 'rm_job_stdout_info_t', 'STATUS_OK',
           'RM_NodeCardQuarter', 'PARTITION_DEALLOCATING_FLAG',
           'RM_JobID', 'RM_PartitionStateEnum', 'RM_PartitionModeEnum',
           'RM_JobStrace', 'JOB_TERMINATED_FLAG', 'RM_PartitionUserName',
           'RM_NextBP',
           'RM_PartitionBPNum', 'rm_nodecard_state_t', 'RM_JobInFile',
           'JOB_ALREADY_DEFINED', 'RM_MODIFY_Options',
           'RM_PartitionNextSwitch',
           'rm_switch_id_t', 'RM_NodeCardListSize', 'rm_bp_id_t',
           'RM_PartitionFirstUser', 'rm_wire', 'rm_connection_type', 
           'RM_BPComputeNodeMemory', 'rm_job_computenodes_used_t',
           'rm_wire_t', 'rm_BP_t', 'RM_PartitionSwitchNum', 
           'PARTITION_CONFIGURING_FLAG', 'RM_SwitchConnNum', 
           'rm_dimension', 'jm_job_id_t', 'rm_job_mode_t']
