"""Cray-specific node information"""

from Cobalt.Components.system.ClusterNode import ClusterNode

class CrayNode(ClusterNode):

    CRAY_STATE_MAP = {'UP': 'idle', 'DOWN':'down', 'UNAVAILABLE':'down',
            'ROUTING':'down', 'SUSPECT':'down', 'ADMIN':'down',
            'UNKNOWN':'down'}

    def __init__(self, spec):
        super(CrayNode, self).__init__(spec)
        print spec
        self.state = self.CRAY_STATE_MAP[spec['state'].upper()]
        self.node_id = spec['node_id']
        self.role = spec['role']
        self.attributes['architecture'] = spec['architecture']
        self.segment_details = spec['SocketArray']

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return str(to_dict)
