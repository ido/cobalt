"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ProcessGroup -- virtual process group running on the system
ProcessGroupDict -- default container for process groups
ClusterBaseSystem -- base system component
"""

import sys
import time
import Cobalt
from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Exceptions import DataCreationError, JobValidationError
from Cobalt.Components.base import Component, exposed, automatic, query
import sets, thread, ConfigParser

__all__ = [
    "ProcessGroup",
    "ProcessGroupDict", 
    "ClusterBaseSystem",
]

CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)


class ProcessGroup (Data):
    required_fields = ['user', 'executable', 'args', 'location', 'size', 'cwd']
    fields = Data.fields + [
        "id", "user", "size", "cwd", "executable", "env", "args", "location",
        "head_pid", "stdin", "stdout", "stderr", "exit_status", "state",
        "mode", "kerneloptions", "true_mpi_args", "jobid",
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
        self.jobid = spec.get('jobid')

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


class ClusterBaseSystem (Component):
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
        self.process_groups = ProcessGroupDict()
        self.pending_diags = dict()
        self.failed_diags = list()
        self.all_nodes = sets.Set()
        self.running_nodes = sets.Set()
        self.down_nodes = sets.Set()
        self.queue_assignments = {}
        self.config_file = kwargs.get("config_file", None)
        if self.config_file is not None:
            self.configure(self.config_file)
        self.queue_assignments["default"] = sets.Set(self.all_nodes)



    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}
        
        max_nodes = len(self.all_nodes)
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

        if required:
            available_nodes = sets.Set(required)
        else:
            available_nodes = self.queue_assignments[queue].difference(forbidden)

        available_nodes = available_nodes.difference(self.running_nodes)
        available_nodes = available_nodes.difference(self.down_nodes)

            
        if nodes <= len(available_nodes):
            return {jobid: [available_nodes.pop() for i in range(nodes)]}
        else:
            return None

    
    # the argument "required" is used to pass in the set of locations allowed by a reservation;
    def find_job_location(self, arg_list, utility_cutoff, backfill_cutoff):
        best_location_dict = {}
        
        # first time through, try for starting jobs based on utility scores
        for args in arg_list:
            if args['utility_score'] < utility_cutoff:
                break
            
            location_data = self._find_job_location(args)
            if location_data:
                best_location_dict.update(location_data)
                break
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_location_dict:
            arg_list.sort(self._walltimecmp)
            for args in arg_list:
                if 60*float(args['walltime']) > backfill_cutoff:
                    break
                
                location_data = self._find_job_location(args)
                if location_data:
                    best_location_dict.update(location_data)
                    break

        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
        for location_list in best_location_dict.itervalues():
            self.running_nodes.update(location_list)

        print "best_location_dict:", best_location_dict
            
        return best_location_dict
    find_job_location = exposed(find_job_location)
    
    def _walltimecmp(self, dict1, dict2):
        return -cmp(float(dict1['walltime']), float(dict2['walltime']))


    def find_queue_equivalence_classes(self, reservation_dict):
        equiv = []
        for q in self.queue_assignments:
            found_a_match = False
            for e in equiv:
                if e['data'].intersection(self.queue_assignments[q]):
                    e['queues'].add(q)
                    e['data'].update(self.queue_assignments[q])
                    found_a_match = True
                    break
            if not found_a_match:
                equiv.append( { 'queues': set([q]), 'data': set(self.queue_assignments[q]), 'reservations': set() } )
        
        
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
                for host_name in reservation_dict[res_name].split(":"):
                    if host_name in eq_class['data']:
                        eq_class['reservations'].add(res_name)

            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
    
    

    def reserve_partition_until(self, partition_name, time):
        try:
            self.partitions[partition_name].reserved_until = time
        except:
            self.logger.error("failed to reserve partition '%s' until '%s'" % (partition_name, time))
    reserve_partition_until = exposed(reserve_partition_until)


    def nodes_up(self, node_list):
        changed = []
        for n in node_list:
            if n in self.down_nodes:
                self.down_nodes.remove(n)
                changed.append(n)
            if n in self.running_nodes:
                self.running_nodes.remove(n)
                changed.append(n)
        return changed
    nodes_up = exposed(nodes_up)
        

    def nodes_down(self, node_list):
        changed = []
        for n in node_list:
            if n in self.all_nodes:
                self.down_nodes.add(n)
                changed.append(n)
        return changed
    nodes_down = exposed(nodes_down)

    def get_node_status(self):
        status = {}
        for n in self.all_nodes:
            if n in self.running_nodes:
                status[n] = "allocated"
            elif n in self.down_nodes:
                status[n] = "down"
            else:
                status[n] = "idle"
        return status
    get_node_status = exposed(get_node_status)

    def get_queue_assignments(self):
        ret = {}
        for q in self.queue_assignments:
            ret[q] = list(self.queue_assignments[q])
        return ret
    get_queue_assignments = exposed(get_queue_assignments)
    
    def set_queue_assignments(self, queue_names, node_list):
        checked_nodes = sets.Set()
        for n in node_list:
            if n in self.all_nodes:
                checked_nodes.add(n)
        
        queue_list = queue_names.split(":")
        for q in queue_list:
            if q not in self.queue_assignments:
                self.queue_assignments[q] = sets.Set()
                
        for q in self.queue_assignments.keys():
            if q not in queue_list:
                self.queue_assignments[q].difference_update(checked_nodes)
                if len(self.queue_assignments[q])==0:
                    del self.queue_assignments[q]
            else:
                self.queue_assignments[q].update(checked_nodes)
        return list(checked_nodes)
    set_queue_assignments = exposed(set_queue_assignments)

    def verify_locations(self, location_list):
        """Providing a system agnostic interface for making sure a 'location string' is valid"""
        ret = []
        for l in location_list:
            if l in self.all_nodes:
                ret.append(l)
        return ret
    verify_locations = exposed(verify_locations)

    def configure(self, filename):
        f = open(filename)
        
        for line in f:
            self.all_nodes.add(line.strip())
        
        f.close()
    
