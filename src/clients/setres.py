#!/usr/bin/env python
"""
Setup reservations in the scheduler

Usage: %prog --help
Usage: %prog [options] <partition1> ... <partitionN>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-A','--project',dest='project',type='string',help='set project name for partitions in args'
'-D','--defer',dest='defer',help='defer flag. needs to be used with -m',action='store_true'
'-c','--cycletime',dest='cycle',type='string',help='set cycle time in minutes or HH:MM:SS',callback=cb_time
'-d','--duration',dest='duration',type='string',help='duration time in minutes or HH:MM:SS',callback=cb_time
'-m','--modify_res',dest='modify_res',help='modify current reservation specified in -n',action='store_true'
'-n','--name',dest='name',type='string',help='reservation name to add or modify'
'-p','--partitions',dest='partitions',type='string',help='partition(s) (now optional) part1:..:partN'
'-q','--queue',dest='queue',type='string',help='queue name'
'-s','--starttime',dest='start',type='string',help='start date time: YYYY_MM_DD-HH:MM, or now',callback=cb_date
'-u','--user',dest='users',type='string',help='user id list (user1:user2:... or "*" for all users)',callback=cb_res_users
'--debug',dest='debug',help='turn on communication debugging',callback=cb_debug


'--allow_passthrough',dest='block_passthrough',help='allow passthrough',callback=cb_passthrough
'--block_passthrough',dest='block_passthrough',help='do not allow passthrough',callback=cb_passthrough

OPTIONS TO CHANGE IDS ONLY:

'--cycle_id',dest='cycle_id',type='int',help='cycle id'
'--force_id',dest='force_id',default=False,help='force id flag (only used with --cycle_id or --res_id',action='store_true'
'--res_id',dest='res_id',type='int',help='res id'
"""
import logging
import math
import sys
import time
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_time, cb_date, cb_passthrough, cb_res_users

from Cobalt.arg_parser import ArgParse

__revision__ = '$Id: setres.py 2154 2011-05-25 00:22:56Z richp $'
__version__ = '$Version$'

SCHMGR = client_utils.SCHMGR
SYSMGR = client_utils.SYSMGR

def validate_starttime(parser):
    """
    make sure the start time plus duration is valid
    """
    _localtime = client_utils.parse_datetime(client_utils.cobalt_date(time.localtime(time.time())))
    _res_st    = parser.options.start + parser.options.duration
    if _res_st < _localtime:
        client_utils.logger.error("Start time + duration %s already in the pass", client_utils.sec_to_str(_res_st))
        sys.exit(1)

def set_res_id(parser):
    """
    set res id
    """
    if parser.options.force_id:
        client_utils.component_call(SCHMGR, False, 'force_res_id', (parser.options.res_id,))
        client_utils.logger.info("WARNING: Forcing res id to %s" % parser.options.res_id)
    else:
        client_utils.component_call(SCHMGR, False, 'set_res_id', (parser.options.res_id,))
        client_utils.logger.info("Setting res id to %s" % parser.options.res_id)

def set_cycle_id(parser):
    """
    set res id
    """
    cycle_id = parser.options.cycle_id
    if parser.options.force_id:
        client_utils.component_call(SCHMGR, False, 'force_cycle_id', (cycle_id,))
        client_utils.logger.info("WARNING: Forcing cycle id to %s" % str(cycle_id))
    else:
        client_utils.component_call(SCHMGR, False, 'set_cycle_id', (cycle_id,))
        client_utils.logger.info("Setting cycle_id to %s" % str(cycle_id))

def verify_locations(partitions):
    """
    verify that partitions are valid
    """
    for p in partitions:
        test_parts = client_utils.component_call(SYSMGR, False, 'verify_locations', (partitions,))
        if len(test_parts) != len(partitions):
            missing = [p for p in partitions if p not in test_parts]
            client_utils.logger.error("Missing partitions: %s" % (" ".join(missing)))
            sys.exit(1)

def validate_args(parser,spec,opt_count):
    """
    Validate setres arguments. Will return true if we want to continue processing options.
    """
    if parser.options.partitions != None:
        parser.args += [part for part in parser.options.partitions.split(':')]

    if parser.options.cycle_id != None or parser.options.res_id != None:
        only_id_change = True
        if not parser.no_args() or (opt_count != 0):
            client_utils.logger.error('No partition arguments or other options allowed with id change options')
            sys.exit(1)
    else:
        only_id_change = False

    if parser.options.force_id and not only_id_change:
        client_utils.logger.error("--force_id can only be used with --cycle_id and/or --res_id.")
        sys.exit(1)

    if only_id_change:

        # make the ID change and we are done with setres
        
        if parser.options.res_id != None:
            set_res_id(parser)
        if parser.options.cycle_id != None:
            set_cycle_id(parser)

        continue_processing_options = False # quit, setres is done

    else:

        if parser.options.name is None:
            client_utils.print_usage(parser)
            sys.exit(1)

        if parser.no_args() and (parser.options.modify_res == None):
            client_utils.logger.error("Must supply either -p with value or partitions as arguments")
            sys.exit(1)

        if parser.options.start == None and parser.options.modify_res == None:
            client_utils.logger.error("Must supply a start time for the reservation with -s")
            sys.exit(1)

        if parser.options.duration == None and parser.options.modify_res == None:
            client_utils.logger.error("Must supply a duration time for the reservation with -d")
            sys.exit(1)

        if parser.options.defer != None and (parser.options.start != None or parser.options.cycle != None):
            client_utils.logger.error("Cannot use -D while changing start or cycle time")
            sys.exit(1)

        # if we have args then verify the args (partitions)
        if not parser.no_args():
            verify_locations(parser.args)

        # if we have command line arguments put them in spec
        if not parser.no_args(): spec['partitions'] = ":".join(parser.args)

        continue_processing_options = True # continue, setres is not done.

    return continue_processing_options

        
def modify_reservation(parser):
    """
    this will handle reservation modifications
    """
    query = [{'name':parser.options.name, 'start':'*', 'cycle':'*', 'duration':'*'}]
    res_list = client_utils.component_call(SCHMGR, False, 'get_reservations', (query,))
    if not res_list:
        client_utils.logger.error("cannot find reservation named '%s'" % parser.options.name)
        sys.exit(1)

    updates = {} # updates to reservation
    if parser.options.defer != None:
        res = res_list[0]

        if not res['cycle']:
            client_utils.logger.error("Cannot use -D on a non-cyclic reservation")
            sys.exit(1)

        start    = res['start']
        duration = res['duration']
        cycle    = float(res['cycle'])
        now      = time.time()
        periods  = math.floor((now - start)/cycle)

        if(periods < 0):
            start += cycle
        elif(now - start) % cycle < duration:
            start += (periods + 1) * cycle
        else:
            start += (periods + 2) * cycle

        newstart = time.strftime("%c", time.localtime(start))
        client_utils.logger.info("Setting new start time for for reservation '%s': %s" % (res['name'], newstart))

        updates['start'] = start

        #add a field to updates to indicate we're deferring:
        updates['defer'] = True
    else:
        if parser.options.start != None:
            updates['start'] = parser.options.start
        if parser.options.duration != None:
            updates['duration'] = parser.options.duration

    if parser.options.users != None:
        updates['users'] = None if parser.options.users == "*" else parser.options.users
    if parser.options.project != None:
        updates['project'] = parser.options.project
    if parser.options.cycle != None:
        updates['cycle'] = parser.options.cycle
    if not parser.no_args():
        updates['partitions'] = ":".join(parser.args)
    if parser.options.block_passthrough != None:
        updates['block_passthrough'] = parser.options.block_passthrough

    comp_args = ([{'name':parser.options.name}], updates, client_utils.getuid())
    client_utils.component_call(SCHMGR, False, 'set_reservations', comp_args)
    reservations = client_utils.component_call(SCHMGR, False, 'get_reservations', 
                                               ([{'name':parser.options.name, 'users':'*','start':'*', 'duration':'*', 'partitions':'*', 
                                                  'cycle': '*', 'res_id': '*', 'project':'*', 'block_passthrough':'*'}], ))
    client_utils.logger.info(reservations)
    client_utils.logger.info(client_utils.component_call(SCHMGR, False, 'check_reservations', ()))

def add_reservation(parser,spec,user):
    """
    add reservation 
    """
    validate_starttime(parser)

    spec['users']   = None if parser.options.users == '*' else parser.options.users
    spec['cycle']   = parser.options.cycle 
    spec['project'] = parser.options.project

    if parser.options.block_passthrough == None: spec['block_passthrough'] = False

    client_utils.logger.info(client_utils.component_call(SCHMGR, False, 'add_reservations', ([spec], user)))
    client_utils.logger.info(client_utils.component_call(SCHMGR, False, 'check_reservations', ()))

def main():
    """
    setres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>           <cb args>
        [ cb_time                , (False, True, True) ], # no delta time, Seconds, return int
        [ cb_date                , (True,) ], # Allow to set the date to 'now'
        [ cb_passthrough         , () ],
        [ cb_debug               , () ],
        [ cb_res_users           , () ]] 

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    user = client_utils.getuid()

    parser.parse_it() # parse the command line
    opt_count = client_utils.get_options(spec, opts, opt2spec, parser)

    # if continue to process options then
    if validate_args(parser,spec,opt_count):

        # modify an existing reservation
        if parser.options.modify_res != None:
            modify_reservation(parser)
        
        # add new reservation
        else:
            add_reservation(parser,spec,user)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
