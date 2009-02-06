#!/usr/bin/env python

'''Cobalt job administration command'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, xmlrpclib
import Cobalt.Logging, Cobalt.Util
import getpass
import os
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import QueueError, ComponentLookupError

__helpmsg__ = 'Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] ' + \
              '[--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>\n' + \
              '       cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] ' + \
              '[--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>\n' + \
              '       cqadm [-j <next jobid>]\n' + \
              '       cqadm [--savestate <filename>]'

def get_queues(cqm_conn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*',
             'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxusernodes':'*', 'maxqueued':'*', 'maxrunning':'*',
             'adminemail':'*', 'totalnodes':'*', 'cron':'*', 'policy':'*', 'priority':'*'}]
    try:
        ret = cqm_conn.get_queues(info)
    except:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    return ret

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqadm %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    options = {'getq':'getq', 'f':'force', 'd':'debug', 'hold':'hold',
               'release':'release', 'kill':'kill', 'delete':'delete',
               'addq':'addq', 'delq':'delq', 'stopq':'stopq',
               'startq':'startq', 'drainq':'drainq', 'killq':'killq'}
    doptions = {'j':'setjobid', 'setjobid':'setjobid', 'queue':'queue',
                'i':'index', 'policy':'policy', 'run':'run',
                'setq':'setq', 'time':'time', 'unsetq':'unsetq', 'savestate':'savestate'}

    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)

    if len(args) == 0 and not [arg for arg in sys.argv[1:] if arg not in
                               ['getq', 'j', 'setjobid', 'savestate']]:
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
    if opts['addq'] or opts['delq'] or opts['getq'] or opts['setq'] \
           or opts['startq'] or opts['stopq'] or opts['drainq'] \
           or opts['killq'] or opts['policy'] or opts['unsetq']:
        spec = [{'tag':'queue', 'name':qname} for qname in args]
    else:
        for i in range(len(args)):
            if args[i] == '*':
                continue
            try:
                args[i] = int(args[i])
            except:
                print >> sys.stderr, "jobid must be an integer"
                raise SystemExit, 1
    
        spec = [{'tag':'job', 'jobid':jobid} for jobid in args]

    try:
        cqm = ComponentProxy("queue-manager")
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
    
    kdata = [item for item in ['--kill', '--delete'] if item in sys.argv]
    if opts['setjobid']:
        try:
            response = cqm.set_jobid(int(opts['setjobid']))
        except ValueError:
            print "The new jobid must be an integer"
            raise SystemExit, 1
        except xmlrpclib.Fault, flt:
            print flt.faultString
            raise SystemExit, 1
    elif opts['savestate']:
        try:
            directory = os.path.dirname(opts['savestate'])
            if not os.path.exists(directory):
                print "directory %s does not exist" % directory
                sys.exit(1)
            response = cqm.save(opts['savestate'])
        except Exception, e:
            print e
            sys.exit(1)
        else:
            print response
    elif kdata:
        user = getpass.getuser()
        for cmd in kdata:
            if cmd == '--delete':
                response = cqm.del_jobs(spec, True, user)
            else:
                response = cqm.del_jobs(spec, user)
    elif opts['run']:
        location = opts['run']
        part_list = ComponentProxy("system").get_partitions([{'name': location}])
        if len(part_list) != 1:
            print "Error: cannot find partition named '%s'" % location
            raise SystemExit, 1
        response = cqm.run_jobs(spec, location.split(':'))
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
            response = cqm.add_queues(spec)
            datatoprint = [('Added Queues', )] + \
                          [(q.get('name'), ) for q in response]
            Cobalt.Util.print_tabular(datatoprint)
    elif opts['getq']:
        response = get_queues(cqm)
        for q in response:
            if q['maxtime'] is not None:
                q['maxtime'] = "%02d:%02d:00" % (divmod(int(q.get('maxtime')), 60))
            if q['mintime'] is not None:
                q['mintime'] = "%02d:%02d:00" % (divmod(int(q.get('mintime')), 60))
        header = [('Queue', 'Users', 'MinTime', 'MaxTime', 'MaxRunning',
                   'MaxQueued', 'MaxUserNodes', 'TotalNodes',
                   'AdminEmail', 'State', 'Cron', 'Policy', 'Priority')]
        datatoprint = [(q['name'], q['users'],
                        q['mintime'], q['maxtime'],
                        q['maxrunning'], q['maxqueued'],
                        q['maxusernodes'], q['totalnodes'],
                        q['adminemail'], q['state'],
                        q['cron'], q['policy'], q['priority'])
                       for q in response]
        datatoprint.sort()
        Cobalt.Util.print_tabular(header + datatoprint)
    elif opts['delq']:
        response = []
        try:
            response = cqm.del_queues(spec, opts['force'])
            datatoprint = [('Deleted Queues', )] + \
                          [(q.get('name'), ) for q in response]
            Cobalt.Util.print_tabular(datatoprint)
        except xmlrpclib.Fault, flt:
            print flt.faultString
    elif opts['setq']:
        props = [p.split('=') for p in opts['setq'].split(' ')]
        for p in props:
            if len(p) != 2:
                print "Improperly formatted argument to setq : %r" % p
                raise SystemExit, 1
        updates = {}
        for prop, val in props:
            if prop.lower() in ['maxtime', 'mintime']:
                if val.count(':') in [0, 2]:
                    t = val.split(':')
                    for i in t:
                        try:
                            if i != '*':
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
        try:
            response = cqm.set_queues(spec, updates)
        except xmlrpclib.Fault, flt:
            if flt.faultCode == QueueError.fault_code:
                print flt.faultString
                sys.exit(1)
    elif opts['unsetq']:
        updates = {}
        for prop in opts['unsetq'].split(' '):
            updates[prop.lower()] = None

        response = cqm.set_queues(spec, updates)
    elif opts['stopq']:
        response = cqm.set_queues(spec, {'state':'stopped'})
    elif opts['startq']:
        response = cqm.set_queues(spec, {'state':'running'})
    elif opts['drainq']:
        response = cqm.set_queues(spec, {'state':'draining'})
    elif opts['killq']:
        response = cqm.set_queues(spec, {'state':'dead'})
    elif opts['policy']:
        response = cqm.set_queues(spec, {'policy':opts['policy']})
    else:
        updates = {}
        new_q_name = None
        if opts['hold']:
            updates['system_state'] = 'hold'
            if not spec:
                print "you must specify a jobid to hold"
                raise SystemExit, 1
            copy = []
            for s in spec:
                s['system_state'] = 'ready'
                copy.append(s.copy())
#            for c in copy:
#                c['state'] = 'user hold'
#            spec += copy
        elif opts['release']:
            updates['system_state'] = 'ready'
            if not spec:
                print "you must specify a jobid to release"
                raise SystemExit, 1
            copy = []
            for s in spec:
                s['system_state'] = 'hold'
                copy.append(s.copy())
#            for c in copy:
#                c['state'] = 'user hold'
#            spec += copy
        if opts['queue']:
            new_q_name = opts['queue']
        if opts['index']:
            updates['index'] = opts['index']
        if opts['time']:
            try:
                minutes = Cobalt.Util.get_time(opts['time'])
            except Cobalt.Exceptions.TimeFormatError, e:
                print "invalid time specification: %s" % e.args[0]
                sys.exit(1)
            updates['walltime'] = str(minutes)
        try:
            response = []
            if updates:
                response = cqm.set_jobs(spec, updates)
            if new_q_name:
                response += cqm.move_jobs(spec, new_q_name)
        except xmlrpclib.Fault, flt:
            response = []
            if flt.faultCode == 30 or flt.faultCode == 42:
                print flt.faultString
                raise SystemExit, 1
            else:
                print flt.faultString
    if not response:
        Cobalt.Logging.logging.error("Failed to match any jobs or queues")
    else:
        Cobalt.Logging.logging.debug(response)
