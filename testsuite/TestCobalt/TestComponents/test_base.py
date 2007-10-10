import logging

from Cobalt.Components.base import Component, exposed, automatic
import Cobalt.Proxy
import Cobalt.Logging


class TestComponent (object):
    
    def setup (self):
        logger = logging.getLogger()
        Cobalt.Logging.log_to_stderr(logger)
    
    def teardown (self):
        Cobalt.Proxy.local_components.clear()
    
    def test_exposed (self):
        
        class TestComponent (Component):
            
            @exposed
            def method1 (self):
                return "return1"
            
            @exposed
            def method2 (self):
                return "return2"
            
            def method3 (self):
                return "return3"
        
        component = TestComponent()
        assert component.method1.exposed
        assert component.method2.exposed
        assert not getattr(component.method3, "exposed", False)
        exposed_methods = component._listMethods()
        assert set(exposed_methods) == set(["get_name", "get_implementation", "method1", "method2"])
        assert component._dispatch("method1", ()) == "return1"
        assert component._dispatch("method2", ()) == "return2"
        try:
            component._dispatch("method3", ())
        except Exception:
            pass
        else:
            assert not "dispatched to unexposed method"
    
    def test_automatic (self):
        
        class TestComponent (Component):
            
            runs = dict(method1=0, method2=0, method3=0)
            
            @automatic
            def method1 (self):
                self.runs['method1'] += 1
            
            @automatic
            def method2 (self):
                self.runs['method2'] += 1
            
            def method3 (self):
                self.runs['method3'] += 1
            
        component = TestComponent()
        component.do_tasks()
        assert component.runs['method1'] == 1
        assert component.runs['method2'] == 1
        assert component.runs['method3'] == 0
        component.do_tasks()
        assert component.runs['method1'] == 2
        assert component.runs['method2'] == 2
        assert component.runs['method3'] == 0
