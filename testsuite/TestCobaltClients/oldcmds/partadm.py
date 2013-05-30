#!/usr/bin/env python

'''Partadm sets partition attributes in the scheduler'''
__revision__ = '$Revision: 1981 $'
__version__ = '$Version$'

import sys
import xmlrpclib
import os
import optparse
import pwd

import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

Cobalt.Util.init_cobalt_config()
get_config_option = Cobalt.Util.get_config_option

sys_type = get_config_option('bgsystem', 'bgtype')

helpmsg = '''Usage: partadm.py [-a] [-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.

'''

opt_parser = optparse.OptionParser(usage=helpmsg, 
        version=("Cobalt Version: %s" % __version__))

opt_parser.add_option("-a", action="store_true", dest="add",
        help="add the block to the list of managed blocks")
opt_parser.add_option("-d", action="store_true", dest="delete",
        help="remove the block from the list of managed blocks")
opt_parser.add_option("-l", action="store_true", dest="list_blocks",
        help="list all blocks and their status")
opt_parser.add_option("-r", "--recursive", action="store_true", dest="recursive",
        help="recursively add all child blocks of the specified blocks in the positional arguments")
opt_parser.add_option("--queue", action="store", type="string", dest="queue",
        help="set the queues associated with the target blocks to this list of queues")
opt_parser.add_option("--activate", action="store_true", dest="activate",
        help="activate the block for scheduling")
opt_parser.add_option("--deactivate", action="store_true", dest="deactivate",
        help="deactivate the block for schedulign")
opt_parser.add_option("--enable", action="store_true", dest="enable",
        help="enable the running of jobs on the target blocks")
opt_parser.add_option("--disable", action="store_true", dest="disable",
        help="disable the running of jobs on the target blocks")
opt_parser.add_option("--fail", action="store_true", dest="fail",
        help="mark the block as though it failed diagnostics (deprecated)")
opt_parser.add_option("--unfail", action="store_true", dest="unfail",
        help="clear failed diagnostics on a block (deprecated)")
opt_parser.add_option("--dump", action="store_true", dest="dump",
        help="dump a representation of the system's block state")
opt_parser.add_option("--xml", action="store_true", dest="xml",
        help="dump a xml representation of the system's blocks for simulator usage")
opt_parser.add_option("--savestate", action="store", type="string", dest="savestate",
        help="force the system component to write it's statefile")
opt_parser.add_option("--boot-stop", action="store_true", dest="boot_stop",
        help="disable booting of any jobs")
opt_parser.add_option("--boot-start", action="store_true", dest="boot_start",
        help="enable booting of any jobs")
opt_parser.add_option("--boot-status", action="store_true", dest="boot_status",
        help="show whether or not booting is enabled")
opt_parser.add_option("-b", "--blockinfo", action="store_true", dest="blockinfo",
        help="print the detailed state and information for all requested blocks.")
opt_parser.add_option("--pg_list", action="store_true", dest="pg_list",
        help="not implemented yet")
opt_parser.add_option("-c", "--clean_block", action="store_true", dest="clean_block",
        help="force the block to cleanup and clear all internal reservations on that resource")

#detect arguemnts that conflict, use this in a verification callback.
conflicting_args = {'add':['delete','fail','unfail','boot_stop','boot_start'],
                    'delete':['add','fail','unfail','boot_stop','boot_start'],
                    'list_blocks':['blockinfo'],
                    }

def component_call(func, args):
    '''Actually call a function on another component and handle XML RPC faults
    gracefully, and other faults with something other than a traceback.

    '''

    try:
        parts = apply(func, args)
    except xmlrpclib.Fault, fault:
        print "Command failure", fault
    except:
        print "Non-RPC Fault failure"
    return parts


def print_block_bgq(block_dicts):
    '''Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    '''
    for block in block_dicts:
        header_list = []
        value_list = []

        for key,value in block.iteritems():

            if key in ['passthrough_node_card_list', 'node_card_list','node_list']:
                if block['size'] >= 512 and key == 'node_card_list':
                    continue
                if block['size'] >= 128 and key == 'node_list':
                    continue
                header_list.append(key)
                value_list.append(' '.join([v['name'] for v in value]))
            elif key == 'wire_list':
                header_list.append(key)
                value.sort()
                value_list.append(' '.join([v['id'] for v in value]))
            elif key in ['midplane_list','parents', 'children', 
                    'passthrough_blocks', 'wiring_conflict_list']:
                header_list.append(key)
                value.sort()
                value_list.append(', '.join(value))
            else:
                header_list.append(key)
                value_list.append(value)

        Cobalt.Util.print_vertical([header_list,value_list])
    return

def print_pg_info(pg_list):
    raise NotImplementedError("Coming Soon!")
    return


def print_block_bgp(block_dicts):
    '''Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    '''
    for block in block_dicts:
        header_list = []
        value_list = []

        for key,value in block.iteritems():

            if key in ['node_cards','nodes']:
                if block['size'] > 32 and key == 'nodes':
                    continue
                else:
                    header_list.append(key)
                    value_list.append(' '.join([v['id'] for v in value]))
            else:
                header_list.append(key)
                value_list.append(value)

        Cobalt.Util.print_vertical([header_list,value_list])
    return


print_block = print_block_bgp

if sys_type == 'bgq':
    print_block = print_block_bgq

if __name__ == '__main__':


    try:
        opts, args  = opt_parser.parse_args() 
    except optparse.OptParseError, msg:
        print msg
        print helpmsg
        raise SystemExit, 1

    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print "Failed to connect to system component"
        raise SystemExit, 1

    whoami = pwd.getpwuid(os.getuid())[0]

    if opts.recursive:
        partdata = system.get_partitions([{'tag':'partition', 'name':name, 'children_list':'*'} for name in args])
        parts = args

        for part in partdata:
            for child in part['children']:
                if child not in parts:
                    parts.append(child)
    else:
        parts = args

    if opts.add:
        args = ([{'tag':'partition', 'name':partname, 'size':"*", 'functional':False,
            'scheduled':False, 'queue':'default', 'deps':[]} for partname in parts])
        parts = system.add_partitions(args, whoami)
    elif opts.delete:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = component_call(system.del_partitions, args)
    elif opts.enable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'scheduled':True}, whoami)
        parts = component_call(system.set_partitions, args)
    elif opts.disable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'scheduled':False}, whoami)
        parts = component_call(system.set_partitions, args)
    elif opts.activate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'functional':True}, whoami)
        parts = component_call(system.set_partitions, args)
    elif opts.deactivate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'functional':False}, whoami)
        parts = component_call(system.set_partitions, args)
    elif opts.fail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = component_call(system.fail_partitions, args)
    elif opts.unfail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = component_call(system.unfail_partitions, args)
    elif opts.xml:
        args = tuple()
        parts = component_call(system.generate_xml, args)
    elif opts.savestate:
        directory = os.path.dirname(opts.savestate)
        if not os.path.exists(directory):
            print "directory %s does not exist" % directory
            sys.exit(1)
        func = system.save
        args = (opts.savestate,)
        parts = component_call(system.save, args)

    elif opts.list_blocks:
        func = system.get_partitions
        if sys_type == 'bgq':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                'queue':'*', 'relatives':'*', 'passthrough_blocks':'*', 'node_geometry':'*'}], )
        if sys_type == 'bgp':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                'queue':'*', 'parents':'*', 'children':'*'}], )
        parts = component_call(system.get_partitions, args)
    elif opts.queue:
        try:
            cqm = ComponentProxy("queue-manager", defer=False)
            existing_queues = [q.get('name') for q in cqm.get_queues([ \
                {'tag':'queue', 'name':'*'}])]
        except:
            print "Error getting queues from queue_manager"
            raise SystemExit, 1
        error_messages = []
        for q in opts.queue.split(':'):
            if not q in existing_queues:
                error_messages.append('\'' + q + '\' is not an existing queue')
        if error_messages:
            for e in error_messages:
                print e
            raise SystemExit, 1
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'queue':opts.queue}, whoami)
        parts = component_call(system.set_partitions, args)
    elif opts.dump:
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'functional':'*',
                  'scheduled':'*', 'queue':'*', 'deps':'*'}], )
        parts = component_call(system.get_partitions, args)
    elif opts.boot_stop:
        if sys_type == 'bgp':
            print "Boot control not available for BG/P systems"
            sys.exit(0)
        system.halt_booting(whoami)
        print "Halting booting: halting scheduling is advised"
        sys.exit(0)
    elif opts.boot_start:
        if sys_type == 'bgp':
            print "Boot control not available for BG/P systems"
            sys.exit(0)
        system.resume_booting(whoami)
        print "Enabling booting"
        sys.exit(0)
    elif opts.boot_status:
        if sys_type == 'bgp':
            print "Boot control not available for BG/P systems"
            sys.exit(0)
        boot_status = system.booting_status()
        if not boot_status:
            print "Block Booting: ENABLED"
        else:
            print "Block Booting: SUSPENDED."
        sys.exit(0)

    if opts.pg_list:
        print_pg_info(None)
        sys.exit(0)

    if opts.blockinfo:
        if sys_type == 'bgq':
            print_block(system.get_blocks([{'name':part,'node_card_list':'*',
                'subblock_parent':'*','midplane_list':'*','node_list':'*', 'scheduled':'*', 'funcitonal':'*',
                'queue':'*','parents':'*','children':'*','reserved_until':'*',
                'reserved_by':'*','used_by':'*','freeing':'*','block_type':'*',
                'corner_node':'*', 'extents':'*', 'cleanup_pending':'*', 'state':'*',
                'size':'*','draining':'*','backfill_time':'*','wire_list':'*',
                'wiring_conflict_list':'*', 'midplane_geometry':'*', 'node_geometry':'*', 
                'passthrough_blocks':'*', 'passthrough_midplane_list':'*'}
                for part in parts]))
        elif sys_type == 'bgp':
            print_block(system.get_partitions([{'name':part,'node_card_list':'*',
                'wire_list':'*','switch_list':'*','scheduled':'*', 'funcitonal':'*',
                'queue':'*','parents':'*','children':'*','reserved_until':'*',
                'reserved_by':'*','used_by':'*','freeing':'*','block_type':'*',
                'cleanup_pending':'*', 'state':'*', 'wiring_conflicts':'*',
                'size':'*','draining':'*','backfill_time':'*'}
                for part in parts]))
        sys.exit(0)

    if opts.clean_block:
        if sys_type == 'bgp':
            print "Force clenaing not available for BG/P systems"
            sys.exit(0)
        sched_enabled = ComponentProxy('scheduler',defer=False).sched_status()
        boot_disabled = system.booting_status()
        #if sched_enabled or not boot_disabled:
        #    print "scheduling and booting must be disabled prior to force-cleaning blocks."
        #    print "No blocks were marked for cleaning."
        #    sys.exit(1)
        for part in parts:
            system.set_cleaning(part, None, whoami)
            print "Initiating cleanup on block %s" % part
        sys.exit(0)

    if opts.list_blocks:
        # need to cascade up busy and non-functional flags
#        print "buildRackTopology sees : " + repr(parts)
#
#        partinfo = Cobalt.Util.buildRackTopology(parts)

        try:
            scheduler = ComponentProxy("scheduler", defer=False)
            if sys_type == 'bgq':
                reservations = scheduler.get_reservations([{'queue':"*",
                    'partitions':"*", 'active':True, 'block_passthrough':'*'}])
            elif sys_type == 'bgp':
                reservations = scheduler.get_reservations([{'queue':"*",
                    'partitions':"*", 'active':True}])
        except ComponentLookupError:
            print "Failed to connect to scheduler; no reservation data available"
            reservations = []

        expanded_parts = {}
        for res in reservations:
            for res_part in res['partitions'].split(":"):
                for p in parts:
                    if p['name'] == res_part:
                        if expanded_parts.has_key(res['queue']):
                            if sys_type == 'bgq':
                                expanded_parts[res['queue']].update(p['relatives'])
                                if res['block_passthrough']:
                                    expanded_parts[res['queue']].update(p['passthrough_blocks'])
                            elif sys_type == 'bgp':
                                expanded_parts[res['queue']].update(p['parents'])
                                expanded_parts[res['queue']].update(p['children'])
                        else:
                            if sys_type == 'bgq':
                                expanded_parts[res['queue']] = set( p['relatives'] )
                                if res['block_passthrough']:
                                    expanded_parts[res['queue']].update(p['passthrough_blocks'])
                            elif sys_type == 'bgp':
                                expanded_parts[res['queue']] = set( p['parents'] )
                                expanded_parts[res['queue']].update(p['children'])
                        expanded_parts[res['queue']].add(p['name'])

        for res in reservations:
            for p in parts:
                if p['name'] in expanded_parts[res['queue']]:
                    p['queue'] += ":%s" % res['queue']

        def my_cmp(left, right):
            val = -cmp(int(left['size']), int(right['size']))
            if val == 0:
                return cmp(left['name'], right['name'])
            else:
                return val

        parts.sort(my_cmp)

        offline = [part['name'] for part in parts if not part['functional']]
        if sys_type == 'bgq':
            forced = [part for part in parts \
                  if [down for down in offline \
                      if down in part['relatives']]]
            [part.__setitem__('functional', '-') for part in forced]
            data = [['Name', 'Queue', 'Size', 'Geometry', 'Functional', 'Scheduled', 'State', 'Dependencies']]
            # FIXME find something useful to output in the 'deps' column, since the deps have vanished
            data += [[part['name'], part['queue'], part['size'],
                "x".join([str(i) for i in part['node_geometry']]),
                part['functional'], part['scheduled'],
                part['state'], ','.join([])] for part in parts]
            Cobalt.Util.printTabular(data, centered=[4, 5])
        elif sys_type == 'bgp':
            forced = [part for part in parts \
                  if [down for down in offline \
                      if (down in part['parents'] or down in part['children']) ]]
            [part.__setitem__('functional', '-') for part in forced]
            data = [['Name', 'Queue', 'Size', 'Functional', 'Scheduled', 'State', 'Dependencies']]
            # FIXME find something useful to output in the 'deps' column, since the deps have vanished
            data += [[part['name'], part['queue'], part['size'],
                part['functional'], part['scheduled'],
                part['state'], ','.join([])] for part in parts]
            Cobalt.Util.printTabular(data, centered=[3,4])

    elif opts.boot_start or opts.boot_stop: 
        pass
    else:
        print parts


