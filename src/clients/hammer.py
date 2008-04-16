#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision: 1221 $'
__version__ = '$Version$'

import sys, getopt, xmlrpclib

import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError


helpmsg = '''Usage: hammer.py [-a] [-d] component1 component2 (add or del)
hammer.py -l
Must supply one of -a, -d, or -l '''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "hammer %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'adl')
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print "Failed to connect to system component"
        raise SystemExit, 1

    if '-a' in sys.argv:
        func = system.add_failed_components
        out_line = "marking component '%s' as failed" 
    elif '-d' in sys.argv:
        func = system.del_failed_components
        out_line = "removing failed state from '%s'"
    elif '-l' in sys.argv:
        func = system.list_failed_components
        out_line = "%s"
    else:
        print helpmsg
        raise SystemExit, 1

    try:
        parts = apply(func, (args, ))
    except xmlrpclib.Fault, fault:
        print "Command failure", fault
    except:
        print "strange failure"

    for part in parts:
        print out_line % part
        
