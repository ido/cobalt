import logging
import os
import sys
import xmlrpclib
import time
import traceback
import logging

from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.simulator import Simulator
from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Proxy import ComponentProxy, ComponentLookupError
import Cobalt.Proxy

class TestIntegration (object):
    def setup (self):
        self.slp = TimingServiceLocator()
        self.qm = QueueManager()
        self.sys = Simulator(config_file="simulator.xml")
        self.sm = ScriptManager()
        
    def teardown (self):
        Cobalt.Proxy.local_components.clear()

    def test_something(self):
        logging.basicConfig()
        def my_do_tasks():
            self.sys.do_tasks()
            self.qm.do_tasks()
        
        try:
            cqm = ComponentProxy("queue-manager")
        except ComponentLookupError:
            assert not "failed to connect to queue manager"
        
        # add a queue    
        queues = cqm.add_queues([{'tag':"queue", 'name':"default"}])
        assert len(queues) == 1
        
        # try adding a job to a queue that doesn't exist
        try:
            jobs = cqm.add_jobs([{'tag':"job", 'queue':"jonx"}])
        except xmlrpclib.Fault:
            # trying to add a job to a queue that doesn't exist results in an xmlrpc Fault
            pass
        else:
            assert not "Adding job to non-existent queue should raise xmlrpclib.Fault"
            
        # add a partition to manage
        try:
            simulator = ComponentProxy("system")
        except ComponentLookupError:
            assert not "failed to connect to simulator"

        simulator.add_partitions([{'name':"ANLR00"}])

            
        # now add a real job
        # we will
        # 1. start it
        # 2. check that it started
        # 3. sleep for a bit, and then check that it's still running
        # 4. sleep some more and then check to see if it actually finished running
        jobs = cqm.add_jobs([{'queue':"default", 'mode':"co", 'command':"/bin/ls", 
                              'outputdir':os.getcwd(), 'walltime':1, 'procs':600,
                              'args':[], 'user':"nobody" }])
        assert len(jobs) == 1
                             
        cqm.run_jobs([{'jobid':1}], ["ANLR00"])

        # this will start to fail if the number of job steps ever changes
        self.qm.do_tasks()
        self.qm.do_tasks()
        self.qm.do_tasks()
        r = cqm.get_jobs([{'jobid':'*', 'state':'running'}])
        if not r:
            assert not "the job didn't start"
    
        time.sleep(20)
        
        my_do_tasks()
    
        r = cqm.get_jobs([{'jobid':'*', 'state':'running'}])
        if len(r) != 1:
            assert not "the job has stopped running prematurely"

        time.sleep(180)

        # finish stepping through the ... uh ... steps, to the point where the job
        # finishes and is removed from the queue.
        # NB: as noted above
        # this will start to fail if the number of job steps ever changes
        for i in range(4):
            my_do_tasks()
        
        r = cqm.get_jobs([{'jobid':'*', 'state':'*'}])
        if r:
            assert not "the job seems to have run overtime"


        # this time, we'll add a job to the queue, start the job, sleep for a bit
        # and then try to kill the job before it has finished
        jobs = cqm.add_jobs([{'queue':"default", 'mode':"co", 'command':"/bin/ls", 
                              'outputdir':os.getcwd(), 'walltime':10, 'procs':600,
                              'args':[], 'user':"nobody" }])
        assert len(jobs) == 1
                             
        cqm.run_jobs([{'jobid':2}], ["ANLR00"])

        self.qm.do_tasks()
        self.qm.do_tasks()
        self.qm.do_tasks()
        r = cqm.get_jobs([{'jobid':'*', 'state':'running'}])
        if not r:
            assert not "the job didn't start"
        
        time.sleep(20)
        
        my_do_tasks()
    
        r = cqm.get_jobs([{'jobid':'*', 'state':'running'}])
        if len(r) != 1:
            assert not "the job has stopped running prematurely"

        cqm.del_jobs([{'jobid':2}])
        
        # give the thread in the simulator a chance to die
        time.sleep(2)
        
        for i in range(4):
            my_do_tasks()
        
        r = cqm.get_jobs([{'jobid':'*', 'state':'*'}])
        if r:
            assert not "the job didn't die when asked to"
