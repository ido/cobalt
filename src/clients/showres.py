#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'

import sys, time
import Cobalt.Proxy, Cobalt.Logging, Cobalt.Util

if __name__ == '__main__':
    Cobalt.Logging.setup_logging('showres', to_syslog=False, level=20)
    scheduler = Cobalt.Proxy.scheduler()
    reservations = {}
    for partition in scheduler.GetPartition([{'tag':'partition', 'name':'*', 'reservations':'*'}]):
        for reservation in partition['reservations']:
            if reservations.has_key(tuple(reservation)):
                reservations[tuple(reservation)].append(partition['name'])
            else:
                reservations[tuple(reservation)] = [partition['name']]

    if '-s' in sys.argv:
        output = [('Reservation', 'User', 'Start', 'Duration', 'End Time')]
        for ((name, user, start, duration), partitions) in reservations.iteritems():
            dmin = duration/60.0
            dhour = dmin/60
            dmin = dmin - (dhour * 60)
            output.append((name, user, time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin), time.strftime("%c", time.localtime(start + duration))))
    else:
        output = [('Reservation', 'User', 'Start', 'Duration', 'Partitions')]
        for ((name, user, start, duration), partitions) in reservations.iteritems():
            dmin = duration/60.0
            dhour = dmin/60
            dmin = dmin - (dhour * 60)
            output.append((name, user, time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin), str(partitions)))
    Cobalt.Util.print_tabular(output)
                     
