#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, operator
from optparse import OptionParser
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

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


    spec = [{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*', 'size':'*',
             'functional':True, 'scheduled':True}]
    parts = system.get_partitions(spec)

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
