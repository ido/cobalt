#!/usr/bin/env python

'''Cobalt queue delete'''
__revision__ = ''
__version__ = '$Version$'

import getopt, os, pwd, sys, time
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

helpmsg = "Usage:\ntest-failure [--version] [-t <overtime fraction>] [-f <failed release fraction>]"

if __name__ == '__main__':
    options = {'v':'verbose', 'd':'debug', 'version':'version', 'h':'held'}
    doptions = {'t':'overtime', 'f':'failedrelease'}
    (opts, command) = Cobalt.Util.dgetopt_long(sys.argv[1:],
                                               options, doptions, helpmsg)

    if opts['version']:
        print "test-failure %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    
    if len(sys.argv) <= 1:
        print helpmsg
        raise SystemExit, 0
    
    level = 30
    if '-d' in sys.argv:
        level = 10
    
    user = pwd.getpwuid(os.getuid())[0]
    Cobalt.Logging.setup_logging('cqdel', to_syslog=False, level=level)
    try:
        brooklyn = Cobalt.Proxy.system()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to script manager"
        raise SystemExit, 1
    
    
    if opts['overtime']:
        brooklyn.SetOvertimeFrac(opts['overtime'])
    
    if opts['failedrelease']:
        brooklyn.SetFailedReleaseFrac(opts['failedrelease'])
    

#     pgroup = sm.CreateProcessGroup({'tag':'process-group', 'user':user, 'pgid':'*', 'executable':execname, 'location':"kwakers", 'jobid':"oo" })
# 
#     print "here's pgroup id " + `pgroup[0]['pgid']`