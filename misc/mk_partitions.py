#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision: 849 $'
__version__ = '$Version$'

import sys, getopt, xmlrpclib
import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: partadm.py [-a] [-d] [-s size] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --deps=dep1:dep2 part1 part2
Usage: partadm.py --xdeps=dep1:dep2 part1 part2
Usage: partadm.py --free part1 part2
Usage: partadm.py --dump
Usage: partadm.py --load <filename>
Usage: partadm.py --version
Must supply one of -a or -d or -l or -start or -stop or --queue'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "partadm %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'adlrs:',
                                     ['dump', 'free', 'load=', 'enable', 'disable', 'activate', 'deactivate',
                                      'queue=', 'deps=', 'xdeps='])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        sched = Cobalt.Proxy.scheduler()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1

    func = sched.GetPartition
    args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*', 'queue':'*', 'deps':'*', 'xdeps':'*'}], )


    try:
        parts = apply(func, args)
    except xmlrpclib.Fault, fault:
        print "Command failure", fault
    except:
        print "strange failure"

    # need to cascade up busy and non-functional flags
    partinfo = Cobalt.Util.buildRackTopology(parts)
    busy = [part['name'] for part in parts if part['state'] == 'busy']
    for part in parts:
        for pname in busy:
            if pname in partinfo[part['name']][0] + partinfo[part['name']][1] and pname != part['name']:
                part.__setitem__('state', 'blocked')
    offline = [part['name'] for part in parts if not part['functional']]
    forced = [part for part in parts \
              if [down for down in offline \
                  if down in partinfo[part['name']][0] + partinfo[part['name']][1]]]
    [part.__setitem__('functional', '-') for part in forced]

    for part in parts:
        print "partadm -a %s" % part['name']
        print "partadm --queue=%s %s" % (part['queue'], part['name'])
        if part['functional'] and part['functional']!='-':
            print "partadm --activate %s" % part['name']
        if part['scheduled']:
            print "partadm --enable %s" % part['name']

        
