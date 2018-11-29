# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
'''Tests for base ProcessGroup class and actions'''


from nose.tools import raises
from mock import Mock, MagicMock, patch

import Cobalt.Exceptions
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from Cobalt.Proxy import ComponentProxy

mock_proxy = MagicMock()

class TestProcessGroup(object):
    '''Group together process group tests, and apply common setup'''

    def setup(self):
        '''common setup for process group tests'''
        self.base_spec = {'args':['arg1', 'arg2'], 'user':'frodo',
                'jobid': 1, 'executable': 'job.exe', 'size': 2,
                'cwd': '/home/frodo', 'location': 'loc1'
                }

    def teardown(self):
        '''common teardown for process group tests'''
        del self.base_spec

    def test_process_group_init(self):
        '''ProcessGroup.__init__: basic initialization'''
        pgroup = ProcessGroup(self.base_spec)
        assert pgroup is not None, "process group creation failed"

    @raises(Cobalt.Exceptions.DataCreationError)
    def test_process_group_init_missing_fields(self):
        '''ProcessGroup.__init__: exception on bad spec'''
        pgroup = ProcessGroup({})
        assert False, "Should raise exception"

    @patch.object(Cobalt.Proxy.DeferredProxyMethod, '__call__', return_value=1)
    def test_process_group_start_base(self, proxy):
        '''basic process group startup'''
        pgroup = ProcessGroup(self.base_spec)
        data = pgroup.prefork()
        pgroup.start()
        proxy.assert_called_with([pgroup.executable] + pgroup.args, pgroup.tag,
                "Job %s/%s/%s" %(pgroup.jobid, pgroup.user, pgroup.id), pgroup.env,
                data, pgroup.runid)
