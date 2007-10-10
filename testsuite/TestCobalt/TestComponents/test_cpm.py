import os

from Cobalt.Components.cpm import ProcessManager
from Cobalt.Components.system import Simulator
import Cobalt.Proxy

from test_base import TestComponent

__all__ = [
    "TestProcessManager",
]


class TestProcessManager (TestComponent):
    
    def setup (self):
        TestComponent.setup(self)
        self.cpm = ProcessManager()
        self.system = Simulator(config_file="simulator.xml")
    
    def test_add_jobs (self):
        assert not self.cpm.jobs
        partition = self.system.partitions.values()[0]
        spec = dict(
            cwd = "~",
            executable = "/bin/ls",
            user = os.getlogin(),
            id = 1,
            size = partition.size,
            location = partition.name,
        )
        jobs = self.cpm.add_jobs([spec])
        assert len(jobs) == len(self.cpm.jobs) == 1
        job = jobs[0]
        assert job is self.cpm.jobs[job.id]
        assert job.cwd == "~"
        assert job.executable == "/bin/ls"
        assert job.user == os.getlogin()
        assert job.id == 1
        assert job.size == partition.size
        assert job.location == partition.name
    
    def test_get_jobs (self):
        jobs = self.cpm.get_jobs([{'jobid':"*"}])
        assert not jobs
        partition = self.system.partitions.values()[0]
        spec = dict(
            cwd = "~",
            executable = "/bin/ls",
            user = os.getlogin(),
            id = 1,
            size = partition.size,
            location = partition.name,
        )
        self.cpm.add_jobs([spec])
        jobs = self.cpm.get_jobs([{'jobid':"*"}])
        assert len(jobs) == 1
        job = jobs[0]
        assert job is self.cpm.jobs[job.id]
        assert job.cwd == "~"
        assert job.executable == "/bin/ls"
        assert job.user == os.getlogin()
        assert job.id == 1
        assert job.size == partition.size
        assert job.location == partition.name
    
    def test_check_jobs (self):
        partition = self.system.partitions.values()[0]
        spec = dict(
            cwd = "~",
            executable = "/bin/ls",
            user = os.getlogin(),
            id = 1,
            size = partition.size,
            location = partition.name,
        )
        jobs = self.cpm.add_jobs([spec])
        job = jobs[0]
        for each in range(self.system.jobs[1].runtime):
            self.cpm.check_jobs()
            assert job.state != "finished"
            self.system.do_tasks()
        self.cpm.check_jobs()
        assert job.state == "finished"
    
    def test_wait_jobs (self):
        partition = self.system.partitions.values()[0]
        spec = dict(
            cwd = "~",
            executable = "/bin/ls",
            user = os.getlogin(),
            id = 1,
            size = partition.size,
            location = partition.name,
        )
        jobs = self.cpm.add_jobs([spec])
        job = jobs[0]
        for each in range(self.system.jobs[1].runtime):
            jobs = self.cpm.wait_jobs([{'id':"*"}])
            assert not jobs
            self.system.do_tasks()
            self.cpm.check_jobs()
        jobs = self.cpm.wait_jobs([{'id':"*"}])
        assert jobs
        for job in jobs:
            assert job.state == "finished"
        assert not self.cpm.jobs
    
    def test_signal_jobs (self):
        partition = self.system.partitions.values()[0]
        spec = dict(
            cwd = "~",
            executable = "/bin/ls",
            user = os.getlogin(),
            id = 1,
            size = partition.size,
            location = partition.name,
        )
        jobs = self.cpm.add_jobs([spec])
        job = jobs[0]
        jobs = self.cpm.signal_jobs([{'id':"*"}])
        assert jobs
