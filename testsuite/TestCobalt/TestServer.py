import os
import socket
import threading
import xmlrpclib
import ssl
import ConfigParser

import Cobalt.Server
from Cobalt.Server import find_intended_location, XMLRPCServer
from Cobalt.Components.base import Component

cp = ConfigParser.ConfigParser()
cp.read("testsuite/configs/cobalt.test_server.conf")
keypath = os.path.expandvars(cp.get('communication', 'key'))
certpath = os.path.expandvars(cp.get('communication', 'cert'))
capath = os.path.expandvars(cp.get('communication', 'ca'))


c = Component()

class TestFindIntendedLocation (object):
    
    def setup (self):
        assert not os.path.exists("testfile")
    
    def teardown (self):
        try:
            os.remove("testfile")
        except OSError:
            assert not os.path.exists("testfile")
    
    def test_nofile (self):
        component = Component()
        location = find_intended_location(component, config_files=["testfile"])
        assert location == ("", 0)
    
    def test_file_without_def (self):
        testfile = open("testfile", "w")
        print >> testfile, "[components]"
        print >> testfile, "someothercomponent=https://localhost:8080"
        testfile.close()
        component = Component()
        location = find_intended_location(component, config_files=["testfile"])
        assert location == ("", 0)
    
    def test_file_with_bad_def (self):
        testfile = open("testfile", "w")
        print >> testfile, "[components]"
        print >> testfile, "component=notaurl"
        testfile.close()
        component = Component()
        location = find_intended_location(component, config_files=["testfile"])
        assert location == ("", 0)
    
    def test_file_with_def (self):
        testfile = open("testfile", "w")
        print >> testfile, "[components]"
        print >> testfile, "component=https://localhost:8080"
        testfile.close()
        component = Component()
        location = find_intended_location(component, config_files=["testfile"])
        assert location == ("", 8080)
    
    def test_file_with_def_noport (self):
        testfile = open("testfile", "w")
        print >> testfile, "[components]"
        print >> testfile, "component=https://localhost"
        testfile.close()
        component = Component()
        location = find_intended_location(component, config_files=["testfile"])
        assert location == ("", 0)


class XMLRPCServerTester (object):

    def setup (self):
        self._outside_credentials = Cobalt.Server.XMLRPCRequestHandler.credentials
        self._outside_require_auth = Cobalt.Server.XMLRPCRequestHandler.require_auth
        Cobalt.Server.XMLRPCRequestHandler.credentials = None
        Cobalt.Server.XMLRPCRequestHandler.require_auth = False
    
    def teardown (self):
        Cobalt.Server.XMLRPCRequestHandler.credentials = self._outside_credentials
        Cobalt.Server.XMLRPCRequestHandler.require_auth = self._outside_require_auth
        self.server.server_close()
    
    def test_require_auth (self):
        assert not self.server.require_auth
        self.server.RequestHandlerClass.require_auth = True
        assert self.server.require_auth
        self.server.require_auth = False
        assert not self.server.require_auth
    
    def test_credentials (self):
        assert self.server.credentials == \
            self.server.RequestHandlerClass.credentials == None
        self.server.credentials = dict()
        assert self.server.credentials is \
            self.server.RequestHandlerClass.credentials == dict()
        self.server.credentials['user'] = "pass"
        assert self.server.credentials is \
            self.server.RequestHandlerClass.credentials == dict(user="pass")
    
    #def test_secure (self):
    #    raise NotImplemented("This test has not been implemented.")
    
    #def test_url (self):
    #    raise NotImplemented("This test has not been implemented.")
    
    def test_listMethods (self):
        server_thread = threading.Thread(target=self.server.handle_request)
        server_thread.start()
        methods = self.proxy.system.listMethods()
        assert set(methods) == set(["ping", "system.listMethods", "system.methodHelp", "system.methodSignature"])
        server_thread.join()
    
    def test_ping (self):
        server_thread = threading.Thread(target=self.server.handle_request)
        server_thread.start()
        sent_args = (1, 5, 8, 2)
        received_args = self.proxy.ping(*sent_args)
        assert list(received_args) == list(sent_args)
        server_thread.join()


class TestXMLRPCServer_http (XMLRPCServerTester):
    
    def setup (self):
        XMLRPCServerTester.setup(self)
        self.server = XMLRPCServer(("localhost", 5900), register=False, keyfile=keypath, certfile=certpath, cafile=capath)
        self.server.register_instance(c)
        self.proxy = xmlrpclib.ServerProxy("https://localhost:5900")
    
    def test_secure (self):
        assert ssl.PROTOCOL_SSLv23 == self.server.ssl_protocol, self.server.ssl_protocol
    
    def test_url (self):
        hname = socket.gethostname()
        assert self.server.url == "https://%s:5900" % hname, self.server.url


class TestXMLRPCServer_http_auth (TestXMLRPCServer_http):
    
    def setup (self):
        XMLRPCServerTester.setup(self)
        self.server = XMLRPCServer(("localhost", 5900), register=False, keyfile=keypath, certfile=certpath, cafile=capath)
        self.server.require_auth = True
        self.server.credentials = dict(user="pass")
        self.server.register_instance(c)
        self.proxy = xmlrpclib.ServerProxy("https://user:pass@localhost:5900")
    
    def test_require_auth (self):
        assert self.server.require_auth == \
            self.server.RequestHandlerClass.require_auth == True
        self.server.RequestHandlerClass.require_auth = False
        assert self.server.require_auth == \
            self.server.RequestHandlerClass.require_auth == False
        self.server.require_auth = True
        assert self.server.require_auth == \
            self.server.RequestHandlerClass.require_auth == True
    
    def test_credentials (self):
        assert self.server.credentials is \
            self.server.RequestHandlerClass.credentials == dict(user="pass")
        self.server.credentials = None
        assert self.server.credentials is \
            self.server.RequestHandlerClass.credentials is None
    
    def test_ping_without_auth (self):
        self.proxy = xmlrpclib.ServerProxy("https://localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.ProtocolError:
            pass
        else:
            assert not "Allowed unauthorized access."
    
    def test_ping_unknown_user (self):
        self.proxy = xmlrpclib.ServerProxy("https://otheruser@localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.ProtocolError:
            pass
        else:
            assert not "Allowed unauthorized access."
    
    def test_ping_wrong_password (self):
        self.proxy = xmlrpclib.ServerProxy("https://user:wrongpassword@localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.ProtocolError:
            pass
        else:
            assert not "Allowed unauthorized access."
        


class TestXMLRPCServer_https (XMLRPCServerTester):
    
    def setup (self):
        XMLRPCServerTester.setup(self)
        assert os.path.exists(keypath) and os.path.exists(certpath)
        self.server = XMLRPCServer(("localhost", 5900), keyfile=keypath, certfile=certpath, cafile=capath, register=False)
        self.server.register_instance(c)
        self.proxy = xmlrpclib.ServerProxy("https://localhost:5900")
    
    def test_secure (self):
        assert ssl.PROTOCOL_SSLv23 == self.server.ssl_protocol, self.server.ssl_protocol
    
    def test_url (self):
        hname = socket.gethostname()
        assert self.server.url == "https://%s:5900" % hname, self.server.url
