"""Hardware abstraction layer for the system on which process groups are run.

Classes:
NodeCard -- node cards make up Partitions
Partition -- atomic set of nodes
PartitionDict -- default container for partitions
ProcessGroup -- virtual process group running on the system
ProcessGroupDict -- default container for process groups
BGBaseSystem -- base system component
"""

import Cobalt
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError, JobValidationError
from Cobalt.Components.base import Component, exposed, automatic, query
import sets, thread, ConfigParser

__all__ = [
    "NodeCard",
    "Partition",
    "PartitionDict",
    "ProcessGroup",
    "ProcessGroupDict", 
    "BGBaseSystem",
]

CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)

class NodeCard (object):
    """node cards make up Partitions"""
    def __init__(self, name, state="RM_NODECARD_UP"):
        self.id = name
        self.used_by = ''
        self.state = ''
        
    def __eq__(self, other):
        return self.id == other.id
        

class Partition (Data):
    
    """An atomic set of nodes.
    
    Partitions can be reserved to run process groups on.
    
    Attributes:
    tag -- partition
    scheduled -- ? (default False)
    name -- canonical name
    functional -- the partition is available for reservations
    queue -- ?
    parents -- super(containing)-partitions
    children -- sub-partitions
    size -- number of nodes in the partition
    
    Properties:
    state -- "idle", "busy", or "blocked"
    """
    
    fields = Data.fields + [
        "tag", "scheduled", "name", "functional",
        "queue", "size", "parents", "children", "state",
    ]
    
    def __init__ (self, spec):
        """Initialize a new partition."""
        Data.__init__(self, spec)
        spec = spec.copy()
        self.scheduled = spec.pop("scheduled", False)
        self.name = spec.pop("name", None)
        self.functional = spec.pop("functional", False)
        self.queue = spec.pop("queue", "default")
        self.size = spec.pop("size", None)
        # these hold Partition objects
        self._parents = sets.Set()
        self._children = sets.Set()
        self.state = spec.pop("state", "idle")
        self.tag = spec.get("tag", "partition")
        self.node_cards = spec.get("node_cards", [])
        self.switches = spec.get("switches", [])
        # this holds partition names
        self._wiring_conflicts = sets.Set()

        self._update_node_cards()

    def _update_node_cards(self):
        if self.state == "busy":
            for nc in self.node_cards:
                nc.used_by = self.name
    
    def _get_parents (self):
        return [parent.name for parent in self._parents]
    
    parents = property(_get_parents)
    
    def _get_children (self):
        return [child.name for child in self._children]
    
    children = property(_get_children)
    
    def _get_node_card_names (self):
        return [nc.id for nc in self.node_cards]
    
    node_card_names = property(_get_node_card_names)
    
    def __str__ (self):
        return self.name
    
    def __repr__ (self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class PartitionDict (DataDict):
    """Default container for partitions.
    
    Keyed by partition name.
    """
    
    item_cls = Partition
    key = "name"

class ProcessGroup (Data):
    required_fields = ['user', 'executable', 'args', 'location', 'size', 'cwd']
    fields = Data.fields + [
        "id", "user", "size", "cwd", "executable", "env", "args", "location",
        "head_pid", "stdin", "stdout", "stderr", "exit_status", "state",
        "mode", "kerneloptions", "true_mpi_args",
    ]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.id = spec.get("id")
        self.head_pid = None
        self.stdin = spec.get('stdin')
        self.stdout = spec.get('stdout')
        self.stderr = spec.get('stderr')
        self.exit_status = None
        self.location = spec.get('location') or []
        self.user = spec.get('user', "")
        self.executable = spec.get('executable')
        self.cwd = spec.get('cwd')
        self.size = spec.get('size')
        self.mode = spec.get('mode', 'co')
        self.args = " ".join(spec.get('args') or [])
        self.kerneloptions = spec.get('kerneloptions')
        self.env = spec.get('env') or {}
        self.true_mpi_args = spec.get('true_mpi_args')

    def _get_state (self):
        if self.exit_status is None:
            return "running"
        else:
            return "terminated"
    
    state = property(_get_state)


class ProcessGroupDict (DataDict):
    """Default container for process groups.
    
    Keyed by process group id.
    
    When instantiating the class, be sure to explicitly set the item_cls attribute.
    """
    
    item_cls = None
    key = "id"
    
    def __init__ (self):
        self.id_gen = IncrID()
 
    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if spec.get("id", "*") != "*":
                raise DataCreationError("cannot specify an id")
            spec['id'] = self.id_gen.next()
        return DataDict.q_add(self, specs)


class BGBaseSystem (Component):
    """base system class.
    
    Methods:
    add_partitions -- tell the system to manage partitions (exposed, query)
    get_partitions -- retrieve partitions in the simulator (exposed, query)
    del_partitions -- tell the system not to manage partitions (exposed, query)
    set_partitions -- change random attributes of partitions (exposed, query)
    update_relatives -- should be called when partitions are added and removed from the managed list
    """
    
    def __init__ (self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self._partitions = PartitionDict()
        self._managed_partitions = sets.Set()
        self.process_groups = ProcessGroupDict()
        self.node_card_cache = dict()
        self._partitions_lock = thread.allocate_lock()
        self.pending_diags = dict()
        self.failed_diags = list()

    def _get_partitions (self):
        return PartitionDict([
            (partition.name, partition) for partition in self._partitions.itervalues()
            if partition.name in self._managed_partitions
        ])
    
    partitions = property(_get_partitions)

    def add_partitions (self, specs):
        self.logger.info("add_partitions(%r)" % (specs))
        specs = [{'name':spec.get("name")} for spec in specs]
        
        self._partitions_lock.acquire()
        partitions = [
            partition for partition in self._partitions.q_get(specs)
            if partition.name not in self._managed_partitions
        ]
        self._partitions_lock.release()
        
        self._managed_partitions.update([
            partition.name for partition in partitions
        ])
        self.update_relatives()
        return partitions
    add_partition = exposed(query(add_partitions))

    def get_partitions (self, specs):
        """Query partitions on simulator."""
        self._partitions_lock.acquire()
        partitions = self.partitions.q_get(specs)
        self._partitions_lock.release()
        
        return partitions
    get_partitions = exposed(query(get_partitions))

    def del_partitions (self, specs):
        """Remove partitions from the list of managed partitions"""
        self.logger.info("del_partitions(%r)" % (specs))
        
        self._partitions_lock.acquire()
        partitions = [
            partition for partition in self._partitions.q_get(specs)
            if partition.name in self._managed_partitions
        ]
        self._partitions_lock.release()
        
        self._managed_partitions -= sets.Set( [partition.name for partition in partitions] )
        self.update_relatives()
        return partitions
    del_partitions = exposed(query(del_partitions))

    def set_partitions (self, specs, updates):
        """Update random attributes on matching partitions"""
        def _set_partitions(part, newattr):
            self.logger.info("updating partition %s: %r" % (part.name, newattr))
            part.update(newattr)
            
        self._partitions_lock.acquire()
        partitions = self._partitions.q_get(specs, _set_partitions, updates)
        self._partitions_lock.release()
        return partitions
    set_partitions = exposed(query(set_partitions))

    def update_relatives(self):
        """Call this method after changing the contents of self._managed_partitions"""
        for p_name in self._managed_partitions:
            self._partitions[p_name]._parents = sets.Set()
            self._partitions[p_name]._children = sets.Set()

        for p_name in self._managed_partitions:
            p = self._partitions[p_name]
            
            # toss the wiring dependencies in with the parents
            for dep_name in p._wiring_conflicts:
                if dep_name in self._managed_partitions:
                    p._parents.add(self._partitions[dep_name])
            
            for other_name in self._managed_partitions:
                if p.name == other_name:
                    break

                other = self._partitions[other_name]
                p_set = sets.Set(p.node_cards)
                other_set = sets.Set(other.node_cards)

                # if p is a subset of other, then p is a child
                if p_set.intersection(other_set)==p_set:
                    p._parents.add(other)
                    other._children.add(p)
                # if p contains other, then p is a parent
                elif p_set.union(other_set)==p_set:
                    p._children.add(other)
                    other._parents.add(p)


    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}
        
        max_nodes = max([int(p.size) for p in self._partitions.values()])
        try:
            sys_type = CP.get('cqm', 'bgtype')
        except:
            sys_type = 'bgl'
        if sys_type == 'bgp':
            job_types = ['smp', 'dual', 'vn', 'script']
        else:
            job_types = ['co', 'vn', 'script']
        try:
            spec['nodecount'] = int(spec['nodecount'])
        except:
            raise JobValidationError("Non-integer node count")
        if not 0 < spec['nodecount'] <= max_nodes:
            raise JobValidationError("Node count out of realistic range")
        if float(spec['time']) < 5:
            raise JobValidationError("Walltime less than minimum")
        if not spec['mode']:
            if sys_type == 'bgp':
                spec['mode'] = 'smp'
            else:
                spec['mode'] = 'co'
        if spec['mode'] not in job_types:
            raise JobValidationError("Invalid mode")
        if not spec['proccount']:
            if spec.get('mode', 'co') == 'vn':
                if sys_type == 'bgl':
                    spec['proccount'] = str(2 * int(spec['nodecount']))
                elif sys_type == 'bgp':
                    spec['proccount'] = str(4 * int(spec['nodecount']))
                else:
                    self.logger.error("Unknown bgtype %s" % (sys_type))
            if spec.get('mode', 'co') == 'dual':
                spec['proccount'] = 2 * int(spec['nodecount'])
            else:
                spec['proccount'] = spec['nodecount']
        else:
            try:
                spec['proccount'] = int(spec['proccount'])
            except:
                JobValidationError("non-integer proccount")
            if spec['proccount'] < 1:
                raise JobValidationError("negative proccount")
            if spec['proccount'] > spec['nodecount']:
                if spec['mode'] not in ['vn', 'dual']:
                    raise JobValidationError("proccount too large")
                if sys_type == 'bgl' and (spec['proccount'] > (2 * spec['nodecount'])):
                    raise JobValidationError("proccount too large")
                elif sys_type == ' bgp'and (spec['proccount'] > (4 * spec['nodecount'])):
                    raise JobValidationError("proccount too large")
        # need to handle kernel
        return spec
    validate_job = exposed(validate_job)
        
    def run_diags(self, partition_list, test_name):
        def size_cmp(left, right):
            return -cmp(left.size, right.size)
        
        def _find_covering(partition):
            kids = [ self._partitions[c_name] for c_name in partition.children]
            kids.sort(size_cmp)
            n = len(kids)
            part_node_cards = sets.Set(partition.node_cards)
            # generate the power set, but try to use the big partitions first (hence the sort above)
            for i in range(1, 2**n + 1):
                test_cover = [ kids[j] for j in range(n) if i & 2**j ]
                
                test_node_cards = sets.Set()
                for t in test_cover:
                    test_node_cards.update(t.node_cards)
                
                if test_node_cards.issubset(part_node_cards) and test_node_cards.issuperset(part_node_cards):
                    return test_cover
                
            return []

        def _run_diags(partition):
            covering = _find_covering(partition)
            for child in covering:
                self.pending_diags[child] = test_name
            return [child.name for child in covering]

        results = []
        for partition_name in partition_list:
            p = self._partitions[partition_name]
            results.append(_run_diags(p))
        
        return results
    run_diags = exposed(run_diags)
    
    def launch_diags(self, partition, test_name):
        '''override this method in derived classes!'''
        pass
    
    def finish_diags(self, partition, test_name, exit_value):
        '''call this method somewhere in your derived class where you deal with the exit values of diags'''
        if exit_value == 0:
            for dead in self.failed_diags[:]:
                if dead == partition.name or dead in partition.children:
                    self.failed_diags.remove(dead)
                    self.logger.info("removing %s from failed_diags list" % dead)
        else:
            if partition.children:
                self.run_diags([partition.name], test_name)
            else:
                self.failed_diags.append(partition.name)
                self.logger.info("adding %s to failed_diags list" % partition.name)
    
    def handle_pending_diags(self):
        for p in self.pending_diags.keys():
            if p.state in ["idle", "blocked by pending diags", "failed diags", "blocked by failed diags"]:
                self.logger.info("launching diagnostics on %s" % p.name)
                self.launch_diags(p, self.pending_diags[p])
                del self.pending_diags[p]
                
    handle_pending_diags = automatic(handle_pending_diags)
    
    def fail_partitions(self, specs):
        parts = self.get_partitions(specs)
        if not parts:
            ret = "no matching partitions found\n"
        else:
            ret = ""
        for p in parts:
            if self.failed_diags.count(p.name) == 0:
                ret += "failing %s\n" % p.name
                self.failed_diags.append(p.name)
            else:
                ret += "%s is already marked as failing\n" % p.name

        return ret
    fail_partitions = exposed(fail_partitions)
    
    def unfail_partitions(self, specs):
        parts = self.get_partitions(specs)
        if not parts:
            ret = "no matching partitions found\n"
        else:
            ret = ""
        for p in self.get_partitions(specs):
            if self.failed_diags.count(p.name):
                ret += "unfailing %s\n" % p.name
                self.failed_diags.remove(p.name)
            else:
                ret += "%s is not currently failing\n" % p.name
        
        return ret
    unfail_partitions = exposed(unfail_partitions)
    
