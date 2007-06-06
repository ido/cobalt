#!/usr/bin/env python

'''This command runs through a basic sequence of pm ops'''
__revision__ = '$Revision$'

import sys, time, Cobalt.Proxy, Cobalt.Logging

if __name__ == '__main__':
    level = 20
    if '-d' in sys.argv:
        level = 10
    Cobalt.Logging.setup_logging('cmd', to_syslog=False, level=0)
    pm = Cobalt.Proxy.process_manager()
    r = pm.CreateProcessGroup([{'tag':'process-group', 'pgid':'*', 'user':'desai', 'args':[],
                                'executable':'/tmp/testscript', 'size':2, 'cwd':'/tmp', 'location':'localhost',
                                'outputfile':'/tmp/test1-output', 'errorfile':'/tmp/test1-error', 'jobid': 'pmrun'}])
    pgid = r[0]['pgid']
    while True:
        r = pm.GetProcessGroup([{'tag':'process-group', 'pgid':pgid, 'state':'*'}])
        state = r[0]['state']
        if state == 'running':
            time.sleep(5)
            continue
        else:
            break
    print "process group %s has completed" % (pgid)
        
