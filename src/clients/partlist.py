#!/usr/bin/env python
"""
Cobalt partlist command - Partlist displays online partitions for users

Usage: %prog [options] 
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug

"""
import time
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import cb_debug

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 1981 $'
__version__ = '$Version$'

SYSMGR = client_utils.SYSMGR
SCHMGR = client_utils.SCHMGR

def main():
    """
    partlist main
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
        client_utils.logger.error("No arguments required")
        sys.exit(1)
    
    sys_info = client_utils.system_info()
    
    sys_type = sys_info[0]

    if sys_type == 'bgq':
        spec = [{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*',
                 'size':'*', 'functional':'*', 'scheduled':'*', 'children':'*',
                 'backfill_time':"*", 'draining':"*",'node_geometry':"*"}]
    else:
        spec = [{'tag':'partition', 'name':'*', 'queue':'*', 'state':'*',
                 'size':'*', 'functional':'*', 'scheduled':'*', 'children':'*',
                 'backfill_time':"*", 'draining':"*"}]

    parts        = client_utils.component_call(SYSMGR, True, 'get_partitions', (spec,))
    reservations = client_utils.component_call(SCHMGR, False, 'get_reservations', 
                                               ([{'queue':'*','partitions':'*','active':True}],))

    expanded_parts = {}
    for res in reservations:
        for res_part in res['partitions'].split(':'):
            for p in parts:
                if p['name'] == res_part:
                    if expanded_parts.has_key(res['queue']):
                        expanded_parts[res['queue']].update(p['children'])
                    else:
                        expanded_parts[res['queue']] = set( p['children'] )
                    expanded_parts[res['queue']].add(p['name'])    
    
    for res in reservations:
        for p in parts:
            if p['name'] in expanded_parts.get(res['queue'], []):
                p['queue'] += ":%s" % res['queue']

    def my_cmp(left, right):
        val = -cmp(int(left['size']), int(right['size']))
        if val == 0:
            return cmp(left['name'], right['name'])
        else:
            return val

    parts.sort(my_cmp)
    now = time.time()
    for part in parts:
        if part['draining'] and part['state'] == "idle":
            # remove a little extra, to make sure that users can just type the number
            # that is output by partlist to get their job to backfill
            remaining = max(0, part['backfill_time'] - now - 90)
            hours, seconds = divmod(remaining, 3600.0)
            minutes = seconds/60.0
            part['backfill'] = "%d:%0.2d" % (int(hours), int(minutes))
        else:
            part['backfill'] = "-"

    if sys_type == 'bgq':
        header = [['Name', 'Queue', 'State', 'Backfill', 'node_geometry']]
        #build output list, adding
        output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts 
                  if part['functional'] and part['scheduled']]
        #Hack to make the display cleaner.
        header[0][4] = 'Geometry'
        for o in output:
            if o[4] != None:
                o[4] = 'x'.join([str(i) for i in o[4]])
    else:
        header = [['Name', 'Queue', 'State', 'Backfill']]
        #build output list, adding
        output = [[part.get(x) for x in [y.lower() for y in header[0]]] for part in parts 
                  if part['functional'] and part['scheduled']]
    client_utils.printTabular(header + output)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)

