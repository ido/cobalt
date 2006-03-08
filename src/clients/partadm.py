#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision$'

import sys, getopt, xmlrpclib
import Cobalt.Proxy

helpmsg = '''Usage: partadm.py [-a] [-d] [-s size] part1 part2 (add or del)
Usage: partadm.py [-enable|-disable] part1 part2 (online or offline)
Usage: partadm.py [-activate|-deactivate] part1 part2 (on or off)
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
        args = ([{'tag':'partition', 'name':partname, 'size':int(size), 'functional':False, 'scheduled':False,
                  'queue':'default', 'deps':[]} for partname in args], )
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
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'usable':'*', 'functional':'*', 'queue':'*',
                  'deps':'*'}], )
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
        for part in parts:
            print part
    else:
        print parts
            
        
