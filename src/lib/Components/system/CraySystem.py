"""Resource management for Cray ALPS based systems"""



from Cobalt.Components.base import Component, exposed
from Cobalt.Components.system.base_system import BaseSystem
import Cobalt.Components.system.AlpsBridge as AlpsBridge
from Cobalt.Components.system.CrayNode import CrayNode

import logging

logger = logging.getLogger(__name__)

class CraySystem(BaseSystem):

    name = "system"
    implementation = "alps_system"

    def __init__(self):
        '''Initialize system.  Read initial states from bridge.
        Get current state

        '''
        self.nodes = {}
        self.alps_reservations = {}
        self._init_nodes_and_reservations()

    def _init_nodes_and_reservations(self):
        '''Initialize nodes from ALPS bridge data'''

        retnodes = {}
        inventory = AlpsBridge.fetch_inventory()
        for nodespec in inventory['nodes']:
            node = CrayNode(nodespec)
            node.managed = True
            retnodes[node.name] = node
        self.nodes = retnodes
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
                    retdict[node.name] = node.to_dict()
                return retdict
            else:
                return self.nodes
        else:
            raise NotImplementedError


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
