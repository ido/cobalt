import time
import xmlrpclib

from Cobalt.Components.cqm import QueueManager, QueueError
from Cobalt.Data import IncrID
import Cobalt.Components.cqm

from test_base import TestComponent

__all__ = ["TestQueueManager"]

class TestQueueManager (TestComponent):
    
    def setup(self):
        TestComponent.setup(self)
        self.cqm = QueueManager()

    def teardown(self):
        Cobalt.Components.cqm.cqm_id_gen = IncrID()
        
    def test_add_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        
        assert len(self.cqm.Queues) == 1
        assert 'default' in self.cqm.Queues
        assert self.cqm.Queues['default'].tag == 'queue'
        
    def test_get_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
         
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
         
        assert len(results) == 1
        assert results[0].name == 'default'
        
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        
        assert len(results) == 1
        assert results[0].name == 'default'

        results = self.cqm.get_queues([{'tag':"queue", 'name':"*"}])
         
        assert len(results) == 3
 
    def test_del_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'name':"empty"}])
     
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"wally"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"wally"}])

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 2
         
        try:
            self.cqm.del_queues([{'tag':"queue", 'name':"foo"}])
        except Exception:
            pass
        else:
            assert not "able to delete queue with jobs in it"

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"default"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"foo"}])
        assert len(results) == 2

        self.cqm.del_queues([{'tag':"queue", 'name':"foo"}], force=True)             

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"default"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'queue':"foo"}])
        assert len(results) == 0
        
        self.cqm.del_queues([{'name':"empty"}])
        r = self.cqm.get_queues([{'name':"empty"}])
        assert len(r) == 0
        
    
    def test_set_queues(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
         
        self.cqm.set_queues([{'tag':"queue", 'name':"default"}], {'state':"bar"})
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        assert results[0].state == 'bar'

        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])
        self.cqm.set_queues([{'tag':"queue", 'name':"*"}], {'state':"bar"})
        results = self.cqm.get_queues([{'tag':"queue", 'name':"*"}])
    
        assert results[0].state == results[1].state == results[2].state == 'bar'
         
    def test_add_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])

        try:
            self.cqm.add_jobs([{'queue':"not a valid name"}])
        except QueueError:
            pass
        else:
            assert not "trying to add a job to a non-existent queue should raise an Exception"
        
        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"default"}])
        assert len(results[0].jobs) == 1
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"foo"}])
        assert len(results[0].jobs) == 0
        
        results = self.cqm.get_queues([{'tag':"queue", 'name':"bar"}])
        assert len(results[0].jobs) == 0

    def test_get_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"bar"}])

        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        
        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*"}])
        assert len(results) == 1
        
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo"}])

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*", 'queue':"foo"}])
        assert len(results) == 1

        results = self.cqm.get_jobs([{'tag':"job", 'jobid':"*", 'queue':"bar"}])
        assert len(results) == 0
    
    def test_del_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
     
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"default", 'user':"wally"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"dilbert"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo", 'user':"wally"}])

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 2
         
        self.cqm.del_jobs([{'tag':"job", 'user':"wally"}])

        results = self.cqm.get_jobs([{'tag':"job", 'user':"dilbert"}])
        assert len(results) == 2

        results = self.cqm.get_jobs([{'tag':"job", 'user':"wally"}])
        assert len(results) == 0


    def test_set_jobs(self):
        self.cqm.add_queues([{'tag':"queue", 'name':"default"}])
        self.cqm.add_queues([{'tag':"queue", 'name':"foo"}])
    
        self.cqm.add_jobs([{'tag':"job", 'queue':"default"}])
        self.cqm.add_jobs([{'tag':"job", 'queue':"foo"}])
        
        self.cqm.set_jobs([{'tag':"job", 'queue':"*"}], {'jobname':"hello"})
        results = self.cqm.get_jobs([{'tag':"job", 'jobname':"hello"}])
        assert len(results) == 2
        
        self.cqm.set_jobs([{'tag':"job", 'queue':"foo"}], {'jobname':"goodbye"})
        results = self.cqm.get_jobs([{'tag':"job", 'jobname':"hello"}])
        assert len(results) == 1

    def test_set_jobid(self):
        # create a local QueueManager so that we can be sure no jobids have been used
        self.cqm.add_queues([{'name':"default"}])
        self.cqm.set_jobid(10)
        self.cqm.add_jobs([{'queue':"default"}])
        r = self.cqm.get_jobs([{'jobid':10}])
        assert len(r) == 1
    
    def test_move_jobs(self):
        self.cqm.add_queues([{'name':"default"}])
        self.cqm.add_queues([{'name':"foo"}])
        self.cqm.add_queues([{'name':"restricted"}])
        self.cqm.set_queues([{'name':"restricted"}], {'users':"alice"})
        
        self.cqm.add_jobs([{'queue':"default", 'jobname':"hello"}])
        
        try:
            self.cqm.move_jobs([{'jobname':"hello"}], "default")
        except QueueError:
            pass
        else:
            assert not "moving a job to the same queue should cause an exception"
            
        try:
            self.cqm.move_jobs([{'jobname':"hello"}], "jonx")
        except QueueError:
            pass
        else:
            assert not "moving a job to a non-existent queue should cause an exception"
                                 

        self.cqm.move_jobs([{'jobname':"hello"}], "foo")
        r = self.cqm.get_jobs([{'jobname':"hello", 'queue':"*"}])
        assert len(r) == 1
        assert r[0].queue == "foo"
        
        try:
            self.cqm.move_jobs([{'jobname':"hello"}], "restricted")
        except QueueError:
            pass
        else:
            assert not "a job failing can_queue should prevent the move_jobs from succeeding"
            
