"""Cobalt component XML-RPC server."""

__revision__ = '$Revision$'

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
import inspect
import signal
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import logging
import urlparse
import threading
import time
import ssl

import Cobalt
from Cobalt.Proxy import ComponentProxy

class ForkedChild(Exception):
    pass

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



class CobaltXMLRPCDispatcher (SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    logger = logging.getLogger("Cobalt.Server.CobaltXMLRPCDispatcher")
    def __init__ (self, allow_none, encoding):
        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self,
                                                           allow_none,
                                                           encoding)
        self.allow_none = allow_none
        self.encoding = encoding

    def _marshaled_dispatch (self, data):
        method_func = None
        params, method = xmlrpclib.loads(data)
        try:
            response = self.instance._dispatch(method, params, self.funcs)
            response = (response,)
            raw_response = xmlrpclib.dumps(response, methodresponse=1,
                                           allow_none=self.allow_none,
                                           encoding=self.encoding)
        except xmlrpclib.Fault, fault:
            raw_response = xmlrpclib.dumps(fault,
                                           allow_none=self.allow_none,
                                           encoding=self.encoding)
        except:
            # report exception back to server
            raw_response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value)),
                allow_none=self.allow_none, encoding=self.encoding)
        return raw_response



class SSLServer (SocketServer.TCPServer, object):

    """TCP server supporting SSL encryption.

    Methods:
    handshake -- perform a SSL/TLS handshake

    Properties:
    url -- A url pointing to this server.

    """

    allow_reuse_address = True
    logger = logging.getLogger("Cobalt.Server.TCPServer")

    def __init__(self, server_address, RequestHandlerClass, keyfile=None,
                 certfile=None, reqCert=False, ca=None, timeout=None, protocol='xmlrpc/ssl'):

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

        all_iface_address = ('', server_address[1])
        try:
            SocketServer.TCPServer.__init__(self, all_iface_address,
                                            RequestHandlerClass)
        except socket.error:
            self.logger.error("Failed to bind to socket")
            raise

        self.timeout = timeout
        self.socket.settimeout(timeout)
        self.keyfile = keyfile
        if keyfile != None:
            if keyfile == False or not os.path.exists(keyfile):
                self.logger.error("Keyfile %s does not exist" % keyfile)
                raise Exception, "keyfile doesn't exist"
        self.certfile = certfile
        if certfile != None:
            if certfile == False or not os.path.exists(certfile):
                self.logger.error("Certfile %s does not exist" % certfile)
                raise Exception, "certfile doesn't exist"
        self.ca = ca
        if ca != None:
            if ca == False or not os.path.exists(ca):
                self.logger.error("CA %s does not exist" % ca)
                raise Exception, "ca doesn't exist"
        self.reqCert = reqCert
        if ca and certfile:
            self.mode = ssl.CERT_OPTIONAL
        else:
            self.mode = ssl.CERT_NONE
        if protocol == 'xmlrpc/ssl':
            self.ssl_protocol = ssl.PROTOCOL_SSLv23
        elif protocol == 'xmlrpc/tlsv1':
            self.ssl_protocol = ssl.PROTOCOL_TLSv1
        else:
            self.logger.error("Unknown protocol %s" % (protocol))
            raise Exception, "unknown protocol %s" % protocol

    def get_request(self):
        (sock, sockinfo) = self.socket.accept()
        sock.settimeout(self.timeout)
        sslsock = ssl.wrap_socket(sock, server_side=True, certfile=self.certfile,
                                  keyfile=self.keyfile, cert_reqs=self.mode,
                                  ca_certs=self.ca, ssl_version=self.ssl_protocol)
        return sslsock, sockinfo

    def close_request(self, request):
        # request.unwrap()
        request.close()

    def _get_url(self):
        port = self.socket.getsockname()[1]
        hostname = socket.gethostname()
        protocol = "https"
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
                self.logger.error("Authentication failed: %s" % e.args[0])
                code = 401
                message, explanation = self.responses[401]
                self.send_error(code, message)
                return False
        return True

    ### FIXME need to override do_POST here
    def do_POST(self):
        try:
            max_chunk_size = 10*1024*1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                L.append(self.rfile.read(chunk_size))
                size_remaining -= len(L[-1])
            data = ''.join(L)

            response = self.server._marshaled_dispatch(data)
        except: 
            raise
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
            self.connection.shutdown(1)
   

class BaseXMLRPCServer (SSLServer, CobaltXMLRPCDispatcher, object):
    
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
                  register=True, allow_none=True, encoding=None, cafile=None):
        
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
        
        CobaltXMLRPCDispatcher.__init__(self, allow_none, encoding)
        
        if not RequestHandlerClass:
            class RequestHandlerClass (XMLRPCRequestHandler):
                """A subclassed request handler to prevent class-attribute conflicts."""

        SSLServer.__init__(self,
            server_address, RequestHandlerClass,
            timeout=timeout, keyfile=keyfile, certfile=certfile, reqCert=True, ca=cafile)
        self.logRequests = logRequests
        self.serve = False
        self.register = register
        self.register_introspection_functions()
        self.register_function(self.ping)
        self.logger.info("service available at %s" % self.url)
        self.timeout = timeout

    
    def register_instance (self, instance, *args, **kwargs):
        CobaltXMLRPCDispatcher.register_instance(self, instance, *args, **kwargs)
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





    # these two "thread" functions need to be in a giant while loop inside serve_forever
    def _slp_thread (self, frequency=120):
        try:
            while self.register:
                self.register_with_slp()
                time.sleep(frequency)
        except:
            self.logger.error("slp_thread failed", exc_info=1)

    def _tasks_thread (self):
        try:
            while self.serve:
                try:
                    if self.instance and hasattr(self.instance, 'do_tasks'):
                        self.instance.do_tasks()
                except:
                    self.logger.error("Unexpected task failure", exc_info=1)
                time.sleep(self.timeout)
        except:
            self.logger.error("tasks_thread failed", exc_info=1)
    
    
    
    
    
    def server_close (self):
        SSLServer.server_close(self)
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
    
    def serve_forever (self, frequency=120):
        """Serve single requests until (self.serve == False)."""
        self.serve = True
        self.logger.info("serve_forever() [start]")
        sigint = signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        sigterm = signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
        last_register = 0

        try:
            while self.serve:
                try:
                    self.handle_request()
                except socket.timeout:
                    pass
                except:
                    self.logger.error("Got unexpected error in handle_request",
                                      exc_info=True)
                if self.instance and hasattr(self.instance, "do_tasks"):
                    try:
                        self.instance.do_tasks()
                    except:
                        self.logger.error("Task executaion failure", exc_info=1)
                        
                try:
                    now = time.time()
                    if self.register and (now - last_register) > frequency:
                        self.register_with_slp()
                        last_register = now
                except:
                    self.logger.error("register_with_slp failed", exc_info=True)
                        
        finally:
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


class XMLRPCServer (SocketServer.ThreadingMixIn, BaseXMLRPCServer): 
    
    def __init__ (self, server_address, RequestHandlerClass=None,
                  keyfile=None, certfile=None,
                  timeout=10,
                  logRequests=False,
                  register=True, allow_none=True, encoding=None, cafile=None):
        
        
        BaseXMLRPCServer.__init__(self, server_address, RequestHandlerClass, keyfile, 
                                  certfile, timeout, logRequests, register, allow_none, encoding, cafile=cafile)
        
        self.task_thread = threading.Thread(target=self._tasks_thread)

    
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
    
    def _slp_thread (self, frequency=120):
        try:
            while self.register:
                self.register_with_slp()
                time.sleep(frequency)
        except:
            self.logger.error("slp_thread failed", exc_info=1)

    def _tasks_thread (self):
        try:
            while self.serve:
                try:
                    if self.instance and hasattr(self.instance, 'do_tasks'):
                        self.instance.do_tasks()
                except:
                    self.logger.error("Unexpected task failure", exc_info=1)
                time.sleep(self.timeout)
        except:
            self.logger.error("tasks_thread failed", exc_info=1)
    
    
    def serve_forever (self):
        """Serve single requests until (self.serve == False)."""
        self.serve = True
        master_pid = os.getpid()
        self.task_thread.start()
        self.logger.info("serve_forever() [start]")
        sigint = signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        sigterm = signal.signal(signal.SIGTERM, self._handle_shutdown_signal)

        try:
            while self.serve:
                try:
                    self.handle_request()
                except socket.timeout:
                    pass
                except:
                    self.logger.error("Got unexpected error in handle_request",
                                      exc_info=1)
        finally:
            self.logger.info("serve_forever() [stop]")
    
