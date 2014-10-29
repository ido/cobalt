'''Booting Thread for Cobalt's BGQ system component.

'''
import logging
import threading
import Cobalt.ContextStateMachine
import Cobalt.QueueThread
import Cobalt.Util

from Cobalt.Components.bgq_cn_boot_states import BootPending, BootInitiating, BootRebooting, BootComplete, BootFailed
from Cobalt.Components.bgq_io_boot_states import IOBootPending, IOBootInitiating, IOBootComplete, IOBootFailed
from Cobalt.Data import IncrID
from Cobalt.Util import get_config_option


#FIXME: also make this handle cleanup

import Cobalt.Logging
_logger = logging.getLogger()

Cobalt.Util.init_cobalt_config()

_boot_id_gen = IncrID()

class BootContext(object):

    '''Context for ongonig boot.  This should include any resources specific to that individual boot.
    A pointer to one of these objects is passed to the boot state for processing.

    '''
    def __init__(self, block, job_id, user, block_lock, subblock_parent=None, timeout=None):
        self.block = block
        self.block_id = self.block.name
        self.job_id = job_id
        self.user = user
        self.block_lock = block_lock
        if subblock_parent == None:
            self.subblock_parent = self.block.name
        else:
            self.subblock_parent = subblock_parent

        self.max_reboot_attempts = get_config_option("bgsystem", "max_reboots", "unlimited")
        #config options always come back as strings.  This will be converted to an int, however.
        if str(self.max_reboot_attempts).lower() == 'unlimited':
            self.max_reboot_attempts = None
        else:
            self.max_reboot_attempts = int(self.max_reboot_attempts)
        self.reboot_attempts = 0
        self.status_string = []
        self.reap_timeout = None
        if timeout is not None:
            self.reap_timeout = timeout

    def under_resource_reservation(self):
        '''Return whether or not the block is under a resource reservation.  Handle locking as well for this check.

        '''
        self.block_lock.acquire()
        under_res = self.block.under_resource_reservation(self.job_id)
        self.block_lock.release()
        return under_res

class IOBlockBootContext(object):
    '''Context for IO Block boots. 

    '''
    def __init__(self, io_block_name, job_id=None, user=None, pending_kernel_reboot=False, ion_kerneloptions=None):
        self.io_block_name = io_block_name
        self.job_id = job_id
        self.user = user
        self.status_string = []
        self.pending_kernel_reboot = pending_kernel_reboot
        self.ion_kerneloptions = ion_kerneloptions

class BGQBoot(Cobalt.ContextStateMachine.ContextStateMachine):
    '''Ongoing boot data object. Contains a statemachine for tracking boot progress.

    '''


    _state_list = [BootPending, BootInitiating, BootComplete, BootFailed, BootRebooting,]
    _state_instances = []

    def __init__(self, block, job_id, user, block_lock, subblock_parent=None, boot_id=None, tag=None, timeout=None):
        super(BGQBoot, self).__init__(context=BootContext(block, job_id, user, block_lock, subblock_parent, timeout=timeout),
                initialstate='pending', exceptionstate='failed')
        if boot_id != None:
            self.boot_id = boot_id
        else:
            self.boot_id = _boot_id_gen.next()
        self.tag = tag
        _logger.info("Boot %s initialized.", self.boot_id)

    #def __del__(self):
    #    _logger.debug("Boot %s destroyed.", self.boot_id)

    #get/setstate not allowed.  Should not be used with this class due to the lock and block data reacquistion.  Must be
    #reconstructed at restart --PMR

    def __getstate__(self):
        '''__getstate__ is overriden so that this class cannot be serialized unintentionally.  Reconstitute from constructor.'''
        raise RuntimeError, "Serialization for Boot not allowed, must be reconstructed."

    def __setstate__(self, state):
        '''__setstate__ is overriden so that this class cannot be deserialized unintentionally.  Reconstitute from constructor.'''
        raise RuntimeError, "Deerialization for Boot not allowed, must be reconstructed."

    @property
    def block_id(self):
        '''Identifier of block being booted.'''
        return self.context.block_id

    @property
    def failure_string(self):
        '''In the event of a failed boot, this will have a message about the nature of the failure.'''
        return self.context.failure_string

    def get_details(self):
        return {'boot_id': self.boot_id, 'block_name': self.context.block.name, 'job_id': self.context.job_id,
                'user': self.context.user, 'state': self.state,}

    def __eq__(self, other):
        return self.boot_id == other.boot_id

    def __hash__(self):
        return hash(self.boot_id)

    def pop_status_string(self):
        '''return any available status strings.  Usually messages the user needs to worry about. '''
        if self.context.status_string == []:
            return None
        else:
            return self.context.status_string.pop(0)

class BGQIOBlockBoot(Cobalt.ContextStateMachine.ContextStateMachine):
    '''Boot an IO Block.  This is very similar to the compute boot.

    '''

    global _boot_id_gen
    _state_list = [IOBootPending, IOBootInitiating, IOBootComplete, IOBootFailed]
    _state_instances = []

    def __init__(self, io_block_name, job_id, user, tag='io_boot', reboot=False, ion_kerneloptions=None):
        super(BGQIOBlockBoot, self).__init__(context=IOBlockBootContext(io_block_name, job_id, user, reboot, ion_kerneloptions),
                initialstate='pending', exceptionstate='failed')
        self.io_boot_id = _boot_id_gen.next()
        self.tag = tag
        _logger.info("IO Block Boot on %s initialized.", self.io_boot_id)

    def __del__(self):
        _logger.debug("IO Boot %s destroyed.", self.boot_id)

    @property
    def block_id(self):
        '''Return the name of the io block associated with the boot.'''
        return self.context.io_block_name

    @property
    def boot_id(self):
        '''Return the autogenerated id associated with the boot.'''
        return self.io_boot_id

    def get_details(self):
        return {'io_boot_id': self.io_boot_id, 'tag':self.tag, 'user':self.context.user,
                'io_block_name':self.context.io_block_name, 'state': self.state,}

    def __eq__(self, other):
        return self.io_boot_id == other.io_boot_id

    def __hash__(self):
        return hash(self.io_boot_id)

    def pop_status_string(self):
        '''return any available status strings.  Usually messages the user needs to worry about. '''
        if self.context.status_string == []:
            return None
        else:
            return self.context.status_string.pop(0)


class BGQBooter(Cobalt.QueueThread.QueueThread):
    '''Track boots and reboots.

    '''

    def __init__(self, all_blocks, block_lock, *args, **kwargs):
        '''register handlers for this set of messages
        The start method must be called separately.
        This thread runs itself detached by default.
        Input:
            block_lock -- reference to the thread lock for block data
            all_blocks -- a reference to the blocks list.  This should be all available blocks, not just managed blocks
        '''
        #must be reinstantiated so that it gets the right lock instance, threading locks are not serializable.
        super(BGQBooter, self).__init__(*args, **kwargs)
        self.pending_boots = set()
        self.all_blocks = all_blocks
        self.block_lock = block_lock
        self.boot_data_lock = threading.Lock()
        self.daemon = True
        #register actions to take during the run loop:
        self.booting_suspended = False
        self.register_run_action('progress_boot', self.progress_boot)
        self.register_handler('initiate_boot', self.handle_initiate_boot)
        self.register_handler('initiate_io_boot', self.handle_initiate_io_boot)
        self.register_handler('reap_boot', self.handle_reap_boot)
        _logger.info("Booter Initialized")

    def __getstate__(self):
        #provided as a convenience for later reconstruction
        return {'version': 1, 'next_boot_id': _boot_id_gen.idnum,
                'pending_boots': [boot.get_details() for boot in list(self.pending_boots)],
                'booting_suspended':self.booting_suspended}

    def __setstate__(self, spec):
        raise NotImplementedError, "Setstate is forbidden for this object."

    def restore_boot_id(self, restore_val):
        '''restore the boot id to a saved value.
        '''
        global _boot_id_gen
        _boot_id_gen.idnum = restore_val - 1
        return

    def suspend_booting(self):
        '''Halt boot progress, needed if force-cleaning a block and certain control system actions'''
        self.booting_suspended = True

    def resume_booting(self):
        '''Allow booting to progress again'''
        self.booting_suspended = False

    def stat(self, block_ids=None):
        '''Return pending boot statuses.

        block_ids (default None): a list of blocks id's to return pending boot statuses, if None, apply to all blocks

        '''
        self.boot_data_lock.acquire()
        if block_ids == None:
            boot_set = self.pending_boots
        else:
            boot_set = [pending_boot for pending_boot in list(self.pending_boots) if pending_boot.block_id in block_ids]
        self.boot_data_lock.release()
        return list(boot_set)

    def fetch_status_strings(self, location):
        self.boot_data_lock.acquire()
        status_strings = []
        for boot in self.pending_boots:
            if boot.block_id == location:
                while True:
                    status_string = boot.pop_status_string()
                    if status_string == None:
                        break
                    status_strings.append(status_string)
                break
        self.boot_data_lock.release()
        return status_strings

    def get_boots_by_jobid(self, job_id):
        self.boot_data_lock.acquire()
        boot_set = [pending_boot for pending_boot in list(self.pending_boots) if pending_boot.context.job_id == job_id]
        self.boot_data_lock.release()
        return boot_set

    def cancel(self, block_id, force=False):
        raise NotImplementedError

    def reap(self, block_id):
        '''clear out completed, failed, or otherwise terminated boots

        Only reap boots that are in a terminal state.

        '''
        boots_to_clear = []
        self.boot_data_lock.acquire()
        for boot in self.pending_boots:
            if boot.block_id == block_id and boot.state in ['complete', 'failed']:
                self.send(ReapBootMsg(boot.boot_id))
        self.boot_data_lock.release()
        return

    def handle_reap_boot(self, msg):
        '''Handler function for reap messages, keep boot cleanup contained to the booting thread.

        '''
        retval = False
        try:
            self.boot_data_lock.acquire()
            if msg.msg_type == 'reap_boot':
                found = None
                for boot in self.pending_boots:
                    if hasattr(boot, 'boot_id') and msg.boot_id == boot.boot_id:
                        _logger.debug("found boot at loc %s to reap.", boot.block_id)
                        found = boot
                        break
                if found != None:
                    self.pending_boots.remove(found)
                    _logger.info('Boot for location %s reaped.', found.block_id)
                    retval = True
        finally:
            self.boot_data_lock.release()
        return retval

    def initiate_boot(self, block_id, job_id, user, subblock_parent=None, tag=None, timeout=None):
        '''Asynchrynously initiate a boot.  This will return immediately, the boot should be in the pending state.

        '''
        self.send(InitiateBootMsg(block_id, job_id, user, subblock_parent, tag, timeout))
        _logger.debug("Sent message to initiate boot: %s %s %s %s", block_id, job_id, user, subblock_parent)
        return

    def initiate_io_boot(self, io_block_id, job_id=None, user=None, tag=None, reboot=False, ion_kerneloptions=None):
        self.send(InitiateIOBootMsg(io_block_id, job_id, user, tag, reboot, ion_kerneloptions))
        _logger.debug("Sent message to initiate IO boot: %s %s %s", io_block_id, user, tag)
        return

    def progress_boot(self, test_delay=0):
        '''callback to be registered with the run method.
        This gets executed after all messages have been parsed.

        '''
        if not self.booting_suspended:
            #A boot could get reaped in the middle of this.
            self.boot_data_lock.acquire()
            for boot in self.pending_boots:
                boot.progress()
                try:
                    #for race-condition testing
                    if test_delay !=0:
                        _logger.debug('sleeping for %s' , test_delay)
                        Cobalt.Util.sleep(test_delay)
                except Exception:
                    self.boot_data_lock.release()
                    raise
            self.boot_data_lock.release()
        return

    def handle_initiate_boot(self, msg):
        '''callback for handling an initate boot message and constructing the boot object

        '''
        retval = False
        try:
            self.boot_data_lock.acquire()
            if msg.msg_type == 'initiate_boot':
                new_boot = BGQBoot(self.all_blocks[msg.block_id], msg.job_id, msg.user, self.block_lock,
                        self.all_blocks[msg.block_id].subblock_parent, tag=msg.tag,
                        timeout=msg.timeout)
                self.pending_boots.add(new_boot)
                retval = True
        except AttributeError:
            #We apparently cannot handle this message as it lacks a message type
            #take no action and let another handler try the message
            pass 
        finally:
            self.boot_data_lock.release()
        return retval

    def handle_initiate_io_boot(self, msg):
        '''Handler for incoming IO boot request messages.

        '''
        retval = False
        try:
            self.boot_data_lock.acquire()
            if msg.msg_type == 'initiate_io_boot':
                new_io_boot = BGQIOBlockBoot(msg.io_block_name, msg.job_id, msg.user, msg.tag, msg.reboot, msg.ion_kerneloptions)
                self.pending_boots.add(new_io_boot)
                retval = True
        except AttributeError:
            pass
        finally:
            self.boot_data_lock.release()
        return retval

    def has_pending_boot(self, job_id):
        '''Check to see if there is a pending boot in the message queue, or in the list of current boots

        '''
        retval = False
        queued_boots = self.fetch_queued_messages()
        for boot_msg in queued_boots:
            if job_id == boot_msg.job_id:
                retval = True
                break
        if not retval:
            if self.get_boots_by_jobid(job_id) != []:
                retval = True
        return retval

#Boot messages, possibly break out into separate file
class InitiateBootMsg(object):

    def __init__(self, block_id, job_id, user, subblock_parent=None, tag=None, timeout=None):
        self.msg_type = 'initiate_boot'
        self.block_id = block_id
        self.job_id = job_id
        self.user = user
        self.subblock_parent = subblock_parent
        self.tag = tag
        self.timeout = timeout

    def __str__(self):
        return "<InitiateBootMsg: msg_type=%s, block_id=%s, job_id=%s, user=%s, subblock_parent=%s, tag=%s, timeout=%s>" % \
                (self.msg_type, self.block_id, self.job_id, self.user, self.subblock_parent, self.tag, self.timeout)


class ReapBootMsg(object):
    def __init__(self, boot_id):
        self.msg_type = 'reap_boot'
        self.boot_id = boot_id

    def __str__(self):
        return "<ReapBootMsg: boot_id=%s>" % self.boot_id

#classes for IO booting let the boot thread do both
class InitiateIOBootMsg(object):
    def __init__(self, io_block_name, job_id=None, user=None, tag='io_boot', reboot=False, ion_kerneloptions=None):
        self.msg_type = 'initiate_io_boot'
        self.io_block_name = io_block_name
        self.user = user
        self.tag = tag
        self.job_id = job_id
        self.reboot = reboot
        self.ion_kerneloptions = ion_kerneloptions

class InitiateIOFreeMsg(object):
    def __init__(self, io_block_name, user=None):
        self.msg_type = 'initiate_io_free'
        self.io_block_name = io_block_name
