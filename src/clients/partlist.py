#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'

import Cobalt.Proxy

helpmsg = '''Usage: partlist'''

if __name__ == '__main__':
    sched = Cobalt.Proxy.scheduler()
    parts = sched.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                 'scheduled':True, 'functional':True}])
    for part in parts:
        print part
