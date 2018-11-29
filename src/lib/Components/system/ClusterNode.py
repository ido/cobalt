# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""General cluster node class.  This contains additional information that nodes
require that may not be needed for indirectly allocated resources like wires.

"""

from Cobalt.Components.system.resource import Resource
from Cobalt.Exceptions import UnschedulableNodeError
import time
import logging

_logger = logging.getLogger()

class ClusterNode(Resource):

    '''Cluster nodes have a few extra fields beyond the default resource
    fields:

    schedulable - should the node be scheduled.  If false this will cause a
                  node to be invisible in the user-level nodelist command.
    draining - If the node has a drain time set, this is True.
    drain_until - If the node is supposed to be drained, this is the time
                  the draining job is supposed to end, in seconds from
                  epoch.
    drain_jobid - The jobid that is setting the drain time.
    backfill_window - the time available for jobs that can be backfilled
                      onto the draining resource.
    backfill_epsilon - the time to subtract from the backfill window.
                       Default is 120 seconds.

    '''

    def __init__(self, spec):
        '''Initialize a ClusterNode object.'''
        super(ClusterNode, self).__init__(spec)
        self.queues = spec.get('queues', ['default']) #list of queues
        self.schedulable = spec.get('schedulable', True)
        self._drain_until = spec.get('drain_until', None)
        self._drain_jobid = spec.get('drain_jobid', None)
        self._backfill_epsilon = None
        self.backfill_epsilon = int(spec.get('backfill_epsilon', 120))

    def reset_info(self, node):
        '''reset node information on restart from a stored node object'''
        super(ClusterNode, self).reset_info(node)
        self.queues = node.queues
        self.schedulable = node.schedulable
        self._drain_until = node.drain_until
        self._drain_jobid = node.drain_jobid

    @property
    def drain_until(self):
        '''Time in seconds from epoch that the node will drain for.'''
        return self._drain_until

    @property
    def drain_jobid(self):
        '''Jobid that the node is waiting for.'''
        return self._drain_jobid

    @property
    def draining(self):
        '''Reutrn if a node is draining.  True if drain_until is set.'''
        return self.drain_until is not None

    @property
    def backfill_window(self, when=None):
        '''The time remaining on this node for backfilling in integer
        seconds.  This incorporates the backfill_epsilon for this node

        Inputs:
            when - The time to use to consider this backfill window.
                   Defaults to the value returned by time.time() at the time
                   of call.

        Output:
            None if node isn't being drained.  The time remaining in the
            drain minus the backfill_epsilon otherwise.

        '''
        now = time.time() if when is None else when
        backfill_time = None
        if self.drain_until is not None:
            backfill_time = int(
                    min(self.drain_until - now - self._backfill_epsilon, 0))
        return backfill_time

    def set_drain(self, drain_until, jobid):
        '''Set a node to draining and mark with the jobid that caused it.
        A non-schedulable node cannot be marked as draining.
        Inputs:
            drain_until - time in seconds from epoch that the job is scheduled
                          to drain until.
            jobid - the cobalt jobid of the job that we are waiting to end.

        Returns: None
        '''
        if not self.schedulable or self.status == 'down':
            err = '%s: Attempted to drain unscheduled or down node.' % self.name 
            _logger.warning(err)
            raise UnschedulableNodeError(err)

        self._drain_until = int(drain_until)
        self._drain_jobid = int(jobid)

    def clear_drain(self):
        '''Clear the draining data from a block.'''
        self._drain_until = None
        self._drain_jobid = None

    @property
    def backfill_epsilon(self):
        '''The time to subtract from the backfill window to most efficiently
        start the draining job.  Must be nonnegative value.  Time is in integer
        seconds.

        '''
        return self._backfill_epsilon

    @backfill_epsilon.setter
    def backfill_epsilon(self, epsilon):
        '''set the backfill epsilon.  Must be nonnegative'''
        if epsilon < 0:
            raise ValueError("epsilon must be a non-negative value")
        self._backfill_epsilon = int(epsilon)
