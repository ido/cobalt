#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys
import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: partlist [--version]'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "partlist %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    try:
        sched = Cobalt.Proxy.scheduler()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1

    parts = sched.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                 'scheduled':'*', 'functional':'*', 'deps':'*'}])
    partinfo = Cobalt.Util.buildRackTopology(parts)
    # need to cascade up busy
    busy = [part['name'] for part in parts if part['state'] == 'busy']
    for part in parts:
        for pname in busy:
            if pname in partinfo[part['name']][0] + partinfo[part['name']][1] and pname != part['name']:
                part.__setitem__('state', 'blocked')

    # need to cascade up non-functional
    offline = [part['name'] for part in parts if not part['functional']]
    forced = [part for part in parts \
              if [down for down in offline \
                  if down in partinfo[part['name']][0] + partinfo[part['name']][1]]]
    [part.__setitem__('functional', False) for part in forced]
    online = [part for part in parts if part['functional'] and part['scheduled']]
    header = [['Name', 'Queue', 'State']]
    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in online]
    Cobalt.Util.printTabular(header + output)

