#!/usr/bin/env python
# Copyright 2019 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""
Submit jobs to the queue manager for execution.

Usage: %prog --help
Usage: %prog [options] <executable> [<excutable options>]


version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-v','--verbose',dest='verbose',help='not used',action='store_true'
'-u','--unavailable',help='include unavailable nodes in selection',action='store_true'
'-i','--immediate',help='include only nodes that are idle',action='store_true'

Option with values:

'-t','--time',dest='time',type='string',help='Time nodes must be unreserved for',callback=cb_time
'-n','--nodecount',dest='nodes',type='int',help='set job node count',callback=cb_nodes
'-q','--queue',dest='queue',type='string',help='list of valid queues to choose from'
'--attrs',dest='attrs',type='string',help='set attributes (attr1=val1:attr2=val2:...:attrN=valN)',callback=cb_attrs
'-s','--start',dest='starttime',type='string',help='work from an anticipated start time.',callback=cb_date_no_log

"""
import logging
import time
import sys
import json
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug,  cb_nodes, cb_time, cb_attrs,  cb_gtzero
from Cobalt.client_utils import SYSMGR, SCHMGR
from Cobalt.arg_parser import ArgParse
from Cobalt.Util import compact_num_list, expand_num_list

__revision__ = '$Revision: 559 $'
__version__  = '$Version$'

def cb_date_no_log(option, opt_str, value, parser, *args):
    """
    parse date: modified from the cobalt_utils one to run silently.
    """
    try:
        _value     = value
        if args is not ():
            if _value.lower() == 'now':
                allow_now = args[0]
                if not allow_now:
                    raise
                _value = client_utils.cobalt_date(time.localtime(time.time()))
        starttime = client_utils.parse_datetime(_value)
    except ValueError, exc:
        client_utils.logger.error("start time '%s. Error: %s' is invalid", value, exc)
        client_utils.logger.error("start time is expected to be in the format: YYYY_MM_DD-HH:MM")
        sys.exit(1)
    setattr(parser.values, option.dest, starttime)


def parse_options(parser, spec, opts, opt2spec, def_spec):
    """
    Will initialize the specs and then parse the command line options
    """
    opts.clear()
    for item in def_spec:
        spec[item] = def_spec[item]

    parser.parse_it() # parse the command line
    opt_count               = client_utils.get_options(spec, opts, opt2spec, parser)
    return opt_count

def tag_lists(keys, lists):
    '''combine the header and options list'''
    # We only get one header entry, however it comes back as a list of headers
    # due to interface quirk
    better_keys = [key.lower() for key in keys[0]]
    return [dict(zip(better_keys, l)) for l in lists]


def node_avail(incl_unavail, node, field):
    return incl_unavail or  node[field] not in ['down']

def node_ready(immediate, node, field):
    return not immediate or node[field] in ['idle']

def node_in_queues(impl, queues, node):
    if not queues:
        return True
    if impl == "cluster_system":
        return set(queues) & set(node['queue'].split(":"))
    else:
        return set(queues) & set(node['queues'])

def node_not_reserved(res_nodes, current_time, expect_time, node, host_key):
    return not (node[host_key] in res_nodes)

def time_in_res(res_start, duration, check_time_start, check_duration):
    '''get if a time falls in a reservation'''
    res_end = res_start + duration
    check_time_end = check_time_start + check_duration
    start_in_res = (res_start <= check_time_start) and (check_time_start <= res_end)
    end_in_res = (res_start <= check_time_end) and (check_time_end <= res_end)
    res_in_check = (res_start <= check_time_end) and (res_end >= check_time_start)
    return start_in_res or end_in_res or res_in_check

def get_existing_res_data(impl, opts, current_time):
    res_nodes = []
    expected_start_time = current_time
    if opts['start']:
        expected_start_time = opts['start']
    if opts['time']:
        res_data = client_utils.component_call(SCHMGR, False, 'get_reservations',
                ([{'start':'*', 'duration':'*', 'partitions':'*',}], ))
        for res in res_data:
            if time_in_res(int(res['start']), int(res['duration']), expected_start_time, int(opts['time']) * 60):
                if impl == "cluster_systems":
                    loc_list = res['partitions'].split(":")
                else:
                    loc_list = [str(p) for p in expand_num_list(res['partitions'])]
                for loc in loc_list:
                    if loc not in res_nodes:
                        res_nodes.append(loc)
    return res_nodes

def get_node_list(impl, opts, node_data, node_status_field, host_key):
    '''Node status field changes from platform to platform.  Get the actual nodes needed.'''
    current_time = int(time.time())
    res_nodes = get_existing_res_data(impl, opts, current_time)
    expect_time = current_time + int(opts['time']) * 60
    queues = set(opts['queue'].split(":")) if opts['queue'] else set([])
    return sorted([n for n in node_data if (node_ready(opts['immediate'], n, node_status_field) and
                                  node_avail(opts['unavailable'], n, node_status_field) and
                                  node_not_reserved(res_nodes, current_time, expect_time, n, host_key) and
                                  node_in_queues(impl, queues, n)
                                 )])

def get_reservation_location(impl, opts):
    '''given a set of constraints, get reservation data.'''
    loc_list = []
    if impl in ['cluster_system']:
        # if we have requested a forward time, get information about reservations so we don't overlap.
        node_data = tag_lists(*client_utils.cluster_display_node_info())
        nodes = get_node_list(impl, opts, node_data, 'state', 'host')
        nodect = int(opts['nodecount']) if opts['nodecount'] else len(nodes)
        if len(nodes) < nodect:
            return "Unable to match requested parameters"
    elif impl in ['alps_system']:
        #we're going to give the compact "Cray nid list" notation as you would get from cnselect.
        fetch_header = ['Node_id', 'Name', 'Queues', 'Status', 'attributes', 'drain_until']
        # Converting into and out of JSON bypasses the XML-RPC marshal step and makes this much, much faster
        # basically required on any large production XC40
        node_data = json.loads(client_utils.component_call(SYSMGR, False, 'get_nodes', (True, None, fetch_header, True))).values()
        nodes = get_node_list(impl, opts, node_data, 'status', 'node_id')
        nodect = int(opts['nodecount']) if opts['nodecount'] else len(nodes)
        if len(nodes) < nodect:
            return "Unable to match requested parameters"
        else:
            return compact_num_list([int(n['node_id']) for n in nodes[:nodect]])
    else:
        raise NotImplementedError("%s not a currently supported system type")
    return ":".join([n['host'] for n in nodes[:nodect]])


def main():
    """
    qsub main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}
    def_spec = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_nodes        , (False,) ), # return string
        ( cb_gtzero       , (False,) ), # return string
        ( cb_time         , (False, False, False) ), # no delta time, minutes, return string
        ( cb_attrs        , () ),
        ( cb_date_no_log  , (True,) ), # will also set date to "now"
        ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    def_spec['queue']          = ''

    parser    = ArgParse(opt_def, callbacks)
    parse_options(parser, spec, opts, opt2spec, def_spec)

    # Logic changes based on system type targeted.
    impl = client_utils.component_call(SYSMGR, False, 'get_implementation',())

    client_utils.logger.info("%s", get_reservation_location(impl, opts))
    return 0

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, exc:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", exc)
        sys.exit(1)
