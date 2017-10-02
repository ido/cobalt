#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

"""Base system component

Outward facing common elements for system components.

key base classes.

Basic job launch

Basic resource reservation

Cluster-based equivalence classes


"""
import logging
from Cobalt.Components.base import exposed, automatic, query, locking
from Cobalt.Components.base import Component
from Cobalt.Util import init_cobalt_config, get_config_option

_logger = logging.getLogger()

init_cobalt_config()



class BaseSystem(Component):


    def __init__(self, *args, **kwargs):
        super(BaseSystem, self).__init__(*args, **kwargs)
        self._init_restart_common()

    def _init_restart_common(self, state=None):
        '''Common (re)initialization for restarts/clean starts'''
        if state is not None:
            self.process_manager = ProcessManager()
            self.resource_manager = ResourceManager()

    def __getstate__(self):
       return super(BaseSystem, self).__getstate__()

    def __setstate__(self, state):
        super(BaseSystem, self).__setstate__(state)
        self._init_restart_common(state)

    @exposed
    def validate_job(self, spec):
        raise NotImplementedError

    @exposed
    def reserve_resources_until(self, location, time, jobid):
        raise NotImplementedError

    @exposed
    @query
    def add_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    @query
    def wait_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    def find_queue_equivalence_classes(self, reservation_dict,
            active_queue_names, passthrough_blocking_res_list=[]):
        raise NotImplementedError

    @exposed
    def find_job_location(self, arg_list, end_times, pt_blocking_locations=[]):
        raise NotImplementedError

    @exposed
    @query
    def signal_process_groups(self, specs, signame="SIGINT"):
        raise NotImplementedError

    @exposed
    @query
    def get_process_groups(self, specs):
        raise NotImplementedError

    @exposed
    def get_nodes(self):
        raise NotImplementedError

    @exposed
    def update_nodes(self, updates, node_list, user):
        raise NotImplementedError

class ResourceManager(object):

    def __init__(self):
        pass

class ProcessManager(object):

    def __init__(self):
        pass
