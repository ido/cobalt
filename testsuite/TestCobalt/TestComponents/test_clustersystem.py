'''Tests for the cluster system component.

'''

from nose import *
import os
import Cobalt
import TestCobalt

#set and override config file prior to importing cluster_system
#the "init on import" behavior is probably a "broken" thing to be doing.
#perhaps this should all be moved to a mandatory configure method called
#by the component init? --PMR

STD_COBALT_CONFIG_FILE_NAME = 'cobalt-cluster-test.conf'
STD_COBALT_CONFIG_FILE = '''
[cluster_system]
hostfile = cobalt.hostfile
simulation_mode = True
run_remote = false

[system]
size = 4

'''
STD_COBALT_HOSTFILE_NAME = 'cobalt.hostfile'
STD_COBALT_HOSTFILE = '''vs1.test
vs2.test
vs3.test
vs4.test
'''

def gen_std_config_files():
    '''Generate a standard Cobalt conf and hostfile for testing.

    '''
    f = open(STD_COBALT_CONFIG_FILE_NAME, 'w')
    f.write(STD_COBALT_CONFIG_FILE)
    f.close()

    f = open(STD_COBALT_HOSTFILE_NAME, 'w')
    f.write(STD_COBALT_HOSTFILE)
    f.close()

    Cobalt.CONFIG_FILES[0] = STD_COBALT_CONFIG_FILE_NAME
gen_std_config_files()

import Cobalt.Components.cluster_base_system
import Cobalt.Components.cluster_system
import time


def teardown_module():
    '''remove standard conf files.'''
    os.remove(STD_COBALT_CONFIG_FILE_NAME)
    os.remove(STD_COBALT_HOSTFILE_NAME)


def get_basic_job_dict():
    return {'jobid': 1,
            'nodes': 1,
            'queue': 'default',
            'walltime': 10,
            }

class TestClusterSystem(object):
    '''Test core cluster system functionality'''

    def __init__(self):
        self.cluster_system = None
        self.full_node_set = set(['vs1.test', 'vs2.test', 'vs3.test', 'vs4.test'])

    def setup(self):
        '''Ensure cluster system exists for all tests.  Refresh the setup between tests'''
        self.cluster_system = Cobalt.Components.cluster_system.ClusterSystem()

    def teardown(self):
        '''Free cluster system base class between tests.  Forces reinitialization.'''
        del self.cluster_system

    def test_init_drain_time_no_jobs(self):
        #Test initilaization of drain times with no currently running jobs.
        end_times = []
        self.cluster_system.node_end_time_dict = {-1:['foo']}
        self.cluster_system.init_drain_times(end_times)
        assert -1 not in self.cluster_system.node_end_time_dict.keys(), "ERROR: node_end_time_dict not reset!"
        assert set(self.cluster_system.node_end_time_dict[0]) ^ self.full_node_set == set([]), \
                "ERROR: Mismatch between node_end_time_dict and full node set for no jobs test! Generated: %s\nExpected %s\n" % \
                (set(self.cluster_system.node_end_time_dict[0]), self.full_node_set)

    def test_init_drain_time_single_node_job(self):
        #Check drain time initialization with single running job
        end_time = int(time.time()) + 300
        end_times = [[['vs2.test'], end_time]]
        self.cluster_system.node_end_time_dict = {-1:['foo']}
        self.cluster_system.init_drain_times(end_times)
        assert -1 not in self.cluster_system.node_end_time_dict.keys(), "ERROR: node_end_time_dict not reset!"
        assert set(self.cluster_system.node_end_time_dict[0]) ^ self.full_node_set == set(['vs2.test']), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time 0!\nGenerated %s\nExpected %s\n" % \
                (set(self.cluster_system.node_end_time_dict[0]) ^ self.full_node_set, set(['vs2.test']))
        assert set(self.cluster_system.node_end_time_dict[end_time]) ^ self.full_node_set == \
                set(['vs1.test', 'vs3.test', 'vs4.test']), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time %s!\nGenerated %s\nExpected %s\n" % \
                (end_time, set(self.cluster_system.node_end_time_dict[0]),set(['vs2.test']))

    def test_init_drain_time_multiple_jobs(self):
        #Check drain time initialization for multiple running jobs.
        now = int(time.time())
        end_time_list = [now + 300, now + 400, now + 600]
        end_times = [[['vs2.test'], end_time_list[0]], [['vs1.test', 'vs3.test'], end_time_list[1]],
                [['vs4.test'], end_time_list[2]]]
        self.cluster_system.node_end_time_dict = {-1:['foo']}
        self.cluster_system.init_drain_times(end_times)
        assert -1 not in self.cluster_system.node_end_time_dict.keys(), "ERROR: node_end_time_dict not reset!"
        assert set(self.cluster_system.node_end_time_dict[0]) == set([]), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time 0!\nGenerated %s\nExpected %s\n" % \
                (set(self.cluster_system.node_end_time_dict[0]), set([]))
        assert set(self.cluster_system.node_end_time_dict[end_time_list[0]]) == set(['vs2.test']), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time %s!\nGenerated %s\nExpected %s\n" % \
                (end_time_list[0], set(self.cluster_system.node_end_time_dict[end_time_list[0]]), set(['vs2.test']))
        assert set(self.cluster_system.node_end_time_dict[end_time_list[1]]) == set(['vs1.test', 'vs3.test']), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time %s!\nGenerated %s\nExpected %s\n" % \
                (end_time_list[1], set(self.cluster_system.node_end_time_dict[end_time_list[1]]), set(['vs1.test', 'vs3.test']))
        assert set(self.cluster_system.node_end_time_dict[end_time_list[2]]) == set(['vs4.test']), \
                "ERROR: Mismatch between node_end_time_dict and full_node set for time %s!\nGenerated %s\nExpected %s\n" % \
                (end_time_list[2], set(self.cluster_system.node_end_time_dict[end_time_list[2]]), set(['vs4.test']))


    def test__find_job_location_basic_job_no_drain(self):
        #Check that find job locations works with a basic job, clean resources, and sets job to run.
        now = int(time.time())
        job = get_basic_job_dict()
        job['nodes'] = 4

        self.cluster_system.init_drain_times([]) #All resources are clear
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)

        assert ready_to_run, "ERROR: Job not ready to run on empty system"
        assert new_drain_time == 0, "Job ready to run, drain time must be 0"
        assert best_location != {}, "ERROR: Ready to run, but we have no best location."
        assert best_location == {'1':['vs2.test', 'vs4.test', 'vs1.test', 'vs3.test']}, "ERROR: Missing nodes from best location," \
            " got: %s" % best_location


    def test__find_job_location_job_all_down_locs(self):
        #ensure no attempt to run if all nodes are down.
        now = int(time.time())
        job = get_basic_job_dict()
        self.cluster_system.nodes_down(list(self.full_node_set))
        assert self.cluster_system.down_nodes ^ self.full_node_set == set([]), "all nodes were not marked down."
        self.cluster_system.init_drain_times([])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)

        assert not ready_to_run, "ERROR: marked ready to run when running impossible."
        assert new_drain_time == 0, "ERROR: No draining possible for all down hardware."
        assert best_location == {}, "ERROR: Best locaion found when no best loc possible! Tried %s" % best_location

    def test__find_job_location_job_too_few_locs(self):
        #ensure we dont' try to schedule a job when we have too few locations available.
        now = int(time.time())
        job = get_basic_job_dict()
        job['nodes'] = 4
        self.cluster_system.nodes_down(['vs1.test'])
        self.cluster_system.init_drain_times([])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)

        assert not ready_to_run, "ERROR: marked ready to run when running impossible."
        assert new_drain_time == 0, "ERROR: No draining possible for this set of down hardware."
        assert best_location == {}, "ERROR: Best locaion found when no best loc possible! Tried %s" % best_location


    def test__find_job_location_drain_for_job(self):
        now = int(time.time())
        end_time = now + 600
        job = get_basic_job_dict()
        job['nodes'] = 4
        self.cluster_system.running_nodes.update(['vs1.test'])
        self.cluster_system.init_drain_times([[['vs1.test'], end_time]])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)
        assert not ready_to_run, "ERROR: marked ready to run when running impossible."
        assert new_drain_time == end_time, "ERROR: Expected new drain time of %d but got %d." % (end_time, new_drain_time)
        assert best_location == {'1':['vs2.test', 'vs4.test', 'vs1.test', 'vs3.test']}, \
                "ERROR: Unexpected best location selection.  Generated %s." % best_location

    def test__find_job_location_drain_soonest(self):
        now = int(time.time())
        end_time_list = [ now + 600, now + 700]
        job = get_basic_job_dict()
        job['nodes'] = 2
        self.cluster_system.running_nodes.update(['vs2.test', 'vs3.test', 'vs4.test'])
        self.cluster_system.init_drain_times([[['vs2.test'], end_time_list[0]], [['vs3.test', 'vs4.test'], end_time_list[1]]])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)
        assert not ready_to_run, "ERROR: job selected to run with insufficient resources."
        assert new_drain_time == end_time_list[0], "ERROR: Expected drain time %d, got %d instead" % (end_time_list[0],
                new_drain_time)
        assert best_location == {'1':['vs2.test', 'vs1.test']}, "ERROR: Expected best location: %s\nGot:%s" % \
                ({'1':['vs2.test', 'vs1.test']}, best_location)

    def test__find_job_location_drain_sufficient(self):
        now = int(time.time())
        end_time_list = [ now + 600, now + 700]
        job = get_basic_job_dict()
        job['nodes'] = 3
        self.cluster_system.running_nodes.update(['vs2.test', 'vs3.test', 'vs4.test'])
        self.cluster_system.init_drain_times([[['vs2.test'], end_time_list[0]], [['vs3.test', 'vs4.test'], end_time_list[1]]])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now)
        assert not ready_to_run, "ERROR: job selected to run with insufficient resources."
        assert new_drain_time == end_time_list[1], "ERROR: Expected drain time %d, got %d instead" % (end_time_list[1],
                new_drain_time)
        assert best_location == {'1':['vs2.test', 'vs1.test', 'vs3.test']}, "ERROR: Expected best location: %s\nGot:%s" % \
                ({'1':['vs2.test', 'vs1.test', 'vs3.test']}, best_location)

    def test__find_job_location_select_backfill_job(self):
        now = int(time.time())
        end_time_list = [ now + 600, now + 700]
        job = get_basic_job_dict()
        job['walltime'] = 5
        self.cluster_system.running_nodes.update(['vs2.test', 'vs3.test', 'vs4.test'])
        self.cluster_system.init_drain_times([[['vs2.test'], end_time_list[0]], [['vs3.test', 'vs4.test'], end_time_list[1]]])
        best_location, new_drain_time, ready_to_run = self.cluster_system._find_job_location(job, now, end_time_list[0])
        assert ready_to_run, "ERROR: job not backfilled."
        assert new_drain_time == 0, "ERROR: Expected drain time %d, got %d instead" % (0,
                new_drain_time)
        assert best_location == {'1':['vs1.test']}, "ERROR: Expected best location: %s\nGot:%s" % \
                ({'1':['vs1.test']}, best_location)
