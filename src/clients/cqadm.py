#!/usr/bin/env python

'''Cobalt job administration command'''
__revision__ = '$Revision$'

import sys, xmlrpclib
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

__helpmsg__ = 'Usage: cqadm [-d] [--hold] [--release] [--run=<location>] ' + \
              '[--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>\n' + \
              '       cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] ' + \
              '[--drainq] [--killq] [--setq property=value:property=value] <queue> <queue>'

def get_queues(cqm_conn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*',
             'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxqueued':'*', 'maxrunning':'*', 'adminemail':'*',
             'totalnodes':'*'}]
    return cqm_conn.GetQueues(info)

if __name__ == '__main__':

    options = {'getq':'getq', 'f':'force', 'd':'debug', 'hold':'hold', 'release':'release',
               'kill':'kill', 'delete':'delete', 'addq':'addq', 'delq':'delq',
               'stopq':'stopq', 'startq':'startq', 'drainq':'drainq', 'killq':'killq'}
    doptions = {'j':'setjobid', 'setjobid':'setjobid', 'queue':'queue','i':'index'
                'run':'run', 'setq':'setq', 'time':'time'}

    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)

    if len(args) == 0 and not [arg for arg in sys.argv[1:] if arg not in
                               ['getq', 'j', 'setjobid']]:
        print "At least one jobid or queue name must be supplied"
        print __helpmsg__
        raise SystemExit, 1

    if opts['debug']:
        debug = True
        level = 10
    else:
        debug = False
        level = 30

    if len(opts) == 0:
        print "At least one command must be specified"
        print __helpmsg__
        raise SystemExit, 1

    if opts['hold'] and opts['release']:
        print "Only one of --hold or --release can be used at once"
        print __helpmsg__
        raise SystemExit, 1

    Cobalt.Logging.setup_logging('cqadm', to_syslog=False, level=level)

    # set the spec whether working with queues or jobs
    if opts['addq'] or opts['delq'] or opts['getq'] or opts['setq'] or opts['startq'] or opts['stopq'] or opts['drainq'] or opts['killq']:
        spec = [{'tag':'queue', 'name':qname} for qname in args]
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
    elif opts['addq']:
        existing_queues = get_queues(cqm)
        if [qname for qname in args if qname in
            [q.get('name') for q in existing_queues]]:
            print 'queue already exists'
            response = ''
        elif len(args) < 1:
            print 'Must specify queue name'
            raise SystemExit, 1
        else:
            response = cqm.AddQueue(spec)
            datatoprint = [('Added Queues', )] + \
                          [(q.get('name'), ) for q in response]
            Cobalt.Util.print_tabular(datatoprint)
    elif opts['getq']:
        response = get_queues(cqm)
        for q in response:
            if q.get('maxtime', '*') != '*':
                q['maxtime'] = "%02d:%02d:00" % (divmod(int(q.get('maxtime')), 60))
            if q.get('mintime', '*') != '*':
                q['mintime'] = "%02d:%02d:00" % (divmod(int(q.get('mintime')), 60))
        header = [('Queue', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                   'MaxQueued', 'MaxUserNodes', 'TotalNodes',
                   'AdminEmail', 'State')]
        datatoprint = [(q.get('name', '*'), q.get('users', '*'),
                        q.get('mintime','*'), q.get('maxtime','*'),
                        q.get('maxrunning','*'),q.get('maxqueued','*'),
                        q.get('maxusernodes','*'),q.get('totalnodes','*'),
                        q.get('adminemail', '*'),q.get('state'))
                       for q in response]
        datatoprint.sort()
        Cobalt.Util.print_tabular(header + datatoprint)
    elif opts['delq']:
        response = []
        try:
            response = cqm.DelQueues(spec, opts['force'])
            datatoprint = [('Deleted Queues', )] + \
                          [(q.get('name'), ) for q in response]
            Cobalt.Util.print_tabular(datatoprint)
        except xmlrpclib.Fault, flt:
            print flt.faultString
    elif opts['setq']:
        props = [p.split('=') for p in opts['setq'].split(' ')]
        updates = {}
        for prop, val in props:
            if prop.lower() in ['maxtime', 'mintime']:
                if val.count(':') in [0, 2]:
                    t = val.split(':')
                    for i in t:
                        try:
                            dummy = int(i)
                        except:
                            print prop + ' value is not a number'
                            raise SystemExit, 1
                    if val.count(':') == 2:
                        t = val.split(':')
                        val = str(int(t[0])*60 + int(t[1]))
                    elif val.count(':') == 0:
                        pass
                else:
                    print 'Time for ' + prop + ' is not valid, must be in hh:mm:ss or mm format'
            updates.update({prop.lower():val})
        response = cqm.SetQueues(spec, updates)
    elif opts['stopq']:
        response = cqm.SetQueues(spec, {'state':'stopped'})
    elif opts['startq']:
        response = cqm.SetQueues(spec, {'state':'running'})
    elif opts['drainq']:
        response = cqm.SetQueues(spec, {'state':'draining'})
    elif opts['killq']:
        response = cqm.SetQueues(spec, {'state':'dead'})
    else:
        updates = {}
        if opts['hold']:
            updates['state'] = 'hold'
            spec[0]['state'] = 'queued'
        elif opts['release']:
            updates['state'] = 'queued'
        if opts['queue']:
            queue = opts['queue']
            updates['queue'] = queue
        if opts['index']:
            updates['index'] = opts['index']
        if opts['time']:
            updates['walltime'] = opts['time']
        try:
            response = cqm.SetJobs(spec, updates)
        except xmlrpclib.Fault, flt:
            response = []
            if flt.faultCode == 30:
                print flt.faultString
                raise SystemExit, 1
    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs")
    else:
        Cobalt.Logging.logging.debug(response)
