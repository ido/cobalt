'''Unit tests for the BGQBooter module

'''
CONFIG_FILE_ENTRY = """
[bgsystem]
max_reboots=3

"""
import Cobalt
#Add a config file to be read
config_file = Cobalt.CONFIG_FILES[0]
config_fp = open(config_file, "w")
config_fp.write(CONFIG_FILE_ENTRY)
config_fp.close()

import threading
from nose import *
from nose.tools import timed, TimeExpired
from TestCobalt.Utilities.Time import timeout
import time
from Cobalt.Components.BGQBooter import *
import copy

import pybgsched

class test_BGQBoot(object):

    class TestBlock(object):

        def __init__(self, name, reserved=True, block_type='normal'):
            self.name = name
            self.reserved = reserved
            self.block_type = 'normal'
            self.current_kernel_options=" "
            self.current_kernel = "default"

        def under_resource_reservation(self, job_id):
            return self.reserved

    def setup(self):
        pybgsched.Block('TB-1', 512)
        self.block_lock = threading.Lock()

    def teardown(self):
        pybgsched.block_dict = {}
        Cobalt.Components.BGQBooter._boot_id_gen.idnum=0

    def test_initialization(self):
        boot = BGQBoot(pybgsched.block_dict['TB-1'], 1, 'testuser', self.block_lock)
        assert str(boot) == "{'block_name': 'TB-1', 'user': 'testuser', 'state': 'pending', 'job_id': 1, 'boot_id': 1}", "Malformed boot: %s" % boot



class test_BGQBooter(object):

    class TestBlock(object):

        def __init__(self, name, reserved=True, block_type='normal', subblock_parent=None):
            self.name = name
            self.reserved = reserved
            self.block_type = block_type
            self.current_kernel_options = " "
            self.current_kernel = "default"
            self.subblock_parent = self.name
            if block_type == 'pseudoblock':
                self.subblock_parent = subblock_parent

        def under_resource_reservation(self, job_id):
             return self.reserved

    class TestIOBlock(object):
        def __init__(self, name):
            self.name = name
            self.current_kernel_options=" "
            self.current_kernel = "default"

    def setup(self):
        pybgsched.Block('TB-1', 512)
        pybgsched.Block('TB-2', 512)
        pybgsched.Block('TB-3', 512)
        self.test_blocks = {}
        self.test_blocks['TB-1'] = test_BGQBooter.TestBlock('TB-1')
        self.test_blocks['TB-2'] = test_BGQBooter.TestBlock('TB-2')
        self.test_blocks['TB-3'] = test_BGQBooter.TestBlock('TB-3')
        self.block_lock = threading.Lock()

        pybgsched.IOBlock('IO-1', 8)
        self.test_io_blocks = {}
        self.test_io_blocks['IO-1'] = test_BGQBooter.TestIOBlock('IO-1')

        self.booter = BGQBooter(self.test_blocks, self.block_lock)
        self.booter.restore_boot_id(1)

    def teardown(self):
        #if self.booter.is_alive():
        #    self.booter.close()
        pybgsched.block_dict = {}

    @timeout(3)
    def test_message_creation(self):
        self.booter.start()
        self.booter.initiate_boot('TB-1', 1, 'testuser')
        assert self.booter.all_blocks['TB-1'].under_resource_reservation(1)
        time.sleep(2)
        assert self.booter.pending_boots, 'boot not added: %s' % self.booter.pending_boots

    @timeout(3)
    def test_boot_list(self):
        correct_boot_list_str = "{'block_name': 'TB-1', 'user': 'testuser', 'state': 'pending', 'job_id': 1, 'boot_id': 1} "\
                "{'block_name': 'TB-2', 'user': 'testuser', 'state': 'pending', 'job_id': 2, 'boot_id': 2} "\
                "{'block_name': 'TB-3', 'user': 'testuser', 'state': 'pending', 'job_id': 3, 'boot_id': 3}"
        boot_list = []
        self.booter.start()
        assert self.booter.is_alive(), "Error starting up booter"
        self.booter.suspend_booting()
        assert self.booter.booting_suspended, "Booting not suspended"
        self.booter.initiate_boot('TB-1', 1, 'testuser')
        self.booter.initiate_boot('TB-2', 2, 'testuser')
        self.booter.initiate_boot('TB-3', 3, 'testuser')
        time.sleep(2)
        boot_list = self.booter.stat()
        bl_str = " ".join([str(boot) for boot in boot_list])
        assert boot_list != [] and bl_str == correct_boot_list_str , "Boot list failed: got %s" % bl_str

    @timeout(9)
    def test_boot_sequence(self):
        #set up pybgsched block transitions, treat these as events
        #It's LIFO, so revere everything, and make sure to reset the final state
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        self.booter.start()
        self.booter.initiate_boot('TB-1',1,'testuser')
        while True:
            if self.booter.pending_boots != set():
                break
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if pybgsched.block_dict['TB-1'].statuses == [pybgsched.Block.Initialized]:
                time.sleep(3)
                break
            #assert str(self.booter.stat('TB-1')[0].state) != 'failed'
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state

    @timeout(14)
    def test_reboot_sequence(self):
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        self.booter.start()
        self.booter.initiate_boot('TB-1',1,'testuser')
        while True:
            if self.booter.pending_boots != set():
                break
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if pybgsched.block_dict['TB-1'].statuses == [pybgsched.Block.Initialized]:
                time.sleep(3)
                break
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state
        reboot_count = self.booter.stat('TB-1')[0].context.reboot_attempts
        assert  reboot_count == 1, "Failure: reboot attempts were %s" % reboot_count

    @timeout(20)
    def test_excessive_reboots(self):
        #ensure that we honor the max_reboots variable
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Free)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        self.booter.start()
        self.booter.initiate_boot('TB-1',1,'testuser')
        while True:
            if self.booter.pending_boots != set():
                break
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        for boot in self.booter.pending_boots:
            boot.context.max_reboot_attempts = 3
        while (True):
            time.sleep(1)
            if len(pybgsched.block_dict['TB-1'].statuses)== 1:
                time.sleep(1)
                break
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'failed', 'Boot state not failed, is %s instead' % boot_state
        reboot_count = self.booter.stat('TB-1')[0].context.reboot_attempts
        assert  reboot_count == 3, "Failure: reboot attempts were %s" % reboot_count


    def test_queued_message_fetch(self):
        #this came out of a bug where the deepcopy blew up on an early
        #iteration of the Reap Boot message.  Make sure all messages
        #can be returned by the fetch function of the underlying queue --PMR
        #Run without the queue being started, so we can ensure messages stay put
        self.booter.initiate_boot('TB-1', 1, 'testuser')
        boot = BGQBoot(pybgsched.block_dict['TB-1'], 2, 'testuser', self.block_lock)
        self.booter.send(ReapBootMsg(2))
        pending_messages = ",".join([str(msg) for msg in self.booter.fetch_queued_messages()])
        correct_messages = "<InitiateBootMsg: msg_type=initiate_boot, block_id=TB-1, job_id=1, user=testuser, subblock_parent=None, tag=None, timeout=None>,<ReapBootMsg: boot_id=2>"
        assert pending_messages == correct_messages, "Pending messages failed: expected %s, got %s" % (correct_messages, pending_messages)

    @timeout(10)
    def test_io_boot_normal_sequence(self):
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Booting)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Booting)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Allocated)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Free)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        while True:
            if self.booter.pending_boots != set([]):
                break
        pybgsched.io_block_dict['IO-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if pybgsched.io_block_dict['IO-1'].statuses == [pybgsched.IOBlock.Initialized]:
                time.sleep(3)
                break
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state


    @timeout(10)
    def test_io_compute_simultaneous_boot(self):
        #make sure an IO boot doesn't interfere with a compute boot
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Booting)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Booting)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Allocated)
        pybgsched.io_block_dict['IO-1'].add_status(pybgsched.IOBlock.Free)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        self.booter.initiate_boot('TB-1',1,'testuser')
        while True:
            if self.booter.pending_boots != set([]):
                break
        pybgsched.io_block_dict['IO-1'].set_action(pybgsched.Action._None)
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if (pybgsched.io_block_dict['IO-1'].statuses == [pybgsched.IOBlock.Initialized] and
                    pybgsched.block_dict['TB-1'].statuses == [pybgsched.Block.Initialized]):
                time.sleep(3)
                break
        io_boot_state = str(self.booter.stat('IO-1')[0].state)
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state
        assert io_boot_state == 'complete', 'Boot state not complete, is %s instead' % io_boot_state

    def test_io_boot_already_initialized(self):
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        time.sleep(3)
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'failed', 'Boot state not complete, is %s instead' % boot_state

    def test_io_boot_already_allocated(self):
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Allocated)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        time.sleep(3)
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'failed', 'Boot state not complete, is %s instead' % boot_state

    def test_io_boot_already_booting(self):
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Booting)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        time.sleep(3)
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'failed', 'Boot state not complete, is %s instead' % boot_state

    def test_io_boot_already_terminating(self):
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Terminating)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        time.sleep(3)
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'failed', 'Boot state not complete, is %s instead' % boot_state

    def test_io_boot_already_free_boot_action_set(self):
        pybgsched.io_block_dict['IO-1'].set_action(pybgsched.Action.Boot)
        self.booter.start()
        self.booter.initiate_io_boot('IO-1', 'testuser')
        time.sleep(3)
        boot_state = str(self.booter.stat('IO-1')[0].state)
        assert boot_state == 'failed', 'Boot state not complete, is %s instead' % boot_state

    @timeout(25)
    def test_boot_timeout_completed(self):
        #walk the boot through its transitions, make sure the boot object goes away without external reaping.
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        self.booter.start()
        self.booter.initiate_boot('TB-1', 1, 'testuser', timeout=10)
        while True:
            if self.booter.pending_boots != set():
                break
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if pybgsched.block_dict['TB-1'].statuses == [pybgsched.Block.Initialized]:
                time.sleep(3)
                break
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state
        while(True):
            time.sleep(1)
            boot = self.booter.stat('TB-1')[0]
            if boot.context.force_clean == True:
                self.booter.reap(boot.context.block_id)
                break
        while(True): #Make sure the boot really died
            msg_count = len(self.booter.fetch_queued_messages())
            if msg_count == 0:
                break
        assert len(self.booter.stat('TB-1')) == 0, "Boot should be deleted, but reference still in boot list."

    @timeout(18)
    def test_boot_timeout_failed(self):
        #take a boot into a failed state and make sure that the object is cleaned up within the expected timeout
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Terminating)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        self.booter.start()
        self.booter.initiate_boot('TB-1', 1, 'testuser', timeout=10)
        while True:
            if self.booter.pending_boots != set():
                break
        for boot in self.booter.pending_boots:
            boot.context.max_reboot_attempts = 0
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            current_status = pybgsched.block_dict['TB-1'].statuses
            if current_status == [pybgsched.Block.Terminating]:
                time.sleep(3)
                break
        boot_state = str(self.booter.stat('TB-1')[0].state)
        assert boot_state == 'failed', 'Boot state not failed, is %s instead' % boot_state
        while(True):
            time.sleep(1)
            boot = self.booter.stat('TB-1')[0]
            if boot.context.force_clean == True:
                self.booter.reap(boot.context.block_id)
                break
        while(True): #Make sure the boot really died
            msg_count = len(self.booter.fetch_queued_messages())
            if msg_count == 0:
                break
        assert len(self.booter.stat('TB-1')) == 0, "Boot should be deleted, but reference still in boot list."

    @timeout(10)
    def test_subblock_boot(self):
        #Test to make sure that the right block gets booted if we pass in a block with a different subblock parent.
        self.test_blocks['TB-P'] = test_BGQBooter.TestBlock('TB-P', block_type='pseudoblock', subblock_parent='TB-1')
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Booting)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Allocated)
        pybgsched.block_dict['TB-1'].add_status(pybgsched.Block.Free)
        self.booter.start()
        self.booter.initiate_boot('TB-P', 1, 'testuser')
        while True:
            if self.booter.pending_boots != set():
                break
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action._None)
        while (True):
            time.sleep(1)
            if pybgsched.block_dict['TB-1'].statuses == [pybgsched.Block.Initialized]:
                time.sleep(3)
                break
            #assert str(self.booter.stat('TB-1')[0].state) != 'failed'
        boot_state = str(self.booter.stat('TB-P')[0].state)
        assert boot_state == 'complete', 'Boot state not complete, is %s instead' % boot_state

class test_BootPending(object):

    class TestBlock(object):

        def __init__(self, name, reserved=True, block_type='normal'):
            self.name = name
            self.reserved = reserved
            self.block_type = 'normal'
            self.current_kernel_options=" "
            self.current_kernel = "default"

        def under_resource_reservation(self, job_id):
            return self.reserved

    def setup(self):
        pybgsched.Block('TB-1', 512)
        self.test_blocks = {}
        self.test_blocks['TB-1'] = test_BGQBooter.TestBlock('TB-1')
        self.block_lock = threading.Lock()
        

    def teardown(self):
        pybgsched.block_dict = {}

    def test_not_reserved(self):
        block = self.TestBlock('TB-1', reserved=False)
        context = BootContext(block, 1, 'testuser', self.block_lock)
        next_state = BootPending(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state

    def test_reserved_non_subblock(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        next_state = BootPending(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_control_system_failure(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        pybgsched.Block.set_error('control system failure')
        next_state = BootPending(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state

    def test_initial_subblock(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        block.block_type = 'pseudoblock'
        next_state = BootPending(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_subblock_pending_action(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        block.block_type = 'pseudoblock'
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action.Free)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        next_state = BootPending(context).progress()
        assert 'pending' == str(next_state), "Returned state was %s" % next_state

    def test_subblock_already_initialized(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        block.block_type = 'pseudoblock'
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        next_state = BootPending(context).progress()
        assert 'complete' == str(next_state), "Returned state was %s" % next_state

class test_BootInitiating(object):

    class TestBlock(object):

        def __init__(self, name, reserved=True, block_type='normal'):
            self.name = name
            self.reserved = reserved
            self.block_type = 'normal'
            self.current_kernel = "default"
            self.current_kernel_options=" "

        def under_resource_reservation(self, job_id):
            return self.reserved

    def setup(self):
        pybgsched.Block('TB-1', 512)
        self.test_blocks = {}
        self.test_blocks['TB-1'] = test_BGQBooter.TestBlock('TB-1')
        self.block_lock = threading.Lock()

    def teardown(self):
        pybgsched.block_dict = {}

    def test_not_reserved(self):
        block = self.TestBlock('TB-1', reserved=False)
        context = BootContext(block, 1, 'testuser', self.block_lock)
        next_state = BootInitiating(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state

    def test_continuing_initialization(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Booting)
        next_state = BootInitiating(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Allocated)
        next_state = BootInitiating(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_action_set(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action.Free)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        next_state = BootInitiating(context).progress()
        assert 'rebooting' == str(next_state), "Returned state was %s" % next_state

    def test_go_to_reboot(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Terminating)
        next_state = BootInitiating(context).progress()
        assert 'rebooting' == str(next_state), "Returned state was %s" % next_state
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Free)
        next_state = BootInitiating(context).progress()
        assert 'rebooting' == str(next_state), "Returned state was %s" % next_state

    def test_boot_completion(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        next_state = BootInitiating(context).progress()
        assert 'complete' == str(next_state), "Returned state was %s" % next_state


class test_BootRebooting(object):

    class TestBlock(object):

        def __init__(self, name, reserved=True, block_type='normal'):
            self.name = name
            self.reserved = reserved
            self.block_type = 'normal'
            self.current_kernel_options=" "
            self.current_kernel = "default"

        def under_resource_reservation(self, job_id):
            return self.reserved

    def setup(self):
        pybgsched.Block('TB-1', 512)
        self.test_blocks = {}
        self.test_blocks['TB-1'] = test_BGQBooter.TestBlock('TB-1')
        self.block_lock = threading.Lock()

    def teardown(self):
        pybgsched.block_dict = {}

    def test_reboot_free(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Free)
        next_state = BootRebooting(context).progress()
        assert 'pending' == str(next_state), "Returned state was %s" % next_state

    def test_reboot_initialized(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        next_state = BootRebooting(context).progress()
        assert 'complete' == str(next_state), "Returned state was %s" % next_state

    def test_reboot_initialized_free_pending(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Initialized)
        pybgsched.block_dict['TB-1'].set_action(pybgsched.Action.Free)
        next_state = BootRebooting(context).progress()
        assert 'rebooting' == str(next_state), "Returned state was %s" % next_state

    def test_reboot_booting(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Booting)
        next_state = BootRebooting(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_reboot_allocating(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Allocated)
        next_state = BootRebooting(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_reboot_terminating(self):
        block = self.TestBlock('TB-1')
        context = BootContext(block, 1, 'testuser', self.block_lock)
        context.max_reboot_attempts = 3
        pybgsched.block_dict['TB-1'].set_status(pybgsched.Block.Terminating)
        next_state = BootRebooting(context).progress()
        assert 'rebooting' == str(next_state), "Returned state was %s" % next_state

class test_IOBootPending(object):

    class TestIOBlock(object):
        def __init__(self, name):
            self.name = name
            self.current_kernel = "default"
            self.current_kernel_options=" "

    def setup(self):
        pybgsched.IOBlock('IO-1', 8)
        self.test_blocks = {}
        self.test_blocks['IO-1'] = test_BGQBooter.TestBlock('IO-1')
        self.block_lock = threading.Lock()

    def teardown(self):
        pybgsched.io_block_dict = {}

    def test_progress_initiating(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        next_state = IOBootPending(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_progress_bridge_failure(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.IOBlock.set_error('control system failure')
        next_state = IOBootPending(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state

    def test_progress_already_initialzied(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        next_state = IOBootPending(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state


class test_IOBootInitiating(object):

    class TestIOBlock(object):
        def __init__(self, name):
            self.name = name
            self.current_kernel_options=" "
            self.current_kernel = "default"

    def setup(self):
        pybgsched.IOBlock('IO-1', 8)
        self.test_blocks = {}
        self.test_blocks['IO-1'] = test_BGQBooter.TestBlock('IO-1')
        self.block_lock = threading.Lock()

    def teardown(self):
        pybgsched.io_block_dict = {}

    def test_progress_initiating_free_booting_action(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', 'testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Free)
        pybgsched.io_block_dict['IO-1'].set_action(pybgsched.Action.Boot)
        next_state = IOBootInitiating(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_progress_initiating_allocated(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', 'testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Allocated)
        next_state = IOBootInitiating(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_progress_initiating_booting(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Booting)
        next_state = IOBootInitiating(context).progress()
        assert 'initiating' == str(next_state), "Returned state was %s" % next_state

    def test_progress_initiating_initialized(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        next_state = IOBootInitiating(context).progress()
        assert 'complete' == str(next_state), "Returned state was %s" % next_state

    def test_progress_initiating_initialized_freeing(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Initialized)
        pybgsched.io_block_dict['IO-1'].set_action(pybgsched.Action.Free)
        next_state = IOBootInitiating(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state

    def test_progress_initiating_terminating(self):
        block = self.TestIOBlock('IO-1')
        context = IOBlockBootContext('IO-1', user='testuser')
        pybgsched.io_block_dict['IO-1'].set_status(pybgsched.IOBlock.Terminating)
        next_state = IOBootInitiating(context).progress()
        assert 'failed' == str(next_state), "Returned state was %s" % next_state


