import time

from Cobalt.Components.cqm import QueueManager

from test_base import TestComponent

__all__ = ["TestQueueManager"]

class TestQueueManager (TestComponent):
    
    def setup(self):
        TestComponent.setup(self)
        self.cqm = QueueManager()
    
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
    
    def test_del_job(self):
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
