#!/usr/bin/env python

'''Setup reservations in the scheduler'''
__revision__ = '$Id$'

import getopt, pwd, sys, time
import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: setres [-a] [-x] [-m] -n name -s <starttime> -d <duration> -p <partition> -u <user> [partion1] .. [partionN]
starttime is in format: YYYY_MM_DD-HH:MM
duration may be in minutes or HH:MM:SS
user and name are optional
-a automatically find all dependancies of the partion(s) listed'''

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print helpmsg
        raise SystemExit, 0
    scheduler = Cobalt.Proxy.scheduler()
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 's:d:mn:p:u:ax', [])
    except getopt.GetoptError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1
    try:
        partitions = [opt[1] for opt in opts if opt[0] == '-p'] + args
    except:
        if args:
            partitions = args
        else:
            print "Must supply either -p with value or partitions as arguments"
            print helpmsg
            raise SystemExit, 1
    try:
        [start] = [opt[1] for opt in opts if opt[0] == '-s']
        [duration] = [opt[1] for opt in opts if opt[0] == '-d']
    except:
        if '-m' not in sys.argv[1:]:
            print "Must supply -s and -d with values" 
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
    if '-u' in sys.argv[1:]:
        user = [opt[1] for opt in opts if opt[0] == '-u'][0]
        for usr in user.split(':'):
            try:
                pwd.getpwnam(usr)
            except KeyError:
                print "User %s does not exist" % (usr)
    else:
        user = ''
    if '-n' in sys.argv[1:]:
        [nameinfo] = [val for (opt, val) in opts if opt == '-n']
    else:
        nameinfo = 'system'
    if '-a' in sys.argv[1:] or '-x' in sys.argv[1:]:
        allparts = []
        spec = []
        rspec = []
        extra_inclusive = []
        extra_exclusive = []
        parts = scheduler.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                     'scheduled':'*', 'functional':'*', 'deps':'*'}])
        partinfo = Cobalt.Util.buildRackTopology(parts)
        try:
            for part in partitions:
                allparts.append(part)
                spec.append({'tag':'partition', 'name':part})
                if '-x' in sys.argv[1:]:
                    if '-a' in sys.argv[1:]:
                        extra_exclusive = partinfo[part][0]
                    else:
                        extra_exclusive = partinfo[part][0] + partinfo[part][1]
                if '-a' in sys.argv[1:]:
                    extra_inclusive = partinfo[part][1]
                for relative in extra_inclusive:
                    if relative not in allparts:
                        allparts.append(relative)
                        spec.append({'tag':'partition', 'name':relative})
                for relative in extra_exclusive:
                    if relative not in allparts:
                        allparts.append(relative)
                        rspec.append({'tag':'partition', 'name':relative})
        except:
            print "Invalid partition(s)"
            print helpmsg
            raise SystemExit, 1
    elif '-m' in sys.argv[1:]:
        if '-n' not in sys.argv[1:]:
            print "-m must by called with -n <reservation name>"
            raise SystemExit
        rname = [arg for (opt, arg) in opts if opt == '-n'][0]
        parts = scheduler.GetPartition([{'tag':'partition', 'reservations':'*'}])
        #(name, user, start, duration)
        d = [(r, p) for p in parts for r in p.get('reservations') if r[0] == rname]
        r = d[0][0]
        parts = [data[1] for data in d]
        tmpnam = rname + '-temp'
        if user:
            nuser = user
        else:
            nuser = r[1]
        try:
            if starttime:
                nstart = starttime
        except:
            nstart = r[2]
        try:
            if dsec:
                ndur = dsec
        except:
            ndur = r[3]
        # set reservation n2 with new args
        scheduler.AddReservation([{'tag':'partition', 'name':n} for n in parts],
                                 tmpnam, nuser, nstart, ndur)
        scheduler.DelReservation([{'tag':'partition', 'name':'*'}], rname)
        scheduler.AddReservation([{'tag':'partition', 'name':n} for n in parts],
                                 rname, nuser, nstart, ndur)
        scheduler.DelReservation([{'tag':'partition', 'name':'*'}], tmpnam)        
    else:
        spec = [{'tag':'partition', 'name':p} for p in partitions]
    try:
        print scheduler.AddReservation(spec, nameinfo, user, starttime, dsec)
        if '-x' in sys.argv[1:]:
            print scheduler.AddReservation(rspec, nameinfo, '', starttime, dsec)
    except:
        print "Couldn't contact the scheduler"
        
