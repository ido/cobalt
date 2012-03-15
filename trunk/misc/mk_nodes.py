#!/usr/bin/env python

#Query the cluster_system component and get a list of partition states, and
#the queues they are associated with.  Output a series of commands to stdout
#that when run, will restore the system to the state it had when this command
#was run.

#Like the other mk_* backup commands, they may work while there are running
#jobs, but they are not intended to work while jobs are running.  Wierd
#behavior may result.

import sys
import Cobalt, Cobalt.Util, Cobalt.Proxy

if __name__ == '__main__':

    try:
        system = Cobalt.Proxy.ComponentProxy("system", defer=False)
    except:
        print >> sys.stderr, "failed to connect to system component"
        sys.exit(1)

    status = system.get_node_status()
    queue_data = system.get_queue_assignments()

    #build output list
    commands = []
    nodes_to_down = []
    queues = {}

    for t in status:
        host_name = t[0]
        state = t[1]
        
        command_str = "nodeadm"
        args = []
        if state == "down":
            nodes_to_down.append(host_name)

        for q in queue_data:
            if host_name in queue_data[q]:
                if queues.has_key(host_name):
                    pass
                    queues[host_name].append(q)
                else:
                    queues[host_name] = [q]
        if queues.has_key(host_name):
            queues[host_name]  = ':'.join(queues[host_name])
 
    commands.append("echo 'Marking nodes as down.'")
    if nodes_to_down != []:
        commands.append("nodeadm --down %s" % ' '.join(nodes_to_down))

    commands.append("echo 'associating queues with nodes.'")
    if queues != {}:
        for key in queues.keys():
            commands.append ("nodeadm --queue=%s %s" %
                             (queues[key], key))

    commands.append("echo 'current node state:'")
    commands.append('nodelist')

    print "\n".join(commands)


