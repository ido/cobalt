#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

'''Program that does not return until the job(s) specified is not
   present in the queue'''
__revision__ = '$Revision: 2030 $'
__version__ = '$Version$'

import sys, time
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
import Cobalt.Util

__helpmsg__ = "Usage: cqwait [--version] [-vr] [--start] <jobid> <jobid>\n"

if __name__ == '__main__':
    if '--version' in sys.argv or '--help' in sys.argv or '-h' in sys.argv:
        print "cqwait %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    options = {'r':'quickreturn', 'v':'version', 'version':'version', 'start':'start'}
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
    Cobalt.Logging.setup_logging('cqwait', to_syslog = False, level = level)
    logger = Cobalt.Logging.logging.getLogger('cqwait')
    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    
    for i in range(len(args)):
        if args[i] == '*':
            continue
        try:
            args[i] = int(args[i])
        except:
            logger.error("jobid must be an integer")
            raise SystemExit, 1
    
    if opts['start']:
        query = [{'tag':'job', 'jobid':jid, 'is_active':False, 'has_completed':False} for jid in args]
    else:
        query = [{'tag':'job', 'jobid':jid} for jid in args]
    
    while True:
        response = cqm.get_jobs(query)
        if len(response) == 0:
            raise SystemExit, 0
        else:
            Cobalt.Util.sleep(2)
