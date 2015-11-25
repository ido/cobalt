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

def reserve():

    '''reserve a set of nodes in ALPS'''
    pass

def release():
    '''release a set of nodes in an ALPS reservation'''
    pass

def confirm():
    '''confirm an ALPS reservation'''
    pass

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
