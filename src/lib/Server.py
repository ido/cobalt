"""Cobalt component XML-RPC server."""

__revision__ = '$Revision: 758 $'

__all__ = [
    "TCPServer", "XMLRPCRequestHandler", "XMLRPCServer",
    "find_intended_location",
]

import sys
import os
import xmlrpclib
import socket
import SocketServer
import SimpleXMLRPCServer
import base64
import signal
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import logging
import urlparse
import threading
import time

import tlslite.integration.TLSSocketServerMixIn
import tlslite.api
from tlslite.api import \
    TLSSocketServerMixIn, parsePrivateKey, \
    X509, X509CertChain, SessionCache, TLSError

import Cobalt
from Cobalt.Proxy import ComponentProxy


def find_intended_location (component, config_files=None):
    """Determine a component's intended service location.
    
    Arguments:
    component -- component to find records for
    
    Keyword arguments:
    config_files -- list of configuration files to use
    """
    if not config_files:
        config_files = Cobalt.CONFIG_FILES
    config = SafeConfigParser()
    config.read(config_files)
    try:
        url = config.get("components", component.name)
    except (NoSectionError, NoOptionError):
        return ('', 0)
    location = urlparse.urlparse(url)[1]
    if ":" in location:
        host, port = location.split(":")
        port = int(port)
        location = ('', port)
    else:
        location = ('', 0)
    return location


class TLSConnection (tlslite.api.TLSConnection):
    
    """TLSConnection supporting additional socket methods.
    
    Methods:
    shutdown -- shut down the underlying socket
    """
    
    def shutdown (self, *args, **kwargs):
        """Shut down the underlying socket."""
        return self.sock.shutdown(*args, **kwargs)

#monkeypatch TLSSocketServerMixIn's module to use new TLSConnection
tlslite.integration.TLSSocketServerMixIn.TLSConnection = TLSConnection


if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and sys.version_info[1] < 5):
    class SimpleXMLRPCDispatcher (SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
        
        def __init__ (self, allow_none, encoding):
            SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
            self.allow_none = allow_none
            self.encoding = encoding
        
        def _marshaled_dispatch (self, data, dispatch_method=None):
            try:
                params, method = xmlrpclib.loads(data)
                if dispatch_method is not None:
                    response = dispatch_method(method, params)
                else:
                    response = self._dispatch(method, params)
                response = (response,)
                response = xmlrpclib.dumps(response, methodresponse=1,
                    allow_none=self.allow_none, encoding=self.encoding)
            except xmlrpclib.Fault, fault:
                response = xmlrpclib.dumps(fault,
                    allow_none=self.allow_none, encoding=self.encoding)
            except:
                # report exception back to server
                response = xmlrpclib.dumps(
                    xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value)),
                    allow_none=self.allow_none, encoding=self.encoding)
            return response
    
else:
    SimpleXMLRPCDispatcher = SimpleXMLRPCServer.SimpleXMLRPCDispatcher


class TCPServer (TLSSocketServerMixIn, SocketServer.TCPServer, object):
    
    """TCP server supporting SSL encryption.
    
    Methods:
    handshake -- perform a SSL/TLS handshake
    
    Properties:
    url -- A url pointing to this server.
    """
    
    allow_reuse_address = True
    logger = logging.getLogger("Cobalt.Server.TCPServer")
    
    def __init__ (self, server_address, RequestHandlerClass, keyfile=None, certfile=None, reqCert=False, timeout=None):
        
        """Initialize the SSL-TCP server.
        
        Arguments:
        server_address -- address to bind to the server
        RequestHandlerClass -- class to handle requests
        
        Keyword arguments:
        keyfile -- private encryption key filename (enables ssl encryption)
        certfile -- certificate file (enables ssl encryption)
        reqCert -- client must present certificate
        timeout -- timeout for non-blocking request handling
        """
        
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        
        self.socket.settimeout(timeout)
        
        if keyfile or certfile:
            self.private_key = parsePrivateKey(open(keyfile or certfile).read())
            x509 = X509()
            x509.parse(open(certfile or keyfile).read())
            self.certificate_chain = X509CertChain([x509])
        else:
            if reqCert:
                raise TypeError("use of reqCert requires a keyfile/certfile")
            self.private_key = None
            self.certificate_chain = None
        self.request_certificate = reqCert
        self.sessions = SessionCache()
    
    def handshake (self, connection):
        
        """Perform the SSL/TLS handshake.
        
        Arguments:
        connection -- handshake through this connection
        """
        
        try:
            connection.handshakeServer(
                certChain = self.certificate_chain,
                privateKey = self.private_key,
                reqCert = self.request_certificate,
                sessionCache = self.sessions,
            )
        except TLSError, e:
            return False
        
        connection.ignoreAbruptClose = True
        return True
    
    def finish_request (self, *args, **kwargs):
        """Support optional ssl/tls handshaking."""
        if self.private_key and self.certificate_chain:
            cls = TLSSocketServerMixIn
        else:
            cls = SocketServer.TCPServer
        try:
            cls.finish_request(self, *args, **kwargs)
        except socket.error:
            self.logger.error("Socket error occurred in send")
    
    def _get_secure (self):
        return self.private_key and self.certificate_chain
    secure = property(_get_secure)
    
    def _get_url (self):
        port = self.socket.getsockname()[1]
        hostname = socket.gethostname()
        if self.secure:
            protocol = "https"
        else:
            protocol = "http"
        return "%s://%s:%i" % (protocol, hostname, port)
    url = property(_get_url)


class XMLRPCRequestHandler (SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    
    """Component XML-RPC request handler.
    
    Adds support for HTTP authentication.
    
    Exceptions:
    CouldNotAuthenticate -- client did not present acceptable authentication information
    
    Methods:
    authenticate -- prompt a check of a client's provided username and password
    handle_one_request -- handle a single rpc (optionally authenticating)
    """
    logger = logging.getLogger("Cobalt.Server.XMLRPCRequestHandler")
    
    class CouldNotAuthenticate (Exception):
        """Client did not present acceptible authentication information."""
    
    require_auth = True
    credentials = {'root':'default'}
    try:
        config = SafeConfigParser()
        config.read(Cobalt.CONFIG_FILES)
        credentials['root'] = config.get('communication', 'password')
    except:
        pass
    
    def authenticate (self):
        """Authenticate the credentials of the latest client."""
        try:
            header = self.headers['Authorization']
        except KeyError:
            self.logger.error("No authentication data presented")
            raise self.CouldNotAuthenticate("client did not present credentials")
        auth_type, auth_content = header.split()
        auth_content = base64.standard_b64decode(auth_content)
        try:
            username, password = auth_content.split(":")
        except ValueError:
            username = auth_content
            password = ""
        try:
            valid_password = self.credentials[username]
        except KeyError:
            raise self.CouldNotAuthenticate("unknown user: %s" % username)
        if password != valid_password:
            raise self.CouldNotAuthenticate("invalid password for %s" % username)
    
    def parse_request (self):
        """Extends parse_request.
        
        Optionally check HTTP authentication when parsing."""
        if not SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.parse_request(self):
            return False
        if self.require_auth:
            try:
                self.authenticate()
            except self.CouldNotAuthenticate, e:
                self.logger.error("Authentication failed: %s" % e.message)
                code = 401
                message, explanation = self.responses[401]
                self.send_error(code, message)
                return False
        return True


class XMLRPCServer (TCPServer, SimpleXMLRPCDispatcher, object):
    
    """Component XMLRPCServer.
    
    Methods:
    serve_daemon -- serve_forever in a daemonized process
    serve_forever -- handle_one_request until not self.serve
    shutdown -- stop serve_forever (by setting self.serve = False)
    ping -- return all arguments received
    
    RPC methods:
    ping
    
    (additional system.* methods are inherited from base dispatcher)
    
    Properties:
    require_auth -- the request handler is requiring authorization
    credentials -- valid credentials being used for authentication
    """
    
    def __init__ (self, server_address, RequestHandlerClass=None,
                  keyfile=None, certfile=None,
                  timeout=10,
                  logRequests=False,
                  register=True, allow_none=True, encoding=None):
        
        """Initialize the XML-RPC server.
        
        Arguments:
        server_address -- address to bind to the server
        RequestHandlerClass -- request handler used by TCP server (optional)
        
        Keyword arguments:
        keyfile -- private encryption key filename
        certfile -- certificate file
        logRequests -- log all requests (default False)
        register -- presence should be reported to service-location (default True)
        allow_none -- allow None values in xml-rpc
        encoding -- encoding to use for xml-rpc (default UTF-8)
        """
        
        SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding)
        
        if not RequestHandlerClass:
            class RequestHandlerClass (XMLRPCRequestHandler):
                """A subclassed request handler to prevent class-attribute conflicts."""
        
        TCPServer.__init__(self,
            server_address, RequestHandlerClass,
            timeout=timeout, keyfile=keyfile, certfile=certfile)
        self.logRequests = logRequests
        self.serve = False
        self.register = register
        self.register_introspection_functions()
        self.register_function(self.ping)
        self.logger.info("service available at %s" % self.url)
    
    def _get_register (self):
        return self._register
    
    def _set_register (self, value):
        old_value = getattr(self, "_register", False)
        self._register = value
        if value and not old_value:
            thread = threading.Thread(target=self._slp_thread)
            thread.setDaemon(True)
            thread.start()
    
    register = property(_get_register, _set_register)
    
    def register_instance (self, instance, *args, **kwargs):
        SimpleXMLRPCDispatcher.register_instance(self, instance, *args, **kwargs)
        try:
            name = instance.name
        except AttributeError:
            name = "unknown"
        if self.register:
            self.register_with_slp()
        self.logger.info("serving %s at %s" % (name, self.url))
    
    def register_with_slp (self):
        try:
            name = self.instance.name
        except AttributeError:
            self.logger.error("register_with_slp() [unknown component]")
            return
        try:
            ComponentProxy("service-location").register(name, self.url)
        except Exception, e:
            self.logger.error("register_with_slp() [%s]" % (e))
        else:
            self.logger.info("register_with_slp()")
    
    def unregister_with_slp (self):
        try:
            name = self.instance.name
        except AttributeError:
            return
        try:
            ComponentProxy("service-location").unregister(name)
        except Exception, e:
            self.logger.error("unregister_with_slp() [%s]" % (e))
        else:
            self.logger.info("unregister_with_slp()")
    
    def _slp_thread (self, frequency=120):
        try:
            while self.register:
                self.register_with_slp()
                time.sleep(frequency)
        except:
            self.logger.error("slp_thread failed", exc_info=1)
    
    def server_close (self):
        TCPServer.server_close(self)
        if self.register:
            self.register = False
            self.unregister_with_slp()
        self.logger.info("server_close()")
    
    def _get_require_auth (self):
        return getattr(self.RequestHandlerClass, "require_auth", False)
    def _set_require_auth (self, value):
        self.RequestHandlerClass.require_auth = value
    require_auth = property(_get_require_auth, _set_require_auth)
    
    def _get_credentials (self):
        try:
            return self.RequestHandlerClass.credentials
        except AttributeError:
            return dict()
    def _set_credentials (self, value):
        self.RequestHandlerClass.credentials = value
    credentials = property(_get_credentials, _set_credentials)
    
    def serve_forever (self):
        """Serve single requests until (self.serve == False)."""
        self.serve = True
        self.logger.info("serve_forever() [start]")
        #sigint = signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        #sigterm = signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
        try:
            while self.serve:
                try:
                    self.handle_request()
                except socket.timeout:
                    pass
                if self.instance and hasattr(self.instance, "do_tasks"):
                    try:
                        self.instance.do_tasks()
                    except:
                        self.logger.error("Task executaion failure", exc_info=1)
        finally:
            #signal.signal(signal.SIGINT, sigint)
            #signal.signal(signal.SIGTERM, sigterm)
            self.logger.info("serve_forever() [stop]")
    
    def shutdown (self):
        """Signal that automatic service should stop."""
        self.serve = False
    
    def _handle_shutdown_signal (self, signum, frame):
        self.shutdown()
    
    def ping (self, *args):
        """Echo response."""
        self.logger.info("ping(%s)" % (", ".join([repr(arg) for arg in args])))
        return args
