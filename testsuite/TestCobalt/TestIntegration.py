import os
import sys
import xmlrpclib
import time
import traceback
import logging

import TestCobalt
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.cqm import QueueManager
from Cobalt.Components.simulator import Simulator
from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Proxy import ComponentProxy
import Cobalt.Proxy
from Cobalt.Exceptions import ComponentLookupError
from Utilities.ThreadSupport import *

class TestIntegration (object):
    def setup (self):
        self.slp = TimingServiceLocator()
        self.system = Simulator(config_file="simulator.xml")
        self.system_thr = ComponentProgressThread(self.system)
        self.system_thr.start()
        self.scriptm = ScriptManager()
        self.scriptm_thr = ComponentProgressThread(self.scriptm)
        self.scriptm_thr.start()
        self.qm = QueueManager()
        self.qm_thr = ComponentProgressThread(self.qm)
        self.qm_thr.start()
        
    def teardown (self):
        self.qm_thr.stop()
        self.scriptm_thr.stop()
        self.system_thr.stop()
        Cobalt.Proxy.local_components.clear()

    def test_something(self):
        logging.basicConfig()
        
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
            
        # get the list of available partitions and add them to the pool of managed partitions
        try:
            simulator = ComponentProxy("system")
        except ComponentLookupError:
            assert not "failed to connect to simulator"
    
        for part_name in self.system._partitions:
            partitions = simulator.add_partitions([{'tag':"partition", 'name':part_name, 'queue':"default"}])
            assert len(partitions) == 1
            partitions = simulator.set_partitions([{'tag':"partition", 'name':part_name}], {'functional':True, 'scheduled':True})
            assert len(partitions) == 1
    
        partitions = simulator.get_partitions([{'name':"*", 'size':"*", 'queue':"*"}])
        assert len(partitions) > 0
    
        # now run a real job
        #
        # 1. add the job to the default queue
        # 2. obtain a partition for it to run on
        # 3. start running it on that paritition
        # 4. check that it started running
        # 5. sleep for a bit, and then check that it's still running
        # 6. sleep some more and then check to see if it actually finished running
    
        nodes = partitions[0]['size']
        jobs = cqm.add_jobs([{'queue':"default", 'mode':"co", 'command':"/bin/ls", 'outputdir':os.getcwd(), 'walltime':4,
            'nodes':nodes, 'procs':nodes, 'args':[], 'user':"nobody", 'jobid':"*"}])
        assert len(jobs) == 1
    
        job = jobs[0]
        jobid = job['jobid']
        job_location_args = [{'jobid':jobid, 'nodes':job['nodes'], 'queue':job['queue'], 'utility_score':1, 'threshold': 1,
            'walltime':job['walltime'], 'attrs': {}}]
        locations = simulator.find_job_location(job_location_args, [])
        assert locations.has_key(jobid)
    
        location = locations[jobid]
        cqm.run_jobs([{'jobid':jobid}], location)
    
        r = cqm.get_jobs([{'jobid':jobid, 'state':"*", 'is_active':True}])
        if not r:
            assert not "the job didn't start"
    
        time.sleep(20)
        
        r = cqm.get_jobs([{'jobid':jobid, 'state':"*", 'is_active':True}])
        if len(r) != 1:
            assert not "the job has stopped running prematurely"
    
        start_time = time.time()
        while True:
            r = cqm.get_jobs([{'jobid':jobid, 'state':"*", 'is_active':True}])
            if r:
                if time.time() - start_time > 240:
                    assert not "the job seems to have run overtime"
                else:
                    time.sleep(5)
            else:
                break

        # this time, we'll add a job to the queue, start the job, sleep for a bit
        # and then try to kill the job before it has finished
        nodes = partitions[0]['size']
        jobs = cqm.add_jobs([{'queue':"default", 'mode':"co", 'command':"/bin/ls", 'outputdir':os.getcwd(), 'walltime':4,
            'nodes':nodes, 'procs':nodes, 'args':[], 'user':"nobody", 'jobid':"*"}])
        assert len(jobs) == 1

        job = jobs[0]
        jobid = job['jobid']
        job_location_args = [{'jobid':jobid, 'nodes': job['nodes'], 'queue': job['queue'], 'utility_score': 1, 'threshold': 1,
            'walltime': job['walltime'], 'attrs': {}}]
        locations = simulator.find_job_location(job_location_args, [])
        assert locations.has_key(jobid)

        location = locations[jobid]
        cqm.run_jobs([{'jobid':jobid}], location)

        r = cqm.get_jobs([{'jobid':jobid, 'state':"*", 'is_active':True}])
        if not r:
            assert not "the job didn't start"
        
        time.sleep(20)
        
        r = cqm.get_jobs([{'jobid':jobid, 'is_active':True}])
        if len(r) != 1:
            assert not "the job has stopped running prematurely"
                                        
        cqm.del_jobs([{'jobid':jobid}])
        
        start_time = time.time()
        while True:
            r = cqm.get_jobs([{'jobid':jobid, 'is_active':True, 'state':"*"}])
            if r:
                if time.time() - start_time > 30:
                    assert not "the job didn't die when asked to"
                else:
                    time.sleep(1)
            else:
                break
