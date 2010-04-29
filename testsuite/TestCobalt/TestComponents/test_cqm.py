DEBUG_OUTPUT = False
CHECK_ALL_SCRIPTS = False
WHITEBOX_TESTING = True
POLL_INTERVAL = 0.1
ENABLE_LOGGING = True
LOG_FILE = "test_cqm.log"
CQM_CONFIG_FILE_ENTRY = """
[bgsched]

[cqm]
log_dir: /tmp
progress_interval: 0.2
poll_process_groups_interval: 0.2
poll_script_manager_interval: 0.2
"""

# override the cobalt config file before the cqm component is loaded
import Cobalt
import TestCobalt
config_file = Cobalt.CONFIG_FILES[0]
config_fp = open(config_file, "w")
config_fp.write(CQM_CONFIG_FILE_ENTRY)
config_fp.close()

import ConfigParser
from nose.tools import timed, TimeExpired
import os
import os.path
import pwd
import tempfile
import time
from threading import Lock, Condition
import traceback
import types
import unittest
import xmlrpclib

import Cobalt.Components.cqm
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Components.cqm import QueueManager, Signal_Map
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Data import IncrID, Data, DataDict
import Cobalt.Exceptions
from Cobalt.Exceptions import QueueError, ComponentLookupError, DataCreationError, \
    JobRunError, JobPreemptionError, JobDeleteError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Util import Timer

from test_base import TestComponent
from TestCobalt.Utilities.ThreadSupport import *
from TestCobalt.Utilities.Time import timeout

# if logging is enabled, send all cqm and generic component logging to a file
if ENABLE_LOGGING:
    import testsuite
    from TestCobalt.Utilities.Logging import setup_file_logging
    testsuite.DISABLE_LOGGING = False
    setup_file_logging("cqm", LOG_FILE, "DEBUG")
    setup_file_logging("%s %s" % (QueueManager.implementation, QueueManager.name), LOG_FILE, "DEBUG")
    setup_file_logging("generic component", LOG_FILE, "DEBUG")

# define appropriate routine for debugging output
if DEBUG_OUTPUT:
    def debug_print(msg):
        print msg
else:
    def debug_print(*args):
        pass

# setup white box testing module
import TestCobalt.Utilities.WhiteBox
from TestCobalt.Utilities.WhiteBox import whitebox
TestCobalt.Utilities.WhiteBox.WHITEBOX_TESTING = WHITEBOX_TESTING

# get name of user running the tests
try:
    uid = os.getuid()
    username = pwd.getpwuid(uid).pw_name
except:
    username = "nobody"


class TestCQMComponent (TestComponent):
    cqm_jobid = None

    def setup(self):
        TestComponent.setup(self)

    def setup_jobid(self):
        if TestCQMComponent.cqm_jobid != None:
            Cobalt.Components.cqm.cqm_id_gen.set(TestCQMComponent.cqm_jobid)
        
    def teardown(self):
        if Cobalt.Components.cqm.cqm_id_gen != None:
            TestCQMComponent.cqm_jobid = Cobalt.Components.cqm.cqm_id_gen.get()
        TestComponent.teardown(self)


class TestCQMQueueManagement (TestCQMComponent):
    def setup(self):
        TestCQMComponent.setup(self)
        self.cqm = QueueManager()
        self.setup_jobid()

    def teardown(self):
        del self.cqm
        TestCQMComponent.teardown(self)
        
    def test_add_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        
        assert len(self.cqm.Queues) == 1
        assert 'default' in self.cqm.Queues
        assert self.cqm.Queues['default'].tag == 'queue'
        
    def test_get_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
         
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
         
        assert len(results) == 1
        assert results[0].name == 'default'
        
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        
        assert len(results) == 1
        assert results[0].name == 'default'

        results = self.cqm.get_queues([{'tag':"queue", 'name':"*"}])
         
        assert len(results) == 3
 
    def test_del_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'name':"empty"}])
     
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"wally"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"wally"}])

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 2
         
        try:
            self.cqm.del_queues([{'tag':"queue", 'name':"foo"}])
        except Exception:
            pass
        else:
            assert not "able to delete queue with jobs in it"

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"default"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"foo"}])
        assert len(results) == 2

        self.cqm.del_queues([{'tag':"queue", 'name':"foo"}], force=True)             

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"default"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"foo"}])
        assert len(results) == 0
        
        r = self.cqm.del_queues([{'name':"empty"}])
        r = self.cqm.get_queues([{'name':"empty"}])
        assert len(r) == 0
        
    def test_set_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
         
        self.cqm.set_queues([{'tag':"queue", 'name':"default"}], {'state':'running'})
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        assert results[0].state == 'running'

        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])
        self.cqm.set_queues([{'tag':"queue", 'name':"*"}], {'state':'stopped'})
        results = self.cqm.get_queues([{'tag':"queue", 'name':"*"}])
    
        assert results[0].state == results[1].state == results[2].state == 'stopped'
         

class TestCQMJobManagement (TestCQMComponent):
    def setup(self):
        TestCQMComponent.setup(self)
        self.cqm = QueueManager()
        self.setup_jobid()

    def teardown(self):
        del self.cqm
        TestCQMComponent.teardown(self)
        
    def test_add_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])

        try:
            self.cqm.add_jobs([{'queue':"not a valid name"}])
        except QueueError:
            pass
        else:
            assert not "trying to add a job to a non-existent queue should raise an Exception"
        
        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        assert len(results[0].jobs) == 1
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"foo"}])
        assert len(results[0].jobs) == 0
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"bar"}])
        assert len(results[0].jobs) == 0

    def test_get_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])

        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        
        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*"}])
        assert len(results) == 1
        
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo"}])

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*", 'queue':"foo"}])
        assert len(results) == 1

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*", 'queue':"bar"}])
        assert len(results) == 0
    
    def test_del_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
     
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"wally"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"wally"}])

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 2
         
        results = self.cqm.del_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 0

    def test_set_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
    
        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo"}])
        
        self.cqm.set_jobs([{'tag':"job", 'queue':"*"}], {'jobname':"hello"})
        results = self.cqm.get_jobs([{'tag':"job", 'jobname':"hello"}])
        assert len(results) == 2
        
        self.cqm.set_jobs([{'tag':"job", 'queue':"foo"}], {'jobname':"goodbye"})
        results = self.cqm.get_jobs([{'tag':"job", 'jobname':"hello"}])
        assert len(results) == 1

    def test_set_jobid(self):
        # create a local QueueManager so that we can be sure no jobids have been used
        id = Cobalt.Components.cqm.cqm_id_gen.get() + 10
        self.cqm.add_queues([{'name':"default"}])
        self.cqm.set_jobid(id)
        self.cqm.add_jobs([{'queue':"default"}])
        r = self.cqm.get_jobs([{'jobid':id}])
        assert len(r) == 1
    
    def test_move_jobs(self):
        self.cqm.add_queues([{'name':"default"}])
        self.cqm.add_queues([{'name':"foo"}])
        self.cqm.add_queues([{'name':"restricted"}])
        self.cqm.set_queues([{'name':"restricted"}], {'users':"alice"})
        
        self.cqm.add_jobs([{'queue':"default", 'jobname':"hello"}])
        
        try:
            self.cqm.set_jobs([{'jobname':"hello"}], {'queue': "jonx"})
        except QueueError:
            pass
        else:
            assert not "moving a job to a non-existent queue should cause an exception"
                                 
        self.cqm.set_jobs([{'jobname':"hello"}], {'queue': "foo"})
        r = self.cqm.get_jobs([{'jobname':"hello", 'queue':"*"}])
        assert len(r) == 1
        assert r[0].queue == "foo"
        
        try:
            self.cqm.set_jobs([{'jobname':"hello"}], {'queue': "restricted"})
        except QueueError:
            pass
        else:
            assert not "a job failing can_queue should prevent the set_jobs from succeeding"
            

class Task (Data):
    required_fields = ['jobid', 'location', 'user', 'cwd', 'executable', 'args', ]
    fields = Data.fields + ["id", "jobid", "location", "size", "mode", "user", "executable", "args", "env", "cwd", "umask", 
        "kernel", "kerneloptions", "cobalt_log_file", "exit_status", "state", ]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.id = spec.get("id")
        self.jobid = spec.get("jobid")
        self.location = spec.get('location') or []
        self.size = spec.get('size')
        self.mode = spec.get('mode', 'co')
        self.user = spec.get('user', "")
        self.executable = spec.get('executable')
        self.args = " ".join(spec.get('args') or [])
        self.env = spec.get('env') or {}
        self.cwd = spec.get('cwd')
        self.umask = spec.get('umask')
        self.kernel = spec.get('kernel')
        self.kerneloptions = spec.get('kerneloptions')
        self.cobalt_log_file = spec.get('cobalt_log_file')

        self.exit_status = None

    def _get_state (self):
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    
    state = property(_get_state)

class TaskDict (DataDict):
    """Default container for tasks.  Keyed by task id. """

    item_cls = None
    key = "id"
    id_gen = IncrID()
    
    # def __init__ (self):
    #     self.id_gen = IncrID()
 
    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if spec.get("id", "*") != "*":
                raise DataCreationError("cannot specify an id")
            spec['id'] = self.id_gen.next()
        return DataDict.q_add(self, specs)

class SimulatedTaskManager (Component):
    """
    A simulated task management component that provides the ability to control the state and actions of the task for the purposes
    of testing other components.  It is expected that this class will be used to build the real components that are exposed via
    XML-RPC.
    """

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.tasks = TaskDict()
        self.excs = {'add':[], 'signal':[], 'wait':[], 'reserve':[]}
        self.ops = []
        self.op_index = 0
        self.__lock = Lock()
        self.__cond = Condition(self.__lock)

    def __raise_pending_exc(self, op_type, *args):
        exc = None
        cb = None
        try:
            self.__lock.acquire()
            if len(self.excs[op_type]) > 0:
                exc, cb = self.excs[op_type].pop(0)
        finally:
            self.__lock.release()
        if cb != None:
            cb(op_type, exc, *args)
        if exc != None:
            op = [op_type, exc]
            op.extend(args)
            self.__op_add(op)
            raise exc

    def __op_add(self, op):
        try:
            self.__lock.acquire()
            self.ops.append(op)
            self.__cond.notify()
        finally:
            self.__lock.release()
        
    def add_tasks(self, specs):
        self.__raise_pending_exc('add', specs)
        tasks = self.tasks.q_add(specs)
        self.__op_add(['add', None, tasks])
        return tasks
    
    def get_tasks(self, specs):
        return self.tasks.q_get(specs)

    def wait_tasks(self, specs):
        self.__raise_pending_exc('wait', specs)
        tasks = [task for task in self.tasks.q_get(specs) if task.exit_status is not None]
        for task in tasks:
            del self.tasks[task.id]
        self.__op_add(['wait', None, tasks])
        return tasks

    def signal_tasks(self, specs, signame = Signal_Map.terminate):
        self.__raise_pending_exc('signal', specs, signame)
        tasks = [task for task in self.tasks.q_get(specs) if task.exit_status is None]
        self.__op_add(['signal', None, tasks, signame])
        return tasks

    def complete_tasks(self, specs, exit_status):
        tasks = self.tasks.q_get(specs)
        for task in tasks:
            task.exit_status = exit_status
        return tasks

    def reserve_resources_until(self, location, duration, jobid):
        self.__raise_pending_exc('reserve')
        self.__op_add(['reserve', None])

    def op_wait(self):
        try:
            self.__lock.acquire()
            while self.op_index == len(self.ops):
                self.__cond.wait(1.0)
            op = self.ops[self.op_index]
            self.op_index += 1
        finally:
            self.__lock.release()
        return op

    def add_exc(self, op_type, exc, cb = None):
        try:
            self.__lock.acquire()
            self.excs[op_type].append([exc, cb])
        finally:
            self.__lock.release()

    def clear_excs(self, op_type):
        try:
            self.__lock.acquire()
            self.excs[op_type] = []
        finally:
            self.__lock.release()

class SystemTask (Task):
    required_fields = Task.required_fields + ['size']
    fields = Task.fields + ["stdin", "stdout", "stderr", "true_mpi_args", ]

    def __init__(self, spec):
        Task.__init__(self, spec)
        self.stdin = spec.get('stdin')
        self.stdout = spec.get('stdout')
        self.stderr = spec.get('stderr')
        self.true_mpi_args = spec.get('true_mpi_args')

class SimulatedSystem (SimulatedTaskManager):
    """
    A simulated system component that provides the ability to control the state and actions of the process groups for the
    purposes of testing other components.
    """
    name = "system"
    implementation = "SimSystem"
    logger = setup_file_logging("%s %s" % (implementation, name), LOG_FILE, "DEBUG")
    
    def __init__(self, *args, **kwargs):
        SimulatedTaskManager.__init__(self, *args, **kwargs)
        self.tasks.item_cls = SystemTask
        
    def add_process_groups(self, specs):
        return self.add_tasks(specs)
    
    add_process_groups = exposed(query(add_process_groups))
    
    def get_process_groups(self, specs):
        return self.get_tasks(specs)

    get_process_groups = exposed(query(get_process_groups))

    def wait_process_groups(self, specs):
        return self.wait_tasks(specs)

    wait_process_groups = exposed(query(wait_process_groups))
    
    def signal_process_groups(self, specs, signame="SIGINT"):
        return self.signal_tasks(specs, signame)

    signal_process_groups = exposed(query(signal_process_groups))

    def reserve_resources_until(self, location, duration, jobid):
        return SimulatedTaskManager.reserve_resources_until(self, location, duration, jobid)

    reserve_resources_until = exposed(reserve_resources_until)

class ScriptTask (Task):
    fields = Task.fields + ["name", "inputfile", "outputfile", "errorfile", "path", ]

    def __init__(self, spec):
        Task.__init__(self, spec)
        self.tag = spec.get("tag", "process-group")
        self.name = spec.get("name", None)
        self.inputfile = spec.pop("inputfile", None)
        self.outputfile = spec.pop("outputfile", None)
        self.errorfile = spec.pop("errorfile", None)
        self.path = spec.pop("path", None)
        
class SimulatedScriptManager (SimulatedTaskManager):
    """
    A simulated script manager component that provides the ability to control the state and actions of the script task for the
    purposes of testing other components.
    """
    name = "script-manager"
    implementation = "SimScript"
    logger = setup_file_logging("%s %s" % (implementation, name), LOG_FILE, "DEBUG")
    
    def __init__(self, *args, **kwargs):
        SimulatedTaskManager.__init__(self, *args, **kwargs)
        self.tasks.item_cls = ScriptTask
        
    def add_jobs(self, specs):
        return self.add_tasks(specs)
    
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs(self, specs):
        return self.get_tasks(specs)

    get_jobs = exposed(query(get_jobs))

    def wait_jobs(self, specs):
        return self.wait_tasks(specs)

    wait_jobs = exposed(query(wait_jobs))
    
    def signal_jobs(self, specs, signame="SIGINT"):
        return self.signal_tasks(specs, signame)

    signal_jobs = exposed(query(signal_jobs))

class BogusException1 (Exception):
    fault_code = Cobalt.Exceptions.fault_code_counter.next()

class BogusException2 (Exception):
    fault_code = Cobalt.Exceptions.fault_code_counter.next()

def cqm_config_file_update(options = {}):
    config_file = Cobalt.CONFIG_FILES[0]
    config_fp = open(config_file, "w")
    config_fp.write(CQM_CONFIG_FILE_ENTRY)
    for option, value in options.iteritems():
        print >>config_fp, "%s: %s" % (option, value)
    config_fp.close()
    config = ConfigParser.ConfigParser()
    config.read(Cobalt.CONFIG_FILES)
    Cobalt.Components.cqm.config = config

def check_output_files(fn_bases, exist = True, fail_msg = None):
    try:
        for fn_base in fn_bases:
            out_fn = "%s.out" % (fn_base,)
            if os.path.exists(out_fn) != exist:
                if fail_msg != None:
                    assert False, "file %s; %s" % (out_fn, fail_msg)
                elif exist:
                    assert False, "file %s does not exist" % (out_fn,)
                else:
                    assert False, "file %s exists and shouldn't" % (out_fn,)
    finally:
        delete_output_files(fn_bases)

def wait_output_files(fn_bases):
    try:
        for fn_base in fn_bases:
            out_fn = "%s.out" % (fn_base,)
            while not os.path.exists(out_fn):
                time.sleep(POLL_INTERVAL)
    finally:
        delete_output_files(fn_bases)

def delete_output_files(fn_bases):
    for fn_base in fn_bases:
        out_fn = "%s.out" % (fn_base,)
        try:
            os.unlink(out_fn)
        except OSError:
            pass

def create_input_files(fn_bases):
    for fn_base in fn_bases:
        sh_fn = "%s.sh" % (fn_base,)
        in_fn = "%s.in" % (fn_base,)
        fp = open(in_fn, "w")
        print >>fp, "input to %s" % (sh_fn,)
        fp.close()

def delete_input_files(fn_bases):
    for fn_base in fn_bases:
        in_fn = "%s.in" % (fn_base,)
        try:
            os.unlink(in_fn)
        except OSError:
            pass

def create_touch_scripts(num_scripts):
    fn_bases = []
    for n in xrange(0, num_scripts):
        (fd, fn) = tempfile.mkstemp("_touch.sh", "test_cqm_")
        fn_base = fn[0:-3]
        fn_bases += [fn_base]
        sh_fn = fn
        out_fn = "%s.out" % (fn_base,)
        fp = os.fdopen(fd, "w")
        fp.write("""\
#!/bin/sh
touch %(out_fn)s
echo "%(out_fn)s has been created"
""" % {'out_fn':out_fn})
        fp.close()
        os.chmod(sh_fn, 0700)
    delete_output_files(fn_bases)
    return fn_bases

def create_wait_scripts(num_scripts, timeout):
    fn_bases = []
    for n in xrange(0, num_scripts):
        (fd, fn) = tempfile.mkstemp("_wait.sh", "test_cqm_")
        fn_base = fn[0:-3]
        fn_bases += [fn_base]
        sh_fn = fn
        in_fn = "%s.in" % (fn_base,)
        out_fn = "%s.out" % (fn_base,)
        fp = os.fdopen(fd, "w")
        fp.write("""\
#!/bin/sh
touch %(out_fn)s
echo "%(out_fn)s has been created"
n=0
echo "waiting for %(in_fn)s to be created"
while test ! -f %(in_fn)s ; do
    sleep 0.2
    n=`expr $n + 1`
    if test $n -gt %(timeout)d ; then
        rm %(out_fn)s
        echo "TIMEOUT: %(in_fn)s not found after 60 seconds" >&2
        exit 1
    fi
done
echo "%(in_fn)s now exists; deleting it"
rm %(in_fn)s
""" % {'in_fn':in_fn, 'out_fn':out_fn, 'timeout':timeout})
        fp.close()
        os.chmod(sh_fn, 0700)
    delete_input_files(fn_bases)
    delete_output_files(fn_bases)
    return fn_bases

def delete_scripts(fn_bases):
    for fn_base in fn_bases:
        sh_fn = "%s.sh" % (fn_base,)
        try:
            os.unlink(sh_fn)
        except OSError:
            pass

def get_script_filenames(fn_bases):
    return ["%s.sh" % (fn_base,) for fn_base in fn_bases]

class CQMIntegrationTestBase (TestCQMComponent):
    taskman = None

    def setup(self):
        TestCQMComponent.setup(self)
        self.slp = TimingServiceLocator()

    def setup_cqm(self):
        self.qm = QueueManager()
        self.qm_thr = ComponentProgressThread(self.qm)
        self.qm_thr.start()
        try:
            self.cqm = ComponentProxy("queue-manager")
        except ComponentLookupError:
            assert not "failed to connect to the queue manager component"
        queues = self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        assert len(queues) == 1
        self.setup_jobid()

    def teardown(self):
        self.qm_thr.stop()
        del self.qm_thr
        del self.qm
        del self.slp
        TestCQMComponent.teardown(self)

    def get_job_query_spec(self, spec = {}):
        query_spec = {}
        query_spec.update(spec)
        if not spec.has_key("jobid"):
            if hasattr(self, "jobid"):
                query_spec['jobid'] = self.jobid
            else:
                query_spec['jobid'] = "*"
        default_query_attrs = ['is_active', 'is_runnable', 'has_completed', 'preemptable', 'user_hold', 'admin_hold', 'state']
        if WHITEBOX_TESTING:
            default_query_attrs.append('sm_state')
        for attr in default_query_attrs:
            if not spec.has_key(attr):
                query_spec[attr] = "*"
        return query_spec

    def assert_job_state(self, state):
        assert self.job['state'] == state, "expected job state to be \"%s\"; actual job state is \"%s\"" % \
            (state, self.job['state'],)

    def assert_job_sm_state(self, state):
        if WHITEBOX_TESTING:
            assert self.job['sm_state'] == state, "expected job sm_state to be \"%s\"; actual job sm_state is \"%s\"" % \
                (state, self.job['sm_state'],)

    def assert_jobid(self):
        assert self.job['jobid'] == self.jobid, "expected job id to be '%s'; actual job id is '%s'" % \
            (self.jobid, self.job['jobid'])

    def assert_next_op(self, op_type, exc_cls = types.NoneType):
        op = self.taskman.op_wait()
        assert op != None, "no operation found"
        assert op[0] == op_type, "expected op type of '%s'; actual op type is '%s'" % (op_type, op[0])
        exc = op[1]
        assert isinstance(exc, exc_cls), "expected exception type to be '%s'; actual type is '%s'" %  (exc_cls, type(exc))
        return op

    def assert_next_task_op(self, op_type, exc_cls = types.NoneType):
        op = self.assert_next_op(op_type, exc_cls)
        if exc_cls == types.NoneType:
            tasks = op[2]
            assert len(tasks) == 1
            assert tasks[0].id == self.taskid
        else:
            specs = op[2]
            assert len(specs) == 1
            spec = specs[0]
            assert spec['id'] == "*" or spec['id'] == self.taskid
        return op

    def job_get_state(self, get_spec = {}, assert_spec = {}, no_job_ok = False):
        job_spec = {}
        job_spec.update(get_spec)
        for attr, val in assert_spec.iteritems():
            if not job_spec.has_key(attr):
                job_spec[attr] = "*"
        jobs = self.cqm.get_jobs([self.get_job_query_spec(job_spec)])
        num_jobs = len(jobs)
        assert num_jobs < 2, "More than one job was returned"
        assert no_job_ok or num_jobs == 1, "Job %s not found in queue" % (self.jobid,)
        if num_jobs > 0:
            self.job = jobs[0]
            self.assert_jobid()
            if not WHITEBOX_TESTING and assert_spec.has_key("sm_state"):
                assert_spec = assert_spec.copy()
                del assert_spec['sm_state']
            for attr, val in assert_spec.iteritems():
                assert self.job[attr] == val, "expected job attribute '%s' to be '%s'; actual value is '%s'" % \
                    (attr, val, self.job[attr])
            return True
        else:
            return False

    def job_add(self, add_spec = {}, get_spec = {}, job_name = None):
        if job_name == None:
            job_name = traceback.extract_stack()[-2][2]
        job_spec = {'queue':"default", 'user':username, 'jobname':job_name, 'jobid':"*"}
        job_spec.update(add_spec)
        for attr, val in self.default_job_spec.iteritems():
            if not job_spec.has_key(attr):
                job_spec[attr] = val
        jobs = self.cqm.add_jobs([job_spec])
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job was not successfully added to the queue"
        self.job = jobs[0]
        self.jobid = self.job['jobid']

        self.job_get_state(get_spec, \
            assert_spec = {'is_active':False, 'is_runnable':True, 'has_completed':False, 'state':"queued"})

    def job_update(self, spec, updates):
        query_spec = {}
        query_spec.update(spec)
        for key, value in updates.iteritems():
            if not query_spec.has_key(key):
                query_spec[key] = "*"
        jobs = self.cqm.set_jobs([self.get_job_query_spec(query_spec)], updates)
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()

    def job_user_hold(self, orig_hold = "*", new_hold = True):
        jobs = self.cqm.set_jobs([self.get_job_query_spec({'user_hold':orig_hold})], {'user_hold':True})
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['user_hold'] == new_hold

    def job_user_release(self, orig_hold = "*", new_hold = False):
        jobs = self.cqm.set_jobs([self.get_job_query_spec({'user_hold':orig_hold})], {'user_hold':False})
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['user_hold'] == new_hold

    def job_admin_hold(self, orig_hold = "*", new_hold = True):
        jobs = self.cqm.set_jobs([self.get_job_query_spec({'admin_hold':orig_hold})], {'admin_hold':True})
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['admin_hold'] == new_hold

    def job_admin_release(self, orig_hold = "*", new_hold = False):
        jobs = self.cqm.set_jobs([self.get_job_query_spec({'admin_hold':orig_hold})], {'admin_hold':False})
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['admin_hold'] == new_hold

    def job_run(self, location):
        jobs = self.cqm.run_jobs([self.get_job_query_spec()], location)
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['is_active'] == True
        assert self.job['is_runnable'] == False
        assert self.job['has_completed'] == False

    def job_running_wait(self):
        while True:
            self.job_get_state()
            if self.job['state'] == "running":
                break
            assert self.job['is_active'] == True
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            self.assert_job_state("starting")

        tasks = self.taskman.get_tasks([{'jobid':self.jobid, 'id':"*", 'state':"*"}])
        assert len(tasks) < 2, "More than one task was returned while looking for job %s" % (self.jobid,)
        assert len(tasks) == 1, "Task associated with job %s not found" % (self.jobid,)
        self.task = tasks[0]
        assert self.task.jobid == self.jobid, "expected job id is %s; actual job id is %s" % (self.jobid, self.task.jobid)
        assert self.task.state == 'running'
        self.taskid = self.task.id

    def job_preempt(self, user = None, force = False):
        jobs = self.cqm.preempt_jobs([self.get_job_query_spec()], user, force)
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()
        assert self.job['is_active'] == True
        assert self.job['is_runnable'] == False
        assert self.job['has_completed'] == False

    def job_preempting_wait(self):
        while True:
            self.job_get_state()
            if self.job['state'] == "preempting":
                assert self.job['is_active'] == True
                assert self.job['is_runnable'] == False
                assert self.job['has_completed'] == False
                break
            assert self.job['is_active'] == True
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            time.sleep(POLL_INTERVAL)

    def job_preempted_wait(self):
        while True:
            self.job_get_state()
            if self.job['is_active'] == False:
                assert self.job['state'] == "preempted" or self.job['state'][-5:] == "_hold"
                assert self.job['has_completed'] == False
                break
            assert self.job['is_active'] == True
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            time.sleep(POLL_INTERVAL)

    def job_kill(self, force = False, user = None, signame = Signal_Map.terminate):
        jobs = self.cqm.del_jobs([self.get_job_query_spec()], force, user, signame)
        assert len(jobs) < 2, "More than one job was returned"
        assert len(jobs) == 1, "Job %s not found in queue" % (self.jobid,)
        self.job = jobs[0]
        self.assert_jobid()

    def task_finished(self, exit_code):
        tasks = self.taskman.complete_tasks([{'id':self.taskid}], exit_code)
        assert len(tasks) < 2, "More than one task was returned while attempting to complete job %s" % (self.jobid,)
        assert len(tasks) == 1, "Task %s associated with job %s failed to complete" % (self.taskid, self.jobid)
        self.task = tasks[0]
        assert self.task.id == self.taskid, "expected task id is %s; actual task id is %s" % (self.taskid, self.task.id)
        assert self.task.jobid == self.jobid, "expected job id is %s; actual job id is %s" % (self.jobid, self.task.jobid)

    def job_finished_wait(self):
        while True:
            found_job = self.job_get_state(no_job_ok = True)
            if found_job == False:
                break
            assert self.job['is_runnable'] == False, "job is runnable and shouldn't be; state='%s'" % (self.job['state'],)
            assert (self.job['is_active'] == True and self.job['has_completed'] == False) or \
                self.job['is_active'] == False and self.job['has_completed'] == True, \
                "unexpected state: is_active=%s, has_completed=%s" % (self.job['is_active'], self.job['has_completed'])
            time.sleep(POLL_INTERVAL)

    def job_exec_driver(
            self, spec = {}, config_opts = {}, job_queued = None, job_pretask = None, resource_pretask = None, exec_task = True,
            task_run = None, task_wait = None, task_active = None, task_complete = None, num_preempts = 0, job_preempt = None,
            job_preempting = None, preempt_posttask = None, job_preempted = None, preempt_pretask = None, resource_posttask = None,
            job_posttask = None, job_complete = None, script_check = CHECK_ALL_SCRIPTS, wait_script_timeout = 60):

        def _task_run(preempt = False):
            if task_wait != None:
                debug_print("JOB_EXEC: task_wait")
                task_wait()
            else:
                debug_print("JOB_EXEC: task_wait (default)")
                self.job_running_wait()
                self.assert_next_task_op('add')
            if task_active != None:
                debug_print("JOB_EXEC: task_active")
                task_active()
            if not preempt:
                if task_complete != None:
                    debug_print("JOB_EXEC: task_complete")
                    task_complete()
                else:
                    debug_print("JOB_EXEC: task_complete (default)")
                    self.task_finished(0)
                    self.assert_next_task_op('wait')

        try:
            if task_run == None:
                task_run = _task_run

            add_spec = {}
            add_spec.update(spec)
            if num_preempts > 0:
                add_spec['preemptable'] = True

            syncs = []
            configs = {}
            configs.update(config_opts)
            if job_pretask != None or script_check:
                self.job_prescripts = create_wait_scripts(1, wait_script_timeout)
                configs['job_prescripts'] = ":".join(get_script_filenames(self.job_prescripts))
                syncs += self.job_prescripts
            if resource_pretask != None or preempt_pretask != None or script_check:
                self.resource_prescripts = create_wait_scripts(1, wait_script_timeout)
                configs['resource_prescripts'] = ":".join(get_script_filenames(self.resource_prescripts))
                syncs += self.resource_prescripts
            if resource_posttask != None or preempt_posttask != None or script_check:
                self.resource_postscripts = create_wait_scripts(1, wait_script_timeout)
                configs['resource_postscripts'] = ":".join(get_script_filenames(self.resource_postscripts))
                syncs += self.resource_postscripts
            if job_posttask != None or script_check:
                self.job_postscripts = create_wait_scripts(1, wait_script_timeout)
                configs['job_postscripts'] = ":".join(get_script_filenames(self.job_postscripts))
                syncs += self.job_postscripts

            test_name = traceback.extract_stack()[-2][2]
            self.logger.debug("job_exec_info executing test '%s'" % (test_name,))
            cqm_config_file_update(configs)
            self.job_add(add_spec, job_name = test_name)
            self.assert_job_state("queued")
            if job_queued != None:
                debug_print("JOB_EXEC: job_queued")
                job_queued()

            if exec_task:
                preempt_count = 0
                resource_postscript_needed = True

                self.job_run(["R00"])

                if hasattr(self, 'job_prescripts'):
                    debug_print("JOB_EXEC: job_prescripts")
                    wait_output_files(self.job_prescripts)
                    self.job_get_state(assert_spec = {'state':"starting"})
                    if job_pretask != None:
                        debug_print("JOB_EXEC: job_pretask")
                        job_pretask()
                    create_input_files(self.job_prescripts)

                if hasattr(self, 'resource_prescripts'):
                    debug_print("JOB_EXEC: resource_prescripts")
                    wait_output_files(self.resource_prescripts)
                    self.job_get_state(assert_spec = {'state':"starting"})
                    if resource_pretask != None:
                        debug_print("JOB_EXEC: resource_pretask")
                        resource_pretask()
                    create_input_files(self.resource_prescripts)

                while True:
                    if preempt_count < num_preempts:
                        task_run(preempt = True)

                        preempt_count += 1
                        if job_preempt:
                            debug_print("JOB_EXEC: job_preempt")
                            rc = job_preempt()
                            if rc == False:
                                break
                        else:
                            debug_print("JOB_EXEC: job_preempt (default)")
                            self.job_preempt()
                            self.assert_next_task_op('signal')

                        if job_preempting:
                            debug_print("JOB_EXEC: job_preempting")
                            rc = job_preempting()
                            if rc == False:
                                break
                        else:
                            debug_print("JOB_EXEC: job_preempting (default)")
                            self.job_preempting_wait()
                            self.task_finished(0)
                            self.assert_next_task_op('wait')

                        rc = True
                        resource_postscript_needed = False
                        if hasattr(self, 'resource_postscripts'):
                            debug_print("JOB_EXEC: resource_postscripts (preempt)")
                            wait_output_files(self.resource_postscripts)
                            self.job_get_state(assert_spec = {'state':"preempting"})
                            if preempt_posttask != None:
                                debug_print("JOB_EXEC: preempt_posttask")
                                rc = preempt_posttask()
                            create_input_files(self.resource_postscripts)
                        resource_postscript_needed = False
                        if rc == False:
                            break

                        self.job_preempted_wait()
                        if job_preempted:
                            debug_print("JOB_EXEC: job_preempted")
                            rc = job_preempted()
                            if rc == False:
                                break

                        self.job_run(["R%02d" % (preempt_count,)])

                        rc = True
                        resource_postscript_needed = True
                        if hasattr(self, 'resource_prescripts'):
                            debug_print("JOB_EXEC: resource_prescripts (preempt)")
                            wait_output_files(self.resource_prescripts)
                            self.job_get_state(assert_spec = {'state':"starting"})
                            if preempt_pretask != None:
                                debug_print("JOB_EXEC: preempt_pretask")
                                rc = preempt_pretask()
                            create_input_files(self.resource_prescripts)
                        if rc == False:
                            break
                    else:
                        task_run(preempt = False)
                        break
                if hasattr(self, 'resource_postscripts') and resource_postscript_needed:
                    debug_print("JOB_EXEC: resource_postscripts")
                    wait_output_files(self.resource_postscripts)
                    self.job_get_state(assert_spec = {'state':"exiting"})
                    if resource_posttask != None:
                        debug_print("JOB_EXEC: resource_posttask")
                        resource_posttask()
                    create_input_files(self.resource_postscripts)
                if hasattr(self, 'job_postscripts'):
                    debug_print("JOB_EXEC: job_postscripts")
                    wait_output_files(self.job_postscripts)
                    self.job_get_state(assert_spec = {'state':"exiting"})
                    if job_posttask != None:
                        debug_print("JOB_EXEC: job_posttask")
                        job_posttask()
                    create_input_files(self.job_postscripts)
            if job_complete != None:
                debug_print("JOB_EXEC: job_complete")
                job_complete()
            else:
                debug_print("JOB_EXEC: job_complete (default)")
                self.job_finished_wait()
        finally:
            if hasattr(self, "job_prescripts"):
                del self.job_prescripts
            if hasattr(self, "resource_prescripts"):
                del self.resource_prescripts
            if hasattr(self, "resource_postscripts"):
                del self.resource_postscripts
            if hasattr(self, "job_postscripts"):
                del self.job_postscripts
            if len(syncs) > 0:
                delete_scripts(syncs)
                delete_input_files(syncs)
                delete_output_files(syncs)

    @timeout(10)
    def test_job_exec_driver(self):
        def _job_queued():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _job_queued")
        def _job_pretask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _job_pretask")
        def _resource_pretask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _resource_pretask")
        def _task_active():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _task_active")
        def _preempt_posttask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _preempt_postask")
        def _job_preempted():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _job_preempted")
        def _preempt_pretask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _preempt_pretask")
        def _resource_posttask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _resource_posttask")
        def _job_posttask():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _job_posttask")
        def _job_complete():
            self.test_calls += [traceback.extract_stack()[-1][2]]
            debug_print("TEST_JOB_EXEC: _job_complete")
            self.job_finished_wait()
        self.test_calls = []
        self.job_exec_driver(
            num_preempts = 1, job_queued = _job_queued, job_pretask = _job_pretask, resource_pretask = _resource_pretask,
            task_active = _task_active, preempt_posttask = _preempt_posttask, job_preempted = _job_preempted,
            preempt_pretask = _preempt_pretask, resource_posttask = _resource_posttask, job_posttask = _job_posttask,
            job_complete = _job_complete)
        assert self.test_calls == ["_job_queued", "_job_pretask", "_resource_pretask", "_task_active", "_preempt_posttask", 
                                   "_job_preempted", "_preempt_pretask", "_task_active", "_resource_posttask", "_job_posttask",
                                   "_job_complete"]
        del self.test_calls

    #
    # tests for non-preemptable jobs
    #
    @timeout(10)
    def test_nonpreempt_queued__run(self):
        # a simple run
        self.job_exec_driver()

    @timeout(10)
    def test_nonpreempt_queued__run_failed(self):
        # attempting to start a new task; if the attempt fails, cqm should try again
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"))
            self.taskman.add_exc('add', BogusException2("error2"))
        def _task_wait():
            self.job_running_wait()
            self.assert_next_task_op('add', BogusException1)
            self.assert_next_task_op('add', BogusException2)
            self.assert_next_task_op('add')
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait)

    @timeout(10)
    def test_nonpreempt_queued__hold_user(self):
        # the job is queued; test user holds and releases
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            self.assert_job_state("user_hold")
            self.job_user_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_queued__hold_admin(self):
        # the job is queued; test admin holds and releases
        def _job_queued():
            self.assert_job_state("queued")
            self.job_admin_hold()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            self.assert_job_state("admin_hold")
            self.job_admin_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_queued__release(self):
        # the job is queued; attempts to release the job should be ignored (and a warning message added to the logs)
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
            self.job_admin_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_queued__kill(self):
        # kill a queued job
        def _job_queued():
            self.assert_job_state("queued")
            self.job_kill()
            self.assert_job_state("done")
        self.job_exec_driver(job_queued = _job_queued, exec_task = False)

    @timeout(10)
    def test_nonpreempt_queued__force_kill(self):
        # forcibly kill a queued job
        def _job_queued():
            self.assert_job_state("queued")
            self.job_kill(force = True)
        self.job_exec_driver(job_queued = _job_queued, exec_task = False)

    @timeout(10)
    def test_nonpreempt_queued__preempt(self):
        # the job is queued; attempts to preempt the job should result in an error
        def _job_queued():
            try:
                self.job_preempt()
                assert False, "attempt to preempt while in the queued state should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
            self.job_get_state(assert_spec = {'state':'queued'})
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_queued__walltime_adjustment(self):
        # change the walltime of a queued job
        def _job_queued():
            self.job_update({}, {'walltime':new_walltime})
            assert self.job['walltime'] == new_walltime
        def _task_active():
            self.job_get_state(assert_spec = {'walltime':new_walltime})
        new_walltime = 903245832
        self.job_exec_driver(job_queued = _job_queued, task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_hold_both(self):
        # test placing both user and admin hold simultaneously starting from a queued state
        def _job_queued():
            self.assert_job_state("queued")
            self.job_admin_hold()
            self.assert_job_state("admin_hold")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            self.job_admin_release()
            self.assert_job_state("user_hold")
            self.job_user_release()
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            self.job_admin_hold()
            self.assert_job_state("user_hold")
            self.job_user_release()
            self.assert_job_state("admin_hold")
            self.job_admin_release()
            self.assert_job_state("queued")
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_hold_repeated(self):
        # try to place a hold that's already been placed
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            self.assert_job_state("user_hold")
            self.job_user_hold()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == False
            assert self.job['has_completed'] == False
            self.assert_job_state("user_hold")
            self.job_user_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
            self.job_user_release()
            assert self.job['is_active'] == False
            assert self.job['is_runnable'] == True
            assert self.job['has_completed'] == False
            self.assert_job_state("queued")
        self.job_exec_driver(job_queued = _job_queued)

    @timeout(10)
    def test_nonpreempt_hold__run(self):
        # the job is in the hold state; attempting to run the job should fail
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
        try:
            self.job_exec_driver(job_queued = _job_queued)
            assert False, "attempt to run while in a hold state should fail"
        except xmlrpclib.Fault, e:
            assert e.faultCode == JobRunError.fault_code

    @timeout(10)
    def test_nonpreempt_hold__kill(self):
        # the job is in the hold state; killing the job should result in immediate termination
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            self.job_kill()
            self.assert_job_state("done")
        self.job_exec_driver(job_queued = _job_queued, exec_task = False)


    @timeout(10)
    def test_nonpreempt_hold__force_kill(self):
        # the job is in the hold state; forcibly killing the job should result in immediate termination
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            self.job_kill(force = True)
        self.job_exec_driver(job_queued = _job_queued, exec_task = False)


    @timeout(10)
    def test_nonpreempt_hold__preempt(self):
        # the job is in the hold state; attempts to preempt the job should fail
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            try:
                self.job_preempt()
                assert False, "attempt to preempt while in a hold state should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
            self.job_kill()
            self.assert_job_state("done")
        self.job_exec_driver(job_queued = _job_queued, exec_task = False)

    @timeout(10)
    def test_nonpreempt_hold__walltime_adjustment(self):
        # change the walltime of a queued job
        def _job_queued():
            self.assert_job_state("queued")
            self.job_user_hold()
            self.assert_job_state("user_hold")
            self.job_update({}, {'walltime':new_walltime})
            assert self.job['walltime'] == new_walltime
            self.job_user_release()
        def _task_active():
            self.job_get_state(assert_spec = {'walltime':new_walltime})
        new_walltime = 903245832
        self.job_exec_driver(job_queued = _job_queued, task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_starting__hold(self):
        # the job is starting; attempts to place a hold on a non-preemptable job should be ignored
        def _pretask():
            self.job_user_hold(new_hold = False)
            self.assert_job_state("starting")
            self.job_admin_hold(new_hold = False)
            self.assert_job_state("starting")
        self.job_exec_driver(job_pretask = _pretask, resource_pretask = _pretask)

    @timeout(10)
    def test_nonpreempt_starting__release(self):
        # the job is starting; attempts to release a hold on a non-preemptable job should be ignored
        def _pretask():
            self.job_user_release(new_hold = False)
            self.assert_job_state("starting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("starting")
        self.job_exec_driver(job_pretask = _pretask, resource_pretask = _pretask)

    @timeout(10)
    def test_nonpreempt_starting__run(self):
        # the job is starting; attempting to run the job should fails
        def _pretask():
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is starting should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
        self.job_exec_driver(job_pretask = _pretask)
        self.job_exec_driver(resource_pretask = _pretask)

    @timeout(10)
    def test_nonpreempt_starting__kill(self):
        # the job is starting but a task has not been started; attempts to kill the job should succeed without the task ever
        # starting
        def _pretask():
            self.assert_job_state("starting")
            self.job_kill()
        # cqm should never entering the running state.  if it does, then something is wrong with the state machine.  to detect
        # this problem, we do nothing during the running state, causing any task that might have been started not to be completed
        # (task_finished is not called by the template).  this will result in the the test hanging in job_finished_wait() until
        # the timeout is reached.
        def _task_run(preempt):
            self.assert_next_op('reserve')
        self.job_exec_driver(job_pretask = _pretask, task_run = _task_run)
        self.job_exec_driver(resource_pretask = _pretask, task_run = _task_run)

    @timeout(10)
    def test_nonpreempt_starting__kill_failed(self):
        def _pretask():
            self.assert_job_state("starting")
            self.taskman.add_exc('reserve', BogusException1("error1"))
            self.taskman.add_exc('reserve', BogusException2("error2"))
            self.job_kill()
        def _task_run(preempt):
            self.assert_next_op('reserve', BogusException1)
            self.assert_next_op('reserve', BogusException2)
            self.assert_next_op('reserve')
        self.job_exec_driver(job_pretask = _pretask, task_run = _task_run)
        self.job_exec_driver(resource_pretask = _pretask, task_run = _task_run)

    @timeout(10)
    def test_nonpreempt_starting__kill_failed__wb(self):
        def _progress_off(op, exc):
            assert op == "reserve"
            self.qm_thr.pause()
        def _pretask():
            self.assert_job_state("starting")
            self.taskman.add_exc('reserve', BogusException1("error1"), _progress_off)
            self.taskman.add_exc('reserve', BogusException2("error2"))
            self.job_kill()
        def _task_run(preempt):
            self.assert_next_op('reserve', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"exiting", 'sm_state':"Release_Resources_Retry"})
            self.qm_thr.resume()
            self.assert_next_op('reserve', BogusException2)
            self.assert_next_op('reserve')
        self.job_exec_driver(job_pretask = _pretask, task_run = _task_run)
        self.job_exec_driver(resource_pretask = _pretask, task_run = _task_run)

    @timeout(10)
    def test_nonpreempt_starting__force_kill(self):
        # the job is starting but a task has not been started; forcibly killing a job should always work
        def _pretask():
            self.assert_job_state("starting")
            self.job_kill(force = True)
        # cqm should never entering the running state.  if it does, then something is wrong with the state machine.  to detect
        # this problem, we do nothing during the running state, causing any task that might have been started not to be completed
        # (task_finished is not called by the template).  this will result in the the test hanging in job_finished_wait() until
        # the timeout is reached.
        def _task_run(preempt):
            pass
        self.job_exec_driver(job_pretask = _pretask, task_run = _task_run)
        self.job_exec_driver(resource_pretask = _pretask, task_run = _task_run)

    @timeout(10)
    def test_nonpreempt_starting__preempt(self):
        # the job is starting; attempts to preempt a non-preemptable job should fail
        def _pretask():
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
        self.job_exec_driver(job_pretask = _pretask)
        self.job_exec_driver(resource_pretask = _pretask)

    @timeout(130)
    def test_nonpreempt_starting__walltime_adjustment(self):
        # the job is starting; let's adjust its walltime
        def _pretask():
            self.job_update({}, {'walltime':new_walltime})
            assert self.job['walltime'] == new_walltime
        def _task_active():
            op = self.assert_next_task_op('signal')
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            assert op[3] == Signal_Map.terminate
        orig_walltime = 1
        new_walltime = 2
        timer = Timer()
        timer.start()
        self.job_exec_driver(spec = {'walltime':orig_walltime}, job_pretask = _pretask, task_active = _task_active)
        timer.stop()
        assert timer.elapsed_time > new_walltime * 60 - 5

    @timeout(10)
    def test_nonpreempt_running__hold(self):
        # a task is running; attempts to place a hold on a non-preemptable job should be ignored
        def _task_active():
            self.job_user_hold(new_hold = False)
            self.assert_job_state("running")
            self.job_admin_hold(new_hold = False)
            self.assert_job_state("running")
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_running__release(self):
        # a task is running; attempts to place a hold on a non-preemptable job should be ignored
        def _task_active():
            self.job_user_release(new_hold = False)
            self.assert_job_state("running")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("running")
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_running__run(self):
        # the job is running; attempting to run the job again should fail
        def _task_active():
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is already running should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_running__kill(self):
        # a task is running; let's kill it
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
        self.job_exec_driver(task_active = _task_active)

    def test_nonpreempt_running__force_kill(self):
        # a task is running; let's forcibly kill it
        def _task_active():
            self.job_kill(force = True)
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        # the job should just disappear, so the normal task completion actions should not be required; if the test hangs, then it
        # is likely that the force kill failed
        def _task_complete():
            pass
        self.job_exec_driver(task_active = _task_active, task_complete = _task_complete)

    @timeout(10)
    def test_nonpreempt_running__kill_failed(self):
        # a task is running and needs to be killed; failed attempts to kill the task should automatically be retried
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"))
            self.job_kill()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.terminate
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == Signal_Map.terminate
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_running__kill_failed__wb(self):
        # a task is running and needs to be killed; failed attempts to kill the task should automatically be retried
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.terminate
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_running__preempt(self):
        # the job is running; attempts to preempt a non-preemptable job should fail
        def _task_active():
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_running__finalize_failed(self):
        def _task_complete():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"))
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.job_get_state(assert_spec = {'state':"exiting", 'sm_state':"Finalize_Retry"})
            self.assert_next_task_op('wait', BogusException2)
            self.assert_next_task_op('wait')
        self.job_exec_driver(task_complete = _task_complete)

    @whitebox
    @timeout(10)
    def test_nonpreempt_running__finalize_failed__wb(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _task_complete():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.qm_thr.pause_wait()
            self.assert_next_task_op('wait', BogusException2)
            self.job_get_state(assert_spec = {'state':"exiting", 'sm_state':"Finalize_Retry"})
            self.qm_thr.resume()
            self.assert_next_task_op('wait')
        self.job_exec_driver(task_complete = _task_complete)

    @timeout(70)
    def test_nonpreempt_running__job_timeout(self):
        def _task_active():
            op = self.assert_next_task_op('signal')
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            assert op[3] == Signal_Map.terminate
        self.job_exec_driver(spec = {'walltime':1}, task_active = _task_active)

    @timeout(130)
    def test_nonpreempt_running__walltime_adjustment(self):
        # a task is running; let's adjust its walltime
        def _task_active():
            self.job_update({}, {'walltime':new_walltime})
            assert self.job['walltime'] == new_walltime
            self.assert_next_op('reserve')
            op = self.assert_next_task_op('signal')
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            assert op[3] == Signal_Map.terminate
        orig_walltime = 1
        new_walltime = 2
        timer = Timer()
        timer.start()
        self.job_exec_driver(spec = {'walltime':orig_walltime}, task_active = _task_active)
        timer.stop()
        assert timer.elapsed_time > new_walltime * 60 - 5

    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__hold(self):
        # while waiting to retry starting a new task, attempts to place hold on a non-preemptable job should be ignored
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            self.job_user_hold(new_hold = False)
            self.qm_thr.resume()
            self.job_get_state(assert_spec = {'user_hold':False})
            self.job_running_wait()
            self.assert_next_task_op('add')
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait)

    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__release(self):
        # while waiting to retry starting a new task, attempts to release a hold on a job should be ignored
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            self.job_user_release(new_hold = False)
            self.qm_thr.resume()
            self.job_running_wait()
            self.assert_next_task_op('add')
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait)

    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__run(self):
        # attempting to run a job that is already attempting to run should fail
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is already running should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
            self.qm_thr.resume()
            self.job_running_wait()
            self.assert_next_task_op('add')
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait)

    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__kill(self):
        # attempting to kill a job while waiting to retry starting a new task should in fact kill the job
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            self.job_kill()
            self.qm_thr.resume()
        def _task_complete():
            # the task has not been started so we shouldn't tell the task manager that it's complete
            pass
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait, task_complete = _task_complete)
    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__force_kill(self):
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            self.job_kill(force = True)
            self.qm_thr.resume()
        def _task_complete():
            # the task has not been started so we shouldn't tell the task manager that it's complete
            pass
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait, task_complete = _task_complete)

    @whitebox
    @timeout(10)
    def test_nonpreempt_run_retry__preempt(self):
        # attempting to preempt a non-preemptable job should fail
        def _progress_off(op, exc, specs):
            assert op == "add"
            self.qm_thr.pause()
        def _job_queued():
            self.taskman.add_exc('add', BogusException1("error1"), _progress_off)
        def _task_wait():
            self.assert_next_task_op('add', BogusException1)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"starting", 'sm_state':"Run_Retry"})
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
            self.qm_thr.resume()
            self.job_running_wait()
            self.assert_next_task_op('add')
        self.job_exec_driver(job_queued = _job_queued, task_wait = _task_wait)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__hold(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            self.job_user_hold(new_hold = False)
            self.qm_thr.resume()
            self.job_get_state(assert_spec = {'user_hold':False})
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__release(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            self.job_user_release(new_hold = False)
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__run(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is already running should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__kill(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            self.job_kill(signame = "SIGINT")
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGINT"
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__force_kill(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            self.job_kill(force = True, signame = "SIGINT")
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGINT"
            self.qm_thr.resume()
        # the job should just disappear, so the normal task completion actions should not be required; if the test hangs, then it
        # is likely that the force kill failed
        def _task_complete():
            pass
        self.job_exec_driver(task_active = _task_active, task_complete = _task_complete)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__preempt(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
        self.job_exec_driver(task_active = _task_active)

    @whitebox
    @timeout(10)
    def test_nonpreempt_kill_retry__task_end(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == "SIGUSR2"
            self.qm_thr.pause()
        def _add_signal_exc(op, exc, specs, signam):
            # keep the state machine from entering the killing state
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            self.test_fault_count += 1
        def _task_active():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == "SIGUSR2"
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Kill_Retry"})
        def _task_complete():
            self.task_finished(0)
            self.qm_thr.resume()
            op = self.taskman.op_wait()
            while op[0] != 'wait':
                assert op[0] == 'signal'
                assert isinstance(op[1], BogusException2)
                assert op[3] == "SIGUSR2"
                op = self.taskman.op_wait()
            self.taskman.clear_excs('signal')
        self.test_fault_count = 0
        self.job_exec_driver(task_active = _task_active, task_complete = _task_complete)
        del self.test_fault_count

    @timeout(10)
    def test_nonpreempt_killing__hold(self):
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            self.job_user_hold(new_hold = False)
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_killing__release(self):
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            self.job_user_release(new_hold = False)
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_killing__run(self):
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is already running should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_killing__kill(self):
        def _task_active():
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            self.job_kill(signame = "SIGINT")
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGINT"
        self.job_exec_driver(task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_killing__force_kill(self):
        def _task_active():
            self.job_kill(signame = "SIGUSR2")
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            self.job_kill(force = True, signame = "SIGINT")
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGINT"
        # the job should just disappear, so the normal task completion actions should not be required; if the test hangs, then it
        # is likely that the force kill failed
        def _task_complete():
            pass
        self.job_exec_driver(task_active = _task_active, task_complete = _task_complete)

    @timeout(10)
    def test_nonpreempt_killing__preempt(self):
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
        self.job_exec_driver(task_active = _task_active)

    @timeout(70)
    def test_nonpreempt_killing__timeout(self):
        def _task_active():
            self.job_kill()
            op = self.assert_next_task_op('signal')
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            assert op[3] == Signal_Map.terminate
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.force_kill
        self.job_exec_driver(spec = {'force_kill_delay':1, 'walltime':2}, task_active = _task_active)

    @timeout(10)
    def test_nonpreempt_exiting__hold(self):
        # the job is exiting; attempts to place a hold on a non-preemptable job should be ignored
        def _user_hold():
            self.job_user_hold(new_hold = False)
            self.assert_job_state("exiting")
        def _admin_hold():
            self.job_admin_hold(new_hold = False)
            self.assert_job_state("exiting")
        self.job_exec_driver(resource_posttask = _user_hold, job_posttask = _user_hold)
        self.job_exec_driver(resource_posttask = _admin_hold,job_posttask = _admin_hold)

    @timeout(10)
    def test_nonpreempt_exiting__release(self):
        # the job is exiting; attempts to release a hold on a non-preemptable job should be ignored
        def _user_release():
            self.job_user_release(new_hold = False)
            self.assert_job_state("exiting")
        def _admin_release():
            self.job_admin_release(new_hold = False)
            self.assert_job_state("exiting")
        self.job_exec_driver(resource_posttask = _user_release, job_posttask = _user_release)
        self.job_exec_driver(resource_posttask = _admin_release, job_posttask = _admin_release)

    @timeout(10)
    def test_nonpreempt_exiting__run(self):
        # the job is exiting; attempts to run the job should fail
        def _posttask():
            try:
                self.job_run(["R99"])
                assert False, "attempt to run a job that is already running should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobRunError.fault_code
        self.job_exec_driver(job_posttask = _posttask)
        self.job_exec_driver(resource_posttask = _posttask)

    @timeout(10)
    def test_nonpreempt_exiting__kill(self):
        # the job is exiting; attempts to kill the job should be ignored
        def _posttask():
            self.job_kill()
            self.assert_job_state("exiting")
        self.job_exec_driver(job_posttask = _posttask)
        self.job_exec_driver(resource_posttask = _posttask)

    @timeout(10)
    def test_nonpreempt_exiting__force_kill(self):
        def _posttask():
            self.job_kill(force = True)
            self.assert_job_state("exiting")
        self.job_exec_driver(job_posttask = _posttask)
        self.job_exec_driver(resource_posttask = _posttask)

    @timeout(10)
    def test_nonpreempt_exiting__preempt(self):
        # the job is exiting; attempts to preempt a non-preemptable job should fail
        def _posttask():
            try:
                self.job_preempt()
                assert False, "attempt to preempt a non-preemptable job should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
        self.job_exec_driver(job_posttask = _posttask)
        self.job_exec_driver(resource_posttask = _posttask)

    @timeout(10)
    def test_nonpreempt_validate_multiple_scripts(self):
        num_scripts = 3
        syncs = []
        configs = {}
        try:
            job_prescripts = create_touch_scripts(num_scripts)
            configs['job_prescripts'] = ":".join(get_script_filenames(job_prescripts))
            syncs += job_prescripts
            resource_prescripts = create_touch_scripts(num_scripts)
            configs['resource_prescripts'] = ":".join(get_script_filenames(resource_prescripts))
            syncs += resource_prescripts
            resource_postscripts = create_touch_scripts(num_scripts)
            configs['resource_postscripts'] = ":".join(get_script_filenames(resource_postscripts))
            syncs += resource_postscripts
            job_postscripts = create_touch_scripts(num_scripts)
            configs['job_postscripts'] = ":".join(get_script_filenames(job_postscripts))
            syncs += job_postscripts
            cqm_config_file_update(configs)
            self.job_add()
            self.job_run(["R00"])
            self.job_running_wait()
            self.assert_next_task_op('add')
            check_output_files(job_prescripts + resource_prescripts)
            self.task_finished(0)
            self.assert_next_task_op('wait')
            self.job_finished_wait()
            check_output_files(resource_postscripts + job_postscripts)
        finally:
            if len(syncs) > 0:
                delete_scripts(syncs)
                delete_input_files(syncs)
                delete_output_files(syncs)

    @timeout(15)
    def test_nonpreempt_validate_script_states(self):
        def _job_queued():
            time.sleep(1)
            check_output_files(self.job_prescripts, False, "job prologue script run prematurely")
        def _job_pretask():
            time.sleep(1)
            check_output_files(self.resource_prescripts, False, "resource prologue script run prematurely")
        def _resource_pretask():
            # force state test
            pass
        def _task_active():
            time.sleep(1)
            check_output_files(self.resource_postscripts, False, "resource epilogue script run prematurely")
        def _resource_posttask():
            time.sleep(1)
            check_output_files(self.job_postscripts, False, "job epilogue script run prematurely")
        def _job_posttask():
            # force state test
            pass
        self.job_exec_driver(
            job_queued = _job_queued, job_pretask = _job_pretask, resource_pretask = _resource_pretask, \
            task_active = _task_active, resource_posttask = _resource_posttask, job_posttask = _job_posttask)
        
    #
    # tests for preemptable jobs
    #
    @timeout(10)
    def test_preempt_multiple_runs(self):
        # verify that a job can be preempted multiple times
        def _job_preempted():
            self.test_preempt_count += 1
        def _task_active():
            self.test_task_count += 1
        num_preempts = 3
        self.test_preempt_count = 0
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, task_active = _task_active, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(10)
    def test_preempt_queued__preempt(self):
        # the job is in the hold state; attempts to preempt the job should fail despite the job being preemptable
        def _job_queued():
            try:
                self.job_preempt()
                assert False, "attempt to preempt while in a hold state should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
        self.job_exec_driver(num_preempts = 1, job_queued = _job_queued)

    @timeout(10)
    def test_preempt_hold__preempt(self):
        # the job is in the hold state; attempts to preempt the job should fail despite the job being preemptable
        def _job_queued():
            self.job_user_hold(new_hold = True)
            try:
                self.job_preempt()
                assert False, "attempt to preempt while in a hold state should fail"
            except xmlrpclib.Fault, e:
                assert e.faultCode == JobPreemptionError.fault_code
            self.job_user_release(new_hold = False)
        self.job_exec_driver(num_preempts = 1, job_queued = _job_queued)

    @timeout(15)
    def test_preempt_starting__hold(self):
        # the job is starting; attempts to place and release a pending hold on a preemptable job should work
        def _pretask():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("starting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("starting")
        def _job_preempted():
            self.job_user_release(new_hold = False)
            self.assert_job_state("admin_hold")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_pretask = _pretask, job_preempted = _job_preempted,
            preempt_pretask = _pretask)
        self.job_exec_driver(num_preempts = num_preempts, resource_pretask = _pretask, job_preempted = _job_preempted,
            preempt_pretask = _pretask)
        assert self.test_preempt_count == 2 * num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (2 * num_preempts, self.test_preempt_count,)
        del self.test_preempt_count

    def test_preempt_starting__release(self):
        # the job is starting; releasing a previous pending hold should work
        def _pretask():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("starting")
            self.job_user_release(new_hold = False)
            self.assert_job_state("starting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("starting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("starting")
        self.job_exec_driver(num_preempts = 1, job_pretask = _pretask, resource_pretask = _pretask)

    @timeout(10)
    def test_preempt_starting__kill(self):
        # the job is starting but a task is not yet running; attempts to kill the job should succeed without the task ever
        # starting (even if a preempt is pending)
        def _pretask():
            self.job_kill()
            self.assert_job_state("starting")
        # cqm should never entering the running state.  if it does, then something is wrong with the state machine.  to detect
        # this problem, we do nothing during the running state and skip job preemption, causing any task that might have been
        # started not to be completed (task_finished is not called by the template).  this will result in the the test hanging in
        # job_finished_wait() until the timeout is reached.
        def _task_run(preempt):
            pass
        def _job_preempt():
            return False
        self.job_exec_driver(num_preempts = 1, job_pretask = _pretask, task_run = _task_run, job_preempt = _job_preempt)
        self.job_exec_driver(num_preempts = 1, resource_pretask = _pretask, task_run = _task_run, job_preempt = _job_preempt)

    @timeout(140)
    def test_preempt_starting__preempt_immediate(self):
        # the job is starting; preempts are immediate after prologue script complete since mintasktime is not set
        def _pretask():
            self.job_preempt()
            self.assert_job_state("starting")
        def _task_active():
            self.test_task_count += 1
        num_preempts = 1
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_pretask = _pretask, task_active = _task_active)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, resource_pretask = _pretask, task_active = _task_active)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_task_count

    @timeout(70)
    def test_preempt_starting__preempt_mintasktime(self):
        # the job is starting; attempts to preempt a preemptable job should be delayed until the minimum task execution timer
        # expires
        def _pretask():
            self.job_preempt()
            self.assert_job_state("starting")
        def _job_preempt():
            # preemption will be started when the minimum task timer expires, so we don't want to call job_preempt here
            self.assert_next_task_op('signal')
        def _task_active():
            self.test_task_count += 1
        num_preempts = 1
        self.test_task_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'mintasktime':1, 'walltime':2}, job_pretask = _pretask,
            task_active = _task_active, job_preempt = _job_preempt)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 60 - 5, timer.elapsed_time) 
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_task_count

    @timeout(10)
    def test_preempt_running__hold(self):
        def _task_active():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("running")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempted():
            self.job_user_release(new_hold = False)
            self.assert_job_state("admin_hold")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, task_active = _task_active, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(10)
    def test_preempt_running__release(self):
        def _task_active():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("running")
            self.job_user_release(new_hold = False)
            self.assert_job_state("running")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("running")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("running")
            self.test_task_count += 1
        num_preempts = 2
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, task_active = _task_active)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_task_count

    @timeout(10)
    def test_preempt_running__preempt_immediate(self):
        def _task_active():
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempted():
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 1
        self.test_preempt_count = 0
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, task_active = _task_active, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(10)
    def test_preempt_running__preempt_forced(self):
        def _task_active():
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempt():
            self.job_preempt(user=username, force=True)
            self.assert_next_task_op('signal')
        def _job_preempted():
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 1
        self.test_preempt_count = 0
        self.test_task_count = 0
        self.job_exec_driver(num_preempts = num_preempts, spec = {'mintasktime':1, 'walltime':num_preempts + 1},
            task_active = _task_active, job_preempt = _job_preempt, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(130)
    def test_preempt_running__preempt_mintasktime(self):
        def _task_active():
            self.assert_job_state("running")
            self.job_preempt()
            self.test_task_count += 1
        def _job_preempt():
            # preemption will be started when the task minimum timer expires, so we don't want job_preempt to be called here
            self.assert_next_task_op('signal')
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.test_task_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'mintasktime':1, 'walltime':num_preempts + 1},
            task_active = _task_active, job_preempt = _job_preempt)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 60 - 5, timer.elapsed_time) 
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(130)
    def test_preempt_running__maxtasktime(self):
        def _task_active():
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempt():
            # preemption will be started when the task maximum timer expires, so we don't want job_preempt to be called here
            self.assert_next_task_op('signal')
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.test_task_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxtasktime':1, 'walltime':num_preempts + 1},
            task_active = _task_active, job_preempt = _job_preempt)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 60 - 5, timer.elapsed_time) 
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(190)
    def test_preempt_running__maxtasktime_force_kill(self):
        def _task_active():
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempt():
            # preemption will be started when the task checkpoint timer expires, so we don't want job_preempt to be called here
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.checkpoint
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.force_kill
            self.test_preempt_count += 1
        num_preempts = 1
        self.test_preempt_count = 0
        self.test_task_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxcptime':1, 'maxtasktime':2, 'force_kill_delay':1,
           'walltime':num_preempts * 4}, task_active = _task_active, job_preempt = _job_preempt)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 180 - 5, timer.elapsed_time)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(130)
    def test_preempt_running__maxtasktime_nowalltime(self):
        def _task_active():
            self.assert_job_state("running")
            self.test_task_count += 1
        def _job_preempt():
            # preemption will be started when the task maximum timer expires, so we don't want job_preempt to be called here
            self.assert_next_task_op('signal')
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.test_task_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxtasktime':1, 'walltime':0}, task_active = _task_active,
            job_preempt = _job_preempt)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 60 - 5, timer.elapsed_time) 
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        assert self.test_task_count == num_preempts + 1, "tasks executed should have been %d, but %d were executed instead" % \
            (num_preempts + 1, self.test_task_count,)
        del self.test_preempt_count
        del self.test_task_count

    @timeout(10)
    def test_preempt_running__preempt_failed(self):
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"))
            self.taskman.add_exc('signal', BogusException2("error2"))
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            # NOTE: no checkpoint time specified, so the task is signaled to terminate immediately
            assert op[3] == Signal_Map.terminate 
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == Signal_Map.terminate
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        del self.test_preempt_count

    @whitebox
    @timeout(10)
    def test_preempt_running__preempt_failed_wb(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == Signal_Map.terminate
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.taskman.add_exc('signal', BogusException2("error2"), _progress_off)
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            # NOTE: no checkpoint time specified, so the task is signaled to terminate immediately
            assert op[3] == Signal_Map.terminate 
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal', BogusException2)
            assert op[3] == Signal_Map.terminate
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        num_preempts = 2
        self.test_progress_off_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt)
        assert self.test_progress_off_count == 2 * num_preempts
        del self.test_progress_off_count

    @whitebox
    @timeout(10)
    def test_preempt_preempt_retry__hold(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == Signal_Map.terminate
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.terminate 
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.job_user_hold(new_hold = True)
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        def _job_preempted():
            self.job_user_release(new_hold = False)
        num_preempts = 2
        self.test_progress_off_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt, job_preempted = _job_preempted)
        assert self.test_progress_off_count == num_preempts
        del self.test_progress_off_count

    @whitebox
    @timeout(10)
    def test_preempt_preempt_retry__kill(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == Signal_Map.checkpoint
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.checkpoint
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.job_kill(signame = "SIGUSR2")
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
            self.job_get_state(assert_spec = {'state':"killing", 'sm_state':"Killing"})
            self.task_finished(0)
            self.assert_next_task_op('wait')
            return False
        num_preempts = 10
        self.test_progress_off_count = 0
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxcptime':1, 'maxtasktime':2, 'walltime':3},
            job_preempt = _job_preempt)
        assert self.test_progress_off_count == 1
        del self.test_progress_off_count

    @whitebox
    @timeout(10)
    def test_preempt_preempt_retry__force_kill(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == Signal_Map.checkpoint
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.checkpoint
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.job_kill(force = True, signame = "SIGUSR2")
            self.qm_thr.resume()
            op = self.assert_next_task_op('signal')
            assert op[3] == "SIGUSR2"
            return False
        num_preempts = 10
        self.test_progress_off_count = 0
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxcptime':1, 'maxtasktime':2, 'walltime':3},
            job_preempt = _job_preempt)
        assert self.test_progress_off_count == 1
        del self.test_progress_off_count

    @whitebox
    @timeout(10)
    def test_preempt_preempt_retry__task_end_no_signal(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert signame == Signal_Map.terminate
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _add_signal_exc(op, exc, specs, signam):
            # keep the state machine from entering the preempting state
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            self.test_fault_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1"), _progress_off)
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            self.job_preempt()
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.terminate 
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.task_finished(0)
            self.qm_thr.resume()
            op = self.taskman.op_wait()
            while op[0] != 'wait':
                assert op[0] == 'signal'
                assert isinstance(op[1], BogusException2)
                assert op[3] == Signal_Map.terminate
                op = self.taskman.op_wait()
            self.taskman.clear_excs('signal')
            return False
        def _resource_posttask():
            # make sure the scripts are run
            pass
        num_preempts = 10
        self.test_progress_off_count = 0
        self.test_fault_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt)
        assert self.test_progress_off_count == 1
        del self.test_progress_off_count
        del self.test_fault_count

    @whitebox
    @timeout(130)
    def test_preempt_preempt_retry__task_end_after_signal(self):
        def _progress_off(op, exc, specs, signame):
            assert op == "signal"
            assert isinstance(exc, BogusException1)
            assert signame == Signal_Map.terminate
            self.qm_thr.pause()
            self.test_progress_off_count += 1
        def _add_signal_exc(op, exc, specs, signam):
            # keep the state machine from entering the preempting state
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            assert isinstance(exc, BogusException2)
            self.test_fault_count += 1
        def _job_preempt():
            self.taskman.add_exc('signal', BogusException1("error1-0"))
            self.job_preempt()
            # let the checkpoint signal pass
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.checkpoint
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.checkpoint
            self.taskman.add_exc('signal', BogusException1("error1-1"), _progress_off)
            self.taskman.add_exc('signal', BogusException2("error2-%d" % (self.test_fault_count,)), _add_signal_exc)
            self.job_preempting_wait()
            # interrupt the terminate signal and end the task in the middle
            op = self.assert_next_task_op('signal', BogusException1)
            assert op[3] == Signal_Map.terminate
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Retry"})
            self.task_finished(0)
            self.qm_thr.resume()
        def _job_preempting():
            # wait for the end of task to be noticed by the state machine
            op = self.taskman.op_wait()
            while op[0] != 'wait':
                assert op[0] == 'signal'
                assert isinstance(op[1], BogusException2)
                assert op[3] == Signal_Map.terminate
                op = self.taskman.op_wait()
            self.taskman.clear_excs('signal')
        def _preempt_posttask():
            # make sure hte scripts are run
            pass
        def _job_preempted():
            self.test_preempted_count += 1
        num_preempts = 2
        self.test_progress_off_count = 0
        self.test_preempted_count = 0
        self.test_fault_count = 0
        timer = Timer()
        timer.start()
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxcptime':1, 'maxtasktime':2, 'walltime':num_preempts * 3},
            job_preempt = _job_preempt, job_preempting = _job_preempting, job_preempted = _job_preempted)
        timer.stop()
        assert timer.elapsed_time > num_preempts * 60 - 5, "timer expected to be greater than %f but was %f" % \
            (num_preempts * 60 - 5, timer.elapsed_time)
        assert self.test_progress_off_count == num_preempts
        assert self.test_preempted_count == num_preempts
        del self.test_progress_off_count
        del self.test_preempted_count
        del self.test_fault_count

    @timeout(10)
    def test_preempt_preempting__hold(self):
        def _job_preempting():
            self.job_preempting_wait()
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.task_finished(0)
            self.assert_next_task_op('wait')
        def _job_preempted():
            self.job_admin_release(new_hold = False)
            self.assert_job_state("user_hold")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempting = _job_preempting, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        del self.test_preempt_count

    @timeout(10)
    def test_preempt_preempting__release(self):
        def _job_preempting():
            self.job_preempting_wait()
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempting")
            self.task_finished(0)
            self.assert_next_task_op('wait')
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting)

    @timeout(10)
    def test_preempt_preempting__kill_same_signal(self):
        def _job_preempt():
            self.job_preempt()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        def _job_preempting():
            # no checkpoint time was request so the terminate signal is used for both the preempt and the kill; as a result, no
            # signal will be sent to the task
            self.job_preempting_wait()
            self.job_kill()
            self.assert_job_state("killing")
            self.task_finished(0)
            self.assert_next_task_op('wait')
            return False
        num_preempts = 10
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt, job_preempting = _job_preempting)

    @timeout(10)
    def test_preempt_preempting__kill_demoted_signal(self):
        def _job_preempt():
            self.job_preempt()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        def _job_preempting():
            self.job_preempting_wait()
            self.job_kill(signame = "SIGUSR2")
            self.assert_job_state("killing")
            self.task_finished(0)
            self.assert_next_task_op('wait')
            return False
        num_preempts = 10
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt, job_preempting = _job_preempting)

    @timeout(10)
    def test_preempt_preempting__kill_different_signal(self):
        def _job_preempt():
            self.job_preempt()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.checkpoint
        def _job_preempting():
            self.job_preempting_wait()
            self.job_kill()
            self.assert_job_state("killing")
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            self.task_finished(0)
            self.assert_next_task_op('wait')
            return False
        num_preempts = 10
        self.job_exec_driver(num_preempts = num_preempts, spec = {'maxcptime':1}, job_preempt = _job_preempt, 
            job_preempting = _job_preempting)

    @timeout(10)
    def test_preempt_preempting__force_kill(self):
        def _job_preempt():
            self.job_preempt()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
        def _job_preempting():
            # no checkpoint time was request so the terminate signal is used for both the preempt and the kill; as a result, no
            # signal will be sent to the task
            self.job_preempting_wait()
            self.job_kill(force = True)
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate
            return False
        num_preempts = 10
        self.job_exec_driver(num_preempts = num_preempts, job_preempt = _job_preempt, job_preempting = _job_preempting)

    @timeout(10)
    def test_preempt_preempting__finalize_failed(self):
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"))
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.assert_next_task_op('wait', BogusException2)
            self.assert_next_task_op('wait')
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting)

    @whitebox
    @timeout(10)
    def test_preempt_preempting__finalize_failed__wb(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.qm_thr.pause_wait()
            self.assert_next_task_op('wait', BogusException2)
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.qm_thr.resume()
            self.assert_next_task_op('wait')
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting)

    @whitebox
    @timeout(10)
    def test_preempt_preempt_finalize_retry__hold(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.qm_thr.pause_wait()
            self.assert_next_task_op('wait', BogusException2)
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.qm_thr.resume()
            self.assert_next_task_op('wait')
        def _job_preempted():
            self.job_admin_release(new_hold = False)
            self.assert_job_state("user_hold")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.job_exec_driver(num_preempts = num_preempts, job_preempting = _job_preempting, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        del self.test_preempt_count

    @whitebox
    @timeout(10)
    def test_preempt_preempt_finalize_retry__release(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.qm_thr.pause_wait()
            self.assert_next_task_op('wait', BogusException2)
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempting")
            self.qm_thr.resume()
            self.assert_next_task_op('wait')
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting)

    @whitebox
    @timeout(10)
    def test_preempt_preempt_finalize_retry__kill(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.qm_thr.pause_wait()
            self.assert_next_task_op('wait', BogusException2)
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.job_kill()
            self.qm_thr.resume()
            self.assert_next_task_op('wait')
        def _preempt_posttask():
            return False
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting, preempt_posttask = _preempt_posttask)

    @whitebox
    @timeout(10)
    def test_preempt_preempt_finalize_retry__force_kill(self):
        def _progress_off(op, exc, specs):
            assert op == "wait"
            self.qm_thr.pause()
        def _job_preempting():
            self.taskman.add_exc('wait', BogusException1("error1"))
            self.taskman.add_exc('wait', BogusException2("error2"), _progress_off)
            self.job_preempting_wait()
            self.task_finished(0)
            self.assert_next_task_op('wait', BogusException1)
            self.assert_next_task_op('wait', BogusException2)
            self.qm_thr.pause_wait()
            self.job_get_state(assert_spec = {'state':"preempting", 'sm_state':"Preempt_Finalize_Retry"})
            self.job_kill(force = True)
            op = self.taskman.op_wait()
            assert op[0] == 'signal'
            assert op[3] == Signal_Map.terminate
            self.qm_thr.resume()
            return False
        self.job_exec_driver(num_preempts = 1, job_preempting = _job_preempting)

    #
    # BRT: the appropriate behavior needs to be defined for this situation and added to CQM
    #
    # @timeout(135)
    # def test_preempt_preempting__walltime_timeout(self):
    #     def _job_preempt():
    #         # preemption will be started when the checkpoint timer expires, so we don't want job_preempt to be called here
    #         op = self.assert_next_task_op('signal')
    #         assert op[3] == Signal_Map.checkpoint
    #         op = self.assert_next_task_op('signal')
    #         assert op[3] == Signal_Map.terminate
    #     def _resource_posttask():
    #         pass
    #     timer = Timer()
    #     timer.start()
    #     self.job_exec_driver(num_preempts = 1, spec = {'maxcptime':4, 'maxtasktime':5, 'walltime':2},
    #         job_preempt = _job_preempt, resource_posttask = _resource_posttask)
    #     timer.stop()
    #     assert timer.elapsed_time > 115, "timer expected to be greater than %f but was %f" % (115, timer.elapsed_time) 
    #     assert timer.elapsed_time < 130, "timer expected to be less than %f but was %f" % (130, timer.elapsed_time) 

    @timeout(10)
    def test_preempt_posttask__hold(self):
        def _preempt_posttask():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
        def _job_preempted():
            self.job_admin_release(new_hold = False)
            self.assert_job_state("user_hold")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempted")
            self.test_preempt_count += 1
        num_preempts = 2
        self.test_preempt_count = 0
        self.job_exec_driver(num_preempts = num_preempts, preempt_posttask = _preempt_posttask, job_preempted = _job_preempted)
        assert self.test_preempt_count == num_preempts, "number of preempts should have been %d, but was %d instead" % \
            (num_preempts, self.test_preempt_count,)
        del self.test_preempt_count

    @timeout(10)
    def test_preempt_posttask__release(self):
        def _preempt_posttask():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempting")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("preempting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempting")
        self.job_exec_driver(num_preempts = 1, preempt_posttask = _preempt_posttask)

    @timeout(10)
    def test_preempt_posttask__kill(self):
        def _preempt_posttask():
            self.job_kill()
            return False
        self.job_exec_driver(num_preempts = 1, preempt_posttask = _preempt_posttask)

    @timeout(10)
    def test_preempt_posttask__force_kill(self):
        def _preempt_posttask():
            self.job_kill(force = True)
            return False
        self.job_exec_driver(num_preempts = 1, preempt_posttask = _preempt_posttask)

    @timeout(10)
    def test_preempt_preempted__hold(self):
        def _job_preempted():
            self.job_user_hold(new_hold = True)
            self.assert_job_state("user_hold")
            self.job_user_release(new_hold = False)
            self.assert_job_state("preempted")
            self.job_admin_hold(new_hold = True)
            self.assert_job_state("admin_hold")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("preempted")
        self.job_exec_driver(num_preempts = 1, job_preempted = _job_preempted)

    @timeout(10)
    def test_preempt_preempted__kill(self):
        def _job_preempted():
            self.job_kill()
            return False
        self.job_exec_driver(num_preempts = 1, job_preempted = _job_preempted)

    @timeout(10)
    def test_preempt_preempted__force_kill(self):
        def _job_preempted():
            self.job_kill(force = True)
            return False
        self.job_exec_driver(num_preempts = 1, job_preempted = _job_preempted)

    @timeout(10)
    def test_preempt_exiting__hold(self):
        # the job is exiting; attempts to place and release a pending hold on a preemptable job should be ignored
        def _posttask():
            self.job_user_hold(new_hold = False)
            self.assert_job_state("exiting")
            self.job_admin_hold(new_hold = False)
            self.assert_job_state("exiting")
            self.test_posttask_count += 1
        num_preempts = 2
        self.test_posttask_count = 0
        self.job_exec_driver(num_preempts = num_preempts, resource_posttask = _posttask, job_posttask = _posttask)
        assert self.test_posttask_count == 2
        del self.test_posttask_count

    @timeout(10)
    def test_preempt_exiting__release(self):
        # the job is exiting; attempts to release a nonexistent hold should be ignored
        def _posttask():
            self.job_user_release(new_hold = False)
            self.assert_job_state("exiting")
            self.job_admin_release(new_hold = False)
            self.assert_job_state("exiting")
            self.test_posttask_count += 1
        num_preempts = 2
        self.test_posttask_count = 0
        self.job_exec_driver(num_preempts = num_preempts, resource_posttask = _posttask, job_posttask = _posttask)
        assert self.test_posttask_count == 2
        del self.test_posttask_count

    @timeout(10)
    def test_preempt_exiting__kill(self):
        # the job is exiting; attempts to kill the job should be ignored
        def _posttask():
            self.job_kill()
            self.assert_job_state("exiting")
            self.test_posttask_count += 1
        num_preempts = 2
        self.test_posttask_count = 0
        self.job_exec_driver(num_preempts = num_preempts, resource_posttask = _posttask, job_posttask = _posttask)
        assert self.test_posttask_count == 2
        del self.test_posttask_count

    @timeout(10)
    def test_preempt_exiting__force_kill(self):
        def _posttask():
            self.job_kill(force = True)
        num_preempts = 2
        self.job_exec_driver(num_preempts = num_preempts, job_posttask = _posttask)

    @timeout(10)
    def test_preempt_exiting__preempt(self):
        # the job is exiting; attempts to preempt a preemptable job should be ignored
        def _posttask():
            self.job_preempt()
            self.assert_job_state("exiting")
            self.test_posttask_count += 1
        num_preempts = 2
        self.test_posttask_count = 0
        self.job_exec_driver(num_preempts = num_preempts, resource_posttask = _posttask, job_posttask = _posttask)
        assert self.test_posttask_count == 2
        del self.test_posttask_count

    @timeout(10)
    def test_preempt_validate_multiple_scripts(self):
        num_scripts = 3
        syncs = []
        configs = {}
        try:
            job_prescripts = create_touch_scripts(num_scripts)
            configs['job_prescripts'] = ":".join(get_script_filenames(job_prescripts))
            syncs += job_prescripts
            resource_prescripts = create_touch_scripts(num_scripts)
            configs['resource_prescripts'] = ":".join(get_script_filenames(resource_prescripts))
            syncs += resource_prescripts
            resource_postscripts = create_touch_scripts(num_scripts)
            configs['resource_postscripts'] = ":".join(get_script_filenames(resource_postscripts))
            syncs += resource_postscripts
            job_postscripts = create_touch_scripts(num_scripts)
            configs['job_postscripts'] = ":".join(get_script_filenames(job_postscripts))
            syncs += job_postscripts
            cqm_config_file_update(configs)
            self.job_add({'preemptable':True})
            self.job_run(["R00"])
            self.job_running_wait()
            check_output_files(job_prescripts + resource_prescripts)
            self.assert_next_task_op('add')
            self.job_preempt()
            op = self.assert_next_task_op('signal')
            assert op[3] == Signal_Map.terminate  # no checkpoint time specified
            self.job_preempting_wait()
            self.task_finished(0)
            self.job_preempted_wait()
            self.assert_next_task_op('wait')
            check_output_files(resource_postscripts)
            check_output_files(job_postscripts, False)
            self.job_run(["R01"])
            self.job_running_wait()
            self.assert_next_task_op('add')
            check_output_files(resource_prescripts)
            check_output_files(job_prescripts, False)
            self.task_finished(0)
            self.job_finished_wait()
            check_output_files(resource_postscripts + job_postscripts)
            self.assert_next_task_op('wait')
        finally:
            if len(syncs) > 0:
                delete_scripts(syncs)
                delete_input_files(syncs)
                delete_output_files(syncs)

    @timeout(15)
    def test_preempt_validate_script_states(self):
        def _job_queued():
            time.sleep(1)
            check_output_files(self.job_prescripts, False, "job prologue script run prematurely")
        def _job_pretask():
            time.sleep(1)
            check_output_files(self.resource_prescripts, False, "resource prologue script run prematurely")
        def _resource_pretask():
            # force state test
            pass
        def _task_active():
            check_output_files(self.resource_postscripts, False, "resource epilogue script run prematurely")
        def _job_preempt():
            self.job_preempt()
            self.assert_next_task_op('signal')
            self.job_preempting_wait()
            time.sleep(1)
            check_output_files(self.resource_postscripts, False, "resource epilogue script run prematurely")
        def _preempt_posttask():
            # force state test
            pass
        def _job_preempted():
            time.sleep(1)
            check_output_files(self.resource_prescripts, False, "resource prologue script run prematurely")
        def _preempt_pretask():
            # force state test
            pass
        def _resource_posttask():
            time.sleep(1)
            check_output_files(self.job_postscripts, False, "job epilogue script run prematurely")
        def _job_posttask():
            # force state test
            pass
        num_preempts = 2
        self.job_exec_driver(
            num_preempts = num_preempts, job_queued = _job_queued, job_pretask = _job_pretask,
            resource_pretask = _resource_pretask, task_active = _task_active, job_preempt = _job_preempt,
            preempt_posttask = _preempt_posttask, job_preempted = _job_preempted, preempt_pretask = _preempt_pretask,
            resource_posttask = _resource_posttask, job_posttask = _job_posttask)
        

class TestCQMIntegration (CQMIntegrationTestBase):
    logger = setup_file_logging("TestCQMSystemIntegration", LOG_FILE, "DEBUG")
    default_job_spec = {'mode':"vn", 'command':"/bin/ls", 'walltime':1, 'nodes':1024, 'procs':4096, 'outputdir':"."}

    def setup(self):
        CQMIntegrationTestBase.setup(self)
        self.taskman = SimulatedSystem()
        self.setup_cqm()

    def teardown(self):
        del self.taskman
        CQMIntegrationTestBase.teardown(self)

# class TestCQMSystemIntegration (CQMIntegrationTestBase):
#     logger = setup_file_logging("TestCQMSystemIntegration", LOG_FILE, "DEBUG")
#     default_job_spec = {'mode':"vn", 'command':"/bin/ls", 'walltime':1, 'nodes':1024, 'procs':4096}
# 
#     def setup(self):
#         CQMIntegrationTestBase.setup(self)
#         self.taskman = SimulatedSystem()
#         self.scriptm = SimulatedScriptManager()
#         self.setup_cqm()
# 
#     def teardown(self):
#         del self.taskman
#         del self.scriptm
#         CQMIntegrationTestBase.teardown(self)

# class TestCQMScriptIntegration (CQMIntegrationTestBase):
#     logger = setup_file_logging("TestCQMScriptIntegration", LOG_FILE, "DEBUG")
#     default_job_spec = {'mode':"script", 'command':"/bin/ls", 'walltime':1, 'nodes':1024, 'procs':4096}
# 
#     def setup(self):
#         CQMIntegrationTestBase.setup(self)
#         self.taskman = SimulatedScriptManager()
#         self.system = SimulatedSystem()
#         self.setup_cqm()
#         
#     def teardown(self):
#         del self.taskman
#         del self.system
#         CQMIntegrationTestBase.teardown(self)
