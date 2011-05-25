#!/usr/bin/env python
'''Display reservations'''
__revision__ = '$Revision$'
__version__ = '$Version$'

import sys, time
import math
import optparse
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Util import sec_to_str


__helpmsg__ = "Usage: showres [-l] [-x] [--oldts] [--version]"

def mergelist(location_string, cluster):
    if not cluster:
        return location_string

    locations = location_string.split(":")

    return Cobalt.Util.merge_nodelist(locations)

#def parse_options()
#    p = optparse.OptionParser()
#    p.add_option("-l", "--long", action="store_true", default=False
#            dest="long", help="shows long display")
#    p.add_option(None, "--version" action="store_true", default=False,
#            dest="version", help="Prints version information")
#    p.add_option(None, 


if __name__ == '__main__':
    if '--version' in sys.argv:
        print "showres %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    Cobalt.Logging.setup_logging('showres', to_syslog=False, level=20)
    try:
        scheduler = ComponentProxy("scheduler", defer=False)
    except ComponentLookupError:
        print "Failed to connect to scheduler"
        raise SystemExit, 1
    cluster = False
    try:
        if "cluster" in ComponentProxy("system", defer=False).get_implementation():
            cluster = True
    except ComponentLookupError:
        print "Failed to connect to system component"
        raise SystemExit, 1

    reservations = scheduler.get_reservations([{'name':'*', 'users':'*', 
        'start':'*', 'duration':'*', 'partitions':'*', 'cycle': '*', 
        'queue': '*', 'res_id': '*', 'cycle_id': '*', 
        'project':'*'}])
    output = []
 
    verbose = False
    really_verbose = False
    header = [('Reservation', 'Queue', 'User', 'Start', 'Duration', 
        'Partitions')]
    
    if '-l' in sys.argv:
        verbose = True
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration', 
            'End Time', 'Cycle Time', 'Partitions')]
    if '-x' in sys.argv:
        really_verbose = True
        header = [('Reservation', 'Queue', 'User', 'Start', 'Duration', 
            'End Time', 'Cycle Time', 'Partitions', 'Project', 'ResID', 'CycleID')]

    for res in reservations:
        start = float(res['start'])
        duration = float(res['duration'])
        # do some crazy stuff to make reservations which cycle display the 
        # "next" start time
        if res['cycle']:
            cycle = float(res['cycle'])
            now = time.time()
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
        endtime = time.strftime(time_fmt, time.localtime(start + duration)) 

        if not ('--oldts' in sys.argv):
            #time_fmt += " %z (%Z)"
            starttime = sec_to_str(start)
            endtime = sec_to_str(start + duration)
    

        if really_verbose:
            output.append((res['name'], res['queue'], res['users'], 
                starttime,
                "%02d:%02d" % (dhour, dmin),
                endtime, cycle, 
                mergelist(res['partitions'], cluster), res['project'],
                res['res_id'], res['cycle_id']))
        elif verbose:
            output.append((res['name'], res['queue'], res['users'], 
                starttime,
                "%02d:%02d" % (dhour, dmin),
                endtime, cycle, 
                mergelist(res['partitions'], cluster)))
        else:
            output.append((res['name'], res['queue'], res['users'], 
                starttime,
                "%02d:%02d" % (dhour, dmin), 
                mergelist(res['partitions'], cluster)))

    output.sort( (lambda x,y: cmp( time.mktime(time.strptime(x[3].split('+')[0].split('-')[0].strip(), time_fmt)), 
        time.mktime(time.strptime(y[3].split('+')[0].split('-')[0].strip(), time_fmt))) ) )
    Cobalt.Util.print_tabular(header + output)
                     
