'''Test the backfill time function from bgq_base_system

'''

from nose import *
from Cobalt.Components.bgq_base_system import BGBaseSystem

class BackfillMockBlock(object):

    def __init__(self, name, state='idle', backfill_time=0.0):
        self.name = name
        self._parents = set()
        self._children = set()
        self._relatives = set()
        self.backfill_time = backfill_time
        self.draining = False
        self.state = state

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def add_parents(self, parent_blocks):
        self._parents.update(set(parent_blocks))
        self._relatives.update(set(parent_blocks))

    def add_children(self, child_blocks):
        self._children.update(set(child_blocks))
        self._relatives.update(set(child_blocks))



class TestBackfillTime(object):

    # Tests for Cobalt.Component.bgq_basse_system.BGBaseSystem.set_backfill_times

    def setup_standard_blocks(self):
        #set up a set of blocks with the following tree:
        #                FullMachine
        #                ^         ^
        #                |         |
        #      _________/|         |\__________
        #     /          |         |           \
        # vert-16k-1 vert-16k-1  horiz-16k-1 horiz-16k-2
        #    |          |            |           |
        #    +----------o---------+  |           |
        #    |          |         |  |           |
        #    |          +---------o--o--------\  |
        #    |          |         |  |        |  |
        #    | /-----+--o---------o--/        |  |
        #    | |     |  |         |           |  |
        #    | |     |  |         |  /--------o--+
        #    | |     |  |         |  |        |  |
        #   8k-1     8k-2         8k-3        8k-4
        #    |        |            |           |
        #   512-1    512-2        512-3       512-4
        #
        #  This gives partial overlaps for the 16k's and should allow us
        #  a good opportunity to test that the function handles overlaps corretly
        #  with jobs in various places
        self.blocks = {'FullMachine':BackfillMockBlock('FullMachine'),
                       'vert-16k-1':BackfillMockBlock('vert-16k-1'),
                       'vert-16k-2':BackfillMockBlock('vert-16k-2'),
                       'horiz-16k-1':BackfillMockBlock('horiz-16k-1'),
                       'horiz-16k-2':BackfillMockBlock('horiz-16k-2'),
                       '8k-1':BackfillMockBlock('8k-1'),
                       '8k-2':BackfillMockBlock('8k-2'),
                       '8k-3':BackfillMockBlock('8k-3'),
                       '8k-4':BackfillMockBlock('8k-4'),
                       '512-1':BackfillMockBlock('512-1'),
                       '512-2':BackfillMockBlock('512-2'),
                       '512-3':BackfillMockBlock('512-3'),
                       '512-4':BackfillMockBlock('512-4'),
                      }

        self.blocks['FullMachine'].add_children([b for b in self.blocks.itervalues() if b.name != 'FullMachine'])
        self.blocks['vert-16k-1'].add_children([self.blocks['8k-1'],self.blocks['8k-3'],self.blocks['512-1'],self.blocks['512-3']])
        self.blocks['vert-16k-2'].add_children([self.blocks['8k-2'],self.blocks['8k-4'],self.blocks['512-2'],self.blocks['512-4']])
        self.blocks['horiz-16k-1'].add_children([self.blocks['8k-1'],self.blocks['8k-2'],self.blocks['512-1'],self.blocks['512-2']])
        self.blocks['horiz-16k-2'].add_children([self.blocks['8k-3'],self.blocks['8k-4'],self.blocks['512-3'],self.blocks['512-4']])
        self.blocks['8k-1'].add_children([self.blocks['512-1']])
        self.blocks['8k-2'].add_children([self.blocks['512-2']])
        self.blocks['8k-3'].add_children([self.blocks['512-3']])
        self.blocks['8k-4'].add_children([self.blocks['512-4']])

        self.blocks['vert-16k-1'].add_parents([self.blocks['FullMachine'], self.blocks['horiz-16k-1'], self.blocks['horiz-16k-2']])
        self.blocks['vert-16k-2'].add_parents([self.blocks['FullMachine'], self.blocks['horiz-16k-1'], self.blocks['horiz-16k-2']])
        self.blocks['horiz-16k-1'].add_parents([self.blocks['FullMachine'], self.blocks['vert-16k-1'], self.blocks['vert-16k-2']])
        self.blocks['horiz-16k-2'].add_parents([self.blocks['FullMachine'], self.blocks['vert-16k-1'], self.blocks['vert-16k-2']])
        self.blocks['8k-1'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-1'], self.blocks['horiz-16k-1']])
        self.blocks['8k-2'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-2'], self.blocks['horiz-16k-1']])
        self.blocks['8k-3'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-1'], self.blocks['horiz-16k-2']])
        self.blocks['8k-4'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-2'], self.blocks['horiz-16k-2']])
        self.blocks['512-1'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-1'], self.blocks['horiz-16k-1'], self.blocks['8k-1']])
        self.blocks['512-2'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-2'], self.blocks['horiz-16k-1'], self.blocks['8k-2']])
        self.blocks['512-3'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-1'], self.blocks['horiz-16k-2'], self.blocks['8k-3']])
        self.blocks['512-4'].add_parents([self.blocks['FullMachine'] ,self.blocks['vert-16k-2'], self.blocks['horiz-16k-2'], self.blocks['8k-4']])

        return

    def set_blocking_states(self, block_name, state):
        #set a blocks states and make sure relatives are blocked appropriately
        self.blocks[block_name].state = state
        for block in self.blocks[block_name]._relatives:
            block.state='blocked'

    def setup_mira_32k_test_blocks(self):
        self.blocks = {'MIR-00000-7BFF1-49152':BackfillMockBlock('MIR-00000-7BFF1-49152'),
                       'MIR-00000-77FF1-32768':BackfillMockBlock('MIR-00000-77FF1-32768'),
                       'MIR-04000-7BFF1-32768':BackfillMockBlock('MIR-04000-7BFF1-32768'),
                       'MIR-00000-7BFF1-0100-32768':BackfillMockBlock('MIR-00000-7BFF1-0100-32768', 'busy'),
                       'MIR-00000-73FF1-16384':BackfillMockBlock('MIR-00000-73FF1-16384'),
                       'MIR-04000-77FF1-16384':BackfillMockBlock('MIR-04000-77FF1-16384'),
                       'MIR-08000-7BFF1-16384':BackfillMockBlock('MIR-08000-7BFF1-16384'),
                       'MIR-00000-33331-512':BackfillMockBlock('MIR-00000-33331-512'),
                       }
        self.blocks['MIR-00000-7BFF1-49152'].add_children([b for b in self.blocks.itervalues() if b.name != 'MIR-00000-7BFF1-49152'])
        self.blocks['MIR-00000-77FF1-32768'].add_children([self.blocks['MIR-00000-73FF1-16384'], self.blocks['MIR-04000-77FF1-16384'], self.blocks['MIR-00000-33331-512']])
        self.blocks['MIR-00000-7BFF1-0100-32768'].add_children([self.blocks['MIR-00000-73FF1-16384'], self.blocks['MIR-08000-7BFF1-16384'], self.blocks['MIR-00000-33331-512']])
        self.blocks['MIR-04000-7BFF1-32768'].add_children([self.blocks['MIR-08000-7BFF1-16384'], self.blocks['MIR-04000-77FF1-16384']])
        self.blocks['MIR-00000-73FF1-16384'].add_children([self.blocks['MIR-00000-33331-512']])

        self.blocks['MIR-00000-77FF1-32768'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-00000-7BFF1-0100-32768'],
            self.blocks['MIR-04000-7BFF1-32768']])
        self.blocks['MIR-04000-7BFF1-32768'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-00000-7BFF1-0100-32768'],
            self.blocks['MIR-00000-77FF1-32768']])
        self.blocks['MIR-00000-7BFF1-0100-32768'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-00000-77FF1-32768'],
            self.blocks['MIR-04000-7BFF1-32768']])
        self.blocks['MIR-00000-73FF1-16384'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-00000-77FF1-32768'],
            self.blocks['MIR-00000-7BFF1-0100-32768']])
        self.blocks['MIR-04000-77FF1-16384'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-04000-7BFF1-32768'],
            self.blocks['MIR-00000-77FF1-32768']])
        self.blocks['MIR-08000-7BFF1-16384'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-04000-7BFF1-32768'],
            self.blocks['MIR-00000-7BFF1-0100-32768']])
        self.blocks['MIR-00000-33331-512'].add_parents([self.blocks['MIR-00000-7BFF1-49152'], self.blocks['MIR-00000-77FF1-32768'],
            self.blocks['MIR-00000-7BFF1-0100-32768'], self.blocks['MIR-00000-73FF1-16384']])


    def test_mira_32_16_512_backfill(self):
        #This came from a situation that occurred during acceptance testing
        #You have a 32k running long, and a short 512, the backfill time (and therefore
        #the drain preference) should be set such that you drain over the 512, not the 32k
        self.setup_mira_32k_test_blocks()
        now = 100.0
        now_delta = 400.0
        job_done_1= 600.0
        job_done_2= 500.0
        job_end_times = {'MIR-04000-7BFF1-32768':job_done_1, 'MIR-00000-33331-512':job_done_2}
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['MIR-00000-73FF1-16384'].backfill_time == job_done_2, "MIR-00000-73FF1-16384 has backfill_time"\
                " of %s should be %s" % (self.blocks['MIR-00000-73FF1-16384'].backfill_time, job_done_2)
        assert self.blocks['MIR-04000-77FF1-16384'].backfill_time == job_done_1, "MIR-00000-73FF1-16384 has backfill_time"\
                " of %s should be %s" % (self.blocks['MIR-04000-77FF1-16384'].backfill_time, job_done_1)

    def test_parent_inherit(self):
        self.setup_standard_blocks()
        now = 100.0
        jobdone = 500.0
        job_end_times = {'512-1':jobdone}
        self.set_blocking_states('512-1', 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['8k-1'].backfill_time == jobdone, "Parent did not recieve correct time"

    def test_child_inherit(self):
        self.setup_standard_blocks()
        now = 100.0
        jobdone = 500.0
        job_end_times = {'8k-1':jobdone}
        self.set_blocking_states('8k-1', 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['512-1'].backfill_time == jobdone, "Child did not recieve correct time"

    def test_minimum_window(self):
        self.setup_standard_blocks()
        now = 100.0
        now_delta = 400.0
        jobdone = 300.0
        job_end_times = {'8k-1':jobdone}
        self.set_blocking_states('8k-1', 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['8k-1'].backfill_time == now_delta, "Minimum backfill window not set."


    def test_overlap_v16blocking_8k_secondary(self):
        self.setup_standard_blocks()
        now = 100.0
        job_done_1 = 600.0
        job_done_2 = 500.0
        job_end_times = {'8k-2':job_done_2, 'vert-16k-1':job_done_1}
        for key in job_end_times.keys():
            self.set_blocking_states(key, 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['vert-16k-1'].backfill_time == job_done_1, 'vert-16k-1 has time %s should be %s' % (self.blocks['vert-16k-1'].backfill_time, job_done_1)
        assert self.blocks['horiz-16k-1'].backfill_time == job_done_1, 'horiz-16k-1 has time %s should be %s' % (self.blocks['horiz-16k-1'].backfill_time, job_done_1)
        assert self.blocks['8k-2'].backfill_time == job_done_2, '8k-2 has time %s should be %s' % (self.blocks['8k-2'].backfill_time, job_done_2)
        assert self.blocks['8k-3'].backfill_time == job_done_1, '8k-2 has time %s should be %s' % (self.blocks['8k-3'].backfill_time, job_done_1)
        assert self.blocks['512-2'].backfill_time == job_done_2, '512-2 has time %s should be %s' % (self.blocks['512-2'].backfill_time, job_done_2)
        assert self.blocks['512-1'].backfill_time == job_done_1, '512-1 has time %s should be %s' % (self.blocks['512-1'].backfill_time, job_done_1)
        assert self.blocks['512-4'].backfill_time == job_done_2, '512-4 has time %s should be %s' % (self.blocks['512-4'].backfill_time, job_done_2)


    def test_overlap_8kblocking_v16_secondary(self):
        self.setup_standard_blocks()
        now = 100.0
        job_done_1 = 600.0
        job_done_2 = 500.0
        job_end_times = {'8k-2':job_done_1, 'vert-16k-1':job_done_2}
        for key in job_end_times.keys():
            self.set_blocking_states(key, 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert self.blocks['vert-16k-1'].backfill_time == job_done_2, 'vert-16k-1 has time %s should be %s' % (self.blocks['vert-16k-1'].backfill_time, job_done_1)
        assert self.blocks['vert-16k-2'].backfill_time == job_done_1, 'vert-16k-2 has time %s should be %s' % (self.blocks['vert-16k-2'].backfill_time, job_done_1)
        assert self.blocks['horiz-16k-1'].backfill_time == job_done_1, 'horiz-16k-1 has time %s should be %s' % (self.blocks['horiz-16k-1'].backfill_time, job_done_1)
        assert self.blocks['8k-2'].backfill_time == job_done_1, '8k-2 has time %s should be %s' % (self.blocks['8k-2'].backfill_time, job_done_1)
        assert self.blocks['8k-3'].backfill_time == job_done_2, '8k-2 has time %s should be %s' % (self.blocks['8k-3'].backfill_time, job_done_2)
        assert self.blocks['512-2'].backfill_time == job_done_1, '512-2 has time %s should be %s' % (self.blocks['512-2'].backfill_time, job_done_1)
        assert self.blocks['512-1'].backfill_time == job_done_2, '512-1 has time %s should be %s' % (self.blocks['512-1'].backfill_time, job_done_2)
        assert self.blocks['512-4'].backfill_time == job_done_2, '512-4 has time %s should be %s' % (self.blocks['512-4'].backfill_time, job_done_2)


    def test_overlap_v16blocking_8k_secondary_short_time(self):
        self.setup_standard_blocks()
        now = 250.0
        now_delta = 550.0
        job_done_1 = 600.0
        job_done_2 = 500.0
        job_end_times = {'8k-2':job_done_2, 'vert-16k-1':job_done_1}
        for key in job_end_times.keys():
            self.set_blocking_states(key, 'allocated')
        BGBaseSystem.set_backfill_times(self.blocks, job_end_times, now)
        assert job_done_2 not in [val.backfill_time  for val in self.blocks.values()], "Minimum backfill shadow not honored."
        assert self.blocks['vert-16k-1'].backfill_time == job_done_1, 'vert-16k-1 has time %s should be %s' % (self.blocks['vert-16k-1'].backfill_time, job_done_1)
        assert self.blocks['vert-16k-2'].backfill_time == now_delta, 'vert-16k-2 has time %s should be %s' % (self.blocks['vert-16k-2'].backfill_time, now_delta)
        assert self.blocks['horiz-16k-1'].backfill_time == job_done_1, 'horiz-16k-1 has time %s should be %s' % (self.blocks['horiz-16k-1'].backfill_time, job_done_1)
        assert self.blocks['8k-2'].backfill_time == now_delta, '8k-2 has time %s should be %s' % (self.blocks['8k-2'].backfill_time, now_delta)
        assert self.blocks['8k-3'].backfill_time == job_done_1, '8k-2 has time %s should be %s' % (self.blocks['8k-3'].backfill_time, job_done_1)
        assert self.blocks['512-2'].backfill_time == now_delta, '512-2 has time %s should be %s' % (self.blocks['512-2'].backfill_time, now_delta)
        assert self.blocks['512-1'].backfill_time == job_done_1, '512-1 has time %s should be %s' % (self.blocks['512-1'].backfill_time, job_done_1)
        assert self.blocks['512-4'].backfill_time == now_delta, '512-4 has time %s should be %s' % (self.blocks['512-4'].backfill_time, now_delta)

