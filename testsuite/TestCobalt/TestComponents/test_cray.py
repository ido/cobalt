# Test Cray-specific utilities/calls.
SYSTEM_CONFIG_ENTRY = """
[system]
size: 10
elogin_hosts: foo:bar
"""
import Cobalt
import TestCobalt
config_file = Cobalt.CONFIG_FILES[0]
config_fp = open(config_file, "w")
config_fp.write(SYSTEM_CONFIG_ENTRY)
config_fp.close()

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

def fake_alps_reserve(user, jobid, nodes, attrs, node_id_list):
    '''mock for AlpsBridge.reserve method'''
    assert type(node_id_list) == type([])
    ret_info = {'reserved_nodes': node_id_list,
                'reservation_id': 1,
                }
    return ret_info

def return_none(*args, **kwargs):
    return None


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
                'queue':'default', 'nodes': 1, 'walltime': 60,
                }
        self.fake_reserve_called = False
        Cobalt.Components.system.CraySystem.BACKFILL_EPSILON = 120
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "first-fit"

    def teardown(self):
        del self.system
        del self.base_job
        Cobalt.Components.system.CraySystem.BACKFILL_EPSILON = 120
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "first-fit"
        self.fake_reserve_called = False


    # HELPER MOCK FUNCTIONS
    def fake_reserve(self, job, new_time, node_id_list):
        '''Mimic first-fit function of ALPS placement scheme'''
        # self gets overriden by the call within fjl to be the real system
        # component.
        self.fake_reserve_called = True
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

    def test_assemble_queue_data_attrs_location_any_not_down(self):
        '''CraySystem._assemble_queue_data: attrs locaiton return any not down'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.base_job['attrs'] = {'location':'1-5'}
        self.base_job['nodes'] = 4
        nodelist = self.system._assemble_queue_data(self.base_job, idle_only=False)
        assert nodelist == ['1', '2', '3', '5'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_attrs_location_any_not_down_drain_limit(self):
        '''CraySystem._assemble_queue_data: attrs locaiton return any not down in drain window'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.system.nodes['1'].set_drain(500.0, 1)
        self.system.nodes['2'].set_drain(600.0, 2)
        self.system.nodes['3'].set_drain(700.0, 3)
        self.base_job['attrs'] = {'location':'1-5'}
        self.base_job['nodes'] = 2
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False, drain_time=650)
        assert nodelist == ['5'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_attrs_location_any_not_down_drain_limit_no_ep(self):
        '''CraySystem._assemble_queue_data: attrs locaiton return any not down in drain window no epsilon'''
        Cobalt.Components.system.CraySystem.BACKFILL_EPSILON = 0
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'cleanup-pending'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].status = 'ADMINDOWN'
        self.system.nodes['1'].set_drain(500.0, 1)
        self.system.nodes['2'].set_drain(600.0, 2)
        self.system.nodes['3'].set_drain(700.0, 3)
        self.base_job['attrs'] = {'location':'1-5'}
        self.base_job['nodes'] = 2
        nodelist = self.system._assemble_queue_data(self.base_job,
                idle_only=False, drain_time=650)
        assert nodelist == ['3', '5'], 'Wrong node in list %s' % nodelist

    def test_assemble_queue_data_non_draining(self):
        '''CraySystem._assemble_queue_data: return idle and non draining only'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'down'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].set_drain(100, 1)
        nodelist = self.system._assemble_queue_data(self.base_job,
                drain_time=150)
        assert_match(sorted(nodelist), ['5'], "Bad Nodelist")

    def test_assemble_queue_data_within_draining(self):
        '''CraySystem._assemble_queue_data: return idle and draining if within
        time'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'down'
        self.system.nodes['3'].set_drain(50.0, 2)
        self.system.nodes['4'].set_drain(220.0, 1) #add in epsilon
        nodelist = self.system._assemble_queue_data(self.base_job,
                drain_time=90.0)
        assert_match(sorted(nodelist), ['4', '5'], "Bad Nodelist")

    def test_assemble_queue_data_match_draining(self):
        '''CraySystem._assemble_queue_data: return idle and matched drain node'''
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'down'
        self.system.nodes['3'].status = 'allocated'
        self.system.nodes['4'].set_drain(220.0, 1) #add in epsilon
        nodelist = self.system._assemble_queue_data(self.base_job,
                drain_time=100.0)
        assert_match(sorted(nodelist), ['4', '5'], "Bad Nodelist")

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

    def test_find_queue_equivalence_classes_disjoint_reservation(self):
        '''CraySystem.find_queue_equivalence_classes: bind reservation all eq classes'''
        self.system.nodes['1'].queues = ['foo']
        self.system.nodes['2'].queues = ['foo']
        val = self.system.find_queue_equivalence_classes({'test':'1-2,4-5'}, ['default', 'foo'], [])
        self.system.current_equivalence_classes
        expect = [{'reservations': ['test'], 'queues': ['foo']},
                  {'reservations': ['test'], 'queues': ['default']}]
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

    def test_select_nodes_for_draining_single_job(self):
        '''CraySystem._select_nodes_for_draining: drain nodes from a single job'''
        end_times = [[['1-3'], 100]]
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.base_job['nodes'] = 4
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1', '2', '3', '4'], "Bad Selection.")

    def test_select_nodes_for_draining_user_location(self):
        '''CraySystem._select_nodes_for_draining: drain nodes for user specified location'''
        end_times = [[['1-3'], 100]]
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.base_job['nodes'] = 4
        self.base_job['attrs'] = {'location':'2-5'}
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['2', '3', '4', '5'], "Bad Selection.")

    def test_select_nodes_for_draining_prefer_running(self):
        '''CraySystem._select_nodes_for_draining: prefer nodes from running job'''
        end_times = [[['4-5'], 100]]
        self.system.nodes['4'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.base_job['nodes'] = 4
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1', '2', '4', '5'], "Bad Selection.")

    def test_select_nodes_for_draining_only_running(self):
        '''CraySystem._select_nodes_for_draining: fit entirely in running job if possible'''
        end_times = [[['2-5'], 100]]
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.base_job['nodes'] = 2
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['2', '3'], "Bad Selection.")

    def test_select_nodes_for_draining_correct_time(self):
        '''CraySystem._select_nodes_for_draining: set correct drain times single job'''
        end_times = [[['5'], 100]]
        self.system.nodes['5'].status = 'busy'
        self.base_job['nodes'] = 5
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        for i in range(1, 6):
            assert_match(self.system.nodes[str(i)].draining, True,
                "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, 100, "Bad drain time")

    def test_select_nodes_for_draining_multiple_running(self):
        '''CraySystem._select_nodes_for_draining: choose from shortest job to drain'''
        end_times = [[['2-3'], 100.0], [['4-5'], 91.0]]
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'allocated'
        self.system.nodes['5'].status = 'allocated'
        self.base_job['nodes'] = 3
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1' ,'4' , '5'], "Bad Selection")
        for i in ['1', '4', '5']:
            assert_match(self.system.nodes[str(i)].draining, True,
                "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, 91, "Bad drain time")

    def test_select_nodes_for_draining_select_multiple_running(self):
        '''CraySystem._select_nodes_for_draining: set time to longest if draining from multiple jobs'''
        end_times = [[['2-3'], 100.0], [['4-5'], 91.0]]
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'allocated'
        self.system.nodes['5'].status = 'allocated'
        self.base_job['nodes'] = 5
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1', '2', '3', '4' , '5'], "Bad Selection")
        for i in range(1,6):
            assert_match(self.system.nodes[str(i)].draining, True,
                "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, 100, "Bad drain time")

    def test_select_nodes_for_draining_select_queue(self):
        '''CraySystem._select_nodes_for_draining: confine to proper queue'''
        self.base_job['queue'] = 'bar'
        end_times = [[['5'], 100.0], [['2'], 50.0]]
        self.system.nodes['1'].queues = ['default']
        self.system.nodes['2'].queues = ['default']
        self.system.nodes['3'].queues = ['bar']
        self.system.nodes['4'].queues = ['default', 'bar']
        self.system.nodes['5'].queues = ['default', 'bar']
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.system.find_queue_equivalence_classes([],['default', 'bar'],[])
        self.system._gen_node_to_queue()
        self.base_job['nodes'] = 3
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['3', '4', '5'], "Bad Selection")
        for i in range(3,6):
            assert_match(self.system.nodes[str(i)].draining, True,
                "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, 100, "Bad drain time")

    def test_select_nodes_for_draining_select_cleaning(self):
        '''CraySystem._select_nodes_for_draining: include cleaning nodes if marked'''
        end_times = []
        now = int(time.time())
        self.system.nodes['2'].status = 'cleanup'
        self.system.nodes['5'].status = 'cleanup-pending'
        self.system.nodes['2'].set_drain(now + 300, -1)
        self.system.nodes['5'].set_drain(now + 300, -1)
        self.base_job['nodes'] = 5
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1', '2', '3', '4', '5'], "Bad Selection")
        for i in range(1,6):
            assert_match(self.system.nodes[str(i)].draining, True, "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, now + 300, "Bad drain time")

    def test_select_nodes_for_draining_running_but_down(self):
        '''CraySystem._select_nodes_for_draining: do not drain down node if job still "running"'''
        # If a node dies while a job is running, it will still show up in the
        # end-times range until termination of that job is complete.
        end_times = [[['1-4'], 100.0]]
        self.system.nodes['2'].status = 'down'
        self.base_job['nodes'] = 4
        drain_nodes = self.system._select_nodes_for_draining(self.base_job,
                end_times)
        assert_match(sorted(drain_nodes), ['1', '3', '4', '5'], "Bad Selection")
        assert_match(self.system.nodes['2'].draining, False, "Draining set")
        assert_match(self.system.nodes['2'].drain_jobid, None, "Should not have drain_jobid", is_match)
        assert_match(self.system.nodes['2'].drain_until, None, "Should not have drain_until", is_match)
        for i in ['1', '3', '4', '5']:
            assert_match(self.system.nodes[str(i)].draining, True, "Draining not set")
            assert_match(self.system.nodes[str(i)].drain_jobid, 1, "Bad drain job")
            assert_match(self.system.nodes[str(i)].drain_until, 100.0, "Bad drain time")

    # common checks for find_job_location
    def assert_draining(self, nid, until, drain_jobid):
        assert self.system.nodes[str(nid)].draining, "Node %s should be draining" % nid
        assert_match(self.system.nodes[str(nid)].drain_until, until,
                "Bad drain_until: node %s" % nid)
        assert_match(self.system.nodes[str(nid)].drain_jobid, drain_jobid,
                "Bad drain_jobid: node %s" % nid)

    def assert_not_draining(self, nid):
        assert not self.system.nodes[str(nid)].draining, "Node %s should not be draining" % nid
        assert_match(self.system.nodes[str(nid)].drain_until, None,
                     "Bad drain_until: node %s" % nid, is_match)
        assert_match(self.system.nodes[str(nid)].drain_jobid, None,
                     "Bad drain_jobid: node %s" % nid, is_match)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_first_fit(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Assign basic job to nodes'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "first-fit"
        retval = self.system.find_job_location([self.base_job], [], [])
        assert retval == {1: ['1']}, 'bad loc: expected %s, got %s' % ({1: ['1']}, retval)
        assert self.system.pending_starts[1] == 800.0, (
                'bad pending start: expected %s, got %s' %
                (800.0, self.system.pending_starts[1]))
        assert self.system.nodes['1'].reserved_jobid == 1, 'Node not reserved'
        assert self.system.nodes['1'].reserved_until == 800.0, (
                'reserved until expected 800.0, got %s' % self.system.nodes['1'].reserved_until)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_first_fit_prior_job(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Assign second job to nodes'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "first-fit"
        self.system.nodes['2'].status = 'allocated'
        self.system.nodes['2'].reserved_jobid = 2
        retval = self.system.find_job_location([self.base_job],
                [[['2'], int(time.time()) + 3600 ]], [])
        assert retval == {1: ['1']}, 'bad loc: expected %s, got %s' % ({1: ['1']}, retval)
        assert self.system.pending_starts[1] == 800.0, (
                'bad pending start: expected %s, got %s' %
                (800.0, self.system.pending_starts[1]))
        assert self.system.nodes['1'].reserved_jobid == 1, 'Node not reserved'
        assert self.system.nodes['1'].reserved_until == 800.0, (
                'reserved until expected 800.0, got %s' % self.system.nodes['1'].reserved_until)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_one_eq(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Assign job to w/drain'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        retval = self.system.find_job_location([self.base_job], [], [])
        assert retval == {1: ['1']}, 'bad loc: expected %s, got %s' % ({1: ['1']}, retval)
        assert self.system.pending_starts[1] == 800.0, (
                'bad pending start: expected %s, got %s' %
                (800.0, self.system.pending_starts[1]))
        assert self.system.nodes['1'].reserved_jobid == 1, 'Node not reserved'
        assert self.system.nodes['1'].reserved_until == 800.0, (
                'reserved until expected 800.1, got %s' % self.system.nodes['1'].reserved_until)
        for i in range(1,6):
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_for_large(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Drain for large job, block other'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        jobs.append(dict(self.base_job))
        jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 5
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 1
        jobs[1]['walltime'] = 400
        self.system.reserve_resources_until('1', 100, 1)
        self.system.nodes['1'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['1'], 600]], [])
        assert_match(retval, {}, "no location should be assigned")
        assert_match(self.system.pending_starts, {}, "no starts should be pending")
        for i in range(1,6):
            self.assert_draining(i, 600, 2)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_first_fit_despite_larger(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: First fit smaller job ahead of large job'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "first-fit"
        jobs = []
        jobs.append(dict(self.base_job))
        jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 5
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 1
        jobs[1]['walltime'] = 400
        self.system.reserve_resources_until('1', 600, 1)
        self.system.nodes['1'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['1'], 600]], [])
        assert_match(retval, {3: ['2']}, "bad location")
        assert_match(self.system.pending_starts, {3: 800.0}, "no starts should be pending")
        for i in range(1, 6):
            # first fit should never set drain characteristics.
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_on_running(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Drain: Favor running location'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,2):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 3
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 2
        jobs[1]['walltime'] = 400
        self.system.reserve_resources_until('3-5', 100, 1)
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['3-5'], 600]], [])
        assert_match(retval, {3: ['1-2']}, 'bad location')
        assert_match(self.system.pending_starts, {3: 800.0}, "bad pending start")
        for i in range(3,6):
            self.assert_draining(i, 600, 2)
        for i in range(1,3):
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_no_drain_on_down(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Drain: Do not drain if insufficient hardware'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,2):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 5
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 2
        jobs[1]['walltime'] = 400
        self.system.reserve_resources_until('2,5', 100, 1)
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'down'
        self.system.nodes['5'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['2,5'], 600]], [])
        assert_match(retval, {3: ['1,4']}, 'bad location')
        assert_match(self.system.pending_starts, {3: 800.0}, "bad pending start")
        for i in range(1, 6):
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(CraySystem, 'update_node_state')
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_correct_queue(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Drain correct queue'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,2):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 2
        jobs[0]['walltime'] = 500
        jobs[0]['queue'] = 'bar'
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 1
        jobs[1]['walltime'] = 400
        jobs[1]['queue'] = 'bar'
        self.system.reserve_resources_until('2,5', 600, 1)
        self.system.update_nodes({'queues': 'foo:default'}, ['1', '2'], None)
        self.system.update_nodes({'queues': 'bar:default'}, ['4', '5'], None)
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default', 'foo', 'bar'], [])
        retval = self.system.find_job_location(jobs, [[['2,5'], 600]], [])
        assert_match(retval, {}, 'bad location')
        assert_match(self.system.pending_starts, {}, "bad pending start")
        for i in [4, 5]:
            self.assert_draining(i, 600, 2)
        for i in [1, 2, 3]:
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(CraySystem, 'update_node_state')
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_correct_queue_run_short_job(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: Drain correct queue, run short job'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,2):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 2
        jobs[0]['walltime'] = 500
        jobs[0]['queue'] = 'bar'
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 1
        jobs[1]['walltime'] = 3
        jobs[1]['queue'] = 'bar'
        self.system.reserve_resources_until('2,5', 1000, 1)
        self.system.update_nodes({'queues': 'foo:default'}, ['1', '2'], None)
        self.system.update_nodes({'queues': 'bar:default'}, ['4', '5'], None)
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['5'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default', 'foo', 'bar'], [])
        retval = self.system.find_job_location(jobs, [[['2,5'], 1000]], [])
        assert_match(retval, {3: ['4']}, 'bad location')
        assert_match(self.system.pending_starts, {3: 800.0}, "bad pending start")
        for i in [4, 5]:
            self.assert_draining(i, 1000, 2)
        for i in [1, 2, 3]:
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_only_required(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: drain only attrs=location nodes'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,2):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 3
        jobs[0]['walltime'] = 500
        jobs[0]['attrs'] = {'location': '1,3,5'}
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 3
        jobs[1]['walltime'] = 400
        self.system.reserve_resources_until('1', 600, 1)
        self.system.nodes['1'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['1'], 600]], [])
        assert_match(retval, {}, 'bad location')
        assert_match(self.system.pending_starts, {}, "bad pending start")
        for i in [1, 3, 5]:
            self.assert_draining(i, 600, 2)
        for i in [2, 4]:
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_multiple(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: drain for multiple jobs'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,3):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 2
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 2
        jobs[1]['walltime'] = 400
        jobs[2]['jobid'] = 4
        jobs[2]['nodes'] = 1
        jobs[2]['walltime'] = 1500
        self.system.reserve_resources_until('1', 600, 1)
        self.system.reserve_resources_until('2-3', 550, 5)
        self.system.reserve_resources_until('4', 700, 6)
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['2-3'], 550.0], [['1'],
            600.0], [['4'], 700.0]], [])
        assert_match(retval, {}, 'bad location')
        assert_match(self.system.pending_starts, {}, "bad pending start")
        for i in [1, 5]:
            self.assert_draining(i, 600, 3)
        for i in [2, 3]:
            self.assert_draining(i, 550, 2)
        for i in [4]:
            self.assert_draining(i, 700, 4)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_drain_multiple_and_run(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: drain for multiple jobs, run leftover'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,3):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 2
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 3
        jobs[1]['nodes'] = 2
        jobs[1]['walltime'] = 400
        jobs[2]['jobid'] = 4
        jobs[2]['nodes'] = 1
        jobs[2]['walltime'] = 1500
        self.system.reserve_resources_until('1,4', 600, 1)
        self.system.reserve_resources_until('2-3', 550, 5)
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['2-3'], 550.0], [['1,4'],
            600.0]], [])
        assert_match(retval, {4: ['5']}, 'bad location')
        assert_match(self.system.pending_starts, {4: 800.0}, "bad pending start")
        for i in [1, 4]:
            self.assert_draining(i, 600, 3)
        for i in [2, 3]:
            self.assert_draining(i, 550, 2)
        for i in [5]:
            self.assert_not_draining(i)

    @patch.object(CraySystem, '_ALPS_reserve_resources', fake_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test_find_job_location_allocate_no_drain_after_run(self, *args, **kwargs):
        '''CraySystem.find_job_locaton: no drain computation after run'''
        Cobalt.Components.system.CraySystem.DRAIN_MODE = "backfill"
        jobs = []
        for _ in range(0,3):
            jobs.append(dict(self.base_job))
        jobs[0]['jobid'] = 2
        jobs[0]['nodes'] = 2
        jobs[0]['walltime'] = 500
        jobs[1]['jobid'] = 4
        jobs[1]['nodes'] = 1
        jobs[1]['walltime'] = 1500
        jobs[2]['jobid'] = 3
        jobs[2]['nodes'] = 2
        jobs[2]['walltime'] = 400
        self.system.reserve_resources_until('1,4', 600, 1)
        self.system.reserve_resources_until('2-3', 550, 5)
        self.system.nodes['1'].status = 'busy'
        self.system.nodes['2'].status = 'busy'
        self.system.nodes['3'].status = 'busy'
        self.system.nodes['4'].status = 'busy'
        self.system.find_queue_equivalence_classes([], ['default'], [])
        retval = self.system.find_job_location(jobs, [[['2-3'], 550.0], [['1,4'],
            600.0]], [])
        assert_match(retval, {4: ['5']}, 'bad location')
        assert_match(self.system.pending_starts, {4: 800.0}, "bad pending start")
        for i in [2, 3]:
            self.assert_draining(i, 550, 2)
        for i in [1, 4, 5]:
            self.assert_not_draining(i)

    def test_validate_job_normal(self):
        '''CraySystem.validate_job: valid job submission'''
        expected = {'nodecount': 1, 'proccount': 1, 'mode': 'script', 'attrs': {'numa': 'quad', 'mcdram': 'cache'}}
        spec = {'mode':'script', 'nodecount': 1}
        ret_spec = self.system.validate_job(spec)
        assert_match(expected, ret_spec, "Invalid spec returned")

    @raises(Cobalt.Exceptions.JobValidationError)
    def test_validate_job_reject_too_large(self):
        '''CraySystem.validate_job: reject too big job'''
        spec  = {'mode':'script', 'nodecount': 9999}
        ret_spec = self.system.validate_job(spec)

    @raises(Cobalt.Exceptions.JobValidationError)
    def test_validate_job_reject_no_host(self):
        '''CraySystem.validate_job: reject missing ssh host'''
        spec  = {'mode':'interactive', 'nodecount': 1, 'qsub_host':'foo'}
        ret_spec = self.system.validate_job(spec)

    #CraySystem._ALPS_reserve_resources test functions

    @staticmethod
    def verify_alps_reservation_dict(system):
        '''check and make sure keys are always strings.'''
        for key in system.alps_reservations.keys():
            assert type(key) == type("string")


    @patch('Cobalt.Components.system.CraySystem.ALPSBridge.reserve', fake_alps_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test__ALPS_reserve_resources(self, *args, **kwargs):
        '''CraySystem._ALPS_reserve_resources: Set valid reservation dictionary entry'''
        job = {'user': 'frodo',
               'jobid': '1',
               'nodes': 5,
               'attrs': {},
               }
        node_id_list = [str(i) for i in xrange(1, 6)]
        new_time = 600.0
        info = self.system._ALPS_reserve_resources(job, new_time, node_id_list)
        assert_match(info, node_id_list, 'Bad reservation info returned')
        TestCraySystem.verify_alps_reservation_dict(self.system)

    @patch('Cobalt.Components.system.CraySystem.ALPSBridge.reserve', return_none)
    def test__ALPS_reserve_resources_reserve_None(self):
        '''CraySystem._ALPS_reserve_resources: No built reservation if None returned'''
        job = {'user': 'frodo',
               'jobid': '1',
               'nodes': 5,
               'attrs': {},
               }
        node_id_list = [str(i) for i in xrange(1, 6)]
        new_time = 600.0
        info = self.system._ALPS_reserve_resources(job, new_time, node_id_list)
        assert_match(info, None, 'Bad reservation info returned', is_match)
        assert_match(len(self.system.alps_reservations.keys()), 0, "Wrong number of entries.")
        TestCraySystem.verify_alps_reservation_dict(self.system)

    def test__ALPS_reserve_resources_handle_ALPS_error(self):
        '''CraySystem._ALPS_reserve_resources: Raise ALPS Exception'''
        Cobalt.Components.system.CraySystem.ALPSBridge.reserve = MagicMock(side_effect=AlpsBridge.ALPSError('test failure', 'ERROR'))
        job = {'user': 'frodo',
               'jobid': '1',
               'nodes': 5,
               'attrs': {},
               }
        node_id_list = [str(i) for i in xrange(1, 6)]
        new_time = 600.0
        info = self.system._ALPS_reserve_resources(job, new_time, node_id_list)
        assert_match(info, None, 'Bad reservation info returned', is_match)
        assert_match(len(self.system.alps_reservations.keys()), 0, "Wrong number of entries.")
        TestCraySystem.verify_alps_reservation_dict(self.system)

    @patch('Cobalt.Components.system.CraySystem.ALPSBridge.reserve', fake_alps_reserve)
    @patch.object(time, 'time', return_value=500.000)
    def test__ALPS_reserve_resources_bad_int_pass(self, *args, **kwargs):
        '''CraySystem._ALPS_reserve_resources: Force integer to string key'''
        job = {'user': 'frodo',
               'jobid': 1,
               'nodes': 5,
               'attrs': {},
               }
        node_id_list = [str(i) for i in xrange(1, 6)]
        new_time = 600.0
        info = self.system._ALPS_reserve_resources(job, new_time, node_id_list)
        assert_match(info, node_id_list, 'Bad reservation info returned')
        TestCraySystem.verify_alps_reservation_dict(self.system)
