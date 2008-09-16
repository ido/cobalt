import os
import socket
import threading
import xmlrpclib

import Cobalt.Server
from Cobalt.Server import find_intended_location, XMLRPCServer
from Cobalt.Components.base import Component

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
    
    def test_secure (self):
        raise NotImplemented("This test has not been implemented.")
    
    def test_url (self):
        raise NotImplemented("This test has not been implemented.")
    
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
        self.server = XMLRPCServer(("localhost", 5900), register=False)
        self.proxy = xmlrpclib.ServerProxy("http://localhost:5900")
    
    def test_secure (self):
        assert not self.server.secure
    
    def test_url (self):
        hname = socket.gethostname()
        assert self.server.url == "http://%s:5900" % hname


class TestXMLRPCServer_http_auth (TestXMLRPCServer_http):
    
    def setup (self):
        XMLRPCServerTester.setup(self)
        self.server = XMLRPCServer(("localhost", 5900), register=False)
        self.server.require_auth = True
        self.server.credentials = dict(user="pass")
        self.proxy = xmlrpclib.ServerProxy("http://user:pass@localhost:5900")
    
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
        self.proxy = xmlrpclib.ServerProxy("http://localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.Fault:
            pass
        else:
            assert not "Allowed unauthorized access."
    
    def test_ping_unknown_user (self):
        self.proxy = xmlrpclib.ServerProxy("http://otheruser@localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.Fault:
            pass
        else:
            assert not "Allowed unauthorized access."
    
    def test_ping_wrong_password (self):
        self.proxy = xmlrpclib.ServerProxy("http://user:wrongpassword@localhost:5900")
        try:
            self.test_ping()
        except xmlrpclib.Fault:
            pass
        else:
            assert not "Allowed unauthorized access."
        


class TestXMLRPCServer_https (XMLRPCServerTester):
    
    def setup (self):
        XMLRPCServerTester.setup(self)
        assert os.path.exists("keyfile") and os.path.exists("certfile")
        self.server = XMLRPCServer(("localhost", 5900), keyfile="keyfile", certfile="certfile", register=False)
        self.proxy = xmlrpclib.ServerProxy("https://localhost:5900")
    
    def test_secure (self):
        assert self.server.secure
    
    def test_url (self):
        hname = socket.gethostname()
        assert self.server.url == "https://%s:5900" % hname
