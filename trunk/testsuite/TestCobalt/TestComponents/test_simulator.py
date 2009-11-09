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
        part_name = self.system._partitions.keys()[0]
        partitions = self.system.add_partitions([{'name':part_name}])
        assert len(partitions) == 1
        partitions = self.system.set_partitions([{'tag':"partition", 'name':part_name}], {'functional':True, 'scheduled':True})
        assert len(partitions) == 1
        idle_partitions = self.system.get_partitions([{'state':"idle"}])
        partition = idle_partitions[0]
        assert partition.name == part_name
        job_location_args = [{'jobid':3003, 'nodes': partition.size, 'queue': "default", 'utility_score': 1, 'threshold': 0,
            'walltime':1}]
        locations = self.system.find_job_location(job_location_args, [])
        assert locations.has_key(3003)
        reserved = self.system.reserve_partition(locations[3003][0])
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
            args = [],
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
            args = [],
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
            args = [], 
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
            args = [],
        )])
        
        for signal in ["SIGINT", "SIGKILL"]:
            process_groups = self.system.signal_process_groups([{'id':"*"}], signal)
            assert len(process_groups) == 1
            assert process_groups[0].signals[-1] == signal
