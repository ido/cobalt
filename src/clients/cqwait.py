#!/usr/bin/env python

'''Program that does not return until the job(s) specified is not
   present in the queue'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError


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
        print "cqwait %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('cqstat', to_syslog = False, level = level)
    try:
        cqm = ComponentProxy("queue-manager")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    
    for i in range(len(args)):
        try:
            args[i] = int(args[i])
        except:
            logger.error("jobid must be an integer")
            raise SystemExit, 1
    
    query = [{'tag':'job', 'jobid':jid} for jid in args]

    while True:
        response = cqm.get_jobs(query)
        if len(response) == 0:
            raise SystemExit, 0
        else:
            time.sleep(2)
    
