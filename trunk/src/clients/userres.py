#!/usr/bin/env python

'''This script removes reservations'''
__revision__ = '$Id: releaseres.py 1361 2008-08-08 16:22:14Z buettner $'
__version__ = '$Version$'

import sys
import optparse
import os
import pwd
import time
import math
import xmlrpclib

from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

if __name__ == '__main__':
    p = optparse.OptionParser(usage="%prog <reservation name>", 
                              description="This program does things to reservations you are done using.  Cyclic reservations are deferred until the next time they repeat, while one time reservations are released.")
    
    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args()

    reservation_names = args
    
    try:
        scheduler = ComponentProxy("scheduler", defer=False)
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        sys.exit(1)

    # Check if reservation exists
    spec = [{'name': rname, 'users':"*", 'start':'*', 'cycle':'*', 'duration':'*'} for rname in reservation_names]
    try:
        result = scheduler.get_reservations(spec)
    except:
        print "Error communicating with scheduler"
        sys.exit(1)

    if len(result) and len(result) != len(args):
        print "Reservation subset matched" 
    elif not result:
        print "No Reservations matched"
        sys.exit(1)


    user_name = pwd.getpwuid(os.getuid())[0]
    
    for spec in result:
        if not spec['users'] or user_name not in spec['users'].split(":"):
            print "You are not a user of reservation '%s' and so cannot alter it." % spec['name']
            continue
        
        if spec['cycle']:
            start = spec['start']
            duration = spec['duration']
            cycle = float(spec['cycle'])
            now = time.time()
            periods = math.floor((now - start)/cycle)
    
            if(periods < 0):
                start += cycle
            elif(now - start) % cycle < duration:
                start += (periods + 1) * cycle
            else:
                start += (periods + 2) * cycle

            updates = {'start':start}
            try:
                scheduler.set_reservations([{'name':spec['name']}], updates, user_name)
            except:
                print "Error deferring reservation '%'" % spec['name']
                continue
            
            newstart = time.strftime("%c", time.localtime(start))
            print "Setting new start time for for reservation '%s': %s" % (spec['name'], newstart)
        else:
            try:
                scheduler.del_reservations([{'name':spec['name']}], user_name)
            except:
                print "Error releasing reservation '%s'" % spec['name']
                continue
            
            print "Releasing reservation '%s'" % spec['name']