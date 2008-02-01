#!/usr/bin/env python

import sys
import logging
import cPickle
from getopt import getopt, GetoptError

import Cobalt
from Cobalt.Components.simulator import Simulator
from Cobalt.Server import XMLRPCServer, find_intended_location
import Cobalt.Logging

def run (argv=None):
    
    if argv is None:
        argv = sys.argv
    
    try:
        (opts, arguments) = getopt(argv[1:], 'C:D:dt:f:', [])
    except GetoptError, e:
        print >> sys.stderr, e
        print >> sys.stderr, "Usage:"
        print >> sys.stderr, "%s [-t <topo>] [-f failures] [-C configfile] [-d] [-D <pidfile>]" % os.path.basename(argv[0])
        sys.exit(1)
    
    daemon = False
    pidfile = ""
    log_level = logging.INFO
    config_files = Cobalt.CONFIG_FILES
    for item in opts:
        if item[0] == "-D":
            daemon = True
            pidfile = item[1]
        elif item[0] == "-d":
            log_level = logging.DEBUG
        if item[0] == '-C':
            config_files = [item[1]]
    
    Cobalt.Logging.setup_logging('brooklyn', level=log_level)
    try:
        simulator = cPickle.load(open('/var/spool/cobalt/brooklyn'))
    except:
        print "failed to restore state, creating new simulator object"
        simulator = Simulator()
        
    try:
        simulator.configure("simulator.xml")
    except IOError:
        print >> sys.stderr, "unable to load simulator.xml from the current directory"
        return
    
    location = find_intended_location(simulator, config_files=config_files)
    server = XMLRPCServer(location, keyfile="/etc/cobalt.key", certfile="/etc/cobalt.key")
    server.register_instance(simulator)
    
    if daemon:
        server.serve_daemon(pidfile)
    else:
        try:
            server.serve_forever()
        finally:
            server.server_close()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
