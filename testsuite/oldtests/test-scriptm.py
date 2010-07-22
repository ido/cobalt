#!/usr/bin/env python

'''simple interaction with the script manager for testing'''
__revision__ = '$Revision: '
__version__ = '$Version$'

import getopt, os, pwd, sys, time
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError


usehelp = "Usage:\ntest-scriptm [--version] <executable>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "test-scriptm %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f')
    except getopt.GetoptError, gerr:
        print gerr
        print usehelp
        raise SystemExit, 1
    if len(args) < 1:
        execname = "/bin/ls"
    else:
        execname = args[0]
    level = 30
    if '-d' in sys.argv:
        level = 10
    user = pwd.getpwuid(os.getuid())[0]
    Cobalt.Logging.setup_logging('scriptm', to_syslog=False, level=level)
    try:
        sm = ComponentProxy("script-manager")
    except ComponentLookupError:
        print "Failed to connect to script manager"
        raise SystemExit, 1
    
    pgs = sm.GetProcessGroup([{'tag':'process-group', 'pgid':'*', 'state':'*'}])
    print pgs


#     pgroup = sm.CreateProcessGroup({'tag':'process-group', 'user':user, 'pgid':'*', 'executable':execname, 'location':"kwakers", 'jobid':"oo" })
# 
#     print "here's pgroup id " + `pgroup[0]['pgid']`