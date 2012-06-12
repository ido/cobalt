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

try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree

import Cobalt
import Cobalt.Data
import Cobalt.Util
get_config_option = Cobalt.Util.get_config_option
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

    def __init__ (self, *args, **kwargs):
        BGBaseSystem.__init__(self, *args, **kwargs)
        sys.setrecursionlimit(5000) #why this magic number?
        self.process_groups.item_cls = BGSimProcessGroup
        self.node_card_cache = dict()
        self.failed_components = set()
        self.config_file = kwargs.get("config_file", get_config_option('bgsystem', 'system_def_file', None))
        if self.config_file is not None:
            self.logger.log(1, "init: loading machine configuration")
            self.configure(self.config_file)
            self.logger.log(1, "init: recomputing partition state")
            self._recompute_partition_state()
    
    def __getstate__(self):
        state = {}
        state.update(BGBaseSystem.__getstate__(self))
        state.update({
                'simulator_version':4,
                'config_file':self.config_file,
                'failed_components': self.failed_components})
        return state
    
    def __setstate__(self, state):
        try:
            self.logger.log(1, "restart: initializing base system class")
            BGBaseSystem.__setstate__(self, state)
            self.process_groups.item_cls = BGSimProcessGroup
            self.node_card_cache = dict()
            try:
                self.failed_components = state['failed_components']
            except KeyError:
                self.failed_components = set()
            try:
                self.config_file = state['config_file']
            except KeyError:
                self.config_file = os.expandvars(get_config_option('system', 'def_file', ""))
            if self.config_file:
                self.logger.log(1, "restart: loading machine configuration")
                self.configure(self.config_file)
                self.logger.log(1, "restart: restoring partition state")
                self._restore_partition_state(state)
                self.logger.log(1, "restart: recomputing partition state")
                self._recompute_partition_state()
        except:
            self.logger.error("A fatal error occurred while restarting the system component", exc_info=True)
            print "A fatal error occurred while restarting the system component.  Terminating."
            sys.exit(1)

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me, float(get_config_option('bgsystem', 'save_me_interval', 10)))

    def _recompute_partition_state(self):
        self.offline_partitions = []

        for p in self._partitions.values():
            if p.state != 'idle':
                continue

            for part_name in self.failed_partitions:
                try:
                    part = self._partitions[part_name]
                except KeyError:
                    pass
                else:
                    if p == part:
                        p.state = "failed diags"
                        break
                    elif p in part._parents or p in part._children:
                        p.state = "blocked (%s)" % (part.name,)
                        break
            if p.state != 'idle':
                continue

            for nc in p.node_cards:
                if nc.id in self.failed_components:
                    p.state = "hardware offline: nodecard %s" % nc.id
                    self.offline_partitions.append(p.name)
                    break
                elif nc.used_by:
                    p.state = "blocked (%s)" % nc.used_by
                    break
            if p.state != 'idle':
                continue

            for s in p.switches:
                if s in self.failed_components:
                    p.state = "hardware offline: switch %s" % (s,)
                    self.offline_partitions.append(p.name)
                    break
            if p.state != 'idle':
                continue

            for w in p.wires:
                if w in self.failed_components:
                    p.state = "hardware offline: switch %s" % (w,)
                    self.offline_partitions.append(p.name)
                    break
            if p.state != 'idle':
                continue

            for dep_name in p._wiring_conflicts:
                try:
                    part = self._partitions[dep_name]
                except KeyError:
                    self.logger.warning("partition %s: wiring conflict %s does not exist in partition table",
                        p.name, dep_name)
                else:
                    if part.state == "busy" or part.used_by:
                        p.state = "blocked-wiring (%s)" % dep_name
                        break
            if p.state != 'idle':
                continue

            if p.used_by:
                p.state = "allocated"
                continue

            for part in p._parents.union(p._children):
                if part.used_by:
                    p.state = "blocked (%s)" % (allocated.name,)
                    break

    def configure (self, config_file):
        """
        Configure simulated partitions.
        
        Arguments:
        config_file -- xml configuration file
        """
        
        self.logger.log(1, "configure: opening machine configuration file")
        def _get_node_card(name):
            if not self.node_card_cache.has_key(name):
                self.node_card_cache[name] = NodeCard(name)
                
            return self.node_card_cache[name]
            
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
        self.logger.log(1, "configure: acquiring machine information and creating partition objects")
        self._partitions.clear()
        for partition_def in system_def.getiterator("Partition"):
            node_list = []
            switch_list = []
            wire_list = []
            
            for nc in partition_def.getiterator("NodeCard"): 
                node_list.append(_get_node_card(nc.get("id")))

            nc_count = len(node_list)
            
            for s in partition_def.getiterator("Switch"):
                switch_list.append(s.get("id"))

            for w in partition_def.getiterator("Wire"):
                wire_list.append(w.get("id"))

            self._partitions.q_add([dict(
                name = partition_def.get("name"),
                queue = partition_def.get("queue", "default"),
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                switches = switch_list,
                wires = wire_list,
                state = "idle",
            )])
        
        # find the wiring deps
        self.logger.log(1, "configure: looking for wiring dependencies")
        for p in self._partitions.values():
            self._detect_wiring_deps(p)
            
        # update partition relationship lists
        self.logger.log(1, "configure: updating partition relationship lists")
        self.update_relatives()

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
            # first determine if the partition and associate node cards are in use
            now = time.time()
            for p in self._partitions.values():
                # since we don't have the bridge, a partition which isn't busy
                # should be set to idle and then blocked states can be derived
                if p.state != "busy":
                    p.state = "idle"

                # check if the partition is not longer reserved or the reservation has expired
                if p.used_by:
                    if not p.reserved_until or now > p.reserved_until:
                        p.reserved_until = None
                        p.reserved_by = None
                        p.used_by = None
                    # for now, assume cleanup happens instantaneously
                    p.state = 'idle'

                p._update_node_cards()

            # then set parition states based on that usage as well as failed hardware, resource reservations, etc.
            self._recompute_partition_state()
        except:
            self.logger.error("error in update_partition_state", exc_info=True)

        self._partitions_lock.release()
    update_partition_state = automatic(update_partition_state)

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
