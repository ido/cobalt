#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import math
import re
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

def _mergelist(locations):
    '''create a set of dashed-ranges from a node list'''
    uniq = []
    reg = re.compile('(\D+)(\d+)')
    [uniq.append(loc) for loc in locations if loc not in uniq]
    uniq.sort()
    retl = [[reg.match(uniq[0]).group(2)]]
    prefix = reg.match(uniq[0]).group(1)
    uniq = uniq[1:]
    while uniq:
        newnum = reg.match(uniq[0]).group(2)
        block = [item for item in retl if (int(item[0]) == int(newnum) + 1)
                 or (int(item[-1]) == int(newnum) -1)]
        if block:
            block[0].append(newnum)
            block[0].sort()
            uniq = uniq[1:]
        else:
            retl.append([newnum])
            uniq = uniq[1:]
    retnl = []
    for item in retl:
        if len(item) > 1:
            retnl.append("[%s%s-%s]" % (prefix, item[0], item[-1]))
        else:
            retnl.append("%s%s" % (prefix, item[0]))
    return ','.join(retnl)

def mergelist(location_string, cluster):
    if not cluster:
        return location_string

    locations = location_string.split(":")

    return _mergelist(locations)

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "showres %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('showres', to_syslog=False, level=20)
    try:
        scheduler = ComponentProxy("scheduler", defer=False)
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1
    cluster = False
    try:
        if "cluster" in ComponentProxy("system", defer=False).get_implementation():
            cluster = True
    except ComponentLookupError:
        print "Failed to connect to system component"
        raise SystemExit, 1

    reservations = scheduler.get_reservations([{'name':'*', 'users':'*', 'start':'*', 'duration':'*', 'partitions':'*', 'cycle': '*', 'queue': '*'}])
    output = []
    if '-l' in sys.argv:
        verbose = True
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration', 'End Time', 'Cycle Time', 'Partitions')]
    else:
        verbose = False
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration', 'Partitions')]

    for res in reservations:
        start = float(res['start'])
        duration = float(res['duration'])
        # do some crazy stuff to make reservations which cycle display the "next" start time
        if res['cycle']:
            cycle = float(res['cycle'])
            now = time.time()
            periods = math.floor((now - start)/cycle)
            # reservations can't become active until they pass the start time -- so negative periods aren't allowed
            if periods < 0:
                pass
            # if we are still inside the reservation, show when it started
            elif (now - start) % cycle < duration:
                start += periods * cycle
            # if we are in the dead time after the reservation ended, show when the next one starts
            else:
                start += (periods+1) * cycle
        
        if res['cycle']:
            cycle = float(res['cycle'])
            if cycle < (60 * 60 * 24):
                cycle = "%02d:%02d" % (cycle/3600, (cycle/60)%60)
            else:
                cycle = "%0.1f days" % (cycle / (60 * 60 * 24))
        else:
            cycle = None
        dmin = (duration/60)%60
        dhour = duration/3600
        if verbose:
            output.append((res['name'], res['queue'], res['users'], time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin),time.strftime("%c", time.localtime(start + duration)), cycle, mergelist(res['partitions'], cluster)))
        else:
            output.append((res['name'], res['queue'], res['users'], time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin), mergelist(res['partitions'], cluster)))

    output.sort( (lambda x,y: cmp( time.mktime(time.strptime(x[3], "%c")), time.mktime(time.strptime(y[3], "%c"))) ) )
    Cobalt.Util.print_tabular(header + output)
                     
