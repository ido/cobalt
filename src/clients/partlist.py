#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'

import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: partlist'''

if __name__ == '__main__':
    sched = Cobalt.Proxy.scheduler()
    parts = sched.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                 'scheduled':True, 'functional':True}])

    header = [['Name', 'Queue', 'State']]

    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts]
    Cobalt.Util.print_tabular([tuple(x) for x in header + output])
