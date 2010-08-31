"""Cobalt component base."""

__revision__ = '$Revision$'

__all__ = ["Component", "exposed", "automatic", "run_component"]

import inspect
import os
import os.path
import cPickle
import ConfigParser
import pydoc
import sys
import getopt
import logging
import time
import threading
import xmlrpclib

import Cobalt
import Cobalt.Proxy
import Cobalt.Logging
from Cobalt.Server import BaseXMLRPCServer, XMLRPCServer, find_intended_location
from Cobalt.Data import get_spec_fields
from Cobalt.Exceptions import NoExposedMethod
from Cobalt.Statistics import Statistics


def state_file_location():
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if _config._sections.has_key("statefiles"):
        state_dir = os.path.expandvars(_config._sections['statefiles'].get("location", "/var/spool/cobalt"))
    else:
        state_dir = "/var/spool/cobalt"

    return state_dir

def run_component (component_cls, argv=None, register=True, state_name=False,
                   cls_kwargs={}, extra_getopt='', time_out=10,
                   single_threaded=False):
    if argv is None:
        argv = sys.argv
    try:
        (opts, arg) = getopt.getopt(argv[1:], 'D:d' + extra_getopt)
    except getopt.GetoptError, e:
        print >> sys.stderr, e
        print >> sys.stderr, "Usage:"
        print >> sys.stderr, "%s [-d] [-D pidfile] [--config-files file1:file2]" % (os.path.basename(argv[0]))
        sys.exit(1)
    
    # default settings
    daemon = False
    pidfile = ""
    level = logging.INFO
    # get user input
    for item in opts:
        if item[0] == '-D':
            daemon = True
            pidfile_name = item[1]
        elif item[0] == '-d':
            level = logging.DEBUG
    
    logging.getLogger().setLevel(level)
    Cobalt.Logging.log_to_stderr(logging.getLogger())
    Cobalt.Logging.setup_logging(component_cls.implementation)

    if daemon:
        child_pid = os.fork()
        if child_pid != 0:
            return
        
        os.setsid()
        
        child_pid = os.fork()
        if child_pid != 0:
            os._exit(0)
        
        redirect_file = open("/dev/null", "w+")
        os.dup2(redirect_file.fileno(), sys.__stdin__.fileno())
        os.dup2(redirect_file.fileno(), sys.__stdout__.fileno())
        os.dup2(redirect_file.fileno(), sys.__stderr__.fileno())
        
        os.chdir(os.sep)
        os.umask(0)
        
        pidfile = open(pidfile_name or "/dev/null", "w")
        print >> pidfile, os.getpid()
        pidfile.close()

    if state_name:
        state_file_name = "%s/%s" % (state_file_location(), state_name)
        try:
            component = cPickle.load(open(state_file_name))
        except:
            component = component_cls(**cls_kwargs)
            component.logger.error("unable to load state from %s", state_file_name, exc_info=True)
        component.statefile = state_file_name
    else:
        component = component_cls(**cls_kwargs)
        
    location = find_intended_location(component)
    try:
        cp = ConfigParser.ConfigParser()
        cp.read([Cobalt.CONFIG_FILES[0]])
        keypath = os.path.expandvars(cp.get('communication', 'key'))
    except:
        keypath = '/etc/cobalt.key'

    if single_threaded:
        server = BaseXMLRPCServer(location, keyfile=keypath, certfile=keypath,
                          register=register, timeout=time_out)
    else:
        server = XMLRPCServer(location, keyfile=keypath, certfile=keypath,
                          register=register, timeout=time_out)
    server.register_instance(component)
    
    try:
        server.serve_forever()
    finally:
        server.server_close()

def exposed (func):
    """Mark a method to be exposed publically.
    
    Examples:
    class MyComponent (Component):
        @expose
        def my_method (self, param1, param2):
            do_stuff()
    
    class MyComponent (Component):
        def my_method (self, param1, param2):
            do_stuff()
        my_method = expose(my_method)
    """
    func.exposed = True
    return func

def automatic (func, period=10):
    """Mark a method to be run periodically."""
    func.automatic = True
    func.automatic_period = period
    func.automatic_ts = -1
    return func

def locking (func):
    """Mark a function as being internally thread safe"""
    func.locking = True
    return func

def readonly (func):
    """Mark a function as read-only -- no data effects in component inst"""
    func.readonly = True
    return func

def query (func=None, **kwargs):
    """Mark a method to be marshalled as a query."""
    def _query (func):
        if kwargs.get("all_fields", True):
            func.query_all_fields = True
        func.query = True
        return func
    if func is not None:
        return _query(func)
    return _query

def marshal_query_result (items, specs=None):
    if specs is not None:
        fields = get_spec_fields(specs)
    else:
        fields = None
    return [item.to_rx(fields) for item in items]

class Component (object):
    
    """Base component.
    
    Intended to be served as an instance by Cobalt.Component.XMLRPCServer
    >>> server = Cobalt.Component.XMLRPCServer(location, keyfile)
    >>> component = Cobalt.Component.Component()
    >>> server.serve_instance(component)
    
    Class attributes:
    name -- logical component name (e.g., "queue-manager", "process-manager")
    implementation -- implementation identifier (e.g., "BlueGene/L", "BlueGene/P")
    
    Methods:
    save -- pickle the component to a file
    do_tasks -- perform automatic tasks for the component
    """
    
    name = "component"
    implementation = "generic"
    
    def __init__ (self, **kwargs):
        """Initialize a new component.
        
        Keyword arguments:
        statefile -- file in which to save state automatically
        """
        self.statefile = kwargs.get("statefile", None)
        if kwargs.get("register", True):
            Cobalt.Proxy.register_component(self)
        self.logger = logging.getLogger("%s %s" % (self.implementation, self.name))
        self.lock = threading.Lock()
        self.statistics = Statistics()
        
    def save (self, statefile=None):
        """Pickle the component.
        
        Arguments:
        statefile -- use this file, rather than component.statefile
        """
        statefile = statefile or self.statefile
        if statefile:
            temp_statefile = statefile + ".temp"
            data = cPickle.dumps(self)

            try:
                import pyxser

                print "-" * 64
                xser_data = pyxser.serialize(obj=self, enc="utf-8", depth=2)
                fileobj = open("__xser_cqm__.txt", 'wb')
                fileobj.write(xser_data)
                fileobj.close()

                xser_data = None

                fileobj = open("__xser_cqm__.txt", 'rb')
                xser_data = fileobj.read()
                fileobj.close()
                print xser_data
                newself = pyxser.unserialize(obj=xser_data, enc="utf-8")
                print dir(newself)
            except Exception, e:
                print "ERROR:%s" % str(e)
                

            try:
                fd = file(temp_statefile, "wb")
                fd.write(data)
                fd.close()
            except IOError, e:
                self.logger.error("statefile failure : %s" % e)
                return str(e)
            else:
                os.rename(temp_statefile, statefile)
                return "state saved to file: %s" % statefile
    save = exposed(save)
    
    def do_tasks (self):
        """Perform automatic tasks for the component.
        
        Automatic tasks are member callables with an attribute
        automatic == True.
        """
        for name, func in inspect.getmembers(self, callable):
            if getattr(func, "automatic", False):
                need_to_lock = not getattr(func, 'locking', False)
                if (time.time() - func.automatic_ts) > func.automatic_period:
                    if need_to_lock:
                        t1 = time.time()
                        self.lock.acquire()
                        t2 = time.time()
                        self.statistics.add_value('component_lock', t2-t1)
                    try:
                        mt1 = time.time()
                        func()
                    except:
                        self.logger.error("Automatic method %s failed" \
                                          % (name), exc_info=1)
                    finally:
                        mt2 = time.time()
                        if need_to_lock:
                            self.lock.release()
                        self.statistics.add_value(name, mt2-mt1)
                        func.__dict__['automatic_ts'] = time.time()

    def _resolve_exposed_method (self, method_name):
        """Resolve an exposed method.
        
        Arguments:
        method_name -- name of the method to resolve
        """
        try:
            func = getattr(self, method_name)
        except AttributeError:
            raise NoExposedMethod(method_name)
        if not getattr(func, "exposed", False):
            raise NoExposedMethod(method_name)
        return func

    def _dispatch (self, method, args, dispatch_dict):
        """Custom XML-RPC dispatcher for components.
        
        method -- XML-RPC method name
        args -- tuple of paramaters to method
        """
        if method in dispatch_dict:
            method_func = dispatch_dict[method]
        else:
            try:
                method_func = self._resolve_exposed_method(method)
            except Exception, e:
                if getattr(e, "log", True):
                    self.logger.error(e, exc_info=True)
                raise xmlrpclib.Fault(getattr(e, "fault_code", 1), str(e))
        
        need_to_lock = not getattr(method_func, 'locking', False)
        if need_to_lock:
            lock_start = time.time()
            self.lock.acquire()
            lock_done = time.time()
        try:
            method_start = time.time()
            result = method_func(*args)
        except Exception, e:
            if getattr(e, "log", True):
                self.logger.error(e, exc_info=True)
            raise xmlrpclib.Fault(getattr(e, "fault_code", 1), str(e))
        finally:
            method_done = time.time()
            if need_to_lock:
                self.lock.release()
                self.statistics.add_value('component_lock',
                                      lock_done - lock_start)
            self.statistics.add_value(method, method_done - method_start)
        if getattr(method_func, "query", False):
            if not getattr(method_func, "query_all_methods", False):
                margs = args[:1]
            else:
                margs = []
            result = marshal_query_result(result, *margs)
        return result

    @exposed
    def listMethods (self):
        """Custom XML-RPC introspective method list."""
        return [
            name for name, func in inspect.getmembers(self, callable)
            if getattr(func, "exposed", False)
        ]

    @exposed
    def methodHelp (self, method_name):
        """Custom XML-RPC introspective method help.
        
        Arguments:
        method_name -- name of method to get help on
        """
        try:
            func = self._resolve_exposed_method(method_name)
        except NoExposedMethod:
            return ""
        return pydoc.getdoc(func)
    
    def get_name (self):
        """The name of the component."""
        return self.name
    get_name = exposed(get_name)
    
    def get_implementation (self):
        """The implementation of the component."""
        return self.implementation
    get_implementation = exposed(get_implementation)

    def get_statistics (self):
        """Get current statistics about component execution"""
        return self.statistics.display()
    get_statistics = exposed(get_statistics)
