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

