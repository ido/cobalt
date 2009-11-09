#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, operator
import sets
import time
from optparse import OptionParser
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

helpmsg = '''Usage: partlist [--version]'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "partlist %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0


    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print "Failed to connect to system"
        raise SystemExit, 1

    try:
        scheduler = ComponentProxy("scheduler", defer=False)
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1

    spec = [{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', 'size':'*',
             'functional':'*', 'scheduled':'*', 'children':'*', 'backfill_time':"*", 'draining':"*"}]
    parts = system.get_partitions(spec)
    reservations = scheduler.get_reservations([{'queue':"*", 'partitions':"*", 'active':True}])

    expanded_parts = {}
    for res in reservations:
        for res_part in res['partitions'].split(":"):
            for p in parts:
                if p['name'] == res_part:
                    if expanded_parts.has_key(res['queue']):
                        expanded_parts[res['queue']].update(p['children'])
                    else:
                        expanded_parts[res['queue']] = sets.Set( p['children'] )
                    expanded_parts[res['queue']].add(p['name'])
        
    
    for res in reservations:
        for p in parts:
            if p['name'] in expanded_parts.get(res['queue'], []):
                p['queue'] += ":%s" % res['queue']

    def my_cmp(left, right):
        val = -cmp(int(left['size']), int(right['size']))
        if val == 0:
            return cmp(left['name'], right['name'])
        else:
            return val

    parts.sort(my_cmp)
    
    now = time.time()
    for part in parts:
        if part['draining'] and part['state'] == "idle":
            # remove a little extra, to make sure that users can just type the number
            # that is output by partlist to get their job to backfill
            remaining = max(0, part['backfill_time'] - now - 90)
            hours, seconds = divmod(remaining, 3600.0)
            minutes = seconds/60.0
            part['backfill'] = "%d:%0.2d" % (int(hours), int(minutes))
        else:
            part['backfill'] = "-"




    header = [['Name', 'Queue', 'State', 'Backfill']]
    #build output list, adding
    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts if part['functional'] and part['scheduled']]
    Cobalt.Util.printTabular(header + output)
