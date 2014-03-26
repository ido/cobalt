#!/usr/bin/env python
"""
Cobalt showres command

Usage: showres [-l] [-x] [--oldts] [--version]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-l',dest='verbose',action='store_true',help='print reservation list verbose'
'--oldts',dest='oldts',action='store_true',help='use old timestamp'
'-x',dest='really_verbose',action='store_true',help='print reservations really verbose'

"""
import logging
import math
import sys
import time
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 2154 $'
__version__ = '$Version$'

SYSMGR = client_utils.SYSMGR
SCHMGR = client_utils.SCHMGR

def mergelist(location_string, cluster):
    if not cluster:
        return location_string

    locations = location_string.split(":")

    return client_utils.merge_nodelist(locations)

def main():
    """
    showres main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args>
        [ cb_debug        , () ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    parser.parse_it() # parse the command line

    if not parser.no_args():
        client_utils.logger.error("No arguments needed")
    
    if parser.options.verbose != None and parser.options.really_verbose != None:
        client_utils.logger.error('Only use -l or -x not both')
        sys.exit(1)

    cluster = False
    if 'cluster' in client_utils.component_call(SYSMGR, False, 'get_implementation', ()):
        cluster = True

    reservations = client_utils.component_call(SCHMGR, False, 'get_reservations', 
                                               ([{'name':'*', 'users':'*','start':'*', 'duration':'*', 'partitions':'*', 
                                                  'cycle': '*', 'queue': '*', 'res_id': '*', 'cycle_id': '*','project':'*', 
                                                  'block_passthrough':'*'}], ))

    output = []

    verbose        = False
    really_verbose = False
    header = [('Reservation', 'Queue', 'User', 'Start', 'Duration','Passthrough', 'Partitions', 'Remaining','T-Minus')]

    if parser.options.verbose:
        verbose = True
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration',
                   'End Time', 'Cycle Time', 'Passthrough', 'Partitions', 'Remaining', 'T-Minus')]
    elif parser.options.really_verbose:
        really_verbose = True
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration','End Time', 'Cycle Time','Passthrough','Partitions', 
                   'Project', 'ResID', 'CycleID', 'Remaining', 'T-Minus' )]

    for res in reservations:

        passthrough = "Allowed"
        if res['block_passthrough']:
            passthrough = "Blocked"

        start     = float(res['start'])
        duration  = float(res['duration'])
        now       = time.time()

        deltatime = now - start
        remaining = "inactive" if deltatime < 0.0 else client_utils.get_elapsed_time(deltatime, duration, True)
        remaining = "00:00:00" if '-' in remaining else remaining
        tminus    = "active" if deltatime >= 0.0 else client_utils.get_elapsed_time(deltatime, duration, True)

        # do some crazy stuff to make reservations which cycle display the 
        # "next" start time
        if res['cycle']:
            cycle = float(res['cycle'])
            periods = math.floor((now - start)/cycle)
            # reservations can't become active until they pass the start time 
            # -- so negative periods aren't allowed
            if periods < 0:
                pass
            # if we are still inside the reservation, show when it started
            elif (now - start) % cycle < duration:
                start += periods * cycle
            # if we are in the dead time after the reservation ended, show 
            # when the next one starts
            else:
                start += (periods+1) * cycle
        if res['cycle_id'] == None:
            res['cycle_id'] = '-'

        if res['cycle']:
            cycle = float(res['cycle'])
            if cycle < (60 * 60 * 24):
                cycle = "%02d:%02d" % (cycle/3600, (cycle/60)%60)
            else:
                cycle = "%0.1f days" % (cycle / (60 * 60 * 24))
        else:
            cycle = None
        dmin = (duration/60)%60
        dhour = duration/3600

        time_fmt = "%c"
        starttime = time.strftime(time_fmt, time.localtime(start))
        endtime   = time.strftime(time_fmt, time.localtime(start + duration)) 

        if parser.options.oldts == None:
            #time_fmt += " %z (%Z)"
            starttime = client_utils.sec_to_str(start)
            endtime = client_utils.sec_to_str(start + duration)

        if really_verbose:
            output.append((res['name'], res['queue'], res['users'], 
                           starttime,"%02d:%02d" % (dhour, dmin),
                           endtime, cycle, passthrough,
                           mergelist(res['partitions'], cluster), 
                           res['project'], res['res_id'], res['cycle_id'], remaining, tminus))
        elif verbose:
            output.append((res['name'], res['queue'], res['users'], 
                           starttime,"%02d:%02d" % (dhour, dmin),
                           endtime, cycle, passthrough,
                           mergelist(res['partitions'], cluster), 
                           remaining, tminus))
        else:
            output.append((res['name'], res['queue'], res['users'], 
                           starttime,"%02d:%02d" % (dhour, dmin), passthrough,
                           mergelist(res['partitions'], cluster), 
                           remaining, tminus))

    output.sort( (lambda x,y: cmp( time.mktime(time.strptime(x[3].split('+')[0].split('-')[0].strip(), time_fmt)), 
                                   time.mktime(time.strptime(y[3].split('+')[0].split('-')[0].strip(), time_fmt))) ) )
    client_utils.print_tabular(header + output)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
