'''support classes and routines allowing the use of threads in tests'''

__revision__ = '$Revision:$'

__all__ = ["ThreadSafetyMetaClass", "ComponentProgressThread"]

import inspect
from threading import Thread, RLock, Event
import time
import traceback

class ThreadSafetyMetaClass (type):
    def __init__(cls, name, bases, dict):
        methods = {}
        methods.update(inspect.getmembers(cls, callable))
        for fn_name, fn_orig_ref in methods.iteritems():
            if hasattr(fn_orig_ref, "automatic") or hasattr(fn_orig_ref, 'exposed'):
                fn_new_ref = cls.thread_safety_wrapper(fn_orig_ref)
                fn_new_ref.__dict__.update(fn_orig_ref.__dict__)
                setattr(cls, fn_name, fn_new_ref)
        setattr(cls, '__init__', cls.init_wrapper(methods.get('__init__', None)))
        type.__init__(cls, name, bases, dict)

    @staticmethod
    def init_wrapper(init_func):
        def _init_wrap(self, *args, **kwargs):
            self.mutex = RLock()
            if init_func:
                init_func(self, *args, **kwargs)
        return _init_wrap

    @staticmethod
    def thread_safety_wrapper(func):
        def _thread_safety_wrap(self, *args, **kwargs):
            self.mutex.acquire()
            try:
                return func(self, *args, **kwargs)
            finally:
                self.mutex.release()
        return _thread_safety_wrap

class ComponentProgressThread (Thread):
    def __init__(self, component):
        Thread.__init__(self)
        self.__component = component
        self.__stop = Event()
        self.__stopped = Event()
        self.setDaemon(True)

    def run(self):
        try:
            while not self.__stop.isSet():
                self.__component.do_tasks()
                time.sleep(0.1)
        except:
            traceback.print_exc()
        finally:
            self.__stopped.set()

    def stop(self):
        self.__stop.set()
        self.__stopped.wait()
        self.join()
