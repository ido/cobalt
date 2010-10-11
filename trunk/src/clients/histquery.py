#!/usr/bin/env python
'''Query history data. get the walltime adjusting parameter by project name, user name or combining both.'''

import sys
import time
import xmlrpclib
import socket
import optparse
from optparse import Option

import Cobalt.Logging
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

if __name__ == '__main__':
    
    if '-h' in sys.argv or '--help' in sys.argv:
        print __helpmsg__
        sys.exit(0)

    p = optparse.OptionParser()

    p.add_option(Option("-p", "--project",
        dest="project", type="string",
        help="query walltime adjusting parameter by project name"))
    p.add_option(Option("-u", "--user",
        dest="user", type="string",
        help="query walltime adjusting parameter by user name"))
    p.add_option(Option("-l", "--list",
        dest="listall", type="string",
        help="-l [project|user] list all adjusting parameter by project name or user name"))
    
    opts, args = p.parse_args()
   
    criteria = None
    if opts.project:
        project = opts.project
        criteria = "project"
        print "project=", project
    if opts.user:
        user = opts.user
        print "user=", user
        if criteria:
            criteria = "paired"
        else:
            criteria = "user"
    if opts.listall:
        criteria = opts.listall
        
    if criteria == None:
        p.print_help()
        sys.exit(0)
        
    print "criteria=", criteria
    
    try:
        histm = ComponentProxy("history-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to history manager"
        sys.exit(0)
    
    if opts.listall:
        apdict = histm.get_Ap_dict(opts.listall)
        for item in apdict.keys():
            msg = "%s:%s" % (item, apdict[item])
            print msg
        sys.exit(0)
    
    if criteria == "project":
        adjp = histm.get_Ap("project", project)
    elif criteria == "user":
        adjp = histm.get_Ap("user", user)
    elif criteria == "paired" :
        adjp = histm.get_Ap_by_keypair(user, project)
    print "Walltime Adjusting Parameter is ", adjp        