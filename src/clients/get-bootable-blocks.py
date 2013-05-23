#!/usr/bin/env python

'''Return a space delimited list of names that a user can boot within their job.
Block names are sent to standard output in a space delimited list.

    Options:
    --size - Constrain to blocks of a particular size within the specified block
    --geometry - A geometry in the form of AxBxCxDxE.  All blocks returned will have this node geometry.

'''

import optparse
import sys
import re

from Cobalt.Proxy import ComponentProxy

geo_re = re.compile(r'^([0-9]+)x([0-9]+)x([0-9]+)x([0-9]+)x([1-2])$')

def main():

    parser = optparse.OptionParser()
    parser.add_option('--size', action='store', dest='block_size', type='int', help='Constrain blocks to a particular nodecount')
    parser.add_option('--geometry', action='store', dest='geometry', type='string', help='Constrain blocks to a particular geometry')

    opts, args = parser.parse_args()

    query_size = None
    if opts.block_size == None:
        pass
    elif opts.block_size < 0:
        print >> sys.stderr, "Invalid size: Blocks cannot have a negative nodecount"
        return 1
    elif opts.block_size > 0:
        query_size = int(opts.block_size)

    geo_list = None
    if opts.geometry != None:
        match = geo_re.match(opts.geometry)
        if match == None:
            print >> sys.stderr, "Invalid Geometry. Geometry must be in the form of AxBxCxDxE"
            return 1
        geo_list = [int(nodect) for nodect in match.groups()]

    if len(args) < 1:
        print >> sys.stderr, "Must specify a block location for search"
        return 1

    block_loc = args[0]

    idle_blocks = ComponentProxy('system', defer=False).get_idle_blocks(block_loc, query_size, geo_list)
    print "\n".join(idle_blocks)

    return 0

if __name__ == '__main__':
    retval = main()
    sys.exit(retval)
