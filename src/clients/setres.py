#!/usr/bin/env python

'''Setup reservations in the scheduler'''
__revision__ = '$Id: setres.py 1.6 05/09/16 10:18:46-05:00 desai@topaz.mcs.anl.gov $'

#from sss.ssslib import comm_lib
from sys import argv
from getopt import getopt, GetoptError
#from elementtree.ElementTree import Element, SubElement, tostring
from time import mktime, strftime, localtime
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

help = '''Usage: setres -n name -s <starttime> -d <duration> -p <partition> -u <user>
starttime is in format: YYYY_MM_DD-HH:MM
duration may be in minutes or HH:MM:SS
user and name are optional'''

if __name__ == '__main__':
    try:
        (opts, args) = getopt(argv[1:], 's:d:n:p:u:', [])
    except GetoptError, msg:
        print msg
        print help
        raise SystemExit, 1
    try:
        [partition] = [opt[1] for opt in opts if opt[0] == '-p']
        [start] = [opt[1] for opt in opts if opt[0] == '-s']
        [duration] = [opt[1] for opt in opts if opt[0] == '-d']
    except:
        print "Must supply -s, -d, and -p options with values"
        print help
        raise SystemExit, 1

    Cobalt.Logging.setup_logging('setres', to_syslog=False, level=30)

    if duration.count(':') == 0:
        dsec = int(duration) * 60
    else:
        units = duration.split(':')
        units.reverse()
        totaltime = 0
        mults = [1, 60, 3600]
        if len(units) > 3:
            print "time too large"
            raise SystemExit, 1
        dsec = int( sum([mults[index] * float(units[index]) for index in range(len(units))]) )
    (day, time) = start.split('-')
    (syear, smonth, sday) = [int(field) for field in day.split('_')]
    (shour, smin) = [int(field) for field in time.split(':')]
    starttime = mktime((syear, smonth, sday, shour, smin, 0, 0, 0, -1))
    print "Got starttime %s" % (strftime('%c', localtime(starttime)))

    resspec = {'tag':'reservation', 'start':str(starttime), 'duration':str(dsec)}
#     msg = Element('AddReservation', start=str(starttime), duration=str(dsec))
    if '-u' in argv[1:]:
        resspec.update({'user':[opt[1] for opt in opts if opt[0] == '-u'][0]})
#         msg.set('user', [opt[1] for opt in opts if opt[0] == '-u'][0])
    else:
        resspec.update({'user':''})
#         msg.set('user', '')
    if '-n' in argv[1:]:
        [nameinfo] = [val for (opt,val) in opts if opt == '-n']
        resspec.update({'name':nameinfo})
#         msg.set('name', nameinfo)
    resspec.update({'partition':partition})
#     SubElement(msg, 'Partition', name=partition)
    print resspec
#     print tostring(msg)
#     comm = comm_lib()
#     handle = comm.ClientInit('scheduler')
#     comm.SendMessage(handle, tostring(msg))
#     resp = comm.RecvMessage(handle)
#     comm.ClientClose(handle)
#     print resp

    try:
        bgsched = Cobalt.Proxy.scheduler()
        reservation = bgsched.AddReservation(resspec)
    except:
        print "Error setting reservation"
        raise SystemExit, 1

    print reservation
    
