# Test Cray-specific utilities/calls.
from nose.tools import raises
from testsuite.TestCobalt.Utilities.assert_functions import assert_match, assert_not_match
from Cobalt.Components.system.CrayNode import CrayNode
import Cobalt.Exceptions
import time
from Cobalt.Components.system.CraySystem import CraySystem
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager
import Cobalt.Components.system.AlpsBridge as AlpsBridge

from mock import MagicMock, Mock, patch


def is_match(a, b):
    return a is b

class TestCrayNode(object):

    def setup(self):
        self.spec = {'name':'test', 'state': 'UP', 'node_id': 1, 'role':'batch',
                'architecture': 'XT', 'SocketArray':['foo', 'bar'],
                }
        self.base_node = CrayNode(self.spec)

    def teardown(self):
        del self.spec
        del self.base_node

    def test_init(self):
        '''CrayNode.__init__: test initilaizer'''
        spec = {'name':'test', 'state': 'UP', 'node_id': 1, 'role':'batch',
                'architecture': 'XT', 'SocketArray':['foo', 'bar'],
                }
        node = CrayNode(spec)
        assert_match(node.status, 'idle', 'bad status')
        assert_match(node.node_id, 1, 'bad nodeid')
        assert_match(node.role, 'BATCH', 'bad role')
        assert_match(node.attributes['architecture'], 'XT',
                'bad architecture',  is_match)
        assert_match(node.segment_details, ['foo', 'bar'],
                'bad segment')
        assert_match(node.ALPS_status, 'UNKNOWN',
                'bad default ALPS status')
        assert 'alps-interactive' in node.RESOURCE_STATUSES,(
                'alps-interactive not in resource statuses')

    def test_init_alps_states(self):
        '''CrayNode.__init__: alps states correctly set'''
        cray_state_list = ['UP', 'DOWN', 'UNAVAILABLE', 'ROUTING', 'SUSPECT',
                           'ADMIN', 'UNKNOWN', 'UNAVAIL', 'SWDOWN', 'REBOOTQ',
                           'ADMINDOWN']
        correct_alps_states = {'UP': 'idle', 'DOWN':'down', 'UNAVAILABLE':'down',
                               'ROUTING':'down', 'SUSPECT':'down', 'ADMIN':'down',
                               'UNKNOWN':'down', 'UNAVAIL': 'down', 'SWDOWN': 'down',
                               'REBOOTQ':'down', 'ADMINDOWN':'down'}
        for state in cray_state_list:
            self.spec['state'] = state
            node = CrayNode(self.spec)
            assert node.status == correct_alps_states[state],(
                    "%s should map to %s" % (node.status,
                        correct_alps_states[state]))

    def test_non_cray_statuses(self):
        '''CrayNode.status: can set cobalt-tracking statuses.'''
        test_statuses = ['busy', 'cleanup-pending', 'allocated',
                'alps-interactive']
        for status in test_statuses:
            self.base_node.status = status
            assert_match(self.base_node.status, status, "failed validation")

class TestCraySystem(object):
    '''Test Cray system component functionality'''
    #SETUP AND TEARDOWN HELPERS
    @patch.object(AlpsBridge, 'init_bridge')
    @patch.object(CraySystem, '_init_nodes_and_reservations', return_value=None)
    @patch.object(CraySystem, '_run_update_state', return_value=None)
    def setup(self, *args, **kwargs):
        self.system = CraySystem()
        self.base_spec = {'name':'test', 'state': 'UP', 'node_id': '1', 'role':'batch',
                'architecture': 'XT', 'SocketArray':['foo', 'bar'],
                'queues':['default'],
                }
        for i in range(1,6):
            self.base_spec['name'] = "test%s" % i
            self.base_spec['node_id'] = str(i)
            node_dict=dict(self.base_spec)
            self.system.nodes[str(i)] = CrayNode(node_dict)
            self.system.node_name_to_id[node_dict['name']] = node_dict['node_id']
        for node in self.system.nodes.values():
            node.managed = True
        self.system._gen_node_to_queue()

        self.base_job = {'jobid':1, 'user':'crusher', 'attrs':{},
                'queue':'default', 'nodes': 1,
                }

    def teardown(self):
        del self.system
        del self.base_job

    # HELPER MOCK FUNCTIONS
    def fake_reserve(self, job, new_time, node_id_list):
        '''Mimic first-fit function of ALPS placement scheme'''
        # self gets overriden by the call within fjl to be the real system
        # component.
        ret_nodes = []
        if job['nodes'] <= len(node_id_list):
            ret_nodes = node_id_list[:int(job['nodes'])]
        return ret_nodes

    #TESTS
    def test_assemble_queue_data(self):
        '''CraySystem._assemble_queue_data: base functionality'''
        nodelist =  self.system._assemble_queue_data(self.base_job)
        assert_match(sorted(nodelist), ['1', '2', '3', '4', '5'], 'nodelist mismatch')

    def test_assemble_queue_data_bad_queue(self):
        '''CraySystem._assemble_queue_data: return nothing if queue for job doesn't exist'''
        self.base_job['queue'] = 'foo'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(nodelist, [], 'nonempty nodelist')

    def test_assemble_queue_data_multiple_queue(self):
        '''CraySystem._assemble_queue_data: return only proper queue nodes'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['4'].queues = ['bar']
        self.system._gen_node_to_queue()
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(sorted(nodelist), ['2', '3', '5'], 'Wrong nodelist')

    def test_assemble_queue_data_multiple_queue_overlap(self):
        '''CraySystem._assemble_queue_data: return only proper queue nodes in overlaping queues'''
        self.system.nodes['1'].queues = ['foo', 'default', 'bar']
        self.system.nodes['4'].queues = ['default','bar']
        self.system.nodes['5'].queues = ['baz']
        self.system._gen_node_to_queue()
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(sorted(nodelist), ['1', '2', '3', '4'], 'Wrong nodelist')
        self.base_job['queue'] = 'foo'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(nodelist, ['1'], 'Wrong nodelist')
        self.base_job['queue'] = 'bar'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(sorted(nodelist), ['1', '4'], 'Wrong nodelist')
        self.base_job['queue'] = 'baz'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(nodelist, ['5'], 'Wrong nodelist')

    def test_assemble_queue_data_idle(self):
        '''CraySystem._assemble_queue_data: return only idle nodes'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.system._gen_node_to_queue()
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert_match(sorted(nodelist), ['2','3','5'], 'Wrong nodelist')

    def test_assemble_queue_data_non_down(self):
        '''CraySystem._assemble_queue_data: return nodes that are not down'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False)
        assert sorted(nodelist) == ['1','2','3','5'], 'Wrong nodes in list %s' % nodelist
        self.system.nodes['1'].status = 'SUSPECT'
        self.system.nodes['2'].status = 'alps-interactive'
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False)
        assert sorted(nodelist) == ['3','5'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_attrs_location(self):
        '''CraySystem._assemble_queue_data: return only attr locaiton loc'''
        self.base_job['attrs'] = {'location':'3'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert nodelist == ['3'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_attrs_location_repeats(self):
        '''CraySystem._assemble_queue_data: eliminate repeat location entries'''
        self.base_job['attrs'] = {'location':'1,1,2,3'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['1', '2', '3'], 'Wrong node in list %s' % nodelist

    @raises(ValueError)
    def test_assemble_queue_data_attrs_bad_location(self):
        '''CraySystem._assemble_queue_data: raise error for location completely outside of
        queue'''
        self.base_job['attrs'] = {'location':'6'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert nodelist == ['3'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_attrs_location_multi(self):
        '''CraySystem._assemble_queue_data: return only attr locaiton complex loc string'''
        self.base_job['attrs'] = {'location':'1-3,5'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['1','2','3','5'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_forbidden_loc(self):
        '''CraySystem._assemble_queue_data: avoid reserved nodes'''
        self.base_job['forbidden'] = ['1-3','5']
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['4'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_forbidden_loc_attrs_loc(self):
        '''CraySystem._assemble_queue_data: avoid reserved nodes despite location being set'''
        self.base_job['forbidden'] = ['1-3']
        self.base_job['attrs'] = {'location':'1-4'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['4'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_forbidden_loc_attrs_loc_complete(self):
        '''CraySystem._assemble_queue_data: avoid reserved nodes block location if superset'''
        self.base_job['forbidden'] = ['1-3']
        self.base_job['attrs'] = {'location':'1-3'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == [], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_forbidden_loc_attrs_loc_permit(self):
        '''CraySystem._assemble_queue_data: forbidden doesn't block everything'''
        self.base_job['forbidden'] = ['1-3']
        self.base_job['attrs'] = {'location':'4-5'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['4','5'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_reserved_loc(self):
        '''CraySystem._assemble_queue_data: return reservation nodes'''
        self.base_job['required'] = ['2-4']
        self.base_job['queue'] = 'reservation'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['2','3','4'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_reserved_loc_idle_only(self):
        '''CraySystem._assemble_queue_data: return reservation nodes that are idle'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.base_job['required'] = ['1-5']
        self.base_job['queue'] = 'reservation'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['5'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_reserved_loc_non_down(self):
        '''CraySystem._assemble_queue_data: return reservation nodes that are not down'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.base_job['required'] = ['1-5']
        self.base_job['queue'] = 'reservation'
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False)
        assert sorted(nodelist) == ['1','2','3','5'], 'Wrong nodes in list %s' % nodelist
        self.system.nodes['1'].status = 'SUSPECT'
        self.system.nodes['2'].status = 'alps-interactive'
        self.base_job['required'] = ['1-5']
        self.base_job['queue'] = 'reservation'
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False)
        assert sorted(nodelist) == ['3','5'], 'Wrong nodes in list %s' % nodelist

    def test_assemble_queue_data_reserved_loc_location_set(self):
        '''CraySystem._assemble_queue_data: return reservation nodes for job with location set'''
        self.base_job['required'] = ['1-4']
        self.base_job['attrs'] = {'location':'1,2,4'}
        self.base_job['queue'] = 'reservation'
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert sorted(nodelist) == ['1','2','4'], 'Wrong nodes in list %s' % nodelist

    #need testcase with loc targeting down nodes.
    def test_assemble_queue_data_attrs_location_blocked_nodes(self):
        '''CraySystem._assemble_queue_data: return only idle locations'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.base_job['attrs'] = {'location':'1-5'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert nodelist == ['5'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_attrs_location_all_blocked_nodes(self):
        '''CraySystem._assemble_queue_data: return no locations if attrs location nodes are
        all non idle'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.base_job['attrs'] = {'location':'1-4'}
        nodelist = self.system._assemble_queue_data(self.base_job)
        assert nodelist == [], 'Wrong node in list %s' % nodelist

    def test_find_queue_equivalence_classes_single(self):
        '''CraySystem.find_queue_equivalence_classes: single queue'''
        self.system.find_queue_equivalence_classes([], ['default'], [])
        self.system.current_equivalence_classes
        assert len(self.system.current_equivalence_classes) == 1, 'Have %s equiv classes, should have 1.'
        for equiv in self.system.current_equivalence_classes:
            assert equiv['queues'] == ['default'], 'mismatch in returned equiv class queues'

    def test_find_queue_equivalence_classes_overlap(self):
        '''CraySystem.find_queue_equivalence_classes: partial overlapping queues'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['2'].queues = ['foo', 'default']
        self.system.find_queue_equivalence_classes([], ['default', 'foo'], [])
        assert len(self.system.current_equivalence_classes) == 1, (
                'Have %s equiv classes, should have 1.' %
                len(self.system.current_equivalence_classes))
        for equiv in self.system.current_equivalence_classes:
            assert sorted(equiv['queues']) == ['default', 'foo'], (
                    'mismatch in returned equiv class queues %s' %
                    equiv['queues'])

    def test_find_queue_equivalence_classes_disjoint(self):
        '''CraySystem.find_queue_equivalence_classes: disjoint queues'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['2'].queues = ['foo']
        val = self.system.find_queue_equivalence_classes([], ['default', 'foo'], [])
        self.system.current_equivalence_classes
        expect = [{'reservations': [], 'queues': ['foo']},
                  {'reservations': [], 'queues': ['default']}]
        assert self.system.current_equivalence_classes == expect, (
                'Expected %s, got %s' % (expect,
                    self.system.current_equivalence_classes))
        assert val == self.system.current_equivalence_classes, (
                "val/current_equivalence_class mismatch\nReturn: %s\nInternal: %s")

    def test_clear_draining_for_queues_full_clear(self):
        '''CraySystem._clear_draining_for_queues: clear queue's draining times'''
        for node in self.system.nodes.values():
            node.set_drain(100.0, 300)
        self.system.find_queue_equivalence_classes([], ['default'], [])
        self.system._clear_draining_for_queues('default')
        for node in self.system.nodes.values():
            assert not node.draining, "node %s marked as draining!" % node.node_id

    def test_clear_draining_for_queues_multi_queue(self):
        '''CraySystem._clear_draining_for_queues: clear whole equivalence class'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['2'].queues = ['foo', 'default']
        for node in self.system.nodes.values():
            node.set_drain(100.0, 300)
        self.system.find_queue_equivalence_classes([], ['default', 'foo'], [])
        self.system._clear_draining_for_queues('default')
        for node in self.system.nodes.values():
            assert not node.draining, "node %s marked as draining!" % node.node_id

    def test_clear_drianing_for_queues_one_equiv(self):
        '''CraySystem._clear_draining_for_queues: clear only one equivalence class'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['2'].queues = ['foo']
        for node in self.system.nodes.values():
            node.set_drain(100.0, 300)
        self.system.find_queue_equivalence_classes([], ['default', 'foo'], [])
        self.system._clear_draining_for_queues('default')
        for node in self.system.nodes.values():
            if node.node_id not in ['1', '2']:
                assert not node.draining, "node %s marked as draining!" % node.node_id
            else:
                assert node.draining, "drain should not be cleared for node %s" % node.node_id


    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_first_fit(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Assign basic job to nodes'''
        retval = self.system.find_job_location([self.base_job], [], [])
        assert retval == {1: ['1']}, 'bad loc: expected %s, got %s' % ({1: ['1']}, retval)
        assert self.system.pending_starts[1] == 800.0, (
                'bad pending start: expected %s, got %s' %
                (800.0, self.system.pending_starts[1]))
        assert self.system.nodes['1'].reserved_jobid == 1, 'Node not reserved'
        assert self.system.nodes['1'].reserved_until == 800.0, (
                'reserved until expected 800.0, got %s' % self.system.nodes['1'].reserved_until)

