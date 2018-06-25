"""RPC client access to cobalt components.

Classes:
ComponentProxy -- an RPC client proxy to Cobalt components

Functions:
load_config -- read configuration files
"""

__revision__ = '$Revision: 2130 $'

from xmlrpclib import ServerProxy, Fault, _Method
from ConfigParser import SafeConfigParser, NoSectionError
import re
import sys
import logging
import socket
import time
import xmlrpclib
import urlparse
import httplib
import ssl
import os.path
import traceback
import datetime
import inspect

import Cobalt
from Cobalt.Exceptions import ComponentLookupError, ComponentOperationError
__all__ = [
    "ComponentProxy", "ComponentLookupError", "RetryMethod",
    "register_component", "find_configured_servers",
]
# FIXME: this cannot be imported from Cobalt.Util because Proxy is imported within Cobalt.Util
def extract_traceback(include_time=True):
    """Extract a traceback, format it nicely and return it.
    This came from trireme.error
    """
    if include_time:
        currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        currenttime = ''
    (exc_cls, exc, tracbk) = sys.exc_info()
    exc_str = traceback.format_exception_only(exc_cls, exc)[0]
    tracebacklst = []
    tracebacklst.append(" ".join(("-" * 32, 'START TRACEBACK', "-" * 30)))
    tracebacklst.append("    Exception  : %s" % (exc_str.strip()))
    tracebacklst.append("    Time       : %s" % currenttime)
    tracebacklst.append("-" * 80)
    stack = traceback.format_tb(tracbk)
    indent = "  "
    for stackpiece in stack:
        stackpiece = stackpiece.strip()
        stackpiece_lst = stackpiece.split(os.linesep)
        for stack_item in stackpiece_lst:
            tracebacklst.append("%s%s|%s" % (indent, currenttime, stack_item))

    tracebacklst.append(" ".join(("-" * 32, 'END TRACEBACK', "-" * 32)))
    return tracebacklst

# FIXME: this cannot be imported from Cobalt.Util because Proxy is imported within Cobalt.Util
def sanitize_password(message):
    """strip the password out of a message"""
    # this patten will remove from a string formatted from an rpc call
    # user:pass@host:port
    # FIXME: use the password to replace
    pattern = re.compile(":([\S]{1,64})@")
    return pattern.sub(":********@", message)

# FIXME: this cannot be imported from Cobalt.Util because Proxy is imported within Cobalt.Util
def get_caller(jump_back_count=1):
    """return the caller of the outer function."""
    try:
        current_frame = inspect.currentframe()
        while jump_back_count > 0:
            current_frame = current_frame.f_back
            jump_back_count -= 1
        frame, filename, line_number, function_name, lines, index = inspect.getouterframes(current_frame)[1]
        fpath, fname = os.path.split(filename)
        caller = "%-13s:L#%s" % (fname, line_number)
    except:
        caller = "UnknownCaller"
    return caller


local_components = dict()
known_servers = dict()

log = logging.getLogger("Proxy")
# To see errors with proxy in the clients, you should turn this on.
# If you don't turn it on, you will see an error with no log handlers for Proxy.
#logging.basicConfig()

class CertificateError(Exception):
    def __init__(self, commonName):
        self.commonName = commonName

class RetryServerProxy(ServerProxy):
    """A Simple proxy wiht it's __getattr__ method overridden to enable
    retries.

    Only overrides the __getattr__.

    """
    #Note to future developers: ServerProxy is a class, not an object.
    #at least that's the case in Python2.x
    #also, don't do this unless you want auto-retries (i.e. the call is
    #idempotent).

    def __init__(self, uri, transport=None, encoding=None, verbose=0,
            allow_none=0, use_datetime=0):
        ServerProxy.__init__(self, uri, transport, 
                encoding, verbose, allow_none, use_datetime)

    def __getattr__(self, name):
        #an even more magiv method dispatcher that includes retries.
        return RetryMethod(self._ServerProxy__request, name)



class RetryMethod(_Method):
    """Method with error handling and retries built in."""
    max_retries = 4
    def __call__(self, *args):
        for retry in range(self.max_retries):
            try:
                retval = _Method.__call__(self, *args)
                return retval
            except xmlrpclib.ProtocolError as err:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("ProtocolError(#%s)[%s]: code:%s msg:%s headers:%s "
                          "error:%s", retry, get_caller(jump_back_count=2), err.errcode, err.errmsg, err.headers, tb_str)
                raise xmlrpclib.Fault(20, "Server Failure")
            except xmlrpclib.Fault as fault:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("xmlrpclib.Fault(#%s)[%s]: faultCode:%s faultString:%s "
                          "error:%s", retry, get_caller(jump_back_count=2), fault.faultCode, fault.faultString, tb_str)
                fault.faultString = sanitize_password(fault.faultString)
                # due to clients using the same code, the error was too verbose and had to be reduced but still sanitized.
                raise fault
                #raise #xmlrpclib.Fault(20, tb_str)
            except socket.error as err:
                # this is the only path that retries
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("socket.error(#%s)[%s]:errno%s error:%s", retry, get_caller(jump_back_count=2), err.errno, tb_str)
                if hasattr(err, 'errno') and err.errno == 336265218:
                    break
                if retry >= (self.max_retries - 1):
                    raise xmlrpclib.Fault(20, tb_str)
            except CertificateError as ce:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("CertificateError(#%s)[%s]: invalid commonName %s from server.  error:%s",
                          retry, get_caller(jump_back_count=2), ce.commonName, tb_str)
                break
            except KeyError:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("KeyError(#%s)[%s]: Server disallowed connection.  error:%s",
                          retry, get_caller(jump_back_count=2), tb_str)
                break
            except Exception:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("KeyError(#%s)[%s]: error:%s", retry, get_caller(jump_back_count=2), tb_str)
                break

            try:
                time.sleep(0.5)
            except IOError:
                tb_str = sanitize_password('\n'.join(extract_traceback()))
                log.error("time.sleep/IOERROR(#%s)[%s]: error:%s", retry, get_caller(jump_back_count=2), tb_str)
                #Yes, you can get an IOError from ppc64 linux kernels
                #It has to do with the select that is used to get sub-second
                #sleeps. We just ignore this attempt if the exception gets
                #thrown Putting this here to avoid a circular dependnecy. --PMR
                pass

        raise xmlrpclib.Fault(20, "Server Failure")

# sorry jon
#xmlrpclib._Method = RetryMethod

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
            log.warning("SSL cert specified, but no key. Cannot authenticate this client with SSL.")
            self.cert = None
            raise Exception, "no SSL key specified"
        if self.key and not self.cert:
            log.warning("SSL key specified, but no cert. Cannot authenticate this client with SSL.")
            raise Exception, "no SSL cert specified"

        rawsock.settimeout(self.timeout)
        self.sock = ssl.SSLSocket(rawsock, cert_reqs=other_side_required,
                                  ca_certs=self.ca, suppress_ragged_eofs=True,
                                  keyfile=self.key, certfile=self.cert,
                                  ssl_version=ssl_protocol_ver)
        try:
            self.sock.connect((self.host, self.port))
        except ssl.SSLError as err:
            log.error("ssl.SSLError: err:%s library:%s reason:%s", err, err.library, err.reason)
            raise
        peer_cert = self.sock.getpeercert()
        if peer_cert and self.scns:
            scn = [x[0][1] for x in peer_cert['subject'] if x[0][0] == 'commonName'][0]
            if scn not in self.scns:
                raise CertificateError, scn
        # reproduce SLP SSLError
        #time.sleep(12.0)
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
        #this is a hack
        try:
            #python 2.7
            self._connection
        except AttributeError:
            #python not 2.7
            host = self.get_host_info(host)[0]
            http = SSLHTTPConnection(host, key=self.key, cert=self.cert, ca=self.ca,
                                 scns=self.scns, timeout=self.timeout)
            https = httplib.HTTP()
            https._setup(http)
        else:
            host, self._extra_headers, x509 = self.get_host_info(host)
            http = SSLHTTPConnection(host, key=self.key, cert=self.cert, ca=self.ca,
                                 scns=self.scns, timeout=self.timeout)
            self._connection = host, http
            https = self._connection[1]
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
        response = self._get_response(h.getfile(), msglen)
        return response

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

def _ComponentProxy(component_name, **kwargs):
    
    """Constructs proxies to components.
    
    Arguments:
    component_name -- name of the component to connect to
    
    Additional arguments are passed to the ServerProxy constructor.
    """
    
    enable_retry = kwargs.get("retry", True)

    if kwargs.get("defer", True):
        return DeferredProxy(component_name, enable_retry)

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
    elif component_name != "service-location":
        try:
            slp = ComponentProxy("service-location")
        except ComponentLookupError:
            raise ComponentLookupError("%s:cn:%s" % (get_caller(), component_name))
        try:
            address = slp.locate(component_name)
        except:
            raise ComponentLookupError("%s:cn:%s" % (get_caller(), component_name))
        if not address:
            raise ComponentLookupError("%s:cn:%s" % (get_caller(), component_name))
        method, path = urlparse.urlparse(address)[:2]
        newurl = "%s://%s:%s@%s" % (method, user, passwd, path)
    else:
        raise ComponentLookupError("%s:cn:%s" % (get_caller(), component_name))

    if enable_retry:
        proxy = RetryServerProxy(newurl, allow_none=True, transport=ssl_trans)
    else:
        proxy = ServerProxy(newurl, allow_none=True, transport=ssl_trans)
    return proxy


def ComponentProxy(component_name, **kwargs):
    """This wraps all ComponentProxy calls to intercept all errors"""
    proxy = None
    try:
        proxy = _ComponentProxy(component_name, **kwargs)
    except:
        #some how we need to get the "error" and modify because on retry=False, it will be a ServerProxy, not a Retry...
        #tb_str = sanitize_password('\n'.join(extract_traceback()))
        #log.error("%s, ComponentProxy: error:%s", get_caller(1), tb_str)
        #print(sanitize_password('\n'.join(extract_traceback())))
        raise
    return proxy


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
    
    def __init__ (self, component_name, retry=True):
        self._component_name = component_name
        self.retry = retry
    
    def __getattr__ (self, attribute):
        return DeferredProxyMethod(self, attribute, self.retry)


class DeferredProxyMethod (object):
    
    def __init__ (self, proxy, func_name, retry=True):
        self._proxy = proxy
        self._func_name = func_name
        self.retry = retry
    
    def __call__ (self, *args):
        proxy = ComponentProxy(self._proxy._component_name, retry=self.retry, defer=False)
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
