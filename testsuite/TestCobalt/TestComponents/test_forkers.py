'''Tests for the forker components
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

'''

CQM_CONFIG_FILE_ENTRY = """
[forker]
foo = bar

[logging]
to_syslog = True
syslog_level = DEBUG
to_console = True
console_level = DEBUG

"""

# override the cobalt config file before the cqm component is loaded
import Cobalt
import TestCobalt
import ConfigParser
import time
import os
import subprocess
import StringIO
import sys

config_file = Cobalt.CONFIG_FILES[0]
config_fp = open(config_file, "w")
config_fp.write(CQM_CONFIG_FILE_ENTRY)
config_fp.close()
config_fp.close()
config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

from mock import Mock, MagicMock, patch
from testsuite.TestCobalt.Utilities.assert_functions import assert_match, assert_not_match
from nose.tools import raises

#Fake the import for cray_messaging.  This has to be mocked if we're testing any ALPS functions.
sys.modules['cray_messaging'] = MagicMock()

import Cobalt.Components.base_forker
from Cobalt.Components.user_script_forker import UserScriptForker
from Cobalt.Components.user_script_forker import UserScriptChild
from Cobalt.Components.alps_script_forker import ALPSScriptChild
from Cobalt.Components.system_script_forker import SystemScriptChild

Cobalt.Components.base_forker.config = config

class TestChild(Cobalt.Components.base_forker.BaseChild):

    def preexec_first(self):
        pass

    def preexec_last(self):
        pass

class TestBaseForker(object):

    def setup_base_forker(self):
        self.child_id = None
        self.bf = Cobalt.Components.base_forker.BaseForker()
        self.bf.child_cls = TestChild

    def test_wait_SIGTERM(self):
        # make sure SIGTERM gets sent when marked for death
        self.setup_base_forker()
        self.child_id = self.bf.fork(['/bin/sleep','60'])
        time.sleep(1)
        assert self.child_id != None, "No child id returned"
        self.bf.marked_for_death[self.child_id] = self.bf.children[self.child_id]
        self.bf._wait() #SIGTERM fires now
        time.sleep(1)
        self.bf._wait() #SIGKILL and we're done
        assert self.bf.children[self.child_id].signum == 15, 'Job not SIGTERMed'

    def test_wait_SIGKILL(self):
        # if SIGTERM fails, make sure a SIGKILL is delivered.
        self.setup_base_forker()
        self.bf.DEATH_TIMEOUT = 2
        self.child_id = self.bf.fork(['testsuite/TestCobalt/TestComponents/ignore_sigterm.py','60'])
        time.sleep(1)
        assert self.child_id != None, "No child id returned"
        self.bf.marked_for_death[self.child_id] = self.bf.children[self.child_id]
        self.bf._wait() #SIGTERM (IGNORED) and start timer
        time.sleep(3)
        self.bf._wait() #SIGKILL (give a moment to propigate)
        time.sleep(1) #If we're not dead by now we're in trouble something has gone wrong
        self.bf._wait() #SIGKILL and we're done
        assert self.bf.children[self.child_id].signum == 9, 'Job not SIGKILLed'


class TestUserScriptForker(object):

    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_pgroup(self, mock_kill, mock_killpg):
        #send a killpg to a script process group
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512})
        usf.children[1].pid = 1234
        usf.signal(1, "SIGTERM")
        mock_killpg.assert_called_with(1234, 15)
        mock_kill.assert_not_called()


    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_nokillpg(self, mock_kill, mock_killpg):
        #use kill if appropriate attr set.
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512, 'attrs':{'nopgkill': True}})
        usf.children[1].pid = 1234
        usf.signal(1, "SIGTERM")
        mock_kill.assert_called_with(1234, 15)
        mock_killpg.assert_not_called()


    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_no_pid_no_kill(self, mock_kill, mock_killpg):
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512, 'attrs':{'nopgkill': True}})
        usf.signal(1, "SIGTERM")
        mock_kill.assert_not_called()
        mock_killpg.assert_not_called()

class TestBaseChild(object):
    '''Test Cobalt.Components.base_forker.BaseChild operations'''

    #start is getting tested as a part of the overall forker test here.

    def setup(self):
        self.old_config = Cobalt.Util.config
        self.args = ['/usr/bin/foo', '--flag0', 'arg0', 'arg1']
        self.child_spec = {'args': self.args,
                      'tag': 'testsuite',
                      'cwd': '/home/joshua',
                      'umask': '0077',
                      'runid': 42,
                     }

    def teardown(self):
        Cobalt.Components.base_forker.BaseChild.id_gen = Cobalt.Data.IncrID()
        Cobalt.Util.config = self.old_config

    def test_child_construction(self):
        '''BaseChild: construction'''
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        assert_match(child.args, self.args, 'Args do not match')
        assert_match(child.tag, 'testsuite', 'Tag Mismatch')
        assert_match(child.cwd, '/home/joshua', 'Bad cwd')
        assert_match(child.id, 1, 'Bad id')
        assert_match(child.umask, '0077', 'Bad umask')
        assert_match(child.runid, 42, 'Bad runid')

    def test_child_construction_set_id(self):
        '''BaseChild: construction w/id'''
        child = Cobalt.Components.base_forker.BaseChild(id=300, **self.child_spec)
        assert_match(child.args, self.args, 'Args do not match')
        assert_match(child.tag, 'testsuite', 'Tag Mismatch')
        assert_match(child.cwd, '/home/joshua', 'Bad cwd')
        assert_match(child.id, 300, 'Bad id')
        assert_match(child.umask, '0077', 'Bad umask')
        assert_match(child.runid, 42, 'Bad runid')


    @patch('Cobalt.Components.base_forker.os.setsid')
    @patch('Cobalt.Components.base_forker.subprocess.Popen')
    def test_child_set_cgroup(self, mock_subprocess_popen, mock_os_setsid):
        '''BaseChild: set cgroup'''
        # Not calling the start() method that would invoke this due to fork/exec being really messy
        # in this environment.  setsid should be separate
        communicate = MagicMock(return_value=('',''))
        mock_subprocess_popen.return_value.communicate = communicate
        mock_subprocess_popen.return_value.returncode = 0
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        child.use_cgroups = True
        child.cgclassify_path = '/usr/bin/foo'
        child.cgclassify_args = ['test', 'arguments']
        expected_arguments = ['/usr/bin/foo', 'test', 'arguments', str(os.getpid())]
        child.preexec_first()
        mock_subprocess_popen.assert_called_once_with(expected_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        communicate.assert_called_once_with(None)

    @patch('Cobalt.Components.base_forker.os.setsid')
    @patch('Cobalt.Components.base_forker.subprocess.Popen')
    def test_child_cgroup_raise_exec_error(self, mock_subprocess_popen, mock_os_setsid):
        '''BaseChild: handle cgclassify exec failure'''
        mock_subprocess_popen.side_effect = IOError('Fake file not found')
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        child.use_cgroups = True
        child.cgclassify_path = '/usr/bin/foo'
        child.cgclassify_args = ['test', 'arguments']
        expected_arguments = ['/usr/bin/foo', 'test', 'arguments', str(os.getpid())]
        child.preexec_first()
        mock_subprocess_popen.assert_called_once_with(expected_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        mock_subprocess_popen.return_value.communicate.assert_not_called()

    @raises(IOError)
    @patch('Cobalt.Components.base_forker.os.setsid')
    @patch('Cobalt.Components.base_forker.subprocess.Popen')
    def test_child_cgroup_raise_exec_error_fatal_flag(self, mock_subprocess_popen, mock_os_setsid):
        '''BaseChild: handle cgclassify exec failure with fatal flag'''
        mock_subprocess_popen.side_effect = IOError('Fake file not found')
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        child.use_cgroups = True
        child.cgroup_failure_fatal = True
        child.cgclassify_path = '/usr/bin/foo'
        child.cgclassify_args = ['test', 'arguments']
        expected_arguments = ['/usr/bin/foo', 'test', 'arguments', str(os.getpid())]
        child.preexec_first()
        mock_subprocess_popen.assert_called_once_with(expected_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        mock_subprocess_popen.return_value.communicate.assert_not_called()

    @patch('Cobalt.Components.base_forker.os.setsid')
    @patch('Cobalt.Components.base_forker.subprocess.Popen')
    def test_child_cgroup_return_nonzero(self, mock_subprocess_popen, mock_os_setsid):
        '''BaseChild: handle nonzero returncode from cgclassify'''
        communicate = MagicMock(return_value=('',''))
        mock_subprocess_popen.return_value.communicate = communicate
        mock_subprocess_popen.return_value.returncode = 1
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        child.use_cgroups = True
        child.cgclassify_path = '/usr/bin/foo'
        child.cgclassify_args = ['test', 'arguments']
        expected_arguments = ['/usr/bin/foo', 'test', 'arguments', str(os.getpid())]
        child.preexec_first()
        mock_subprocess_popen.assert_called_once_with(expected_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        communicate.assert_called_once_with(None)

    @raises(RuntimeError)
    @patch('Cobalt.Components.base_forker.os.setsid')
    @patch('Cobalt.Components.base_forker.subprocess.Popen')
    def test_child_cgroup_return_nonzero_fatal_flag(self, mock_subprocess_popen, mock_os_setsid):
        '''BaseChild: handle nonzero returncode from cgclassify with fatal flag'''
        communicate = MagicMock(return_value=('',''))
        mock_subprocess_popen.return_value.communicate = communicate
        mock_subprocess_popen.return_value.returncode = 1
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        child.use_cgroups = True
        child.cgroup_failure_fatal = True
        child.cgclassify_path = '/usr/bin/foo'
        child.cgclassify_args = ['test', 'arguments']
        expected_arguments = ['/usr/bin/foo', 'test', 'arguments', str(os.getpid())]
        child.preexec_first()
        mock_subprocess_popen.assert_called_once_with(expected_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        communicate.assert_called_once_with(None)


    def test_set_cgclassify_attributes(self):
        '''BaseForker: set cgclassify attributes'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        old_config = Cobalt.Util.config
        # Need to override the one in Util so actually correctly override things.
        Cobalt.Util.config = local_config
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        assert_match(child.use_cgroups, True, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, False, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/usr/bin/cgclassify', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, None, 'bad cgclassify args')
        Cobalt.Util.config = old_config

    def test_set_cgclassify_path(self):
        '''BaseForker: set cgclassify path'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'cgclassify_path = /why/did/you/move/this'
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        old_config = Cobalt.Util.config
        # Need to override the one in Util so actually correctly override things.
        Cobalt.Util.config = local_config
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        assert_match(child.use_cgroups, False, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, False, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/why/did/you/move/this', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, None, 'bad cgclassify args')
        Cobalt.Util.config = old_config

    def test_set_cgclassify_args(self):
        '''BaseForker: set cgclassify args'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgclassify_args = -g foo bar'
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        old_config = Cobalt.Util.config
        # Need to override the one in Util so actually correctly override things.
        Cobalt.Util.config = local_config
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        assert_match(child.use_cgroups, True, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, False, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/usr/bin/cgclassify', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, ['-g', 'foo', 'bar'], 'bad cgclassify args')
        Cobalt.Util.config = old_config

    def test_set_cgclassify_failure_fatal(self):
        '''BaseForker: set cgclassify_failure_fatal'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'cgroup_failure_fatal = True'
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        old_config = Cobalt.Util.config
        # Need to override the one in Util so actually correctly override things.
        Cobalt.Util.config = local_config
        child = Cobalt.Components.base_forker.BaseChild(**self.child_spec)
        assert_match(child.use_cgroups, False, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, True, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/usr/bin/cgclassify', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, None, 'bad cgclassify args')

class TestALPSScriptChild(object):

    def setup(self):
        self.old_config = Cobalt.Util.config
        self.args = ['/usr/bin/foo', '--flag0', 'arg0', 'arg1']
        self.child_spec = {'data':{'args': self.args,
                      'tag': 'testsuite',
                      'cwd': '/home/joshua',
                      'umask': '0077',
                      'runid': 42,
                      'jobid': 1,
                      'executable':'/usr/bin/foo',
                      'size': 1,
                      'user': 'joshua',
                      'location': '0',
                     }}

    def teardown(self):
        Cobalt.Components.base_forker.BaseChild.id_gen = Cobalt.Data.IncrID()
        Cobalt.Util.config = self.old_config

    def test_set_cgclassify_args_base_only(self):
        '''ALPSScriptChild: set cgclassify attributes'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /why/did/you/move/this',
                              'cgclassify_args = -g foo bar',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        Cobalt.Util.config = local_config
        child = Cobalt.Components.alps_script_forker.ALPSScriptChild(1, **self.child_spec)
        assert_match(child.use_cgroups, True, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, True, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/why/did/you/move/this', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, ['-g', 'foo', 'bar'], 'bad cgclassify args')

    def test_set_cgclassify_args_override_all_forkers(self):
        '''ALPSScriptChild: set cgclassify attributes for alps_script_forker'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /why/did/you/move/this',
                              'cgclassify_args = -g foo bar',
                              '[forker.alps]',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /yet/another/one',
                              'cgclassify_args = -g baz',
                              '[forker.system]',
                              'use_cgroups = False',
                              'cgroup_failure_fatal = False',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        Cobalt.Util.config = local_config
        child = Cobalt.Components.alps_script_forker.ALPSScriptChild(1, **self.child_spec)
        assert_match(child.use_cgroups, True, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, True, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/yet/another/one', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, ['-g', 'baz'], 'bad cgclassify args')

    def test_set_cgclassify_args_override_single_forker(self):
        '''ALPSScriptChild: set cgclassify attributes for alps_script_forker_localhost_1'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /why/did/you/move/this',
                              'cgclassify_args = -g foo bar',
                              '[forker.alps]',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /yet/another/one',
                              'cgclassify_args = -g baz',
                              '[forker.system]',
                              'use_cgroups = False',
                              'cgroup_failure_fatal = False',
                              '[forker.alps_script_forker_localhost_1]',
                              'use_cgroups = False',
                              'cgroup_failure_fatal = False',
                              'cgclassify_path = /again',
                              'cgclassify_args = -g qux',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        Cobalt.Util.config = local_config
        self.child_spec['forker_name'] = 'alps_script_forker_localhost_1'
        child = Cobalt.Components.alps_script_forker.ALPSScriptChild(1, **self.child_spec)
        assert_match(child.use_cgroups, False, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, False, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/again', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, ['-g', 'qux'], 'bad cgclassify args')


class TestSystemScriptChild(object):
    def setup(self):
        self.old_config = Cobalt.Util.config
        self.args = ['/usr/bin/foo', '--flag0', 'arg0', 'arg1']
        self.child_spec = {'data':{'args': self.args,
                      'tag': 'testsuite',
                      'cwd': '/home/joshua',
                      'umask': '0077',
                      'runid': 42,
                      'jobid': 1,
                      'executable':'/usr/bin/foo',
                      'size': 1,
                      'user': 'joshua',
                      'location': '0',
                     }}

    def teardown(self):
        Cobalt.Components.base_forker.BaseChild.id_gen = Cobalt.Data.IncrID()
        Cobalt.Util.config = self.old_config

    def test_set_cgclassify_args_base_only(self):
        '''SystemScriptChild: set cgclassify attributes'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /why/did/you/move/this',
                              'cgclassify_args = -g foo bar',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        # Need to override the one in Util so actually correctly override things.
        Cobalt.Util.config = local_config
        child = Cobalt.Components.system_script_forker.SystemScriptChild(1, **self.child_spec)
        assert_match(child.use_cgroups, True, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, True, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/why/did/you/move/this', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, ['-g', 'foo', 'bar'], 'bad cgclassify args')

    def test_set_cgclassify_args_override_system_script_forker(self):
        '''SystemScriptChild: set cgclassify attributes for system_script_forker'''
        test_config_params = ['[forker]',
                              'foo = bar',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              '[forker.alps]',
                              'use_cgroups = True',
                              'cgroup_failure_fatal = True',
                              'cgclassify_path = /yet/another/one',
                              'cgclassify_args = -g baz',
                              '[forker.system]',
                              'use_cgroups = False',
                              'cgroup_failure_fatal = False',
                              '[forker.alps_script_forker_localhost_1]',
                              'use_cgroups = False',
                              'cgroup_failure_fatal = False',
                              'cgclassify_path = /yet/another/one',
                              'cgclassify_args = -g baz',
                              ]

        fake_config_file = StringIO.StringIO("\n".join(test_config_params))
        local_config = ConfigParser.ConfigParser()
        local_config.readfp(fake_config_file)
        Cobalt.Util.config = local_config
        self.child_spec['forker_name'] = 'alps_script_forker_localhost_1'
        child = Cobalt.Components.system_script_forker.SystemScriptChild(1, **self.child_spec)
        assert_match(child.use_cgroups, False, 'cgroup use flag wrong')
        assert_match(child.cgroup_failure_fatal, False, 'cgroup_failure_fatal wrong')
        assert_match(child.cgclassify_path, '/usr/bin/cgclassify', 'wrong cgclassify path')
        assert_match(child.cgclassify_args, None, 'bad cgclassify args')
