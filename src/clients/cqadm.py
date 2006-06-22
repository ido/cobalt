#!/usr/bin/env python

'''Cobalt job administration command'''
__revision__ = '$Revision$'

import getopt, sys
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

helpmsg = 'Usage: cqadm [-d] [--drain] [--resume] [--hold] [--release] [--run=<location>] ' + \
          '[--kill] [--delete] [--queue=queuename] <jobid> <jobid>\n' + \
          '       cqadm [-d] [--addq] [--delq] [--getq] [--setq property=value:property=value] <queue> <queue>'

def getQueues(cqmConn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue','qname':'*', 'drain':'*', 'users':'*', 'maxtime':'*'}]
    return cqmConn.GetQueues(info)

if __name__ == '__main__':

    options = {'drain':'drain', 'resume':'resume', 'getq':'getq', 'd':'debug',
               'hold':'hold', 'release':'release', 'kill':'kill', 'delete':'delete',
               'addq':'addq', 'delq':'delq'}
    doptions = {'j':'setjobid', 'setjobid':'setjobid', 'queue':'queue', 'run':'run', 'setq':'setq'}

    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options, doptions, helpmsg)

    if len(args) == 0 and not [arg for arg in sys.argv[1:] if arg not in ['drain', 'resume', 'getq', 'j', 'setjobid']]:
        print "At least one jobid or queue must be supplied"
        print helpmsg
        raise SystemExit, 1

    if opts['debug']:
        debug = True
        level = 10
    else:
        debug = False
        level = 30

    if len(opts) == 0:
        print "At least one command must be specified"
        print helpmsg
        raise SystemExit, 1

    if opts['hold'] and opts['release']:
        print "Only one of --hold or --release can be used at once"
        print helpmsg
        raise SystemExit, 1

    Cobalt.Logging.setup_logging('cqadm', to_syslog=False, level=level)

    # set the spec whether working with queues or jobs
    if opts['addq'] or opts['delq'] or opts['getq'] or opts['setq']:
        spec = [{'tag':'queue', 'qname':qname} for qname in args]
    else:
        spec = [{'tag':'job', 'jobid':jobid} for jobid in args]

    cqm = Cobalt.Proxy.queue_manager()
    kdata = [item for item in ['--kill', '--delete'] if item in sys.argv]
    if opts['setjobid']:
        response = cqm.SetJobID(int(opts['setjobid']))
    elif kdata:
        for cmd in kdata:
            if cmd == '--delete':
                response = cqm.DelJobs(spec, True)
            else:
                response = cqm.DelJobs(spec)
    elif opts['run']:
        location = opts['run']
        response = cqm.RunJobs(spec, location.split(':'))
    elif opts['drain']:
        cqm.Drain()
    elif opts['resume']:
        cqm.Resume()
    elif opts['addq']:
        existing_queues = getQueues(cqm)
        if [qname for qname in args if qname in [q.get('qname') for q in existing_queues]]:
            print 'queue \'' + qname + '\' already exists'
            response = ''
        elif len(args) < 1:
            print 'Must specify queue name'
            raise SystemExit, 1
        else:
            response = cqm.AddQueue(spec)
            print "Added queue(s)", [q.get('qname') for q in response]
    elif opts['getq']:
        response = getQueues(cqm)
        datatoprint = [('Queue', 'Users', 'MaxTime', 'Drain')] + [(q.get('qname'), ','.join(q.get('users')), q.get('maxtime'), q.get('drain')) for q in response]
        Cobalt.Util.print_tabular(datatoprint)
    elif opts['delq']:
        response = cqm.DelQueues(spec)
        datatoprint = [('Queue', )] + [(q.get('qname'), ) for q in response]
        print "      Deleted Queues"
        Cobalt.Util.print_tabular(datatoprint)
    elif opts['setq']:
        props = [p.split('=') for p in opts['setq'].split(' ')]
        updates = {}
        for prop,val in props:
            if prop == 'users':
                val = val.split(',')
            updates.update({prop:val})
        response = cqm.SetQueues(spec, updates)
    else:
        updates = {}
        if opts['hold']:
            updates['state'] = 'hold'
        elif opts['release']:
            updates['state'] = 'queued'
        if opts['queue']:
            queue = opts['queue']
            updates['queue'] = queue
        response = cqm.SetJobs(spec, updates)
    print response
