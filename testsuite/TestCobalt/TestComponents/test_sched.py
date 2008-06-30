import time

from Cobalt.Exceptions import DataCreationError

from Cobalt.Components.simulator import Simulator
from Cobalt.Components.bgsched import Reservation, Partition, PartitionDict, BGSched, Queue, QueueDict, ReservationDict

import Cobalt.Proxy
from Cobalt.Components.cqm import QueueManager
from Cobalt.Exceptions import ComponentLookupError, ReservationError
from Cobalt.Components import bgsched          #**** FIX ME *****

from Cobalt.Data import DataDict

class Job (object):
    def __init__(self, walltime, queue):
        # remember that walltime is in minutes
        self.walltime = walltime
        self.queue = queue
        

class TestReservation (object):

    def setup (self):
        self.system = Simulator(config_file="simulator.xml")
        self.system.add_partitions([{'name':"ANL-R00-1024"}])
        self.test_partition = self.system.partitions.values()[0]

    def teardown(self):
        Cobalt.Proxy.local_components.clear()      

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
        assert reservation.users == ""
        assert reservation.partitions == ""

    def test_update (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10})
       
        try: 
            reservation.update({'users':"newuser"})                   
        except ComponentLookupError:
            cqm = QueueManager()      
            reservation.update({'users':"newuser"})

        assert reservation.users == "newuser"
        
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'users':"group"})
        reservation.update({'users':"newuser"})
        assert not reservation.users == "group"
        assert reservation.users == "newuser"


    def test_active (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50})
        for current_time in xrange(1, 100):
            assert not reservation.is_active(current_time)
        for current_time in xrange(100, 150):
            assert reservation.is_active(current_time)
        for current_time in xrange(151, 250):
            assert not reservation.is_active(current_time)

    def test_active_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50})
        assert not reservation.is_active(99)
        assert reservation.is_active(100)
        assert reservation.is_active(109)
        assert not reservation.is_active(111)
        assert not reservation.is_active(149)
        assert reservation.is_active(150)
        assert reservation.is_active(159)
        assert not reservation.is_active(161)
    
    def test_overlaps (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50, 'partitions':"ANL-R00-1024"})
        assert not reservation.overlaps(partition=self.test_partition, start=0, duration=99)
        assert reservation.overlaps(partition=self.test_partition, start=0, duration=100)
        assert reservation.overlaps(partition=self.test_partition, start=0, duration=151)
        assert reservation.overlaps(partition=self.test_partition, start=99, duration=1)   
        assert reservation.overlaps(partition=self.test_partition, start=99, duration=50)
        assert reservation.overlaps(partition=self.test_partition, start=149, duration=1)
        assert not reservation.overlaps(partition=self.test_partition, start=150, duration=100)
 
        #check different partition than constructed
        reservation = Reservation({'name':"mine", 'start':100, 'duration':50, 'partitions':"anotherpartion"})
        assert not reservation.overlaps(partition=self.test_partition, start=0, duration=100)
       
    def test_overlaps_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50, 'partitions':"ANL-R00-1024"})
        assert not reservation.overlaps(partition=self.test_partition, start=0, duration=99)
        assert reservation.overlaps(partition=self.test_partition, start=0, duration=100)
        assert reservation.overlaps(partition=self.test_partition, start=99, duration=1)
        assert reservation.overlaps(partition=self.test_partition, start=99, duration=10)
        assert reservation.overlaps(partition=self.test_partition, start=101, duration=1)
        assert reservation.overlaps(partition=self.test_partition, start=109, duration=1)
        assert not reservation.overlaps(partition=self.test_partition, start=110, duration=39)
        assert reservation.overlaps(partition=self.test_partition, start=90, duration=100)
        

    def test_job_within_reservation (self):
        # past reservation
        reservation = Reservation({'name':"mine", 'start':100, 'duration':3600, 'partitions':"ANLR00", 'queue':"default"})
        j = Job(5, "default")
        assert not reservation.job_within_reservation(j)
        j = Job(70, "default")
        assert not reservation.job_within_reservation(j)
        
        # current reservation
        reservation = Reservation({'name':"mine", 'start':time.time(), 'duration':3600, 'partitions':"ANLR00", 'queue':"default"})
        j = Job(5, "default")
        assert reservation.job_within_reservation(j)
        j = Job(70, "default")
        assert not reservation.job_within_reservation(j)
        
        # future reservation
        reservation = Reservation({'name':"mine", 'start':time.time() + 3600, 'duration':3600, 'partitions':"ANLR00", 'queue':"default"})
        j = Job(5, "default")
        assert not reservation.job_within_reservation(j)
        j = Job(40, "default")
        assert not reservation.job_within_reservation(j)
        j = Job(70, "default")
        assert not reservation.job_within_reservation(j)

    def test_job_within_reservation_cyclic (self):
        reservation = Reservation({'name':"mine", 'start':time.time()-3000, 'duration':3600, 'cycle':4000, 'partitions':"ANLR00", 'queue':"default"})
        # jobs ends inside the reservation
        j = Job(6, "default")
        assert reservation.job_within_reservation(j)
        # job ends in the "dead zone"
        j = Job(12, "default")
        assert not reservation.job_within_reservation(j)
        # job ends the next time the reservation is active
        j = Job(50, "default")
        assert not reservation.job_within_reservation(j)
        # job lasts longer than the reservation
        j = Job(100, "default")
        assert not reservation.job_within_reservation(j)
        # queue doesn't exist
        j = Job(0,"notaqueue")
        assert not reservation.job_within_reservation(j)

    def test_is_over(self):
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':50})
        assert not reservation.is_over()
        reservation = Reservation({'name':"mine", 'start':100, 'duration':10})
        assert reservation.is_over()
        reservation = Reservation({'name':"mine", 'start':time.time(), 'duration':1000})
        assert not reservation.is_over()

    def test_q_add (self):     #|finish| assert logger
        reservationdict = ReservationDict()  
        reservationdict['res1'] = Reservation({'name':"mine1", 'start':100, 'duration':10})
        reservationdict['res2'] = Reservation({'name':"mine2", 'start':200, 'duration':10})
        resqueue = {'queue':"newqueue", 'name':"newres", 'start':10, 'duration':20}

        try:
            reslist = reservationdict.q_add([resqueue])
        except ComponentLookupError:
            cqm = QueueManager() 

        #new reservation created
        reslist = reservationdict.q_add([resqueue])        

        assert reservationdict['newres'].queue == "newqueue"
        assert reservationdict['newres'].name == "newres"
        assert len(reslist) == 1
        assert reslist[0].name == "newres"
        assert reslist[0].queue == "newqueue"
        assert reslist[0].createdQueue

        #reservation already exists
        try:
            new = reservationdict.q_add([resqueue])
        except ReservationError:
            pass

        #change queue for existing reservations
        res1 = {'queue':"newqueue1", 'name':"mine1", 'start':10, 'duration':20}
        res2 = {'queue':"newqueue2", 'name':"mine2", 'start':10, 'duration':20}
        reslist = reservationdict.q_add([res1,res2])
        assert reservationdict['mine1'].queue == "newqueue1"
        assert reservationdict['mine2'].queue == "newqueue2"

        #queue already exists
        cqm.add_queues([{'tag':"queue", 'name':"default"}])     
        resqueue = {'queue':"default", 'name':"other", 'start':10, 'duration':20}
        reslist = reservationdict.q_add([resqueue])

    def test_q_del (self): #|alert| there is not ComponenentLookup exception for the queuemanger
        cqm = QueueManager()
        reservationdict = ReservationDict()
        reservationdict['res1'] = Reservation({'queue':"myqueue", 'name':"mine1", 'start':100, 'duration':10})
        reservationdict['res2'] = Reservation({'name':"mine2", 'start':200, 'duration':10})
        resqueue = {'queue':"myqueue", 'name':"mine1", 'start':10, 'duration':20}
        
        reslist = reservationdict.q_del([resqueue])
        


class TestPartition(object):

    def setup (self):
        pass
    
    def teardown(self):
        Cobalt.Proxy.local_components.clear()   

    def test_init (self):
        partition = Partition({'queue':"default", 'name':"mine", 'nodecards':4, 'functional':True, 'state':"idle"})
        assert partition.queue == "default"
        assert partition.name == "mine"
        assert partition.nodecards == 4
        assert partition.scheduled == None
        assert partition.functional == True
        assert partition.size == None
        assert partition.parents == None
        assert partition.children == None
        assert partition.state == "idle"

    def test_can_run(self):
        j = Job(10, "default")

        partition = Partition({'scheduled':True, 'functional':True})
        assert partition._can_run(j)
        partition = Partition({'scheduled':True, 'functional':False})
        assert not partition._can_run(j)
        partition = Partition({'scheduled':False, 'functional':False})
        assert not partition._can_run(j)

    def test_part_can_run(self):
        j = bgsched.Job({'nodes':20})

        target_part = Partition({'name':"mine", 'functional':False, 'state':"idle", 'size':100})
        part = Partition({'children':"mine", 'functional':False, 'state':"idle"})
        partitiondict = PartitionDict({'part1':part, 'part2':part})
        assert not partitiondict.can_run(target_part, j)
        
        target_part = Partition({'name':"mine", 'functional':True, 'scheduled':True,
                                 'state':"idle", 'size':100 })
        part = Partition({'children':"mine", 'functional':True, 'scheduled':True, 'size':100})
        partitiondict = PartitionDict({'part1':part, 'part2':part})
        assert partitiondict.can_run(target_part, j)

        #target partition is not idle 
        target_part = Partition({'state':"running"})
        assert not partitiondict.can_run(target_part, j)

class TestJob (object):
    def test_init(self):
        job = bgsched.Job({'nodes':20, 'state':"idle", 'jobid':1234, 'walltime':10 })
        
        assert job.partition == "none"
        assert job.nodes == 20
        assert job.state == "idle"
        assert job.jobid == 1234
        assert job.walltime == 10
        assert job.queue == None
        assert job.user == None


class TestQueue (object):
    def test_init(self):
        queue = Queue({'name':"myqueue", 'state':"idle", 'policy':"smallest-first"})
        assert queue.name == "myqueue"
        assert queue.state == "idle"
        assert queue.policy == "smallest-first"
        assert queue.priority == 0

    def test_load_policy(self):  #|finish| assert test logger?
        queue = Queue({'name':"myqueue", 'policy':"smallest-first"})
        queue.LoadPolicy()

        queue = Queue({'name':"myqueue", 'policy':"default"})
        queue.LoadPolicy()

class TestBGSched(object):

    def setup(self):
        pass
    
    def teardown(self):
        Cobalt.Proxy.local_components.clear()       

    def test_get_state(self):
        sched = BGSched()
        assert sched.__getstate__()['reservations'] == sched.reservations
        assert sched.__getstate__()['version'] == 1
        assert sched.__getstate__()['active'] == sched.active
    
    def test_setstate_(self):
        sched = BGSched()
        assert sched.active

        res = Reservation({'name':"mine", 'start':0, 'duration':0})
        sched.__setstate__({'reservations':res, 'active':False})
        assert not sched.active 

        sched.__setstate__({'reservations':res})
        assert sched.active

    #******test my  initialization sometime******

    def test_get_sched_info(self):
        sched = BGSched()
        assert sched.get_sched_info() == {}
        sched.sched_info = {'im':"a", 'broken':"bgsched"}
        assert sched.get_sched_info() == {'im':"a", 'broken':"bgsched"}
        
    def test_enable_and_disable(self):
        sched = BGSched()
        assert sched.active
        sched.disable()
        assert not sched.active
        sched.enable()
        assert sched.active
       
    def test_prioritycmp(self):
        sched = BGSched()
        q1 = Queue({'priority':2})      

        #prioriy is the same for both queues
        sched.queues['queue1'] = q1
        sched.queues['queue2'] = q1
        j1 = bgsched.Job({'queue':"queue1"})      
        j2 = bgsched.Job({'queue':"queue2"})
        
        assert sched.prioritycmp(j1, j2) == 0
    
        q1 = Queue({'priority':2}) 
        q2 = Queue({'priority':3})
        sched.queues['queue1'] = q1
        sched.queues['queue2'] = q2

        assert sched.prioritycmp(j1, j2) > 0

    def test_fifocmp(self):
        sched = BGSched()
        
        #job1.queue == job2.queue:  

        #test job1.nodes > job2 .nodes
        q1 = Queue({'policy':"largest-first"})
        sched.queues['queue1'] = q1
        j1 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':8, 'walltime':8})
        j2 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':4, 'walltime':4})
        assert sched.fifocmp(j1, j2) < 0

        #test job1.nodes < job2.nodes
        q1 = Queue({'policy':"smallest-first"})
        sched.queues['queue1'] = q1
        j1 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':1, 'walltime':8})
        
        assert sched.fifocmp(j1, j2) < 0
        
        #test job1.walltime > job2.walltime
        q1 = Queue({'policy':"longest-first"})        
        sched.queues['queue1'] = q1        
        assert sched.fifocmp(j1, j2) < 0

        #test job1.walltime < job2.walltime
        q1 = Queue({'policy':"shortest-first"})
        sched.queues['queue1'] = q1
        j1 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':1, 'walltime':1})   
        assert sched.fifocmp(j1, j2) < 0

        #test nested else
        j1 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':4, 'walltime':4})    
        assert sched.fifocmp(j1, j2) == 0  #return index comparison test

        #job1.queue != job2.queue
        j1 = bgsched.Job({'queue':"queue1", 'jobid':1234, 'index':2, 'nodes':8, 'walltime':8})
        j2 = bgsched.Job({'queue':"diff", 'jobid':1234, 'index':2, 'nodes':4, 'walltime':4})
                
        assert sched.fifocmp(j1, j2) == 0  #return index comparison test
        
        #note: last line of code in fifocmp() is useless.


    def test_save_me(self):
        pass

#    def test_add_reservations(self):
#        sched = BGSched()
#        cqm = QueueManager()

        #sched.add_reservations({'name':"mine", 'start':100, 'duration':10})

    def test_set_reservations(self):
        pass


    def test_check_reservations(self): #|finish|
        sched = BGSched()

        #if 'cycle' is not None
        r1 = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':"50", 'partitions':"ANL-R00-1024"})
        sched.reservations['res1'] = r1
        r2 = Reservation({'name':"mine", 'start':100, 'duration':20, 'cycle':"50", 'partitions':"ANL-R01-1024"})
        sched.reservations['res2'] = r2

        p1 = Partition({'children':"blah", 'parents':"some", 'name':"mine"})
        sched.partitions['ANL-R00-1024'] = p1
        p2 = Partition({'children':"ANL-R01-1024", 'parents':"other", 'name':"mine"})
        sched.partitions['ANL-R01-1024'] = p2

        sched.check_reservations()
        
        #if 'cycle' is None
        r1 = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':None, 'partitions':"ANL-R00-1024"})
        sched.reservations['res1'] = r1
        r2 = Reservation({'name':"mine", 'start':100, 'duration':10, 'cycle':None, 'partitions':"ANL-R01-1024"})
        sched.reservations['res2'] = r2

        sched.check_reservations()


    def test_sync_data(self): #|finish|
        sched = BGSched()
        sched.sync_data()

    def test_start_job(self):
        sched = BGSched()
        part = Partition({'name':"mine"})
        j = bgsched.Job({'jobid':1234})    

        try:
            sched._start_job(j, part)
        except ComponentLookupError:
            pass
             
        cqm = QueueManager()  
        sched._start_job(j, part)
        assert sched.assigned_partitions[part.name] < time.time()
        assert sched.started_jobs[j.jobid] < time.time()





