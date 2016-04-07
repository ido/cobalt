"""Bridge for communicating and fetching system state in ALPS."""

#this requires forking off a apbasil process, sending XML to stdin and
#parsing XML from stdout. Synchyronous, however, the system script
#forker isn't.  These will be able to block for now.

import logging
import xml.etree
from cray_messaging import InvalidBasilMethodError, BasilRequest
from cray_messaging import parse_response, ALPSError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Data import IncrID
from Cobalt.Util import sleep
from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.Util import compact_num_list, expand_num_list

_logger = logging.getLogger()
init_cobalt_config()

FORKER = get_config_option('alps', 'forker', 'system_script_forker')
BASIL_PATH = get_config_option('alps', 'basil',
                               '/home/richp/alps-simulator/apbasil.sh')

_RUNID_GEN = IncrID()
CHILD_SLEEP_TIMEOUT = float(get_config_option('alps', 'child_sleep_timeout',
                                              1.0))
DEFAULT_DEPTH = int(get_config_option('alps', 'default_depth', 72))

class BridgeError(Exception):
    '''Exception class so that we may easily recognize bridge-specific errors.'''
    pass

def init_bridge():
    '''Initialize the bridge.  This includes purging all old bridge messages
    from the system_script_forker.  On restart or reinitialization, these old
    children should be considered invalid and purged.

    '''
    forker = ComponentProxy(FORKER, defer=True)
    try:
        stale_children = forker.get_children('apbridge', None)
        forker.cleanup_children([int(child['id']) for child in stale_children])
    except Exception:
        _logger.error('Unable to clear children from prior runs.  Init failed.',
                exc_info=True)
        raise BridgeError('Bridge initialization failed.')
    return

def reserve(user, jobid, nodecount, attributes=None, node_id_list=None):

    '''reserve a set of nodes in ALPS'''
    if attributes is None:
        attributes = {}
    params = {}
    param_attrs = {}

    params['user_name'] = user
    params['batch_id'] = jobid
    param_attrs['width'] = attributes.get('width', nodecount * DEFAULT_DEPTH)
    param_attrs['depth'] = attributes.get('depth', None)
    param_attrs['nppn'] = attributes.get('nppn', DEFAULT_DEPTH)
    param_attrs['npps'] = attributes.get('nnps', None)
    param_attrs['nspn'] = attributes.get('nspn', None)
    param_attrs['reservation_mode'] = attributes.get('reservation_mode',
                                                     'EXCLUSIVE')
    param_attrs['nppcu'] = attributes.get('nppcu', None)
    param_attrs['p-state'] = attributes.get('p-state', None)
    param_attrs['p-govenor'] = attributes.get('p-govenor', None)
    for key, val in param_attrs.items():
        if val is not None:
            params[key] = val
    if node_id_list is not None:
        params['node_list'] = [int(i) for i in node_id_list]
    _logger.debug('reserve request: %s', str(BasilRequest('RESERVE',
        params=params)))
    retval = _call_sys_forker(BASIL_PATH, str(BasilRequest('RESERVE',
        params=params)))
    _logger.debug('reserve return %s', retval)
    return retval

def release(alps_res_id):
    '''release a set of nodes in an ALPS reservation.  May be used on a
    reservation with running jobs.  If that occurs, the reservation will be
    released when the jobs exit/are terminated.

    Input:
        alps_res_id - id of the ALPS reservation to release.

    Returns:
        True if relese was successful

    Side Effects:
        ALPS reservation will be released.  New aprun attempts agianst
        reservation will fail.

    Exceptions:
        None Yet

    '''
    params = {'reservation_id': alps_res_id}
    retval = _call_sys_forker(BASIL_PATH, str(BasilRequest('RELEASE',
            params=params)))
    return retval

def confirm(alps_res_id, pg_id):
    '''confirm an ALPS reservation.  Call this after we have the process group
    id of the user job that we are reserving nodes for.

    Input:
        alps_res_id - The id of the reservation that is being confirmed.
        pg_id - process group id to bind the reservation to.

    Return:
        True if the reservation is confirmed.  False otherwise.

    Side effects:
        None

    Exceptions:
        None Yet.
    '''
    params = {'pagg_id': pg_id,
              'reservation': alps_res_id}
    retval = _call_sys_forker(BASIL_PATH, str(BasilRequest('CONFIRM',
            params=params)))
    return retval

def system():
    '''fetch system information using the SYSTEM query.  Provides memory
    information'''
    params = {}
    req = BasilRequest('QUERY', 'SYSTEM', params)
    return _call_sys_forker(BASIL_PATH, str(req))

def fetch_inventory(changecount=None, resinfo=False):
    '''fetch the inventory for the machine

        changecount -  changecount to send if we only want deltas past a certain
        point
        resinfo - also fetch information on current reservations

        return:
        dictionary of machine information parsed from XML response
    '''
    params = {}
    if changecount is not None:
        params['changecount'] = changecount
    if resinfo:
        params['resinfo'] = True
    #TODO: add a flag for systems with version <=1.4 of ALPS
    req = BasilRequest('QUERY', 'INVENTORY', params)
    #print str(req)
    return _call_sys_forker(BASIL_PATH, str(req))

def fetch_reservations():
    '''fetch reservation data.  This includes reservation metadata but not the
    reserved nodes.

    '''
    params = {'resinfo': True, 'nonodes' : True}
    req = BasilRequest('QUERY', 'INVENTORY', params)
    return _call_sys_forker(BASIL_PATH, str(req))

def reserved_nodes():
    params = {}
    req = BasilRequest('QUERY', 'RESERVEDNODES', params)
    return _call_sys_forker(BASIL_PATH, str(req))

def fetch_aggretate_reservation_data():
    '''correlate node and reservation data to get which nodes are in which
    reservation.

    '''

def extract_system_node_data(node_data):
    ret_nodeinfo = {}
    for node_info in node_data['nodes']:
        #extract nodeids, construct from bulk data block...
        for node_id in expand_num_list(node_info['node_ids']):
            node = {}
            node['node_id'] = node_id
            node['state'] = node_info['state']
            node['role'] = node_info['role']
            node['attrs'] = node_info
            ret_nodeinfo[str(node_id)] = node
        del node_info['state']
        del node_info['node_ids']
        del node_info['role']
    return ret_nodeinfo


def _call_sys_forker(basil_path, in_str):
    '''take a parameter dictionary and make appropriate call through to BASIL
    wait until we get output and clean up child info.'''

    runid = None #_RUNID_GEN.next()i
    resp = None
    try:
        child = ComponentProxy(FORKER).fork([basil_path], 'apbridge',
                'alps', None, None, runid, in_str, True)
        runid = child
    except Exception:
        _logger.critical("error communicating with bridge", exc_info=True)
        raise

    while True:
        #Is a timeout needed here?
        children = ComponentProxy(FORKER).get_children('apbridge', [runid])
        complete = False
        for child in children:
            if child['complete']:
                if child['exit_status'] != 0:
                    _logger.error("BASIL returned a status of %s",
                            child['exit_status'])
                resp = child['stdout_string']
                ComponentProxy(FORKER).cleanup_children([runid])
                complete = True
        if complete:
            break
        sleep(CHILD_SLEEP_TIMEOUT)

    parsed_resp = {}
    try:
        parsed_resp = parse_response(resp)
    except xml.etree.ElementTree.ParseError as exc:
        _logger.error('Error parsing response "%s"', resp)
        raise exc
    return parsed_resp

def print_node_names(spec):
    '''Debugging utility to print nodes returned by ALPS'''
    print spec['reservations']
    print spec['nodes'][0]
    for node in spec['nodes']:
        print node['name']

if __name__ == '__main__':
    #print_node_names(fetch_inventory(resinfo=True))

    # print fetch_inventory(changecount=0)
    # print extract_system_node_data(system())
    # print fetch_reserved_nodes()
    # print fetch_inventory(resinfo=True)
    print fetch_reservations()
