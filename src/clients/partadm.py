#!/usr/bin/env python
"""
Partadm sets partition attributes in the scheduler

Usage: partadm.py --help
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
  help='set the queues associated with the target blocks to this list of queues.'

'--rmq', action='store_true', dest='rmq', /
  help='Only valid with --queue option. If provided queue(s) will be removed from the target block association.'
'--appq', action='store_true', dest='appq', /
  help='Only valid with --queue option. If provided queue(s) will be appended to the target block association.'

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
'-i', '--list_io', action='store_true', dest='list_io', help='list information on IOBlock status'
'--add_io_block', action='store_true', dest='add_io_block', help='add an IO Block to the list of managed IO blocks'
'--del_io_block', action='store_true', dest='del_io_block', help='delete an IO Block to the list of managed IO blocks'
'--boot_io_block', action='store_true', dest='boot_io_block', help='initiate a boot of the IO Blocks as positional arguments'
'--free_io_block', action='store_true', dest='free_io_block', help='initiate a free of the IO Blocks as positional arguments'
'--set_io_autoboot', action='store_true', dest='set_io_autoboot', help='set an IO block to be automatically booted'
'--unset_io_autoboot', action='store_true', dest='unset_io_autoboot', help='stop automatically rebooting an IO block'
'--io_autoboot_start', action='store_true', dest='autoboot_start', help='enable IO Block autobooting'
'--io_autoboot_stop', action='store_true', dest='autoboot_stop', help='disable IO Block autobooting'
'--io_autoboot_status', action='store_true', dest='autoboot_status', help='get status of IO Block autobooting'

"""
import logging
import sys

from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_path

from Cobalt.arg_parser import ArgParse
from Cobalt.Exceptions import ComponentLookupError

__revision__ = '$Revision: 1981 $'
__version__  = '$Version$'

SYSMGR = client_utils.SYSMGR
SCHMGR = client_utils.SCHMGR
QUEMGR = client_utils.QUEMGR

def validate_args(parser):
    """
    Validate arguments
    """
    spec     = {} 
    opts     = {} 
    opt2spec = {}

    opt_count = client_utils.get_options(spec, opts, opt2spec, parser)

    if opt_count == 0:
        client_utils.print_usage(parser)
        sys.exit(1)

    opts_wo_args = ['list_blocks', 'xml', 'dump', 'savestate', 'boot_stop', 'boot_start', 'boot_status', 'list_io',
                    'autoboot_start', 'autoboot_stop', 'autoboot_status']

    # Make sure jobid or queue is supplied for the appropriate commands
    if parser.no_args() and not [opt for opt in spec if opt in opts_wo_args]:
        client_utils.logger.error("At least one partition must be supplied")
        sys.exit(1)

    # Check mutually exclusive options
    base_list  = ['add', 'delete', 'enable', 'disable', 'activate', 'deactivate', 'fail', 'unfail', 'xml',
                  'savestate', 'list_blocks', 'dump', 'boot_stop', 'boot_start', 'boot_status']
    list_1  = base_list + ['queue'] 
    list_2  = base_list + ['rmq','appq']
    list_3  = ['pg_list', 'blockinfo','clean_block', 'list_blocks', 'rmq','appq']
    list_4  = ['list_io', 'rmq', 'appq']
    
    mux_option_lists = [list_1, list_2, list_3, list_4]

    if opt_count > 1:
        client_utils.validate_conflicting_options(parser, mux_option_lists)

def print_block_bgq(block_dicts):
    """Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    """
    for block in block_dicts:
        header_list = []
        value_list = []

        header_list.append('Name')
        value_list.append(block['name'])

        for key, value in block.iteritems():

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
            elif key in ['midplane_list', 'parents', 'children', 
                    'passthrough_blocks', 'wiring_conflict_list', 'io_drawer_list', 'io_node_list']:
                header_list.append(key)
                value.sort()
                value_list.append(', '.join(value))
            elif key == 'name':
                pass
            else:
                header_list.append(key)
                value_list.append(value)

        client_utils.print_vertical([header_list, value_list])
    return

def print_pg_info(pg_list):
    '''Print out process group information.

    '''
    raise NotImplementedError("Coming Soon!")


def print_io_block(io_block_dicts):
    '''print detailed information on a set of IO blocks.'''
    for block in io_block_dicts:
        header_list = block.keys()
        value_list = block.values()
        client_utils.print_vertical([header_list, value_list])


def print_block_bgp(block_dicts):
    """
    Formatted printing of a list of blocks.  This expects a list of 
    dictionaries of block data, such as the output from the system component's
    get_blocks call.

    """
    for block in block_dicts:
        header_list = []
        value_list = []

        for key, value in block.iteritems():

            if key in ['node_cards','nodes']:
                if block['size'] > 32 and key == 'nodes':
                    continue
                else:
                    header_list.append(key)
                    value_list.append(' '.join([v['id'] for v in value]))
            else:
                header_list.append(key)
                value_list.append(value)

        client_utils.print_vertical([header_list, value_list])
    return

def recursive(args):
    """
    Handle Recursive option
    """
    parts = []
    comp_args = ([{'tag':'partition', 'name':name, 'children':'*'} for name in args], )
    partdata = client_utils.component_call('system', False, 'get_partitions', comp_args)
    parts    =  args

    for part in partdata:
        if 'children' not in part:
            continue
        for child in part['children']:
            if child not in parts:
                parts.append(child)
    return parts

def partition_queues(opts, parts, sys_type):
    """
    This will get the list for each partition
    """
    if sys_type == 'bgq':
        args = ([{'name':partname, 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                  'queue':'*', 'relatives':'*', 'passthrough_blocks':'*', 'node_geometry':'*'} for partname in parts], )
    if sys_type == 'bgp':
        args = ([{'name':partname, 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                  'queue':'*', 'parents':'*', 'children':'*'} for partname in parts], )
    _parts = client_utils.component_call(SYSMGR, False, 'get_partitions', args)

    queues_dict = {}
    for p in _parts:
        qs_1 = p['queue'].split(':')
        qs_2 = opts.queue.split(':')
        new_queues = [q for q in qs_1[:] if q is not '']
        for q in qs_2:
            if q in new_queues and opts.rmq != None:
                new_queues.remove(q)
            if q not in new_queues and opts.appq != None:
                new_queues.append(q)
        if len(new_queues) == 1:
            queues_dict[p['name']] = new_queues[0]
        else:
            queues_dict[p['name']] = ':'.join(new_queues)

    return queues_dict

def process_queues(opts, parts, whoami, sys_type):
    """
    This function will get the new list of queues that are associated wth given partition
    """
    if opts.rmq != None or opts.appq != None:
        part_queues = partition_queues(opts, parts, sys_type)
        _parts = []
        for p in part_queues:
            args = ([{'tag':'partition', 'name':p}],  {'queue':part_queues[p]}, whoami)
            _parts.append(client_utils.component_call(SYSMGR, False, 'set_partitions', args))
    else:
        _parts = None
        args = ([{'tag':'partition', 'name':partname} for partname in parts],  {'queue':opts.queue}, whoami)
        _parts = client_utils.component_call(SYSMGR, False, 'set_partitions', args)

    return _parts

def validate_queues(opts):
    """
    This function will valdate to see if the given queues exists
    """
    args = ([{'tag':'queue', 'name':'*'}], )
    queues = client_utils.component_call(QUEMGR, True, 'get_queues', args)
    existing_queues = [q.get('name') for q in queues]
    error_messages = []
    for queue in opts.queue.split(':'):
        if not queue in existing_queues:
            error_messages.append('\'' + queue + '\' is not an existing queue')
    if error_messages:
        for err in error_messages:
            client_utils.logger.error(err)
        sys.exit(1)

def handle_queue_option(opts, parts, whoami, sys_type):
    """
    handles queue option
    """
    validate_queues(opts)
    parts = process_queues(opts, parts, whoami, sys_type)
    return parts

def handle_mux_options(opts, parts, whoami, sys_type):
    """
    this is a messy function with lots of if elifs to handle all the mutually exclusive options
    """
    if opts.add != None:
        args = ([{'tag':'partition', 'name':partname, 'size':"*", 'functional':False,
                  'scheduled':False, 'queue':'default', 'deps':[]} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'add_partitions', args)
    elif opts.add_io_block != None:
        args = ([{'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'add_io_blocks', args)
    elif opts.del_io_block:
        args = ([{'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'del_io_blocks', args)
    elif opts.delete:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'del_partitions', args)
    elif opts.enable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'scheduled':True}, whoami)
        parts = client_utils.component_call(SYSMGR, False, 'set_partitions', args)
    elif opts.disable:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'scheduled':False}, whoami)
        parts = client_utils.component_call(SYSMGR, False, 'set_partitions', args)
    elif opts.activate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'functional':True}, whoami)
        parts = client_utils.component_call(SYSMGR, False, 'set_partitions', args)
    elif opts.deactivate:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], {'functional':False}, whoami)
        parts = client_utils.component_call(SYSMGR, False, 'set_partitions', args)
    elif opts.fail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'fail_partitions', args)
    elif opts.unfail:
        args = ([{'tag':'partition', 'name':partname} for partname in parts], whoami)
        parts = client_utils.component_call(SYSMGR, False, 'unfail_partitions', args)
    elif opts.xml:
        parts = client_utils.component_call(SYSMGR, False, 'generate_xml', ())
    elif opts.savestate:
        parts = client_utils.component_call(SYSMGR, False, 'save', (opts.savestate,))

    elif opts.list_blocks:
        if sys_type == 'bgq':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                      'queue':'*', 'relatives':'*', 'passthrough_blocks':'*', 'node_geometry':'*'}], )
        if sys_type == 'bgp':
            args = ([{'name':'*', 'size':'*', 'state':'*', 'scheduled':'*', 'functional':'*',
                      'queue':'*', 'parents':'*', 'children':'*'}], )
        parts = client_utils.component_call(SYSMGR, False, 'get_partitions', args)
    elif opts.queue:
        parts = handle_queue_option(opts, parts, whoami, sys_type)

    elif opts.dump:
        args = ([{'tag':'partition', 'name':'*', 'size':'*', 'state':'*', 'functional':'*',
                  'scheduled':'*', 'queue':'*', 'deps':'*'}], )
        parts = client_utils.component_call(SYSMGR, False, 'get_partitions', args)
    elif opts.boot_stop:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        client_utils.component_call(SYSMGR, False, 'halt_booting', (whoami,))
        client_utils.logger.info("Halting booting: halting scheduling is advised")
        sys.exit(0)
    elif opts.boot_start:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        client_utils.component_call(SYSMGR, False, 'resume_booting', (whoami,))
        client_utils.logger.info("Enabling booting")
        sys.exit(0)
    elif opts.boot_status:
        if sys_type == 'bgp':
            client_utils.logger.info("Boot control not available for BG/P systems")
            sys.exit(0)
        boot_status = client_utils.component_call(SYSMGR, False, 'booting_status', ())
        if not boot_status:
            client_utils.logger.info("Block Booting: ENABLED")
        else:
            client_utils.logger.info("Block Booting: SUSPENDED.")
        sys.exit(0)
    elif opts.boot_io_block:
        client_utils.component_call(SYSMGR, False, 'initiate_io_boot', (parts, whoami))
        client_utils.logger.info('IO Boot initiated on %s', " ".join(parts))
        sys.exit(0)

    elif opts.free_io_block:
        client_utils.component_call(SYSMGR, False, 'initiate_io_free', (parts, False, whoami))
        client_utils.logger.info('IO Free initiated on %s', " ".join(parts))
        sys.exit(0)

    elif opts.set_io_autoboot:
        client_utils.component_call(SYSMGR, False, 'set_autoreboot', (parts, whoami))
        client_utils.logger.info('Autoreboot flag set for IO Blocks: %s', " ".join(parts))
        sys.exit(0)

    elif opts.unset_io_autoboot:
        client_utils.component_call(SYSMGR, False, 'unset_autoreboot', (parts, whoami))
        client_utils.logger.info('Autoreboot flag unset for IO Blocks: %s', " ".join(parts))
        sys.exit(0)

    elif opts.autoboot_start:
        client_utils.component_call(SYSMGR, False, 'enable_io_autoreboot', ())
        client_utils.logger.warning('IO Block autoreboot enabled.')
        sys.exit(0)

    elif opts.autoboot_stop:
        client_utils.component_call(SYSMGR, False, 'disable_io_autoreboot', ())
        client_utils.logger.warning('IO Block autoreboot disabled.')
        sys.exit(0)

    elif opts.autoboot_status:
        stat = client_utils.component_call(SYSMGR, False, 'get_io_autoreboot_status', ()) 
        autoreboot_status = "ENABLED" if stat else "DISABLED"
        client_utils.logger.warning('IO Block autoreboot: %s', autoreboot_status)
        sys.exit(0)

    return parts

def handle_blockinfo_option(parts, sys_type, print_block):
    """
    function to handle the block info option
    """

    if sys_type == 'bgq':
        args = ([{'name':part,'node_card_list':'*','subblock_parent':'*',
                  'midplane_list':'*','node_list':'*', 'scheduled':'*', 
                  'funcitonal':'*','queue':'*','parents':'*','children':'*',
                  'reserved_until':'*','reserved_by':'*','used_by':'*','freeing':'*',
                  'block_type':'*','corner_node':'*', 'extents':'*', 'cleanup_pending':'*', 
                  'state':'*','size':'*','draining':'*','backfill_time':'*','wire_list':'*',
                  'wiring_conflict_list':'*', 'midplane_geometry':'*', 'node_geometry':'*',
                  'passthrough_blocks':'*', 'passthrough_midplane_list':'*', 'io_node_list':'*',
                  'current_kernel':'*', 'current_kernel_options':'*'}
                 for part in parts], )
        info = client_utils.component_call(SYSMGR, False, 'get_blocks', args)
        print_block(info)

        args = ([{'name':part, 'status':'*', 'state':'*', 'size':'*', 'io_drawer_list':'*',
            'io_node_list':'*', 'block_computes_for_reboot':'*', 'autoreboot':'*', 'current_kernel':'*', 
            'current_kernel_options':'*'} for part in parts], )

        info =  client_utils.component_call(SYSMGR, False, 'get_io_blocks', args)
        print_block(info)
        sys.exit(0)

    elif sys_type == 'bgp':
        args = ([{'name':part,'node_card_list':'*','wire_list':'*','switch_list':'*',
                  'scheduled':'*', 'funcitonal':'*','queue':'*','parents':'*',
                  'children':'*','reserved_until':'*','reserved_by':'*','used_by':'*',
                  'freeing':'*','block_type':'*','cleanup_pending':'*', 'state':'*',
                  'wiring_conflicts':'*','size':'*','draining':'*','backfill_time':'*'}
                 for part in parts], )

        info = client_utils.component_call(SYSMGR, False, 'get_partitions', args)
        print_block(info)
        sys.exit(0)

def handle_clean_block_option(parts, whoami, sys_type):
    """
    function to process the clean block option
    """
    if sys_type == 'bgp':
        client_utils.logger.info("Force clenaing not available for BG/P systems")
        sys.exit(0)

    client_utils.component_call(SCHMGR, False, 'sched_status', ())
    client_utils.component_call(SYSMGR, False, 'booting_status', ())
    for part in parts:
        client_utils.component_call(SYSMGR, False, 'set_cleaning', (part, None, whoami))
        client_utils.logger.info("Initiating cleanup on block %s" % part)
    sys.exit(0)


def handle_list_blocks_option(parts, sys_type):
    """
    function to handle the list io option
    """
    # need to cascade up busy and non-functional flags
    if sys_type == 'bgq':
        query = [{'queue':"*", 'partitions':"*", 'active':True, 'block_passthrough':'*'}]
    elif sys_type == 'bgp':
        query = [{'queue':"*", 'partitions':"*", 'active':True}]
    try:
        reservations = client_utils.component_call(SCHMGR, False, 'get_reservations', (query,), exit_on_error = False)
    except ComponentLookupError:
        client_utils.logger.error("Failed to connect to scheduler; no reservations data available")
        reservations = []

    expanded_parts = {}
    for res in reservations:
        for res_part in res['partitions'].split(":"):
            for part in parts:
                if part['name'] == res_part:
                    if expanded_parts.has_key(res['queue']):
                        if sys_type == 'bgq':
                            expanded_parts[res['queue']].update(part['relatives'])
                            if res['block_passthrough']:
                                expanded_parts[res['queue']].update(part['passthrough_blocks'])
                        elif sys_type == 'bgp':
                            expanded_parts[res['queue']].update(part['parents'])
                            expanded_parts[res['queue']].update(part['children'])
                    else:
                        if sys_type == 'bgq':
                            expanded_parts[res['queue']] = set( part['relatives'] )
                            if res['block_passthrough']:
                                expanded_parts[res['queue']].update(part['passthrough_blocks'])
                        elif sys_type == 'bgp':
                            expanded_parts[res['queue']] = set( part['parents'] )
                            expanded_parts[res['queue']].update(part['children'])
                    expanded_parts[res['queue']].add(part['name'])

    for res in reservations:
        for part in parts:
            if part['name'] in expanded_parts[res['queue']]:
                part['queue'] += ":%s" % res['queue']

    def my_cmp(left, right):
        '''Comparator for partition sorting.  Size has priority followed by names in lexical order.

        '''
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
        for part in forced:
            part.__setitem__('functional', '-')
        data = [['Name', 'Queue', 'Size', 'Geometry', 'Functional', 'Scheduled', 'State', 'Dependencies']]
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
        for part in forced:
            part.__setitem__('functional', '-')
        data = [['Name', 'Queue', 'Size', 'Functional', 'Scheduled', 'State', 'Dependencies']]
        data += [[part['name'], part['queue'], part['size'],
                  part['functional'], part['scheduled'],
                  part['state'], ','.join([])] for part in parts]
        client_utils.printTabular(data, centered=[3, 4])

def handle_list_io_option(sys_type):
    """
    handles list io option
    """
    if sys_type != 'bgq':
        client_utils.logger.error("WARNING: IO Block information only exists on BG/Q-type systems.")


    #fetch and print bulk IO Block data
    if sys_type == 'bgq':
        args = ([{'name':'*', 'size':'*', 'status':'*', 'state':'*', 'block_computes_for_reboot':'*', 'autoreboot':'*', 
            'current_kernel':'*', 'current_kernel_options':'*'}],)
        io_block_info = client_utils.component_call(SYSMGR, False, 'get_io_blocks', args)
        data = [['Name', 'Size', 'State', 'CS Status', 'BlockComputes', 'Autoreboot']]
        for io_block in io_block_info:
            data.append([io_block['name'], io_block['size'], io_block['state'], io_block['status'],
                'x' if io_block['block_computes_for_reboot'] else '-', 'x' if io_block['autoreboot'] else '-'])
        client_utils.printTabular(data, centered=[4])

def main():
    """
    partadm main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

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
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    parser = ArgParse(opt_def, callbacks)

    # Set required default values: None

    parser.parse_it() # parse the command line
    args  = parser.args
    opts  = parser.options

    whoami = client_utils.getuid()

    validate_args(parser)
    parts = []

    if parser.options.recursive:
        parts = recursive(args)
    else:
        parts = args

    parts = handle_mux_options(opts, parts, whoami, sys_type)

    # make sure parts is an a list even if it is an empty list
    if parts is None:
        parts = []

    if opts.pg_list:
        print_pg_info(None)
        sys.exit(0)

    if opts.blockinfo:
        handle_blockinfo_option(parts, sys_type, print_block)

    if opts.clean_block:
        handle_clean_block_option(parts, whoami, sys_type)

    if opts.list_blocks:
        handle_list_blocks_option(parts, sys_type)

    elif opts.boot_start or opts.boot_stop or opts.list_io:
        pass

    else:
        client_utils.logger.info(parts)

    if opts.list_io:
        handle_list_io_option(sys_type)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
