#!/usr/bin/env python
'''cweb: Cobalt client for serving json-encoded job and system status
required by the gornkulator.

cweb queries a running Cobalt instance to obtain system configuration
information, pending and active reservations, queued jobs and running jobs.

This client is intended to run as a daemon and provides the system status as a
REST-ish service.

'''

import logging
import sys
import time
import traceback
from collections import deque, defaultdict
from logging.handlers import SysLogHandler
from optparse import OptionParser
from random import shuffle
from socket import getfqdn
from wsgiref.simple_server import make_server, WSGIRequestHandler
try:
    import json
except ImportError:
    import simplejson as json

import daemon #python-daemon
try:
    # works for python-daemon 1.5.5 or earlier, needed for 2.6 compat.
    from daemon.pidlockfile import PIDLockFile
except (ImportError, TypeError):
    # We are in the 2.7 or later world
    from daemon.pidfile import PIDLockFile

from Cobalt.Proxy import ComponentProxy
from Cobalt.Util import merge_nodelist


class GronkdRequestHandler(WSGIRequestHandler):
    """subclass of WSGIRequestHandler so I can override the default logging
    mechanism."""
    def log_message(self, format, *args):
        msg = '%s - ' % self.client_address[0] + format % args
        logger.info(msg)

# Set up some basic logging information
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('cweb[%(process)d]: %(message)s')
syslog_handler = SysLogHandler(address='/dev/log', facility='daemon')
syslog_handler.setFormatter(formatter)
logger.addHandler(syslog_handler)

# Artifact of how this was put together and this ends up being an efficient way
# to get data into the wsgi server app.
system_type = None
system_types = ['bgsystem', 'bgqsystem', 'cluster_system', 'alps_system']
bg_types = ['bgsystem', 'bgqsystem']
cluster_types = ['cluster_system']
cray_types = ['alps_system']
hostname = getfqdn()
partition_table = {}
node_state = {}
indexes = {}
alps_system_query_fields = ['Node_id', 'Name', 'Queues', 'Status', 'Backfill']
job_query_fields = ['jobid', 'walltime', 'nodes', 'mode', 'queue', 'starttime',
                    'submittime', 'project']
reservation_query_fields = ['name', 'start', 'duration', 'partitions', 'queue']

# Maps colors to nodes and partitions
color_map = {}
# A queue containing the currently running colors
color_queue = deque(['#028F5C', '#051EB8', '#70AE14', '#0A3D70', '#0CCCCC',
                     '#0F5C28', '#11EB84', '#147AE0', '#170A3C', '#199998',
                     '#1C28F4', '#1EB850', '#2147AC', '#23D708', '#266664',
                     '#28F5C0', '#2B851C', '#2E1478', '#30A3D4', '#333330',
                     '#35C28C', '#3851E8', '#3AE144', '#3D70A0', '#3FFFFC',
                     '#428F58', '#451EB4', '#47AE10', '#4A3D6C', '#4CCCC8',
                     '#4F5C24', '#51EB80', '#547ADC', '#570A38', '#599994',
                     '#5C28F0', '#5EB84C', '#6147A8', '#63D704', '#666660',
                     '#68F5BC', '#6B8518', '#6E1474', '#70A3D0', '#73332C',
                     '#75C288', '#7851E4', '#7AE140', '#7D709C', '#7FFFF8',
                     '#828F54', '#851EB0', '#87AE0C', '#8A3D68', '#8CCCC4',
                     '#8F5C20', '#91EB7C', '#947AD8', '#970A34', '#999990',
                     '#9C28EC', '#9EB848', '#A147A4', '#A3D700', '#A6665C',
                     '#A8F5B8', '#AB8514', '#AE1470', '#B0A3CC', '#B33328',
                     '#B5C284', '#B851E0', '#BAE13C', '#BD7098', '#BFFFF4',
                     '#C28F50', '#C51EAC', '#C7AE08', '#CA3D64', '#CCCCC0',
                     '#CF5C1C', '#D1EB78', '#D47AD4', '#D70A30', '#D9998C',
                     '#DC28E8', '#DEB844', '#E147A0', '#E3D6FC', '#E66658',
                     '#E8F5B4', '#EB8510', '#EE146C', '#F0A3C8', '#F33324',
                     '#F5C280', '#F851DC', '#FAE138', '#FD7094'])
shuffle(color_queue)

def tdformat(seconds):
    '''Convert from an integer representing seconds to an #d HH:MM:SS format'''
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(int(remainder), 3600)
    minutes, seconds = divmod(remainder, 60)
    out = ''
    if days: out += '%dd ' % days
    out += ':'.join('%02d' % x for x in (hours, minutes, seconds))
    return out

def check_finished(run_jobs):
    '''checks if the job has finished running and removes from color map'''
    for job_id, color in color_map.items():
        if job_id not in run_jobs:
            color_queue.appendleft(color)
            del(color_map[job_id])

def cobalt_query(state):
    cqm = ComponentProxy('queue-manager', defer=True)
    scheduler = ComponentProxy('scheduler', defer=True)
    if state not in ('running', 'starting', 'queued', 'reservation'):
        return None
    # Templates for queries to coblat

    query_job = dict.fromkeys(job_query_fields, '*')
    query_res = dict.fromkeys(reservation_query_fields, '*')
    if state == 'reservation':
        return scheduler.get_reservations([query_res])
    if state == 'running' or state == 'starting':
        query_job['state'] = state
        query_job['location'] = '*'
    if state == 'queued':
        query_job['state'] = 'queued'
        query_job['score'] = '*'
    return cqm.get_jobs([query_job])

def get_job_data():
    # Import this here to bypass problems with daemonization
    global partition_table
    global node_state
    global system_type
    now = time.time()
    jobs = {'lastUpdated': int(now),
            'nodeinfo': defaultdict(dict),
            'indexes': indexes,
            'running': cobalt_query('running'),
            'starting': cobalt_query('starting'),
            'queued': cobalt_query('queued'),
            'reservation': cobalt_query('reservation'),
            'systemType': system_type,
            }
    # Remove stale jobs from color map
    check_finished([job['jobid'] for job in jobs['running']])
    for state in jobs:
        if state not in ('running', 'starting', 'queued', 'reservation'):
            continue
        for job in jobs[state]:
            if 'walltime' in job: #walltime is in minutes
                job['walltimef'] = tdformat(job['walltime'] * 60)
            if 'duration' in job: #duration is in seconds
                job['durationf'] = tdformat(job['duration'])
            if 'location' in job:
                if system_type in cluster_types:
                    job['locationf'] = merge_nodelist(job['location'])
                elif system_type in cray_types:
                    #location needs no format changes in this case (?)
                    pass
                else:
                    # On BGQ jobs only have one location
                    job['location'] = job['location'][0]
                    job['locationf'] = job['location']
            if state in ['running', 'starting']:
                if not color_map.get(job['jobid']):
                    color_map[job['jobid']] = color_queue.pop()
                job['color'] = color_map[job['jobid']]
                job['runtimef'] = tdformat(now - float(job['starttime']))
                nodes = job['location']
                if system_type in bg_types:
                    nodes = partition_table[job['location']]
                for node in nodes:
                    jobs['nodeinfo'][node]['jobid'] = job['jobid']
                    jobs['nodeinfo'][node]['color'] = job['color']
            if state == 'queued':
                job['queuedtimef'] = tdformat(now - job['submittime'])
            if state == 'reservation':
                job['startf'] = time.strftime('%x %X %Z',
                                              time.localtime(job['start']))
                if system_type in cluster_types:
                    nodes = job['partitions'].split(',')
                    job['partitions'] = merge_nodelist(nodes)
                elif system_type in cray_types:
                    nodes = job['partitions'].split(':')
                if now > job['start']:
                    job['tminus'] = 'active'
                else:
                    job['tminus'] = tdformat(job['start'] - now)
            for node in node_state:
                jobs['nodeinfo'][node]['state'] = node_state[node]
    return json.dumps(jobs, separators=(',', ':'))

def fetch_hardware():
    '''Autodetect which system we are trying to contact and perform hardware
    information fetch'''
    global partition_table
    global node_state
    global indexes
    global system_type
    # Generate a list of all possible nodecards in all possible partitions
    system = ComponentProxy('system', defer=True)
    if system_type is None:
        # We are self-discovering.  Can save this step if we
        # already know the system type.
        system_type = system.get_implementation()
    if system_type in bg_types:
        partition_table = dict((part['name'], part['node_card_names'])
            for part in system.get_partitions([{'name': '*',
                                                'node_card_names': '*'}]))
        node_state = {}
    elif system_type in cluster_types:
        partition_table = {}
        node_state = dict((node[0], node[1]) for node in system.get_node_status())
    elif system_type in cray_types:
        partition_table = {}
        # Using JSON for speed and avoinding the XML-RPC marshaller.
        stst = json.loads(system.get_nodes(True, None, alps_system_query_fields, True))
        indexes = {}
        for idx in stst:
            r = stst[idx]
            if r['status'] == 'busy':
                indexes[idx] = r['name']
        node_state = dict((k, v['status']) for k, v in stst.iteritems())
    else:
        raise RuntimeError('The %s system implementation is not supported by cweb')
    return system_type


def immediate_run():
    '''run queries and immediately print json output.  Exit immediately
    afterward. Return a valid exit status.'''
    try:
        fetch_hardware()
        # Generate a list of all possible nodecards in all possible partitions
        data = get_job_data()
    except Exception as exc:
        traceback.print_exc()
        return 1
    else:
        # pretty-print this
        print json.dumps(json.loads(data), separators=(',', ':'), indent=4)
    return 0

def app(environ, start_response):
    '''set application infomration'''
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)

    # Allow a method for checking status of server without querying cobalt
    if 'ping' in environ['PATH_INFO']:
        return 'PONG\n'

    return get_job_data()

def get_opts_and_args():
    '''parse out options and extract arguments'''
    parser = OptionParser('usage: %prog [options]')
    parser.add_option('-p', '--port', dest='port', default=5050, type='int',
                      help='port to run server on')
    parser.add_option('-g', '--debug', dest='debug', action='store_true',
                      help='run in debug mode')
    parser.add_option('-d', '--daemon', dest='daemon', action='store_true',
                      help='daemonize the script')
    parser.add_option('-f', '--pidfile', dest='pidfile', default='/var/run/cweb.pid',
                      help='location of pidfile')
    parser.add_option('-i', '--immediate', dest='immediate_return', action='store_true',
                      default=False,
                      help='query Cobalt daemons once, print json, and exit immediately')
    parser.add_option('--job-fields', dest='job_fields', action='store',
                      default=None, help='additional fields to query for jobs')
    parser.add_option('--reservation-fields', dest='reservation_fields', action='store',
                      default=None, help='additional fields to query for reservations')
    parser.add_option('--node-fields', dest='node_fields', action='store',
                      default=None, help='additional fields to query for nodes')

    return parser.parse_args()

def main():
    '''Gronkd driver funciton'''


    global job_query_fields
    global reservation_query_fields
    global alps_system_query_fields

    options, args = get_opts_and_args()


    if options.job_fields is not None:
        try:
            for field in options.job_fields.split(':'):
                if field.lower() not in job_query_fields:
                    job_query_fields.append(field)
        except Exception:
            logger.info('Error extending job attributes with argument %s',
                    options.job_fields)
            sys.exit(1)
    if options.reservation_fields is not None:
        try:
            reservation_query_fields.extend(options.reservation_fields.split(':'))
            for field in options.reservation_fields.split(':'):
                if field.lower() not in reservation_query_fields:
                    reservation_query_fields.append(field)
        except Exception:
            logger.info('Error extending reservation attributes with argument %s',
                    options.reservation_fields)
            sys.exit(1)
    if options.node_fields is not None:
        try:
            alps_system_query_fields.extend(options.node_fields.split(':'))
            for field in options.node_fields.split(':'):
                if field.lower() not in alps_system_query_fields:
                    alps_system_query_fields.append(field)
        except Exception:
            logger.info('Error extending node attributes with argument %s',
                    options.node_fields)
            sys.exit(1)

    if options.debug:
        # enable a simple ping-pong server for debugging.
        print json.dumps(json.loads(app({}, lambda x, y: None)), indent=4)
        sys.exit(0)

    if options.immediate_return:
        # Run, drop json to stdout and exit immediately.
        sys.exit(immediate_run())

    httpd = make_server('0.0.0.0', options.port, app,
                        handler_class=GronkdRequestHandler)
    if options.daemon:
        pidfile = PIDLockFile(options.pidfile)
        files = [httpd.fileno()]
        context = daemon.DaemonContext(pidfile=pidfile, files_preserve=files)
        with context:
            logger.info('Starting server on port %d...\n', options.port)
            while 1:
                try:
                    # Most common cause of breakage is a need to refetch
                    # hardware.
                    fetch_hardware()
                    httpd.serve_forever()
                except Exception:
                    # When we get exceptions, let's print them out to our
                    # logger and continue on with operation.
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    for line in traceback.format_exception(exc_type,
                                                           exc_value,
                                                           exc_traceback):
                        for sub_line in line.splitlines():
                            logger.error(sub_line)
    else:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.info('Starting server on port %d...\n', options.port)
        httpd.serve_forever()

if __name__ == '__main__':
    sys.exit(main())
