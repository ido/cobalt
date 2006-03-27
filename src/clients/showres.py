#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'

import time
import Cobalt.Proxy, Cobalt.Logging, Cobalt.Util

if __name__ == '__main__':
    Cobalt.Logging.setup_logging('showres', to_syslog=False)
    scheduler = Cobalt.Proxy.scheduler()
    reservations = {}
    for partition in scheduler.GetPartition([{'tag':'partition', 'name':'*', 'reservations':'*'}]):
        for reservation in partition['reservations']:
            if reservations.has_key(tuple(reservation)):
                reservations[tuple(reservation)].append(partition['name'])
            else:
                reservations[tuple(reservation)] = [partition['name']]

    output = [('Reservation', 'User', 'Start', 'Duration', 'Partitions')]
    for ((name, user, start, duration), partitions) in reservations.iteritems():
        output.append((name, user, time.strftime("%c", time.localtime(start)), duration, str(partitions)))
    Cobalt.Util.print_tabular(output)
                     
