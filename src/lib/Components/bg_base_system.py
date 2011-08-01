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
import copy
import re
import Cobalt
from Cobalt.Data import Data, DataDict
from Cobalt.Exceptions import JobValidationError, ComponentLookupError
from Cobalt.Components.base import Component, exposed, automatic, query, locking
import thread, ConfigParser
from Cobalt.Proxy import ComponentProxy
from Cobalt.DataTypes.ProcessGroup import ProcessGroupDict


__all__ = [
    "NodeCard",
    "Partition",
    "PartitionDict",
    "BGBaseSystem",
]

CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)

try:
    max_drain_hours = float(CP.get('bgsystem', 'max_drain_hours'))
except:
    max_drain_hours = float(sys.maxint)
    
# *AdjEst*
config = ConfigParser.ConfigParser() 
config.read(Cobalt.CONFIG_FILES)
def get_histm_config(option, default):
    try:
        value = config.get('histm', option)
    except ConfigParser.NoSectionError:
        value = default
    return value
walltime_prediction = get_histm_config("walltime_prediction", "False").lower()
if walltime_prediction  == "true":
    walltime_prediction_enabled = True
else:
    walltime_prediction_enabled = False
# *AdjEst*

def parse_nodecard_location(name):
    '''convert a location string to a R,M,N tuple
    must have up to nodecard information in name.

    '''
    parser = re.compile(r'R(?P<rack>[0-9]{2})-M(?P<midplane>[0-9])-N(?P<nodecard>[0-9]{2})')
    match = parser.search(name)
    if match == None:
        raise RuntimeError("%s caused a parser error!"% name)
    return match.groups()
    

class NodeCard (object):
    """node cards make up Partitions
    
        useful members:
        id - Nodecard location, according to the control system (RXX-MY-NZZ)
        used_by - Name of <something> using a particular nodecard
        state - state of the nodecard (like RM_NODECARD_UP)
        rack - rack location
        midplane - midplane location in rack
        nodecard - nodecard location in midplane

        __eq__ - nodecards are equal if their id's are equal
        
    """
    def __init__(self, name, state="RM_NODECARD_UP"):
        self.id = name
        self.used_by = ''
        self.state = ''
        self.set_physical_location(name)

    def __eq__(self, other):
        return self.id == other.id

    def set_physical_location(self, name):
        try:
            rack, midplane, nodecard = parse_nodecard_location(name)
        except RuntimeError:
            self.rack = 0
            self.midplane = 0
            self.nodecard = 0
            return
        self.rack = int(rack)
        self.midplane = int(midplane)
        self.nodecard = int(nodecard)
        return
    

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
        "backfill_time",
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
        self._parents = set()
        self._children = set()
        self._all_children = set()
        self.state = spec.pop("state", "idle")
        self.tag = spec.get("tag", "partition")
        self.bridge_partition = None
        self.node_cards = spec.get("node_cards", [])
        self.switches = spec.get("switches", [])
        self.reserved_until = False
        self.reserved_by = None
        self.used_by = None
        self.cleanup_pending = False

        # this holds partition names
        self._wiring_conflicts = set()
        self.backfill_time = None
        self.draining = False

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
    
    def _get_all_children (self):
        return [child.name for child in self._all_children]
    
    all_children = property(_get_all_children)
    
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



class BGProcessGroupDict(ProcessGroupDict):
    """ProcessGroupDict modified for Blue Gene systems"""

    def __init__(self):
        ProcessGroupDict.__init__(self)

    def find_by_jobid(self, jobid):
        """Find process groups by jobid"""
        for id, pg in self.iteritems():
            if pg.jobid == jobid:
                return pg
        return None



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
        self._managed_partitions = set()
        self.process_groups = BGProcessGroupDict()
        self.node_card_cache = dict()
        self._partitions_lock = thread.allocate_lock()
        self.pending_diags = dict()
        self.failed_diags = list()
        self.bridge_in_error = False
        self.cached_partitions = None
        self.offline_partitions = []

    def _get_partitions (self):
        return PartitionDict([
            (partition.name, partition) for partition in self._partitions.itervalues()
            if partition.name in self._managed_partitions
        ])
    
    partitions = property(_get_partitions)

    def add_partitions (self, specs, user_name=None):
        self.logger.info("%s called add_partitions(%r)", user_name, specs)
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

    def del_partitions (self, specs, user_name=None):
        """Remove partitions from the list of managed partitions"""
        self.logger.info("%s called del_partitions(%r)", user_name, specs)
        
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
        
        self._managed_partitions -= set( [partition.name for partition in partitions] )
        self.update_relatives()
        return partitions
    del_partitions = exposed(query(del_partitions))

    def set_partitions (self, specs, updates, user_name=None):
        """Update random attributes on matching partitions"""
        def _set_partitions(part, newattr):
            self.logger.info("%s updating partition %s: %r", user_name, part.name, newattr)
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
            self._partitions[p_name]._parents = set()
            self._partitions[p_name]._children = set()

        for p in self._partitions.itervalues():
            p._all_children = set()

        for p_name in self._managed_partitions:
            p = self._partitions[p_name]
            

            # toss the wiring dependencies in with the parents
            for dep_name in p._wiring_conflicts:
                if dep_name in self._managed_partitions:
                    p._parents.add(self._partitions[dep_name])
            
            for other in self._partitions.itervalues():
                if p.name == other.name:
                    continue

                p_set = set(p.node_cards)
                other_set = set(other.node_cards)
                
               
                if p.size == 16 and other.size == 16 and len(p_set ^ other_set) == 0:
                    continue

                if other.name in self._managed_partitions:
                    # if p is a subset of other, then p is a child; add other to p's list of managed parent partitions, and p to
                    # other's list of managed child partitions
                    if p_set.intersection(other_set)==p_set:
                        if p.size < other.size:
                            p._parents.add(other)
                            other._children.add(p)
                    # if p contains other, then p is a parent; add other to p's list of managed child partitions and p to other's
                    # list of managed parent partitions
                    elif p_set.union(other_set)==p_set:
                        if p.size > other.size:
                            p._children.add(other)
                            other._parents.add(p)

                # if p contains other, then p is a parent; add other to p's list of all child partitions
                if p_set.union(other_set)==p_set:
                    if p.size > other.size:
                        p._all_children.add(other)

        #Let's get the wiring conflicts for direct childeren as well, 
        #we shouldn't be able to run on these either. --PMR
        for p_name in self._managed_partitions:

            p = self._partitions[p_name]
            for child in p._children:
                for dep_name in child._wiring_conflicts:
                    if dep_name in self._managed_partitions:        
                        p._parents.add(self._partitions[dep_name])
                #we shouldn't be scheduling on the parents of our children either
                for par in child._parents:
                    if ((par.name != p_name) and
                        (par.name in self._managed_partitions)):
                        p._parents.add(self._partitions[par.name])
                    
    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}
        
        max_nodes = max([int(p.size) for p in self._partitions.values()])
        try:
            sys_type = CP.get('bgsystem', 'bgtype')
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
        if spec['attrs'].has_key("location"):
            p_name = spec['attrs']['location']
            if not self.partitions.has_key(p_name):
                raise JobValidationError("Partition %s not found" % p_name)
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
        
    def run_diags(self, partition_list, test_name, user_name=None):
        self.logger.info("%s running diags %s on partitions %s", user_name, test_name, partition_list)
        def size_cmp(left, right):
            return -cmp(left.size, right.size)
        
        def _find_covering(partition):
            kids = [ self._partitions[c_name] for c_name in partition.children]
            kids.sort(size_cmp)
            n = len(kids)
            part_node_cards = set(partition.node_cards)
            # generate the power set, but try to use the big partitions first (hence the sort above)
            for i in xrange(1, 2**n + 1):
                test_cover = [ kids[j] for j in range(n) if i & 2**j ]
                
                test_node_cards = set()
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
    
    def fail_partitions(self, specs, user_name=None):
        self.logger.info("%s failing partition %s", user_name, specs)
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
    
    def unfail_partitions(self, specs, user_name=None):
        self.logger.info("%s unfailing partition %s", user_name, specs)
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
    
    def _find_job_location(self, args, drain_partitions=set(), backfilling=False):
        jobid = args['jobid']
        nodes = args['nodes']
        queue = args['queue']
        utility_score = args['utility_score']
        walltime = args['walltime']
        walltime_p = args.get('walltime_p', walltime)  #*AdjEst* 
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])
        
        if walltime_prediction_enabled:  # *Adj_Est*
            runtime_estimate = float(walltime_p)  
        else:
            runtime_estimate = float(walltime)
        
        best_score = sys.maxint
        best_partition = None
        
        available_partitions = set()
        
        requested_location = None
        if args['attrs'].has_key("location"):
            requested_location = args['attrs']['location']
                
        if required:
            # whittle down the list of required partitions to the ones of the proper size
            # this is a lot like the stuff in _build_locations_cache, but unfortunately, 
            # reservation queues aren't assigned like real queues, so that code doesn't find
            # these
            for p_name in required:
                available_partitions.add(self.cached_partitions[p_name])
                available_partitions.update(self.cached_partitions[p_name]._children)

            possible = set()
            for p in available_partitions:            
                possible.add(p.size)
                
            desired_size = 0
            job_nodes = int(nodes)
            for psize in sorted(possible):
                if psize >= job_nodes:
                    desired_size = psize
                    break
            
            for p in available_partitions.copy():
                if p.size != desired_size:
                    available_partitions.remove(p)
                elif p.name in self._not_functional_set:
                    available_partitions.remove(p)
                elif requested_location and p.name != requested_location:
                    available_partitions.remove(p)
        else:
            for p in self.possible_locations(nodes, queue):
                skip = False
                for bad_name in forbidden:
                    if p.name==bad_name or bad_name in p.children or bad_name in p.parents:
                        skip = True
                        break
                if not skip:
                    if (not requested_location) or (p.name == requested_location):
                        available_partitions.add(p)
        
        available_partitions -= drain_partitions
        now = time.time()
        
        for partition in available_partitions:
            # if the job needs more time than the partition currently has available, look elsewhere    
            if backfilling: 
                               
                if partition.reserved_by:
                    #if the partition is reserved, we don't use predicted walltime to backfill
                    runtime_estimate = float(walltime)
                
                if 60 * runtime_estimate > (partition.backfill_time - now):      # *Adj_Est*
                    continue
                
                if 60*float(walltime) > (partition.backfill_time - now):
                    continue
                
            if partition.state == "idle":
                # let's check the impact on partitions that would become blocked
                score = 0
                for p in partition.parents:
                    if self.cached_partitions[p].state == "idle" and self.cached_partitions[p].scheduled:
                        score += 1
                
                # the lower the score, the fewer new partitions will be blocked by this selection
                if score < best_score:
                    best_score = score
                    best_partition = partition        

        if best_partition:
            return {jobid: [best_partition.name]}


    def _find_drain_partition(self, job):
        # if the user requested a particular partition, we only try to drain that one
        if job['attrs'].has_key("location"):
            target_name = job['attrs']['location']
            return self.cached_partitions.get(target_name, None)
        
        drain_partition = None
        locations = self.possible_locations(job['nodes'], job['queue'])
        
        for p in locations:
            if not drain_partition:
                drain_partition = p
            else:
                if p.backfill_time < drain_partition.backfill_time:
                    drain_partition = p
        
        if drain_partition:
            # don't try to drain for an entire weekend 
            hours = (drain_partition.backfill_time - time.time()) / 3600.0
            if hours > max_drain_hours:
                drain_partition = None

        return drain_partition


    def possible_locations(self, job_nodes, q_name):
        desired_size = 0
        job_nodes = int(job_nodes)
        if self._defined_sizes.has_key(q_name):
            for psize in self._defined_sizes[q_name]:
                if psize >= job_nodes:
                    desired_size = psize
                    break

        if self._locations_cache.has_key(q_name):
            return self._locations_cache[q_name].get(desired_size, [])
        else:
            return []

    # this function builds three things, namely a pair of dictionaries keyed by queue names, and a set of 
    # partition names which are not functional
    #
    # self._defined_sizes maps queue names to an ordered list of partition sizes available in that queue
    #     for all schedulable partitions (even if currently offline and not functional)
    # self._locations_cache maps queue names to dictionaries which map partition sizes to partition objects;
    #     this structure will only contain partitions which are fully online, so we don't try to drain a
    #     broken partition
    # self._not_functional_set contains names of partitions which are not functional (either themselves, or
    #     a parent or child) 
    def _build_locations_cache(self):
        per_queue = {}
        defined_sizes = {}
        not_functional_set = set()
        for target_partition in self.cached_partitions.itervalues():
            usable = True
            if target_partition.name in self.offline_partitions:
                usable = False
            else:
                for part in self.cached_partitions.itervalues():
                    if not part.functional:
                        not_functional_set.add(part.name)
                        if target_partition.name in part.children or target_partition.name in part.parents:
                            usable = False
                            not_functional_set.add(target_partition.name)
                            break

            for queue_name in target_partition.queue.split(":"):
                if not per_queue.has_key(queue_name):
                    per_queue[queue_name] = {}
                if not defined_sizes.has_key(queue_name):
                    defined_sizes[queue_name] = set()
                if target_partition.scheduled:
                    defined_sizes[queue_name].add(target_partition.size)
                if target_partition.scheduled and target_partition.functional and usable:
                    if not per_queue[queue_name].has_key(target_partition.size):
                        per_queue[queue_name][target_partition.size] = []
                    per_queue[queue_name][target_partition.size].append(target_partition)
        
        for q_name in defined_sizes:
            defined_sizes[q_name] = sorted(defined_sizes[q_name])
        
        self._defined_sizes = defined_sizes
        self._locations_cache = per_queue
        self._not_functional_set = not_functional_set
    
    def find_job_location(self, arg_list, end_times):
        best_partition_dict = {}
        
        if self.bridge_in_error:
            return {}
        
        self._partitions_lock.acquire()
        try:
            self.cached_partitions = copy.deepcopy(self.partitions)
        except:
            self.logger.error("error in copy.deepcopy", exc_info=True)
            return {}
        finally:
            self._partitions_lock.release()

        # build the cached_partitions structure first
        self._build_locations_cache()

            
        # first, figure out backfilling cutoffs per partition (which we'll also use for picking which partition to drain)
        job_end_times = {}
        for item in end_times:
            job_end_times[item[0][0]] = item[1]
            
        now = time.time()
        for p in self.cached_partitions.itervalues():
            if p.state == "idle":
                p.backfill_time = now
            else:
                p.backfill_time = now + 5*60
            p.draining = False
        
        for p in self.cached_partitions.itervalues():    
            if p.name in job_end_times:
                if job_end_times[p.name] > p.backfill_time:
                    p.backfill_time = job_end_times[p.name]
                
                for parent_name in p.parents:
                    parent_partition = self.cached_partitions[parent_name]
                    if p.backfill_time > parent_partition.backfill_time:
                        parent_partition.backfill_time = p.backfill_time
        
        for p in self.cached_partitions.itervalues():
            if p.backfill_time == now:
                continue
            
            for child_name in p.children:
                child_partition = self.cached_partitions[child_name]
                if child_partition.backfill_time == now or child_partition.backfill_time > p.backfill_time:
                    child_partition.backfill_time = p.backfill_time

        
        # first time through, try for starting jobs based on utility scores
        drain_partitions = set()
        
        for job in arg_list:
            partition_name = self._find_job_location(job, drain_partitions)
            if partition_name:
                best_partition_dict.update(partition_name)
                break
            
            location = self._find_drain_partition(job)
            if location is not None:
                for p_name in location.parents:
                    drain_partitions.add(self.cached_partitions[p_name])
                for p_name in location.children:
                    drain_partitions.add(self.cached_partitions[p_name])
                    self.cached_partitions[p_name].draining = True
                drain_partitions.add(location)
                #self.logger.info("job %s is draining %s" % (winning_job['jobid'], location.name))
                location.draining = True
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_partition_dict:
            
            # arg_list.sort(self._walltimecmp)

            for args in arg_list:
                partition_name = self._find_job_location(args, backfilling=True)
                if partition_name:
                    self.logger.info("backfilling job %s" % args['jobid'])
                    best_partition_dict.update(partition_name)
                    break

        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
        #
        # also, this is the only part of finding a job location where we need to lock anything
        self._partitions_lock.acquire()
        try:
            for p in self.partitions.itervalues():
                # push the backfilling info from the local cache back to the real objects
                p.draining = self.cached_partitions[p.name].draining
                p.backfill_time = self.cached_partitions[p.name].backfill_time
                
            for jobid, partition_list in best_partition_dict.iteritems():
                part = self.partitions[partition_list[0]]
                # FIXME: use reserve_resources_until() here? --brt
                part.used_by = int(jobid)
                part.reserved_until = time.time() + 5*60
                part.state = "allocated"
                print "parents:"
                for p in part._parents:
                    if p.state == "idle":
                        p.state = "blocked (%s)" % (part.name,)
                print "children:"
                for p in part._children:
                    if p.state == "idle":
                        p.state = "blocked (%s)" % (part.name,)
        except:
            self.logger.error("error in find_job_location", exc_info=True)
        self._partitions_lock.release()
        
        return best_partition_dict
    find_job_location = locking(exposed(find_job_location))
    
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
                        if self.partitions.has_key(dep_name):
                            if eq_class['data'].intersection(self.partitions[dep_name].node_card_names):
                                eq_class['reservations'].add(res_name)
                                break

            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
    
    
    def can_run(self, target_partition, node_count, partition_dict):
        if target_partition.state != "idle":
            return False
        desired = sys.maxint
        for part in partition_dict.itervalues():
            if not part.functional:
                if target_partition.name in part.children or target_partition.name in part.parents:
                    return False
            else:
                if part.scheduled:
                    if int(node_count) <= int(part.size) < desired:
                        desired = int(part.size)
        return target_partition.scheduled and target_partition.functional and int(target_partition.size) == desired

    def reserve_resources_until(self, location, new_time, jobid):
        rc = False
        partition_name = location[0]
        pg = self.process_groups.find_by_jobid(jobid)
        try:
            self._partitions_lock.acquire()
            used_by = self.partitions[partition_name].used_by
            if used_by == None:
                self.partitions[partition_name].used_by = jobid
                used_by = jobid
            if new_time:
                if used_by == jobid:
                    self.partitions[partition_name].reserved_until = new_time
                    self.partitions[partition_name].reserved_by = jobid
                    self.logger.info("job %s: partition '%s' now reserved until %s", jobid, partition_name,
                        time.asctime(time.gmtime(new_time)))
                    rc = True
                else:
                    self.logger.error("job %s wasn't allowed to update the reservation on partition %s (owner=%s)",
                        jobid, partition_name, used_by)
            else:
                if used_by == jobid:
                    self.partitions[partition_name].reserved_until = False
                    self.partitions[partition_name].reserved_by = None
                    self.logger.info("reservation on partition '%s' has been removed", partition_name)
                    rc = True
                else:
                    self.logger.error("job %s wasn't allowed to clear the reservation on partition %s (owner=%s)",
                        jobid, partition_name, used_by)
        except:
            self.logger.exception("an unexpected error occurred will adjusting the partition reservation time")
        finally:
            self._partitions_lock.release()
        return rc
    reserve_resources_until = exposed(reserve_resources_until)

    # # yarrrrr!   deadlock ho!!
    # # making more than one RPC call in the same atomic method is a recipe for disaster
    # # maybe i need a second automatic method to do the waiting?
    # def sm_sync(self):
    #     '''Resynchronize with the script manager'''
    #     # get this cache first -- it's no problem if this data is old, but bad things
    #     # happen when this data is newer than the list of running processes in scriptm
    #     self.lock.acquire()
    #     try:
    #         process_groups_cache = self.process_groups.values()
    #     except:
    #         self.logger.error("error copying process_groups.values()", exc_info=True)
    #     self.lock.release()
    # 
    #     try:
    #         pgroups = ComponentProxy("script-manager").get_jobs([{'id':'*', 'state':'running'}])
    #     except (ComponentLookupError, xmlrpclib.Fault):
    #         self.logger.error("Failed to communicate with script manager")
    #         return
    #     live = [item['id'] for item in pgroups]
    #     
    #     for each in process_groups_cache:
    #         if each.mode == 'script' and each.script_id not in live:
    #             self.logger.info("Found dead pg for script job %s" % (each.script_id))
    #             result = ComponentProxy("script-manager").wait_jobs([{'id':each.script_id, 'exit_status':'*'}])
    #             self.logger.info("wait returned %r" % result)
    #             for r in result:
    #                 which_one = None
    #                 if r['id'] == each.script_id:
    #                     each.exit_status = r['exit_status']
    #                     self.reserve_resources_until(each.location, None, each.jobid)
    # 
    # sm_sync = locking(automatic(sm_sync))

