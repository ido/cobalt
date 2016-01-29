"""Cray-specific node information"""

from Cobalt.Components.system.ClusterNode import ClusterNode

class CrayNode(ClusterNode):

    CRAY_STATE_MAP = {'UP': 'idle', 'DOWN':'down', 'UNAVAILABLE':'down',
            'ROUTING':'down', 'SUSPECT':'down', 'ADMIN':'down',
            'UNKNOWN':'down'}

    def __init__(self, spec):
        super(CrayNode, self).__init__(spec)
        self._status = self.CRAY_STATE_MAP[spec['state'].upper()]
        self.node_id = spec['node_id']
        self.role = spec['role']
        self.attributes['architecture'] = spec['architecture']
        self.segment_details = spec['SocketArray']

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return str(self.to_dict())

    @property
    def status(self):
        return super(CrayNode, self).status

    @status.setter
    def status(self, new_status):
        '''set status using cray states, as well as internal state.
        also, coerce to allocated if we are used by something, but still marked
        idle.

        '''
        if new_status.upper() in self.CRAY_STATE_MAP.keys():
            self._status = self.CRAY_STATE_MAP[new_status.upper()]
        elif new_status in CrayNode.RESOURCE_STATUSES:
            self._status = new_status
        else:
            raise KeyError('%s is not a valid state for Cray Nodes.' % new_status)
        if self._status == 'idle' and self.reserved:
            self.status == 'allocated'

