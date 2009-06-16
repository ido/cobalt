'''support classes and routines allowing the use of threads in tests'''

__revision__ = '$Revision:$'

__all__ = ["ThreadSafeComponent", "ComponentProgressThread", "OtherThreadException"]

import atexit
import inspect
import sys
from threading import Thread, Lock, RLock, Condition
import time
import traceback

class OtherThreadException (Exception):
    def __init__(self, exc_info = None):
        self.args = ("An exception occurred in another thread", exc_info)
        self.exc_info = exc_info

# class ThreadSafetyMetaClass (type):
#     def __init__(cls, name, bases, dict):
#         methods = {}
#         methods.update(inspect.getmembers(cls, callable))
#         for fn_name, fn_orig_ref in methods.iteritems():
#             if hasattr(fn_orig_ref, "automatic") or hasattr(fn_orig_ref, 'exposed') or hasattr(fn_orig_ref, 'query'):
#                 fn_new_ref = cls.thread_safety_wrapper(fn_orig_ref)
#                 fn_new_ref.__dict__.update(fn_orig_ref.__dict__)
#                 setattr(cls, fn_name, fn_new_ref)
#         setattr(cls, '__init__', cls.init_wrapper(methods.get('__init__', None)))
#         type.__init__(cls, name, bases, dict)
# 
#     @staticmethod
#     def init_wrapper(init_func):
#         def _init_wrap(self, *args, **kwargs):
#             self.__ts_mutex = RLock()
#             self.__ts_exception = None
#             if init_func:
#                 init_func(self, *args, **kwargs)
#         return _init_wrap
# 
#     @staticmethod
#     def thread_safety_wrapper(func):
#         def _thread_safety_wrap(self, *args, **kwargs):
#             # if self.__ts_exception != None:
#             #     raise OtherThreadException(self.__ts_exception)
#             self.__ts_mutex.acquire()
#             try:
#                 return func(self, *args, **kwargs)
#             except:
#                 self.__ts_exception = sys.exc_info()
#                 raise
#             finally:
#                 self.__ts_mutex.release()
#         return _thread_safety_wrap

class ThreadSafeComponent (type):
    def __init__(cls, name, bases, dict):
        methods = {}
        methods.update(inspect.getmembers(cls, callable))
        for fn_name, fn_orig_ref in methods.iteritems():
            if hasattr(fn_orig_ref, "automatic") or hasattr(fn_orig_ref, 'exposed') or hasattr(fn_orig_ref, 'query'):
                fn_new_ref = cls.thread_safety_wrapper(fn_orig_ref)
                fn_new_ref.__dict__.update(fn_orig_ref.__dict__)
                setattr(cls, fn_name, fn_new_ref)
        setattr(cls, '__init__', cls.init_wrapper(methods.get('__init__', None)))
        type.__init__(cls, name, bases, dict)

    @staticmethod
    def init_wrapper(init_func):
        def _init_wrap(self, *args, **kwargs):
            # self.__ts_mutex = RLock() -- now defined in Component as self.lock
            self.__ts_exception = None
            if init_func:
                init_func(self, *args, **kwargs)
        return _init_wrap

    @staticmethod
    def thread_safety_wrapper(func):
        def _thread_safety_wrap(self, *args, **kwargs):
            # if self.__ts_exception != None:
            #     raise OtherThreadException(self.__ts_exception)
            need_to_lock = not getattr(func, 'locking', False)
            if need_to_lock:
                self.lock.acquire()
            try:
                return func(self, *args, **kwargs)
            except:
                self.__ts_exception = sys.exc_info()
                raise
            finally:
                if need_to_lock:
                    self.lock.release()
        return _thread_safety_wrap

class ComponentProgressThread (Thread):
    def __init__(self, component):
        Thread.__init__(self)
        self.__component = component
        self.__pause = False
        self.__stop = False
        self.__paused = False
        self.__stopped = True
        self.__lock = Lock()
        self.__cond = Condition(self.__lock)
        atexit.register(self.atexit_stop)
        self.setDaemon(True)

    def run(self):
        try:
            self.__stopped = False
            while self.__stop == False:
                self.__component.do_tasks()
                if self.__pause:
                    try:
                        self.__lock.acquire()
                        self.__paused = True
                        self.__cond.notify()
                        while self.__pause:
                            self.__cond.wait()
                        self.__paused = False
                        self.__cond.notify()
                    finally:
                        self.__lock.release()
                else:
                    time.sleep(0.1)
        # except OtherThreadException:
        #     pass
        except:
            traceback.print_exc()
        finally:
            try:
                self.__lock.acquire()
                self.__stopped = True
                self.__cond.notify()
            finally:
                self.__lock.release()

    def stop(self):
        try:
            self.__lock.acquire()
            self.__pause = False
            self.__stop = True
            self.__cond.notify()
            while not self.__stopped:
                self.__cond.wait()
        finally:
            self.__lock.release()
        self.join()

    def atexit_stop(self):
        if not self.__stopped:
            self.stop()

    def pause(self):
        try:
            self.__lock.acquire()
            self.__pause = True
        finally:
            self.__lock.release()

    def pause_wait(self):
        try:
            self.__lock.acquire()
            while not self.__paused:
                self.__cond.wait()
        finally:
            self.__lock.release()

    def resume(self):
        try:
            self.__lock.acquire()
            self.__pause = False
            self.__cond.notify()
        finally:
            self.__lock.release()

    def resume_wait(self):
        try:
            self.__lock.acquire()
            while self.__paused and not self.__stopped:
                self.__cond.wait()
        finally:
            self.__lock.release()
