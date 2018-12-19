#/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import logging
from mock import patch, call
import Cobalt
import Cobalt.client_utils
from Cobalt.Proxy import ComponentProxy

from nose.tools import raises

class TestCqadm(object):
    '''Internal tests for cqadm functionality'''

    test_nodes = dict.fromkeys(['1', '2', '3', '5', '6', '7'], None)

    def setup(self):
        Cobalt.client_utils.setup_logging(logging.DEBUG)

    @patch.object(Cobalt.client_utils, 'component_call', side_effect=['alps_system', test_nodes, None])
    def test_force_run_alps(self, proxy):
        '''alps force run calling right versions of proxy calls.'''
        location = '1-3,5-7'
        raw_location = [1,2,3,5,6,7]
        Cobalt.client_utils.run_jobs([1], location, 'frodo')
        calls = [call('system', True, 'get_implementation', ()),
                call('system', True, 'get_nodes', (True, raw_location, ['node_id'], False)),
                call('queue-manager', True, 'run_jobs', ([1], [location], 'frodo')),
                ]
        proxy.assert_has_calls(calls)

    @raises(SystemExit)
    @patch.object(Cobalt.client_utils, 'component_call', side_effect=['alps_system', test_nodes, None])
    def test_force_run_alps_bad_nodes(self, proxy):
        '''alps force run fails for nonexistent nodes.'''
        location = '1-7'
        raw_location = [1,2,3,4,5,6,7]
        Cobalt.client_utils.run_jobs([1], location, 'frodo')
        calls = [call('system', True, 'get_implementation', ()),
                call('system', True, 'get_nodes', (True, raw_location, ['node_id'], False)),
                ]
        proxy.assert_has_calls(calls)


    @patch.object(Cobalt.client_utils, 'component_call', side_effect=['alps_system', test_nodes, None])
    def test_force_run_alps_handle_colons(self, proxy):
        '''alps force run handles ':' '''
        location = '1:2-3:5-7'
        raw_location = [1,2,3,5,6,7]
        Cobalt.client_utils.run_jobs([1], location, 'frodo')
        calls = [call('system', True, 'get_implementation', ()),
                call('system', True, 'get_nodes', (True, raw_location, ['node_id'], False)),
                ]
        proxy.assert_has_calls(calls)
