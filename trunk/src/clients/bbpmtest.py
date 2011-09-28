#!/usr/bin/env python

'''This command runs through a basic sequence of pm ops'''
__revision__ = '$Revision: 1221 $'

import sys, time, Cobalt.Proxy, Cobalt.Logging
import pwd
import os
from Cobalt.Data import Data
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError, NodeAllocationError
import Cobalt.Util

if __name__ == '__main__':
    level = 20
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=0)
    user = pwd.getpwuid(os.getuid())[0]
    try:
        pm = ComponentProxy("bbsystem", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to bbsystem"
        raise SystemExit(1)
    spec = {'tag':'process-group', 'user':user, 'args':['--arg'], 'env':{"FOO":"bar"}, 
                      'executable':'/home/andrew/dev/testscript.py', 'size':700, 
                      'cwd':'/tmp', 'location':'*', 'nodes':1,
                      'outputfile':'/tmp/test1-output', 
                      'errorfile':'/tmp/test1-error', 'id': '*'}
    try:
        r = pm.create_processgroup(spec)
    except NodeAllocationError:
        print >> sys.stderr, "Failed to allocate nodes"
        raise SystemExit(1)
    print "jobs : " + `len(r)`
    pgid = r[0]['id']
    while True:
        query = {'tag':'process-group', 'id':pgid, 'state':'*'}
        r = pm.get_processgroup(query)
        state = r[0]['state']
        if state == 'finished':
            break
        else:
            Cobalt.Util.sleep(5)
    print "process group %s has completed" % (pgid)
        
