'''Process Manager for cluster/cray systems tests'''
import time
import logging
import sys
from nose.tools import raises
from mock import Mock, MagicMock, patch

import Cobalt.Proxy
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager
from testsuite.TestCobalt.Utilities.assert_functions import assert_match, assert_not_match

def is_match(a, b):
    return a is b

default_child_data = [{'id': 1}]

def fake_forker(*args, **kwargs):
    print args
    print kwargs
    raise RuntimeError('boom')
    #return 1

class InspectMock(MagicMock):
    '''allow us to inspect what is going on within a proxy call'''
    def __getattr__(self, attr):
        if attr == 'get_children':
            return MagicMock(return_value=[{'id': 1}])
        elif attr == 'fork':
            return MagicMock(return_value=1)
        return super(InspectMock, self).__getattr__(attr)

_loc_list = [{'name': 'system', 'location': 'https://localhost:52140'},
             {'name': 'system_script_forker', 'location': 'https://localhost:49242'},
             {'name': 'alps_script_forker_localhost_0', 'location': 'https://localhost:39303'},
             {'name': 'alps_script_forker_localhost_1', 'location': 'https://localhost:39304'},
             {'name': 'scheduler', 'location': 'https://localhost:41740'},
             {'name': 'queue-manager', 'location': 'https://localhost:50308'}
            ]

class ServicesMock(MagicMock):
    '''Fake expected services with multiple forkers'''

    def __init__(self, *args, **kwargs):
        super(ServicesMock, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'get_services':
            return MagicMock(return_value=_loc_list)
        return super(ServicesMock, self).__getattr__(attr)

class TestProcessManager(object):
    '''tests for the base project manager'''

    def setup(self):
        '''common setup for process group tests'''
        self.base_spec = {'args':['arg1', 'arg2'], 'user':'frodo',
                'jobid': 1, 'executable': 'job.exe', 'size': 2,
                'cwd': '/home/frodo', 'location': 'loc1'
                }
        self.process_manager = ProcessGroupManager()
        self.process_manager.forkers = ['forker1']
        self.process_manager.forker_taskcounts = {'forker1': 0}
        self.process_manager.forker_reachable = {'forker1': True}

    def teardown(self):
        '''common teardown for process group tests'''
        del self.base_spec
        del self.process_manager

    def test_init_groups_single(self):
        '''ProcessGroupManager.init_groups: create a process group and add to process manager'''
        specs = [self.base_spec]
        self.process_manager.init_groups(specs)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert self.process_manager.process_groups[1].forker == 'forker1', "forker not set"

    def test_init_groups_multiple(self):
        '''ProcessGroupManager.init_groups: select a forker for pgroup'''
        specs = [self.base_spec]
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 0, 'forker2': 0}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': True}
        self.process_manager.init_groups(specs)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[1].forker, 'forker1', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 1, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 0, "wrong forker taskcount modified")

    def test_init_groups_choose_lowest(self):
        '''ProcessGroupManager.init_groups: choose lightest forker load'''
        specs = [self.base_spec]
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 2, 'forker2': 0}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': True}
        self.process_manager.init_groups(specs)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[1].forker, 'forker2', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 1, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 2, "wrong forker taskcount modified")


    def test_init_groups_round_robin(self):
        '''ProcessGroupManager.init_groups: spread across multiple forkers'''
        specs1 = [dict(self.base_spec)]
        specs2 = [dict(self.base_spec)]
        specs2[0]['jobid'] = 2
        specs2[0]['location'] = 'loc2'
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 0, 'forker2': 0}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': True}
        self.process_manager.init_groups(specs1)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[1].forker, 'forker1', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 1, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 0, "wrong forker taskcount modified")
        self.process_manager.init_groups(specs2)
        assert self.process_manager.process_groups.get(2, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[2].forker, 'forker2', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 1, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 1, "wrong forker taskcount modified")

    def test_init_groups_select_reachable(self):
        '''ProcessGroupManager.init_groups: select only reachable forker'''
        specs1 = [self.base_spec]
        specs2 = [dict(self.base_spec)]
        specs2[0]['jobid'] = 2
        specs2[0]['location'] = 'loc2'
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 2, 'forker2': 0}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': False}
        self.process_manager.init_groups(specs1)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[1].forker, 'forker1', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 0, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 3, "wrong forker taskcount modified")
        self.process_manager.init_groups(specs2)
        assert self.process_manager.process_groups.get(2, None) is not None, "process group not created"
        assert_match(self.process_manager.process_groups[2].forker, 'forker1', "Incorrect forker set")
        assert_match(self.process_manager.forker_taskcounts['forker2'], 0, "wrong taskcount set")
        assert_match(self.process_manager.forker_taskcounts['forker1'], 4, "wrong forker taskcount modified")


    @patch.object(Cobalt.Proxy.DeferredProxyMethod, '__call__', return_value=1)
    def test_start_groups_single(self, *args, **kwargs):
        '''ProcessGroupManager.start_groups: start up a single process group'''
        self.base_spec['startup_timeout'] = 120
        self.process_manager.init_groups([self.base_spec])
        started = self.process_manager.start_groups([1])
        assert len(started) == 1, "started %s groups, should have started 1" % len(started)
        assert sorted(started) == [1], "wrong groups started."
        assert self.process_manager.process_groups[1].startup_timeout == 0, (
                "startup_timeout not reset")

    @patch.object(Cobalt.Proxy.DeferredProxyMethod, '__call__', return_value=1,
            side_effect=[Cobalt.Exceptions.ComponentLookupError('failed lookup'), 1])
    def test_start_groups_one_bad_forker(self, *args, **kwargs):
        '''ProcessGroupManager.start_groups: switch forker for failure'''
        self.base_spec['startup_timeout'] = 120
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 0, 'forker2': 1}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': True}
        self.process_manager.init_groups([self.base_spec])
        started = self.process_manager.start_groups([1])
        started = self.process_manager.start_groups([1])
        assert len(started) == 1, "started %s groups, should have started 1" % len(started)
        assert sorted(started) == [1], "wrong groups started."
        assert self.process_manager.process_groups[1].startup_timeout == 0, (
                "startup_timeout not reset")
        assert_match(self.process_manager.process_groups[1].forker, 'forker2', "Wrong forker selected")

    @patch.object(Cobalt.Proxy.DeferredProxyMethod, '__call__', return_value=1,
            side_effect=Cobalt.Exceptions.ComponentLookupError('failed lookup'))
    @raises(Cobalt.Exceptions.ProcessGroupStartupError)
    def test_start_groups_no_forkers(self, *args, **kwargs):
        '''ProcessGroupManager.start_groups: RuntimeError if no forkers reachable'''
        self.base_spec['startup_timeout'] = 120
        self.process_manager.forkers = ['forker1', 'forker2']
        self.process_manager.forker_taskcounts = {'forker1': 0, 'forker2': 1}
        self.process_manager.forker_reachable = {'forker1': True, 'forker2': True}
        self.process_manager.init_groups([self.base_spec])
        started = self.process_manager.start_groups([1])
        started = self.process_manager.start_groups([1])


    @patch('Cobalt.Proxy.DeferredProxy', side_effect=InspectMock)
    def test_update_groups_timeout(self, *args, **kwargs):
        '''ProcessGroupManager.update_groups: startup timeout respected.'''
        now = int(time.time())
        pgroups = self.process_manager.process_groups
        self.process_manager.init_groups([self.base_spec])
        pgroups[1].startup_timeout = 120 + now
        self.process_manager.update_groups()
        pgroups = self.process_manager.process_groups
        assert len(pgroups) == 1, "%s groups, should have 1" % len(pgroups)
        assert sorted(pgroups.keys()) == [1], "wrong groups."
        assert pgroups[1].startup_timeout == now + 120, (
                "bad startup timeout: %s" % pgroups[1].startup_timeout)

    @patch('Cobalt.Proxy.DeferredProxy', side_effect=InspectMock)
    def test_update_groups_over_timeout(self, *args, **kwargs):
        '''ProcessGroupManager.update_groups: startup timeout exceeded.'''
        now = int(time.time())
        pgroups = self.process_manager.process_groups
        self.process_manager.init_groups([self.base_spec])
        pgroups[1].startup_timeout = now - 120
        self.process_manager.update_groups()
        pgroups = self.process_manager.process_groups
        assert len(pgroups) == 0, "%s groups, should have 0" % len(pgroups)
        assert sorted(pgroups.keys()) == [], "groups should be empty"

class TestPMUpdateLaunchers(object):


    def setup(self):
        '''common setup for process group tests'''
        global _loc_list
        self.init_loc_list = _loc_list

    def teardown(self):
        '''common teardown for process group tests'''
        global _loc_list
        _loc_list = self.init_loc_list

    @patch('Cobalt.Proxy.DeferredProxy', side_effect=ServicesMock)
    def test_update_launchers_register(self, *args, **kwargs):
        '''ProcessGroupManager.update_launchers: register new launcher'''
        pgm = ProcessGroupManager() #implicit update_launchers call on init.
        assert_match(pgm.forkers, ['alps_script_forker_localhost_0', 'alps_script_forker_localhost_1'],
                'Forker list mismatch')
        assert_match(pgm.forker_locations,
                {'alps_script_forker_localhost_1': 'localhost',
                    'alps_script_forker_localhost_0': 'localhost'},
                'Incorrect forker locations')
        assert_match(pgm.forker_reachable,
                {'alps_script_forker_localhost_1': True, 'alps_script_forker_localhost_0': True},
                'Incorrect forker reachable')

    @patch('Cobalt.Proxy.DeferredProxy', side_effect=ServicesMock)
    def test_update_launchers_unregister(self, *args, **kwargs):
        '''ProcessGroupManager.update_launchers: detect down forker'''
        pgm = ProcessGroupManager() #implicit update_launchers call on init.
        global _loc_list
        _loc_list = [{'name': 'system', 'location': 'https://localhost:52140'},
                {'name': 'system_script_forker', 'location': 'https://localhost:49242'},
                {'name': 'alps_script_forker_localhost_1', 'location': 'https://localhost:39304'},
                {'name': 'scheduler', 'location': 'https://localhost:41740'},
                {'name': 'queue-manager', 'location': 'https://localhost:50308'}
               ]
        pgm.update_launchers()
        assert_match(pgm.forkers, ['alps_script_forker_localhost_1'],
                'Forker list mismatch')
        assert_match(pgm.forker_locations,
                {'alps_script_forker_localhost_1': 'localhost'},
                'Incorrect forker locations')
        assert_match(pgm.forker_reachable,
                {'alps_script_forker_localhost_1': True, 'alps_script_forker_localhost_0': False},
                'Incorrect forker reachable')

    @patch('Cobalt.Proxy.DeferredProxy', side_effect=ServicesMock)
    def test_update_launchers_reregister(self, *args, **kwargs):
        '''ProcessGroupManager.update_launchers: detect forker reregister'''
        pgm = ProcessGroupManager() #implicit update_launchers call on init.
        global _loc_list
        _loc_list = [{'name': 'system', 'location': 'https://localhost:52140'},
                {'name': 'system_script_forker', 'location': 'https://localhost:49242'},
                {'name': 'alps_script_forker_localhost_1', 'location': 'https://localhost:39304'},
                {'name': 'scheduler', 'location': 'https://localhost:41740'},
                {'name': 'queue-manager', 'location': 'https://localhost:50308'}
               ]
        pgm.update_launchers()
        _loc_list = self.init_loc_list
        pgm.update_launchers()
        assert_match(pgm.forkers, ['alps_script_forker_localhost_0', 'alps_script_forker_localhost_1'],
                'Forker list mismatch')
        assert_match(pgm.forker_locations,
                {'alps_script_forker_localhost_1': 'localhost',
                    'alps_script_forker_localhost_0': 'localhost'},
                'Incorrect forker locations')
        assert_match(pgm.forker_reachable,
                {'alps_script_forker_localhost_1': True, 'alps_script_forker_localhost_0': True},
                'Incorrect forker reachable')
