# no one could possibly need more than a million kinds of exceptions?  right?
fault_code_counter = xrange(1000, 1000000).__iter__()

class NoExposedMethod (Exception):
    """There is no method exposed with the given name."""

class ProcessGroupCreationError (Exception):
    """An error occured when creation a process group."""

class TimerException(Exception):
    '''This error occurs when timer methods are called in the wrong order'''

class DataCreationError (Exception):
    '''Used when a new object cannot be created'''

class IncrIDError (Exception):
    '''Used when trying to set the IncrID counter to a value that has already been used'''

class ComponentError (Exception):
    """Component error baseclass"""

class ComponentOperationError (ComponentError):
    """Component Failure during operation"""

class NodeAllocationError (ComponentError):
    """Component failed to allocate nodes"""


class ReservationError(Exception):
    """An error has occured creating a reservation"""
    log = False
    fault_code = fault_code_counter.next()

class QueueError(Exception):
    '''This error indicates a problem with a queue'''
    log = False
    fault_code = fault_code_counter.next()

class TimeFormatError (Exception):
    '''This error is raised by Cobalt.Util.get_time'''
    fault_code = fault_code_counter.next()

class ComponentLookupError (ComponentError):
    """Unable to locate an address for the given component."""
    fault_code = fault_code_counter.next()

class JobValidationError(Exception):
    """This error indicates that a job could not be validated."""
    log = False
    fault_code = fault_code_counter.next()

class NotSupportedError(Exception):
    log = False
    fault_code = fault_code_counter.next()

class JobProcessingError (Exception):
    fault_code = fault_code_counter.next()
    def __init__(self, msg, jobid, user, state, sm_state, sm_event):
        self.args = (msg, jobid, user, state, sm_state, sm_event)
        self.message = msg
        self.jobid = jobid
        self.user = user
        self.state = state
        self.sm_state = sm_state
        self.sm_event = sm_event

class JobPreemptionError (Exception):
    log = False
    fault_code = fault_code_counter.next()
    def __init__(self, msg, jobid, user, force):
        self.args = (msg, jobid, user, force)
        self.message = msg
        self.jobid = jobid
        self.user = user
        self.force = force

class JobRunError (Exception):
    log = False
    fault_code = fault_code_counter.next()
    def __init__(self, msg, jobid, state, sm_state):
        self.args = (msg, jobid, state, sm_state)
        self.message = msg
        self.jobid = jobid
        self.state = state
        self.sm_state = sm_state

class JobDeleteError (Exception):
    log = False
    fault_code = fault_code_counter.next()
    def __init__(self, msg, jobid, user, force, state, sm_state):
        self.args = (msg, jobid, user, force, state, sm_state)
        self.message = msg
        self.jobid = jobid
        self.user = user
        self.force = force
        self.state = state
        self.sm_state = sm_state

class DataStateError(Exception):
    log = True
    fault_code = fault_code_counter.next()

class DataStateTransitionError(Exception):
    log = True
    fault_code = fault_code_counter.next()

class StateMachineError (Exception):
    log = True
    fault_code = fault_code_counter.next()

class StateMachineIllegalEventError (Exception):
    log = True
    fault_code = fault_code_counter.next()

class StateMachineNonexistentEventError (Exception):
    log = True
    fault_code = fault_code_counter.next()

class ThreadPickledAliveException (Exception):
    log = True
    fault_code = fault_code_counter.next()
