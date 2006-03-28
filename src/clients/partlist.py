#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'

import Cobalt.Proxy, types

def print_tabular(rows, centered = []):
    '''print data in tabular format'''
    for row in rows:
        for index in xrange(len(row)):
            if isinstance(row[index], types.BooleanType):
                if row[index]:
                    row[index] = 'X'
                else:
                    row[index] = ''
    total = 0
    for column in xrange(len(rows[0])):
        width = max([len(str(row[column])) for row in rows])
        for row in rows:
            if column in centered:
                row[column] = row[column].center(width)
            else:
                row[column] = str(row[column]).ljust(width)
        total += width + 2
    print '  '.join(rows[0])
    print total * '='
    for row in rows[1:]:
        print '  '.join(row)

helpmsg = '''Usage: partlist'''

if __name__ == '__main__':
    sched = Cobalt.Proxy.scheduler()
    parts = sched.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', \
                                 'scheduled':True, 'functional':True}])
    header = [['Name', 'Queue', 'State']]
    output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts]
    print_tabular(header + output)

