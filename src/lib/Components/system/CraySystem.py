"""Resource management for Cray ALPS based systems"""

import logging
import threading
import thread
import time
import sys
import xmlrpclib
import json
import ConfigParser
import Cobalt.Util
import Cobalt.Components.system.AlpsBridge as ALPSBridge
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Components.system.base_system import BaseSystem
from Cobalt.Components.system.CrayNode import CrayNode
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager
from Cobalt.Components.system.ALPSProcessGroup import ALPSProcessGroup
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Exceptions import JobNotInteractive
from Cobalt.Components.system.ALPSProcessGroup import ALPSProcessGroup
from Cobalt.Exceptions import JobValidationError
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from Cobalt.Util import compact_num_list, expand_num_list
from Cobalt.Util import init_cobalt_config, get_config_option

_logger = logging.getLogger(__name__)
init_cobalt_config()

UPDATE_THREAD_TIMEOUT = int(get_config_option('alpssystem', 'update_thread_timeout', 10))
TEMP_RESERVATION_TIME = int(get_config_option('alpssystem', 'temp_reservation_time', 300))
SAVE_ME_INTERVAL = float(get_config_option('alpsssytem', 'save_me_interval', 10.0))
#default 20 minutes to account for boot.
PENDING_STARTUP_TIMEOUT = float(get_config_option('alpssystem', 'pending_startup_timeout', 1200))
APKILL_CMD = get_config_option('alps', 'apkill', '/opt/cray/alps/default/bin/apkill')
DRAIN_MODE = get_config_option('system', 'drain_mode', 'first-fit')
#cleanup time in seconds
CLEANUP_DRAIN_WINDOW = get_config_option('system', 'cleanup_drain_window', 300)
#SSD information
DEFAULT_MIN_SSD_SIZE = int(get_config_option('alpssystem', 'min_ssd_size', -1))

#Epsilon for backfilling.  This system does not do this on a per-node basis.
BACKFILL_EPSILON = int(get_config_option('system', 'backfill_epsilon', 120))
ELOGIN_HOSTS = [host for host in get_config_option('system', 'elogin_hosts', '').split(':')]
if ELOGIN_HOSTS == ['']:
    ELOGIN_HOSTS = []
DRAIN_MODES = ['first-fit', 'backfill']
CLEANING_ID = -1
DEFAULT_MCDRAM_MODE = get_config_option('alpssystem', 'default_mcdram_mode', 'cache')
DEFAULT_NUMA_MODE = get_config_option('alpssystem', 'default_numa_mode', 'quad')
MCDRAM_TO_HBMCACHEPCT = {'flat':'0', 'cache':'100', 'split':'25', 'equal':'50', '0':'0', '25':'25', '50':'50', '100':'100'}
VALID_MCDRAM_MODES = ['flat', 'cache', 'split', 'equal', '0', '25', '50', '100']
VALID_NUMA_MODES = ['a2a', 'hemi', 'quad', 'snc2', 'snc4']


def chain_loc_list(loc_list):
    '''Take a list of compact Cray locations,
    expand and concatenate them.

    '''
    retlist = []
    for locs in loc_list:
        retlist.extend(expand_num_list(locs))
    return retlist


class CraySystem(BaseSystem):
    '''Cray/ALPS-specific system component.  Behaviors should go here.  Direct
    ALPS interaction through BASIL/other APIs should go through the ALPSBridge
    (or other bridge) module as appropriate.

    '''
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
        self._common_init_restart()
        _logger.info('ALPS SYSTEM COMPONENT READY TO RUN')
        _logger.info('Initilaization complete in %s sec.', (time.time() -
                start_time))

    def _common_init_restart(self, spec=None):
        '''Common routine for cold and restart intialization of the system
        component.

        '''
        try:
            self.system_size = int(get_config_option('system', 'size'))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            _logger.critical('ALPS SYSTEM: ABORT STARTUP: System size must be specified in the [system] section of the cobalt configuration file.')
            sys.exit(1)
        if DRAIN_MODE not in DRAIN_MODES:
            #abort startup, we have a completely invalid config.
            _logger.critical('ALPS SYSTEM: ABORT STARTUP: %s is not a valid drain mode.  Must be one of %s.',
                DRAIN_MODE, ", ".join(DRAIN_MODES))
            sys.exit(1)
        #initilaize bridge.
        bridge_pending = True
        while bridge_pending:
            # purge stale children from prior run.  Also ensure the
            # system_script_forker is currently up.
            # These attempts may fail due to system_script_forker not being up.
            # We don't want to trash the statefile in this case.
            try:
                ALPSBridge.init_bridge()
            except ALPSBridge.BridgeError:
                _logger.error('Bridge Initialization failed.  Retrying.')
                Cobalt.Util.sleep(10)
            except ComponentLookupError:
                _logger.warning('Error reaching forker.  Retrying.')
                Cobalt.Util.sleep(10)
            else:
                bridge_pending = False
                _logger.info('BRIDGE INITIALIZED')
        #process manager setup
        if spec is None:
            self.process_manager = ProcessGroupManager(pgroup_type=ALPSProcessGroup)
        else:
            self.process_manager = ProcessGroupManager(pgroup_type=ALPSProcessGroup).__setstate__(spec['process_manager'])
            self.logger.debug('pg type %s', self.process_manager.process_groups.item_cls)
        #self.process_manager.forkers.append('alps_script_forker')
        self.process_manager.update_launchers()
        self.pending_start_timeout = PENDING_STARTUP_TIMEOUT
        _logger.info('PROCESS MANAGER INTIALIZED')
        #resource management setup
        self.nodes = {} #cray node_id: CrayNode
        self.node_name_to_id = {} #cray node name to node_id map
        self.alps_reservations = {} #cobalt jobid : AlpsReservation object
        if spec is not None:
            self.alps_reservations = spec['alps_reservations']
        self._init_nodes_and_reservations()
        if spec is not None:
            node_info = spec.get('node_info', {})
            for nid, node in node_info.items():
                try:
                    self.nodes[nid].reset_info(node)
                except: #check the exception types later.  Carry on otherwise.
                    self.logger.warning("Node nid: %s not found in restart information.  Bringing up node in a clean configuration.", nid)
        #storage for pending job starts.  Allows us to handle slow starts vs
        #user deletes
        self.pending_starts = {} #jobid: time this should be cleared.
        self.nodes_by_queue = {} #queue:[node_ids]
        #populate initial state
        #state update thread and lock
        self._node_lock = threading.RLock()
        self._gen_node_to_queue()
        self.node_update_thread = thread.start_new_thread(self._run_update_state, tuple())
        _logger.info('UPDATE THREAD STARTED')
        self.current_equivalence_classes = []
        self.killing_jobs = {}
        #hold on to the initial spec in case nodes appear out of nowhere.
        self.init_spec = None
        if spec is not None:
            self.init_spec = spec

    def __getstate__(self):
        '''Save process, alps-reservation information, along with base
        information'''
        state = {}
        state.update(super(CraySystem, self).__getstate__())
        state['alps_system_statefile_version'] = 1
        state['process_manager'] = self.process_manager.__getstate__()
        state['alps_reservations'] = self.alps_reservations
        state['node_info'] = self.nodes
        return state

    def __setstate__(self, state):
        start_time = time.time()
        super(CraySystem, self).__setstate__(state)
        _logger.info('BASE SYSTEM INITIALIZED')
        self._common_init_restart(state)
        _logger.info('ALPS SYSTEM COMPONENT READY TO RUN')
        _logger.info('Reinitilaization complete in %s sec.', (time.time() -
                start_time))

    def save_me(self):
        '''Automatically save a copy of the state of the system component.'''
        #should we be holding the block lock as well?
        Component.save(self)
    save_me = automatic(save_me, SAVE_ME_INTERVAL)

    def _init_nodes_and_reservations(self):
        '''Initialize nodes from ALPS bridge data'''

        retnodes = {}
        pending = True
        while pending:
            try:
                # None of these queries has strictly degenerate data.  Inventory
                # is needed for raw reservation data.  System gets memory and a
                # much more compact representation of data.  Reservednodes gives
                # which notes are reserved.
                inventory = ALPSBridge.fetch_inventory()
                _logger.info('INVENTORY FETCHED')
                system = ALPSBridge.extract_system_node_data(ALPSBridge.system())
                _logger.info('SYSTEM DATA FETCHED')
                reservations = ALPSBridge.fetch_reservations()
                _logger.info('ALPS RESERVATION DATA FETCHED')
                # reserved_nodes = ALPSBridge.reserved_nodes()
                ssd_enabled = ALPSBridge.fetch_ssd_enable()
                _logger.info('CAPMC SSD ENABLED DATA FETCHED')
                ssd_info = ALPSBridge.fetch_ssd_static_data()
                _logger.info('CAPMC SSD DETAIL DATA FETCHED')
                ssd_diags = ALPSBridge.fetch_ssd_diags()
                _logger.info('CAPMC SSD DIAG DATA FETCHED')
            except Exception:
                #don't crash out here.  That may trash a statefile.
                _logger.error('Possible transient encountered during initialization. Retrying.',
                        exc_info=True)
                Cobalt.Util.sleep(10)
            else:
                pending = False

        self._assemble_nodes(inventory, system, ssd_enabled, ssd_info, ssd_diags)
        #Reversing the node name to id lookup is going to save a lot of cycles.
        for node in self.nodes.values():
            self.node_name_to_id[node.name] = node.node_id
        _logger.info('NODE INFORMATION INITIALIZED')
        _logger.info('ALPS REPORTS %s NODES', len(self.nodes))
        # self._assemble_reservations(reservations, reserved_nodes)
        return

    def _assemble_nodes(self, inventory, system, ssd_enabled, ssd_info, ssd_diags):
        '''merge together the INVENTORY and SYSTEM query data to form as
        complete a picture of a node as we can.

        Args:
            inventory - ALPS QUERY(INVENTORY) data
            system - ALPS QUERY(SYSTEM) data
            ssd_enable - CAPMC get_ssd_enable data
            ssd_info - CAPMC get_ssds data
            ssd_diags - CAPMC get_ssd_diags data

        Returns:
            None

        Side Effects:
            Populates the node dictionary

        '''
        nodes = {}
        for nodespec in inventory['nodes']:
            node = CrayNode(nodespec)
            node.managed = True
            nodes[node.node_id] = node
        for node_id, nodespec in system.iteritems():
            nodes[node_id].attributes.update(nodespec['attrs'])
            # Should this be a different status?
            nodes[node_id].role = nodespec['role'].upper()
            if nodes[node_id].role.upper() not in ['BATCH']:
                nodes[node_id].status = 'down'
            nodes[node_id].status = nodespec['state']
        self._update_ssd_data(nodes, ssd_enabled, ssd_info, ssd_diags)
        self.nodes = nodes

    def _update_ssd_data(self, nodes, ssd_enabled=None, ssd_info=None, ssd_diags=None):
        '''Update/add ssd data from CAPMC'''
        if ssd_enabled is not None:
            for ssd_data in ssd_enabled['nids']:
                try:
                    nodes[str(ssd_data['nid'])].attributes['ssd_enabled'] = int(ssd_data['ssd_enable'])
                except KeyError:
                    _logger.warning('ssd info present for nid %s, but not reported in ALPS.', ssd_data['nid'])
        if ssd_info is not None:
            for ssd_data in ssd_info['nids']:
                try:
                    nodes[str(ssd_data['nid'])].attributes['ssd_info'] = ssd_data
                except KeyError:
                    _logger.warning('ssd info present for nid %s, but not reported in ALPS.', ssd_data['nid'])
        if ssd_diags is not None:
            for diag_info in ssd_diags['ssd_diags']:
                try:
                    node = nodes[str(diag_info['nid'])]
                except KeyError:
                    _logger.warning('ssd diag data present for nid %s, but not reported in ALPS.', ssd_data['nid'])
                else:
                    for field in ['life_remaining', 'ts', 'firmware', 'percent_used']:
                        node.attributes['ssd_info'][field] = diag_info[field]


    def _assemble_reservations(self, reservations, reserved_nodes):
        # FIXME: we can recover reservations now.  Implement this.
        pass

    def _gen_node_to_queue(self):
        '''(Re)Generate a mapping for fast lookup of node-id's to queues.'''
        with self._node_lock:
            self.nodes_by_queue = {}
            for node in self.nodes.values():
                for queue in node.queues:
                    if queue in self.nodes_by_queue.keys():
                        self.nodes_by_queue[queue].add(node.node_id)
                    else:
                        self.nodes_by_queue[queue] = set([node.node_id])

    @exposed
    def get_nodes(self, as_dict=False, node_ids=None, params=None, as_json=False):
        '''fetch the node dictionary.

            as_dict  - Return node information as a dictionary keyed to string
                        node_id value.
            node_ids - A list of node names to return, if None, return all nodes
                       (default None).
            params   - If requesting a dict, only request this list of
                       parameters of the node.
            json     - Encode to json before sending.  Useful on large systems.

            returns the node dictionary.  Can reutrn underlying node data as
            dictionary for XMLRPC purposes

        '''
        def node_filter(node):
            if node_ids is not None:
                return (str(node[0]) in [str(nid) for nid in node_ids])
            return True

        node_info = None
        if as_dict:
            retdict = {k:v.to_dict(True, params) for k, v in self.nodes.items()}
            node_info = dict(filter(node_filter, retdict.items()))
        else:
            node_info = dict(filter(node_filter, self.nodes.items()))
        if as_json:
            return json.dumps(node_info)
        return node_info

    def _run_update_state(self):
        '''automated node update functions on the update timer go here.'''

        def _run_and_wrap(func):
            try:
                func()
            except Exception:
                # Prevent this thread from dying.
                _logger.critical('Error in _run_update_state', exc_info=True)

        while True:
            # Each of these is wrapped in it's own log-and-preserve block.
            # The outer try is there to ensure the thread update timeout happens.
            _run_and_wrap(self.process_manager.update_launchers)
            _run_and_wrap(self.update_node_state)
            _run_and_wrap(self._get_exit_status)
            Cobalt.Util.sleep(UPDATE_THREAD_TIMEOUT)

    def _reconstruct_node(self, inven_node, inventory):
        '''Reconstruct a node from statefile information.  Needed whenever we
        find a new node.  If no statefile information from the orignal cobalt
        invocation exists, bring up a node in default states and mark node
        administratively down.

        This node was disabled and invisible to ALPS at the time Cobalt was
        initialized and so we have no current record of that node.

        '''
        nid = inven_node['node_id']
        new_node = None
        #construct basic node from inventory
        for node_info in inventory['nodes']:
            if int(node_info['node_id']) == int(nid):
                new_node = CrayNode(node_info)
                break
        if new_node is None:
            #we have a phantom node?
            self.logger.error('Unable to find inventory information for nid: %s', nid)
            return
        # if we have information from the statefile we need to repopulate the
        # node with the saved data.
        # Perhaps this should be how I construct all node data anyway?
        if self.init_spec is not None:
            node_info = self.init_spec.get('node_info', {})
            try:
                new_node.reset_info(node_info[str(nid)])
                self.logger.warning('Node %s reconstructed.', nid)
            except:
                self.logger.warning("Node nid: %s not found in restart information.  Bringing up node in a clean configuration.", nid, exc_info=True)
                #put into admin_down
                new_node.admin_down = True
                new_node.status = 'down'
                self.logger.warning('Node %s marked down.', nid)
        new_node.managed = True
        self.nodes[str(nid)] = new_node
        self.logger.warning('Node %s added to tracking.', nid)


    @exposed
    def update_node_state(self):
        '''update the state of cray nodes. Check reservation status and system
        stateus as reported by ALPS

        '''
        #Check clenaup progress.  Check ALPS reservations.  Check allocated
        #nodes.  If there is no resource reservation and the node is not in
        #current alps reservations, the node is ready to schedule again.
        now = time.time()
        startup_time_to_clear = []
        #clear pending starttimes.
        for jobid, start_time in self.pending_starts.items():
            if int(now) > int(start_time):
                startup_time_to_clear.append(jobid)
        for jobid in startup_time_to_clear:
            del self.pending_starts[jobid]

        self.check_killing_aprun()
        with self._node_lock:
            fetch_time_start = time.time()
            try:
                #I have seen problems with the kitchen-sink query here, where
                #the output gets truncated on it's way into Cobalt.
                #inventory = ALPSBridge.fetch_inventory(resinfo=True) #This is a full-refresh,
                #determine if summary may be used under normal operation
                #updated for >= 1.6 interface
                inven_nodes = ALPSBridge.extract_system_node_data(ALPSBridge.system())
                reservations = ALPSBridge.fetch_reservations()
                #reserved_nodes = ALPSBridge.reserved_nodes()
                # Fetch SSD diagnostic data and enabled flags. I would hope these change in event of dead ssd
                ssd_enabled = ALPSBridge.fetch_ssd_enable()
                ssd_diags = ALPSBridge.fetch_ssd_diags()
            except (ALPSBridge.ALPSError, ComponentLookupError):
                _logger.warning('Error contacting ALPS for state update.  Aborting this update',
                        exc_info=True)
                return
            inven_reservations = reservations.get('reservations', [])
            fetch_time_start = time.time()
            #_logger.debug("time in ALPS fetch: %s seconds", (time.time() - fetch_time_start))
            start_time = time.time()
            self._detect_rereservation(inven_reservations)
            # check our reservation objects.  If a res object doesn't correspond
            # to any backend reservations, this reservation object should be
            # dropped
            alps_res_to_delete = []
            current_alps_res_ids = [int(res['reservation_id']) for res in
                    inven_reservations]
            res_jobid_to_delete = []
            if self.alps_reservations == {}:
                # if we have nodes in cleanup-pending but no alps reservations,
                # then the nodes in cleanup pending are considered idle (or
                # at least not in cleanup).  Hardware check can catch these
                # later. This catches leftover reservations from hard-shutdowns
                # while running.
                for node in self.nodes.values():
                    if node.status in ['cleanup', 'cleanup-pending']:
                        node.status = 'idle'
            for alps_res in self.alps_reservations.values():
                if alps_res.jobid in self.pending_starts.keys():
                    continue #Get to this only after timeout happens
                #find alps_id associated reservation
                if int(alps_res.alps_res_id) not in current_alps_res_ids:
                    for node_id in alps_res.node_ids:
                        if not self.nodes[str(node_id)].reserved:
                            #pending hardware status update
                            self.nodes[str(node_id)].status = 'idle'
                    res_jobid_to_delete.append(alps_res.jobid)
                    _logger.info('job %s: Nodes %s cleanup complete.', alps_res.jobid, compact_num_list(alps_res.node_ids))
            for jobid in res_jobid_to_delete:
                _logger.info('%s: ALPS reservation for this job complete.', jobid)
                try:
                    del self.alps_reservations[str(jobid)]
                except KeyError:
                    _logger.warning('Job %s: Attempted to remove ALPS reservation for this job multiple times', jobid)
                if self.alps_reservations.get(int(jobid), None) is not None:
                    # in case of type leakage
                    _logger.warning('Job %s: ALPS reservation found with integer key: deleting', jobid)
                    del self.alps_reservations[jobid]
            #process group should already be on the way down since cqm released the
            #resource reservation
            cleanup_nodes = [node for node in self.nodes.values()
                             if node.status in ['cleanup-pending', 'cleanup']]
            #If we have a block marked for cleanup, send a release message.
            released_res_jobids = []
            cleaned_nodes = []
            for node in cleanup_nodes:
                found = False
                for alps_res in self.alps_reservations.values():
                    if str(node.node_id) in alps_res.node_ids:
                        found = True
                        if alps_res.jobid not in released_res_jobids:
                            #send only one release per iteration
                            apids = alps_res.release()
                            if apids is not None:
                                for apid in apids:
                                    self.signal_aprun(apid)
                            released_res_jobids.append(alps_res.jobid)
                if not found:
                    # There is no alps reservation to release, cleanup is
                    # already done.  This happens with very poorly timed
                    # qdel requests. Status will be set properly with the
                    # subsequent hardware status check.
                    _logger.info('Node %s cleanup complete.', node.node_id)
                    node.status = 'idle'
                    cleaned_nodes.append(node)
            for node in cleaned_nodes:
                cleanup_nodes.remove(node)

        #find hardware status
            #so we do this only once for nodes being added.
            #full inventory fetch is expensive.
            recon_inventory = None
            for inven_node in inven_nodes.values():
                if self.nodes.has_key(str(inven_node['node_id'])):
                    node = self.nodes[str(inven_node['node_id'])]
                    node.role = inven_node['role'].upper()
                    node.attributes.update(inven_node['attrs'])
                    if node.reserved:
                        #node marked as reserved.
                        if self.alps_reservations.has_key(str(node.reserved_jobid)):
                            node.status = 'busy'
                        else:
                            # check to see if the resource reservation should be
                            # released.
                            if node.reserved_until >= now:
                                node.status = 'allocated'
                            else:
                                node.release(user=None, jobid=None, force=True)
                    else:
                        node.status = inven_node['state'].upper()
                        if node.role.upper() not in ['BATCH'] and node.status is 'idle':
                            node.status = 'alps-interactive'
                else:
                    # Apparently, we CAN add nodes on the fly.  The node would
                    # have been disabled.  We need to add a new node and update
                    # it's state.
                    _logger.warning('Unknown node %s found. Starting reconstruction.', inven_node['node_id'])
                    try:
                        if recon_inventory is None:
                            recon_inventory = ALPSBridge.fetch_inventory()
                    except:
                        _logger.error('Failed to fetch inventory.  Will retry on next pass.', exc_info=True)
                    else:
                        self._reconstruct_node(inven_node, recon_inventory)
                   # _logger.error('UNS: ALPS reports node %s but not in our node list.',
                   #               inven_node['node_id'])
            # Update SSD data:
            self._update_ssd_data(self.nodes, ssd_enabled=ssd_enabled, ssd_diags=ssd_diags)
            #should down win over running in terms of display?
            #keep node that are marked for cleanup still in cleanup
            for node in cleanup_nodes:
                node.status = 'cleanup-pending'
        #_logger.debug("time in UNS lock: %s seconds", (time.time() - start_time))
        return

    def _detect_rereservation(self, inven_reservations):
        '''Detect and update the ALPS reservation associated with a running job.
        We are only concerned with BATCH reservations.  Others would be
        associated with running jobs, and should not be touched.

        '''
        def _construct_alps_res():
            with self._node_lock:
                job_nodes = [node.node_id for node in self.nodes.values()
                        if node.reserved_jobid == int(alps_res['batch_id'])]
            new_resspec = {'reserved_nodes': job_nodes,
                           'reservation_id': str(alps_res['reservation_id']),
                           'pagg_id': 0 #unknown.  Not used here.
                            }
            new_jobspec = {'jobid': int(alps_res['batch_id']),
                           'user' : alps_res['user_name']}

            return ALPSReservation(new_jobspec, new_resspec, self.nodes)

        replaced_reservation = None
        for alps_res in inven_reservations:
            try:
                #This traversal is terrible. May want to hide this in the API
                #somewhere
                if alps_res['ApplicationArray'][0]['Application'][0]['CommandArray'][0]['Command'][0]['cmd'] != 'BASIL':
                    # Not a reservation we're in direct control of.
                    continue
            except (KeyError, IndexError):
                #not a batch reservation
                continue
            if str(alps_res['batch_id']) in self.alps_reservations.keys():
                # This is a reservation we may already know about
                if (int(alps_res['reservation_id']) ==
                        self.alps_reservations[str(alps_res['batch_id'])].alps_res_id):
                    # Already know about this one
                    continue
                # we have a re-reservation.  If this has a batch id, we need
                # to add it to our list of tracked reservations, and inherit
                # other reservation details.  We can pull the reservation
                # information out of reserve_resources_until.

                # If this is a BATCH reservation and no hardware has that
                # reservation id, then this reservation needs to be released
                # Could happen if we have a job starting right at the RRU
                # boundary.
                new_alps_res = _construct_alps_res()
                tracked_res = self.alps_reservations.get(new_alps_res.jobid, None)
                if tracked_res is not None:
                    try:
                        apids = tracked_res.release()
                    except ALPSBridge.ALPSError:
                        # backend reservation probably is gone, which is why
                        # we are here in the first place.
                        pass
                self.alps_reservations[str(alps_res['batch_id'])] = new_alps_res
            else:
                #this is a basil reservation we don't know about already.
                new_alps_res = _construct_alps_res()
                if len(new_alps_res.node_ids) == 0:
                    # This reservation has no resources, so Cobalt's internal
                    # resource reservation tracking has no record.  This needs to
                    # be removed.
                    new_alps_res.release()
                else:
                    self.alps_reservations[str(alps_res['batch_id'])] = new_alps_res
        return

    def signal_aprun(self, aprun_id, signame='SIGINT'):
        '''Signal an aprun by aprun id (application_id).  Does not block.
        Use check_killing_aprun to determine completion/termination.  Does not
        depend on the host the aprun(s) was launched from.

        Input:
            aprun_id - integer application id number.
            signame  - string name of signal to send (default: SIGINT)
        Notes:
            Valid signals to apkill are:
            SIGHUP, SIGINT, SIGQUIT, SIGTERM, SIGABRT, SIGUSR1, SIGUSR2, SIGURG,
            and SIGWINCH (from apkill(1) man page.)  Also allowing SIGKILL.

        '''
        #Expect changes with an API updte

        #mark legal signals from docos
        if (signame not in ['SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGTERM', 'SIGABRT',
            'SIGUSR1', 'SIGUSR2', 'SIGURG','SIGWINCH', 'SIGKILL']):
            raise ValueError('%s is not a legal value for signame.', signame)
        try:
            retval = Cobalt.Proxy.ComponentProxy('system_script_forker').fork(
                    [APKILL_CMD, '-%s' % signame, '%d' % int(aprun_id)],
                    'aprun_termination', '%s cleanup:'% aprun_id)
            _logger.info("killing backend ALPS application_id: %s", aprun_id)
        except xmlrpclib.Fault:
            _logger.warning("XMLRPC Error while killing backend job: %s, will retry.",
                    aprun_id, exc_info=True)
        except:
            _logger.critical("Unknown Error while killing backend job: %s, will retry.",
                    aprun_id, exc_info=True)
        else:
            self.killing_jobs[aprun_id] = retval
        return

    def check_killing_aprun(self):
        '''Check that apkill commands have completed and clean them from the
        system_script_forker.  Allows for non-blocking cleanup initiation.

        '''

        try:
            system_script_forker = Cobalt.Proxy.ComponentProxy('system_script_forker')
        except:
            self.logger.critical("Cannot connect to system_script_forker.",
                    exc_info=True)
            return
        complete_jobs = []
        rev_killing_jobs = dict([(v,k) for (k,v) in self.killing_jobs.iteritems()])
        removed_jobs = []
        current_killing_jobs = system_script_forker.get_children(None, self.killing_jobs.values())

        for job in current_killing_jobs:
            if job['complete']:
                del self.killing_jobs[rev_killing_jobs[int(job['id'])]]
                removed_jobs.append(job['id'])
        system_script_forker.cleanup_children(removed_jobs)
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
        node_active_queues = set([])
        self.current_equivalence_classes = [] #reverse mapping of queues to nodes
        for node in self.nodes.values():
            if node.managed and node.schedulable:
                #only condiser nodes that we are scheduling.
                node_active_queues = set([])
                for queue in node.queues:
                    if queue in active_queue_names:
                        node_active_queues.add(queue)
                if node_active_queues == set([]):
                    #this node has nothing active.  The next check can get
                    #expensive, so skip it.
                    continue
            #determine the queues that overlap.  Hardware has to be included so
            #that reservations can be mapped into the equiv classes.
            found_a_match = False
            for e in equiv:
                for queue in node_active_queues:
                    if queue in e['queues']:
                        e['data'].add(node.node_id)
                        e['queues'] = e['queues'] | set(node_active_queues)
                        found_a_match = True
                        break
                if found_a_match:
                    break
            if not found_a_match:
                equiv.append({'queues': set(node_active_queues),
                              'data': set([node.node_id]),
                              'reservations': set()})
        #second pass to merge queue lists based on hardware
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
        #add in reservations:
        for eq_class in equiv:
            for res_name in reservation_dict:
                for node_hunk in reservation_dict[res_name].split(":"):
                    for node_id in expand_num_list(node_hunk):
                        if str(node_id) in eq_class['data']:
                            eq_class['reservations'].add(res_name)
                            break
            #don't send what could be a large block list back in the returun
            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
            self.current_equivalence_classes.append(eq_class)
        return equiv

    def _setup_special_locations(self, job):
        forbidden = set([str(loc) for loc in chain_loc_list(job.get('forbidden', []))])
        required = set([str(loc) for loc in chain_loc_list(job.get('required', []))])
        requested_locations = set([str(n) for n in expand_num_list(job['attrs'].get('location', ''))])
        # If ssds are required, add nodes without working SSDs to the forbidden list
        ssd_unavail = set([])
        if job.get('attrs', {}).get("ssds", "none").lower() == "required":
            ssd_min_size = int(job.get('attrs', {}).get("ssd_size", DEFAULT_MIN_SSD_SIZE)) * 1000000000 #convert to bytes
            ssd_unavail.update(set([str(node.node_id) for node in self.nodes.values()
                                  if (node.attributes['ssd_enabled'] == 0 or
                                      int(node.attributes.get('ssd_info', {'size': DEFAULT_MIN_SSD_SIZE})['size'])  < ssd_min_size)
                                ]))
        return (forbidden, required, requested_locations, ssd_unavail)

    def _assemble_queue_data(self, job, idle_only=True, drain_time=None):
        '''put together data for a queue, or queue-like reservation structure.

        Input:
            job - dictionary of job data.
            idle_only - [default: True] if True, return only idle nodes.
                        Otherwise return nodes in any non-down status.

        return count of idle resources, and a list of valid nodes to run on.
        if idle_only is set to false, returns a set of candidate draining nodes.


        '''
        # RESERVATION SUPPORT: Reservation queues are ephemeral, so we will
        # not find the queue normally. In the event of a reservation we'll
        # have to intersect required nodes with the idle and available
        # we also have to forbid a bunch of locations, in  this case.
        unavailable_nodes = []
        forbidden, required, requested_locations, ssd_unavail = self._setup_special_locations(job)
        requested_loc_in_forbidden = False
        for loc in requested_locations:
            if loc in forbidden:
                #don't spam the logs.
                requested_loc_in_forbidden = True
                break
        if job['queue'] not in self.nodes_by_queue.keys():
            # Either a new queue with no resources, or a possible
            # reservation need to do extra work for a reservation
            node_id_list = list(required - forbidden - ssd_unavail)
        else:
            node_id_list = list(set(self.nodes_by_queue[job['queue']]) - forbidden - ssd_unavail)
        if requested_locations != set([]): # handle attrs location= requests
            job_set = set([str(nid) for nid in requested_locations])
            if job['queue'] not in self.nodes_by_queue.keys():
                #we're in a reservation and need to further restrict nodes.
                if job_set <= set(node_id_list):
                    # We are in a reservation there are no forbidden nodes.
                    node_id_list = list(requested_locations - ssd_unavail)
                else:
                    # We can't run this job.  Insufficent resources in this
                    # reservation to do so.  Don't risk blocking anything.
                    node_id_list = []
            else:
                #normal queues.  Restrict to the non-reserved nodes.
                if job_set <= set([str(node_id) for node_id in
                                    self.nodes_by_queue[job['queue']]]):
                    node_id_list = list(requested_locations)
                    if not set(node_id_list).isdisjoint(forbidden):
                        # this job has requested locations that are a part of an
                        # active reservation.  Remove locaitons and drop available
                        # nodecount appropriately.
                        node_id_list = list(set(node_id_list) - forbidden - ssd_unavail)
                    if not requested_loc_in_forbidden:
                        raise ValueError("forbidden locations not in queue")
        with self._node_lock:
            if idle_only:
                unavailable_nodes = [node_id for node_id in node_id_list
                        if self.nodes[str(node_id)].status not in ['idle']]
            else:
                unavailable_nodes = [node_id for node_id in node_id_list
                        if self.nodes[str(node_id)].status in
                        self.nodes[str(node_id)].DOWN_STATUSES]
            if drain_time is not None:
                unavailable_nodes.extend([node_id for node_id in node_id_list
                    if (self.nodes[str(node_id)].draining and
                        (self.nodes[str(node_id)].drain_until - BACKFILL_EPSILON) < int(drain_time))])
        for node_id in set(unavailable_nodes):
            node_id_list.remove(node_id)
        return sorted(node_id_list, key=lambda nid: int(nid))

    def _select_first_nodes(self, job, node_id_list):
        '''Given a list of nids, select the first node count nodes fromt the
        list.  This is the target for alternate allocator replacement.

        Input:
            job - dictionary of job data from the scheduler
            node_id_list - a list of possible candidate nodes

        Return:
            A list of nodes.  [] if insufficient nodes for the allocation.

        Note: hold the node lock while doing this.  We really don't want a
        update to happen while doing this.

        '''
        ret_nodes = []
        with self._node_lock:
            if int(job['nodes']) <= len(node_id_list):
                node_id_list.sort(key=lambda nid: int(nid))
                ret_nodes = node_id_list[:int(job['nodes'])]
        return ret_nodes

    def _select_first_nodes_prefer_memory_match(self, job, node_id_list):
        '''Given a list of nids, select the first node count nodes fromt the
        list.  Prefer nodes that match the memory modes for a given job, then
        go in nid order.

        Input:
            job - dictionary of job data from the scheduler
            node_id_list - a list of possible candidate nodes

        Return:
            A list of nodes.  [] if insufficient nodes for the allocation.

        Note: hold the node lock while doing this.  We really don't want a
        update to happen while doing this.

        '''
        ssd_required = (job.get('attrs', {}).get("ssds", "none").lower() == "required")
        if job.get('attrs', {}).get('mcdram', None) is None or job.get('attrs', {}).get('numa', None) is None:
            # insufficient information to include a mode match
            return self._select_first_nodes(job, node_id_list)
        ret_nids = []
        with self._node_lock:
            considered_nodes = [node for node in self.nodes.values() if node.node_id in node_id_list]
            for node in considered_nodes:
                if (node.attributes['hbm_cache_pct'] == MCDRAM_TO_HBMCACHEPCT[job['attrs']['mcdram']] and
                        node.attributes['numa_cfg'] == job['attrs']['numa']):
                    ret_nids.append(int(node.node_id))
            if len(ret_nids) < int(job['nodes']):
                node_id_list.sort(key=lambda nid: int(nid))
                for nid in node_id_list:
                    if int(nid) not in ret_nids:
                        ret_nids.append(int(nid))
                        if len(ret_nids) >= int(job['nodes']):
                            break
        return ret_nids[:int(job['nodes'])]


    def _associate_and_run_immediate(self, job, resource_until_time, node_id_list):
        '''Given a list of idle node ids, choose a set that can run a job
        immediately, if a set exists in the node_id_list.

        Inputs:
            job - Dictionary of job data
            node_id_list - a list of string node id values

        Side Effects:
            Will reserve resources in ALPS and will set resource reservations on
            allocated nodes.

        Return:
            None if no match, otherwise the pairing of a jobid and set of nids
            that have been allocated to a job.

        '''
        compact_locs = None
        if int(job['nodes']) <= len(node_id_list):
            #this job can be run immediately
            to_alps_list = self._select_first_nodes_prefer_memory_match(job, node_id_list)
            job_locs = self._ALPS_reserve_resources(job, resource_until_time,
                    to_alps_list)
            if job_locs is not None and len(job_locs) == int(job['nodes']):
                compact_locs = compact_num_list(job_locs)
                #temporary reservation until job actually starts
                self.pending_starts[job['jobid']] = resource_until_time
                self.reserve_resources_until(compact_locs, resource_until_time, job['jobid'])
        return compact_locs

    @locking
    @exposed
    def find_job_location(self, arg_list, end_times, pt_blocking_locations=[]):
        '''Given a list of jobs, and when jobs are ending, return a set of
        locations mapped to a jobid that can be run.  Also, set up draining
        as-needed to run top-scored jobs and backfill when possible.

        Called once per equivalence class.

        Args::
            arg_list: A list of dictionaries containning information on jobs to
                   cosnider.
            end_times: list containing a mapping of locations and the times jobs
                    runninng on those locations are scheduled to end.  End times
                    are in seconds from Epoch UTC.
            pt_blocking_locations: Not used for this system.  Used in partitioned
                                interconnect schemes. A list of locations that
                                should not be used to prevent passthrough issues
                                with other scheduler reservations.

        Returns:
        A mapping of jobids to locations to run a job to run immediately.

        Side Effects:
        May set draining flags and backfill windows on nodes.
        If nodes are being returned to run, set ALPS reservations on them.

        Notes:
        The reservation set on ALPS resources is uncomfirmed at this point.
        This reservation may timeout.  The forker when it confirms will detect
        this and will re-reserve as needed.  The alps reservation id may change
        in this case post job startup.

        pt_blocking_locations may be used later to block out nodes that are
        impacted by warmswap operations.

        This function *DOES NOT* hold the component lock.

        '''
        now = time.time()
        resource_until_time = now + TEMP_RESERVATION_TIME
        with self._node_lock:
            # only valid for this scheduler iteration.
            self._clear_draining_for_queues(arg_list[0]['queue'])
            #check if we can run immedaitely, if not drain.  Keep going until all
            #nodes are marked for draining or have a pending run.
            best_match = {} #jobid: list(locations)
            for job in arg_list:
                label = '%s/%s' % (job['jobid'], job['user'])
                # walltime is in minutes.  We should really fix the storage of
                # that --PMR
                job_endtime = now + (int(job['walltime']) * 60)
                try:
                    node_id_list = self._assemble_queue_data(job, drain_time=job_endtime)
                    available_node_list = self._assemble_queue_data(job, idle_only=False)
                except ValueError:
                    _logger.warning('Job %s: requesting locations that are not in requested queue.',
                            job['jobid'])
                    continue
                if int(job['nodes']) > len(available_node_list):
                    # Insufficient operational nodes for this job at all
                    continue
                elif len(node_id_list) == 0:
                    pass #allow for draining pass to run.
                elif int(job['nodes']) <= len(node_id_list):
                    # enough nodes are in a working state to consider the job.
                    # enough nodes are idle that we can run this job
                    compact_locs = self._associate_and_run_immediate(job,
                            resource_until_time, node_id_list)
                    # do we want to allow multiple placements in a single
                    # pass? That would likely help startup times.
                    if compact_locs is not None:
                        best_match[job['jobid']] = [compact_locs]
                        _logger.info("%s: Job selected for running on nodes  %s",
                                label, compact_locs)
                        break #for now only select one location
                if DRAIN_MODE in ['backfill', 'drain-only']:
                    # drain sufficient nodes for this job to run
                    drain_node_ids = self._select_nodes_for_draining(job,
                            end_times)
                    if drain_node_ids != []:
                        _logger.info('%s: nodes %s selected for draining.', label,
                                compact_num_list(drain_node_ids))
        return best_match

    def _ALPS_reserve_resources(self, job, new_time, node_id_list):
        '''Call ALPS to reserve resrources.  Use their allocator.  We can change
        this later to substitute our own allocator if-needed.

        Input:
        Nodecount - number of nodes to reserve for  a job.

        Returns: a list of locations that ALPS has reserved.

        Side effects:
        Places an ALPS reservation on resources.  Calls reserve resources until
        on the set of nodes, and will mark nodes as allocated.

        '''
        try:
            res_info = ALPSBridge.reserve(job['user'], job['jobid'],
                int(job['nodes']), job['attrs'], node_id_list)
        except ALPSBridge.ALPSError as exc:
            _logger.warning('unable to reserve resources from ALPS: %s', exc.message)
            return None
        new_alps_res = None
        if res_info is not None:
            new_alps_res = ALPSReservation(job, res_info, self.nodes)
            self.alps_reservations[str(job['jobid'])] = new_alps_res
        else:
            _logger.warning('Job %s: Attempted reservation but allocator returned no nodes.', job['jobid'])
            return None
        return new_alps_res.node_ids

    def _clear_draining_for_queues(self, queue):
        '''Given a list of queues, remove the draining flags on nodes.

        queues - a queue in an equivalence class to consider.  This will clear
        the entire equiv class

        return - none

        Note: does not acquire block lock.  Must be locked externally.

        '''
        now = int(time.time())
        current_queues = []
        for equiv_class in self.current_equivalence_classes:
            if queue in equiv_class['queues']:
                current_queues = equiv_class['queues']
        if current_queues:
            with self._node_lock:
                for node in self.nodes.values():
                    for q in node.queues:
                        if q in current_queues:
                            node.clear_drain()

    def _select_nodes_for_draining(self, job, end_times):
        '''Select nodes to be drainined.  Set backfill windows on draining
        nodes.

        Inputs:
            job - dictionary of job information to consider
            end_times - a list of nodes and their endtimes should be sorted
                        in order of location preference

        Side Effect:
            end_times will be sorted in ascending end-time order

        Return:
            List of node ids that have been selected for draining for this job,
            as well as the expected drain time.

        '''
        now = int(time.time())
        end_times.sort(key=lambda x: int(x[1]))
        drain_list = []
        candidate_list = []
        cleanup_statuses = ['cleanup', 'cleanup-pending']
        forbidden, required, requested_locations, ssd_unavail = self._setup_special_locations(job)
        try:
            node_id_list = self._assemble_queue_data(job, idle_only=False)
        except ValueError:
            _logger.warning('Job %s: requesting locations that are not in queue.', job['jobid'])
        else:
            with self._node_lock:
                drain_time = None
                candidate_drain_time = None
                # remove the following from the list:
                # 1. idle nodes that are already marked for draining.
                # 2. Nodes that are in an in-use status (busy, allocated).
                # 3. Nodes marked for cleanup that are not allocated to a real
                #    jobid. CLEANING_ID is a sentiel jobid value so we can set
                #    a drain window on cleaning nodes easiliy.  Not sure if this
                #    is the right thing to do. --PMR
                candidate_list = []
                candidate_list = [nid for nid in node_id_list
                        if (not self.nodes[str(nid)].draining and
                            (self.nodes[str(nid)].status in ['idle']) or
                            (self.nodes[str(nid)].status in cleanup_statuses)
                            )]
                for nid in candidate_list:
                    if self.nodes[str(nid)].status in cleanup_statuses:
                        candidate_drain_time = now + CLEANUP_DRAIN_WINDOW
                for loc_time in end_times:
                    running_nodes = [str(nid) for nid in
                            expand_num_list(",".join(loc_time[0]))
                            if ((job['queue'] in self.nodes[str(nid)].queues or
                                nid in required) and
                                not self.nodes[str(nid)].draining)]
                    for nid in running_nodes:
                        # We set a drain on all running nodes for use in a later
                        # so that we can "favor" draining on the longest
                        # running set of nodes.
                        if (self.nodes[str(nid)].status != 'down' and
                                self.nodes[str(nid)].managed):
                            self.nodes[str(nid)].set_drain(loc_time[1], job['jobid'])
                    candidate_list.extend([nid for nid in running_nodes if
                        self.nodes[str(nid)].draining])
                    candidate_drain_time = int(loc_time[1])
                    if len(candidate_list) >= int(job['nodes']):
                        # Enough nodes have been found to drain for this job
                        break
                candidates = set(candidate_list)
                # We need to further restrict this list based on requested
                # location and reservation avoidance data:
                if forbidden != set([]):
                    candidates = candidates.difference(forbidden)
                if ssd_unavail != set([]):
                    candidates = candidates.difference(ssd_unavail)
                if requested_locations != set([]):
                    candidates = candidates.intersection(requested_locations)
                candidate_list = list(candidates)
                if len(candidate_list) >= int(job['nodes']):
                    drain_time = candidate_drain_time
                if drain_time is not None:
                    # order the node ids by id and drain-time. Longest drain
                    # first
                    candidate_list.sort(key=lambda nid: int(nid))
                    candidate_list.sort(reverse=True,
                            key=lambda nid: self.nodes[str(nid)].drain_until)
                    drain_list = candidate_list[:int(job['nodes'])]
                    for nid in drain_list:
                        self.nodes[str(nid)].set_drain(drain_time, job['jobid'])
        return drain_list

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
        completed = False
        with self._node_lock:
            succeeded_nodes = []
            failed_nodes = []
            #assemble from locaion list:
            exp_location = []
            if isinstance(location, list):
                exp_location = chain_loc_list(location)
            elif isinstance(location, str):
                exp_location = expand_num_list(location)
            else:
                raise TypeError("location type is %s.  Must be one of 'list' or 'str'", type(location))
            if new_time is not None:
                #reserve the location. Unconfirmed reservations will have to
                #be lengthened.  Maintain a list of what we have reserved, so we
                #extend on the fly, and so that we don't accidentally get an
                #overallocation/user
                for loc in exp_location:
                    # node = self.nodes[self.node_name_to_id[loc]]
                    node = self.nodes[str(loc)]
                    try:
                        node.reserve(new_time, jobid=jobid)
                        succeeded_nodes.append(int(loc))
                    except Cobalt.Exceptions.ResourceReservationFailure as exc:
                        self.logger.error(exc)
                        failed_nodes.append(loc)
                self.logger.info("job %s: nodes '%s' now reserved until %s",
                    jobid, compact_num_list(succeeded_nodes),
                    time.asctime(time.gmtime(new_time)))
                if failed_nodes != []:
                    self.logger.warning("job %s: failed to reserve nodes '%s'",
                        jobid, compact_num_list(failed_nodes))
                else:
                    completed = True
            else:
                #release the reservation and the underlying ALPS reservation
                #and the reserration on blocks.
                for loc in exp_location:
                    # node = self.nodes[self.node_name_to_id[loc]]
                    node = self.nodes[str(loc)]
                    try:
                        node.release(user=None, jobid=jobid)
                        succeeded_nodes.append(int(loc))
                    except Cobalt.Exceptions.ResourceReservationFailure as exc:
                        self.logger.error(exc)
                        failed_nodes.append(loc)
                    #cleanup pending has to be dealt with.  Do this in UNS for
                    #now
                self.logger.info("job %s: nodes '%s' released. Cleanup pending.",
                    jobid, compact_num_list(succeeded_nodes))
                if failed_nodes != []:
                    self.logger.warning("job %s: failed to release nodes '%s'",
                        jobid, compact_num_list(failed_nodes))
                else:
                    completed = True
        return completed

    @exposed
    def add_process_groups(self, specs):
        '''Add process groups and start their runs.  Adjust the resource
        reservation time to full run time at this point.

        Args:
            specs: A list of dictionaries that contain information on the Cobalt
                   job required to start the backend process.

        Returns:
            A created process group object.  This is wrapped and sent via XMLRPC
            to the caller.

        Side Effects:
            Invokes a forker component to run a user script.  In the event of a
            fatal startup error, will release resource reservations.

        '''
        start_apg_timer = int(time.time())

        for spec in specs:
            spec['forker'] = None
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
            except ComponentLookupError:
                _logger.error("%s: failed to contact the %s component",
                        pgroup.label, pgroup.forker)
                #this should be reraised and the queue-manager handle it
                #that would allow re-requesting the run instead of killing the
                #job --PMR
            except xmlrpclib.Fault:
                _logger.error("%s: a fault occurred while attempting to start "
                        "the process group using the %s component",
                        pgroup.label, pgroup.forker)
                pgroup.exit_status = 255
                self.reserve_resources_until(pgroup.location, None,
                        pgroup.jobid)
            except Exception:
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

        # process_groups = [pg for pg in
                          # self.process_manager.process_groups.q_get(specs)
                          # if pg.exit_status is not None]
        return self.process_manager.cleanup_groups([pg.id for pg in
            self.process_manager.process_groups.q_get(specs)
            if pg.exit_status is not None])
        # for process_group in process_groups:
            # del self.process_manager.process_groups[process_group.idh
        # return process_groups

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
        for pgroup in completed_pgs:
            _logger.info('%s: process group reported as completed with status %s',
                    pgroup.label, pgroup.exit_status)
            self.reserve_resources_until(pgroup.location, None, pgroup.jobid)
        return

    @exposed
    def validate_job(self, spec):
        '''Basic validation of a job to run on a cray system.  Make sure that
        certain arguments have been passsed in.  On failure raise a
        JobValidationError.

        '''
        #set default memory modes.
        if spec.get('attrs', None) is None:
            spec['attrs'] = {'mcdram': DEFAULT_MCDRAM_MODE, 'numa': DEFAULT_NUMA_MODE}
        else:
            if spec['attrs'].get('mcdram', None) is None:
                spec['attrs']['mcdram'] = DEFAULT_MCDRAM_MODE
            if spec['attrs'].get('numa', None) is None:
                spec['attrs']['numa'] = DEFAULT_NUMA_MODE
        # It helps when the mode requested actually exists.
        if spec['attrs']['mcdram'] not in VALID_MCDRAM_MODES:
            raise JobValidationError('mcdram %s not valid must be one of: %s'% (spec['attrs']['mcdram'],
                    ', '.join(VALID_MCDRAM_MODES)))
        if spec['attrs']['numa'] not in VALID_NUMA_MODES:
            raise JobValidationError('numa %s not valid must be one of: %s' % (spec['attrs']['numa'],
                    ', '.join(VALID_NUMA_MODES)))
        # mode on this system defaults to script.
        mode = spec.get('mode', None)
        if ((mode is None) or (mode == False)):
            spec['mode'] = 'script'
        if spec['mode'] not in ['script', 'interactive']:
            raise JobValidationError("Mode %s is not supported on Cray systems." % mode)
        # FIXME: Pull this out of the system configuration from ALPS ultimately.
        # For now, set this from config for the PE count per node
        spec['nodecount'] = int(spec['nodecount'])
        # proccount = spec.get('proccount', None)
        # if proccount is None:
            # nodes *
        if spec['nodecount'] > self.system_size:
            raise JobValidationError('Job requested %s nodes.  Maximum permitted size is %s' %
                    (spec['nodecount'], self.system_size))
        spec['proccount'] = spec['nodecount'] #set multiplier for default depth
        mode = spec.get('mode', 'script')
        spec['mode'] = mode
        if mode == 'interactive':
            # Handle which script host should handle their job if they're on a
            # login.
            if spec.get('qsub_host', None) in ELOGIN_HOSTS:
                try:
                    spec['ssh_host'] = self.process_manager.select_ssh_host()
                except RuntimeError:
                    spec['ssh_host'] = None
                if spec['ssh_host'] is None:
                    raise JobValidationError('No valid SSH host could be found for interactive job.')
        return spec

    @exposed
    def verify_locations(self, nodes):
        '''verify that a list of nodes exist on this system.  Return the list
        that can be found.

        '''
        good_nodes = [node for node in nodes if str(node) in self.nodes.keys()]
        return good_nodes

    @exposed
    def update_nodes(self, updates, node_list, user):
        '''Apply update to a node's status from an external client.

        Updates apply to all nodes.  User is for logging purposes.

        node_list should be a list of nodeids from the cray system

        Hold the node lock while doing this.

        Force a status update while doing this operation.

        '''
        mod_nodes = []
        with self._node_lock:
            for node_id in node_list:
                node = self.nodes[str(node_id)]
                try:
                    if updates.get('down', False):
                        node.admin_down = True
                        node.status = 'down'
                    elif updates.get('up', False):
                        node.admin_down = False
                        node.status = 'idle'
                    elif updates.get('queues', None):
                        node.queues = list(updates['queues'].split(':'))
                except Exception:
                    _logger.error("Unexpected exception encountered!", exc_info=True)
                else:
                    mod_nodes.append(node_id)
        if updates.get('queues', False):
            self._gen_node_to_queue()
        if mod_nodes != []:
            self.update_node_state()
        _logger.info('Updates %s applied to nodes %s by %s', updates,
                compact_num_list(mod_nodes), user)
        return mod_nodes

    @exposed
    def confirm_alps_reservation(self, specs):
        '''confirm or rereserve if needed the ALPS reservation for an
        interactive job.

        '''
        try:
            pg = None
            for pgroup in self.process_manager.process_groups.values():
                if pgroup.jobid == int(specs['jobid']):
                    pg = pgroup
            #pg = self.process_manager.process_groups[int(specs['pg_id'])]
            pg_id = int(specs['pgid'])
        except KeyError:
            raise
        if pg is None:
            raise ValueError('invalid jobid specified')
        # Try to find the alps_res_id for this job.  if we don't have it, then we
        # need to reacquire the source reservation.  The job locations will be
        # critical for making this work.
        with self._node_lock:
            # do not want to hit this during an update.
            alps_res = self.alps_reservations.get(str(pg.jobid), None)
            # find nodes for jobid.  If we don't have sufficient nodes, job
            # should die
            job_nodes = [node for node in self.nodes.values()
                            if node.reserved_jobid == pg.jobid]
            nodecount = len(job_nodes)
            if nodecount == 0:
                _logger.warning('%s: No nodes reserved for job.', pg.label)
                return False
            new_time = job_nodes[0].reserved_until
            node_list = compact_num_list([node.node_id for node in job_nodes])
        if alps_res is None:
            job_info = {'user': specs['user'],
                        'jobid':specs['jobid'],
                        'nodes': nodecount,
                        'attrs': {},
                        }
            self._ALPS_reserve_resources(job_info, new_time, expand_num_list(node_list))
            alps_res = self.alps_reservations.get(str(pg.jobid), None)
            if alps_res is None:
                _logger.warning('%s: Unable to re-reserve ALPS resources.',
                        pg.label)
                return False

        # try to confirm, if we fail at confirmation, try to reserve same
        # resource set again
        _logger.info('%s/%s: confirming with pagg_id %s', specs['jobid'],
                specs['user'], pg_id)
        ALPSBridge.confirm(int(alps_res.alps_res_id), pg_id)
        return True

    @exposed
    def interactive_job_complete (self, jobid):
        """Will terminate the specified interactive job
        """
        job_not_found = True
        for pg in self.process_manager.process_groups.itervalues():
            if pg.jobid == jobid:
                job_not_found = False
                if pg.mode == 'interactive':
                    pg.interactive_complete = True
                else:
                    msg = "Job %s not an interactive" % str(jobid)
                    self.logger.error(msg)
                    raise JobNotInteractive(msg)
                break
        if job_not_found:
            self.logger.warning("%s: Interactive job not found", str(jobid))
        return

class ALPSReservation(object):
    '''Container for ALPS Reservation information.  Can be used to update
    reservations and also internally relases reservation.

    Should be built from an ALPS reservation response dict as returned by the
    bridge.

    '''

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
        _logger.info('ALPS Reservation %s registered for job %s',
                self.alps_res_id, self.jobid)

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
        _logger.info('ALPS Reservation %s confirmed for job %s',
                self.alps_res_id, self.jobid)

    def release(self):
        '''Release an underlying ALPS reservation.

        Note:
        A reservation may remain if there are still active claims.  When all
        claims are gone

        Returns a list of apids and child_ids for the system script forker
        for any apids that are still cleaning.

        '''
        if self.dying:
            #release already issued.  Ignore
            return
        apids = []
        status = ALPSBridge.release(self.alps_res_id)
        if int(status['claims']) != 0:
            _logger.info('ALPS reservation: %s still has %s claims.',
                    self.alps_res_id, status['claims'])
            # fetch reservation information so that we can send kills to
            # interactive apruns.
            resinfo = ALPSBridge.fetch_reservations()
            apids = _find_non_batch_apids(resinfo['reservations'], self.alps_res_id)
        else:
            _logger.info('ALPS reservation: %s has no claims left.',
                self.alps_res_id)
        self.dying = True
        return apids

def _find_non_batch_apids(resinfo, alps_res_id):
    '''Extract apids from non-basil items.'''
    apids = []
    for alps_res in resinfo:
        if str(alps_res['reservation_id']) == str(alps_res_id):
            #wow, this is ugly. Traversing the XML from BASIL
            for applications in alps_res['ApplicationArray']:
                for application in applications.values():
                    for app_data in application:
                        # applicaiton id is at the app_data level.  Multiple
                        # commands don't normally happen.  Maybe in a MPMD job?
                        # All commands will have the same applicaiton id.
                        for commands in app_data['CommandArray']:
                            for command in commands.values():
                                # BASIL is the indicaiton of a apbasil
                                # reservation.  apruns with the application of
                                # BASIL would be an error.
                                if command[0]['cmd'] != 'BASIL':
                                    apids.append(app_data['application_id'])
    return apids
