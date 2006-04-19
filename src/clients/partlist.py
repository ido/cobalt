#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'

import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: partlist'''

if __name__ == '__main__':
    sched = Cobalt.Proxy.scheduler()
    parts = sched.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                 'scheduled':True, 'functional':'*', 'deps':'*'}])
    partinfo = Cobalt.Util.buildRackTopology(parts)
    # need to cascade up busy
    busy = [part['name'] for part in parts if part['state'] == 'busy']
    [part.__setitem__('state', 'busy*') for part in parts for pname in busy if pname in part['deps']]
    # need to cascade up non-functional
    offline = [part['name'] for part in parts if not part['functional']]
    [part.__setitem__('functional', False) for part in parts for pname in offline if pname in part['deps']]
    online = [part for part in parts if part['functional']]
    header = [['Name', 'Queue', 'State']]
    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in online]
    Cobalt.Util.printTabular(header + output)

