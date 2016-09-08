'''Process Manager for cluster/cray systems tests'''
import time
import logging
import sys
from mock import Mock, MagicMock, patch

import Cobalt.Proxy
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager

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
        self.process_manager.forker_taskcounts = {'forker1':0}
    def teardown(self):
        '''common teardown for process group tests'''
        del self.base_spec
        del self.process_manager

    def test_process_manager_init_groups_single(self):
        '''ProcessGroupManager.init_groups: create a process group and add to process manager'''
        specs = [self.base_spec]
        self.process_manager.init_groups(specs)
        assert self.process_manager.process_groups.get(1, None) is not None, "process group not created"
        assert self.process_manager.process_groups[1].forker == 'forker1', "forker not set"

    @patch.object(Cobalt.Proxy.DeferredProxyMethod, '__call__', return_value=1)
    def test_process_manager_start_groups_single(self, *args, **kwargs):
        '''ProcessGroupManager.start_groups: start up a single process group'''
        self.base_spec['startup_timeout'] = 120
        self.process_manager.init_groups([self.base_spec])
        started = self.process_manager.start_groups([1])
        assert len(started) == 1, "started %s groups, should have started 1" % len(started)
        assert sorted(started) == [1], "wrong groups started."
        assert self.process_manager.process_groups[1].startup_timeout == 0, (
                "startup_timeout not reset")

    @patch('Cobalt.Proxy.DeferredProxy', side_effect=InspectMock)
    def test_process_manager_update_groups_timeout(self, *args, **kwargs):
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
    def test_process_manager_update_groups_timeout_exceeded(self, *args, **kwargs):
        '''ProcessGroupManager.update_groups: startup timeout exceeded.'''
        now = int(time.time())
        pgroups = self.process_manager.process_groups
        self.process_manager.init_groups([self.base_spec])
        pgroups[1].startup_timeout = now - 120
        self.process_manager.update_groups()
        pgroups = self.process_manager.process_groups
        assert len(pgroups) == 0, "%s groups, should have 0" % len(pgroups)
        assert sorted(pgroups.keys()) == [], "groups should be empty"
