#!/usr/bin/env python

import sys
import optparse
import Cobalt
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy


if __name__ == '__main__':
    p = optparse.OptionParser(usage="%prog [-l] [--down part1 part2] [--up part1 part2]")
    
    p.add_option("--down", action="store_true", dest="down", help="mark nodes as down")
    p.add_option("--up", action="store_true", dest="up", help="mark nodes as up (even if allocated)")
    p.add_option("--queue", action="store", dest="queue", help="set queue associations")
    p.add_option("-l", action="store_true", dest="list", help="list node states")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args()
    
    try:
        system = Cobalt.Proxy.ComponentProxy("system", defer=False)
    except:
        print >> sys.stderr, "failed to connect to system component"
        sys.exit(1)

    if opt.down and opt.up:
        print >> sys.stderr, "--down and --up cannot be used together"
        sys.exit(1)

    if opt.down:
        delta = system.nodes_down(args)
        print "nodes marked down:"
        for d in delta:
            print "   %s" % d
        print
        print "unknown nodes:"
        for a in args:
            if a not in delta:
                print "   %s" % a
    
    elif opt.up:
        delta = system.nodes_up(args)
        print "nodes marked up:"
        for d in delta:
            print "   %s" % d
        print
        print "nodes that weren't in the down list:"
        for a in args:
            if a not in delta:
                print "   %s" %a
    
    elif opt.list:
        status = system.get_node_status()
        queue_data = system.get_queue_assignments()

        header = [['Host', 'Queue', 'State']]
        #build output list
        output = []
        dumb = status.keys()
        dumb.sort()
        for host_name in dumb:
            queues = []
            for q in queue_data:
                if host_name in queue_data[q]:
                    queues.append(q) 
            output.append([host_name, ":".join(queues), status[host_name]])
            
        Cobalt.Util.printTabular(header + output)

    elif opt.queue:
        data = system.set_queue_assignments(opt.queue, args)
        
        print data