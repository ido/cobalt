"""Tests for the bgqsystem component of Cobalt.  Right now these focus on subblock handling.

Mock is required for this set of tests to work

"""

from mock import MagicMock, Mock, patch

pybgsched_mock = Mock()
with patch.dict('sys.modules', {'pybgsched':pybgsched_mock}):
    import Cobalt.Components.bgqsystem
    from Cobalt.Components.bgqsystem import BGSystem

class TestBGQSystem(object):
    '''General BGQSystem component tests.'''
    def setup (self):
        #bypass configuration and do not start up UBS thread!
        BGSystem.configure = MagicMock(name='configure')
        BGSystem.update_block_state = MagicMock(name='update_block_state')
        self.bgqsystem = BGSystem()

    def teardown (self):
        pass

    def test_parse_subblock_config_empty(self):

        ret = self.bgqsystem.parse_subblock_config('Empty')
        assert {} == ret, "Failed: String 'Empty' did not return empty dict."

    def test_parse_subblock_config_none(self):
        ret = self.bgqsystem.parse_subblock_config(None)
        assert {} == ret, "Failed: Passing in None did not return empty dict."


    def test_parse_subblock_config_empty_str(self):
        ret = self.bgqsystem.parse_subblock_config('')
        assert {} == ret, "Failed: Passing in  empty string did not return empty dict."

    def test_parse_subblock_cofng_str(self):

        ok_dict ={'TEST-00000-11331-128':32, 
                  'TEST1-22000-33331-128':64,
                  'TEST2-00040-11331-128':1}
        ret = self.bgqsystem.parse_subblock_config(
                'TEST-00000-11331-128:32,TEST1-22000-33331-128:64,TEST2-00040-11331-128:1')
        assert ok_dict == ret, "Failed: Incorrect parsing of test string."

    def test_node_map_gen(self):

        correct_node_map = {0:[0,0,0,0,0],1:[ 0,0,1,0,0],
                           2:[0,1,1,0,0],3:[0,1,0,0,0],
                           4:[0,1,0,0,1],5:[0,1,1,0,1],
                           6:[0,0,1,0,1],7:[0,0,0,0,1],
                           8:[0,1,0,1,1],9:[0,1,1,1,1],
                           10:[0,0,1,1,1],11:[0,0,0,1,1],
                           12:[0,0,0,1,0],13:[0,0,1,1,0],
                           14:[0,1,1,1,0],15:[0,1,0,1,0],
                           16:[1,0,1,1,0],17:[1,0,0,1,0],
                           18:[1,1,0,1,0],19:[1,1,1,1,0],
                           20:[1,1,1,1,1],21:[1,1,0,1,1],
                           22:[1,0,0,1,1],23:[1,0,1,1,1],
                           24:[1,1,1,0,1],25:[1,1,0,0,1],
                           26:[1,0,0,0,1],27:[1,0,1,0,1],
                           28:[1,0,1,0,0],29:[1,0,0,0,0],
                           30:[1,1,0,0,0],31:[1,1,1,0,0]}
        generated_node_map = Cobalt.Components.bgq_base_system.generate_base_node_map()

        for i in range(0,32):
            assert correct_node_map[i] == generated_node_map[i], "Node map failure: expected %s for position %s, got %s"% (correct_node_map[i], i, generated_node_map[i])

    def test_nodeboard_masks(self):

        #make sure that the proper dimension reversals happen.

        assert Cobalt.Components.bgq_base_system.NODECARD_A_DIM_MASK == 4
        assert Cobalt.Components.bgq_base_system.NODECARD_B_DIM_MASK == 8
        assert Cobalt.Components.bgq_base_system.NODECARD_C_DIM_MASK == 1
        assert Cobalt.Components.bgq_base_system.NODECARD_D_DIM_MASK == 2
        assert Cobalt.Components.bgq_base_system.NODECARD_E_DIM_MASK == 8


        for i in range(0,16):
            check = 0
            check += i & Cobalt.Components.bgq_base_system.NODECARD_A_DIM_MASK
            check += i & Cobalt.Components.bgq_base_system.NODECARD_B_DIM_MASK
            check += i & Cobalt.Components.bgq_base_system.NODECARD_C_DIM_MASK
            check += i & Cobalt.Components.bgq_base_system.NODECARD_D_DIM_MASK
            assert i == check, "Mask for %d did not match expected value" % i


        reverse_dims = ([0,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,1,1,0],
                        [1,0,0,0,0],[1,0,1,0,0],[1,0,0,1,0],[1,0,1,1,0], 
                        [0,1,0,0,1],[0,1,1,0,1],[0,1,0,1,1],[0,1,1,1,1],
                        [1,1,0,0,1],[1,1,1,0,1],[1,1,0,1,1],[1,1,1,1,1]) 

        for i in range(0,16):
            rev_A = bool(i & Cobalt.Components.bgq_base_system.NODECARD_A_DIM_MASK)
            rev_B = bool(i & Cobalt.Components.bgq_base_system.NODECARD_B_DIM_MASK)
            rev_C = bool(i & Cobalt.Components.bgq_base_system.NODECARD_C_DIM_MASK)
            rev_D = bool(i & Cobalt.Components.bgq_base_system.NODECARD_D_DIM_MASK)
            rev_E = bool(i & Cobalt.Components.bgq_base_system.NODECARD_E_DIM_MASK)

            assert int(rev_A) == reverse_dims[i][0], "Mismatch in reversed A dimension: board %d, value" % i
            assert int(rev_B) == reverse_dims[i][1], "Mismatch in reversed B dimension: board %d, value" % i
            assert int(rev_C) == reverse_dims[i][2], "Mismatch in reversed C dimension: board %d, value" % i
            assert int(rev_D) == reverse_dims[i][3], "Mismatch in reversed D dimension: board %d, value" % i
            assert int(rev_E) == reverse_dims[i][4], "Mismatch in reversed E dimension: board %d, value" % i

    def test_extents_from_size(self):

        correct_extents = {1:[1, 1, 1, 1, 1],
                           2:[1, 1, 1, 1, 2],
                           4:[1, 1, 1, 2, 2],
                           8:[1, 1, 2, 2, 2],
                           16:[1, 2, 2, 2, 2],
                           32:[2, 2, 2, 2, 2],
                           64:[2, 2, 4, 2, 2],
                           128:[2, 2, 4, 4, 2]}

        for size, extents in correct_extents.iteritems():
            ret_extents = Cobalt.Components.bgq_base_system.get_extents_from_size(size)

            for i in range(0, 5):
                assert ret_extents[i] == extents [i], "Mismatch in extents for size %d"% size


    def test_subblock_pgroup_forker_call(self):
        #make sure that the forker gets proper details for subblock startup.
        #put in enough fake block data to test:
        class FakeBlock(object):
            def __init__(self, spec):
                for arg, val in spec.items():
                    self.__setattr__(arg, val)

        self.bgqsystem._blocks['TEST-00000-00000-1'] = FakeBlock({'name': 'TEST-00000-00000-1',
                                                       'subblock_parent': 'TEST-00000-11331-128',
                                                       'corner_node': 'R00-M0-N00-J00',
                                                       'extents': '1x1x1x1x1',
                                                       'block_type': 'pseudoblock',
                                                       'current_reboots': 0,
                                                       })
        self.bgqsystem._blocks['TEST-00000-11331-128'] = FakeBlock({'name': 'TEST-00000-11331-128',
                                                       'subblock_parent': 'TEST-00000-11331-128',
                                                       'block_type': 'normal',
                                                       'current_reboots': 0,
                                                       })

        pgspec = {'cobalt_log_file': '',
                  'cwd': '', 
                  'executable': '', 
                  'id': 1,
                  'jobid': 1,
                  'kernel': 'default',
                  'kerneloptions': None,
                  'location': ['TEST-00000-00000-1'],
                  'mode': 'c1',
                  'size': 1,
                  'stderr': '', 
                  'stdin': '', 
                  'stdout': '', 
                  'umask': '0022',
                  'starttime': 0.0,
                  'walltime': 600,
                  'killtime': 600.0,
                  'args': [],
                  'user': 'crusher',
                 }
        pg = Cobalt.Components.bgqsystem.BGProcessGroup(pgspec)
        pg.label = 'foo'
        pg.start = MagicMock(name='start')
        pg.head_pid = 1 #since we're not actually executing anything, avoid the start-failure path.
        self.bgqsystem.reserve_resources_until = Mock(name='reserve_resources_until')
        self.bgqsystem._start_process_group(pg, self.bgqsystem._blocks['TEST-00000-00000-1'])
        assert pg.subblock_parent == 'TEST-00000-11331-128', 'bad subblock_parent %s' % pg.subblock_parent
        assert pg.corner == 'R00-M0-N00-J00', 'bad corner'
        assert pg.extents == '1x1x1x1x1', 'bad extents'
        assert pg.subblock == True, 'not marked subblock'

    def test_normal_block_pgroup_forker_call(self):
        #make sure that the forker gets proper details for normal block startup.
        #put in enough fake block data to test:
        class FakeBlock(object):
            def __init__(self, spec):
                for arg, val in spec.items():
                    self.__setattr__(arg, val)

        self.bgqsystem._blocks['TEST-00000-00000-1'] = FakeBlock({'name': 'TEST-00000-00000-1',
                                                       'subblock_parent': 'TEST-00000-11331-128',
                                                       'corner_node': 'R00-M0-N00-J00',
                                                       'extents': '1x1x1x1x1',
                                                       'block_type': 'pseudoblock',
                                                       'current_reboots': 0,
                                                       })
        self.bgqsystem._blocks['TEST-00000-11331-128'] = FakeBlock({'name': 'TEST-00000-11331-128',
                                                       'subblock_parent': 'TEST-00000-11331-128',
                                                       'block_type': 'normal',
                                                       'current_reboots': 0,
                                                       })

        pgspec = {'cobalt_log_file': '',
                  'cwd': '', 
                  'executable': '', 
                  'id': 1,
                  'jobid': 1,
                  'kernel': 'default',
                  'kerneloptions': None,
                  'location': ['TEST-00000-11331-128'],
                  'mode': 'c1',
                  'size': 1,
                  'stderr': '', 
                  'stdin': '', 
                  'stdout': '', 
                  'umask': '0022',
                  'starttime': 0.0,
                  'walltime': 600,
                  'killtime': 600.0,
                  'args': [],
                  'user': 'crusher',
                 }
        pg = Cobalt.Components.bgqsystem.BGProcessGroup(pgspec)
        pg.label = 'foo'
        pg.start = MagicMock(name='start')
        pg.head_pid = 1 #since we're not actually executing anything, avoid the start-failure path.
        self.bgqsystem.reserve_resources_until = Mock(name='reserve_resources_until')
        self.bgqsystem._start_process_group(pg, self.bgqsystem._blocks['TEST-00000-11331-128'])
        assert not pg.subblock, 'not a subblock'
        assert pg.corner is None, 'corner should not be set %s' % pg.corner
        assert pg.subblock_parent is None, 'subblock_parent should not be set %s' % pg.subblock_parent
        assert pg.extents is None, 'extents should not be set %s' % pg.extents
