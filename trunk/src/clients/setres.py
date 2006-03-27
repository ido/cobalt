#!/usr/bin/env python

'''Setup reservations in the scheduler'''
__revision__ = '$Id$'

import getopt, sys, time
import Cobalt.Proxy

helpmsg = '''Usage: setres -n name -s <starttime> -d <duration> -p <partition> -u <user>
starttime is in format: YYYY_MM_DD-HH:MM
duration may be in minutes or HH:MM:SS
user and name are optional'''

if __name__ == '__main__':
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 's:d:n:p:u:', [])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        [partition] = [opt[1] for opt in opts if opt[0] == '-p']
        [start] = [opt[1] for opt in opts if opt[0] == '-s']
        [duration] = [opt[1] for opt in opts if opt[0] == '-d']
    except:
        print "Must supply -s, -d, and -p options with values"
        print help
        raise SystemExit, 1
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
        dsec = sum([mults[index] * float(units[index]) for index in range(len(units))])
    (day, rtime) = start.split('-')
    (syear, smonth, sday) = [int(field) for field in day.split('_')]
    (shour, smin) = [int(field) for field in rtime.split(':')]
    starttime = time.mktime((syear, smonth, sday, shour, smin, 0, 0, 0, -1))
    print "Got starttime %s" % (time.strftime('%c', time.localtime(starttime)))
    if '-u' in sys.argv[1:]:
        user = [opt[1] for opt in opts if opt[0] == '-u'][0]
    else:
        user = ''
    if '-n' in sys.argv[1:]:
        [nameinfo] = [val for (opt, val) in opts if opt == '-n']
    else:
        nameinfo = 'system'
    spec = [{'tag':'partition', 'name':partition}]
    scheduler = Cobalt.Proxy.scheduler()
    print scheduler.AddReservation(spec, nameinfo, user, starttime, dsec)

