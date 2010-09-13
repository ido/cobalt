#!/usr/bin/env python

'''Cobalt state upgrade helper'''
__revision__ = '$Revision: 619 $'
__version__ = '$Version$'

import sys, xmlrpclib
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util
import getpass

def get_queues(cqm_conn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*',
             'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxusernodes':'*', 'maxqueued':'*', 'maxrunning':'*',
             'adminemail':'*', 'totalnodes':'*', 'cron':'*', 'policy':'*'}]
    return cqm_conn.GetQueues(info)

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqadm.py %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    try:
        cqm = Cobalt.Proxy.queue_manager()
    except Cobalt.Exceptions.ComponentLookupError:
        print "Failed to connect to queue manager"
        raise SystemExit, 1

    response = get_queues(cqm)

    for q in response:
        name = q.get('name')
        print "cqadm.py --addq %s" % name
        if q.get('users', '*') != '*':
            print "cqadm.py --setq users=%s %s" % (q.get('users'), name)
        if q.get('mintime', '*') != '*':
            print "cqadm.py --setq mintime=%s %s" % (q.get('mintime'), name)
        if q.get('maxtime', '*') != '*':
            print "cqadm.py --setq maxtime=%s %s" % (q.get('maxtime'), name)
        if q.get('maxrunning', '*') != '*':
            print "cqadm.py --setq maxrunning=%s %s" % (q.get('maxrunning'), name)
        if q.get('maxqueued', '*') != '*':
            print "cqadm.py --setq maxqueued=%s %s" % (q.get('maxqueued'), name)
        if q.get('maxusernodes', '*') != '*':
            print "cqadm.py --setq maxusernodes=%s %s" % (q.get('maxusernodes'), name)
        if q.get('totalnodes', '*') != '*':
            print "cqadm.py --setq totalnodes=%s %s" % (q.get('totalnodes'), name)
        if q.get('adminemail', '*') != '*':
            print "cqadm.py --setq adminemail=%s %s" % (q.get('adminemail'), name)
        if q.get('state', '*') != '*':
            print "cqadm.py --setq state=%s %s" % (q.get('state'), name)
        if q.get('cron', '*') != '*':
            print "cqadm.py --setq cron=%s %s" % (q.get('cron'), name)
        if q.get('policy', '*') != '*':
            print "cqadm.py --setq policy=%s %s" % (q.get('policy'), name)
