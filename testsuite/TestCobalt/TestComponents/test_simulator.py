import os
import time
import logging

CONFIG_FILE = "simulator.xml"

logging.basicConfig()

from Cobalt.Components.simulator import Simulator

from test_base import TestComponent
from TestCobalt.Utilities.Time import timeout

__all__ = [
    "TestSimulator",
]

class TestSimulator (TestComponent):
    
    def setup (self):
        TestComponent.setup(self)

        assert os.path.exists(CONFIG_FILE)
        self.system = Simulator(config_file=CONFIG_FILE)
        assert self.system._partitions
        assert len(self.system._partitions) > 0

        part_names = self.system._partitions.keys()
        for part_name in part_names:
            partitions = self.system.add_partitions([{'name':part_name}])
            assert len(partitions) == 1
            partitions = self.system.set_partitions([{'tag':"partition", 'name':part_name}], {'functional':True, 'scheduled':True})
            assert len(partitions) == 1
            idle_partitions = self.system.get_partitions([{'state':"idle"}])
            assert part_name in [p.name for p in idle_partitions]

        partition_sizes = [p.size for p in self.system._partitions.itervalues()]
        partition_sizes.sort()
        self.min_size = partition_sizes[0]
        self.median_size = partition_sizes[len(partition_sizes) / 2]
        self.max_size = partition_sizes[-1]
    
    def test_init_configure (self):
        assert os.path.exists(CONFIG_FILE)
        system = Simulator()
        assert not system.partitions
        system = Simulator(config_file=CONFIG_FILE)
        assert system._partitions
        assert len(system._partitions) > 0

    def test_configure (self):
        assert os.path.exists(CONFIG_FILE)
        system = Simulator()
        assert not system._partitions
        system.configure(CONFIG_FILE)
        assert system._partitions
    
    def _find_location(self, jobid, size):
        job_location_args = [{
            'jobid': jobid,
            'nodes': self.median_size,
            'queue': "default",
            'utility_score': 1,
            'threshold': 0,
            'walltime': 1,
            'attrs': {}}]
        locations = self.system.find_job_location(job_location_args, [])
        assert locations.has_key(jobid)
        return locations[jobid]

    def test_reserve_partition (self):
        jobid = 3002
        location = self._find_location(jobid, self.max_size / 2)
        partition = self.system._partitions[location[0]]
        reserved = self.system.reserve_partition(partition.name)
        assert reserved
        assert partition.state == "busy"
        for parent in self.system._partitions.q_get([{'name':parent} for parent in partition.parents]):
            assert parent.state[0:7] == "blocked"
        for child in self.system._partitions.q_get([{'name':child} for child in partition.children]):
            assert child.state[0:7] == "blocked"
    
    def test_release_partition (self):
        jobid = 3003
        idle_partitions_before = self.system.get_partitions([{'state':"idle"}])
        location = self._find_location(jobid, self.median_size)
        partition = self.system._partitions[location[0]]
        reserved = self.system.reserve_partition(partition.name)
        assert reserved
        idle_partitions_after = self.system.get_partitions([{'state':"idle"}])
        assert len(idle_partitions_after) != len(idle_partitions_before)
        self.system.release_partition(partition.name)
        idle_partitions_after = self.system.get_partitions([{'state':"idle"}])
        assert len(idle_partitions_after) == len(idle_partitions_before)

    def _add_pg(self, jobid):
        location = self._find_location(jobid, self.median_size)
        self.system.add_process_groups([dict(
            id = "*",
            jobid = jobid,
            size = self.median_size,
            mode = "vn",
            executable = "/bin/ls",
            location = location,
            cwd = os.getcwd(),
            inputfile = "infile",
            outputfile = "outfile",
            errorfile = "errfile",
            user = os.getlogin(),
            args = [],
        )])

    def test_add_process_groups (self):
        jobid = 3004
        self._add_pg(jobid)

    def test_get_process_groups (self):
        jobid = 3005
        process_groups = self.system.get_process_groups([{'id':"*"}])
        assert not process_groups
        self._add_pg(jobid)
        process_groups = self.system.get_process_groups([{'id':"*"}])
        assert process_groups
        assert process_groups[0].jobid == jobid

    @timeout(Simulator.MAX_RUN_TIME + 30)
    def test_run_process_groups (self):
        jobid = 3006
        self._add_pg(jobid)
        process_groups = self.system.get_process_groups([{'id':"*"}])
        assert process_groups
        assert len(process_groups) == 1
        id = process_groups[0].id
        assert process_groups[0].jobid == jobid
        while True:
            process_groups = self.system.wait_process_groups([{'id': id}])
            if len(process_groups) > 0:
                assert len(process_groups) == 1
                assert process_groups[0].id == id
                assert process_groups[0].jobid == jobid
                break
            time.sleep(1)
    
    def test_signal_process_groups (self):
        jobid = 3007
        self._add_pg(jobid)
        for signal in ["SIGINT", "SIGKILL"]:
            process_groups = self.system.signal_process_groups([{'id':"*"}], signal)
            assert len(process_groups) == 1
            assert process_groups[0].jobid == jobid
            assert process_groups[0].signals[-1] == signal
