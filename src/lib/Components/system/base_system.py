#!/usr/bin/env python

"""Base system component

Outward facing common elements for system components.

key base classes.

Basic job launch

Basic resource reservation

Cluster-based equivalence classes


"""
import logging
from Cobalt import exposed, automatic, query, locking
from Cobalt.Util import init_cobalt_config, get_config_option

_logger = logging.getLogger()

init_cobalt_config()



class BaseSystem(object):

    def __init__(self, *args, **kwargs):
        pass
        #self.process manager = ClusterNodeProcessManager()
        #self.resource manager = CluserNodeResourceManager()

    #TODO: Add setstate/getstate

    @exposed
    def reserve_resources_until(self, location, time, jobid):
        raise NotImplementedError

    @exposed
    def add_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    def wait_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    def del_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    def find_queue_equivalence_classes(self):
        raise NotImplementedError

    @exposed
    def signal_process_groups(self):
        raise NotImplementedError

class ResourceManager(object):

    def __init__(self):
        pass

class ProcessManager(object):

    def __init__(self):
        pass
