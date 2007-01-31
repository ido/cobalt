#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import Cobalt.Proxy, Cobalt.Logging, Cobalt.Util

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "showres %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('showres', to_syslog=False, level=20)
    try:
        scheduler = Cobalt.Proxy.scheduler()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1
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
    output = []
    if '-l' in sys.argv:
        header = [('Reservation', 'User', 'Start', 'Duration', 'End Time', 'Partitions')]
        for ((name, user, start, duration), partitions) in reservations.iteritems():
            maxsize = max([npart[part].get('size') for part in partitions])
            topparts = [npart[part] for part in partitions if npart[part].get('size') == maxsize]
            for tp in topparts:
                if len([part for part in partitions if part in depinfo[tp.get('name')][1]]) == len(depinfo[tp.get('name')][1]):
                    # remove names of parts in depinfo of tp
                    for p in partitions[:]:
                        if p in depinfo[tp.get('name')][1] or p == tp.get('name'):
                            partitions.remove(p)
                    partitions.append(tp.get('name') + '*')
#             if len([part for part in partitions if part in depinfo[toppart][1]]) == len(depinfo[toppart][1]):
#                 partitions = toppart + '*'
            dmin = (duration/60)%60
            dhour = duration/3600
            output.append((name, user, time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin),time.strftime("%c", time.localtime(start + duration)), str(' '.join(partitions))))
    else:
        header = [('Reservation', 'User', 'Start', 'Duration', 'Partitions')]
        for ((name, user, start, duration), partitions) in reservations.iteritems():
            maxsize = max([npart[part].get('size') for part in partitions])
            topparts = [npart[part] for part in partitions if npart[part].get('size') == maxsize]
            for tp in topparts:
                if len([part for part in partitions if part in depinfo[tp.get('name')][1]]) == len(depinfo[tp.get('name')][1]):
                    # remove names of parts in depinfo of tp
                    for p in partitions[:]:
                        if p in depinfo[tp.get('name')][1] or p == tp.get('name'):
                            partitions.remove(p)
                    partitions.append(tp.get('name') + '*')
            dmin = (duration/60)%60
            dhour = duration/3600
            output.append((name, user, time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin), str(' '.join(partitions))))

    output.sort( (lambda x,y: cmp( time.mktime(time.strptime(x[2], "%c")), time.mktime(time.strptime(y[2], "%c"))) ) )
    Cobalt.Util.print_tabular(header + output)
                     
