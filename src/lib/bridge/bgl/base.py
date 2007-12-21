from ctypes import cdll, byref, c_int, c_char_p, pointer

from Cobalt.bridge.bgl import header

__all__ = [
    "BlueGene", "NodeCardList", "Partition", "BasePartition", "PSet",
    "PartitionUsers", "NodeCard", "Switch", "Port", "Wire", "Job",
    "JobList", "PartList",
]

bridge = None

def configure ():
    global bridge
    bridge = cdll.LoadLibrary("libbglbridge.so.1")
    bridge.rm_get_serial.restype = header.status_t
    bridge.rm_set_serial.restype = header.status_t
    bridge.rm_get_BGL.restype = header.status_t
    bridge.rm_get_data.restype = header.status_t
    bridge.rm_set_serial(c_char_p("BGL"))


class RMGenerator (object):
    
    def __init__ (self, container, sizeattr, headattr, tailattr, cls):
        """List-like object for accessing members of resource lists.
        
        Arguments:
        container -- parent object (e.g., 'NodeCard' would be a parent to 'Node's
        sizeattr -- attribute of object that reflects the size of the list
        headattr -- attribute of object that reflects the first item in the list
        tailattr -- attribute of object that reflects the next item in the list
        cls -- Python class to use for items of the list
        """
        self._container = container
        self._sizeattr = sizeattr
        self._headattr = headattr
        self._tailattr = tailattr
        self._cls = cls
            
    def __len__ (self):
        return getattr(self._container, self._sizeattr)

    def __iter__ (self):
        for x in xrange(getattr(self._container, self._sizeattr)):
            if x == 0:
                yield self._cls(getattr(self._container, self._headattr))
            else:
                yield self._cls(getattr(self._container, self._tailattr))

    def __getitem__ (self, index):
        return list(self)[index]


class BGDevice (object):
    
    def __init__(self, pointer):
        self._pointer = pointer
    
    def _get_bridge_field (self, field, ctype):
        value = ctype()
        bridge.rm_get_data(self._pointer, field, byref(value))
        return value


class BlueGene (BGDevice):
    
    def __init__ (self):
        my_pointer = pointer(header.rm_BGL_t())
        bridge.rm_get_BGL(byref(my_pointer))
        BGDevice.__init__(self, my_pointer)
        self.basePartitions = RMGenerator(self, "BPnum", "BPhead", "BPtail", BasePartition)
        self.wires = RMGenerator(self, "WireNum", "FirstWire", "NextWire", Wire)
    
    def reload (self):
        bridge.rm_get_BGL(byref(self._pointer))
    
    def _get_BPsize (self):
        BPsize = self._get_bridge_field(header.RM_BPsize, header.rm_size3D_t)
        return {'X':BPsize.X, 'Y':BPsize.Y, 'Z':BPsize.Z}
    
    BPsize = property(_get_BPsize)
    
    def _get_BPnum (self):
        BPnum = self._get_bridge_field(header.RM_BPNum, c_int)
        return BPnum.value
    
    BPnum = property(_get_BPnum)
    
    def _get_BPhead (self):
        return self._get_bridge_field(header.RM_FirstBP, header.rm_element_t)
    
    BPhead = property(_get_BPhead)
    
    def _get_BPtail (self):
        return self._get_bridge_field(header.RM_NextBP, header.rm_element_t)
    
    BPtail = property(_get_BPtail)
    
    def _get_SwitchNum (self):
        SwitchNum = self._get_bridge_field(header.RM_SwitchNum, c_int)
        return SwitchNum.value
    
    SwitchNum = property(_get_SwitchNum)
    
    def _get_WireNum (self):
        WireNum = self._get_bridge_field(header.RM_WireNum, c_int)
        return WireNum.value
    
    WireNum = property(_get_WireNum)
    
    def _get_FirstWire (self):
        return self._get_bridge_field(header.RM_FirstWire, header.rm_element_t)
    
    FirstWire = property(_get_FirstWire)
    
    def _get_NextWire (self):
        return self._get_bridge_field(header.RM_NextWire, header.rm_element_t)
    
    NextWire = property(_get_NextWire)


class NodeCardList (BGDevice, RMGenerator):
    
    """Builds a list of NodeCards given a basepartition."""
    
    def __init__(self, basepart_id):
        my_pointer = pointer(header.rm_nodecard_list_t())
        bridge.rm_get_nodecards(basepart_id, byref(my_pointer))
        BGDevice.__init__(self, my_pointer)
        RMGenerator.__init__(self, self, "size", "head", "tail", NodeCard)
    
    def _get_size (self):
        size = self._get_bridge_field(header.RM_NodeCardListSize, c_int)
        return size.value
    
    size = property(_get_size)
    
    def _get_head (self):
        return self._get_bridge_field(header.RM_NodeCardListFirst, header.rm_element_t)
    
    head = property(_get_head)
    
    def _get_tail (self):
        return self._get_bridge_field(header.RM_NodeCardListNext, header.rm_element_t)
    
    tail = property(_get_tail)


class Partition (BGDevice):
    
    def by_id (cls, id):
        mypointer = pointer(header.rm_partition_t())
        bridge.rm_get_partition(c_char_p(id), byref(mypointer))
        return Partition(mypointer)
    by_id = classmethod(by_id)
    
    def __init__ (self, pointer):
        BGDevice.__init__(self, pointer)
        self.basePartitions = RMGenerator(self, "BPnum", "BPhead", "BPtail", BasePartition)
        self.switches = RMGenerator(self, "Switchnum", "Switchhead", "Switchtail", Switch)
        self.users = RMGenerator(self, "Usersnum", "Usershead", "Userstail", PartitionUsers)
        
        if self.small:
            assert len(self.basePartitions) == 1
            bpid = self.basePartitions[0].id
            self.nodecards = RMGenerator(self, "NCnum", "NChead", "NCtail", NodeCard)
        else:
            self.nodecards = []
            for bp in self.basePartitions:
                self.nodecards.extend([nodecard for nodecard in NodeCardList(bp.id)])

    def reload (self):
        bridge.rm_get_partition(c_char_p(self.id), byref(self._pointer))
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_PartitionID, header.pm_partition_id_t)
        return id.value
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_bridge_field(header.RM_PartitionState, header.rm_partition_state_t)
        return header.RM_PartitionStateEnum[state.value]
    
    state = property(_get_state)
    
    def _get_BPnum (self):
        BPnum = self._get_bridge_field(header.RM_PartitionBPNum, c_int)
        return BPnum.value
    
    BPnum = property(_get_BPnum)
    
    def _get_BPhead (self):
        return self._get_bridge_field(header.RM_PartitionFirstBP, header.rm_element_t)
    
    BPhead = property(_get_BPhead)
    
    def _get_BPtail (self):
        return self._get_bridge_field(header.RM_PartitionNextBP, header.rm_element_t)
    
    BPtail = property(_get_BPtail)
    
    def _get_Switchnum (self):
        Switchnum = self._get_bridge_field(header.RM_PartitionSwitchNum, c_int)
        return Switchnum.value
    
    Switchnum = property(_get_Switchnum)
    
    def _get_Switchhead (self):
        return self._get_bridge_field(header.RM_PartitionFirstSwitch, header.rm_element_t)
    
    Switchhead = property(_get_Switchhead)
    
    def _get_Switchtail (self):
        return self._get_bridge_field(header.RM_PartitionNextSwitch, header.rm_element_t)
    
    Switchtail = property(_get_Switchtail)
    
    def _get_connection (self):
        connection = self._get_bridge_field(header.RM_PartitionConnection, header.rm_connection_type_t)
        return header.RM_ConnectionTypeEnum[connection.value]
    
    connection = property(_get_connection)
    
    def _get_user (self):
        user = self._get_bridge_field(header.RM_PartitionUserName, c_char_p)
        return user.value
    
    def _set_user (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_Owner, value)
    
    user = property(_get_user, _set_user)
    
    def _get_mloader (self):
        mloader = self._get_bridge_field(header.RM_PartitionMloaderImg, c_char_p)
        return mloader.value
    
    def _set_mloader (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_MloaderImg, value)
    
    mloader = property(_get_mloader, _set_mloader)
    
    def _get_blrts (self):
        blrts = self._get_bridge_field(header.RM_PartitionBlrtsImg, c_char_p)
        return blrts.value
    
    def _set_blrts (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_BlrtsImg, value)
    
    blrts = property(_get_blrts, _set_blrts)
    
    def _get_linux (self):
        linux = self._get_bridge_field(header.RM_PartitionLinuxImg, c_char_p)
        return linux.value
    
    def _set_linux (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_LinuxImg, value)
    
    linux = property(_get_linux, _set_linux)
    
    def _get_ramdisk (self):
        ramdisk = self._get_bridge_field(header.RM_PartitionRamdiskImg, c_char_p)
        return ramdisk.value
    
    def _set_ramdisk (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_RamdiskImg, value)
    
    ramdisk = property(_get_ramdisk, _set_ramdisk)
    
    def _get_mode (self):
        mode = self._get_bridge_field(header.RM_PartitionMode, header.rm_partition_mode_t)
        return header.RM_PartitionModeEnum[mode.value]
    
    mode = property(_get_mode)
    
    def _get_description (self):
        description = self._get_bridge_field(header.RM_PartitionDescription, c_char_p)
        return description.value
    
    def _set_description (self, value):
        value = c_char_p(value)
        bridge.rm_modify_partition(self.id, header.RM_MODIFY_Description, value)
    
    description = property(_get_description, _set_description)
    
    def _get_small (self):
        small = self._get_bridge_field(header.RM_PartitionSmall, c_int)
        return small.value != 0
    
    small = property(_get_small)
    
    def _get_psetsPerBP (self):
        psetsPerBP = self._get_bridge_field(header.RM_PartitionPsetsPerBP, c_int)
        return psetsPerBP.value
    
    psetsPerBP = property(_get_psetsPerBP)
    
    def _get_Usersnum (self):
        Usersnum = self._get_bridge_field(header.RM_PartitionUsersNum, c_int)
        return Usersnum.value
    
    Usersnum = property(_get_Usersnum)
    
    def _get_Usershead (self):
        return self._get_bridge_field(header.RM_PartitionFirstUser, c_char_p)
    
    Usershead = property(_get_Usershead)
    
    def _get_Userstail (self):
        return self._get_bridge_field(header.RM_PartitionNextUser, c_char_p)
    
    Userstail = property(_get_Userstail)
    
    def _get_NCnum (self):
        NCnum = self._get_bridge_field(header.RM_PartitionNodeCardNum, c_int)
        return NCnum.value
    
    NCnum = property(_get_NCnum)
    
    def _get_NChead (self):
        return self._get_bridge_field(header.RM_PartitionFirstNodeCard, header.rm_element_t)
    
    NChead = property(_get_NChead)
    
    def _get_NCtail (self):
        return self._get_bridge_field(header.RM_PartitionNextNodeCard, header.rm_element_t)
    
    NCtail = property(_get_NCtail)


class BasePartition (BGDevice):
    
    def __init__ (self, *args, **kwargs):
        BGDevice.__init__(self, *args, **kwargs)
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_BPID, header.rm_bp_id_t)
        return id.value
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_bridge_field(header.RM_BPState, header.rm_BP_state_t)
        return header.RM_BPStateEnum[state.value]
    
    state = property(_get_state)
    
    def _get_location (self):
        location = self._get_bridge_field(header.RM_BPLoc, header.rm_location_t)
        return dict(X=location.X, Y=location.Y, Z=location.Z)
    
    location = property(_get_location)
    
    def _get_partid (self):
        partid = self._get_bridge_field(header.RM_BPPartID, header.pm_partition_id_t)
        return partid.value
    
    partid = property(_get_partid)
    
    def _get_partstate (self):
        partstate = self._get_bridge_field(header.RM_BPPartState, header.rm_partition_state_t)
        return header.RM_PartitionStateEnum[partstate.value]
    
    partstate = property(_get_partstate)
    
    def _get_sdb (self):
        sdb = self._get_bridge_field(header.RM_BPSDB, c_int)
        return sdb.value != 0
    
    sdb = property(_get_sdb)
    
    def _get_sd (self):
        sd = self._get_bridge_field(header.RM_BPSD, c_int)
        return sd.value != 0
    
    sd = property(_get_sd)
    
    def _get_computenodememory (self):
        sd = self._get_bridge_field(header.RM_BPComputeNodeMemory, header.rm_BP_computenode_memory_t)
        return header.RM_ComputenodeMemoryEnum[sd.value]
    
    computenodememory = property(_get_computenodememory)


class PSet (BGDevice):
    pass


class PartitionUsers (BGDevice):
    
    def _get_name (self):
        name = _get_bridge_field(header.RM_PartitionUserName, c_char_p)
        return name.value

    name = property(_get_name)


class NodeCard (BGDevice):
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_NodeCardID, header.rm_nodecard_id_t)
        return id.value
    
    id = property(_get_id)
    
    def _get_quarter (self):
        quarter = self._get_bridge_field(header.RM_NodeCardQuarter, header.rm_quarter_t)
        return header.RM_QuarterEnum[quarter.value]
    
    quarter = property(_get_quarter)
    
    def _get_cardstate (self):
        cardstate = self._get_bridge_field(header.RM_NodeCardState, header.rm_nodecard_state_t)
        return header.RM_NodeCardStateEnum[cardstate.value]
    
    cardstate = property(_get_cardstate)
    
    def _get_cardionodes (self):
        cardionodes = self._get_bridge_field(header.RM_NodeCardIONodes, c_int)
        return cardionodes.value
    
    cardionodes = property(_get_cardionodes)
    
    def _get_cardpartid (self):
        cardpartid = self._get_bridge_field(header.RM_NodeCardPartID, header.pm_partition_id_t)
        return cardpartid.value
    
    cardpartid = property(_get_cardionodes)
    
    def _get_cardpartstate (self):
        cardpartstate = self._get_bridge_field(header.RM_NodeCardPartState, header.pm_partition_state_t)
        return cardpartstate.value
    
    cardpartid = property(_get_cardionodes)


class Switch (BGDevice):
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_SwitchID, header.rm_switch_id_t)
        return id.value
    
    id = property(_get_id)


class Port (BGDevice):
    
    def _get_component (self):
        component = self._get_bridge_field(header.RM_PortComponentID, header.rm_component_id_t)
        return component.value
    
    component = property(_get_component)
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_PortID, header.rm_port_id_t)
        return id.value


class Wire (BGDevice):
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_WireID, header.rm_wire_id_t)
        return id.value
    
    id = property(_get_id)
    
    def _get_state (self):
        state = self._get_bridge_field(header.RM_WireState, header.rm_wire_state_t)
        return state.value
    
    state = property(_get_state)
    
    def _get_src (self):
        src = self._get_bridge_field((header.RM_WireFromPort, header.rm_element_t))
        return Port(src)
    
    src = property(_get_src)
    
    def _get_dest (self):
        dest = self._get_bridge_field(header.RM_WireToPort, header.rm_element_t)
        return Port(dest)
    
    dest = property(_get_dest)
    
    def _get_partition (self):
        partition = self._get_bridge_field(header.RM_WirePartID, header.pm_partition_id_t)
        return partition.value
    
    partition = property(_get_partition)
    

class Job (BGDevice):
    
    def _get_id (self):
        id = self._get_bridge_field(header.RM_JobDBJobID, header.db_job_id_t)
        return id.value
    
    id = property(_get_id)
    
    def _get_pid (self):
        pid = self._get_bridge_field(header.RM_JobID, None, header.jm_job_id_t)
        return pid.value
    
    pid = property(_get_pid)
    
    def _get_state (self):
        state = self._get_bridge_field(header.RM_JobState, header.rm_job_state_t)
        return header.RM_JobStateEnum[state.value]
    
    state = property(_get_state)
    
    def _get_executable (self):
        executable = self._get_bridge_field(header.RM_JobExecutable, c_char_p)
        return executable.value
    
    executable = property(_get_executable)
    
    def _get_user (self):
        user = self._get_bridge_field(header.RM_JobUserName, c_char_p)
        return user.value
    
    user = property(_get_user)
    
    def _get_outfile (self):
        outfile = self._get_bridge_field(header.RM_JobOutFile, c_char_p)
        return outfile.value
    
    outfile = property(_get_outfile)
    
    def _get_infile (self):
        infile = self._get_bridge_field(header.RM_JobInFile, c_char_p)
        return invile.value
    
    infile = property(_get_infile)
    
    def _get_errfile (self):
        errfile = self._get_bridge_field(header.RM_JobErrFile, c_char_p)
        return errfile.value
    
    errfile = property(_get_errfile)
    
    def _get_outdir (self):
        outdir = self._get_bridge_field(header.RM_JobOutDir, c_char_p)
        return outdir.value
    
    outdir = property(_get_outdir)
    
    def _get_errtext (self):
        errtext = self._get_bridge_field(header.RM_JobErrText, c_char_p)
        return errtext.value
    
    errtext = property(_get_errtext)
    
    def _get_args (self):
        args = self._get_bridge_field(header.RM_JobArgs, c_char_p)
        return args.value
    
    args = property(_get_args)
    
    def _get_envs (self):
        envs = self._get_bridge_field(header.RM_JobEnvs, c_char_p)
        return envs.value
    
    envs = property(_get_envs)
    
    def _get_inhist (self):
        inhist = self._get_bridge_field(header.RM_JobInHist, c_int)
        return inhist.value != 0
    
    inhist = property(_get_inhist)
    
    def _get_mode (self):
        mode = self._get_bridge_field(header.RM_JobMode, header.rm_job_mode_t)
        return mode.value
    
    mode = property(_get_mode)
    
    def _get_strace (self):
        strace = self._get_bridge_field(header.RM_JobStrace, header.rm_job_strace_t)
        return strace.value
    
    strace = property(_get_strace)
    
    def _get_stdin (self):
        stdin = self._get_bridge_field(header.RM_JobStdinInfo, header.rm_job_stdin_info_t)
        return stdin.value
    
    stdin = property(_get_stdin)
    
    def _get_stdout (self):
        stdout = self._get_bridge_field(header.RM_JobStdoutInfo, header.rm_job_stdout_info_t)
        return stdout.value
    
    stdout = property(_get_stdout)
    
    def _get_stderr (self):
        stderr = self._get_bridge_field(header.RM_JobStderrInfo, header.rm_job_stderr_info_t)
        return stderr.value
    
    stderr = property(_get_stderr)
    
    def _get_starttime (self):
        starttime = self._get_bridge_field((header.RM_JobStartTime, c_char_p))
        return starttime.value
    
    starttime = property(_get_starttime)
    
    def _get_endtime (self):
        endtime = self._get_bridge_field(header.RM_JobEndTime, c_char_p)
        return endtime.value
    
    endtime = property(_get_endtime)
    
    def _get_runtime (self):
        runtime = self._get_bridge_field(header.RM_JobRunTime, header.rm_job_runtime_t)
        return runtime.value
    
    runtime = property(_get_runtime)
    
    def _get_computenodesused (self):
        computenodesused = self._get_bridge_field(header.RM_JobComputeNodesUsed, header.rm_job_computenodes_used_t)
        return computenodesused.value
    
    computenodesused = property(_get_computenodesused)
    
    def _get_exitstatus (self):
        exitstatus = self._get_bridge_field(header.RM_JobExitStatus, header.rm_job_exitstatus_t)
        return exitstatus.value
    
    exitstatus = property(_get_exitstatus)


class JobList (BGDevice, RMGenerator):
    
    def _get_size (self):
        size = self._get_bridge_field(header.RM_JobListSize, c_int)
        return size.value
    
    size = property(_get_size)
    
    def _get_head (self):
        return self._get_bridge_field(header.RM_JobListFirstJob, header.rm_element_t)
    
    head = property(_get_head)
    
    def _get_tail (self):
        return self._get_bridge_field(header.RM_JobListNextJob, header.rm_element_t)

    def __init__(self, flags=4095):
        my_pointer = pointer(header.rm_job_list_t())
        bridge.rm_get_jobs(c_int(flags), byref(my_pointer))
        BGDevice.__init__(self, my_pointer)
        RMGenerator.__init__(self, self, "size", "head", "tail", Job)


class PartList (BGDevice, RMGenerator):
    
    def _get_size (self):
        size = self._get_bridge_field(header.RM_PartListSize, c_int)
        return size.value
    
    size = property(_get_size)
    
    def _get_head (self):
        return self._get_bridge_field(header.RM_PartListFirstPart, header.rm_element_t)
    
    head = property(_get_head)
    
    def _get_tail (self):
        return self._get_bridge_field(header.RM_PartListNextPart, header.rm_element_t)
    
    tail = property(_get_tail)

    def __init__ (self, filter=header.PARTITION_ALL_FLAG):
        self._filter = filter
        my_pointer = pointer(header.rm_partition_list_t())
        bridge.rm_get_partitions(c_int(self._filter), byref(my_pointer))
        BGDevice.__init__(self, my_pointer)
        RMGenerator.__init__(self, self, "size", "head", "tail", Partition)

    def __del__ (self):
        bridge.rm_free_partition_list(self._pointer)

    def reload (self):
        bridge.rm_free_partition_list(self._pointer)
        bridge.rm_get_partitions(c_int(self._filter), byref(self._pointer))
        
        local_bridge = {}
        for bridgepart in self:
            local_bridge.update({bridgepart.id:bridgepart})
