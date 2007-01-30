#!/usr/bin/env python

'''Setup reservations in the scheduler'''
__revision__ = '$Id: setres.py 64 2006-04-01 20:07:13Z voran $'
__version__ = '$Version$'

import getopt, sys, time, os
import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: userres -s <starttime> -d <duration> -p <partition> -u <user[:user:user...]>
starttime is in format: YYYY_MM_DD-HH:MM
duration may be in minutes or HH:MM:SS
-p partition where partition is restricted to R00 and R001
-u user where user can be a : delimited list of users is optional'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "userres %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 's:d:p:u:', [])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        [partition] = [opt[1] for opt in opts if opt[0] == '-p']
        [start] = [opt[1] for opt in opts if opt[0] == '-s']
        [duration] = [opt[1] for opt in opts if opt[0] == '-d']
    except:
        print "Must supply -s, -d, and -p with values" 
        print helpmsg
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
    if partition[0] not in ['R00', 'R001'] or len(partition) > 1:
        print "Invalid partition selection"
        print helpmsg
        raise SystemExit, 1
    user = os.getlogin()
    if '-u' in sys.argv[1:]:
        users = [opt[1] for opt in opts if opt[0] == '-u'][0]
        user += ":" + users
    nameinfo = "%s.%d" %(user[0],int(time.time() * 1000 % 10000))
    allparts = []
    scheduler = Cobalt.Proxy.scheduler()
    parts = scheduler.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                     'scheduled':'*', 'functional':'*', 'deps':'*'}])
    partinfo = Cobalt.Util.buildRackTopology(parts)
    try:
        for part in partition:
            allparts.append(part)
            for relative in partinfo[part][0] + partinfo[part][1]:
                if relative not in allparts:
                    allparts.append(relative)                
    except:
        print "Invalid partition(s)"
        print helpmsg
        raise SystemExit, 1 
    spec = [{'tag':'partition', 'name':allparts}]
    print scheduler.AddReservation(spec, nameinfo, user, starttime, dsec)


