from Cobalt.Util import Timer, disk_writer_thread
from Cobalt.Exceptions import TimerException
import time
import os
import pwd
import errno


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

class TestDiskWriter(object):
    '''Test out the threaded disk writer used by cqm and other components
    mainly for cobaltlog writing to possibly unreliable filesystems.

    '''
    def __init__(self):
        self.dwt = disk_writer_thread()
        #init a series of file objects, some should and some should not exist.
        new_file = os.open('base_cobaltlog', os.O_WRONLY|os.O_CREAT, 0640)
        os.close(new_file)

        new_file = os.open('cobaltlog_bad_perms', os.O_RDONLY|os.O_CREAT, 0440)
        os.close(new_file)

    
    def test_message_queueing(self):
        
        if self.dwt.is_alive():
            self.dwt.send(None)
            time.sleep(10)

        self.dwt.send('test_message')
        msg_list = self.dwt.extract()
        assert 'test_message' == msg_list[0], 'test_message not appriopriately queued. Got %s' % msg_list
        msg_list = self.dwt.extract()
        assert [] == msg_list, 'extract did not clear the list.'
        return

    def test_multiple_message_queueing(self):
        
        if self.dwt.is_alive():
            self.dwt.send(None)
            time.sleep(11)
        
        self.dwt.send('test_message')
        self.dwt.send('test_message')
        self.dwt.send('test_message')
        self.dwt.send('test_message')
        msg_list = self.dwt.extract()
        assert ('test_message'*4) == ''.join(msg_list), 'multiple test_messages not appriopriately queued. Got %s' % msg_list
        msg_list = self.dwt.extract()
        assert [] == msg_list, 'extract did not clear the list.'

    def test_shutdown(self):

        if self.dwt.is_alive():
            self.dwt.send(None)
            time.sleep(10)
        
        self.dwt.daemon = True
        self.dwt.start()
        assert self.dwt.is_alive() == True, 'disk_writer_thread failed to start.'
        self.dwt.send(None)
        time.sleep(10)
        assert self.dwt.is_alive() == False, 'disk_writer_thread failed to shutdown when None sent'
        return

    def test_file_write(self):
        self.dwt.daemon = True
        self.dwt.start()
        user = pwd.getpwuid(os.getuid())[0]
        self.dwt.send(('./base_cobaltlog', 'SUCCESS', user))
        self.dwt.send(None)
        time.sleep(10)
        f = open('./base_cobaltlog')
        count = 0;
        success_found = False
        success_line = ''
        for line in f:
            count += 1
            success_line = line
            if line == 'SUCCESS\n':
                success_found = True
        assert success_found, 'SUCCESS not written to file, found %s instead' % (success_line)
        
        assert count == 1, 'Improper number of lines in file'
        f.close()
        new_file = os.open('./base_cobaltlog', os.O_WRONLY|os.O_TRUNC)
        os.close(new_file)
        return

    def test_nonexistent_file_write(self):
        self.dwt.daemon = True
        self.dwt.start()
        user = pwd.getpwuid(os.getuid())[0]
        self.dwt.send(('./nonexistent_cobaltlog', 'SUCCESS', user))
        self.dwt.send(None)
        time.sleep(10)
        try:
            os.stat('./nonexistent_cobaltlog')
        except OSError as (num, strerror): 
            errcode = errno.errorcode[num]
            assert (errno.ENOENT == num), 'Wrong error status retured from OSError: %s' % errcode 
        else:
            #file must have been found and statted, this is wrong!
            assert False, 'FAILURE: Created a file to write to.'
        return

    def test_bad_perm_write(self):
        self.dwt.daemon = True
        self.dwt.start()
        user = pwd.getpwuid(os.getuid())[0]
        self.dwt.send(('./cobaltlog_bad_perms', 'FAILURE', user))
        self.dwt.send(None)
        time.sleep(10)
        f = open('./cobaltlog_bad_perms')
        lines = f.readlines()
        f.close()
        assert (len(lines) == 0), 'Lines were written to file with wrong permission.'
        return

