#!/usr/bin/env python

'''Program that does not return until the job(s) specified is not
   present in the queue'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

__helpmsg__ = "Usage: cqwait [--version] [-vr] <jobid> <jobid>\n"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqwait %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    options = {'r':'quickreturn', 'v':'version', 'version':'version'}
    doptions = {}
    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)
    if len(args) == 0:
        print "\nNeed jobid\n"
        print __helpmsg__
        raise SystemExit, 1
    level = 30
    if opts['version']:
        print "cqstat %s" % __revision__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('cqstat', to_syslog = False, level = level)
    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1
    query = [{'tag':'job', 'jobid':jid} for jid in args]

    while True:
        response = cqm.GetJobs(query)
        if len(response) == 0:
            raise SystemExit, 0
        else:
            time.sleep(2)
    
