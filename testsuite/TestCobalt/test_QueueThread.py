from Cobalt.QueueThread import *
from nose.tools import *
import sys

_logger = Cobalt.QueueThread._logger

class TestQueueThread(object):

    global _logger
    _logger.addHandler(logging.StreamHandler(sys.stdout))

    def setup(self):
        self.qt = QueueThread()
        self.qt.daemon = True
        self.action = False

    def teardown(self):
        if self.qt.is_alive():
            self.qt.close()
        self.qt = None

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
        #'''Thread must not be started by the initializer.

        #'''
        assert not self.qt.is_alive(), "Thread started active"

    def test_close(self):
        #'''Ensure close kills the thread.

        #'''
        self.qt.start()
        self.qt.close()
        Cobalt.Util.sleep(2)
        alive = self.qt.is_alive()
        assert not alive, "Thread still active after close"

    def test_null_handler(self):
        #'''Do nothing with a message if no handlers defined.

        #'''
        assert not self.action, "Action not false"
        self.qt.start()
        self.qt.send('test_msg')
        assert self.action == False, "Action was %s" % self.action

    @raises(ValidationError)
    def test_validator(self):
        #'''Make sure that a failed validation raises appropraite exception.

        #'''
        self.qt.start()
        self.qt.register_validator("validator", self.validator_1)
        self.qt.send('foo')
        return

    def test_bad_validator(self):
        #'''Ensure that a validator throwing a non-validator error, doesn't propigate
        #the message.

        #'''
        assert not self.action, "Action not false"
        self.qt.start()
        self.qt.register_validator("validator", self.other_exception_validator)
        self.qt.send('foo')
        Cobalt.Util.sleep(5)
        assert not self.action, "Action taken after failed validation"

    def test_msg_handling(self):
        #'''Basic message handler functionality

        #'''
        assert not self.action, "Action not false"
        self.qt.start()
        self.qt.register_handler("handle_a", self.handler_1)
        self.qt.send("a")
        Cobalt.Util.sleep(2)
        assert self.action, "No Action Taken!"

    def test_multi_handler_pass(self):
        #'''Ensure that registering multiple handlers works as expected.

        #'''
        assert not self.action, "Action not false"
        self.qt.start()
        self.qt.register_handler("handle_a", self.handler_1)
        self.qt.register_handler("handle_b", self.handler_2)
        self.qt.send("a")
        Cobalt.Util.sleep(1)
        assert self.action, "No action for a"
        self.action = False
        self.qt.send("b")
        Cobalt.Util.sleep(1)
        assert self.action, "No action for b"
        self.action = False
        self.qt.send('a')
        self.qt.send('b')
        Cobalt.Util.sleep(5)
        assert self.qt.msg_queue.empty(), "Queue not cleared."
        assert self.action, "Actions not taken"

    def test_multi_handler_miss(self):
        #'''Ensure that multiple handlers register missing a message.

        #'''
        self.qt.start()
        self.qt.register_handler("handle_a", self.handler_1)
        self.qt.register_handler("handle_b", self.handler_2)
        self.qt.send('c')
        Cobalt.Util.sleep(2)
        assert not self.action, "Inappropraite action taken"

    def test_obj_handler(self):
        #'''Check arbitrary object handler

        #'''
        self.qt.start()
        self.qt.register_handler("object", self.handle_check_object)
        test_obj = self.checkObject()
        self.qt.send(test_obj)
        Cobalt.Util.sleep(2)
        assert self.action, "Action not taken for object test."

