#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

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
    reservations = scheduler.get_reservations([{'name':'*', 'users':'*', 'start':'*', 'duration':'*', 'partitions':'*'}])
    output = []
    if '-l' in sys.argv:
        verbose = True
        header = [('Reservation', 'User', 'Start', 'Duration', 'End Time', 'Partitions')]
    else:
        verbose = False
        header = [('Reservation', 'User', 'Start', 'Duration', 'Partitions')]

    for res in reservations:
        start = float(res['start'])
        duration = float(res['duration'])
        dmin = (duration/60)%60
        dhour = duration/3600
        if verbose:
            output.append((res['name'], res['users'], time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin),time.strftime("%c", time.localtime(start + duration)), res['partitions']))
        else:
            output.append((res['name'], res['users'], time.strftime("%c", time.localtime(start)),
                           "%02d:%02d" % (dhour, dmin), res['partitions']))

    output.sort( (lambda x,y: cmp( time.mktime(time.strptime(x[2], "%c")), time.mktime(time.strptime(y[2], "%c"))) ) )
    Cobalt.Util.print_tabular(header + output)
                     
