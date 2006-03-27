'''Cobalt component base classes'''
__revision__ = '$Revision$'

import atexit, logging, os, select, signal, socket, sys, time, urlparse, xmlrpclib, cPickle, ConfigParser
import BaseHTTPServer, Cobalt.Proxy, OpenSSL.SSL, SimpleXMLRPCServer, SocketServer

log = logging.getLogger('Component')

def daemonize(filename):
    '''Do the double fork/setsession dance'''
    # Fork once
    if os.fork() != 0:      
        os._exit(0)         
    os.setsid()                     # Create new session
    pid = os.fork()
    if pid != 0:
        pidfile = open(filename, "w")
        pidfile.write("%i" % pid)
        pidfile.close()
        os._exit(0)     
    os.chdir("/")         
    os.umask(0)

    null = open("/dev/null", "w+")

    os.dup2(null.fileno(), sys.__stdin__.fileno())
    os.dup2(null.fileno(), sys.__stdout__.fileno())
    os.dup2(null.fileno(), sys.__stderr__.fileno())

class CobaltXMLRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    '''CobaltXMLRPCRequestHandler takes care of ssl xmlrpc requests'''
    def finish(self):
        '''Finish HTTPS connections properly'''
        #self.request.set_shutdown(M2Crypto.SSL.SSL_RECEIVED_SHUTDOWN | \
        #                          M2Crypto.SSL.SSL_SENT_SHUTDOWN)
        self.request.close()

    def do_POST(self):
        '''Overload do_POST to pass through client address information'''
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            response = self.server._cobalt_marshalled_dispatch(data, self.client_address)
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            log.error("Unexcepted handler failure in do_POST", exc_info=1)
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown()

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

class SSLServer(BaseHTTPServer.HTTPServer):
    '''This class encapsulates all of the ssl server stuff'''
    def __init__(self, address, keyfile, handler):
        SocketServer.BaseServer.__init__(self, address, handler)
        ctxt = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        ctxt.use_privatekey_file (keyfile)
        ctxt.use_certificate_file(keyfile)
        self.socket = OpenSSL.SSL.Connection(ctxt,
                                             socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()

class Component(SSLServer,
                SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    """Cobalt component providing XML-RPC access"""
    __name__ = 'Component'
    __implementation__ = 'Generic'
    __statefields__ = []
    async_funcs = ['assert_location']

    def __init__(self, setup):
        # need to get addr
        self.setup = setup
        self.shut = False
        signal.signal(signal.SIGINT, self.start_shutdown)
        signal.signal(signal.SIGTERM, self.start_shutdown)
        self.logger = logging.getLogger('Component')
        self.cfile = ConfigParser.ConfigParser()
        if setup['configfile']:
            cfilename = setup['configfile']
        else:
            cfilename = '/etc/cobalt.conf'
        self.cfile.read([cfilename])
        if not self.cfile.has_section('communication'):
            print "Configfile missing communication section"
            raise SystemExit, 1
        self.static = False
        if not self.cfile.has_section('components'):
            print "Configfile missing components section"
            raise SystemExit, 1
        if self.cfile._sections['components'].has_key(self.__name__):
            self.static = True
            location = urlparse.urlparse(self.cfile.get('components', self.__name__))[1].split(':')
            location = ('', int(location[1]))
        else:
            location = ('', 0)
        try:
            keyfile = self.cfile.get('communication', 'key')
        except ConfigParser.NoOptionError:
            print "No key specified in cobalt.conf"
            raise SystemExit, 1

        self.password = self.cfile.get('communication', 'password')
            
        SSLServer.__init__(self, location, keyfile, CobaltXMLRPCRequestHandler)
        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        self.logRequests = 0
        if self.setup['daemon']:
            daemonize(self.setup['daemon'])
        self.port = self.socket.getsockname()[1]
        self.url = "https://%s:%s" % (socket.gethostname(), self.port)
        self.logger.info("Bound to port %s" % self.port)
        self.funcs.update({'HandleEvents':self.HandleEvents,
                           'system.listMethods':self.addr_system_listMethods})
        self.atime = 0
        self.assert_location()
        atexit.register(self.deassert_location)

        if self.__statefields__:
            self.load_state()

    def HandleEvents(self, address, event_list):
        '''Default event handler'''
        return True

    def handle_sslinfo(self, where, ret, ssl_ptr):
        '''This is where we need to handle all ssl negotiation issues'''
        pass

    def _cobalt_marshalled_dispatch(self, data, address):
        """Decode and dispatch XMLRPC requests. Overloaded to pass through
        client address information
        """
        rawparams, method = xmlrpclib.loads(data)
        if len(rawparams) < 2:
            self.logger.error("No authentication included with request from %s" % address[0])
            return xmlrpclib.dumps(xmlrpclib.Fault(2, "No Authentication Info"))
        user = rawparams[0]
        password = rawparams[1]
        params = rawparams[2:]
        # check authentication
        if not self._authenticate_connection(method, user, password, address):
            self.logger.error("Authentication failure from %s" % address[0])
            return xmlrpclib.dumps(xmlrpclib.Fault(3, "Authentication Failure"))
        # generate response
        try:
            # all handlers must take address as the first argument
            response = self._dispatch(method, (address, ) + params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except xmlrpclib.Fault, fault:
            response = xmlrpclib.dumps(fault)
        except TypeError, terror:
            self.logger.error("Client %s called function %s with wrong argument count" %
                           (address[0], method), exc_info=1)
            response = xmlrpclib.dumps(xmlrpclib.Fault(4, terror.args[0]))
        except:
            self.logger.error("Unexpected handler failure", exc_info=1)
            # report exception back to server
            response = xmlrpclib.dumps(xmlrpclib.Fault(1,
                                   "%s:%s" % (sys.exc_type, sys.exc_value)))
        return response

    def _authenticate_connection(self, method, user, password, address):
        '''Authenticate new connection'''
        (user, address, method)
        return password == self.password

    def save_state(self):
        '''Save fields defined in __statefields__ in /var/spool/cobalt/__implementation__'''
        if self.__statefields__:
            self.logger.debug("saving state for %s" % self.__statefields__)
            savedata = tuple([getattr(self, field) for field in self.__statefields__])
        try:
            statefile = open("/var/spool/cobalt/%s" % self.__implementation__, 'w')
            # need to flock here
            #print cPickle.dumps(savedata)
            #statefile.write(cPickle.dumps(savedata))
            cPickle.dump( savedata, statefile )
            statefile.close()
        except:
            self.logger.info("Statefile save failed; data persistence disabled: %s" % sys.exc_info()[1])
            self.__statefields__ = []

    def load_state(self):
        '''Load fields defined in __statefields__ from /var/spool/cobalt/__implementation__'''
        if self.__statefields__:
            self.logger.debug("loading state for %s" % self.__statefields__)
            try:
                #statefile = open("/var/spool/cobalt/%s" % self.__implementation__, 'r')
                #loaddata = cPickle.loads(statefile.read())
                statefile = "/var/spool/cobalt/%s" % self.__implementation__
                loaddata = cPickle.load( file(statefile) )
                #statefile.close()
            except:
                self.logger.info("Statefile load failed %s" % sys.exc_info()[1])
                return
            for field in self.__statefields__:
                setattr(self, field, loaddata[self.__statefields__.index(field)])
                
    def addr_system_listMethods(self, address):
        """get rid of the address argument and call the underlying dispatcher method"""
        return SimpleXMLRPCServer.SimpleXMLRPCDispatcher.system_listMethods(self)

    def get_request(self):
        '''We need to do work between requests, so select with timeout instead of blocking in accept'''
        rsockinfo = []
        while self.socket not in rsockinfo:
            if self.shut:
                raise socket.error
            for funcname in self.async_funcs:
                func = getattr(self, funcname, False)
                if callable(func):
                    func()
                else:
                    self.logger.error("Cannot call uncallable method %s" % (funcname))
            try:
                rsockinfo = select.select([self.socket], [], [], 10)[0]
            except select.error:
                continue
            if self.socket in rsockinfo:
                # workaround for m2crypto 0.15 bug
                # self.socket.postConnectionCheck = None
                return self.socket.accept()

    def assert_location(self):
        '''Assert component location with slp'''
        if self.__name__ == 'service-location' or self.static:
            return
        if (time.time() - self.atime) > 240:
            slp = Cobalt.Proxy.service_location()
            slp.AssertService({'tag':'location', 'name':self.__name__, 'url':self.url})
            self.atime = time.time()

    def deassert_location(self):
        '''remove registration from slp'''
        if self.__name__ == 'service-location' or self.static:
            return
        slp = Cobalt.Proxy.service_location()
        try:
            slp.DeassertService([{'tag':'location', 'name':self.__name__, 'url':self.url}])
        except xmlrpclib.Fault, fault:
            if fault.faultCode == 11:
                self.logger.error("Failed to deregister self; no matching component")

    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        while not self.shut:
            self.handle_request()

            if self.__statefields__:
                self.save_state()

    def start_shutdown(self, signum, frame):
        '''Shutdown on unexpected signals'''
        self.shut = True

        if self.__statefields__:
            self.save_state()

