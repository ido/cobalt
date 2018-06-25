"""Hardware abstraction layer for the system on which process groups are run.

Classes:
BGSimProcessGroup -- virtual process group running on the system
Simulator -- simulated system component
"""
import logging
import sys
import os
import random
import time
import uuid
import threading
from Queue import Queue
try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree
import Cobalt
import Cobalt.Data
import Cobalt.Util
from Cobalt.Components.base import Component, exposed, automatic, locking
from Cobalt.Components.bg_base_system import NodeCard, PartitionDict, BGBaseSystem
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from Cobalt.Util import sanitize_password, extract_traceback, get_current_thread_identifier
get_config_option = Cobalt.Util.get_config_option

__all__ = [
    "BGSimProcessGroup",
    "Simulator",
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BGSimProcessGroup(ProcessGroup):
    """Process Group modified for Blue Gene Simulator"""

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec)
        self.nodect = spec.get("nodect", None)


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
        self.config_file = kwargs.get("config_file", get_config_option('bgsystem', 'system_def_file', None))
        self._common_init_restart()

    def do_lookup(self):
        system_script_forker = Cobalt.Proxy.ComponentProxy('system_script_forker')
        current_killing_jobs = system_script_forker.get_children(None, [])
        pass

    def do_something_intense(self, worktime=20000):
        """This will create some synthetic work for python and the lst.sort() will not release the GIL.
        This can be used to find timeouts due to locking in the GIL."""
        # worktime can be increased to find race conditions.
        # worktime = worktime * 1000
        lst = list([random.random() for x in range(worktime)])
        lst.sort()

    def do_something_intense_lock_a(self):
        """Do some work and grab a lock"""
        self.logger.info('do_something_intense_lock_a, tid:%s, lock_a try', get_current_thread_identifier())
        with self._lock_a:
            self.logger.info('do_something_intense_lock_a, tid:%s, lock_a acq', get_current_thread_identifier())
            self.do_lookup()
            self.do_something_intense(worktime=4000)
        self.logger.info('do_something_intense_lock_a, tid:%s, lock_a rel', get_current_thread_identifier())

    def do_something_intense_lock_b(self):
        """Do some work and grab b lock"""
        self.logger.info('do_something_intense_lock_b, tid:%s, lock_b try', get_current_thread_identifier())
        with self._lock_b:
            self.logger.info('do_something_intense_lock_b, tid:%s, lock_b acq', get_current_thread_identifier())
            self.do_lookup()
            self.do_something_intense(worktime=4000)
        self.logger.info('do_something_intense_lock_b, tid:%s, lock_b rel', get_current_thread_identifier())

    def do_something_intense_with_lock(self):
        """Do some work and grab b lock, then a lock"""
        self.logger.info('do_something_intense_with_lock, tid:%s, lock_b try', get_current_thread_identifier())
        with self._lock_b:
            self.logger.info('do_something_intense_with_lock, tid:%s, lock_b acq', get_current_thread_identifier())
            self.logger.info('do_something_intense_with_lock, tid:%s, lock_a try', get_current_thread_identifier())
            with self._lock_a:
                self.logger.info('do_something_intense_with_lock, tid:%s, lock_a acq', get_current_thread_identifier())
                self.do_lookup()
                self.do_something_intense(worktime=4000)
            self.logger.info('do_something_intense_with_lock, tid:%s, lock_a rel', get_current_thread_identifier())
        self.logger.info('do_something_intense_with_lock, tid:%s, lock_b rel', get_current_thread_identifier())

    def _run_and_wrap(self, update_func):
        """same code pulled from CraySystem.py"""
        self.logger.info('_run_and_wrap %s, tid:%s', update_func, get_current_thread_identifier())
        update_func_name = update_func.__name__
        ts = time.time()
        try:
            update_func()
        except Exception:
            te = time.time()
            tb_str = sanitize_password('\n'.join(extract_traceback()))
            td = te - ts
            self.logger.error('_run_and_wrap(%s): td:%s error:%s' % (update_func_name, td, tb_str))
            bool_error = True
        else:
            te = time.time()
            td = te - ts
            bool_error = False
        return update_func_name, bool_error, td

    def _run_update_state(self):
        '''automated node update functions on the update timer go here.'''
        try:
            self.logger.info('_run_update_state starting, tid:%s, queue:%s',
                              get_current_thread_identifier(), self.node_update_thread_kill_queue.qsize())
            while self.node_update_thread_kill_queue.empty() is True:
                self.logger.info('_run_update_state running, tid:%s', get_current_thread_identifier())
                # Each of these is wrapped in it's own log-and-preserve block.
                # The outer try is there to ensure the thread update timeout happens.
                metadata_lst = []
                metadata_lst.append(self._run_and_wrap(self.do_something_intense_lock_a))
                metadata_lst.append(self._run_and_wrap(self.do_something_intense_lock_b))
                metadata_lst.append(self._run_and_wrap(self.do_something_intense_with_lock))
                any_error = False
                for func_name, error, td in metadata_lst:
                    if error is True:
                        any_error = True
                if any_error is True:
                    self.logger.critical("_run_update_state: error occurred, timings below.")
                    for func_name, error, td in metadata_lst:
                        self.logger.critical("%s: %s", func_name, td)
                self.logger.info('_run_update_state sleeping for %s, tid:%s', self.update_thread_timeout,
                                 get_current_thread_identifier())
                Cobalt.Util.sleep(self.update_thread_timeout)
            self.logger.critical('_run_update_state exiting, tid:%s', get_current_thread_identifier())
            self.node_update_thread_kill_queue.get(timeout=1.0)
            self.node_update_thread_dead = True
        finally:
            self.node_update_thread_dead = True
        self.logger.critical('_run_update_state dead, tid:%s', get_current_thread_identifier())
        return


    def _common_init_restart(self, spec=None):
        """this is the common code that must be called when instanciating the class or
        bringing it back from a state file."""
        self.logger.info("init: Brooklyn starting.")
        self._lock_a = threading.RLock()
        self._lock_b = threading.RLock()
        self.process_groups.item_cls = BGSimProcessGroup
        self.node_card_cache = dict()
        self.update_thread_timeout = 10.0
        if spec is None:
            operation = 'start'
            self.failed_components = set()
        else:
            operation = 'restart'
            try:
                self.failed_components = spec['failed_components']
            except KeyError:
                self.failed_components = set()
            try:
                self.config_file = spec['config_file']
            except KeyError:
                self.config_file = os.path.expandvars(get_config_option('system', 'def_file', ""))
        if self.config_file is not None:
            self.logger.log(1, "%s: loading machine configuration", operation)
            self.configure(self.config_file)
            self.logger.log(1, "%s: restoring partition state", operation)
            if spec is not None:
                self._restore_partition_state(spec)
            self.logger.log(1, "%s: recomputing partition state", operation)
            self._recompute_partition_state()

        self.node_update_thread_kill_queue = Queue()
        self.node_update_thread_dead = False
        self.logger.info("_run_update_state thread starting.")
        self.node_update_thread = threading.Thread(target=self._run_update_state)
        self.node_update_thread.daemon = True
        self.node_update_thread.start()
        self.logger.info("_run_update_state thread started:%s", self.node_update_thread)

        self.logger.info("init: Brooklyn ready.")

    def __getstate__(self):
        state = {}
        state.update(BGBaseSystem.__getstate__(self))
        state.update({
                'simulator_version':4,
                'config_file':self.config_file,
                'failed_components': self.failed_components})
        return state

    def __setstate__(self, state):
        operation = 'restart'
        try:
            self.logger.log(1, "%s: initializing base system class", operation)
            BGBaseSystem.__setstate__(self, state)
            self._common_init_restart(spec=state)
        except:
            self.logger.error("A fatal error occurred while %sing the system component", operation, exc_info=True)
            print("A fatal error occurred while restarting the system component.  Terminating.")
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
                    p.state = "blocked (%s)" % (part.name,)
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
            self.logger.error("problem loading data from file: %r" % config_file, exc_info=True)
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
                name=partition_def.get("name"),
                queue=partition_def.get("queue", "default"),
                size=NODES_PER_NODECARD * nc_count,
                node_cards=node_list,
                switches=switch_list,
                wires=wire_list,
                state="idle",
            )])

        # find the wiring deps
        self.logger.log(1, "configure: looking for wiring dependencies")
        for p in self._partitions.values():
            self._detect_wiring_deps(p)

        # update partition relationship lists
        self.logger.log(1, "configure: updating partition relationship lists")
        self.update_relatives()

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

    def _mark_partition_for_cleaning(self, pname, jobid):
        pass

    def _set_kernel(self, partition, kernel):
        # TODO: allow the kernel set step to work in the simulator.  For now this doesn't fly.
        pass

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
                return False
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

    @locking
    @exposed
    def find_job_location(self, arg_list, end_times):
        """This is a wrapper around find_job_location that can be used to create a circumstance
        that can allow finding of errors.  This also provides entry and exit logging."""
        self.logger.debug("Simulator:starting find_job_location")
        result = super(Simulator, self).find_job_location(arg_list, end_times)
        #lets do at least 10 seconds of work.
        #self.logger.debug("Simulator:starting *** do_something_intense *** ")
        with self._lock_a:
            self.do_something_intense(worktime=4000)
        #self.logger.debug("Simulator:complete *** do_something_intense *** ")
        self.logger.debug("Simulator:complete find_job_location")
        return result

    @exposed
    def reserve_resources_until(self, location, new_time, jobid):
        """This is a wrapper around reserve_resources_until that can be used to create a circumstance
        that can allow finding of errors.  This also provides entry and exit logging."""
        self.logger.debug("Simulator:starting reserve_resources_until")
        result = super(Simulator, self).reserve_resources_until(location, new_time, jobid)
        #lets do at least 10 seconds of work.
        ident = uuid.uuid4().hex
        self.logger.debug("Simulator:starting *** %s do_something_intense *** ", ident)
        with self._lock_a:
            self.do_something_intense(worktime=4000)
        self.logger.debug("Simulator:complete *** %s do_something_intense *** ", ident)
        self.logger.debug("Simulator:complete reserve_resources_until")
        return result

