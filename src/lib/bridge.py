import bgl_rm_api
from ctypes import *

bridge = cdll.LoadLibrary('libbglbridge.so.1')

bridge.rm_get_serial.restype = bgl_rm_api.status_t
bridge.rm_set_serial.restype = bgl_rm_api.status_t
bridge.rm_get_BGL.restype = bgl_rm_api.status_t
bridge.rm_get_data.restype = bgl_rm_api.status_t

getvalue = lambda x:x.value
passthru = lambda x:x
boolean = lambda x:x.value != 0

class BGStub(object):
    nocache = []
    def __init__(self, debug=4):
        self.setDebug(debug)
        s = bridge.rm_set_serial(c_char_p("BGL"))
        self.attrcache = {}

    def setDebug(self, level):
        pass

    def fetchattr(self, attr):
        (field, dtype, massage) = self.__attrinfo__[attr]
        data = dtype()
        s = bridge.rm_get_data(self.ptr, field, byref(data))
        if attr not in self.nocache:
            self.attrcache[attr] = massage(data)
        return massage(data)

    def __getattr__(self, attr):
        if attr in self.__attrinfo__:
            # use local cache
            if attr not in self.attrcache:
                return self.fetchattr(attr)
            return self.attrcache[attr]
        else:
            return object.__getattribute__(self, attr)

class LazyRMSet(object):
    def __init__(self, object, sname, hname, tname, cclass):
        self.nocache = [tname]
        self.object = object
        self.sname = sname
        self.hname = hname
        self.tname = tname
        self.cclass = cclass
        self.data = []
        if len(self) > 0:
            head = self.cclass(getattr(self.object, self.hname))
            self.data = [head]
            while len(self.data) < getattr(self.object, self.sname):
                tail = self.cclass(getattr(self.object, self.tname))
                self.data.append(tail)
            
    def __len__(self):
        return getattr(self.object, self.sname)

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, num):
        return self.data.__getitem__(num)

class PreStub(BGStub):
    def __init__(self, pointer):
        self.attrcache = {}
        self.ptr = pointer

class BasePartition(PreStub):
    __attrinfo__ = {'ID': \
                    (bgl_rm_api.RM_BPID, bgl_rm_api.rm_bp_id_t, getvalue),
                    'state': \
                    (bgl_rm_api.RM_BPState, bgl_rm_api.rm_BP_state_t,
                     getvalue),
                    'location':\
                    (bgl_rm_api.RM_BPLoc, bgl_rm_api.rm_location_t,
                     lambda data:{'X':data.X, 'Y':data.Y, 'Z':data.Z}),
                    }
    def __init__(self, pointer):
        self.attrcache = {}
        self.ptr = pointer

class Port(PreStub):
    __attrinfo__ = {'component': \
                    (bgl_rm_api.RM_PortComponentID,
                     bgl_rm_api.rm_component_id_t, getvalue),
                    'id': \
                    (bgl_rm_api.RM_PortID, bgl_rm_api.rm_port_id_t,
                     getvalue),
                    }

class Wire(PreStub):
    __attrinfo__ = {'id': \
                    (bgl_rm_api.RM_WireID, bgl_rm_api.rm_wire_id_t,
                     getvalue),
                    'state': \
                    (bgl_rm_api.RM_WireState, bgl_rm_api.rm_wire_state_t,
                     getvalue),
                    'src': \
                    (bgl_rm_api.RM_WireFromPort, bgl_rm_api.rm_element_t,
                     Port),
                    'dst': \
                    (bgl_rm_api.RM_WireToPort, bgl_rm_api.rm_element_t,
                     Port),
                    'partition': \
                    (bgl_rm_api.RM_WirePartID, bgl_rm_api.pm_partition_id_t,
                     getvalue)
                    }

class Job(PreStub):
    __attrinfo__ = \
                 {'id': \
                  (bgl_rm_api.RM_JobID, bgl_rm_api.jm_job_id_t, getvalue),
                  'partition': \
                  (bgl_rm_api.RM_JobPartitionID,
                   bgl_rm_api.pm_partition_id_t, getvalue),
                  'state': \
                  (bgl_rm_api.RM_JobState, bgl_rm_api.rm_job_state_t,
                   bgl_rm_api.RM_JobStateEnum),
                  'executable': \
                  (bgl_rm_api.RM_JobExecutable, c_char_p, getvalue),
                  'user': \
                  (bgl_rm_api.RM_JobUserName, c_char_p, getvalue),
                  'dbjobid': \
                  (bgl_rm_api.RM_JobDBJobID,
                   bgl_rm_api.db_job_id_t, getvalue),
                  'outfile': \
                  (bgl_rm_api.RM_JobOutFile, c_char_p, getvalue),
                  'infile': \
                  (bgl_rm_api.RM_JobInFile, c_char_p, getvalue),
                  'errfile': \
                  (bgl_rm_api.RM_JobErrFile, c_char_p, getvalue),
                  'outdir': \
                  (bgl_rm_api.RM_JobOutDir, c_char_p, getvalue),
                  'errtext': \
                  (bgl_rm_api.RM_JobErrText, c_char_p, getvalue),
                  'args': \
                  (bgl_rm_api.RM_JobArgs, c_char_p, getvalue),
                  'envs': \
                  (bgl_rm_api.RM_JobEnvs, c_char_p, getvalue),
                  'inhist': \
                  (bgl_rm_api.RM_JobInHist, c_int, boolean),
                  'mode': \
                  (bgl_rm_api.RM_JobMode,
                   bgl_rm_api.rm_job_mode_t, getvalue),
                  'strace': \
                  (bgl_rm_api.RM_JobStrace,
                   bgl_rm_api.rm_job_strace_t, getvalue),
                  'stdin': \
                  (bgl_rm_api.RM_JobStdinInfo,
                   bgl_rm_api.rm_job_stdin_info_t, getvalue),
                  'stdout': \
                  (bgl_rm_api.RM_JobStdoutInfo,
                   bgl_rm_api.rm_job_stdout_info_t, getvalue),
                  'stderr': \
                  (bgl_rm_api.RM_JobStderrInfo,
                   bgl_rm_api.rm_job_stderr_info_t, getvalue),
                  'starttime': \
                  (bgl_rm_api.RM_JobStartTime, c_char_p, getvalue),
                  'endtime': \
                  (bgl_rm_api.RM_JobEndTime, c_char_p, getvalue),
                  'runtime': \
                  (bgl_rm_api.RM_JobRunTime,
                   bgl_rm_api.rm_job_runtime_t, getvalue),
                  'computenodesused': \
                  (bgl_rm_api.RM_JobComputeNodesUsed,
                   bgl_rm_api.rm_job_computenodes_used_t, getvalue),
                  'exitstatus': \
                  (bgl_rm_api.RM_JobExitStatus,
                   bgl_rm_api.rm_job_exitstatus_t, getvalue),
                  }

class Switch(PreStub):
    pass

class PSet(PreStub):
    pass

class Partition(PreStub):
    nocache = ['Switchtail', 'BPtail', 'psetNext']
    __attrinfo__ = \
                 {'id': \
                  (bgl_rm_api.RM_PartitionID,
                   bgl_rm_api.pm_partition_id_t, getvalue),
                  'state': \
                  (bgl_rm_api.RM_PartitionState,
                   bgl_rm_api.rm_partition_state_t,
                   bgl_rm_api.RM_PartitionStateEnum),
                  'BPnum': \
                  (bgl_rm_api.RM_PartitionBPNum, c_int, getvalue),
                  'BPhead': \
                  (bgl_rm_api.RM_PartitionFirstBP, bgl_rm_api.rm_element_t,
                   passthru),
                  'BPtail': \
                  (bgl_rm_api.RM_PartitionNextBP, bgl_rm_api.rm_element_t,
                   passthru),
                  'Switchnum': \
                  (bgl_rm_api.RM_PartitionSwitchNum, c_int, getvalue),
                  'Switchhead': \
                  (bgl_rm_api.RM_PartitionFirstSwitch,
                   bgl_rm_api.rm_element_t, passthru),
                  'Switchtail': \
                  (bgl_rm_api.RM_PartitionNextSwitch,
                   bgl_rm_api.rm_element_t, passthru),
                  'connection': \
                  (bgl_rm_api.RM_PartitionConnection,
                   bgl_rm_api.rm_connection_type_t,
                   bgl_rm_api.RM_ConnectionTypeEnum),
                  'user': \
                  (bgl_rm_api.RM_PartitionUserName, c_char_p, getvalue),
                  'mloader': \
                  (bgl_rm_api.RM_PartitionMloaderImg, c_char_p, getvalue),
                  'blrts': \
                  (bgl_rm_api.RM_PartitionBlrtsImg, c_char_p, getvalue),
                  'linux': \
                  (bgl_rm_api.RM_PartitionLinuxImg, c_char_p, getvalue),
                  'ramdisk': \
                  (bgl_rm_api.RM_PartitionRamdiskImg, c_char_p, getvalue),
                  'mode': \
                  (bgl_rm_api.RM_PartitionMode,
                   bgl_rm_api.rm_partition_mode_t,
                   bgl_rm_api.RM_PartitionModeEnum),
                  'description': \
                  (bgl_rm_api.RM_PartitionDescription, c_char_p, getvalue),
                  'small': \
                  (bgl_rm_api.RM_PartitionSmall, c_int, boolean),
                  'psetsPerBP': \
                  (bgl_rm_api.RM_PartitionPsetsPerBP, c_int, getvalue),
                  }
    def __init__(self, pointer):
        PreStub.__init__(self, pointer)
        self.basePartitions = LazyRMSet(self, 'BPnum', 'BPhead',
                                        'BPtail', BasePartition)
        self.switches = LazyRMSet(self, 'Switchnum', 'Switchhead',
                                        'Switchtail', Switch)

class BG(BGStub):
    __attrinfo__ = {'BPsize': \
                    (bgl_rm_api.RM_BPsize, bgl_rm_api.rm_size3D_t, \
                     lambda data:{'X':data.X, 'Y':data.Y, 'Z':data.Z}),
                    'BPnum': \
                    (bgl_rm_api.RM_BPNum, c_int, getvalue),
                    'BPhead': \
                    (bgl_rm_api.RM_FirstBP, bgl_rm_api.rm_element_t,
                     passthru),
                    'BPtail': \
                    (bgl_rm_api.RM_NextBP, bgl_rm_api.rm_element_t,
                     passthru),
                    'SwitchNum': \
                    (bgl_rm_api.RM_SwitchNum, c_int, getvalue),
                    'WireNum': \
                    (bgl_rm_api.RM_WireNum, c_int, getvalue),
                    'FirstWire': \
                    (bgl_rm_api.RM_FirstWire, bgl_rm_api.rm_element_t,
                     passthru),
                    'NextWire': \
                    (bgl_rm_api.RM_NextWire, bgl_rm_api.rm_element_t,
                     passthru),
                    }
    def __init__(self, debug=1):
        self.ptr = pointer(bgl_rm_api.rm_BGL_t())
        BGStub.__init__(self, debug)
        bridge.rm_get_BGL(byref(self.ptr))
        self.basePartitions = LazyRMSet(self, 'BPnum', 'BPhead',
                                        'BPtail', BasePartition)
        self.wires = LazyRMSet(self, 'WireNum', 'FirstWire', 'NextWire',
                               Wire)

class JobList(BGStub, LazyRMSet):
    __attrinfo__ = \
                 {'size': \
                  (bgl_rm_api.RM_JobListSize, c_int, lambda data:data.value),
                  'head': \
                  (bgl_rm_api.RM_JobListFirstJob, bgl_rm_api.rm_element_t, \
                   lambda data:data),
                  'tail': \
                  (bgl_rm_api.RM_JobListNextJob, bgl_rm_api.rm_element_t, \
                   lambda data:data)}
    nocache = ['tail']

    def __init__(self, flags=4095, debug=1):
        self.ptr = pointer(bgl_rm_api.rm_job_list_t())
        BGStub.__init__(self, debug)
        bridge.rm_get_jobs(c_int(flags), byref(self.ptr))
        LazyRMSet.__init__(self, self, 'size', 'head', 'tail', Job)

class PartList(BGStub,LazyRMSet):
    __attrinfo__ = \
                 {'size': \
                  (bgl_rm_api.RM_PartListSize, c_int, lambda data:data.value),
                  'head': \
                  (bgl_rm_api.RM_PartListFirstPart, bgl_rm_api.rm_element_t, \
                   lambda data:data),
                  'tail': \
                  (bgl_rm_api.RM_PartListNextPart, bgl_rm_api.rm_element_t, \
                   lambda data:data)}
    nocache = ['tail']

    def __init__(self, filter=bgl_rm_api.PARTITION_ALL_FLAG, debug=1):
        self.ptr = pointer(bgl_rm_api.rm_partition_list_t())
        BGStub.__init__(self, debug)
        bridge.rm_get_partitions(c_int(filter), byref(self.ptr))
        LazyRMSet.__init__(self, self, 'size', 'head', 'tail', Partition)

if __name__ == '__main__':
    bg = BG()
    joblist = JobList(debug=4)
    partlist = PartList(debug=4)
    #for wire in bg.wires:
    #    print wire.src.component, wire.src.id, "=>", wire.dst.component, wire.dst.id
    #for job in joblist:
    #    print job.id, job.user, job.partition, job.state
    for part in partlist:
        print [getattr(part, name) for name in \
               ['id', 'description', 'small', 'connection', 'ramdisk']]

    for job in joblist:
        print [getattr(job, name) for name in \
               ['id', 'dbjobid', 'user', 'partition', 'state']]
