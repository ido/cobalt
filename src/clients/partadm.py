#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision$'

import sys, getopt, types, xmlrpclib
import Cobalt.Proxy

def print_tabular(rows, centered = []):
    '''print data in tabular format'''
    for row in rows:
        for index in xrange(len(row)):
            if isinstance(row[index], types.BooleanType):
                if row[index]:
                    row[index] = 'X'
                else:
                    row[index] = ''
    total = 0
    for column in xrange(len(rows[0])):
        width = max([len(str(row[column])) for row in rows])
        for row in rows:
            if column in centered:
                row[column] = row[column].center(width)
            else:
                row[column] = str(row[column]).ljust(width)
        total += width + 2
    print '  '.join(rows[0])
    print total * '='
    for row in rows[1:]:
        print '  '.join(row)


helpmsg = '''Usage: partadm.py [-a] [-d] [-s size] part1 part2 (add or del)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --deps=dep1:dep2 part1 part2
Usage: partadm.py --free part1 part2
Usage: partadm.py --dump
Usage: partadm.py --load <filename>
Must supply one of -a or -d -start or -stop or --queue'''

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'adls:',
                                     ['dump', 'free', 'load=', 'enable', 'disable', 'activate', 'deactivate',
                                      'queue=', 'deps='])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    sched = Cobalt.Proxy.scheduler()
    if '-a' in sys.argv:
        func = sched.AddPartition
        try:
            [size] = [opt[1] for opt in opts if opt[0] == '-s']
        except:
            print "Must supply partition size with -s"
            raise SystemExit, 1
        args = ([{'tag':'partition', 'name':partname, 'size':int(size), 'functional':False,
                  'scheduled':False, 'queue':'default', 'deps':[]} for partname in args], )
    elif '-d' in sys.argv:
        func = sched.DelPartition
        args = ([{'tag':'partition', 'name':partname} for partname in args], )
    elif '--enable' in sys.argv:
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'scheduled':True})
    elif '--disable' in sys.argv:
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'scheduled':False})
    elif '--activate' in sys.argv:
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'functional':True})
    elif '--deactivate' in sys.argv:
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'functional':False})
    elif '-l' in sys.argv:
        func = sched.GetPartition
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*', 'queue':'*',
                  'deps':'*'}], )
    elif '--queue' in [opt for (opt, arg)  in opts]:
        queue = [arg for (opt, arg) in opts if opt == '--queue'][0]
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'queue':queue})
    elif '--deps' in [opt for (opt, arg) in opts]:
        deps = [arg for (opt, arg) in opts if opt == '--deps'][0]
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'deps':deps.split(':')})
    elif '--free' in [opt for (opt, arg) in opts]:
        func = sched.Set
        args = ([{'tag':'partition', 'name':partname} for partname in args], {'state':'idle'})
    elif '--dump' in [opt for (opt, arg) in opts]:
        func = sched.GetPartition
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'functional':'*',
                  'scheduled':False, 'queue':'*', 'deps':'*'}], )
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
        data = [['Name', 'Queue', 'Size', 'Functional', 'Scheduled', 'State', 'Dependencies']]
        data += [[part['name'], part['queue'], part['size'], part['functional'], part['scheduled'], part['state'], ','.join(part['deps'])] for part in parts]
        print_tabular(data, centered=[3,4])
    else:
        print parts
            
        
