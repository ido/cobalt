#!/usr/bin/env python
"""
Partadm sets partition attributes in the scheduler

Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.

version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-a', action='store_true', dest='add', help='add the block to the list of managed blocks'
'-d', action='store_true', dest='delete', help='remove the block from the list of managed blocks'
'--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-l', action='store_true', dest='list_blocks', help='list all blocks and their status'

'-r', '--recursive', action='store_true', dest='recursive', /
  help='recursively add all child blocks of the specified blocks in the positional arguments'

'--queue', action='store', type='string', dest='queue', /
  help='set the queues associated with the target blocks to this list of queues'

'--activate', action='store_true', dest='activate', help='activate the block for scheduling'
'--deactivate', action='store_true', dest='deactivate', help='deactivate the block for schedulign'
'--enable', action='store_true', dest='enable', help='enable the running of jobs on the target blocks'
'--disable', action='store_true', dest='disable', help='disable the running of jobs on the target blocks'
'--fail', action='store_true', dest='fail', help='mark the block as though it failed diagnostics (deprecated)'
'--unfail', action='store_true', dest='unfail', help='clear failed diagnostics on a block (deprecated)'
'--dump', action='store_true', dest='dump', help="dump a representation of the system's block state"

'--xml', action='store_true', dest='xml', /
  help="dump a xml representation of the system's blocks for simulator usage"

'--savestate', type='string', dest='savestate', /
  help="force the system component to write it's statefile", callback=cb_path

'--boot-stop', action='store_true', dest='boot_stop', help='disable booting of any jobs'
'--boot-start', action='store_true', dest='boot_start', help='enable booting of any jobs'
'--boot-status', action='store_true', dest='boot_status', help='show whether or not booting is enabled'

'-b', '--blockinfo', action='store_true', dest='blockinfo', /
  help='print the detailed state and information for all requested blocks.'

'--pg_list', action='store_true', dest='pg_list', help='not implemented yet'

'-c', '--clean_block', action='store_true', dest='clean_block', /
  help='force the block to cleanup and clear all internal reservations on that resource'

"""
import logging
import sys

from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_path

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 1981 $'
__version__  = '$Version$'

def validate_args(parser):
    """
    Validate arguments
    """
    spec     = {} 
    opts     = {} 
    opt2spec = {}
    
    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)

    if opt_count == 0:
        errmsg = 'Must supply one of -a or -d or -l or -start or -stop or --queue or -b.\n'
        errmsg += 'Adding "-r" or "--recursive" will add the children of the blocks passed in.\n'
        client_utils.logger.error(errmsg)
        sys.exit(1)

    opts_wo_args = ['list_blocks','xml','dump','savestate','boot_stop','boot_start','boot_status']

    # Make sure jobid or queue is supplied for the appropriate commands
    if parser.no_args() and not [opt for opt in spec if opt in opts_wo_args]:
        client_utils.logger.error("At least one partition must be supplied")
        sys.exit(1)

    optc = 0 # init option count
    errmsg = '' # init error msessage to empty string
    # Check mutually exclusive options
    if opt_count > 1:
        if parser.options.add         != None: 
            errmsg += ' add'
            optc += 1
        if parser.options.delete      != None: 
            errmsg += ' delete'
            optc += 1
        if parser.options.enable      != None: 
            errmsg += ' enable'
            optc += 1
        if parser.options.disable     != None: 
            errmsg += ' disable'
            optc += 1
        if parser.options.activate    != None: 
            errmsg += ' activate'
            optc += 1
        if parser.options.deactivate  != None: 
            errmsg += ' deactivate'
            optc += 1
        if parser.options.fail        != None: 
            errmsg += ' fail'
            optc += 1
        if parser.options.unfail      != None: 
            errmsg += ' unfail'
            optc += 1
        if parser.options.xml         != None: 
            errmsg += ' xml'
            optc += 1
        if parser.options.savestate   != None: 
            errmsg += ' savestate'
            optc += 1
        if parser.options.list_blocks != None: 
            errmsg += ' list_blocks'
            optc += 1
        if parser.options.queue       != None: 
            errmsg += ' queue'
            optc += 1
        if parser.options.dump        != None: 
            errmsg += ' dump'
            optc += 1
        if parser.options.boot_stop   != None: 
            errmsg += ' boot_stop'
            optc += 1
        if parser.options.boot_start  != None: 
            errmsg += ' boot_start'
            optc += 1
        if parser.options.boot_status != None: 
            errmsg += ' boot_status'
            optc += 1

    if optc > 1:
        errmsg = 'Option combinations not allowed with: %s option(s)' % errmsg[1:].replace(' ',', ')
        client_utils.logger.error(errmsg)
        sys.exit(1)

    optc = 0 # init option count
    errmsg = '' # init error msessage to empty string
    # Check more mutually exclusive options
    if opt_count > 1:
        if parser.options.pg_list     != None: 
            errmsg += ' pg_list'
            optc += 1
        if parser.options.blockinfo   != None: 
            errmsg += ' blockinfo'
            optc += 1
        if parser.options.clean_block != None: 
            errmsg += ' clean_block'
            optc += 1
        if parser.options.list_blocks != None: 
            errmsg += ' list_blocks'
            optc += 1

    if optc > 1:
        errmsg = 'Option combinations not allowed with: %s option(s)' % errmsg[1:].replace(' ',', ')
        client_utils.logger.error(errmsg)
        sys.exit(1)

def print_block_bgq(block_dicts):
    """Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    """
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

        client_utils.print_vertical([header_list,value_list])
    return

def print_pg_info(pg_list):
    raise NotImplementedError("Coming Soon!")
    return


def print_block_bgp(block_dicts):
    """
    Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    """
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

        client_utils.print_vertical([header_list,value_list])
    return

def main():
    """
    partadm main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # read the cobalt config files
    client_utils.read_config()

    # get the system info
    sysinfo  = client_utils.system_info()
    sys_type =  sysinfo[0]

    print_block = print_block_bgp
    if sys_type == 'bgq':
        print_block = print_block_bgq

    use_cwd = False
    options = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        [ cb_debug        , () ],
        [ cb_path         , (options, use_cwd) ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    # Set required default values: None

    parser.parse_it() # parse the command line
    args  = parser.args
    opts  = parser.options

    whoami = client_utils.getuid()

    validate_args(parser)

    if parser.options.recursive:
        partdata = client_utils.get_partitions([{'tag':'partition', 'name':name, 'children_list':'*'} for name in args])
        parts    =  args

        for part in partdata:
            for child in part['children']:
                if child not in parts:
                    parts.append(child)
    else:
        parts = args

    system = client_utils.client_data.system_manager(False)

    if opts.add:
        args = ([{'tag':'partition', 'name':partname, 'size':"*", 'functional':False,
                  'scheduled':False, 'queue':'default', 'deps':[]} for partname in parts])
        parts = system.add_partitions(args, whoami)
    elif opts.delete:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(system.del_partitions, args)
    elif opts.enable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'scheduled':True}, whoami)
        parts = client_utils.component_call(system.set_partitions, args)
    elif opts.disable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'scheduled':False}, whoami)
        parts = client_utils.component_call(system.set_partitions, args)
    elif opts.activate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'functional':True}, whoami)
        parts = client_utils.component_call(system.set_partitions, args)
    elif opts.deactivate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'functional':False}, whoami)
        parts = client_utils.component_call(system.set_partitions, args)
    elif opts.fail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(system.fail_partitions, args)
    elif opts.unfail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(system.unfail_partitions, args)
    elif opts.xml:
        args = tuple()
        parts = client_utils.component_call(system.generate_xml, args)
    elif opts.savestate:
        args = (opts.savestate,)
        parts = client_utils.component_call(system.save, args)

    elif opts.list_blocks:
        if sys_type == 'bgq':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                      'queue':'*', 'relatives':'*', 'passthrough_blocks':'*', 'node_geometry':'*'}], )
        if sys_type == 'bgp':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                      'queue':'*', 'parents':'*', 'children':'*'}], )
        parts = client_utils.component_call(system.get_partitions, args)
    elif opts.queue:
        existing_queues = [q.get('name') for q in client_utils.get_queues([{'tag':'queue', 'name':'*'}])]
        error_messages = []
        for q in opts.queue.split(':'):
            if not q in existing_queues:
                error_messages.append('\'' + q + '\' is not an existing queue')
        if error_messages:
            for e in error_messages:
                client_utils.logger.error(e)
            sys.exit(1)
        args = ([{'tag':'partition', 'name':partname} for partname in parts],
                {'queue':opts.queue}, whoami)
        parts = client_utils.component_call(system.set_partitions, args)
    elif opts.dump:
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'functional':'*',
                  'scheduled':'*', 'queue':'*', 'deps':'*'}], )
        parts = client_utils.component_call(system.get_partitions, args)
    elif opts.boot_stop:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        system.halt_booting(whoami)
        client_utils.logger.info("Halting booting: halting scheduling is advised")
        sys.exit(0)
    elif opts.boot_start:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        system.resume_booting(whoami)
        client_utils.logger.info("Enabling booting")
        sys.exit(0)
    elif opts.boot_status:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        boot_status = system.booting_status()
        if not boot_status:
            client_utils.logger.info("Block Booting: ENABLED")
        else:
            client_utils.logger.info("Block Booting: SUSPENDED.")
        sys.exit(0)

    if opts.pg_list:
        print_pg_info(None)
        sys.exit(0)

    if opts.blockinfo:
        if sys_type == 'bgq':
            print_block(system.get_blocks(
                    [{'name':part,'node_card_list':'*','subblock_parent':'*',
                      'midplane_list':'*','node_list':'*', 'scheduled':'*', 'funcitonal':'*',
                      'queue':'*','parents':'*','children':'*','reserved_until':'*',
                      'reserved_by':'*','used_by':'*','freeing':'*','block_type':'*',
                      'corner_node':'*', 'extents':'*', 'cleanup_pending':'*', 'state':'*',
                      'size':'*','draining':'*','backfill_time':'*','wire_list':'*',
                      'wiring_conflict_list':'*', 'midplane_geometry':'*', 'node_geometry':'*',
                      'passthrough_blocks':'*', 'passthrough_midplane_list':'*'}
                     for part in parts]))
        elif sys_type == 'bgp':
            print_block(system.get_partitions(
                    [{'name':part,'node_card_list':'*','wire_list':'*','switch_list':'*',
                      'scheduled':'*', 'funcitonal':'*','queue':'*','parents':'*',
                      'children':'*','reserved_until':'*','reserved_by':'*','used_by':'*',
                      'freeing':'*','block_type':'*','cleanup_pending':'*', 'state':'*',
                      'wiring_conflicts':'*','size':'*','draining':'*','backfill_time':'*'}
                     for part in parts]))
        sys.exit(0)

    if opts.clean_block:
        if sys_type == 'bgp':
            client_utils.logger.info("Force clenaing not available for BG/P systems")
            sys.exit(0)
        sched_enabled = client_utils.sched_status()
        boot_disabled = system.booting_status()
        #if sched_enabled or not boot_disabled:
        #    print "scheduling and booting must be disabled prior to force-cleaning blocks."
        #    print "No blocks were marked for cleaning."
        #    sys.exit(1)
        for part in parts:
            system.set_cleaning(part, None, whoami)
            client_utils.logger.info("Initiating cleanup on block %s" % part)
        sys.exit(0)

    if opts.list_blocks:
        # need to cascade up busy and non-functional flags
        if sys_type == 'bgq':
            query = [{'queue':"*",'partitions':"*", 'active':True, 'block_passthrough':'*'}]
            reservations = client_utils.get_reservations(query,False)
        elif sys_type == 'bgp':
            query = [{'queue':"*",'partitions':"*", 'active':True}]
            reservations = client_utils.get_reservations(query,False)
        if not reservations:
            client_utils.logger.error("No reservations data available")

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
            for part in parts:
                if not part['node_geometry']:
                    part['node_geometry'] = []
            data += [[part['name'], part['queue'], part['size'],
                      "x".join([str(i) for i in part['node_geometry']]),
                      part['functional'], part['scheduled'],
                      part['state'], ','.join([])] for part in parts]
            client_utils.printTabular(data, centered=[4, 5])
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
            client_utils.printTabular(data, centered=[3,4])

    elif opts.boot_start or opts.boot_stop: 
        pass
    else:
        client_utils.logger.info(parts)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
