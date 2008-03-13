"""Cobalt component base."""

__revision__ = '$Revision$'

__all__ = ["Component", "exposed", "automatic", "run_component"]

import inspect
import os
import cPickle
import ConfigParser
import pydoc
import sys
import getopt
import logging
import time
import xmlrpclib

import Cobalt
import Cobalt.Proxy
import Cobalt.Logging
from Cobalt.Server import XMLRPCServer, find_intended_location
from Cobalt.Data import get_spec_fields
from Cobalt.Exceptions import NoExposedMethod



def state_file_location():
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read(Cobalt.CONFIG_FILES)
    if _config._sections.has_key("statefiles"):
        state_dir = _config._sections['statefiles'].get("location", "/var/spool/cobalt")
    else:
        state_dir = "/var/spool/cobalt"

    return state_dir

def run_component (component_cls, argv=None, register=True, state_name=False,
                   cls_kwargs={}):
    if argv is None:
        argv = sys.argv
    try:
        (opts, arg) = getopt.getopt(argv[1:], 'C:D:d')
    except getopt.GetoptError, e:
        print >> sys.stderr, e
        print >> sys.stderr, "Usage:"
        print >> sys.stderr, "%s [-d] [-D pidfile] [-C config file]" % (os.path.basename(argv[0]))
        sys.exit(1)
    
    # default settings
    daemon = False
    pidfile = ""
    level = logging.INFO
    # get user input
    for item in opts:
        if item[0] == '-C':
            Cobalt.CONFIG_FILES = (item[1], )
        elif item[0] == '-D':
            daemon = True
            pidfile_name = item[1]
        elif item[0] == '-d':
            level = logging.DEBUG
    
    logging.getLogger().setLevel(level)
    Cobalt.Logging.log_to_stderr(logging.getLogger())
    Cobalt.Logging.setup_logging(component_cls.implementation, True, True)

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
        component.statefile = state_file_name
    else:
        component = component_cls(**cls_kwargs)
        
    location = find_intended_location(component)
    try:
        cp = ConfigParser.ConfigParser()
        cp.read([Cobalt.CONFIG_FILES[0]])
        keypath = cp.get('communication', 'key')
    except:
        keypath = '/etc/cobalt.key'

    server = XMLRPCServer(location, keyfile=keypath, certfile=keypath,
                          register=register)
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
        
    def save (self, statefile=None):
        """Pickle the component.
        
        Arguments:
        statefile -- use this file, rather than component.statefile
        """
        statefile = statefile or self.statefile
        if statefile:
            data = cPickle.dumps(self)
            try:
                statefile = file(statefile or self.statefile, "wb")
                statefile.write(data)
            except IOError:
                self.logger.error("Failed to write to statefile %s" % statefile)
                self.logger.error("Disabling state persisitence code")
                self.statefile = None
    
    def do_tasks (self):
        """Perform automatic tasks for the component.
        
        Automatic tasks are member callables with an attribute
        automatic == True.
        """
        for name, func in inspect.getmembers(self, callable):
            if getattr(func, "automatic", False):
                if (time.time() - func.automatic_ts) > \
                   func.automatic_period:
                    func()
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
    
    def _dispatch (self, method, args):
        """Custom XML-RPC dispatcher for components.
        
        method -- XML-RPC method name
        args -- tuple of paramaters to method
        """
        try:
            func = self._resolve_exposed_method(method)
            result = func(*args)
            if getattr(func, "query", False):
                if not getattr(func, "query_all_methods", False):
                    margs = args[:1]
                else:
                    margs = []
                result = marshal_query_result(result, *margs)
            return result
        except Exception, e:
            if getattr(e, "log", True):
                self.logger.error(e, exc_info=True)
            raise xmlrpclib.Fault(getattr(e, "fault_code", 1), str(e))
    
    def _listMethods (self):
        """Custom XML-RPC introspective method list."""
        return [
            name for name, func in inspect.getmembers(self, callable)
            if getattr(func, "exposed", False)
        ]
    
    def _methodHelp (self, method_name):
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
