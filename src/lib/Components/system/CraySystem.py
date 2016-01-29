"""Resource management for Cray ALPS based systems"""

import logging
import threading
import thread
import copy
import time
import xmlrpclib

import Cobalt.Util
import Cobalt.Components.system.AlpsBridge as ALPSBridge

from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Components.system.base_system import BaseSystem
from Cobalt.Components.system.CrayNode import CrayNode
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.DataTypes.ProcessGroup import ProcessGroup


_logger = logging.getLogger(__name__)

#TODO: these need to be config options
UPDATE_THREAD_TIMEOUT = 10 #TODO: Time in seconds, make setable
TEMP_RESERVATION_TIME = 300 #Time in seconds to set a temp resource res for startup


class ALPSProcessGroup(ProcessGroup):

    def __init__(self, spec):
        super(ALPSProcessGroup, self).__init__(spec)
        self.alps_res_id = spec['alps_res_id']



class CraySystem(BaseSystem):

    name = "system"
    implementation = "alps_system"
    logger = _logger

    def __init__(self, *args, **kwargs):
        '''Initialize system.  Read initial states from bridge.
        Get current state

        '''
        start_time = time.time()
        super(CraySystem, self).__init__(*args, **kwargs)
        _logger.info('BASE SYSTEM INITIALIZED')
        #process manager setup
        self.process_manager = ProcessGroupManager()
        self.process_manager.forkers.append('alps_script_forker')
        _logger.info('PROCESS MANAGER INTIALIZED')
        #resource management setup
        self.nodes = {} #cray node_id: CrayNode
        self.node_name_to_id = {} #cray node name to node_id map.
        self.alps_reservations = {}
        self._init_nodes_and_reservations()
        #populate initial state
        #state update thread and lock
        self._node_lock = threading.RLock()
        self.node_update_thread = thread.start_new_thread(self._run_update_state,
                tuple())
        _logger.info('UPDATE THREAD STARTED')
        self.alps_reservations = {} #cobalt jobid : AlpsReservation object
        self.current_equivalence_classes = []

        _logger.info('ALPS SYSTEM COMPONENT READY TO RUN')
        _logger.info('Initilaization complete in %s sec.', (time.time() -
                start_time))

    def _init_nodes_and_reservations(self):
        '''Initialize nodes from ALPS bridge data'''

        retnodes = {}
        inventory = ALPSBridge.fetch_inventory(resinfo=True)
        for nodespec in inventory['nodes']:
            node = CrayNode(nodespec)
            node.managed = True
            retnodes[node.node_id] = node
        self.nodes = retnodes
        #Reversing the node name to id lookup is going to save a lot of cycles.
        for node in self.nodes.values():
            self.node_name_to_id[node.name] = node.node_id
        _logger.info('NODE INFORMATION INITIALIZED')
        _logger.info('ALPS REPORTS %s NODES', len(self.nodes))
        #for resspec in inventory['reservations']:
        #    self.alps_reservations[resspec['reservation_id']] = ALPSReservation(2, resspec)
        #Have to persist this otherwise.  Subsequent reservation calls don't
        #help here.

    @exposed
    def get_nodes(self, as_dict=False, node_ids=None):
        '''fetch the node dictionary.

            node_ids - a list of node names to return, if None, return all nodes
                       (default None)

            returns the node dictionary.  Can reutrn underlying node data as
            dictionary for XMLRPC purposes

        '''
        if node_ids is None:
            if as_dict:
                retdict = {}
                for node in self.nodes.values():
                    raw_node = node.to_dict()
                    cooked_node = {}
                    for key, val in raw_node.items():
                        if key.startswith('_'):
                            cooked_node[key[1:]] = val
                        else:
                            cooked_node[key] = val
                    retdict[node.name] = cooked_node
                return retdict
            else:
                return self.nodes
        else:
            raise NotImplementedError

    def _run_update_state(self):
        '''automated node update functions on the update timer go here.'''
        while True:
            self.update_node_state()
            self._get_exit_status()
            Cobalt.Util.sleep(UPDATE_THREAD_TIMEOUT)

    @exposed
    def update_node_state(self):
        '''update the state of cray nodes. Check reservation status and system
        stateus as reported by ALPS

        '''
        #Check clenaup progress.  Check ALPS reservations.  Check allocated
        #nodes.  If there is no resource reservation and the node is not in
        #current alps reservations, the node is ready to schedule again.
        with self._node_lock:
            inventory = ALPSBridge.fetch_inventory(resinfo=True) #This is a full-refresh,
            #determine if summary may be used under normal operation
            inven_nodes = inventory['nodes']
            inven_reservations = inventory['reservations']
            print inven_reservations
            start_time = time.time()
            #Check our reservations.  If it's ID is not in the inventory, then the
            #nodes need to be returned to the pool. Give them the 'idle' state
            res_jobid_to_delete = []
            print self.alps_reservations
            if self.alps_reservations == {}:
                # if we have nodes in cleanup-pending but no alps reservations,
                # then the nodes in cleanup pending are considered idle (or
                # at least not in cleanup).  Hardware check can catch these
                # later.
                for node in self.nodes.values():
                    if node.status in ['cleanup', 'cleanup-pending']:
                        node.status = 'idle'

            for alps_res in self.alps_reservations.values():
                print 'checking reservations'
                #find alps_id associated reservation
                found = False
                current_reservation_ids = [int(res['reservation_id'])
                                           for res in inven_reservations]
                print current_reservation_ids
                print alps_res
                if int(alps_res.alps_res_id) not in current_reservation_ids:
                #for res_info in inven_reservations:
                    #if int(alps_res.alps_res_id) == int(res_info['reservation_id']):
                    #    found = True
                #if not found:
                    for node_id in alps_res.node_ids:
                        print "Reserved: ", self.nodes[str(node_id)].reserved
                        print "Reserved by: ", self.nodes[str(node_id)].reserved_by
                        if not self.nodes[str(node_id)].reserved:
                            #pending hardware status update
                            self.nodes[str(node_id)].status = 'idle'
                    res_jobid_to_delete.append(alps_res.jobid)
            for jobid in res_jobid_to_delete:
                print 'clearing reservations'
                _logger.info('%s: ALPS reservation for this job complete.', jobid)
                del self.alps_reservations[str(jobid)]
            #process group should already be on the way down since cqm released the
            #resource reservation
            cleanup_nodes = [node for node in self.nodes.values()
                             if node.status == 'cleanup-pending']
            print 'cleanup nodes saved'
            #If we have a block marked for cleanup, send a relesae message.
            released_res_jobids = []
            for node in cleanup_nodes:
                print 'releasing alps reservations'
                for alps_res in self.alps_reservations.values():
                    print alps_res.node_ids
                    if (alps_res.jobid not in released_res_jobids and
                            str(node.node_id) in alps_res.node_ids):
                        #send only one release per iteration
                        print 'attempting release'
                        print  alps_res.release()
                        released_res_jobids.append(alps_res.jobid)

        #find hardware status
            print 'updating hardware status'
            for inven_node in inven_nodes:
                if self.nodes.has_key(str(inven_node['node_id'])):
                    node = self.nodes[str(inven_node['node_id'])]
                    if node.reserved:
                        if self.alps_reservations.has_key(str(node.reserved_by)):
                            node.status = 'busy'
                        else:
                            node.status = 'allocated'
                    else:
                        node.status = inven_node['state'].upper()
                else:
                    # Cannot add nodes on the fly.  Or at lesat we shouldn't be
                    # able to.
                    _logger.error('UNS: ALPS reports node %s but not in our node list.',
                                  inven_node['name'])
            #should down win over running in terms of display?
            #keep node that are marked for cleanup still in cleanup
            for node in cleanup_nodes:
                print "setting cleanup"
                node.status = 'cleanup-pending'
        _logger.debug("time in UNS lock: %s seconds", (time.time() - start_time))
        return

    @exposed
    def find_queue_equivalence_classes(self, reservation_dict,
            active_queue_names, passthrough_blocking_res_list=[]):
        '''Aggregate queues together that can impact eachother in the same
        general pass (both drain and backfill pass) in find_job_location.
        Equivalence classes will then be used in find_job_location to consider
        placement of jobs and resources, in separate passes.  If multiple
        equivalence classes are returned, then they must contain orthogonal sets
        of resources.

        Inputs:
        reservation_dict -- a mapping of active reservations to resrouces.
                            These will block any job in a normal queue.
        active_queue_names -- A list of queues that are currently enabled.
                              Queues that are not in the 'running' state
                              are ignored.
        passthrough_partitions -- Not used on Cray systems currently.  This is
                                  for handling hardware that supports
                                  partitioned interconnect networks.

        Output:
        A list of dictionaries of queues that may impact eachother while
        scheduling resources.

        Side effects:
        None

        Internal Data:
        queue_assignments: a mapping of queues to schedulable locations.

        '''
        equiv = []
        node_active_queues = []
        self.current_equivalence_classes = []
        #reverse mapping of queues to nodes
        for node in self.nodes.values():
            if node.managed and node.schedulable:
                #only condiser nodes that we are scheduling.
                node_active_queues = []
                for queue in node.queues:
                    if queue in active_queue_names:
                        node_active_queues.append(queue)
                if node_active_queues == []:
                    #this node has nothing active.  The next check can get
                    #expensive, so skip it.
                    continue
            #determine the queues that overlap.  Hardware has to be included so
            #that reservations can be mapped into the equiv classes.
            found_a_match = False
            for e in equiv:
                for queue in node_active_queues:
                    if queue in e['queues']:
                        e['data'].add(node.name)
                        e['queues'] = e['queues'] | set(node_active_queues)
                        found_a_match = True
                        break
                if found_a_match:
                    break
            if not found_a_match:
                equiv.append({'queues': set(node_active_queues),
                              'data': set([node.name]),
                              'reservations': set()})
        #second pass to merge queue lists based on hardware
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
        #add in reservations:
        for eq_class in equiv:
            for res_name in reservation_dict:
                for node_name in reservation_dict[res_name].split(":"):
                    if node_name in eq_class['data']:
                        eq_class['reservations'].add(res_name)
                        break
            #don't send what could be a large block list back in the return
            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
            self.current_equivalence_classes.append(eq_class)
        return equiv

    @exposed
    def find_job_location(self, arg_list, end_times, pt_blocking_locations=[]):
        '''Given a list of jobs, and when jobs are ending, return a set of
        locations mapped to a jobid that can be run.  Also, set up draining
        as-needed to run top-scored jobs and backfill when possible.

        Called once per equivalence class.

        Input:
        arg_list - A list of dictionaries containning information on jobs to
                   cosnider.
        end_times - list containing a mapping of locations and the times jobs
                    runninng on those locations are scheduled to end.  End times
                    are in seconds from Epoch UTC.
        pt_blocking_locations - Not used for this system.  Used in partitioned
                                interconnect schemes. A list of locations that
                                should not be used to prevent passthrough issues
                                with other scheduler reservations.

        Output:
        A mapping of jobids to locations to run a job to run immediately.

        Side Effects:
        May set draining flags and backfill windows on nodes.
        If nodes are being returned to run, set ALPS reservations on them.

        Notes:
        The reservation set on ALPS resources is uncomfirmed at this point.
        This reservation may timeout.  The forker when it confirms will detect
        this and will re-reserve as needed.  The alps reservation id may change
        in this case post job startup.

        '''
        #TODO: make not first-fit
        now = time.time()
        resource_until_time = now + TEMP_RESERVATION_TIME
        with self._node_lock:
            idle_nodecount = len([node for node in self.nodes.values() if
                node.managed and node.status is 'idle'])
            print arg_list[0]
            self._clear_draining_for_queues(arg_list[0]['queue'])
            #check if we can run immedaitely, if not drain.  Keep going until all
            #nodes are marked for draining or have a pending run.
            best_match = {} #jobid: list(locations)
            current_idle_nodecount = idle_nodecount
            print "cinc: ", current_idle_nodecount
            for job in arg_list:
                if idle_nodecount == 0:
                    break
                elif idle_nodecount < 0:
                    _logger.error("FJL showing negative nodecount of %s",
                            idle_nodecount)
                elif int(job['nodes']) <= idle_nodecount:
                    label = '%s/%s' % (job['jobid'], job['user'])
                    #this can be run immediately
                    job_locs = self._ALPS_reserve_resources(job,
                            resource_until_time)
                    print "job locs", job_locs
                    if job_locs is not None and len(job_locs) == int(job['nodes']):
                        #temporary reservation until job actually starts
                        self.reserve_resources_until(job_locs,
                                resource_until_time, job['jobid'])
                        #set resource reservation, adjust idle count
                        idle_nodecount -= int(job['nodes'])
                        best_match[job['jobid']] = job_locs
                        _logger.info("%s: Job selected for running on nodes  %s",
                                label, " ".join(job_locs))
                else:
                    #TODO: draining goes here
                    pass
            #TODO: backfill pass goes here
            return best_match

    def _ALPS_reserve_resources(self, job, new_time):
        '''Call ALPS to reserve resrources.  Use their allocator.  We can change
        this later to substitute our own allocator if-needed.

        Input:
        Nodecount - number of nodes to reserve for  a job.

        Returns: a list of locations that ALPS has reserved.

        Side effects:
        Places an ALPS reservation on resources.  Calls reserve resources until
        on the set of nodes, and will mark nodes as allocated.

        '''
        #TODO: passthrough from attrs for cray-specific options
        print "reserving resources"
        res_info = ALPSBridge.reserve(job['user'], job['jobid'],
                int(job['nodes']))
        print "res_info: ", res_info
        new_alps_res = None
        if res_info is not None:
            new_alps_res = ALPSReservation(job, res_info, self.nodes)
            self.alps_reservations[job['jobid']] = new_alps_res
        #place a resource_reservation
        if new_alps_res is not None:
            self.reserve_resources_until(new_alps_res.node_names, new_time,
                    job['jobid'])
        return new_alps_res.node_names

    def _clear_draining_for_queues(self, queue):
        '''Given a list of queues, remove the draining flags on nodes.

        queues - a queue in an equivalence class to consider.  This will clear
        the entire equiv class

        return - none

        Note: does not acquire block lock.  Must be locked externally.

        '''
        current_queues = []
        print queue
        print "curr equiv class: %s" % self.current_equivalence_classes
        for equiv_class in self.current_equivalence_classes:
            if queue in equiv_class['queues']:
                current_queues = equiv_class['queues']
        if current_queues:
            for node in self.nodes.values():
                for queue in node.queues:
                    if queue in current_queues:
                        node.clear_drain

    @exposed
    def reserve_resources_until(self, location, new_time, jobid):
        '''Place, adjust and release resource reservations.

        Input:
            location: the location to reserve [list of nodes]
            new_time: the new end time of a resource reservation
            jobid: the Cobalt jobid that this reservation is for

        Output:
            True if resource reservation is successfully placed.
            Otherwise False.

        Side Effects:
            * Sets/releases reservation on specified node list
            * Sets/releases ALPS reservation.  If set reservation is unconfirmed
              Confirmation must occur a cray_script_forker

        Notes:
            This holds the node data lock while it's running.
        '''
        rc = False
        with self._node_lock:
            if new_time is not None:
                #reserve the location. Unconfirmed reservations will have to
                #be lengthened.  Maintain a list of what we have reserved, so we
                #extend on the fly, and so that we don't accidentally get an
                #overallocation/user
                for loc in location:
                    node = self.nodes[self.node_name_to_id[loc]]
                    try:
                        node.reserve(new_time, jobid=jobid)
                    except Cobalt.Exceptions.ResourceReservationFailure as exc:
                        self.logger.error(exc)
                    self.logger.info("job %s: block '%s' now reserved until %s",
                        jobid, loc, time.asctime(time.gmtime(new_time)))
                rc = True
            else:
                #release the reservation and the underlying ALPS reservation
                #and the reserration on blocks.
                for loc in location:
                    node = self.nodes[self.node_name_to_id[loc]]
                    try:
                        node.release(user=None, jobid=jobid)
                    except Cobalt.Exceptions.ResourceReservationFailure as exc:
                        self.logger.error(exc)
                    #cleanup pending has to be dealt with.  Do this in UNS for
                    #now
                    self.logger.info("job %s:  node '%s' released. Cleanup pending.",
                        jobid, loc)
                rc = True
        return rc

    @exposed
    def add_process_groups(self, specs):
        '''Add process groups and start their runs.  Adjust the resource
        reservation time to full run time at this point.

        '''
        _logger.debug("add_process_groups(%r)", specs)
        start_apg_timer = int(time.time())

        for spec in specs:
            spec['forker'] = 'alps_script_forker'
            alps_res = self.alps_reservations.get(str(spec['jobid']), None)
            if alps_res is not None:
                spec['alps_res_id'] = alps_res.alps_res_id
            new_pgroups = self.process_manager.init_groups(specs)

        for pgroup in new_pgroups:
            _logger.info('%s: process group %s created to track job status',
                    pgroup.label, pgroup.id)
            #check resource reservation, and attempt to start.  If there's a
            #failure here, set exit status in process group to a sentinel value.
            try:
                started = self.process_manager.start_groups([pgroup.id])
            except ComponentLookupError as exc:
                _logger.error("%s: failed to contact the %s component",
                        pgroup.label, pgroup.forker)
                #this should be reraised and the queue-manager handle it
                #that would allow re-requesting the run instead of killing the
                #job --PMR
            except xmlrpclib.Fault as exc:
                _logger.error("%s: a fault occurred while attempting to start "
                        "the process group using the %s component",
                        pgroup.label, pgroup.forker)
                pgroup.exit_status = 255
                self.reserve_resources_until(pgroup.location, None,
                        pgroup.jobid)
            except Exception as exc:
                _logger.error("%s: an unexpected exception occurred while "
                        "attempting to start the process group using the %s "
                        "component; releasing resources", pgroup.label,
                        pgroup.forker, exc_info=True)
                pgroup.exit_status = 255
                self.reserve_resources_until(pgroup.location, None,
                        pgroup.jobid)
            else:
                if started is not None and started != []:
                    _logger.info('%s: Process Group %s started successfully.',
                            pgroup.label, pgroup.id)
                else:
                    _logger.error('%s: Process Group startup failed. Aborting.',
                            pgroup.label)
                    pgroup.exit_status = 255
                    self.reserve_resources_until(pgroup.location, None,
                            pgroup.jobid)

        end_apg_timer = int(time.time())
        self.logger.debug("add_process_groups startup time: %s sec",
                (end_apg_timer - start_apg_timer))
        return new_pgroups

    @exposed
    def wait_process_groups(self, specs):
        '''Get the exit status of any completed process groups.  If completed,
        initiate the partition cleaning process, and remove the process group
        from system's list of active processes.

        '''

        process_groups = [pg for pg in
                          self.process_manager.process_groups.q_get(specs)
                          if pg.exit_status is not None]
        for process_group in process_groups:
            del self.process_manager.process_groups[process_group.id]
        return process_groups

    @exposed
    @query
    def get_process_groups(self, specs):
        '''Return a list of process groups using specs as a filter'''
        return self.process_manager.process_groups.q_get(specs)

    @exposed
    @query
    def signal_process_groups(self, specs, signame="SIGINT"):
        '''Send a signal to underlying child process.  Defalut signal is SIGINT.
        May be any signal avaliable to the system.  This signal goes to the head
        process group.

        '''
        pgids = [spec['id'] for spec in specs]
        return self.process_manager.signal_groups(pgids, signame)

    def _get_exit_status(self):
        '''Check running process groups and set exit statuses.

        If status is set, cleanup will be invoked next time wait_process_groups
        is called.

        '''
        completed_pgs = self.process_manager.update_groups()
        for pg in completed_pgs:
            self.reserve_resources_until(pg.location, None, pg.jobid)
        return

    @exposed
    def validate_job(self, spec):
        '''Basic validation of a job to run on a cray system.  Make sure that
        certain arguments have been passsed in.  On failure raise a
        JobValidationError.

        '''
        #Right now this does nothing.  Still figuring out what a valid
        #specification looks like.
        return spec

class ALPSReservation(object):

    def __init__(self, job, spec, nodes):
        '''spec should be the information returned from the Reservation Response
        object.

        '''
        self.jobid = int(job['jobid'])
        self.node_ids = [node_id for node_id in spec['reserved_nodes']]
        self.node_names = []
        for node_id in self.node_ids:
            self.node_names.append(nodes[node_id].name)
        self.pg_id = spec.get('pagg_id', None) #process group of executing script
        if self.pg_id is not None:
            self.pg_id = int(self.pg_id)
        self.alps_res_id = int(spec['reservation_id'])
        #self.app_info = spec['ApplicationArray']
        self.user = job['user']
        #self.gid = spec['account_name'] #appears to be gid.
        self.dying = False
        self.dead = False #System no longer has this alps reservation

    def __str__(self):
        return ", ".join([str(self.jobid), str(self.node_ids),
            str(self.node_names), str(self.pg_id), str(self.alps_res_id),
            str(self.user)])

    @property
    def confirmed(self):
        '''Has this reservation been confirmed?  If not, it's got a 2 minute
        lifetime.

        '''
        return self.pg_id is not None

    def confirm(self, pagg_id):
        '''Mark a reservation as confirmed.  This must be passed back from the
        forker that confirmed the reservation and is the process group id of the
        child process forked for the job.

        '''
        self.pg_id = pagg_id

    def release(self):
        '''Release an underlying ALPS reservation.

        Note:
        A reservation may remain if there are still active claims.  When all
        claims are gone

        '''
        status = ALPSBridge.release(self.alps_res_id)
        if int(status['claims']) != 0:
            _logger.info('ALPS reservation: %s still has %s claims.',
                    self.alps_res_id, status['claims'])
        else:
            _logger.info('ALPS reservation: %s has no claims left.',
                self.alps_res_id)


#if __name__ == '__main__':
#
#    cs = CraySystem()
#    nodes = cs.get_nodes()
#
#    for node_name, node in nodes.iteritems():
#        print "Name: %s" % node_name
#        for key, val in node.to_dict().iteritems():
#            print "    %s: %s" % (key, val)
#
#    for res_id, reservation in cs.alps_reservations.items():
#        print "Resid: %s" % res_id
#        for key, val in reservation.__dict__.items():
#            print "    %s: %s" % (key, val)
#
