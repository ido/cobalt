#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

'''This command runs through a basic sequence of pm ops'''
__revision__ = '$Revision: 2030 $'

import sys, time, Cobalt.Proxy, Cobalt.Logging
import pwd
import os
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
import Cobalt.Util

if __name__ == '__main__':
    level = 20
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=0)
    user = pwd.getpwuid(os.getuid())[0]
    try:
        pm = ComponentProxy("process-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to process manager"
        sys.exit(1)

    r = pm.add_jobs([{'tag':'process-group', 'user':user, 'args':[], 'env':{}, 
                                'executable':'/tmp/testscript', 'size':700, 'cwd':'/tmp', 'location':['ANLR00'],
                                'outputfile':'/tmp/test1-output', 'errorfile':'/tmp/test1-error', 'id': '*'}])
    print "jobs : " + `len(r)`
    pgid = r[0]['id']
    while True:
        r = pm.get_jobs([{'tag':'process-group', 'id':pgid, 'state':'*'}])
        state = r[0]['state']
        if state == 'running':
            Cobalt.Util.sleep(5)
            continue
        else:
            break
    print "process group %s has completed" % (pgid)
        
