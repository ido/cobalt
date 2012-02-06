"""Hardware abstraction layer for the system on which process groups are run.

Classes:
BGSimProcessGroup -- virtual process group running on the system
Simulator -- simulated system component
"""

import pwd
import logging
import sys
import os
import operator
import random
import time
import thread
import threading
import xmlrpclib
from datetime import datetime
from ConfigParser import ConfigParser

try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree

import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Components import bg_base_system
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Components.bg_base_system import NodeCard, Partition, PartitionDict, BGProcessGroupDict, BGBaseSystem
from Cobalt.Exceptions import ProcessGroupCreationError, ComponentLookupError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Statistics import Statistics
from Cobalt.DataTypes.ProcessGroup import ProcessGroup

__all__ = [
    "BGSimProcessGroup", 
    "Simulator",
]

logger = logging.getLogger(__name__)


class BGSimProcessGroup(ProcessGroup):
    """Process Group modified for Blue Gene Simulator"""

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get("nodect",None)



class Simulator (BGBaseSystem):
    
    """Generic system simulator.
    
    Methods:
    configure -- load partitions from an xml file
    reserve_partition -- lock a partition for use by a process_group (exposed)
    release_partition -- release a locked (busy) partition (exposed)
    add_process_groups -- add (start) a process group on the system (exposed, query)
    get_process_groups -- retrieve process groups (exposed, query)
    wait_process_groups -- get process groups that have exited, and remove them from the system (exposed, query)
    signal_process_groups -- send a signal to the head process of the specified process groups (exposed, query)
    update_partition_state -- simulates updating partition state from the bridge API (automatic)
    """
    
    name = "system"
    implementation = "simulator"
    
    logger = logger

    bgsystem_config = BGBaseSystem.bgsystem_config

    def __init__ (self, *args, **kwargs):
        BGBaseSystem.__init__(self, *args, **kwargs)
        sys.setrecursionlimit(5000) #why this magic number?
        self.process_groups.item_cls = BGSimProcessGroup
        self.config_file = kwargs.get("config_file", None)
        self.failed_components = set()
        if self.config_file is not None:
            self.configure(self.config_file)
    
    def __getstate__(self):
        state = {}
        state.update(BGBaseSystem.__getstate__(self))
        state.update({
                'simulator_version':3,
                'config_file':self.config_file})
        return state
    
    def __setstate__(self, state):
        BGBaseSystem.__setstate__(self, state)
        self.config_file = state['config_file']
        self.process_groups.item_cls = BGSimProcessGroup
        if self.config_file is not None:
            self.configure(self.config_file)
        self.update_relatives()
        self._restore_partition_state(state)
        
    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me, float(bgsystem_config.get('save_me_interval', 10)))


    def configure (self, config_file):
        
        """Configure simulated partitions.
        
        Arguments:
        config_file -- xml configuration file
        """
        
        def _get_node_card(name):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name)
                
            return self.node_card_cache[name]
            
            
        self.logger.info("configure()")
        try:
            system_doc = ElementTree.parse(config_file)
        except IOError:
            self.logger.error("unable to open file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)
        except:
            self.logger.error("problem loading data from file: %r" % config_file)
            self.logger.error("exiting...")
            sys.exit(1)
            
        system_def = system_doc.getroot()
        if system_def.tag != "BG":
            self.logger.error("unexpected root element in %r: %r" % (config_file, system_def.tag))
            self.logger.error("exiting...")
            sys.exit(1)
        
        # that 32 is not really constant -- it needs to either be read from cobalt.conf or from the bridge API
        NODES_PER_NODECARD = 32
                
        # initialize a new partition dict with all partitions
        #
        partitions = PartitionDict()
        
        tmp_list = []

        # this is going to hold partition objects from the bridge (not our own Partition)
        wiring_cache = {}
        bp_cache = {}
        
        for partition_def in system_def.getiterator("Partition"):
            node_list = []
            switch_list = []
            
            for nc in partition_def.getiterator("NodeCard"): 
                node_list.append(_get_node_card(nc.get("id")))

            nc_count = len(node_list)
            
            if not wiring_cache.has_key(nc_count):
                wiring_cache[nc_count] = []
            wiring_cache[nc_count].append(partition_def.get("name"))

            for s in partition_def.getiterator("Switch"):
                switch_list.append(s.get("id"))

            tmp_list.append( dict(
                name = partition_def.get("name"),
                queue = partition_def.get("queue", "default"),
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                switches = switch_list,
                state = "idle",
            ))
        
        partitions.q_add(tmp_list)
        
        # find the wiring deps
        for size in wiring_cache:
            for p in wiring_cache[size]:
                p = partitions[p]
                s1 = set( p.switches )
                for other in wiring_cache[size]:
                    other = partitions[other]
                    if (p.name == other.name):
                        continue

                    s2 = set( other.switches )
                    
                    if s1.intersection(s2):
                        self.logger.info("found a wiring dep between %s and %s", p.name, other.name)
                        partitions[p.name]._wiring_conflicts.add(other.name)
        
            
        # update object state
        self._partitions.clear()
        self._partitions.update(partitions)

    
    def reserve_partition (self, name, size=None):
        """Reserve a partition and block all related partitions.
        
        Arguments:
        name -- name of the partition to reserve
        size -- size of the process group reserving the partition (optional)
        """
        
        try:
            self._partitions_lock.acquire()

            try:
                partition = self.partitions[name]
            except KeyError:
                self.logger.error("reserve_partition(%r, %r) [does not exist]" % (name, size))
                return False
            if partition.state != "allocated":
                self.logger.error("reserve_partition(%r, %r) [%s]" % (name, size, partition.state))
                return False
            if not partition.functional:
                self.logger.error("reserve_partition(%r, %r) [not functional]" % (name, size))
            if size is not None and size > partition.size:
                self.logger.error("reserve_partition(%r, %r) [size mismatch]" % (name, size))
                return False

            partition.state = "busy"
            # partition.reserved_until = False
        finally:
            self._partitions_lock.release()

        # explicitly call this, since the above "busy" is instantaneously available
        self.update_partition_state()
        
        self.logger.info("reserve_partition(%r, %r)" % (name, size))
        return True
    reserve_partition = exposed(reserve_partition)
    
    def release_partition (self, name):
        """Release a reserved partition.
        
        Arguments:
        name -- name of the partition to release
        """
        try:
            self._partitions_lock.acquire()

            try:
                partition = self.partitions[name]
            except KeyError:
                self.logger.error("release_partition(%r) [already free]" % (name))
                return False
            if not partition.state == "busy":
                self.logger.info("release_partition(%r) [not busy]" % (name))
                return False
                
            if partition.used_by is not None:
                partition.state = "allocated"
            else:
                partition.state = "idle"
        finally:
            self._partitions_lock.release()

        # explicitly unblock the blocked partitions
        self.update_partition_state()

        self.logger.info("release_partition(%r)" % (name))
        return True
    release_partition = exposed(release_partition)
    
    def _mark_partition_for_cleaning(self, pname, jobid):
        pass

    def _set_kernel(self, partition, kernel):
        # TODO: allow the kernel set step to work in the simulator.  For now this doesn't fly.
        pass

    def update_partition_state(self):
        # first, set all of the nodecards to not busy
        for nc in self.node_card_cache.values():
            nc.used_by = ''

        self._partitions_lock.acquire()
        try:
            for p in self._partitions.values():
                p._update_node_cards()
                
            now = time.time()
            
            # since we don't have the bridge, a partition which isn't busy
            # should be set to idle and then blocked states can be derived
            for p in self._partitions.values():
                if p.state != "busy":
                    p.state = "idle"
                if p.reserved_until and now > p.reserved_until:
                    p.reserved_until = None
                    p.reserved_by = None
                    
            for p in self._partitions.values():
                if p.state == "busy":
                    # when the partition becomes busy, if a script job isn't reserving it, then release the reservation
                    if not p.reserved_by:
                        p.reserved_until = False
                else:
                    if p.reserved_until:
                        p.state = "allocated"
                        for part in p._parents:
                            if part.state == "idle":
                                part.state = "blocked (%s)" % (p.name,)
                        for part in p._children:
                            if part.state == "idle":
                                part.state = "blocked (%s)" % (p.name,)
                    for diag_part in self.pending_diags:
                        if p.name == diag_part.name or p.name in diag_part.parents or p.name in diag_part.children:
                            p.state = "blocked by pending diags"
                    for nc in p.node_cards:
                        if nc.used_by:
                            p.state = "blocked (%s)" % nc.used_by
                            break
                    for dep_name in p._wiring_conflicts:
                        if self._partitions[dep_name].state in ["allocated", "busy"]:
                            p.state = "blocked-wiring (%s)" % dep_name
                            break
                    for part_name in self.failed_diags:
                        part = self._partitions[part_name]
                        if p.name == part.name:
                            p.state = "failed diags"
                        elif p.name in part.parents or p.name in part.children:
                            p.state = "blocked by failed diags"
        except:
            self.logger.error("error in update_partition_state", exc_info=True)
        
        self._partitions_lock.release()
    update_partition_state = automatic(update_partition_state)

    def add_failed_components(self, component_names):
        success = []
        for name in component_names:
            if self.node_card_cache.has_key(name):
                self.failed_components.add(name)
                success.append(name)
            else:
                for p in self._partitions.values():
                    if name in p.switches:
                        self.failed_components.add(name)
                        success.append(name)
                        break
        return success
    add_failed_component = exposed(add_failed_components)
    
    def del_failed_components(self, component_names):
        success = []
        for name in component_names:
            try:
                self.failed_components.remove(name)
                success.append(name)
            except KeyError:
                pass
            
        return success
    del_failed_components = exposed(del_failed_components)
    
    def list_failed_components(self, component_names):
        return list(self.failed_components)
    list_failed_components = exposed(list_failed_components)
    
    def launch_diags(self, partition, test_name):
        exit_value = 0
        for nc in partition.node_cards:
            if nc.id in self.failed_components:
                exit_value = 1
        for switch in partition.switches:
            if switch in self.failed_components:
                exit_value = 2

        self.finish_diags(partition, test_name, exit_value)
