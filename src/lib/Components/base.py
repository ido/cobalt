"""Cobalt component base."""

__revision__ = '$Revision: 2130 $'

__all__ = ["Component", "exposed", "automatic", "run_component"]

import inspect
import os
import os.path
import cPickle
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
import Cobalt.Util
init_cobalt_config = Cobalt.Util.init_cobalt_config
get_config_option = Cobalt.Util.get_config_option
ParsingError = Cobalt.Util.ParsingError


try:
    print >>sys.stderr, "INFO: initializing configuration system"
    _config_files_read = init_cobalt_config()
    _missing_config_files = list(set(Cobalt.CONFIG_FILES).difference(set(_config_files_read)))
    if _missing_config_files:
        print >>sys.stderr, "Warning: one or more config files were not found: %s" % (str(_missing_config_files)[1:-1],)
except Exception, e:
    print >>sys.stderr, "ERROR: unable to parse config file:\n\t%s" % (e.message,)
    sys.exit(1)


def state_file_location():

    '''Grab the location of the Cobalt statefiles.  

    default: /var/spool/cobalt

    '''
    return os.path.expandvars(get_config_option('statefiles', "location", "/var/spool/cobalt"))

def run_component (component_cls, argv=None, register=True, state_name=False,
                   cls_kwargs={}, extra_getopt='', time_out=10,
                   single_threaded=False):
    '''Run the Cobalt component.  

    arguments:

    component_cls
    argv
    register
    state_name
    cls_kwargs
    extra_getopt
    time_out
    single_threaded

    This will run until a the component is terminated.

    '''

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
    Cobalt.Logging.setup_logging(component_cls.implementation, console_timestamp=True)

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
            component.logger.error("UNABLE TO LOAD STATE FROM %s.  STARTING WITH A BLANK SLATE.", state_file_name, exc_info=True)
        component.statefile = state_file_name
    else:
        component = component_cls(**cls_kwargs)

    location = find_intended_location(component)
    try:
        keypath = os.path.expandvars(get_config_option('communication', 'key'))
        certpath = os.path.expandvars(get_config_option('communication', 'cert'))
        capath = os.path.expandvars(get_config_option('communication', 'ca'))
    except:
        keypath = '/etc/cobalt.key'
        certpath = None
        capath = None

    if single_threaded:
        server = BaseXMLRPCServer(location, keyfile=keypath, certfile=certpath, 
                          cafile=capath, register=register, timeout=time_out)
    else:
        server = XMLRPCServer(location, keyfile=keypath, certfile=certpath,
                          cafile=capath, register=register, timeout=time_out)

    #Two components of the same type cannot be allowed to run at the same time.
    if component.name != 'service-location':
        address = Cobalt.Proxy.ComponentProxy('service-location').locate(component.name)
        if address:
            component.logger.critical("CRITICAL: Instance of component %s already registered.  Startup of this instance aborted.", component.name)
            sys.exit(1)
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
            self._registered_component=True
            Cobalt.Proxy.register_component(self)
        else:
            self._registered_component=False
        self.logger = logging.getLogger("%s %s" % (self.implementation, self.name))
        self._component_lock = threading.Lock()
        self._component_lock_acquired_time = None
        self.statistics = Statistics()

    def __getstate__(self):
        state = {}
        return {
            'base_component_version':1,
            'register_component':self._registered_component}

    def __setstate__(self, state):
        Cobalt.Util.fix_set(state)
        if hasattr(state, 'register_component') and state['register_component']:
            self._registered_component=True
            Cobalt.Proxy.register_component(self)
        else:
            self._registered_component=False
        self.logger = logging.getLogger("%s %s" % (self.implementation, self.name))
        self._component_lock = threading.Lock()
        self._component_lock_acquired_time = None
        self.statistics = Statistics()

    def component_lock_acquire(self):
        entry_time = time.time()
        self._component_lock.acquire()
        self._component_lock_acquired_time = time.time()
        self.statistics.add_value('component_lock_wait', self._component_lock_acquired_time - entry_time)

    def component_lock_release(self):
        self.statistics.add_value('component_lock_held', time.time() - self._component_lock_acquired_time)
        self._component_lock_acquired_time = None
        self._component_lock.release()

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
                        self.component_lock_acquire()
                    try:
                        mt1 = time.time()
                        func()
                    except:
                        self.logger.error("Automatic method %s failed" \
                                          % (name), exc_info=1)
                    finally:
                        mt2 = time.time()
                        if not need_to_lock:
                            self.component_lock_acquire()
                        self.statistics.add_value(name, mt2-mt1)
                        self.component_lock_release()
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
            self.component_lock_acquire()
        try:
            method_start = time.time()
            result = method_func(*args)
        except Exception, e:
            if getattr(e, "log", True):
                self.logger.error(e, exc_info=True)
            raise xmlrpclib.Fault(getattr(e, "fault_code", 1), str(e))
        finally:
            method_done = time.time()
            if not need_to_lock:
                self.component_lock_acquire()
            self.statistics.add_value(method, method_done - method_start)
            self.component_lock_release()
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


