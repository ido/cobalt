#!/usr/bin/env python

'''This command runs through a basic sequence of pm ops'''
__revision__ = '$Revision$'

import sys, time, Cobalt.Proxy, Cobalt.Logging
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

if __name__ == '__main__':
    level = 20
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=0)
    try:
        pm = ComponentProxy("process-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to process manager"
        sys.exit(1)

    r = pm.add_jobs([{'tag':'process-group', 'user':'buettner', 'args':[],
                                'executable':'/tmp/testscript', 'size':700, 'cwd':'/tmp', 'location':'ANLR00',
                                'outputfile':'/tmp/test1-output', 'errorfile':'/tmp/test1-error', 'id': 13}])
    print "jobs : " + `len(r)`
    pgid = r[0]['id']
    while True:
        r = pm.get_jobs([{'tag':'process-group', 'id':pgid, 'state':'*'}])
        state = r[0]['state']
        if state == 'running':
            time.sleep(5)
            continue
        else:
            break
    print "process group %s has completed" % (pgid)
        
