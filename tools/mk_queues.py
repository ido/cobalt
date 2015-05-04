#!/usr/bin/env python
#THIS COMMAND IS EXTREMELY DANGEROUS AND SHOULD NOT BE USED.
#THIS IS PRESENT FOR HISTORICAL PURPOSES ONLY.

'''Cobalt state upgrade helper'''
__revision__ = '$Revision: 619 $'
__version__ = '$Version$'

import sys, xmlrpclib
import Cobalt.Logging, Cobalt.Util
import getpass
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError


def get_queues(cqm_conn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*',
             'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxusernodes':'*', 'maxqueued':'*', 'maxrunning':'*',
             'adminemail':'*', 'totalnodes':'*', 'cron':'*', 'policy':'*', 'priority':'*'}]
    return cqm_conn.get_queues(info)

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cqadm %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)

    response = get_queues(cqm)

    for q in response:
        name = q.get('name')
        print "cqadm --addq %s" % name
        if q.get('users'):
            print "cqadm --setq users=%s %s" % (q.get('users'), name)
        if q.get('mintime'):
            print "cqadm --setq mintime=%s %s" % (q.get('mintime'), name)
        if q.get('maxtime'):
            print "cqadm --setq maxtime=%s %s" % (q.get('maxtime'), name)
        if q.get('maxrunning'):
            print "cqadm --setq maxrunning=%s %s" % (q.get('maxrunning'), name)
        if q.get('maxqueued'):
            print "cqadm --setq maxqueued=%s %s" % (q.get('maxqueued'), name)
        if q.get('maxusernodes'):
            print "cqadm --setq maxusernodes=%s %s" % (q.get('maxusernodes'), name)
        if q.get('totalnodes'):
            print "cqadm --setq totalnodes=%s %s" % (q.get('totalnodes'), name)
        if q.get('adminemail'):
            print "cqadm --setq adminemail=%s %s" % (q.get('adminemail'), name)
        if q.get('state'):
            print "cqadm --setq state=%s %s" % (q.get('state'), name)
        if q.get('cron'):
            print "cqadm --setq cron=%s %s" % (q.get('cron'), name)
        if q.get('policy'):
            print "cqadm --setq policy=%s %s" % (q.get('policy'), name)
        if q.get('priority'):
            print "cqadm --setq priority=%s %s" % (q.get('priority'), name)
