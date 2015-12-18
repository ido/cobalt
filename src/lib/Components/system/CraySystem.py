"""Resource management for Cray ALPS based systems"""



from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Components.system.base_system import BaseSystem
import Cobalt.Components.system.AlpsBridge as AlpsBridge
from Cobalt.Components.system.CrayNode import CrayNode
from Cobalt.Components.system.base_pg_manager import ProcessGroupManager
import Cobalt.Util

import logging
import threading
import thread
import copy

_logger = logging.getLogger(__name__)

UPDATE_THREAD_TIMEOUT = 10 #TODO: Time in seconds, make setable

class CraySystem(BaseSystem):

    name = "system"
    implementation = "alps_system"
    logger = _logger

    def __init__(self, *args, **kwargs):
        '''Initialize system.  Read initial states from bridge.
        Get current state

        '''
        super(CraySystem, self).__init__(*args, **kwargs)
        #process manager setup
        self.process_manager = ProcessGroupManager()
        self.process_manager.forkers.append('user_script_forker')
        _logger.info('PROCESS MANAGER INTIALIZED')
        #resource management setup
        self.nodes = {}
        self.alps_reservations = {}
        self._init_nodes_and_reservations()
        #state update thread and lock
        self._node_lock = threading.Lock()
        self.node_update_thread = thread.start_new_thread(self._run_update_state,
                tuple())
        _logger.info('ALPS SYSTEM COMPONENT READY TO RUN.')

    def _init_nodes_and_reservations(self):
        '''Initialize nodes from ALPS bridge data'''

        retnodes = {}
        inventory = AlpsBridge.fetch_inventory(resinfo=True)
        for nodespec in inventory['nodes']:
            node = CrayNode(nodespec)
            node.managed = True
            retnodes[node.name] = node
        self.nodes = retnodes
        _logger.info('NODE INFORMATION INITIALIZED')
        _logger.info('ALPS REPORTS %s NODES', len(self.nodes))
        print [str(node) for node in self.nodes.values()]
        for resspec in inventory['reservations']:
            self.alps_reservations[resspec['reservation_id']] = ALPSReservation(resspec)

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
            Cobalt.Util.sleep(UPDATE_THREAD_TIMEOUT)

    @exposed
    def update_node_state(self):
        '''update the state of cray nodes. Check reservation status and system
        stateus as reported by ALPS

        '''
        with self._node_lock:
            original_nodes = copy.deepcopy(self.nodes)
        updates = {} #node_id and node to update
        inventory = AlpsBridge.fetch_inventory(resinfo=True) #This is a full-refresh,
                                                 #summary should be used otherwise
        inven_nodes  = inventory['nodes']
        inven_reservations = inventory['reservations']
        #find hardware status
        with self._node_lock:
            for inven_node in inven_nodes:
                if self.nodes.has_key(inven_node['name']):
                    self.nodes[inven_node['name']].status = inven_node['state'].upper()
                else:
                    # Cannot add nodes on the fly.  Or at lesat we shouldn't be
                    # able to.
                    _logger.error('UNS: ALPS reports node %s but not in our node list.',
                            inven_node['name'])
        #check/update reservation information and currently running locations?
        #fetch info from process group manager for currently running jobs.
        #should down win over running in terms of display?

        return


class ALPSReservation(object):

    def __init__(self, spec):
        self.jobid = spec['batch_id']
        self.node_ids = None
        self.pg_id = spec.get('pagg_id', None) #process group of executing script
        self.alps_res_id = spec['reservation_id']
        self.app_info = spec['ApplicationArray']
        self.user = spec['user_name']
        self.gid = spec['account_name'] #appears to be gid.

if __name__ == '__main__':

    cs = CraySystem()
    nodes = cs.get_nodes()

    for node_name, node in nodes.iteritems():
        print "Name: %s" % node_name
        for key, val in node.to_dict().iteritems():
            print "    %s: %s" % (key, val)

    for res_id, reservation in cs.alps_reservations.items():
        print "Resid: %s" % res_id
        for key, val in reservation.__dict__.items():
            print "    %s: %s" % (key, val)

