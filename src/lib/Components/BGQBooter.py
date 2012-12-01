import threading
import Queue
import logging
import Cobalt.QueueThread
from Cobalt.QueueThread import ValidatorError
import threading

#Note: should this also handle up cleanup actions?


_logger = logging.getLogger(__name__)

class DupicateStateError(Exception):
    pass

class BaseState(object):

    def __init__(self, callback=None):
        self.__destination_states = frozenset([])
        self.name = None
        self.callback = callback

    def exit(self):
        '''Actions to execute on exiting a state

        '''
        pass

    def progress(self):
        raise NotImplementedError('Progress has not been overridden.')

    def validate_transition(self, new_state):
        '''Take terminal actions for new state

        '''
        if new_state.name not in self.__destination_states:
            return False
        return True

class BootPending(BaseState):

    def __init__(self, callback):
        super(BootPending, self).__init__()
        self.__destination_states = frozenset(['initiated','complete','canceled'])
        self.name = 'pending'
        self.callback = callback

    def progress(self):
        #Make sure we have the lock for this resource, set user and start booting.
        #Subblocks change this, potentially.
        check_lock()

class BootInitiated(BaseState):
    pass

class BootComplete(BaseState):
    pass

class BootFailed(BaseState):
    pass

class BootRebooting(BaseState):
    pass

class BootCanceled(BaseState):
    pass

class Boot(BaseStateMachineDriver):
    '''Ongoing boot data object

    '''

    __state_list = [BootPending, BootInitiated, BootComplete, BootFailed, BootRebootng,
            BootCanceled]

    def __init__(self, block_id, job_id,
            subblock_parent=None):

        state_list

        super(Boot, self).__init__(__state_list
        self.block_id = block_id
        self.job_id = job_id
        if subblock_parent != None:
            self.subblock_parent = block_id
        else:
            self.subblock_parent = subblock_parent
        self.reboot_attempts = 0
        self.status = 'pending'
        self.bgsched_block_state = None
        self.__state = BootPending()


class BaseStateMachineDriver(object):
    '''Mixin class to add a class-based statemachine

    '''

    __known_states = {}

    def __init__(self, *args, **kwargs):
        register_states(kwargs['state_list'])
        self.__state = kwargs['initial_state']

    def register_states(self, state_list):
        for state in state_list:
            if arg.name not in __known_states.keys()
                __known_states[arg.name] = arg
            else:
                raise DuplicateStateError

    def setState(self, state_name):
        #the __known_states dict holds the actual classes.
        #This creates an instance of the class listed in the table for that transition.
        if self.__state.validate_transition(state_name):
            self.__state = __known_states[state_name]()
        else:
            raise RuntimeError("Invalid state transition")

    def progress(self):
        self.__state.progress()

class BGQBooter(Cobalt.QueueThread.QueueThread):
    '''Track boots and reboots.

    '''

    def __init__(self, *args, **kwargs):
        '''register handlers for this set of messages

        '''
        super(BGQBooter, self).__init__(*args, **kwargs)
        self.pending_boots = set()
        self.boot_data_lock = threading.Lock()

    def stat(self, block_ids=None):
        '''Return pending boot statuses.

        block_ids (default None): a list of blocks id's to return pending boot statuses, if None, apply to all blocks

        '''
        self.boot_data_lock.acquire()
        if block_ids == None:
            boot_set = list(self.pending_boots)
        else:
            boot_set = set([pending_boot for pending_boot in list(self.pending_boots) if pending_boot.block_id in block_ids])
        self.boot_data_lock.release()
        return list(boot_set)

    def reap(self, boot_id=None):
        '''clear out completed, failed, or otherwise terminated boots

        '''
        pass

    def progress_boot(self):
        '''callback to be registered with the run method.
        This gets executed after all messages have been parsed.

        '''
        self.boot_data_lock.acquire()
        for boot in self.pending_boots:
            boot.progress()
        self.boot_data_lock.release()

