"""Tests for general system component classes.

"""
from nose.tools import raises
from testsuite.TestCobalt.Utilities.assert_functions import assert_match, assert_not_match
from Cobalt.Components.system.resource import Resource
from Cobalt.Components.system.ClusterNode import ClusterNode
import Cobalt.Exceptions
import time

def is_match(a, b):
    return a is b

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
        assert_match(resource.name, 'foo', "Resource not initialized")
        assert_match(resource.attributes, {}, "Improper attributes set")
        assert_match(resource.status, 'idle', "Default resource not idle")
        assert not resource.managed, "Default resource shouldn't be managed"

    def test_resource_init_with_attrs(self):
        #expected default initialization
        attrs = {'bar':1, 'baz':'hi'}
        resource = Resource({'name':'foo', 'attributes': attrs})
        assert_match(resource.name, 'foo', "Resource not initialized")
        assert_match(resource.attributes, attrs, "Imporper attributes set.")
        assert_match(resource.status, 'idle', "Default resource not idle")
        assert not resource.managed, "Default resource shouldn't be managed"

    @raises(Cobalt.Exceptions.InvalidStatusError)
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
        assert_match(self.resource_list[0].reserved_until, until,
                "reserved_until not set.")
        assert_match(self.resource_list[0].reserved_by, 'foo',
            "reserved_by not set.")
        assert_match(self.resource_list[0].reserved_jobid, 1,
                "reserved_jobid not set.")
        assert_match(self.resource_list[0].status, 'allocated',
                "resource not allocated")

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
        except Cobalt.Exceptions.ResourceReservationFailure:
            pass
        else:
            assert False, "ResourceReservationFailure not raised"
        assert_match(res.reserved_until, now, "reserved until modified.")
        assert_match(res.reserved_by, user, "reserved user modified.")
        assert_match(res.reserved_jobid, jobid, "reserved jobid modified.")
        assert_match(res.status, "allocated", "improper status")

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
        except Cobalt.Exceptions.ResourceReservationFailure:
            pass
        else:
            assert False, "ResourceReservationFailure not raised"
        assert_match(res.reserved_until, now, "reserved until modified.")
        assert_match(res.reserved_by, user, "reserved user modified.")
        assert_match(res.reserved_jobid, jobid, "reserved jobid modified.")
        assert_match(res.status, "allocated", "improper status")


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
        assert_match(res.reserved_until, None, "reserved until not unset",
                is_match)
        assert_match(res.reserved_by, None, "reserved by not unset",
                is_match)
        assert_match(res.reserved_jobid, None, "reserved jobid not unset.",
                is_match)
        assert_match(res.status, "idle", "improper status")

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
        assert_match(res.reserved_until, None, "reserved until not unset",
                is_match)
        assert_match(res.reserved_by, None, "reserved by not unset",
                is_match)
        assert_match(res.reserved_jobid, None, "reserved jobid not unset.",
                is_match)
        assert_match(res.status, "idle", "improper status")

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
        assert_match(res.reserved_until, until, 'reserve until unset')
        assert_match(res.reserved_by, user, 'reserve by unset')
        assert_match(res.reserved_jobid, jobid, 'reserve jobid unset')
        assert_not_match(res.status, 'allocated', 'improper status')

    def test_resource_release_bad_jobid(self):
        #what happens in a jobid stays in the jobid, even for the same user.
        res = self.resource_list[0]
        until = time.time() + 600
        user = 'foo'
        jobid = 1
        assert res.reserve(until, user, jobid), "failed to reserve"
        assert res.reserved, "reservation failed"
        assert not res.release(user, 2), "release succeeded"
        assert_match(res.reserved_until, until, 'reserve until unset')
        assert_match(res.reserved_by, user, 'reserve by unset')
        assert_match(res.reserved_jobid, jobid, 'reserve jobid unset')
        assert_not_match(res.status, 'allocated', 'improper status')

    @raises(Cobalt.Exceptions.UnmanagedResourceError)
    def test_unmanaged_reserve(self):
        #can't do anything to unmanaged resources
        self.resource_list[0].managed = False
        self.resource_list[0].reserve(time.time())

    @raises(Cobalt.Exceptions.UnmanagedResourceError)
    def test_unmanaged_release(self):
        #if we're not managing it, we can't release it.
        self.resource_list[0].managed = False
        self.resource_list[0].release()

class TestClusterNode(object):

    def setup(self):
        '''Set up common test parameters. Run as a part of every test.'''
        self.now = time.time()

    def teardown(self):
        '''Clean up any default parameters that need it.  Run every test.'''
        pass


    def setup_base_node(self):
        '''Generate a bare-bones test node.'''
        spec = {'name': 'node1'}
        self.nodelist = [ClusterNode(spec)]
        self.testnode = self.nodelist[0]
        self.testnode.schedulable = True

    def test_init(self):
        #test basic initialization
        spec = {'name': 'node1',
                'attributes': {'ncpu': 1, 'mem':4},
                'queues': ['foo', 'bar'],
                'backfill_epsilon': 600,
                }
        node = ClusterNode(spec)
        assert_match(node.name, 'node1', "wrong name")
        assert_match(node.attributes, {'ncpu': 1, 'mem':4}, "Attributes not set.")
        assert not node.schedulable, "defaulted to schedulable"
        assert_match(node.drain_until, None, "drain_until should not be set",
                is_match)
        assert_match(node.drain_jobid, None, "drain_jobid should not be set",
                is_match)
        assert_match(node.queues, ['foo', 'bar'], "queues not set")
        assert_match(node.backfill_epsilon, 600, "backfill_epsilon not set")

    def test_init_defaults(self):
        #test that defaults are being properly set
        spec = {'name': 'node1'}
        node = ClusterNode(spec)
        assert_match(node.attributes, {}, 'bad default attributes')
        assert_match(node.queues, ['default'], 'bad default queues')
        assert_match(node.backfill_epsilon, 120, 'bad default backfill_epsilon')


    def test_set_drain(self):
        #Set all draining parameters correctly.
        self.setup_base_node()
        self.testnode.set_drain(self.now + 500, 1234)
        assert self.testnode.draining, "Node not reporting that it is draining"
        assert_match(self.testnode.drain_jobid, 1234,
            "Draining jobid set incorrectly.")
        assert_match(self.testnode.drain_until, int(self.now + 500),
            "Drain until set incorrectly.")

    def test_clear_drain(self):
        #make sure draining gets cleared correctly
        self.setup_base_node()
        self.testnode.set_drain(self.now + 500, 1234)
        self.testnode.clear_drain()
        assert not self.testnode.draining, "Node still draining."
        assert_match(self.testnode.drain_jobid, None,
                "Draining jobid still set.", is_match)
        assert_match(self.testnode.drain_until, None, "Drain until still set.",
                is_match)


    def test_read_only_attrs(self):
        #These are read-only attributes. Make sure they stay that way.
        self.setup_base_node()
        testattrs = ['drain_until', 'drain_jobid', 'draining']
        for attr in testattrs:
            try:
                setattr(self.testnode, attr, 'foo')
            except AttributeError:
                pass
            else:
                assert False, ("Read only attribute %s did not raise exception"
                         % (attr))

    @raises(ValueError)
    def test_no_negative_backfill_epsilon(self):
        #ensure ValueError raised for backfill_epsilon
        self.setup_base_node()
        self.testnode.backfill_epsilon = -1

    @raises(Cobalt.Exceptions.UnschedulableNodeError)
    def test_no_drain_down(self):
        #don't drain down hardware
        self.setup_base_node()
        self.testnode.status = 'down'
        self.testnode.set_drain(self.now, 1234)

    @raises(Cobalt.Exceptions.UnschedulableNodeError)
    def test_no_drain_unschedulable(self):
        #don't drain on unscheduled hardware
        self.setup_base_node()
        self.testnode.schedulable = False
        self.testnode.set_drain(self.now, 1234)
