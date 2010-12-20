#!/usr/bin/env python

'''Generate a set of commands that can be used
   to restore a set of reservations in cobalt.'''

__revision__ = '$Revision: 1 $'
__version__ = '$Version$'

import sys, time
import Cobalt.Proxy, Cobalt.Exceptions


starttime_format = "%Y_%m_%d-%H:%M"

if __name__ == '__main__':

    try:
        scheduler = Cobalt.Proxy.ComponentProxy("scheduler", defer=False)
    except Cobalt.Exceptions.ComponentLookupError:
        print >> sys.stderr, "Failed to connect to scheduler."
        raise SystemExit, 1

    reservations = scheduler.get_reservations([{'name':'*', 'users':'*', 'start':'*', 'duration':'*', 'partitions':'*', 'cycle': '*', 'queue': '*', 'res_id':'*', 'cycle_id':'*'}])
    

    commands = []

    next_res_id = scheduler.get_next_res_id()
    next_cycle_id = scheduler.get_next_cycle_id()

    for res in reservations:
        

        commands.append("setres --res_id %d --force_id" % res['res_id'])
        if res['cycle_id'] != None:
            commands.append("setres --cycle_id %d --force_id" % res['cycle_id'])
                    

        command = ["setres"]
        
        command.append("-n %s" % res['name'])
        command.append("-d %s" % res['duration'])
        command.append("-q %s" % res['queue'])
        command.append("-s %s" % time.strftime(starttime_format,
                                               time.localtime(res['start'])))

        if res['cycle'] != None:
            command.append("-c %s" % res['cycle'])
        
        if res['users'] != None:
            command.append("-u %s" % res['users'])
        
        command.extend(res['partitions'].split(':'))
        
        commands.append(" ".join(command))

    commands.append ('setres --res_id %s' % next_res_id)
    commands.append ('setres --cycle_id %s' % next_cycle_id)
    
    print "\n".join(commands)
