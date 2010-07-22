import time

from Cobalt.Components.slp import \
    ServiceLocator, PollingServiceLocator, TimingServiceLocator

from test_base import TestComponent

__all__ = [
    "TestServiceLocator",
    "TestPollingServiceLocator", "TestTimingServiceLocator",
]

class TestServiceLocator (TestComponent):
    
    def setup (self):
        TestComponent.setup(self)
        self.slp = ServiceLocator()
    
    def test_register (self):
        for each in range(2):
            try:
                self.slp.register("foo_service", "http://localhost:5900")
            except:
                raise
                assert not "Wasn't able to register a service."
    
    def test_unregister (self):
        try:
            self.slp.unregister("foo_service")
        except:
            assert not "Wasn't able to unregister an unregistered service."
        self.slp.register("foo_service", "http://localhost:5900")
        try:
            self.slp.unregister("foo_service")
        except:
            assert not "Wasn't able to unregister."
        try:
            self.slp.unregister("foo_service")
        except:
            assert not "Wasn't able to unregister multiple times."
    
    def test_locate (self):
        location = self.slp.locate("foo_service")
        assert location == ""
        self.slp.register("foo_service", "http://localhost:5900")
        location = self.slp.locate("foo_service")
        assert location == "http://localhost:5900"
        self.slp.unregister("foo_service")
        location = self.slp.locate("foo_service")
        assert location == ""
    
    def test_get_services (self):
        services = self.slp.get_services([{'name':"foo_service"}])
        assert len(services) == 0
        self.slp.register("foo_service", "http://localhost:5900")
        services = self.slp.get_services([{'name':"foo_service"}])
        assert len(services) == 1
        assert services[0].name == "foo_service"
        services = self.slp.get_services([{'name':"*", 'location':"*"}])
        assert len(services) == 1
        assert services[0].name == "foo_service"
        assert services[0].location == "http://localhost:5900"


class TestPollingServiceLocator (TestServiceLocator):
    
    def setup (self):
        self.slp = PollingServiceLocator()
    
    def test_check_services (self):
        self.slp.register("foo_service", "http://localhost:5900")
        location = self.slp.locate("foo_service")
        assert location == "http://localhost:5900"
        self.slp.check_services()
        location = self.slp.locate("foo_service")
        assert location == ""


class TestTimingServiceLocator (TestServiceLocator):
    
    def setup (self):
        self.slp = TimingServiceLocator(expire=2)
    
    def test_init_expire (self):
        assert self.slp.expire == 2
    
    def test_expire_services (self):
        self.slp.register("foo_service", "http://localhost:5900")
        start = time.time()
        self.slp.expire_services()
        assert time.time() < start + 2
        location = self.slp.locate("foo_service")
        assert location == "http://localhost:5900"
        time.sleep(3)
        assert (time.time() - start) > 2
        self.slp.expire_services()
        location = self.slp.locate("foo_service")
        assert location == ""
