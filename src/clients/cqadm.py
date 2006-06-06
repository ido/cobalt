#!/usr/bin/env python

'''Cobalt job administration command'''
__revision__ = '$Revision$'

import getopt, sys
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

helpmsg = 'Usage: cqadm [-d] [--drain] [--resume] [--hold] [--release] [--run=<location>] ' + \
          '[--kill] [--delete] [--queue=queuename] <jobid> <jobid>\n' + \
          '       cqadm [-d] [--addq --name=queuename] [--delq queuename queuename] [--getq]'

def getQueues(cqmConn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue','qname':'*'}]
    return cqmConn.GetQueues(info)

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'dj', ['drain', 'hold', 'release',
                                                          'kill', 'delete', 'queue=', 'resume', 'run=',
                                                          'addq', 'name=', 'getq', 'delq='])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1

    if len(args) == 0 and not [opt for opt in sys.argv if opt in ['--addq','--delq','--getq']]:
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

    # set the spec whether working with queues or jobs
    if [opt for opt in sys.argv if opt in ['--addq','--delq','--getq']]:
        spec = [{'tag':'queue'}]
    else:
        spec = [{'tag':'job', 'jobid':jobid} for jobid in args]

    cqm = Cobalt.Proxy.queue_manager()
    kdata = [item for item in ['--kill', '--delete'] if item in sys.argv]
    if '-j' in sys.argv:
        response = cqm.SetJobID(int(args[0]))
    elif kdata:
        for cmd in kdata:
            if cmd == '--delete':
                response = cqm.DelJobs(spec, True)
            else:
                response = cqm.DelJobs(spec)
    elif '--run' in [opt for (opt, arg) in opts]:
        [location] = [arg for (opt, arg) in opts if opt == '--run']
        response = cqm.RunJobs(spec, location.split(':'))
    elif '--drain' in sys.argv:
        cqm.Drain()
    elif '--resume' in sys.argv:
        cqm.Resume()
    elif '--addq' in sys.argv:
        if '--name' in [opt[0] for opt in opts]:
            qname = [opt[1] for opt in opts if '--name' == opt[0]][0]
            existing_queues = getQueues(cqm)
            if qname in [q.get('qname') for q in existing_queues]:
                print 'queue \'' + qname + '\' already exists'
                response = ''
            else:
                spec[0].update({'qname':qname})
                response = cqm.AddQueue(spec)
                print "Added queue", response[0]['qname']
        else:
            print 'Must specify queue name'
    elif '--getq' in sys.argv:
        response = getQueues(cqm)
        datatoprint = [('Queue', )] + [(q.get('qname'), ) for q in response]
        Cobalt.Util.print_tabular(datatoprint)
    elif '--delq' in sys.argv:
        qname = [opt[1] for opt in opts if '--delq' == opt[0]][0]
        spec[0].update({'qname':qname})
        otherqueues = [{'tag':'queue','qname':queue} for queue in args]
        response = cqm.DelQueues(spec + otherqueues)
        datatoprint = [('Queue', )] + [(q.get('qname'), ) for q in response]
        print "      Deleted Queues"
        Cobalt.Util.print_tabular(datatoprint)
        
    else:
        updates = {}
        if ('--hold', '') in opts:
            updates['state'] = 'hold'
        elif ('--release', '') in opts:
            updates['state'] = 'queued'
        if '--queue' in [opt[0] for opt in opts]:
            [queue] = [opt[1] for opt in opts if '--queue' == opt[0]]
            updates['queue'] = queue
        response = cqm.SetJobs(spec, updates)
    print response
    
