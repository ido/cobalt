"""Hardware abstraction layer for the system on which process groups are run.

Classes:
NodeCard -- node cards make up Partitions
Partition -- atomic set of nodes
PartitionDict -- default container for partitions
ProcessGroup -- virtual process group running on the system
ProcessGroupDict -- default container for process groups
BGBaseSystem -- base system component
"""

import sys
import time
import xmlrpclib
import Cobalt
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError, JobValidationError, ComponentLookupError
from Cobalt.Components.base import Component, exposed, automatic, query
import sets, thread, ConfigParser
from Cobalt.Proxy import ComponentProxy


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
        self.reserved_until = False
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
        self.cobalt_log_file = spec.get('cobalt_log_file')
        self.umask = spec.get('umask')
        self.exit_status = None
        self.script_id = None
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
        try:
            partitions = [
                partition for partition in self._partitions.q_get(specs)
                if partition.name not in self._managed_partitions
            ]
        except:
            partitions = []
            self.logger.error("error in add_partitions", exc_info=True)
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
        try:
            partitions = self.partitions.q_get(specs)
        except:
            partitions = []
            self.logger.error("error in get_partitions", exc_info=True)
        self._partitions_lock.release()
        
        return partitions
    get_partitions = exposed(query(get_partitions))
    
    def verify_locations(self, location_list):
        """Providing a system agnostic interface for making sure a 'location string' is valid"""
        parts = self.get_partitions([{'name':l} for l in location_list])
        return [ p.name for p in parts ]
    verify_locations = exposed(verify_locations)

    def del_partitions (self, specs):
        """Remove partitions from the list of managed partitions"""
        self.logger.info("del_partitions(%r)" % (specs))
        
        self._partitions_lock.acquire()
        try:
            partitions = [
                partition for partition in self._partitions.q_get(specs)
                if partition.name in self._managed_partitions
            ]
        except:
            partitions = []
            self.logger.error("error in del_partitions", exc_info=True)
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
        try:
            partitions = self._partitions.q_get(specs, _set_partitions, updates)
        except:
            partitions = []
            self.logger.error("error in set_partitions", exc_info=True)
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
            elif spec.get('mode', 'co') == 'dual':
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
            for i in xrange(1, 2**n + 1):
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
    
    def _find_job_location(self, args):
        jobid = args['jobid']
        nodes = args['nodes']
        queue = args['queue']
        utility_score = args['utility_score']
        walltime = args['walltime']
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])
        
        best_score = sys.maxint
        best_partition = None
        
        available_partitions = set()
        if required:
            for p_name in required:
                available_partitions.add(self.partitions[p_name])
                available_partitions.update(self.partitions[p_name]._children)
        else:
            for p in self.partitions.itervalues():
                skip = False
                for bad_name in forbidden:
                    if p.name==bad_name or bad_name in p.children or bad_name in p.parents:
                        skip = True
                        break
                if not skip:
                    available_partitions.add(p)
                
        for partition in available_partitions:
            # check if the current partition is linked to the job's queue (but if reservation locations were
            # passed in via the "required" argument, then we know it's all good)
            if not required and queue not in partition.queue.split(':'):
                continue
                
            if self.can_run(partition, nodes):
                # let's check the impact on partitions that would become blocked
                score = 0
                for p in partition.parents:
                    if self.partitions[p].state == "idle" and self.partitions[p].scheduled:
                        score += 1
                
                # the lower the score, the fewer new partitions will be blocked by this selection
                if score < best_score:
                    best_score = score
                    best_partition = partition        

        if best_partition:
            return {jobid: [best_partition.name]}

    
    # the argument "required" is used to pass in the set of locations allowed by a reservation;
    def find_job_location(self, arg_list, utility_cutoff, backfill_cutoff):
        best_partition_dict = {}
        
        # first time through, try for starting jobs based on utility scores
        for args in arg_list:
            if args['utility_score'] < utility_cutoff:
                break
            
            partition_name = self._find_job_location(args)
            if partition_name:
                best_partition_dict.update(partition_name)
                break
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_partition_dict:
            arg_list.sort(self._walltimecmp)
            for args in arg_list:
                if 60*float(args['walltime']) > backfill_cutoff:
                    continue
                
                partition_name = self._find_job_location(args)
                if partition_name:
                    best_partition_dict.update(partition_name)
                    break

        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
        for partition_list in best_partition_dict.itervalues():
            part = self.partitions[partition_list[0]] 
            part.reserved_until = time.time() + 5*60
            part.state = "starting job"
            for p in part._parents:
                if p.state == "idle":
                    p.state = "blocked by starting job"
            for p in part._children:
                if p.state == "idle":
                    p.state = "blocked by starting job"
            
        return best_partition_dict
    find_job_location = exposed(find_job_location)
    
    def _walltimecmp(self, dict1, dict2):
        return -cmp(float(dict1['walltime']), float(dict2['walltime']))


    def find_queue_equivalence_classes(self, reservation_dict, active_queue_names):
        equiv = []
        for part in self.partitions.itervalues():
            if part.functional and part.scheduled:
                part_active_queues = []
                for q in part.queue.split(":"):
                    if q in active_queue_names:
                        part_active_queues.append(q)

                # go on to the next partition if there are no running
                # queues using this partition
                if not part_active_queues:
                    continue
                
                found_a_match = False
                for e in equiv:
                    if e['data'].intersection(part.node_card_names):
                        e['queues'].update(part_active_queues)
                        e['data'].update(part.node_card_names)
                        found_a_match = True
                        break
                if not found_a_match:
                    equiv.append( { 'queues': set(part_active_queues), 'data': set(part.node_card_names), 'reservations': set() } ) 
        
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for e in real_equiv:
                if e['queues'].intersection(eq_class['queues']):
                    e['queues'].update(eq_class['queues'])
                    e['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)

        equiv = real_equiv
                
        for eq_class in equiv:
            for res_name in reservation_dict:
                skip = True
                for p_name in reservation_dict[res_name].split(":"):
                    p = self.partitions[p_name]
                    if eq_class['data'].intersection(p.node_card_names):
                        eq_class['reservations'].add(res_name)
                    for dep_name in p._wiring_conflicts:
                        if eq_class['data'].intersection(self.partitions[dep_name].node_card_names):
                            eq_class['reservations'].add(res_name)
                            break

            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
    
    
    def can_run(self, target_partition, node_count):
        if target_partition.state != "idle":
            return False
        desired = sys.maxint
        for part in self.partitions.itervalues():
            if not part.functional:
                if target_partition.name in part.children or target_partition.name in part.parents:
                    return False
            else:
                if part.scheduled:
                    if int(node_count) <= int(part.size) < desired:
                        desired = int(part.size)
        return target_partition.scheduled and target_partition.functional and int(target_partition.size) == desired

    def reserve_partition_until(self, partition_name, time):
        try:
            self.partitions[partition_name].reserved_until = time
        except:
            self.logger.error("failed to reserve partition '%s' until '%s'" % (partition_name, time))
    reserve_partition_until = exposed(reserve_partition_until)

    # yarrrrr!   deadlock ho!!
    # making more than one RPC call in the same atomic method is a recipe for disaster
    # maybe i need a second automatic method to do the waiting?
    def sm_sync(self):
        '''Resynchronize with the script manager'''
        print "starting sm_sync"
        try:
            pgroups = ComponentProxy("script-manager").get_jobs([{'id':'*', 'state':'running'}])
        except (ComponentLookupError, xmlrpclib.Fault):
            self.logger.error("Failed to communicate with script manager")
            return
        live = [item['id'] for item in pgroups]
        print "live:", live
        for each in self.process_groups.itervalues():
            if each.mode == 'script' and each.script_id not in live:
                self.logger.info("Found dead pg for script job %s" % (each.script_id))
                result = ComponentProxy("script-manager").wait_jobs([{'id':each.script_id, 'exit_status':'*'}])
                for r in result:
                    which_one = None
                    if r['id'] == each.script_id:
                        each.exit_status = r['exit_status']
                        self.reserve_partition_until(each.location[0], 1)

        print "ending sm_sync"
    sm_sync = automatic(sm_sync)

