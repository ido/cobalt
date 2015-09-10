"""Tests for general system component classes.

"""
from nose.tools import raises
from Cobalt.Components.system.resource import *
from Cobalt.Components.system.ClusterNode import ClusterNode
import time

class TestSystemResource(object):

    def setup(self):
        default_spec = {'name': 'res1',
                        'attributes': {'mem':64, 'cpupn':16, 'pubnet':True},
                       }
        self.resource_list=[]
        self.resource_list.append(Resource(default_spec))
        self.resource_list[0].managed = True

    def teardown(self):
        del self.resource_list

    def test_resource_init_no_attrs(self):
        #initialize a resource with no attributes set, need to get {}.
        resource = Resource({'name':'foo'})
        assert resource.name == 'foo', "Resource not initialized"
        assert resource.attributes == {}, "Imporper attributes set"
        assert resource.status == 'idle', "Default resource not idle"
        assert not resource.managed, "Default resource shouldn't be managed"

    def test_resource_init_with_attrs(self):
        #expected default initializatin
        attrs = {'bar':1, 'baz':'hi'}
        resource = Resource({'name':'foo', 'attributes': attrs})
        assert resource.name == 'foo', "Resource not initialized"
        assert resource.attributes == attrs, "Imporper attributes set %s" % resource.attributes
        assert resource.status == 'idle', "Default resource not idle"
        assert not resource.managed, "Default resource shouldn't be managed"

    @raises(InvalidStatusError)
    def test_resource_set_bad_state(self):
        #Make sure the resource state constraint is obeyed.
        self.resource_list[0].status = 'badstatus'
        assert False, "Exception not raised"

    def test_resource_state_reserved(self):
        #if resource_until is set, the resource is reserved.
        assert not self.resource_list[0].reserved, "Resource erroniously reserved."
        self.resource_list[0].reserved_until = time.time() + 600
        assert self.resource_list[0].reserved, "Resource should be reserved."

    def test_resource_reservation_idle(self):
        #Can we make a reservation
        until = time.time() + 600
        assert self.resource_list[0].reserve(until, 'foo', 1), "reservation failed."
        assert self.resource_list[0].reserved_until == until, "reserved_until not set."
        assert self.resource_list[0].reserved_by == 'foo', "reserved_by not set."
        assert self.resource_list[0].reserved_jobid == 1, "reserved_jobid not set."
        assert self.resource_list[0].status == 'allocated', "resource not allocated"

    def test_resource_reservation_reserved_bad_user(self):
        #Fence the reservation manipulation to user
        now = time.time()
        until = now + 600
        user = 'foo'
        jobid = 1
        res = self.resource_list[0]
        assert res.reserve(now, user, jobid), "failed initial reservation"
        try:
            res.reserve(until, "bar", 1)
        except ReservationError:
            pass
        else:
            assert False, "ReservationError not raised"
        assert res.reserved_until == now, "reserved until modified."
        assert res.reserved_by == user, "reserved user modified."
        assert res.reserved_jobid == jobid, "reserved jobid modified."
        assert res.status == "allocated", "improper status"

    def test_resource_reservation_reserved_bad_job(self):
        #make sure a bad jobid but right user doesn't re-reserve resource.
        now = time.time()
        until = now + 600
        user = 'foo'
        jobid = 1
        res = self.resource_list[0]
        assert res.reserve(now, user, jobid), "failed initial reservation"
        try:
            res.reserve(until, user, 2)
        except ReservationError:
            pass
        else:
            assert False, "ReservationError not raised"
        assert res.reserved_until == now, "reserved until modified."
        assert res.reserved_by == user, "reserved user modified."
        assert res.reserved_jobid == jobid, "reserved jobid modified."
        assert res.status == "allocated", "improper status"

    def test_resource_release(self):
        #release resource reservation
        res = self.resource_list[0]
        until = time.time() + 600
        user = 'foo'
        jobid = 1
        res.reserve(until, user, jobid)
        assert res.reserved, "reservation failed"
        assert res.release(user, jobid), "release failed"
        assert not res.reserved, "still reserved"
        assert res.reserved_until is None, "reserved until not unset"
        assert res.reserved_by is None, "reserved by not unset"
        assert res.reserved_jobid is None, "reserved jobid not unset."
        assert res.status == "idle", "imporper status"

    def test_resource_release_force(self):
        #force-release reservation, because admin commands are a thing.
        res = self.resource_list[0]
        until = time.time() + 600
        user = 'foo'
        jobid = 1
        res.reserve(until, user, jobid)
        assert res.reserved, "reservation failed"
        assert res.release(force=True), "release failed"
        assert not res.reserved, "release failed"
        assert res.reserved_until is None, "reserved until not unset"
        assert res.reserved_by is None, "reserved by not unset"
        assert res.reserved_jobid is None, "reserved jobid not unset."
        assert res.status == "idle", "imporper status"

    def test_resource_release_unreserved(self):
        #you can't release something that hasn't been reserved yet.
        res = self.resource_list[0]
        assert not res.release(force=True), "cannot release unreserved."

    def test_resource_release_bad_user(self):
        #keep a user from releasing some one else's reservation
        res = self.resource_list[0]
        until = time.time() + 600
        user = 'foo'
        jobid = 1
        assert res.reserve(until, user, jobid), "failed to reserve"
        assert res.reserved, "reservation failed"
        assert not res.release('bar', jobid), "release succeeded"
        assert res.reserved_until == until, 'reserve until unset'
        assert res.reserved_by == user, 'reserve by unset'
        assert res.reserved_jobid == jobid, 'reserve jobid unset'
        assert res.status != 'allocated', 'imporper status'

    def test_resource_release_bad_jobid(self):
        #what happens in a jobid stays in the jobid, even for the same user.
        res = self.resource_list[0]
        until = time.time() + 600
        user = 'foo'
        jobid = 1
        assert res.reserve(until, user, jobid), "failed to reserve"
        assert res.reserved, "reservation failed"
        assert not res.release(user, 2), "release succeeded"
        assert res.reserved_until == until, 'reserve until unset'
        assert res.reserved_by == user, 'reserve by unset'
        assert res.reserved_jobid == jobid, 'reserve jobid unset'
        assert res.status != 'allocated', 'imporper status'

    @raises(UnmanagedResourceError)
    def test_unmanaged_reserve(self):
        #can't do anything to unmanaged resources
        self.resource_list[0].managed = False
        self.resource_list[0].reserve(time.time())

    @raises(UnmanagedResourceError)
    def test_unmanaged_release(self):
        #if we're not managing it, we can't release it.
        self.resource_list[0].managed = False
        self.resource_list[0].release()

class TestClusterNode(object):

    def test_init(self):
        #test basic initialization
        spec = {'name': 'node1',
                'attributes': {'ncpu': 1, 'mem':4},
                'queues': ['foo', 'bar'],
                'backfill_epsilon': 600,
                }
        node = ClusterNode(spec)
        assert node.name == 'node1', "name not set"
        assert node.attributes == {'ncpu': 1, 'mem':4}, "Attributes not set."
        assert not node.schedulable, "defaulted to schedulable"
        assert node.drain_until is None, "drain_until should not be set"
        assert node.drain_jobid is None, "drain_jobid should not be set"
        assert node.queues == ['foo', 'bar'], "queues not set"
        assert node.backfill_epsilon == 600, "backfill_epsilon not set"

    def test_init_defaults(self):
        #test that defaults are being properly set
        spec = {'name': 'node1'}
        node = ClusterNode(spec)
        assert node.attributes == {}, 'bad default attributes'
        assert node.queues == ['default'], 'bad default queues'
        assert node.backfill_epsilon == 120, 'bad default backfill_epsilon'

    def setup_test_node(self):
        spec = {'name': 'node1'}
        self.nodelist = [ClusterNode(spec)]
        self.testnode = self.nodelist[0]



