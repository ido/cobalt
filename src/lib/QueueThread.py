'''A Queue.queue paired with a comsumer thread with regiserable handlers and validator functions.

'''

import Queue
import threading
import logging
import Cobalt.Util
import Cobalt.Logging
import copy

_logger = logging.getLogger(__name__)

class ValidationError(Exception):
    '''Exception to indicate that a message failed to validate.  Should be raised from within a validator.

    '''
    pass

class QueueThread(threading.Thread):

    '''Run a thread with a queue in place for message passing

    '''

    identity = 'generic'

    def __init__(self, *args, **kwargs):
        '''Initializes the queue and thread for use.  This does not start the thread.

        '''
        super(QueueThread, self).__init__(*args, **kwargs)
        self.msg_queue = Queue.Queue()
        self.msg_validators = {}
        self.msg_handlers = {}
        self.run_callbacks = {}
        self.hold = False
        self.msg_queue_process_lock = threading.Lock()

    def send(self, msg):
        '''Add a message to the queue, should the queue be full, will raise the Queue.Empty exception
        Sending None will cause the thread to terminate.

        '''
        for name, validator in self.msg_validators.iteritems():
            try:
                validator(msg)
            except ValidationError as exc:
                _logger.info("Validation failed: queue: %s validator: %s", self.identity, name, exc_info=True)
                raise exc
            except Exception as  exc:
                _logger.critical("Unexpected Exception recieved in queue %s:", self.identity, exc_info=True)
        _logger.debug("Adding message: %s", str(msg))
        self.msg_queue.put(msg)

    def close(self):
        '''Termninate the thread and block until all messages have been processed.

        '''
        self.msg_queue.put(None)
        self.msg_queue.join()

    def register_handler(self, name, func):
        '''Add a new handler to apply to messages.

        '''
        self.msg_handlers[name] = func

    def register_validator(self, name, func):
        '''Add a new validator for messages.

        '''
        self.msg_validators[name] = func

    def unregister_handler(self, name):
        '''Remove a message handler

        '''
        del self.msg_handlers[name]

    def unregister_validator(self, name):
        '''Remove a validation step

        '''
        del self.msg_validators[name]

    def register_run_action(self, name, func):
        '''Register actions to take during the running of the thread.
        These are called post-message handling.

        '''
        self.run_callbacks[name] = func

    def unregister_run_action(self, name):
        '''Remove an action from the running of the thread.

        '''
        del self.run_callbacks[name]

    @property
    def handlers(self):
        '''List the names of registered message handlers

        '''
        return self.msg_handlers.keys()

    @property
    def validators(self):
        '''List the names of registered message handlers

        '''
        return self.msg_validators.keys()

    @property
    def callbacks(self):
        '''List the names of registered message handlers

        '''
        return self.run_callbacks.keys()

    def fetch_queued_messages(self):
        '''Return a list of messages that are currently in the queue that have yet to be processed.

        '''
        self.msg_queue_process_lock.acquire()
        retitems = []
        try:
            queued_items = list(self.msg_queue.queue)
            retitems = copy.deepcopy(queued_items)
        except Exception:
            #we must preserve the thread.  Report the traceback, but try to continue on.
            _logger.critical("Queue: %s Unexpected fetch_queued_messages failure, Exception info follows:",
                    self.identity, exc_info=True)
        finally:
            self.msg_queue_process_lock.release()
        return retitems

    def handle_queued_messages(self):
        '''Pull messages off the queue and invoke handlers.

        '''
        empty = False
        while(not empty):
            if self.msg_queue.empty() or self.hold:
                #no work to do, just iterate
                empty = True
            else:
                self.msg_queue_process_lock.acquire()
                curr_msg = self.msg_queue.get()
                # Terminate this queue if None is sent as a message
                if curr_msg == None:
                    self.msg_queue.task_done()
                    return True

                handled = False
                for name, handler in self.msg_handlers.items():
                    try:
                        handled = handled or handler(curr_msg)
                    except Exception:
                        _logger.critical("Queue: %s Handler failure: in %s, Exception info follows:", self.identity, name, 
                                exc_info=True)
                        _logger.critical("Queue: %s Message causing failure was: %s", self.identity, curr_msg)
                if not handled:
                    _logger.warning("No handlers for message %s", curr_msg)

                self.msg_queue.task_done()
                self.msg_queue_process_lock.release()
        return False

    def run(self):
        '''Pull messages off the queue and apply handlers.  If you have additional work to perofrm 
        in this thread, override this method.  You will have to make sure to call handle_queued_messages in
        the overriden code as well.

        '''
        shutdown = False
        while(not shutdown):
            shutdown = self.handle_queued_messages()
            for name, callback in self.run_callbacks.items():
                try:
                    callback()
                except Exception:
                    #Must keep the thread running.  Catch and log exceptions that are raised.
                    _logger.critical("Queue: %s Action failure: in %s, Exception info follows:", self.identity, name, exc_info=True)
                    _logger.critical("Queue: %s Action Exception unhandled, trapping to preserve thread.", self.identity)

            Cobalt.Util.sleep(1) #FIXME: make this an adjustable time
        #End of while(True)
