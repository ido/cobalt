#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'

import sys, time
import Cobalt.Proxy, Cobalt.Logging, Cobalt.Util

if __name__ == '__main__':
    Cobalt.Logging.setup_logging('showres', to_syslog=False, level=20)
    scheduler = Cobalt.Proxy.scheduler()
    reservations = {}
    partitions = scheduler.GetPartition([{'size':'*', 'tag':'partition', 'name':'*', 'reservations':'*', 'deps':'*'}])
    npart = {}
    [npart.__setitem__(partition.get('name'), partition) for partition in partitions]
    depinfo = Cobalt.Util.buildRackTopology(partitions)
    for partition in partitions:
        for reservation in partition['reservations']:
            if reservations.has_key(tuple(reservation)):
                reservations[tuple(reservation)].append(partition['name'])
            else:
                reservations[tuple(reservation)] = [partition['name']]

    output = [('Reservation', 'User', 'Start', 'Duration', 'Partitions')]
    for ((name, user, start, duration), partitions) in reservations.iteritems():
        maxsize = max([npart[part].get('size') for part in partitions])
        toppart = [npart[part] for part in partitions if npart[part].get('size') == maxsize][0].get('name')
        if len([part for part in partitions if part in depinfo[toppart][1]]) == len(depinfo[toppart][1]):
            partitions = toppart + '*'
        dmin = (duration/60)%60
        dhour = duration/3600
        output.append((name, user, time.strftime("%c", time.localtime(start)),
                       "%02d:%02d" % (dhour, dmin), str(partitions)))
    Cobalt.Util.print_tabular(output)
                     
