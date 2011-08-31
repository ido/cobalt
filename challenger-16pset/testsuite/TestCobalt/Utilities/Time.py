'''time utilities'''

__revision__ = '$Revision:$'

__all__ = ["timeout"]

from nose.tools import TimeExpired, make_decorator
import signal
import sys

def _timeout_signal_handler(signum, frame):
    raise TimeExpired

def timeout(limit):
    """Test must finish within specified time limit or it is aborted"""
    def decorate(func):
        def newfunc(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_signal_handler)
            try:
                signal.alarm(int(limit + 1.0 // 1))
                rc = func(*args, **kwargs)
                signal.alarm(0)
            except TimeExpired:
                exc_cls, exc, tb = sys.exc_info()
                raise exc_cls, TimeExpired("Time limit (%s) exceeded" % limit), tb
            finally:
                signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return rc
        newfunc = make_decorator(func)(newfunc)
        return newfunc
    return decorate
