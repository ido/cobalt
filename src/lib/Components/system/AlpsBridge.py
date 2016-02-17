"""Bridge for communicating and fetching system state in ALPS."""

#this requires forking off a apbasil process, sending XML to stdin and
#parsing XML from stdout. Synchyronous, however, the system script
#forker isn't.  These will be able to block for now.

import logging

from cray_messaging import InvalidBasilMethodError, BasilRequest
from cray_messaging import parse_response, ALPSError
from Cobalt.Proxy import ComponentProxy
from Cobalt.Data import IncrID
from Cobalt.Util import sleep
from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.Util import compact_num_list

_logger = logging.getLogger()
init_cobalt_config()

FORKER = get_config_option('alps', 'forker', 'system_script_forker')
BASIL_PATH = get_config_option('alps', 'basil_path',
                               '/home/richp/alps_simulator/apbasil.sh')

_RUNID_GEN = IncrID()
CHILD_SLEEP_TIMEOUT = float(get_config_option('alps', 'child_sleep_timeout',
                                              1.0))
DEFAULT_DEPTH = int(get_config_option('alps', 'default_depth', 8))

class BridgeError(Exception):
    '''Exception class so that we may easily recognize bridge-specific errors.'''
    pass

def reserve(user, jobid, nodecount, attributes=None, node_id_list=None):

    '''reserve a set of nodes in ALPS'''
    if attributes is None:
        attributes = {}
    params = {}
    param_attrs = {}

    params['user_name'] = user
    params['batch_id'] = jobid
    param_attrs['width'] = attributes.get('width', nodecount)
    param_attrs['depth'] = attributes.get('depth', DEFAULT_DEPTH)
    param_attrs['nppn'] = attributes.get('nnpn', None)
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
        params['node_id_list'] = compact_num_list(node_id_list)
    print str(BasilRequest('RESERVE', params=params))
    retval = _call_sys_forker(BASIL_PATH, str(BasilRequest('RESERVE',
        params=params)))
    print str(retval)
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
    req = BasilRequest('QUERY', 'INVENTORY', params)
    return _call_sys_forker(BASIL_PATH, str(req))

def _call_sys_forker(basil_path, in_str):
    '''take a parameter dictionary and make appropriate call through to BASIL
    wait until we get output and clean up child info.'''

    runid = None #_RUNID_GEN.next()i
    resp = None
    try:
        child = ComponentProxy(FORKER).fork([BASIL_PATH], 'apbridge',
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

    return parse_response(resp)

def print_node_names(spec):
    '''Debugging utility to print nodes returned by ALPS'''
    print spec['reservations']
    print spec['nodes'][0]
    for node in spec['nodes']:
        print node['name']

if __name__ == '__main__':
    print_node_names(fetch_inventory(resinfo=True))

    #print fetch_inventory(changecount=0)
    print reserve('richp', 42, 11)
