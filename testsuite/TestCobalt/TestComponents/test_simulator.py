import os
import time

from Cobalt.Components.simulator import Simulator

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
        assert system._partitions
    
    def test_configure (self):
        config_file = "simulator.xml"
        assert os.path.exists(config_file)
        system = Simulator()
        assert not system._partitions
        system.configure(config_file)
        assert system._partitions
    
    def test_reserve_partition (self):
        self.system.add_partitions([{'name':self.system._partitions.keys()[0]}])
        idle_partitions = self.system.get_partitions([{'state':"idle"}])
        partition = idle_partitions[0]
        reserved = self.system.reserve_partition(partition.name)
        assert reserved
        assert partition.state == "busy"
        for parent in self.system._partitions.q_get([{'name':parent} for parent in partition.parents]):
            assert parent.state == "blocked"
        for child in self.system._partitions.q_get([{'name':child} for child in partition.children]):
            assert child.state == "blocked"
    
    def test_release_partition (self):
        self.system.add_partitions([{'name':self.system._partitions.keys()[0]}])
        idle_partitions_before = self.system.get_partitions([{'state':"idle"}])
        partition = idle_partitions_before[0]
        self.system.reserve_partition(partition.name)
        self.system.release_partition(partition.name)
        idle_partitions_after = self.system.get_partitions([{'state':"idle"}])
        assert idle_partitions_before == idle_partitions_after
    
    def test_add_process_groups (self):
        self.system.add_process_groups([dict(
            id = "*",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
    
    def test_get_process_groups (self):
        specs = self.system.get_process_groups([{'id':"*"}])
        assert not specs
        self.system.add_process_groups([dict(
            id = "*",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        specs = self.system.get_process_groups([{'id':"*"}])
        assert specs
    
    def test_run_process_groups (self):
        self.system.add_process_groups([dict(
            id = "*",
            size = "32",
            executable = "/bin/ls",
            location = ["ANLR00"],
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
    
    def test_signal_process_groups (self):
        self.system.add_process_groups([dict(
            id = "*",
            size = "32",
            executable = "/bin/ls",
            location = "ANLR00",
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
        )])
        
        for signal in ["SIGINT", "SIGKILL"]:
            process_groups = self.system.signal_process_groups([{'id':"*"}], signal)
            assert len(process_groups) == 1
            assert process_groups[0].signals[-1] == signal
