from Cobalt.Util import Timer
from Cobalt.Exceptions import TimerException
import time

class TestTimers (object):
    def test_elapsed_timer(self, reps = 5):
        sleep_time = 1
        tolerance = 0.1
        start_times = []
        stop_times = []
        t = Timer()
        for n in range(reps):
            assert not t.is_active
            assert len(t.start_times) == n
            assert len(t.stop_times) == n
            start_times.append(time.time())
            t.start()
            time.sleep(sleep_time)
            assert t.is_active
            assert len(t.start_times) == n + 1
            assert len(t.stop_times) == n
            t.stop()
            stop_times.append(time.time())
            assert not t.is_active
            assert len(t.start_times) == n + 1
            assert len(t.stop_times) == n + 1
            assert abs(t.elapsed_time - (n + 1) * sleep_time) < (n + 1) * tolerance
        for n in range(reps):
            assert abs(t.start_times[n] - start_times[n]) < tolerance
            assert abs(t.stop_times[n] - stop_times[n]) < tolerance

    def test_countdown_timer(self):
        sleep_time = 1
        t = Timer(1.5 * sleep_time)
        assert t.max_time == 1.5 * sleep_time
        t.start()
        time.sleep(sleep_time)
        assert not t.has_expired
        time.sleep(sleep_time)
        assert t.has_expired
        t.max_time = 3.0 * sleep_time
        assert not t.has_expired
        time.sleep(sleep_time)
        assert t.has_expired
        t.stop()
