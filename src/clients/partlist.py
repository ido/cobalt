#!/usr/bin/env python

'''Partlist displays online partitions for users'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, operator
from optparse import OptionParser
import Cobalt.Proxy, Cobalt.Util

helpmsg = '''Usage: partlist [--version]'''

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "partlist %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    parser = OptionParser(usage=helpmsg, description="Displays online partitions for users")
    parser.add_option("--hardware", dest="hardware", default=False,
                      action="store_true", 
                      help="Displays hardware (nodecard) status")
    parser.add_option("--flat", dest="flat", default=True,
                      action="store_false",
                      help="Displays partitions as flat list")
    (opts, args) = parser.parse_args()

    try:
        system = Cobalt.Proxy.system()
    except Cobalt.Proxy.CobaltComponentError:
        print "Failed to connect to system"
        raise SystemExit, 1

    if opts.hardware:
        parts = system.GetState()
        header = [['Name', 'Midplane', 'HW id', 'State', 'Queue']]
        output = [[part.get('name'), part.get('bpid'), part.get('id'),
                   part.get('state'), part.get('queue')] for part in parts]
        Cobalt.Util.printTabular(header + output)

    else:
        #display partition status
        parts = system.GetPartition([{'tag':'partition', 'name':'*', 'queue':'*',
                                      'state':'*', 'scheduled':'*',
                                      'functional':'*', 'depth':'*'}])
        somelist = []
        
        header = [['Name', 'Queue', 'State', 'Nodecards']]
        #build output list, adding
        if opts.flat:
            output = []
            for part in parts:
                name = '  '*int(part.get('depth')) + part.get('name')
                output.append([name] + [part.get(x) for x in [y.lower() for y in header[0][1:]]])
        else:
            output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts]
        Cobalt.Util.printTabular(header + output)
