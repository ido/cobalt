import logging

from Cobalt.Components.base import Component, exposed, automatic
import Cobalt.Proxy
import time, random
from TestCobalt.Utilities.Time import timeout

class TestComponent (object):
    
    def setup (self):
        pass
    
    def teardown (self):
        Cobalt.Proxy.local_components.clear()
    
    def test_exposed (self):
        
        class TestComponent (Component):
            
            def method1 (self):
                return "return1"
            method1 = exposed(method1)
            
            def method2 (self):
                return "return2"
            method2 = exposed(method2)
            
            def method3 (self):
                return "return3"
        
        component = TestComponent()
        assert component.method1.exposed
        assert component.method2.exposed
        assert not getattr(component.method3, "exposed", False)
        exposed_methods = component.listMethods()
        assert set(exposed_methods) == set(['get_implementation', 'get_name', 'get_statistics', 'listMethods', 'method1',
            'method2', 'methodHelp', 'save'])
        assert component._dispatch("method1", (), {}) == "return1"
        assert component._dispatch("method2", (), {}) == "return2"
        try:
            component._dispatch("method3", ())
        except Exception:
            pass
        else:
            assert not "dispatched to unexposed method"
    
    def test_automatic (self):
        
        class TestComponent (Component):
            
            runs = dict(method1=0, method2=0, method3=0)
            m4data = []
            
            def method1 (self):
                self.runs['method1'] += 1
            method1 = automatic(method1)
            
            def method2 (self):
                self.runs['method2'] += 1
            method2 = automatic(method2, 0)
            
            def method3 (self):
                self.runs['method3'] += 1

            def method4 (self):
                self.m4data.append(time.time())
            method4 = automatic(method4, 4)
                
        component = TestComponent()
        component.do_tasks()
        assert component.runs['method1'] == 1
        assert component.runs['method2'] == 1
        assert component.runs['method3'] == 0
        component.do_tasks()
        assert component.runs['method1'] == 1
        assert component.runs['method2'] == 2
        assert component.runs['method3'] == 0
        for i in range(15):
            time.sleep(random.randrange(0, 6))
            component.do_tasks()
        while len(component.m4data) > 1:
            assert component.m4data[1] - component.m4data[0] > 4
            component.m4data = component.m4data[1:]
