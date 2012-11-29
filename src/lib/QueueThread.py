import Queue
import threading
import logging
import Cobalt.Util

_logger = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

class QueueThread(threading.Thread):

    '''Run a thread with a queue in place for message passing

    '''

    identity = 'generic'

    def __init__(self):
        '''Initializes the queue and thread for use.  This does not start the thread.

        '''
        super(QueueThread, self).__init__()
        self.msg_queue = Queue.Queue()
        self.msg_validators = {}
        self.msg_handlers = {}
        self.hold = False

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

    def run(self):

        while(True):

            if self.msg_queue.empty() or self.hold:
                #no work to do, just iterate
                Cobalt.Util.sleep(1)

            curr_msg = self.msg_queue.get()
            # Terminate this queue if None is sent as a message
            if curr_msg == None:
                self.msg_queue.task_done()
                break

            handled = False
            for name, handler in self.msg_handlers.items():
                try:
                    handled = handled or handler(curr_msg)
                except Exception as exc:
                    _logger.critical("Queue: %s Handler failure: in %s, Exception info follows:", self.identity, name, exc_info=True)
                    _logger.critical("Queue: %s Message causing failure was: %s", self.identity, curr_msg)
            if not handled:
                _logger.warning("No handlers for message %s", curr_msg)
            self.msg_queue.task_done()

        #End of while(True)
# End of class QueueThread
