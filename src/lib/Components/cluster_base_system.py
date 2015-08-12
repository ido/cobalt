"""Hardware abstraction layer for the system on which process groups are run.

Classes:
ClusterBaseSystem -- base system component
"""

import time
import sys
import Cobalt
import pwd
import grp
import ConfigParser
import os
import Cobalt.Util
from Cobalt.Exceptions import  JobValidationError, NotSupportedError, ComponentLookupError, RequiredLocationError
from Cobalt.DataTypes.ProcessGroup import ProcessGroupDict
from Cobalt.Data import DataDict
from Cobalt.Proxy import ComponentProxy
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Util import config_true_values

__all__ = [
    "ClusterBaseSystem",
]

__config = ConfigParser.ConfigParser()
__config.read(Cobalt.CONFIG_FILES)

if not __config.has_section('cluster_system'):
    print '''"ERROR: cluster_system" section missing from cobalt config file'''
    sys.exit(1)

def get_cluster_system_config(option, default):
    try:
        value = __config.get('cluster_system', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

cluster_hostfile = os.path.expandvars(get_cluster_system_config('hostfile', None))
if cluster_hostfile == None:
    print '''ERROR: No "hostfile" entry in "cluster_system" section of cobalt config file'''
    sys.exit(1)


class ClusterNode(object):

    def __init__(self, name):

        self.name = name
        self.running = False
        self.down = False
        self.queues = []
        self.allocated = False
        self.cleaning = False
        self.cleaning_process = None
        self.assigned_jobid = None
        self.alloc_timeout = None
        self.alloc_start = None
        self.assigned_user = None
        self.draining_jobid = None
        self.drain_time = None

    def allocate(self, jobid, user, time=None):

        self.alloc_timeout = 300
        if time == None:
            self.alloc_start = time.time()
        else:
            self.alloc_start = time
        self.allocated = True
        self.assigned_user = user
        self.assigned_jobid = jobid

    def start_running(self):
        self.running = True
        #invoke prescripts

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

    def mark_draining(self, jobid, drain_time):
        '''mark that a node is being drained for a job, and how long it is to be drained for.'''
        self.draining_jobid = int(jobid)
        self.drain_time = int(drain_time) #integer seconds from epoch

    def clear_draining(self):
        '''Clear the drain state from the node being drained.'''
        self.draining_jobid = None
        self.drain_time = None

    def add_queues(self, queue_list):
        self.queues.extend(queue_list)
        #logger.info('node %s queues are now %s', self.name, " ".join(q for q in self.queues))

    def del_queues(self, queue_list):
        for queue in queue_list:
            del self.queues[queue]
        #logger.info('node %s queues are now %s', self.name, " ".join(q for q in self.queues))

    def set_queues(self, queue_list):
        self.queues = queue_list
        #logger.info('node %s queues are now %s', self.name, " ".join(q for q in self.queues))

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
        self.active_queues = []
        self.all_nodes = set()
        self.running_nodes = set()
        self.down_nodes = set()
        self.queue_assignments = {}
        self.node_order = {}
        self.MINIMUM_BACKFILL_WINDOW = 300
        self.drain_mode = 'backfill'
        self.set_drain_mode(get_cluster_system_config("drain_mode", 'backfill'))

        try:
            self.configure(cluster_hostfile)
        except IOError:
            self.logger.error("unable to load hostfile", exc_info=True)

        self.queue_assignments["default"] = set(self.all_nodes)
        self.alloc_only_nodes = {} # nodename:starttime
        self.cleaning_processes = []
        #keep track of which jobs still have hosts being cleaned
        self.cleaning_host_count = {} # jobid:count
        self.locations_by_jobid = {} #jobid:[locations]
        self.jobid_to_user = {} #jobid:username

        self.alloc_timeout = int(get_cluster_system_config("allocation_timeout", 300))
        self.node_end_time_dict = {}
        self.draining_nodes = {}
        self.draining_queues = {} #{queue_name:time}
        self.logger.info("allocation timeout set to %d seconds." % self.alloc_timeout)
        self.logger.info("Minimum Backfill Window set to %d seconds." % self.MINIMUM_BACKFILL_WINDOW)

    def __getstate__(self):
        state = {}
        state.update(Component.__getstate__(self))
        state.update({
                "cluster_base_version": 1,
                "queue_assignments": self.queue_assignments,
                "down_nodes": self.down_nodes })
        return state

    def __setstate__(self, state):
        Component.__setstate__( self, state)
        self.all_nodes = set()
        self.active_queues = []
        self.node_order = {}
        self.MINIMUM_BACKFILL_WINDOW = 300
        try:
            self.configure(cluster_hostfile)
        except IOError:
            self.logger.error("unable to load hostfile", exc_info=True)
        self.queue_assignments = state.get('queue_assignments', {})
        nonexistent_queues = []
        #make sure we can't try and schedule nodes that don't exist
        if self.queue_assignments == {}:
            self.queue_assignments["default"] = set(self.all_nodes)
        else:
            #remove nodes that have been removed from cobalt.hostfile
            for queue, nodes in self.queue_assignments.iteritems():
                corrected_nodes = self.all_nodes & set(nodes)
                if corrected_nodes == set():
                    nonexistent_queues.append(queue)
                self.queue_assignments[queue] = corrected_nodes
            for queue in nonexistent_queues:
                del self.queue_assignments[queue]
        self.down_nodes = self.all_nodes & set(state.get('down_nodes', set()))
        self.process_groups = ProcessGroupDict()
        self.running_nodes = set()
        self.alloc_only_nodes = {} # nodename:starttime
        if not state.has_key("cleaning_processes"):
            self.cleaning_processes = []
        self.cleaning_host_count = {} # jobid:count
        self.locations_by_jobid = {} #jobid:[locations]
        self.jobid_to_user = {} #jobid:username

        self.alloc_timeout = int(get_cluster_system_config("allocation_timeout", 300))
        self.logger.info("allocation timeout set to %d seconds." % self.alloc_timeout)
        self.node_end_time_dict = {}
        self.draining_nodes = {} #{int(time):list(locations)}
        self.draining_queues = {} #{queue_name:time}
        self.logger.info("Minimum Backfill Window set to %d seconds." % self.MINIMUM_BACKFILL_WINDOW)
        self.drain_mode = 'backfill'
        self.set_drain_mode(get_cluster_system_config("drain_mode", 'backfill'))


    def save_me(self):
        '''Automatically write statefiles.'''
        Component.save(self)
    save_me = automatic(save_me)

    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}

        max_nodes = len(self.all_nodes)

        if spec['mode'] == 'interactive':
            spec['command'] = "/bin/sleep"
            spec['args']    = [str(int(spec['time']) * 60),]
        else:
            spec['mode'] = 'script'

        try:
            spec['nodecount'] = int(spec['nodecount'])
        except:
            raise JobValidationError("Non-integer node count")
        if not 0 < spec['nodecount'] <= max_nodes:
            raise JobValidationError("Node count out of realistic range")
        if float(spec['time']) < 5 and float(spec['time']) > 0:
            raise JobValidationError("Walltime less than minimum")
        if not spec['proccount']:
            spec['proccount'] = spec['nodecount']
        else:
            try:
                spec['proccount'] = int(spec['proccount'])
            except:
                JobValidationError("non-integer proccount")
            if spec['proccount'] < 1:
                raise JobValidationError("negative proccount")

        # need to handle kernel
        return spec
    validate_job = exposed(validate_job)

    def fail_partitions(self, specs):
        self.logger.error("Fail_partitions not used on cluster systems.")
        return ""
    fail_partitions = exposed(fail_partitions)

    def unfail_partitions(self, specs):
        self.logger.error("unfail_partitions not used on cluster systems.")
        return ""
    unfail_partitions = exposed(unfail_partitions)

    def _find_job_location(self, job, now, drain_time=0, already_draining=set([])):
        '''Get a list of nodes capable of running a job.

        job - data about the job under consideration
        drain_location_times - the set of locations that are being drained this pass
        drain_time - the time remaining on the drain locations.  If 0 do not consider
                     drain locations
        already_draining - set of locations that have been set for draining by a higher
                           scored job.  Don't consider these locations for running.

        return:
        jobid: locations - map of jobid to locations for this job
        new_drain_time - if we selected a job to drain, this is the new time
        ready_to_run - no longer have to drain for this job, it's ready to run

        NOTES:
        - This method assumes that the job is the highest scored job under consideration.
        - Call with a drain_time of 0 (default if not passed) to generate a list of drain
          locations if we can't fit the high-scoring job we want to run.


        '''
        forbidden = set(job.get('forbidden', [])) #These are locations the scheduler has decided are inelligible for running.
        required = set(job.get('required', [])) #Always consider these nodes for scheduling, due to things being in a reservation
        selected_locations = set()
        new_drain_time = 0
        ready_to_run = False
        nodes = int(job['nodes'])
        available_nodes = set()
        try:
            available_nodes = self.queue_assignments[job['queue']].difference(forbidden).difference(already_draining)
        except KeyError:
            #The key error is due to the queue being a reservation queue.  Those have no resources assigned in the system
            #component.  This should be changed in a later version, but for now, we can run straight off the "required"
            #nodes list
            pass
        finally:
            available_nodes.update(set(required))

        #TODO: include bit to enable predicted walltimes to be used
        #Remember, until we fix it, walltimes are in minutes, not seconds.
        job_end_time = int(job['walltime']) * 60 + int(now)

        #check to make sure all required nodes are currently in the queue that this job belongs to
        if not required.issubset(available_nodes):
            err_str = '%s/%s has required locations %s that are not in the queue for this job.  Job will never run.' % \
                    (job['user'], job['jobid'], ", ".join([str(s) for s in required.difference(available_nodes)]))
            self.logger.warning(err_str)
            raise RequiredLocationError(err_str)

        #remove forbidden and down nodes from consideration
        available_nodes = available_nodes.difference(forbidden, self.down_nodes)

        if len(available_nodes) < nodes:
            #bail out early, we don't have enough nodes to even consider this job!
            return {}, 0, False

        if len(available_nodes) >= nodes and (int(job_end_time) < int(drain_time) or int(drain_time) == 0):
            # do we have enough that are idle?  The job is smaller than our drain time.
            idle_nodes = available_nodes.difference(self.running_nodes)
            if len(idle_nodes) >= nodes:
                selected_locations = set([idle_nodes.pop() for _ in range(nodes)])
                ready_to_run = True

        if drain_time == 0 and ready_to_run == False: #go ahead and select locations for draining.
            #choose the idle nodes, iterate over times adding nodes until we have enough with the shortest wait.
            remaining_node_count = nodes
            ready_times = self.node_end_time_dict.keys()
            ready_times.sort() # make sure we're getting the soonest available.
            for ready_time in ready_times:
                new_drain_time = ready_time
                locations = self.node_end_time_dict[ready_time]
                for location in locations:
                    if location in available_nodes:
                        selected_locations.add(location)
                        remaining_node_count -= 1
                        if remaining_node_count == 0:
                            break
                if remaining_node_count == 0:
                    break

        if selected_locations == set([]):
            return {}, 0, False
        #Jobid has to be a string or else xmlrpc has trouble with the dict. XMLRPC also doesn't like sets.
        return {str(job['jobid']): list(selected_locations)}, new_drain_time, ready_to_run

    def _get_available_nodes(self, args):
        '''Get all nodes required for a job, ignoring forbidden ones (i.e. reserved nodes).

        '''
        queue = args['queue']
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])

        if required:
            available_nodes = set(required)
        else:
            available_nodes = self.queue_assignments[queue].difference(forbidden)

        return self._get_available_node_subset(available_nodes)

    def _get_available_node_subset(self, node_set):
        '''Given a set of nodes, return the subset of available nodes.

        '''
        available_nodes = node_set.difference(self.running_nodes)
        return available_nodes.difference(self.down_nodes)

    # the argument "required" is used to pass in the set of locations allowed by a reservation;
    def find_job_location(self, job_list, end_times):
        '''Find the best location for a job and start the job allocation
        process (this is different from what happens on BlueGenes!)

        job_list: list of dictionaries of job data.  Each entry has the
        following fields:

        user -- username of the job
        pt_forbidden -- (ignored for cluster_systems)
        geometry -- (ignored for cluster_systems)
        forbidden -- locations that are forbidden for scheduling, usually due
                     to reservations
        jobid -- id of the Cobalt job
        queue -- queue of the Cobalt job
        walltime_p -- predicted wallclock time of the job (not used in
                      cluster_systems currently)
        walltime -- requested wall clock time for the job
        utility_score -- score of the job
        attrs -- a list of attributes on the job (currently used to constrain
                 locations)
        nodes -- number of requested nodes
        queue_equivalence -- the other queues to consider with this job

        end_times: This is a list of locations and when the job on them is
                   expected to expire.

        This may be run with:
        first_fit - run immediately in a location
        backfill - drain for jobs and allow for backfilling

        Reservation handling:
        Reservations are a special case, as they don't (necessarily) have
        queues bound tightly to resources in the system component.  Under the
        current behavior, they should first-fit their jobs.  A reservation pass
        on this function can will have 'requires' set in the passed in jobs,
        allowing us to react accordingly.

        Reservation passes do not respect drain decisions otherwise.  The
        behavior of two overlapping reservations is undefined, since a
        reservation is effectively max-priority on the affected resources.  All
        reservations are equal and will race as such.

        '''
        best_location_dict = {}
        jobid = None
        user = None
        now = int(time.time())
        drain_locs_by_queue = {}
        self.init_drain_times(end_times)
        #self.draining_nodes cannot be reset here, due to the fact that this
        #may be called on a second pass if you have multiple
        #queue equivalence classes.
        #self.logger.debug('job_list: %s', job_list)
        # first time through, try for starting jobs based on utility scores

        #remove queues from draining if they are not in the active queue list,
        #from the scheduler via find_queue_equivalence_classes
        inactive_queues = []
        for queue in self.draining_queues.keys():
            if queue not in self.active_queues:
                inactive_queues.append(queue)
        for queue in inactive_queues:
            del self.draining_queues[queue]

        #to make sure that we properly reevaluated the drains on this pass,
        #we need to clear out old times, make sure not to clear
        #out times that are in use by other equivalence classes.
        if 'queue_equivalence' in job_list[0]:
            current_equiv = job_list[0]['queue_equivalence']
            for queue in current_equiv:
                if queue in self.draining_queues.keys():
                    del self.draining_queues[queue]
            still_draining_times = [str(t) for t in self.draining_queues.values()]
            not_found_times = [t for t in self.draining_nodes.keys()
                    if t not in still_draining_times]
            for drain_time in not_found_times:
                del self.draining_nodes[drain_time]

            self.logger.debug('*' * 80)
            self.logger.debug('initial draining_queues:\n%s', self.draining_queues)
            self.logger.debug('stilldraining times:\n%s', still_draining_times)
            self.logger.debug('initial draining_nodes:\n%s', self.draining_nodes)
            self.logger.debug('*' * 80)

        for jobs in job_list:
            jobid = int(jobs['jobid'])
            queue = jobs['queue']
            user = jobs['user']
            has_required = False
            try:
                if jobs['required']:
                    #if this exists we're scheduling on the reservation pass, treat accordingly.
                    has_required = True
            except KeyError: #required locations is totally optional and may not be in the dict.
                pass
            drain_time = 0
            self.logger.debug('Queue considered: %s', queue)
            if queue in drain_locs_by_queue.keys():
                #self.logger.debug('queue seen')
                continue
            else: #first time we're seeing this queue this pass
                if queue in self.draining_queues.keys():
                    del self.draining_queues[queue]
            self.logger.debug("current draining nodes: %s", self.draining_nodes)
            already_draining = set([loc for drain_locs in self.draining_nodes.values() for loc in drain_locs])
            self.logger.debug("Already draining: %s" % already_draining)
            #short circuit, we won't be able to schedule anything if our entire queue is being drained.
            try:
                if self.queue_assignments[queue].issubset(already_draining):
                    self.logger.debug("queue %s has no nodes that aren't already drained.", queue)
                    drain_locs_by_queue[queue] = set(self.queue_assignments[queue])
                    #use shortest drain time of all resources for this queue:
                    shortest_time = None
                    for drain_time, drain_nodes in self.draining_nodes.iteritems():
                        if self.queue_assignments[queue].intersection(drain_nodes):
                            #self.logger.debug("Finding new shortest time")
                            if shortest_time is None or shortest_time > int(drain_time):
                                shortest_time = int(drain_time)
                    self.draining_queues[queue] = shortest_time
                    continue
            except KeyError:
                #Reservation queues will cause a key error on this test, the
                #queue is not actually assigned to resources in the component.
                #Treat as though this check passed, reservations don't
                #drain. --PMR
                pass
            try:
                location_data, drain_time, ready_to_run = self._find_job_location(jobs,
                        now, already_draining=already_draining)
            except RequiredLocationError:
                self.logger.debug("Required location error PRIMARY LOOP!")
                continue #location_data, drain_time and ready_to_run not set.
            if ready_to_run:
                if self.drain_mode == 'first_fit':
                    self.logger.info("locations %s selected to run immediately by first fit", location_data)
                else:
                    self.logger.info("locations %s selected to run immediately", location_data)
                best_location_dict.update(location_data)
                break
            elif drain_time != 0 and (self.drain_mode != 'first_fit' or has_required): #found a drain location
                #In the event reservation scheduling, use first fit.
                drain_locs_by_queue[queue] = set(location_data[str(jobid)])
                self.draining_queues[queue] = drain_time
                self.draining_nodes[str(self.draining_queues[queue])] = list(location_data[str(jobid)])
                self.logger.info("%s/%s: Is draining nodes %s in queue %s", user, jobid, ":".join(location_data[str(jobid)]), queue)
                #do not break out here, we need to cover other queues!

        self.logger.debug('primary pass complete')

        #make a second pass to pick a job for the draining nodes

        #for queue in drain_locs_by_queue.keys():
        if drain_locs_by_queue != {} and self.drain_mode == 'backfill':
            #only make this pass if we are allowing backfilling.
            self.logger.debug("locs_by_queue: %s", drain_locs_by_queue)
            self.logger.debug("locs_by_time: %s", self.draining_queues)
            for jobs in job_list:
                jobid = int(jobs['jobid'])
                user = jobs['user']
                queue = jobs['queue']
                drain_time = 0
                try:
                    location_data, drain_time, ready_to_run = self._find_job_location(jobs, now,
                            drain_time=int(self.draining_queues[queue]))
                except RequiredLocationError:
                    continue #location_data, drain_time and ready_to_run not set.
                except KeyError:
                    pass
                    #self.logger.warning("Queue %s not found in draining queue times.", queue)
                    #raise
                else:
                    if ready_to_run:
                        #first backfill we find is the winner, and we start it.
                        best_location_dict.update(location_data)
                        self.logger.info("%s/%s: job selected for backfill on locations %s from queue %s",
                                user, jobid, ':'.join(location_data[str(jobid)]), jobs['queue'])
                        break

        self.logger.debug('secondary_pass_complete')
        # reserve the stuff in the best_partition_dict, as those partitions are allegedly going to
        # be running jobs very soon
        for jobid_str, location_list in best_location_dict.iteritems():
            self.running_nodes.update(location_list)
            self.logger.info("Job %s: Allocating nodes: %s" % (int(jobid_str), location_list))
            #just in case we're not going to be running a job soon, and have to
            #return this to the pool:
            self.jobid_to_user[jobid] = user
            for location in location_list:
                self.alloc_only_nodes[location] = now
            self.locations_by_jobid[jobid] = location_list
        return best_location_dict
    find_job_location = exposed(find_job_location)

    def init_drain_times(self, end_times):
        '''Update a list of the locations and times.  Return a list of nodes and their drain times.

        end_times: a list of dicts [[locations]:time] with the scheduled end times of locations that are running

        side-effect: self.node_end_time_dict has every location initialized to 0 (immediately available)
                     or to the time remaining on the jobs running

        '''
        #all nodes init to 0-time.  (ready immediately)
        self.node_end_time_dict = {0:list(self.all_nodes)}
        #All currently running nodes should have their times marked
        for locations, float_end_time in end_times:
            end_time = int(float_end_time)
            for location in locations:
                if end_time not in self.node_end_time_dict.keys():
                    self.node_end_time_dict[end_time] = [location]
                else:
                    self.node_end_time_dict[end_time].append(location)
                try:
                    self.node_end_time_dict[0].remove(location)
                except ValueError:
        # add in locations that are being cleaned, but are not coming from the scheduling component
                    self.logger.warning("WARNING: Location %s not found in node end times.", location)
        for locations in self.locations_by_jobid.itervalues():
            self._append_cleanup_drain_shadow(locations)

        return

    def _append_cleanup_drain_shadow(self, locations):
        '''Append locations to our list of end times so that cleanup casts an appropriate backfill shadow.

        '''
        # add in locations that are being cleaned, but are not coming from the scheduling component
        now = int(time.time())
        #take the set of locations that we haven't assigned end-times to, and extend their times appropriately.
        #these locations are in cleanup
        cleaning_locations = list(set(locations) & set(self.node_end_time_dict[0]))
        if not cleaning_locations == []:
            #cast a shadow 5 minutes in the future until these locations are no longer tracked.
            if self.node_end_time_dict.has_key(now + self.MINIMUM_BACKFILL_WINDOW):
                # Don't stomp on times from a job that ends at the same time as cleanup would.
                self.node_end_time_dict[now + self.MINIMUM_BACKFILL_WINDOW].extend(cleaning_locations)
            else:
                self.node_end_time_dict[now + self.MINIMUM_BACKFILL_WINDOW] = cleaning_locations
            for location in cleaning_locations:
                if location in self.node_end_time_dict[0]:
                    self.node_end_time_dict[0].remove(location)

    def check_alloc_only_nodes(self):
        '''Check to see if nodes that we have allocated but not run yet should be freed.

        '''
        jobids = []
        check_time = time.time()
        dead_locations = []
        for location, start_time in self.alloc_only_nodes.iteritems():
            if int(check_time) - int(start_time) > self.alloc_timeout:
                self.logger.warning("Location: %s: released.  Time between allocation and run exceeded.", location)
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
                    if location in dead_locations:
                        dead_locations.remove(location)
            if dead_locations == []:
                #well we don't have anything dying this time.
                break
        self.invoke_node_cleanup(jobids)
        return
    check_alloc_only_nodes = automatic(check_alloc_only_nodes, get_cluster_system_config("automatic_method_interval", 10.0))

    def invoke_node_cleanup(self, jobids):
        '''Invoke cleanup for nodes that have exceeded their allocated time

        '''
        found_locations = set()
        for jobid in jobids:
            user = self.jobid_to_user[jobid]
            locations = self.locations_by_jobid[jobid]
            locations_to_clean = set()
            for location in locations:
                if location not in found_locations:
                    try:
                        del self.alloc_only_nodes[location]
                    except KeyError:
                        self.logger.warning('WANING: Location: %s Jobid: %s; Location already removed from alloc_only_nodes',
                            location, jobid)
                    else:
                        locations_to_clean.add(location)
                        found_locations.add(location)

            self.clean_nodes(list(locations_to_clean), user, jobid)

    def _walltimecmp(self, dict1, dict2):
        return -cmp(float(dict1['walltime']), float(dict2['walltime']))

    def find_queue_equivalence_classes(self, reservation_dict, active_queue_names,
            passthrough_partitions=[]):
        '''Aggregate queues together that can impact eachother in the same
        general pass (both drain and backfill pass) in find_job_location.
        Equivalence classes will then be used in FJL to consider placement of
        jobs and resources, in separate passes.  If multiple equivalence
        classes are returned, then they must contain orthogonal sets
        of resources.

        Inputs:
        reservation_dict -- a mapping of active reservations to resrouces.
                            These will block any job in a normal queue.
        active_queue_names -- A list of queues that are currently enabled.
                              Queues that are not in the 'running' state
                              are ignored.
        passthrough_partitions -- Not used in the general cluster_system
                                  version.  Nominally this would be a list of
                                  location identifiers that would be impacted
                                  by runs on a queue, but would not be directly
                                  scheduled. The implication is that these
                                  locations may be made unavailable by having
                                  resources in this equivalence class
                                  scheduled, or vice-versa.

        Output:
        A list of dictionaries of queues that may impact eachother while
        scheduling resources.

        Side effects:
        Updates a list of currently active queues used for find_job_location.

        Internal Data:
        queue_assignments: a mapping of queues to schedulable locations.

        '''
        #Bring together sets of queues that need to be considered together in a scheduling pass.
        #if two queues have overlapping sets of resources we need to consider them toegether in the same scheduler
        #pass.  By the same token, we can treat each orthogonal set of resources in their own pass.  Which is exactly
        #what find_job_location will do with this data.
        equiv = []
        self.active_queues = active_queue_names

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

        #merge together queue/resource groupings that you missed on the first pass
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for e in real_equiv:
                if e['data'].intersection(eq_class['data']):
                    e['queues'].update(eq_class['queues'])
                    e['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)

        equiv = real_equiv

        #add in locations for active reservations that may impact scheduling decisions in these queues.
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
        '''hold onto resources until a timeout has passed, and then clear the
        nodes for another job.

        '''

        #WARNING: THIS IS VERY DIFFERENT FROM BLUE GENES!
        #THIS WILL FORCIBLY CLEAR THE NODE!

        if time is None:
            for host in location:
                self.running_nodes.discard(host)
                self.logger.info("hasty job kill: freeing %s" % host)
        else:
            self.logger.error("failed to reserve location '%r' until '%s'" % (location, time))
            return True #So we can progress.
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
        '''Get current node status for clients.'''
        def my_cmp(left, right):
            '''force an ordering on the nodes, needed for display'''
            return cmp(left[2], right[2])

        status_list = []
        for node in self.all_nodes:
            if node in self.running_nodes:
                status = "allocated"
            elif node in self.down_nodes:
                status = "down"
            else:
                status = "idle"

            status_list.append( (node, status, self.node_order[node]) )
        status_list.sort(my_cmp)
        return status_list
    get_node_status = exposed(get_node_status)

    def get_queue_assignments(self):
        '''Fetch the node to queue mapping for display.'''
        ret = {}
        for queues in self.queue_assignments:
            ret[queues] = list(self.queue_assignments[queues])
        return ret
    get_queue_assignments = exposed(get_queue_assignments)

    def set_queue_assignments(self, queue_names, node_list, user_name=None):
        '''Associate queues with nodes from an external client.'''
        checked_nodes = set()
        for node in node_list:
            if node in self.all_nodes:
                checked_nodes.add(node)

        queue_list = queue_names.split(":")
        for queue in queue_list:
            if queue not in self.queue_assignments:
                self.queue_assignments[queue] = set()

        for queue in self.queue_assignments.keys():
            if queue not in queue_list:
                self.queue_assignments[queue].difference_update(checked_nodes)
                if len(self.queue_assignments[queue])==0:
                    del self.queue_assignments[queue]
            else:
                self.queue_assignments[queue].update(checked_nodes)
        self.logger.info("%s assigning queues %s to nodes %s", user_name, queue_names, " ".join(checked_nodes))
        return list(checked_nodes)
    set_queue_assignments = exposed(set_queue_assignments)

    def get_backfill_windows(self):
        '''Get the current drain limits for display'''
        return self.draining_nodes
    get_backfill_windows = exposed(get_backfill_windows)

    def verify_locations(self, location_list):
        """Providing a system agnostic interface for making sure a 'location string' is valid"""
        ret = []
        for l in location_list:
            if l in self.all_nodes:
                ret.append(l)
        return ret
    verify_locations = exposed(verify_locations)

    def configure(self, filename):
        '''Add nodes from hostfile to Cobalt's configuration of tracked nodes.

        '''
        hostfile = open(filename)

        counter = 0
        for line in hostfile:
            name = line.strip()
            self.all_nodes.add(name)
            self.node_order[name] = counter
            counter += 1

        hostfile.close()

        #On configuration call, set minimum backfill window.
        self.MINIMUM_BACKFILL_WINDOW = int(get_cluster_system_config("minimum_backfill_window", 300))

    # this gets called by bgsched in order to figure out if there are partition overlaps;
    # it was written to provide the data that bgsched asks for and raises an exception
    # if you try to ask for more
    def get_partitions (self, specs):
        '''Fetch node information and their respective states.

        '''
        partitions = []
        for spec in specs:
            item = {}
            for node in self.all_nodes:
                if "name" in spec:
                    if spec["name"] == '*':
                        item.update( {"name": node} )
                    elif spec["name"] == node:
                        item.update( {"name": node} )

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
        #Make sure we cast an appropriate backfill shadow.
        self._append_cleanup_drain_shadow(locations)
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
            cleaning_process_info = {
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
                    self.running_nodes.discard(cleaning_process_info["host"])
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
            if (get_cluster_system_config("run_remote", 'true').lower() in config_true_values):
                cmd = ["/usr/bin/ssh", host, script, str(jobid), user, group_name]
            else:
                cmd = script.split()
                cmd.append(str(jobid))
                cmd.append(user)
                cmd.append(group_name)
            return ComponentProxy("system_script_forker").fork(cmd, "system epilogue", "Job %s/%s" % (jobid, user))

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
                        "component." % (cleaning_process['jobid'],
                            cleaning_process['user']))
                except:
                    self.logger.error("Job %s/%s: Failed to run epilogue on "
                            "host %s, marking node down",
                            cleaning_process['jobid'], cleaning_process['user'],
                            cleaning_process['host'],
                            exc_info=True)
                    self.cleaning_host_count[cleaning_process['jobid']] -= 1
                    self.down_nodes.add(cleaning_process['host'])
                    self.running_nodes.discard(cleaning_process['host'])

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

        children = []
        current_time = time.time()
        try:
            children = ComponentProxy("system_script_forker").get_children(None,
                    [cleaning_process['cleaning_id']
                        for cleaning_process in self.cleaning_processes])
        except ComponentLookupError:
            self.logger.error("Could not communicate with "
                            "forker component during cleanup")
            return None

        #reap completed children from the component
        try:
            ComponentProxy("system_script_forker").cleanup_children(
                    [child['id'] for child in children if child['complete']])
        except ComponentLookupError:
            self.logger.error("Could not communicate with "
                "forker component during cleanup")
                # cleanup faled.  reattempt in a little while...
            return None


        child_dict = {}
        for child in children:
            child_dict[child['id']] = child

        for cleaning_process in self.cleaning_processes:
            #if we can't reach the forker, we've lost all the cleanup scripts.
            #don't try and recover, just assume all nodes that were being
            #cleaned are down. --PMR
            if cleaning_process['retry'] == True:
                continue #skip this.  Try anyway, if component came back up.

            jobid = cleaning_process['jobid']
            user = cleaning_process['user']
            child = child_dict[cleaning_process['cleaning_id']]
            exit_status = child['exit_status']

            # check if all of the scripts have completed
            if (exit_status == None) and (current_time - cleaning_process["start_time"] <=
                    float(get_cluster_system_config("epilogue_timeout", 60.0))):
                continue

            if child['lost_child']:
                self.logger.warning("Job %s/%s: a script was lost: %s",
                        user, jobid, child['id'])
                self.__mark_failed_cleaning(cleaning_process)
            elif exit_status == 0:
                #we're done, this node is now free to be scheduled again.
                self.logger.info("Job %s/%s: cleanup completed for host: %s",
                        user, jobid, cleaning_process['host'])
                self.running_nodes.discard(cleaning_process["host"])
                cleaning_process["completed"] = True
                self.cleaning_host_count[jobid] -= 1
            elif (exit_status != 0) and (exit_status != None):
                #assume a nonzero status is a script-failure.
                self.__mark_failed_cleaning(cleaning_process)
                self.logger.debug("Job %s/%s: stderr from epilogue on host %s: [%s]",
                        user, jobid, cleaning_process['host'],
                        "\n".join(child['stderr']))
            else:
                #timeout exceeded otherwise wait until next cycle
                self.logger.debug('cleaning_time: %s' %(current_time -cleaning_process['start_time']))
                if (current_time - cleaning_process["start_time"] >
                        float(get_cluster_system_config("epilogue_timeout", 60.0))):
                    cleaning_process["completed"] = True

                    try:
                        #attempt to clean up the child.
                        forker = ComponentProxy("system_script_forker",
                                defer=False)
                        forker.signal(cleaning_process['cleaning_id'],
                                "SIGINT")
                        child_output = forker.get_children(None,
                            [cleaning_process['cleaning_id']])[0]
                        forker.cleanup_children([child_output['id']])
                    except ComponentLookupError:
                        self.logger.error("Job %s/%s: Error contacting forker "
                            "component. Running child processes are "
                            "unrecoverable." % (jobid, user))
                    finally:
                        self.__mark_failed_cleaning(cleaning_process,
                            "Job %s/%s: epilogue timed out on host %s, marking "
                            "host down" % (user, jobid, cleaning_process['host']))

            if self.cleaning_host_count[jobid] == 0:
                self.del_process_groups(jobid)
                #clean up other cleanup-monitoring stuff
                self.logger.info("Job %s/%s: job finished on %s",
                    user, jobid, Cobalt.Util.merge_nodelist(self.locations_by_jobid[jobid]))
                del self.locations_by_jobid[jobid]
                del self.jobid_to_user[jobid]

        self.cleaning_processes = [cleaning_process for cleaning_process in self.cleaning_processes
                                    if not cleaning_process["completed"]]
    check_done_cleaning = automatic(check_done_cleaning,
            get_cluster_system_config("automatic_method_interval", 10.0))

    def __mark_failed_cleaning(self, cleaning_process, msg=None):
        '''Mark that a node has failed cleanup and take the node out of service.

        '''
        user = cleaning_process['user']
        jobid = cleaning_process['jobid']
        host = cleaning_process['host']

        if msg == None:
            msg = "Job %s/%s: Cleanup failed on host %s, marking node down." % \
                    (user, jobid, host)

        self.down_nodes.add(host)
        self.running_nodes.discard(host)
        self.cleaning_host_count[jobid] -= 1
        cleaning_process['completed'] = True
        self.logger.error(msg)
        return

    def del_process_groups(self, jobid):
        '''Set actions to take when deleting process groups.  This must be
        overridden in the implementation.

        '''
        raise NotImplementedError("Must be overridden in child class")

    def set_drain_mode(self, mode):
        valid_modes = ['backfill', 'drain_only', 'first_fit']
        if mode not in valid_modes:
            raise ValueError("Mode %s is not a valid drain mode" % mode)
        self.drain_mode = mode
