from Cobalt.Data import DataCreationError

from Cobalt.Components.system import Simulator
from Cobalt.Components.bgsched import Reservation

def setup (self):
    Simulator()

class TestReservation (object):
    
    def test_required_name (self):
        spec = {'start':0, 'duration':0}
        try:
            reservation = Reservation(spec)
        except DataCreationError:
            pass
        else:
            assert not "didn't require name"
        spec['name'] = "my_reservation"
        try:
            reservation = Reservation(spec)
        except DataCreationError:
            assert not "failed with name specified"
    
    def test_init (self):
        reservation = Reservation({'name':"mine", 'start':0, 'duration':0})
        assert reservation.tag == "reservation"
        assert reservation.name == "mine"
        assert reservation.start == 0
        assert reservation.duration == 0
        assert reservation.cycle is None
        assert reservation.users == []
        assert reservation.partitions == []
    
    def test_active (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50})
        for current_time in xrange(1, 100):
            assert not reservation.active(current_time)
        for current_time in xrange(100, 150):
            assert reservation.active(current_time)
        for current_time in xrange(150, 250):
            assert not reservation.active(current_time)
    
    def test_active_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50})
        assert not reservation.active(99)
        assert reservation.active(100)
        assert reservation.active(109)
        assert not reservation.active(110)
        assert not reservation.active(149)
        assert reservation.active(150)
        assert reservation.active(159)
        assert not reservation.active(160)
    
    def test_overlaps (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50})
        assert not reservation.overlaps(location=None, start=0, duration=99)
        assert reservation.overlaps(location=None, start=0, duration=100)
        assert reservation.overlaps(location=None, start=99, duration=1)
        assert reservation.overlaps(location=None, start=99, duration=50)
        assert reservation.overlaps(location=None, start=149, duration=1)
        assert not reservation.overlaps(location=None, start=150, duration=100)
    
    def test_overlaps_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50})
        assert not reservation.overlaps(location=None, start=0, duration=99)
        assert reservation.overlaps(location=None, start=0, duration=100)
        assert reservation.overlaps(location=None, start=99, duration=1)
        assert reservation.overlaps(location=None, start=99, duration=10)
        assert reservation.overlaps(location=None, start=101, duration=1)
        assert reservation.overlaps(location=None, start=109, duration=1)
        assert not reservation.overlaps(location=None, start=110, duration=39)
        assert reservation.overlaps(location=None, start=90, duration=100)
        
    def test_active_during (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50})
        assert not reservation.active_during(start=0, duration=100)
        assert reservation.active_during(start=0, duration=101)
        assert reservation.active_during(start=100, duration=1)
        assert reservation.active_during(start=100, duration=50)
        assert reservation.active_during(start=149, duration=1)
        assert not reservation.active_during(start=150, duration=100)
    
    def test_active_during_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50})
        assert not reservation.active_during(start=0, duration=100)
        assert reservation.active_during(start=0, duration=101)
        assert reservation.active_during(start=100, duration=1)
        assert reservation.active_during(start=100, duration=10)
        assert reservation.active_during(start=109, duration=1)
        assert not reservation.active_during(start=110, duration=40)
