import os

from Cobalt.Components.system import Simulator

from test_base import TestComponent

__all__ = [
    "TestSimulator",
]

class TestSimulator (TestComponent):
    
    def setup (self):
        TestComponent.setup(self)
        self.system = Simulator(config_file="simulator.xml")
    
    def test_init_configure (self):
        config_file = "simulator.xml"
        assert os.path.exists(config_file)
        system = Simulator()
        assert not system.partitions
        system = Simulator(config_file=config_file)
        assert system.partitions
    
    def test_configure (self):
        config_file = "simulator.xml"
        assert os.path.exists(config_file)
        system = Simulator()
        assert not system.partitions
        system.configure(config_file)
        assert system.partitions
    
    def test_reserve_partition (self):
        idle_partitions = self.system.partitions.q_get([{'state':"idle"}])
        partition = idle_partitions[0]
        reserved = self.system.reserve_partition(partition.name)
        assert reserved
        print partition.state
        assert partition.state == "busy"
        for parent in partition.parents:
            assert parent.state == "blocked"
        for child in partition.children:
            assert child.state == "blocked"
    
    def test_release_partition (self):
        idle_partitions_before = self.system.partitions.q_get([{'state':"idle"}])
        partition = idle_partitions_before[0]
        self.system.reserve_partition(partition.name)
        self.system.release_partition(partition.name)
        idle_partitions_after = self.system.partitions.q_get([{'state':"idle"}])
        assert idle_partitions_before == idle_partitions_after
    
    def test_add_jobs (self):
        self.system.add_jobs([dict(
            id = "1",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
    
    def test_get_jobs (self):
        specs = self.system.get_jobs([{'id':"*"}])
        assert not specs
        self.system.add_jobs([dict(
            id = "1",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        specs = self.system.get_jobs([{'id':"*"}])
        assert specs
    
    def test_del_jobs (self):
        self.system.add_jobs([dict(
            id = "1",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        jobs = self.system.get_jobs([{'id':"*"}])
        assert jobs
        specs = [job.to_rx(["id"]) for job in jobs]
        self.system.del_jobs(specs)
        jobs = self.system.get_jobs([{'id':"*"}])
        assert not jobs
    
    def test_run_jobs (self):
        self.system.add_jobs([dict(
            id = "1",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        runtime = self.system.jobs.values()[0].runtime
        for each in range(runtime):
            self.system.run_jobs()
    
    def test_signal_jobs (self):
        self.system.add_jobs([dict(
            id = "1",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        
        jobs = self.system.signal_jobs([{'id':"*"}], "SIGINT")
        assert jobs
        assert self.system.jobs
        jobs = self.system.signal_jobs([{'id':"*"}], "SIGKILL")
        assert jobs
        assert not self.system.jobs
