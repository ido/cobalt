"""RPC client access to cobalt components.

Classes:
ComponentProxy -- an RPC client proxy to Cobalt components

Functions:
load_config -- read configuration files
"""

__revision__ = '$Revision$'

from xmlrpclib import ServerProxy, Fault, _Method
from ConfigParser import SafeConfigParser, NoSectionError
import logging
import socket
import time
import xmlrpclib
import urlparse
import httplib
import ssl
import os.path

import Cobalt
from Cobalt.Exceptions import ComponentLookupError, ComponentOperationError

__all__ = [
    "ComponentProxy", "ComponentLookupError", "RetryMethod",
    "register_component", "find_configured_servers",
]

local_components = dict()
known_servers = dict()

log = logging.getLogger("Proxy")

class CertificateError(Exception):
    def __init__(self, commonName):
        self.commonName = commonName


class RetryMethod(_Method):
    """Method with error handling and retries built in."""
    max_retries = 4
    def __call__(self, *args):
        for retry in range(self.max_retries):
            try:
                return _Method.__call__(self, *args)
            except xmlrpclib.ProtocolError, err:
                log.error("Server failure: Protocol Error: %s %s" % \
                              (err.errcode, err.errmsg))
                raise xmlrpclib.Fault(20, "Server Failure")
            except xmlrpclib.Fault:
                raise
            except socket.error, err:
                if hasattr(err, 'errno') and err.errno == 336265218:
                    log.error("SSL Key error")
                    break
                if retry == 3:
                    log.error("Server failure: %s" % err)
                    raise xmlrpclib.Fault(20, err)
            except CertificateError, ce:
                log.error("Got unallowed commonName %s from server" \
                               % ce.commonName)
                break
            except KeyError:
                log.error("Server disallowed connection")
                break
            except:
                log.error("Unknown failure", exc_info=1)
                break
            time.sleep(0.5)
        raise xmlrpclib.Fault(20, "Server Failure")

# sorry jon
xmlrpclib._Method = RetryMethod

class SSLHTTPConnection(httplib.HTTPConnection):
    """Extension of HTTPConnection that implements SSL and related behaviors."""

    def __init__(self, host, port=None, strict=None, timeout=90, key=None,
                 cert=None, ca=None, scns=None, protocol='xmlrpc/ssl'):
        """Initializes the `httplib.HTTPConnection` object and stores security
        parameters

        Parameters
        ----------
        host : string
            Name of host to contact
        port : int, optional
            Port on which to contact the host.  If none is specified,
            the default port of 80 will be used unless the `host`
            string has a port embedded in the form host:port.
        strict : Boolean, optional
            Passed to the `httplib.HTTPConnection` constructor and if
            True, causes the `BadStatusLine` exception to be raised if
            the status line cannot be parsed as a valid HTTP 1.0 or
            1.1 status.
        timeout : int, optional
            Causes blocking operations to timeout after `timeout`
            seconds.
        key : string, optional
            The file system path to the local endpoint's SSL key.  May
            specify the same file as `cert` if using a file that
            contains both.  See
            http://docs.python.org/library/ssl.html#ssl-certificates
            for details.  Required if using xmlrpc/ssl with client
            certificate authentication.
        cert : string, optional
            The file system path to the local endpoint's SSL
            certificate.  May specify the same file as `cert` if using
            a file that contains both.  See
            http://docs.python.org/library/ssl.html#ssl-certificates
            for details.  Required if using xmlrpc/ssl with client
            certificate authentication.
        ca : string, optional
            The file system path to a set of concatenated certificate
            authority certs, which are used to validate certificates
            passed from the other end of the connection.
        scns : array-like, optional
            List of acceptable server commonNames.  The peer cert's
            common name must appear in this list, otherwise the
            connect() call will throw a `CertificateError`.
        protocol : {'xmlrpc/ssl', 'xmlrpc/tlsv1'}, optional
            Communication protocol to use.

        """
    
        httplib.HTTPConnection.__init__(self, host, port, strict, timeout)
        self.key = key
        self.cert = cert
        self.ca = ca
        self.scns = scns
        self.protocol = protocol
        self.timeout = timeout

    def connect(self):
        """Initiates a connection using the ssl module."""
        rawsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.protocol == 'xmlrpc/ssl':
            ssl_protocol_ver = ssl.PROTOCOL_SSLv23
        else:
            log.error("Unknown protocol %s" % (self.protocol))
            raise Exception, "unknown protocol %s" % self.protocol
        if self.ca:
            other_side_required = ssl.CERT_REQUIRED
        else:
            other_side_required = ssl.CERT_NONE
            log.warning("No ca is specified. Cannot authenticate the server with SSL.")
        if self.cert and not self.key:
            log.warning("SSL cert specfied, but no key. Cannot authenticate this client with SSL.")
            self.cert = None
            raise Exception, "no SSL key specified"
        if self.key and not self.cert:
            log.warning("SSL key specfied, but no cert. Cannot authenticate this client with SSL.")
            raise Exception, "no SSL cert specified"

        rawsock.settimeout(self.timeout)
        self.sock = ssl.SSLSocket(rawsock, cert_reqs=other_side_required,
                                  ca_certs=self.ca, suppress_ragged_eofs=True,
                                  keyfile=self.key, certfile=self.cert,
                                  ssl_version=ssl_protocol_ver)
        self.sock.connect((self.host, self.port))
        peer_cert = self.sock.getpeercert()
        if peer_cert and self.scns:
            scn = [x[0][1] for x in peer_cert['subject'] if x[0][0] == 'commonName'][0]
            if scn not in self.scns:
                raise CertificateError, scn
        self.sock.closeSocket = True


class XMLRPCTransport(xmlrpclib.Transport):
    def __init__(self, key=None, cert=None, ca=None, scns=None, use_datetime=0, timeout=90):
        if hasattr(xmlrpclib.Transport, '__init__'):
            xmlrpclib.Transport.__init__(self, use_datetime)
        self.key = key
        self.cert = cert
        self.ca = ca
        self.scns = scns
        self.timeout = timeout

    def make_connection(self, host):
        host = self.get_host_info(host)[0]
        http = SSLHTTPConnection(host, key=self.key, cert=self.cert, ca=self.ca,
                                 scns=self.scns, timeout=self.timeout)
        https = httplib.HTTP()
        https._setup(http)
        return https

    def request(self, host, handler, request_body, verbose=0):
        """Send request to server and return response."""
        h = self.make_connection(host)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise xmlrpclib.ProtocolError(host + handler, errcode, errmsg, headers)

        self.verbose = verbose
        msglen = int(headers.dict['content-length'])
        return self._get_response(h.getfile(), msglen)

    def _get_response(self, fd, length):
        # read response from input file/socket, and parse it
        recvd = 0

        p, u = self.getparser()

        while recvd < length:
            rlen = min(length - recvd, 1024)
            response = fd.read(rlen)
            recvd += len(response)
            if not response:
                break
            if self.verbose:
                print "body:", repr(response), len(response)
            p.feed(response)

        fd.close()
        p.close()

        return u.close()


def register_component (component):
    local_components[component.name] = component


def ComponentProxy(component_name, **kwargs):
    
    """Constructs proxies to components.
    
    Arguments:
    component_name -- name of the component to connect to
    
    Additional arguments are passed to the ServerProxy constructor.
    """
    

    
    if kwargs.get("defer", True):
        return DeferredProxy(component_name)

    user = 'root'
    try:
        config = SafeConfigParser()
        config.read(Cobalt.CONFIG_FILES)
        passwd = config.get('communication', 'password')
        keypath = os.path.expandvars(config.get('communication', 'key'))
        certpath = os.path.expandvars(config.get('communication', 'cert'))
        capath = os.path.expandvars(config.get('communication', 'ca'))
    except:
        passwd = 'default'
        keypath = None
        certpath = None
        capath = None

    ssl_trans = XMLRPCTransport(keypath, certpath, capath, timeout=90)    
    
    if component_name in local_components:
        return LocalProxy(local_components[component_name])
    elif component_name in known_servers:
        method, path = urlparse.urlparse(known_servers[component_name])[:2]
        newurl = "%s://%s:%s@%s" % (method, user, passwd, path)
        return ServerProxy(newurl, allow_none=True, transport=ssl_trans)
    elif component_name != "service-location":
        try:
            slp = ComponentProxy("service-location")
        except ComponentLookupError:
            raise ComponentLookupError(component_name)
        try:
            address = slp.locate(component_name)
        except:
            raise ComponentLookupError(component_name)
        if not address:
            raise ComponentLookupError(component_name)
        method, path = urlparse.urlparse(address)[:2]
        newurl = "%s://%s:%s@%s" % (method, user, passwd, path)
        return ServerProxy(newurl, allow_none=True, transport=ssl_trans)
    else:
        raise ComponentLookupError(component_name)




class LocalProxy (object):
    
    """Proxy-like filter for inter-component communication.
    
    Used to access other components stored in local memory,
    without having to transport across tcp/http.
    
    Dispatches method calls through the component's _dispatch
    method to keep the interface between this and ServerProxy
    consistent.
    """
    
    def __init__ (self, component):
        self._component = component
    
    def __getattr__ (self, attribute):
        return LocalProxyMethod(self, attribute)


class LocalProxyMethod (object):
    
    def __init__ (self, proxy, func_name):
        self._proxy = proxy
        self._func_name = func_name
    
    def __call__ (self, *args):
        return self._proxy._component._dispatch(self._func_name, args, dict())


class DeferredProxy (object):
    
    """Defering proxy object.
    
    Gets a new proxy when it can't connect to a component.
    """
    
    def __init__ (self, component_name):
        self._component_name = component_name
    
    def __getattr__ (self, attribute):
        return DeferredProxyMethod(self, attribute)


class DeferredProxyMethod (object):
    
    def __init__ (self, proxy, func_name):
        self._proxy = proxy
        self._func_name = func_name
    
    def __call__ (self, *args):
        proxy = ComponentProxy(self._proxy._component_name, defer=False)
        func = getattr(proxy, self._func_name)
        return func(*args)


def find_configured_servers (config_files=None):
    """Read associated config files into the module.
    
    Arguments:
    config_files -- a list of paths to config files.
    """
    if not config_files:
        config_files = Cobalt.CONFIG_FILES
    config = SafeConfigParser()
    config.read(config_files)
    try:
        components = config.options("components")
    except NoSectionError:
        return []
    known_servers.clear()
    known_servers.update(dict([
        (component, config.get("components", component))
        for component in components
    ]))
    return known_servers.copy()

find_configured_servers()
