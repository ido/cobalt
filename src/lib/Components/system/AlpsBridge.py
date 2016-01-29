"""Bridge for communicating and fetching system state in ALPS."""

#this requires forking off a apbasil process, sending XML to stdin and
#parsing XML from stdout. Synchyronous, however, the system script
#forker isn't.  These will be able to block for now.

from cray_messaging import InvalidBasilMethodError, BasilRequest
from cray_messaging import parse_response, ALPSError

import logging

from Cobalt.Proxy import ComponentProxy
from Cobalt.Data import IncrID
from Cobalt.Util import sleep
import os

_logger = logging.getLogger()

FORKER = 'system_script_forker'
BASIL_PATH = '/home/richp/alps_simulator/apbasil.sh' #fetch this from config
#BASIL_PATH = '/usr/bin/cat' #fetch this from config

_RUNID_GEN = IncrID()
CHILD_SLEEP_TIMEOUT = 1.0


class BridgeError(Exception):

    pass

def reserve(user, jobid, nodecount, node_id_list=None):

    '''reserve a set of nodes in ALPS'''
    params = {}
    params['user_name'] = user
    params['batch_id'] = jobid
    params['width'] = nodecount
    params['depth'] = 1 #FIXME fix this.  Pass this in from qsub. FIXME
    if node_id_list is not None:
        params['node_id_list'] = node_id_list
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

    while(True):
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
    print spec['reservations']
    print spec['nodes'][0]
    for node in spec['nodes']:
        print node['name']

if __name__ == '__main__':
    print_node_names(fetch_inventory(resinfo=True))

    #print fetch_inventory(changecount=0)
    print reserve('richp', 42, 11)
