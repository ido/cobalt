"""Tests for Cobalt v1 reservations"""

import time

import Cobalt.Components.bgsched
from Cobalt.Components.bgsched import Reservation
from Cobalt.Data import IncrID
from testsuite.TestCobalt.Utilities.assert_functions import assert_match

class TestReservations(object):

    def setup(self):
        Cobalt.Components.bgsched.bgsched_cycle_id_gen = IncrID()
        Cobalt.Components.bgsched.bgsched_id_gen = IncrID()
        self.base_res_spec = {'name': 'test', 'start': 100, 'duration': 60, 'cycle': None, 'users': None, 'partitions': '0-10',
                'queue': None, 'res_id': 1, 'resource_list': {}}

    def test_reservation_creation(self):
        '''reservation creation'''
        res = Reservation(self.base_res_spec)
        assert_match(res.name, 'test', 'bad name')
        assert_match(res.start, 100, 'bad start time')
        assert_match(res.duration, 60, 'bad duration')
        assert_match(res.cycle, None, 'bad cycle')
        assert_match(res.cycle_id, None, 'bad cycle_id')
        assert_match(res.active_id, 1, 'bad active_id')
        assert_match(res.users, None, 'bad_users')
        assert_match(res.res_id, 1, 'bad_resid')
        assert_match(res.queue, None, 'bad queue')

    def test_reservation_creation_cyclic(self):
        '''reservation creation: cyclic'''
        self.base_res_spec['cycle'] = 120
        res = Reservation(self.base_res_spec)
        assert_match(res.cycle, 120, 'bad cycle')
        assert_match(res.cycle_id, 1, 'bad cycle_id')

    def test_reservation_cycle(self):
        '''reservation cycles when reservation runs out of time'''
        # Yes the start time doesn't get reset
        self.base_res_spec['cycle'] = 120
        self.base_res_spec['duration'] = 3
        self.base_res_spec['res_id'] = Cobalt.Components.bgsched.bgsched_id_gen.get()
        now = time.time()
        self.base_res_spec['start'] = now
        res = Reservation(self.base_res_spec)
        res.running = True #mark this as active
        res.stime = now
        time.sleep(4) #wait for reservation to complete and cycle
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        assert_match(res.is_active(), False, 'res should be no longer active and shutting down')
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        # idempotency check
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        assert_match(res.is_active(), False, 'res should be no longer active')
        assert_match(res.running, False, 'should not be running')
        assert_match(res.res_id, 2, 'bad res_id')
        assert_match(res.cycle_id, 1, 'bad_cycle_id')
        assert_match(res.active_id, 1, 'bad_active_id')
        assert_match(res.start, now + 120, 'bad start') # active periods handled as a modulo of the cycle time.

    def test_reservation_cycle_while_active(self):
        '''reservation cycle time handled properly during deferral'''
        # deferrals reset the start time
        self.base_res_spec['cycle'] = 120
        self.base_res_spec['duration'] = 60
        self.base_res_spec['res_id'] = Cobalt.Components.bgsched.bgsched_id_gen.get()
        now = time.time()
        self.base_res_spec['start'] = now
        res = Reservation(self.base_res_spec)
        res.running = True #mark this as active
        res.stime = now
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        assert_match(res.is_active(), True, 'res should be active')
        res.start = now + 120 # Deferrals reset the start time as a part of the defer command
        # Setres -m -n <resname> -D deferral works by resetting the start time to the next cycle start.
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        assert_match(res.is_active(), False, 'res should be deferred')
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        # idempotency check
        assert_match(res.is_over(), False, 'cyclic reservations are never over')
        assert_match(res.is_active(), False, 'res should be no longer active')
        res.is_over()
        assert_match(res.running, False, 'should not be running')
        assert_match(res.res_id, 2, 'bad res_id')
        assert_match(res.cycle_id, 1, 'bad_cycle_id')
        assert_match(res.active_id, 1, 'bad_active_id')
        assert_match(res.start, now + 120, 'bad start')

