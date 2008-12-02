#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, operator
import sets
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
             'functional':True, 'scheduled':True, 'children':'*'}]
    parts = system.get_partitions(spec)
    reservations = scheduler.get_reservations([{'queue':"*", 'partitions':"*", 'active':True}])

    expanded_parts = {}
    for res in reservations:
        for res_part in res['partitions'].split(":"):
            for p in parts:
                if p['name'] == res_part:
                    if expanded_parts.has_key(res['queue']):
                        for child in p['children']:
                            expanded_parts[res['queue']].add(child)
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

    header = [['Name', 'Queue', 'State']]
    #build output list, adding
    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts]
    Cobalt.Util.printTabular(header + output)
