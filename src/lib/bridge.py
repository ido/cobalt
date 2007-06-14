import sys
import bgl_rm_api
from ctypes import *

bridge = cdll.LoadLibrary('libbglbridge.so.1')
# saymsg = cdll.LoadLibrary('libsaymessage.so.1')

bridge.rm_get_serial.restype = bgl_rm_api.status_t
bridge.rm_set_serial.restype = bgl_rm_api.status_t
bridge.rm_get_BGL.restype = bgl_rm_api.status_t
bridge.rm_get_data.restype = bgl_rm_api.status_t

getvalue = lambda x:x.value
passthru = lambda x:x
boolean = lambda x:x.value != 0

class BGStub(object):
    nocache = []
    hidden = []
    def __init__(self, debug=4):
        self.setDebug(debug)
        s = bridge.rm_set_serial(c_char_p("BGL"))
        self.attrcache = {}
        self.settable = []

    def setDebug(self, level):
#         saymsg.setSayMessageParams(saymsg.stderr, c_int(level))
        pass

    def fetchattr(self, attr):
        (field, mfield, dtype, massage) = self.__attrinfo__[attr]
        data = dtype()
#         print "going to get %s (%s)" % (attr, field)
        s = bridge.rm_get_data(self.ptr, field, byref(data))
        if s:
            raise Exception, 'problem getting %s' % attr
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

    def setattribute(self, attr, value):
        (field, mfield, dtype, massage) = self.__attrinfo__[attr]
        if mfield == None:
            raise Exception, 'attr %s not settable' % attr
        data = dtype(value)
        s = apply(self.__modify__, (self.id, mfield, data))
        if s:
            raise Exception, 'problem setting %s' % attr
#         s = bridge.rm_set_data(self.ptr, field, byref(data))
#         if attr not in self.nocache:
#             self.attrcache[attr] = massage(data)
#        return massage(data)
        if attr in self.attrcache:
            del self.attrcache[attr]
        return

    def __setattr__(self, attr, value):
        if attr in object.__getattribute__(self, '__attrinfo__'):
            #try setting the attr
            return self.setattribute(attr, value)
        return object.__setattr__(self, attr, value)

    def Visible(self):
        return [item for item in self.__attrinfo__ \
                if item not in self.hidden]

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
    __attrinfo__ = {}
    def __init__(self, pointer):
        self.attrcache = {}
        self.ptr = pointer

class BasePartition(PreStub):
    __attrinfo__ = {'ID': \
                    (bgl_rm_api.RM_BPID, None, bgl_rm_api.rm_bp_id_t, getvalue),
                    'state': \
                    (bgl_rm_api.RM_BPState, None, bgl_rm_api.rm_BP_state_t,
                     getvalue),
                    'location':\
                    (bgl_rm_api.RM_BPLoc, None, bgl_rm_api.rm_location_t,
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
                    (bgl_rm_api.RM_WireID, None, bgl_rm_api.rm_wire_id_t,
                     getvalue),
                    'state': \
                    (bgl_rm_api.RM_WireState, None, bgl_rm_api.rm_wire_state_t,
                     getvalue),
                    'src': \
                    (bgl_rm_api.RM_WireFromPort, None, bgl_rm_api.rm_element_t,
                     Port),
                    'dst': \
                    (bgl_rm_api.RM_WireToPort, None, bgl_rm_api.rm_element_t,
                     Port),
                    'partition': \
                    (bgl_rm_api.RM_WirePartID, None, bgl_rm_api.pm_partition_id_t,
                     getvalue)
                    }

class Job(PreStub):
    __attrinfo__ = \
                 {'id': \
                  (bgl_rm_api.RM_JobID, None, bgl_rm_api.jm_job_id_t, getvalue),
                  'partition': \
                  (bgl_rm_api.RM_JobPartitionID, None,
                   bgl_rm_api.pm_partition_id_t, getvalue),
                  'state': \
                  (bgl_rm_api.RM_JobState, None, bgl_rm_api.rm_job_state_t,
                   bgl_rm_api.RM_JobStateEnum),
                  'executable': \
                  (bgl_rm_api.RM_JobExecutable, None, c_char_p, getvalue),
                  'user': \
                  (bgl_rm_api.RM_JobUserName, None, c_char_p, getvalue),
                  'dbjobid': \
                  (bgl_rm_api.RM_JobDBJobID, None, 
                   bgl_rm_api.db_job_id_t, getvalue),
                  'outfile': \
                  (bgl_rm_api.RM_JobOutFile, None, c_char_p, getvalue),
                  'infile': \
                  (bgl_rm_api.RM_JobInFile, None, c_char_p, getvalue),
                  'errfile': \
                  (bgl_rm_api.RM_JobErrFile, None, c_char_p, getvalue),
                  'outdir': \
                  (bgl_rm_api.RM_JobOutDir, None, c_char_p, getvalue),
                  'errtext': \
                  (bgl_rm_api.RM_JobErrText, None, c_char_p, getvalue),
                  'args': \
                  (bgl_rm_api.RM_JobArgs, None, c_char_p, getvalue),
                  'envs': \
                  (bgl_rm_api.RM_JobEnvs, None, c_char_p, getvalue),
                  'inhist': \
                  (bgl_rm_api.RM_JobInHist, None, c_int, boolean),
                  'mode': \
                  (bgl_rm_api.RM_JobMode, None,
                   bgl_rm_api.rm_job_mode_t, getvalue),
                  'strace': \
                  (bgl_rm_api.RM_JobStrace, None,
                   bgl_rm_api.rm_job_strace_t, getvalue),
                  'stdin': \
                  (bgl_rm_api.RM_JobStdinInfo, None,
                   bgl_rm_api.rm_job_stdin_info_t, getvalue),
                  'stdout': \
                  (bgl_rm_api.RM_JobStdoutInfo, None,
                   bgl_rm_api.rm_job_stdout_info_t, getvalue),
                  'stderr': \
                  (bgl_rm_api.RM_JobStderrInfo, None,
                   bgl_rm_api.rm_job_stderr_info_t, getvalue),
                  'starttime': \
                  (bgl_rm_api.RM_JobStartTime, None, c_char_p, getvalue),
                  'endtime': \
                  (bgl_rm_api.RM_JobEndTime, None, c_char_p, getvalue),
                  'runtime': \
                  (bgl_rm_api.RM_JobRunTime, None,
                   bgl_rm_api.rm_job_runtime_t, getvalue),
                  'computenodesused': \
                  (bgl_rm_api.RM_JobComputeNodesUsed, None,
                   bgl_rm_api.rm_job_computenodes_used_t, getvalue),
                  'exitstatus': \
                  (bgl_rm_api.RM_JobExitStatus, None,
                   bgl_rm_api.rm_job_exitstatus_t, getvalue),
                  }

class Switch(PreStub):
    pass

class PSet(PreStub):
    pass

class Partition(PreStub):
    nocache = ['Switchtail', 'BPtail', 'psetNext']
    __modify__ = bridge.rm_modify_partition
#     __settable__ = ['BPnum', 'Switchnum', 'NodeCardNum',
#                     'FirstNodecard', 'NextNodecard', 'FirstBP',
#                     'NextBP', 'FirstSwitch', 'NextSwitch', 'connection',
#                     'user', 'mloader', 'blrts', 'linux', 'ramdisk',
#                     'description', 'small', 'psetsPerBP']
    hidden = ['id', 'BPnum', 'BPhead', 'BPtail', 'Switchnum', 'Switchhead',
              'Switchtail']
    __attrinfo__ = \
                 {'id': \
                  (bgl_rm_api.RM_PartitionID, None,
                   bgl_rm_api.pm_partition_id_t, getvalue),
                  'state': \
                  (bgl_rm_api.RM_PartitionState, None,
                   bgl_rm_api.rm_partition_state_t,
                   bgl_rm_api.RM_PartitionStateEnum),
                  'BPnum': \
                  (bgl_rm_api.RM_PartitionBPNum, None, c_int, getvalue),
                  'BPhead': \
                  (bgl_rm_api.RM_PartitionFirstBP, None,
                   bgl_rm_api.rm_element_t, passthru),
                  'BPtail': \
                  (bgl_rm_api.RM_PartitionNextBP, None,
                   bgl_rm_api.rm_element_t, passthru),
                  'Switchnum': \
                  (bgl_rm_api.RM_PartitionSwitchNum, None, c_int, getvalue),
                  'Switchhead': \
                  (bgl_rm_api.RM_PartitionFirstSwitch, None,
                   bgl_rm_api.rm_element_t, passthru),
                  'Switchtail': \
                  (bgl_rm_api.RM_PartitionNextSwitch, None,
                   bgl_rm_api.rm_element_t, passthru),
                  'connection': \
                  (bgl_rm_api.RM_PartitionConnection, None,
                   bgl_rm_api.rm_connection_type_t,
                   bgl_rm_api.RM_ConnectionTypeEnum),
                  'user': \
                  (bgl_rm_api.RM_PartitionUserName, bgl_rm_api.RM_MODIFY_Owner,
                   c_char_p, getvalue),
                  'mloader': \
                  (bgl_rm_api.RM_PartitionMloaderImg,
                   bgl_rm_api.RM_MODIFY_MloaderImg, c_char_p, getvalue),
                  'blrts': \
                  (bgl_rm_api.RM_PartitionBlrtsImg,
                   bgl_rm_api.RM_MODIFY_BlrtsImg, c_char_p, getvalue),
                  'linux': \
                  (bgl_rm_api.RM_PartitionLinuxImg,
                   bgl_rm_api.RM_MODIFY_LinuxImg, c_char_p, getvalue),
                  'ramdisk': \
                  (bgl_rm_api.RM_PartitionRamdiskImg,
                   bgl_rm_api.RM_MODIFY_RamdiskImg, c_char_p, getvalue),
                  'mode': \
                  (bgl_rm_api.RM_PartitionMode, None,
                   bgl_rm_api.rm_partition_mode_t,
                   bgl_rm_api.RM_PartitionModeEnum),
                  'description': \
                  (bgl_rm_api.RM_PartitionDescription,
                   bgl_rm_api.RM_MODIFY_Description, c_char_p, getvalue),
                  'small': \
                  (bgl_rm_api.RM_PartitionSmall, None, c_int, boolean),
                  'psetsPerBP': \
                  (bgl_rm_api.RM_PartitionPsetsPerBP, None, c_int, getvalue),
                  }
    
    def __init__(self, pointer):
        PreStub.__init__(self, pointer)
        self.basePartitions = LazyRMSet(self, 'BPnum', 'BPhead',
                                        'BPtail', BasePartition)
        self.switches = LazyRMSet(self, 'Switchnum', 'Switchhead',
                                        'Switchtail', Switch)

class BG(BGStub):
    __attrinfo__ = {'BPsize': \
                    (bgl_rm_api.RM_BPsize, None, bgl_rm_api.rm_size3D_t, \
                     lambda data:{'X':data.X, 'Y':data.Y, 'Z':data.Z}),
                    'BPnum': \
                    (bgl_rm_api.RM_BPNum, None, c_int, getvalue),
                    'BPhead': \
                    (bgl_rm_api.RM_FirstBP, None, bgl_rm_api.rm_element_t,
                     passthru),
                    'BPtail': \
                    (bgl_rm_api.RM_NextBP, None, bgl_rm_api.rm_element_t,
                     passthru),
                    'SwitchNum': \
                    (bgl_rm_api.RM_SwitchNum, None, c_int, getvalue),
                    'WireNum': \
                    (bgl_rm_api.RM_WireNum, None, c_int, getvalue),
                    'FirstWire': \
                    (bgl_rm_api.RM_FirstWire, None, bgl_rm_api.rm_element_t,
                     passthru),
                    'NextWire': \
                    (bgl_rm_api.RM_NextWire, None, bgl_rm_api.rm_element_t,
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
                  (bgl_rm_api.RM_JobListSize, None, c_int,
                   lambda data:data.value),
                  'head': \
                  (bgl_rm_api.RM_JobListFirstJob, None,
                   bgl_rm_api.rm_element_t, lambda data:data),
                  'tail': \
                  (bgl_rm_api.RM_JobListNextJob, None,
                   bgl_rm_api.rm_element_t, lambda data:data)}
    nocache = ['tail']

    def __init__(self, flags=4095, debug=1):
        self.ptr = pointer(bgl_rm_api.rm_job_list_t())
        BGStub.__init__(self, debug)
        bridge.rm_get_jobs(c_int(flags), byref(self.ptr))
        LazyRMSet.__init__(self, self, 'size', 'head', 'tail', Job)

class PartList(BGStub,LazyRMSet):
    __attrinfo__ = \
                 {'size': \
                  (bgl_rm_api.RM_PartListSize, None, c_int,
                   lambda data:data.value),
                  'head': \
                  (bgl_rm_api.RM_PartListFirstPart, None,
                   bgl_rm_api.rm_element_t, lambda data:data),
                  'tail': \
                  (bgl_rm_api.RM_PartListNextPart, None,
                   bgl_rm_api.rm_element_t, lambda data:data)}
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
#         print [getattr(part, name) for name in \
#                ['id', 'description', 'small', 'connection', 'ramdisk']]
        if part.id == 'test32_R000_J102':
            part.description = 'modified by PyBridge'
            part.user = 'nobody'
            break

    for job in joblist:
        print [getattr(job, name) for name in \
               ['id', 'dbjobid', 'user', 'partition', 'state']]
