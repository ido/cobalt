"""Hardware abstraction layer for the system on which process groups are run.

Classes:
NodeCard -- node cards make up Partitions
Partition -- atomic set of nodes
PartitionDict -- default container for partitions
ProcessGroup -- virtual process group running on the system
ProcessGroupDict -- default container for process groups
BGBaseSystem -- base system component
"""

from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError
from Cobalt.Components.base import Component, exposed, automatic, query
import sets
import thread

__all__ = [
    "NodeCard",
    "Partition",
    "PartitionDict",
    "ProcessGroup",
    "ProcessGroupDict", 
    "BGBaseSystem",
]

class NodeCard (object):
    """node cards make up Partitions"""
    def __init__(self, name):
        self.id = name
        self.used_by = ''
        
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
