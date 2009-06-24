#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, getopt, xmlrpclib
import sets
import os

import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError


helpmsg = '''Usage: partadm.py [-a] [-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --diag=diag_name partition
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename
Must supply one of -a or -d or -l or -start or -stop or --queue'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "partadm %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'adlrs:',
                                     ['dump', 'free', 'load=', 'enable', 'disable', 'activate', 'deactivate',
                                      'queue=', 'deps=', 'xml', 'diag=', 'fail', 'unfail', 'savestate'])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print "Failed to connect to system component"
        raise SystemExit, 1

    if '-r' in sys.argv:
        partdata = system.get_partitions([{'tag':'partition', 'name':name, 'children':'*'} for name in args])
        parts = args
        
        for part in partdata:
            for child in part['children']:
                if child not in parts:
                    parts.append(child)
    else:
        parts = args
    if '-a' in sys.argv:
        func = system.add_partitions
        args = ([{'tag':'partition', 'name':partname, 'size':"*", 'functional':False,
                  'scheduled':False, 'queue':'default', 'deps':[]} for partname in parts], )
    elif '-d' in sys.argv:
        func = system.del_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts], )
    elif '--enable' in sys.argv:
        func = system.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'scheduled':True})
    elif '--disable' in sys.argv:
        func = system.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'scheduled':False})
    elif '--activate' in sys.argv:
        func = system.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'functional':True})
    elif '--deactivate' in sys.argv:
        func = system.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'functional':False})
    elif '--fail' in sys.argv:
        func = system.fail_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts], )
    elif '--unfail' in sys.argv:
        func = system.unfail_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts], )
    elif '--xml' in sys.argv:
        func = system.generate_xml
        args = tuple()
    elif '--savestate' in sys.argv:
        if not args:
            print "please specify a filename"
            sys.exit(1)
        directory = os.path.dirname(args[0])
        if not os.path.exists(directory):
            print "directory %s does not exist" % directory
            sys.exit(1)
        func = system.save
        args = (args[0],)
    elif '-l' in sys.argv:
        func = system.get_partitions
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                  'queue':'*', 'parents':'*', 'children':'*'}], )
    elif '--queue' in [opt for (opt, arg)  in opts]:
        try:
            cqm = ComponentProxy("queue-manager", defer=False)
            existing_queues = [q.get('name') for q in cqm.get_queues([ \
                {'tag':'queue', 'name':'*'}])]
        except:
            print "Error getting queues from queue_manager"
            raise SystemExit, 1
        queue = [arg for (opt, arg) in opts if opt == '--queue'][0]
        error_messages = []
        for q in queue.split(':'):
            if not q in existing_queues:
                error_messages.append('\'' + q + '\' is not an existing queue')
        if error_messages:
            for e in error_messages:
                print e
            raise SystemExit, 1
        func = system.set_partitions
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'queue':queue})
    elif '--dump' in [opt for (opt, arg) in opts]:
        func = system.get_partitions
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'functional':'*',
                  'scheduled':'*', 'queue':'*', 'deps':'*'}], )
    elif '--diag' in [opt for (opt, arg)  in opts]:
        func = system.run_diags
        test_name = [arg for (opt, arg) in opts if opt == '--diag'][0]
        args = (parts, test_name)
    else:
        print helpmsg
        raise SystemExit, 1

    try:
        parts = apply(func, args)
    except xmlrpclib.Fault, fault:
        print "Command failure", fault
    except:
        print "strange failure"

    if '-l' in sys.argv:
        # need to cascade up busy and non-functional flags
#        print "buildRackTopology sees : " + repr(parts)
#
#        partinfo = Cobalt.Util.buildRackTopology(parts)

        try:
            scheduler = ComponentProxy("scheduler", defer=False)
            reservations = scheduler.get_reservations([{'queue':"*", 'partitions':"*", 'active':True}])
        except ComponentLookupError:
            print "Failed to connect to scheduler; no reservation data available"
            reservations = []
    
        expanded_parts = {}
        for res in reservations:
            for res_part in res['partitions'].split(":"):
                for p in parts:
                    if p['name'] == res_part:
                        if expanded_parts.has_key(res['queue']):
                            expanded_parts[res['queue']].update(p['children'])
                        else:
                            expanded_parts[res['queue']] = sets.Set( p['children'] )
                        expanded_parts[res['queue']].add(p['name'])
            
        
        for res in reservations:
            for p in parts:
                if p['name'] in expanded_parts[res['queue']]:
                    p['queue'] += ":%s" % res['queue']
    
        def my_cmp(left, right):
            val = -cmp(int(left['size']), int(right['size']))
            if val == 0:
                return cmp(left['name'], right['name'])
            else:
                return val
        
        parts.sort(my_cmp)
    
        offline = [part['name'] for part in parts if not part['functional']]
        forced = [part for part in parts \
                  if [down for down in offline \
                      if down in part['children'] + part['parents']]]
        [part.__setitem__('functional', '-') for part in forced]
        data = [['Name', 'Queue', 'Size', 'Functional', 'Scheduled', 'State', 'Dependencies']]
        # FIXME find something useful to output in the 'deps' column, since the deps have vanished
        data += [[part['name'], part['queue'], part['size'], part['functional'], part['scheduled'],
                  part['state'], ','.join([])] for part in parts]
        Cobalt.Util.printTabular(data, centered=[3, 4])
    else:
        print parts
            
        
