import time
import os
import pwd
import errno
import tempfile
import re
NamedTemporaryFile = tempfile.NamedTemporaryFile

import Cobalt.Util
Timer = Cobalt.Util.Timer
disk_writer_thread = Cobalt.Util.disk_writer_thread
init_cobalt_config = Cobalt.Util.init_cobalt_config
check_required_options = Cobalt.Util.check_required_options
get_config_option = Cobalt.Util.get_config_option
ParsingError = Cobalt.Util.ParsingError
NoSectionError = Cobalt.Util.NoSectionError
NoOptionError = Cobalt.Util.NoOptionError
import Cobalt.Exceptions
TimerException = Cobalt.Exceptions.TimerException

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
            m = re.match(r'[a-zA-Z]+ [a-zA-Z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [0-9]+ [+-][0-9]+ \([a-zA-Z]+\) SUCCESS\n', line)
            if m is not None:
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

class TestConfig (object):
    def setup(self):
        Cobalt.CONFIG_FILES = []
        Cobalt.Util.config = None
        self.file_objects = []

    def teardown(self):
        Cobalt.CONFIG_FILES = []
        Cobalt.Util.config = None
        for fo in self.file_objects:
            fo.close()
        del self.file_objects

    def test_init_cobalt_config_no_files(self):
        Cobalt.CONFIG_FILES = []
        files = init_cobalt_config()
        assert len(files) == 0

    def test_init_cobalt_config_nonexistent_file(self):
        Cobalt.CONFIG_FILES = ["/foo/bar/baz/bif.conf"]
        files = init_cobalt_config()
        assert len(files) == 0

    def test_init_cobalt_config_missing_section(self):
        fn = self._create_config_file("""
setting = 1
""")
        Cobalt.CONFIG_FILES = [fn]
        try:
            files = init_cobalt_config()
            assert fn not in files, "bad config file was successfully parsed"
            assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
            assert False, "init_cobalt_config returned successfully"
        except ParsingError, e:
            pass

    def test_init_cobalt_config_bad_option(self):
        fn = self._create_config_file("""
[foo]
setting
""")
        Cobalt.CONFIG_FILES = [fn]
        try:
            files = init_cobalt_config()
            assert fn not in files, "bad config file was successfully parsed"
            assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
            assert False, "init_cobalt_config returned successfully"
        except ParsingError, e:
            pass

    def test_init_cobalt_config_empty_file(self):
        fn = self._create_config_file("")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"

    def test_init_cobalt_config_simple_file(self):
        fn = self._create_config_file("""
[foo]
setting = 1
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"

    def test_init_cobalt_config_multiple_files(self):
        fn1 = self._create_config_file("""
[foo]
setting = 1
""")
        fn2 = self._create_config_file("""
[bar]
setting = 2
""")
        Cobalt.CONFIG_FILES = [fn1, fn2]
        files = init_cobalt_config()
        assert fn1 in files, "first config file was not parsed"
        assert fn2 in files, "second config file was not parsed"
        assert len(set(files).difference((fn1, fn2))) == 0, "unknown config file was successfully parsed"

    def test_init_cobalt_config_multiple_files_one_missing(self):
        fn1 = self._create_config_file("""
[foo]
setting = 1
""")
        fn2 = self._create_config_file("""
[bar]
setting = 2
""")
        Cobalt.CONFIG_FILES = [fn1, fn2, "/foo/bar/baz/bif.conf"]
        files = init_cobalt_config()
        assert fn1 in files, "first config file was not parsed"
        assert fn2 in files, "second config file was not parsed"
        assert "/foo/bar/baz/bif.conf" not in files, "missing config file was successfully parsed"
        assert len(set(files).difference((fn1, fn2))) == 0, "unknown config file was successfully parsed"

    def test_check_required_options(self):
        fn = self._create_config_file("""
[foo]
setting = 1
[bar]
setting = 2
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
        missing = check_required_options([('foo', 'setting'), ('bar', 'value'), ('baz', 'setting')])
        assert len(missing) == 2, "incorrect number of missing options: %s" % (missing, )
        assert len(set(missing).difference((('bar', 'value'), ('baz', 'setting')))) == 0, \
            "unexpected missing options: %s" % (missing,)

    def test_get_config_option(self):
        fn = self._create_config_file("""
[foo]
setting = 1
[bar]
setting = 2
[baz]
setting = bif bing
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
        foo = get_config_option('foo', 'setting')
        assert int(foo) == 1
        bar = get_config_option('bar', 'setting')
        assert int(bar) == 2
        baz = get_config_option('baz', 'setting')
        assert baz == "bif bing"

    def test_get_config_option_with_default(self):
        fn = self._create_config_file("""
[foo]
setting = 1
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
        foo = get_config_option('foo', 'setting', 100)
        assert int(foo) == 1
        bar = get_config_option('bar', 'setting', 200)
        assert int(bar) == 200
        foo_key = get_config_option('foo', 'key', 300)
        assert int(foo_key) == 300

    def test_get_config_option_missing_section(self):
        fn = self._create_config_file("""
[foo]
setting = 1
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
        try:
            bar = get_config_option('bar', 'setting')
            assert False, "section 'bar' does not exist but get_config_option returned '%s'" % (bar,)
        except NoSectionError, e:
            pass

    def test_get_config_option_missing_option(self):
        fn = self._create_config_file("""
[foo]
setting = 1
""")
        Cobalt.CONFIG_FILES = [fn]
        files = init_cobalt_config()
        assert fn in files, "config file was not parsed"
        assert len(set(files).difference((fn,))) == 0, "unknown config file was successfully parsed"
        try:
            foo = get_config_option('foo', 'key')
            assert False, "option 'key' in section 'foo' does not exist but get_config_option returned '%s'" % (foo,)
        except NoOptionError, e:
            pass

    def test_get_config_option_multiple_files(self):
        fn1 = self._create_config_file("""
[foo]
setting = 1
""")
        fn2 = self._create_config_file("""
[bar]
setting = 2
""")
        Cobalt.CONFIG_FILES = [fn1, fn2]
        files = init_cobalt_config()
        assert fn1 in files, "first config file was not parsed"
        assert fn2 in files, "second config file was not parsed"
        assert len(set(files).difference((fn1, fn2))) == 0, "unknown config file was successfully parsed"
        foo = get_config_option('foo', 'setting')
        assert int(foo) == 1
        bar = get_config_option('bar', 'setting')
        assert int(bar) == 2

    def _create_config_file(self, text):
        fo = NamedTemporaryFile()
        self.file_objects.append(fo)
        fo.write(text)
        fo.flush()
        return fo.name
