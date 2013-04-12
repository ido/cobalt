#!/usr/bin/env python
"""
Setup reservations in the scheduler

Usage: %prog [options] <partition1> ... <partitionN>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-A','--project',dest='project',type='string',help='set project name for partitions in args'
'-D','--defer',dest='defer',help='defer flag. needs to be used with -m',action='store_true'
'-c','--cycletime',dest='cycle',type='string',help='set cycle time in minutes or HH:MM:SS',callback=cb_time
'-d','--duration',dest='duration',type='string',help='duration time in minutes or HH:MM:SS>',callback=cb_time
'-m','--modify_res',dest='modify_res',help='modify current reservation specified in -n',action='store_true'
'-n','--name',dest='name',type='string',help='reservation name to add or modify'
'-p','--partition',dest='partitions',type='string',help='partition (now optional)'
'-q','--queue',dest='queue',type='string',help='queue name'
'-s','--starttime',dest='start',type='string',help='start date time: YYYY_MM_DD-HH:MM>',callback=cb_date
'-u','--user',dest='users',type='string',help='user id list (user1:user2:...)',callback=cb_user_list

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
from Cobalt.client_utils import \
    cb_time, cb_date, cb_passthrough, cb_user_list

from Cobalt.arg_parser import ArgParse

__revision__ = '$Id: setres.py 2154 2011-05-25 00:22:56Z richp $'
__version__ = '$Version$'

def validate_args(parser,spec,opt_count):
    """
    Validate setres arguments. Will return true if we want to continue processing options.
    """
    if parser.options.partitions != None:
        parser.args += [parser.options.partitions]

    if parser.options.cycle_id != None or parser.options.res_id != None:
        only_id_change = True
        if not parser.no_args() or (opt_count != 0):
            client_utils.logger.error('No partition arguments or other options allowed with id change options')
            sys.exit(1)
    else:
        only_id_change = False

    if parser.options.force_id and not only_id_change:
        client_utils.logging.error("--force_id can only be used with --cycle_id and/or --res_id.")
        sys.exit(1)

    if only_id_change:

        # make the ID change and we are done with setres
        
        if parser.options.res_id != None:
            client_utils.set_res_id(parser)
        if parser.options.cycle_id != None:
            client_utils.set_cycle_id(parser)

        continue_processing_options = False # quit, setres is done

    else:

        if parser.no_args() and (parser.options.modify_res == None):
            client_utils.logging.error("Must supply either -p with value or partitions as arguments")
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

        if parser.options.name == None and parser.options.modify_res != None:
            client_utils.logger.error("-m must by called with -n <reservation name>")
            sys.exit(1)

        # if we have args then verify the args (partitions)
        if not parser.no_args():
            client_utils.verify_locations(parser.args)

        # if we have command line arguments put them in spec
        if not parser.no_args(): spec['partitions'] = ":".join(parser.args)

        continue_processing_options = True # continue, setres is not done.

    return continue_processing_options

        
def modify_reservation(parser):
    """
    this will handle reservation modifications
    """
    query = [{'name':parser.options.name, 'start':'*', 'cycle':'*', 'duration':'*'}]
    res_list = client_utils.get_reservations(query)
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
        updates['users'] = ':'.join(parser.options.users)
    if parser.options.project != None:
        updates['project'] = parser.options.project
    if parser.options.cycle != None:
        updates['cycle'] = parser.options.cycle
    if not parser.no_args():
        updates['partitions'] = ":".join(parser.args)
    if parser.options.block_passthrough != None:
        updates['block_passthrough'] = parser.options.block_passthrough

    client_utils.modify_reservation(parser.options.name,updates)

def add_reservation(parser,spec,user):
    """
    add reservation 
    """
    spec['users']             = ':'.join(parser.options.users) if parser.options.users != None else None
    spec['cycle']             = parser.options.cycle 
    spec['project']           = parser.options.project
    if parser.options.name              == None: spec['name']              = 'system'
    if parser.options.block_passthrough == None: spec['block_passthrough'] = False

    client_utils.add_reservation(spec,user)


def main():
    """
    setres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    dt_allowed = False # Delta time not allowed
    seconds    = True  # convert to seconds
    add_user   = False # do not add current user to the list

    # list of callback with its arguments
    callbacks = [
        # <cb function>           <cb args>
        [ cb_time                , (dt_allowed,seconds) ],
        [ cb_date                , () ],
        [ cb_passthrough         , () ],
        [ cb_user_list           , (opts,add_user) ]]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    user = client_utils.getuid()

    parser.parse_it() # parse the command line
    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)

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
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
