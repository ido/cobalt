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

    def get_messages(self):
        element_list =[]
        while not self.msg_queue.empty():
            element_list.append(self.message_queue.get())
        for e in element_list:
            self.message_queue.put()
        return element_list

    def halt_processing(self):
        self.hold = True

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
            for name, handler in self.msg_handlers.iteritems():
                try:
                    handled = handler(curr_msg)
                    if handled:
                        break
                except Exception as exc:
                    _logger.critical("Queue: %s Handler failure: in %s, Exception info follows:", self.identity, name, exc_info=True)
                    _logger.critical("Queue: %s Message causing failure was: %s", self.identity, curr_msg)
            if not handled:
                _logger.warning("No handlers for message %s", curr_msg)
            self.msg_queue.task_done()

        #End of while(True)

from nose.tools import *

class TestQueueThread(object):

    def setup(self):
        self.qt = QueueThread()
        self.qt.daemon = True
        self.action = False

    def teardown(self):
        if self.qt.is_alive():
            self.qt.close()

    def handler_1(self, msg):
        if msg == 'a':
            self.action = True
            return True
        return False

    def handler_2(self, msg):
        if msg == 'b':
            self.action = True
            return True
        return False

    def handle_check_object(self, msg):
        if str(msg) == 'check object':
            self.action = True
            return True
        return False

    def validator_1(self, msg):
        if msg != 'a':
            raise ValidationError("test_validator_1 failed")

    def other_exception_validator(self, msg):
        raise RuntimeError("Test Failure")

    class checkObject(object):
        def __str__(self):
            return 'check object'

    def test_start_not_active(self):
        assert not self.qt.is_alive(), "Thread started active"

    def test_close(self):
        self.qt.start()
        self.qt.close()
        alive = self.qt.is_alive()
        assert not alive, "Thread still active after close"

    def test_null_handler(self):
        self.qt.start()
        self.qt.send('test_msg')
        assert self.action == False, "Action was %s" % self.action

    @raises(ValidationError)
    def test_validator(self):
        self.qt.start()
        self.qt.register_validator("validator", self.validator_1)
        self.qt.send('foo')
        return

    def test_bad_validator(self):
       self.qt.start()
       self.qt.register_validator("validator", self.other_exception_validator)
       self.qt.send('foo')
       Cobalt.Util.sleep(5)
       assert not self.action, "Action taken after failed validation"

    def test_msg_handling(self):
        self.qt.start()
        self.qt.register_handler("handle_a", self.handler_1)
        self.qt.send("a")
        Cobalt.Util.sleep(2)
        assert self.action, "No Action Taken!"

