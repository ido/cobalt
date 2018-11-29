# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""Generic resource model for Cobalt.  This should be used as the base for any
allocatable resource.  Under certain circumstances this may also be used as a
base for a resource grouping, like a machine partition.

"""
import logging

from Cobalt.Exceptions import UnmanagedResourceError, InvalidStatusError
from Cobalt.Exceptions import ResourceReservationFailure

_logger = logging.getLogger()



class Resource(object):
    '''Generic resource class.  This may be used as a base for any schedulable
    resource in Cobalt.  Subclasses of Resource may contain aggregates of other
    resources as well.

    '''
    RESOURCE_STATUSES = ['idle', 'allocated', 'down', 'busy', 'cleanup',
                         'cleanup-pending']

    def __init__(self, spec):
        self.name = spec['name']
        self.attributes = spec.get('attributes', {})
        self._status = 'idle'
        self.reserved_by = None
        self.reserved_jobid = None
        self.reserved_until = None
        self.managed = False
        self.init_actions = []
        self.cleanup_actions = []
        self.admin_down = False

    def reset_info(self, node):
        '''reset node information on restart from a stored node object'''
        #self.attributes = node.attributes
        self.reserved_by = node.reserved_by
        self.reserved_jobid = node.reserved_jobid
        self.reserved_until = node.reserved_until
        self.managed = node.managed
        try:
            self.admin_down = node.admin_down
        except:
            self.admin_down = False

    def __hash__(self):
        '''Hash is the hash of the string name for the resource.'''
        return hash(self.name)

    def __str__(self):
        return "\n".join(["%s: %s," % (key, val) for key, val in self.__dict__.items()])

    @property
    def reserved(self):
        '''If true, the node is reserved'''
        return self.reserved_until is not None

    @property
    def status(self):
        '''The status of the underlying hardware.  This may only be set to
        resource statuses valid for a particular class. By default valid
        statuses are:

        idle - resource is free and ready to be scheduled
        allocated - resource is reserved for a job that is starting up
        busy - resource has job actively running on it
        cleanup - resource is in post-job cleanup
        down - resource is offline due to diagnostic failure or admin action

        '''
        return self._status

    @status.setter
    def status(self, value):
        '''set status, check for validity'''
        if value not in self.RESOURCE_STATUSES:
            raise InvalidStatusError('%s status invalid.  Must be one of %s' % \
                    (value, self.RESOURCE_STATUSES))
        if self.admin_down:
            self._status = 'down'
        else:
            self._status = value

    @property
    def available_attributes(self):
        '''The available attributes for a given resource'''
        return self.attributes.keys()

    def _check_managed(self):
        '''Check to see if this resource is managed, if it isn't raise an
        UnmanagedResourceError.  Used in commands that don't make sense on
        unmanaged resources.

        '''
        if not self.managed:
            raise UnmanagedResourceError('Cobalt cannot reserve unmanaged resource %s' % \
                    (self.name))

    def reserve(self, until, user=None, jobid=None):
        '''Reserve a resource until a certain time.  If applicable, the user and
        queue-manager jobid should be included.

        Inputs:
            until - time to reserve until in integer seconds from epoch
            user  - (optional) user reserving the resource
            jobid - (optional) queue-manager job the resource is reserved for

        Returns:
            True on successful reservation.

        Exceptions:
            UnmanagedResourceError - resource isn't currently managed by Cobalt.
            ReservationError - Resource could not be reserved at this time.

        '''
        self._check_managed()
        # we need to be able to update reserved time in this call.  If
        # user/jobid match, then allow the set to go through.
        if jobid is not None:
            jobid = int(jobid)
        if (self.reserved and
                ((user is not None and user != self.reserved_by) or
                 (jobid is not None and jobid != self.reserved_jobid))):
            raise ResourceReservationFailure('%s/%s/%s: Unable to reserve already reserved resource' % (self.name, user, jobid))
        self.reserved_until = until
        self.reserved_by = user
        self.reserved_jobid = jobid
        self.status = 'allocated'
        return True

    def release(self, user=None, jobid=None, force=False):
        '''Release resource reservation on this resource, by clearing reserved_*
        variables. If this completes, then the resource should be schedulable
        again.

        Arguments:
            user  - requesting user
            jobid - requesting jobid
            force - force the release of resources (admin)

        Return:
            True if resources successfully released, False if the ownership
            check fails.

        Exceptions:
            UnmanagedResourceError - resource isn't currently managed by Cobalt.

        '''
        self._check_managed()
        released = False
        if not self.reserved:
            _logger.warning('Release of already free resource %s attempted.' \
                    ' Resetting reserved attributes.', self.name)
            self.reserved_until = None
            self.reserved_by = None
            self.reserved_jobid = None
            released = True
        elif (force or (user == self.reserved_by or
                        jobid == self.reserved_jobid)):
            if force:
                _logger.warning('Release of reservation on %s forced. jobid: %s, user %s.',
                        self.name, jobid, user)
            self.reserved_until = None
            self.reserved_by = None
            self.reserved_jobid = None
            released = True
        else:
            _logger.warning('%s/%s: Attempted to release reservation owned by %s/%s',
                    user, jobid, self.reserved_by, self.reserved_jobid)
        self.status = 'cleanup-pending'
        return released

