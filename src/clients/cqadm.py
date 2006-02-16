#!/usr/bin/env python

'''Cobalt job administration command'''
__revision__ = '$Revision$'

import getopt, sys
import Cobalt.Logging, Cobalt.Proxy

helpmsg = 'Usage: cqadm [-d] [--hold] [--release] [--kill] [--delete] [--queue=queuename] <jobid> <jobid>'

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'd', ['hold', 'release', 'kill', 'delete', 'queue='])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1

    if len(args) == 0:
        print "At least one jobid must be supplied"
        print helpmsg
        raise SystemExit, 1

    if ('-d', '') in opts:
        debug = True
        opts.remove(('-d', ''))
        level = 10
    else:
        debug = False
        level = 30

    if len(opts) == 0:
        print "At least one command must be specified"
        print helpmsg
        raise SystemExit, 1

    if ((('--hold', '') in opts) and (('--release', '') in opts)):
        print "Only one of --hold or --release can be used at once"
        print helpmsg
        raise SystemExit, 1

    Cobalt.Logging.setup_logging('cqadm', to_syslog=False, level=level)
    spec = [{'tag':'job', 'jobid':jobid} for jobid in args]
    cqm = Cobalt.Proxy.queue_manager()
    for cmd in [item for item in ['--kill', '--delete'] if item in sys.argv]:
        if cmd == '--delete':
            cqm.DelJobs(spec, force=True)
        else:
            cqm.DelJobs(spec)
    else:
        updates = {}
        if ('--hold', '') in opts:
            updates['state'] = 'hold'
        elif ('--release', ) in opts:
            updates['state'] = 'queued'
        if '--queue' in [opt[0] for opt in opts]:
            [queue] = [opt[1] for opt in opts if '--queue' == opt[0]]
            updates['queue'] = queue
        cqm.SetJobs(spec, updates)
    print response
    
