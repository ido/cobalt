"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ClusterBaseSystem -- base system component
"""

import time
import sys
import Cobalt
import threading
import pwd
import grp
import ConfigParser
import Cobalt.Util
from Cobalt.Exceptions import  JobValidationError, NotSupportedError, ComponentLookupError
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.DataTypes.ProcessGroup import ProcessGroupDict
from Cobalt.Statistics import Statistics
from Cobalt.Data import DataDict
from Cobalt.Proxy import ComponentProxy

__all__ = [
    "ClusterBaseSystem",
]

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

if not config.has_section('cluster_system'):
    print '''"ERROR: cluster_system" section missing from cobalt config file'''
    sys.exit(1)

def get_cluster_system_config(option, default):
    try:
        value = config.get('cluster_system', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

cluster_hostfile = get_cluster_system_config('hostfile', None)
if cluster_hostfile == None:
    print '''ERROR: No "hostfile" entry in "cluster_system" section of cobalt config file'''
    sys.exit(1)


class ClusterNode(object):
    
    def __init__(self, name):

        self.name = name
        self.running = False
        self.down = False
        self.queues = None
        self.allocated = False
        self.cleaning = False
        self.cleaning_process = None
        self.assigned_jobid = None
        self.alloc_timeout = None
        self.alloc_start = None
        self.assigned_user = None

    def allocate(self, jobid, user, t=None):

        self.alloc_timeout = 300
        if t == None:
            self.alloc_start = time.time()
        else:
            self.alloc_start = t
        self.allocated = True
        self.assigned_user = user
        self.assigned_jobid = jobid

    def start_running(self):
        self.running = True

    def stop_running(self):

        self.running = False
        self.cleaning = True
        #invoke cleanup

    def deallocate(self):

        self.assigned_user = None
        self.assigned_jobid = None
        self.alloc_timeout = None
        self.alloc_start = None
        self.allocated = False

    def mark_up(self):
        self.down = False

    def mark_down (self):
        self.down = True

    

class ClusterNodeDict(DataDict):
    '''default container for ClusterNode information
        
       keyed by node name
    '''
    item_cls = ClusterNode
    key = "name"


class ClusterBaseSystem (Component):
    """base system class.
    
    Methods:
    add_partitions -- tell the system to manage partitions (exposed, query)
    get_partitions -- retrieve partitions in the simulator (exposed, query)
    del_partitions -- tell the system not to manage partitions (exposed, query)
    set_partitions -- change random attributes of partitions (exposed, query)
    update_relatives -- should be called when partitions are added and removed from the managed list
    """
    
    global cluster_hostfile
    
    def __init__ (self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.process_groups = ProcessGroupDict()
        self.all_nodes = set()
        self.running_nodes = set()
        self.down_nodes = set()
        self.queue_assignments = {}
        self.node_order = {}
    
        try:
            self.configure(cluster_hostfile)
        except:
            self.logger.error("unable to load hostfile")
        
        self.queue_assignments["default"] = set(self.all_nodes)
        self.alloc_only_nodes = {} # nodename:starttime
        self.cleaning_processes = []
        #keep track of which jobs still have hosts being cleaned
        self.cleaning_host_count = {} # jobid:count
        self.locations_by_jobid = {} #jobid:[locations]
        self.jobid_to_user = {} #jobid:username
        
        self.alloc_timeout = int(get_cluster_system_config("allocation_timeout", 300))

        self.logger.info("allocation timeout set to %d seconds." % self.alloc_timeout)

    def __getstate__(self):
        return {"queue_assignments": self.queue_assignments, "version": 1, 
                "down_nodes": self.down_nodes }


    def __setstate__(self, state):
        Cobalt.Util.fix_set(state)
        self.queue_assignments = state["queue_assignments"]
        self.down_nodes = state["down_nodes"]

        self.process_groups = ProcessGroupDict()
        self.all_nodes = set()
        self.running_nodes = set()
        self.node_order = {}
        try:
            self.configure(cluster_hostfile)
        except:
            self.logger.error("unable to load hostfile")
        self.lock = threading.Lock()
        self.statistics = Statistics()
        self.alloc_only_nodes = {} # nodename:starttime
        if not state.has_key("cleaning_processes"):
            self.cleaning_processes = []
        self.cleaning_host_count = {} # jobid:count
        self.locations_by_jobid = {} #jobid:[locations]
        self.jobid_to_user = {} #jobid:username

        self.alloc_timeout = int(get_cluster_system_config("allocation_timeout", 300))
        self.logger.info("allocation timeout set to %d seconds." % self.alloc_timeout)
    
    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)


    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}
        
        max_nodes = len(self.all_nodes)
        # FIXME: is bgtype really needed for clusters?
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
     

    #there is absolutely no reason for this to exist in cluster_systems at this point. --PMR
    def run_diags(self, partition_list, test_name):
     
        self.logger.error("Run_diags not used on cluster systems.")
        return None

    run_diags = exposed(run_diags)
    
    def launch_diags(self, partition, test_name):
        '''override this method in derived classes!'''
        raise NotImplementedError("launch_diags is not implemented by this class.")
    
    def finish_diags(self, partition, test_name, exit_value):
        '''call this method somewhere in your derived class where you deal with the exit values of diags'''
        raise NotImplementedError("Finish diags not implemented in this class.")

    def handle_pending_diags(self):
        '''implement to handle diags that are still running.

        '''
        raise NotImplementedError("handle_pending_diags not implemented in this class.")
    #can't automate what isn't there
    #handle_pending_diags = automatic(handle_pending_diags)
    
    def fail_partitions(self, specs):
        self.logger.error("Fail_partitions not used on cluster systems.")
        return ""
    fail_partitions = exposed(fail_partitions)
    
    def unfail_partitions(self, specs):
        self.logger.error("unfail_partitions not used on cluster systems.")
        return ""
    unfail_partitions = exposed(unfail_partitions)
    
    def _find_job_location(self, args):
        nodes = args['nodes']
        jobid = args['jobid']
        
        available_nodes = self._get_available_nodes(args)
            
        if nodes <= len(available_nodes):
            return {jobid: [available_nodes.pop() for i in range(nodes)]}
        else:
            return None


    def _get_available_nodes(self, args):
        queue = args['queue']
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])
        
        if required:
            available_nodes = set(required)
        else:
            available_nodes = self.queue_assignments[queue].difference(forbidden)

        available_nodes = available_nodes.difference(self.running_nodes)
        available_nodes = available_nodes.difference(self.down_nodes)

        return available_nodes
    
    def _backfill_cmp(self, left, right):
        return cmp(left[1], right[1])
    
    # the argument "required" is used to pass in the set of locations allowed by a reservation;
    def find_job_location(self, arg_list, end_times):
        best_location_dict = {}
        winner = arg_list[0]

        jobid = None
        user = None
        
        # first time through, try for starting jobs based on utility scores
        for args in arg_list:
            location_data = self._find_job_location(args)
            if location_data:
                best_location_dict.update(location_data)
                jobid = int(args['jobid'])
                user = args['user']
                break
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_location_dict:
            job_end_times = {}
            total = 0
            for item in sorted(end_times, cmp=self._backfill_cmp):
                total += len(item[0])
                job_end_times[total] = item[1]
    
            needed = winner['nodes'] - len(self._get_available_nodes(winner))
            now = time.time()
            backfill_cutoff = 0
            for num in sorted(job_end_times):
                if needed <= num:
                    backfill_cutoff = job_end_times[num] - now

            for args in arg_list:
                if 60*float(args['walltime']) > backfill_cutoff:
                    continue
               
                location_data = self._find_job_location(args)
                if location_data:
                    best_location_dict.update(location_data)
                    self.logger.info("backfilling job %s" % args['jobid'])
                    jobid = int(args['jobid'])
                    user = args['user']
                    break

        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to 
        # be running jobs very soon
        for jobid_str, location_list in best_location_dict.iteritems():
            self.running_nodes.update(location_list)
            self.logger.info("Job %s: Allocating nodes: %s" % (int(jobid_str), location_list))
            #just in case we're not going to be running a job soon, and have to
            #return this to the pool:
            self.jobid_to_user[jobid] = user
            alloc_time = time.time()
            for location in location_list:
                self.alloc_only_nodes[location] = alloc_time
            self.locations_by_jobid[jobid] = location_list
        
        
        return best_location_dict
    find_job_location = exposed(find_job_location)
    
    def check_alloc_only_nodes(self):
        loc_to_release = []
        jobids = []
        check_time = time.time()
        dead_locations = []
        for location, start_time in self.alloc_only_nodes.iteritems():
            if int(check_time) - int(start_time) > self.alloc_timeout:
                self.logger.warning("Location: %s: released.  Time between "\
                        "allocation and run exceeded.", location)
                dead_locations.append(location)
        
        if dead_locations == []:
            #well we don't have anything dying this time.
            return

        for jobid, locations in self.locations_by_jobid.iteritems(): 
            clear_from_dead_locations = False
            for location in locations:
                if location in dead_locations:
                    clear_from_dead_locations = True
                    if jobid not in jobids:
                        jobids.append(jobid)
            #bagging the jobid will cause all locs assoc with job to be
            #cleaned so clear them out to make this faster
            if clear_from_dead_locations:
                for location in locations:
                    dead_locations.remove(location)
            if dead_locations == []:
                #well we don't have anything dying this time.
                break
        self.invoke_node_cleanup(jobids)

    check_alloc_only_nodes = automatic(check_alloc_only_nodes, 
            get_cluster_system_config("automatic_method_interval",10.0))

    def invoke_node_cleanup(self, jobids):
        '''Invoke cleanup for nodes that have exceeded their allocated time
           
        '''
        for jobid in jobids:
            user = self.jobid_to_user[jobid]
            locations = self.locations_by_jobid[jobid]
            for location in locations:
                del self.alloc_only_nodes[location]

            self.clean_nodes(locations, user, jobid)


    def _walltimecmp(self, dict1, dict2):
        return -cmp(float(dict1['walltime']), float(dict2['walltime']))


    def find_queue_equivalence_classes(self, reservation_dict, active_queue_names):
        equiv = []
        for q in self.queue_assignments:
            # skip queues that aren't "running"
            if not q in active_queue_names:
                continue

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
    
    def reserve_resources_until(self, location, time, jobid):
        if time is None:
            for host in location:
                self.running_nodes.discard(host)
                self.logger.info("hasty job kill: freeing %s" % host)
        else:
            self.logger.error("failed to reserve location '%r' until '%s'" % (location, time))
    reserve_resources_until = exposed(reserve_resources_until)


    def nodes_up(self, node_list, user_name=None):
        changed = []
        for n in node_list:
            if n in self.down_nodes:
                self.down_nodes.remove(n)
                changed.append(n)
            if n in self.running_nodes:
                self.running_nodes.remove(n)
                changed.append(n)
        if changed:
            self.logger.info("%s marking nodes up: %s", user_name, ", ".join(changed))
        return changed
    nodes_up = exposed(nodes_up)
        

    def nodes_down(self, node_list, user_name=None):
        changed = []
        for n in node_list:
            if n in self.all_nodes:
                self.down_nodes.add(n)
                changed.append(n)
        if changed:
            self.logger.info("%s marking nodes down: %s", user_name, ", ".join(changed))
        return changed
    nodes_down = exposed(nodes_down)

    def get_node_status(self):
        def my_cmp(left, right):
            return cmp(left[2], right[2])
        
        status_list = []
        for n in self.all_nodes:
            if n in self.running_nodes:
                status = "allocated"
            elif n in self.down_nodes:
                status = "down"
            else:
                status = "idle"
            
            status_list.append( (n, status, self.node_order[n]) )
        status_list.sort(my_cmp)
        return status_list
    get_node_status = exposed(get_node_status)

    def get_queue_assignments(self):
        ret = {}
        for q in self.queue_assignments:
            ret[q] = list(self.queue_assignments[q])
        return ret
    get_queue_assignments = exposed(get_queue_assignments)
    
    def set_queue_assignments(self, queue_names, node_list, user_name=None):
        checked_nodes = set()
        for n in node_list:
            if n in self.all_nodes:
                checked_nodes.add(n)
        
        queue_list = queue_names.split(":")
        for q in queue_list:
            if q not in self.queue_assignments:
                self.queue_assignments[q] = set()
                
        for q in self.queue_assignments.keys():
            if q not in queue_list:
                self.queue_assignments[q].difference_update(checked_nodes)
                if len(self.queue_assignments[q])==0:
                    del self.queue_assignments[q]
            else:
                self.queue_assignments[q].update(checked_nodes)
        self.logger.info("%s assigning queues %s to nodes %s", user_name, queue_names, " ".join(checked_nodes))
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
        
        counter = 0
        for line in f:
            name = line.strip()
            self.all_nodes.add(name)
            self.node_order[name] = counter
            counter += 1
        
        f.close()

    # this gets called by bgsched in order to figure out if there are partition overlaps;
    # it was written to provide the data that bgsched asks for and raises an exception
    # if you try to ask for more
    def get_partitions (self, specs):
        
        partitions = []
        for spec in specs:
            item = {}
            for n in self.all_nodes:
                if "name" in spec:
                    if spec["name"] == '*':
                        item.update( {"name": n} )
                    elif spec["name"] == n:
                        item.update( {"name": n} )
            
            if "name" in spec:    
                spec.pop("name")
            if "children" in spec:
                item.update( {"children": []} )
                spec.pop("children")
            if "parents" in spec:
                item.update( {"parents": []} )
                spec.pop("parents")
            if spec:
                raise NotSupportedError("clusters lack information on: %s" % ", ".join(spec.keys()))
            if item:
                partitions.append(item)
        
        return partitions
    get_partitions = exposed(get_partitions)


    def clean_nodes(self, locations, user, jobid):
        """Given a process group, start cleaning the nodes that were involved.
        The rest of the cleanup is done in check_done_cleaning.
        
        """
        self.logger.info("Job %s/%s: starting node cleanup." , user, jobid)
        try:
            tmp_data = pwd.getpwnam(user)
            groupid = tmp_data.pw_gid
            group_name = grp.getgrgid(groupid)[0]
        except KeyError:
            group_name = ""
            self.logger.error("Job %s/%s: unable to determine group name for epilogue" % (user, jobid))
     
        self.cleaning_host_count[jobid] = 0
        for host in locations:
            h = host.split(":")[0]
            cleaning_process_info ={
                    "host": h, 
                    "cleaning_id": None, 
                    "user": user,
                    "jobid": jobid,
                    "group": group_name,
                    "start_time":time.time(), 
                    "completed":False, 
                    "retry":False,
                    }
            try:
                cleaning_id = self.launch_script("epilogue", h, jobid, user,
                        group_name)
                if cleaning_id == None:
                    #there was no script to run.
                    self.running_nodes.discard(cleaning_processes["host"]) 
                    return 
                self.cleaning_host_count[jobid] += 1
                cleaning_process_info["cleaning_id"] = cleaning_id
                self.cleaning_processes.append(cleaning_process_info)
            except ComponentLookupError:
                self.logger.warning("Job %s/%s: Error contacting forker "
                        "component.  Will Retry until timeout." % (user, jobid))
                cleaning_process_info["retry"] = True
                self.cleaning_processes.append(cleaning_process_info)
                self.cleaning_host_count[jobid] += 1
            except:
                self.logger.error("Job %s/%s: Failed to run epilogue on host "
                        "%s, marking node down", jobid, user, h, exc_info=True)
                self.down_nodes.add(h)
                self.running_nodes.discard(h)
    


    def launch_script(self, config_option, host, jobid, user, group_name):
        '''Start our script processes used for node prep and cleanup.

        '''
        script = get_cluster_system_config(config_option, None)
        if script == None:
            self.logger.error("Job %s/%s: %s not defined in the "\
                    "cluster_system section of the cobalt config file!",
                    user, jobid, config_option)
            return None
        else:
            cmd = ["/usr/bin/ssh", host, script, 
                    str(jobid), user, group_name]
            return ComponentProxy("system_script_forker").fork(cmd, "system epilogue", 
                    "Job %s/%s" % (jobid, user))

        

    #def launch_cleaning_process(self, host, jobid, user, group_name):
    #    '''Ping the forker to launch the cleaning process.
    #
    #    '''
    #    epilogue_script = get_cluster_system_config("epilogue", None)
    #    if epilogue_script == None:
    #        self.logger.error("Job %s/%s: epilogue not defined in the "\
    #                "cluster_system section of the cobalt config file!",
    #                user, jobid)
    #        return None
    #    else:
    #        cmd = ["/usr/bin/ssh", host, epilogue_script, 
    #                str(jobid), user, group_name]
    #        return ComponentProxy("system_script_forker").fork(cmd, "system epilogue", 
    #                "Job %s/%s" % (jobid, user))

    
    def retry_cleaning_scripts(self):
        '''Continue retrying scripts in the event that we have lost contact 
        with the forker component.  Reset start-time to when script starts.

        '''
        for cleaning_process in self.cleaning_processes:
            if cleaning_process['retry'] == True:
                try:
                    cleaning_id = self.launch_script(
                            "epilogue",
                            cleaning_process["host"],
                            cleaning_process['jobid'],
                            cleaning_process['user'],
                            cleaning_process['group'])
                    cleaning_process["cleaning_id"] = cleaning_id
                    cleaning_process["start_time"] = time.time()
                    cleaning_process["retry"] = False
                except ComponentLookupError:
                    self.logger.warning("Job %s/%s: Error contacting forker "
                        "component." % (pg.jobid, pg.user))
                except:
                    self.logger.error("Job %s/%s: Failed to run epilogue on "
                            "host %s, marking node down", pg.jobid, pg.user, h,
                            exc_info=True)
                    self.cleaning_host_count[jobid] -= 1
                    self.down_nodes.add(h)
                    self.running_nodes.discard(h)

    retry_cleaning_scripts = automatic(retry_cleaning_scripts,
            get_cluster_system_config("automatic_method_interval", 10.0))

    def check_done_cleaning(self):
        """Check to see if the processes we are using to clean up nodes 
        post-run are done. If they are, release the nodes back for general 
        consumption.  If the cleanup fails for some reason, then mark the node
        down and release it. 

        """
        
        if self.cleaning_processes == []:
            #don't worry if we have nothing to cleanup
            return
        
        for cleaning_process in self.cleaning_processes: 

            #if we can't reach the forker, we've lost all the cleanup scripts.
            #don't try and recover, just assume all nodes that were being 
            #cleaned are down. --PMR
            if cleaning_process['retry'] == True:
                continue #skip this.  Try anyway, if component came back up.
            
            jobid = cleaning_process['jobid']
            user = cleaning_process['user']

            try:
                exit_status = ComponentProxy("system_script_forker").child_completed(
                        cleaning_process['cleaning_id'])
                ComponentProxy("system_script_forker").child_cleanup(
                        [cleaning_process['cleaning_id']])

            except ComponentLookupError:
                self.logger.error("Job %s/%s: Error contacting forker "
                        "component. Running child processes are "
                        "unrecoverable." % (jobid, user))
                return

            if exit_status != None:
                #we're done, this node is now free to be scheduled again.
                self.running_nodes.discard(cleaning_process["host"])
                cleaning_process["completed"] = True
                self.cleaning_host_count[jobid] -= 1
            else:
                #timeout exceeded
                if (time.time() - cleaning_process["start_time"] > 
                        float(get_cluster_system_config("epilogue_timeout", 60.0))): 
                    cleaning_process["completed"] = True
                    try:
                        forker = ComponentProxy("system_script_forker").signal(
                                cleaning_process['cleaning_id'], "SIGINT")
                        child_output = forker.get_child_data(
                            cleaning_process['cleaning_id'])
                        forker.child_cleanup([cleaning_process['cleaning_id']])
                            
                        #mark as dirty and arrange to mark down.
                        self.down_nodes.add(cleaning_process['host'])
                        self.running_nodes.discard(cleaning_process['host'].host) # <---????check this!
                        self.logger.error("Job %s/%s: epilogue timed out on host %s, marking hosts down", 
                            user, jobid, cleaning_process['host'])
                        self.logger.error("Job %s/%s: stderr from epilogue on host %s: [%s]",
                            user, jobid,
                            cleaning_process['host'], 
                            child_output['stderr'].strip())
                        self.cleaning_host_count[jobid] -= 1
                    except ComponentLookupError:
                        self.logger.error("Job %s/%s: Error contacting forker "
                            "component. Running child processes are "
                            "unrecoverable." % (jobid, user))

            if self.cleaning_host_count[jobid] == 0:
                self.del_process_groups(jobid)
                #clean up other cleanup-monitoring stuff
                self.logger.info("Job %s/%s: job finished on %s",
                    user, jobid, Cobalt.Util.merge_nodelist(self.locations_by_jobid[jobid]))
                del self.locations_by_jobid[jobid]
                del self.jobid_to_user[jobid]
        
        self.cleaning_processes = [cleaning_process for cleaning_process in self.cleaning_processes 
                                    if cleaning_process["completed"] == False]
            
    check_done_cleaning = automatic(check_done_cleaning, 
            get_cluster_system_config("automatic_method_interval", 10.0))



    def del_process_groups(self, jobid):

        raise NotImplementedError("Must be overridden in child class")

