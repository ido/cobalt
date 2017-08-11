"""Bridge for communicating and fetching system state in ALPS."""

#this requires forking off a apbasil process, sending XML to stdin and
#parsing XML from stdout. Synchyronous, however, the system script
#forker isn't.  These will be able to block for now.

import logging
import xml.etree
import xmlrpclib
import json
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
# Make sure that you have key and cert set for CAPMC operaition and paths are established in the exec environment
CAPMC_PATH = get_config_option('capmc', 'path', '/opt/cray/capmc/default/bin/capmc')
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
    retval = _call_sys_forker_basil(BASIL_PATH, str(BasilRequest('RESERVE',
        params=params)))
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
    retval = _call_sys_forker_basil(BASIL_PATH, str(BasilRequest('RELEASE',
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
              'reservation_id': alps_res_id}
    retval = _call_sys_forker_basil(BASIL_PATH, str(BasilRequest('CONFIRM',
            params=params)))
    return retval

def system():
    '''fetch system information using the SYSTEM query.  Provides memory
    information'''
    params = {}
    req = BasilRequest('QUERY', 'SYSTEM', params)
    return _call_sys_forker_basil(BASIL_PATH, str(req))

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
    return _call_sys_forker_basil(BASIL_PATH, str(req))

def fetch_reservations():
    '''fetch reservation data.  This includes reservation metadata but not the
    reserved nodes.

    '''
    params = {'resinfo': True, 'nonodes' : True}
    req = BasilRequest('QUERY', 'INVENTORY', params)
    return _call_sys_forker_basil(BASIL_PATH, str(req))

def reserved_nodes():
    params = {}
    req = BasilRequest('QUERY', 'RESERVEDNODES', params)
    return _call_sys_forker_basil(BASIL_PATH, str(req))

def fetch_aggretate_reservation_data():
    '''correlate node and reservation data to get which nodes are in which
    reservation.

    '''
    pass

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


def fetch_ssd_static_data(nid_list=None, raw=False):
    '''Get static SSD information from CAPMC.

    Args:
        nid_list - optional list of nodes as a comma-delimited, hyphenated string (default None).
        raw - If True returns raw json dict.  If False, adds nid indexing (default False)

    Returns:
        A dictionary with call status, Consult CAPMC documentation for details

    Notes:
        Consult CAPMC v1.2 or ls' call for more information.

    '''
    args = ['get_ssds']
    if nid_list is not None:
        args.extend(['-n', nid_list])
    ret_info = _call_sys_forker_capmc(CAPMC_PATH, args)
    if not raw:
        # Because everything else in this system works on nids.
        fixed_ret_info = {}
        fixed_ret_info = {'e': ret_info['e'],
                          'err_msg': ret_info['err_msg']}
        fixed_ret_info['nids'] = []
        for key, val in ret_info.items():
            if key not in ['e', 'err_msg']:
                for ssd_info in val: # This is a list of SSDs potentially
                    fixed_ret_info['nids'].append(ssd_info)
        ret_info = fixed_ret_info
    return ret_info

def fetch_ssd_enable(nid_list=None):
    '''Get SSD enable flags from CAPMC.

    Args:
        nid_list - optional list of nodes as a comma-delimited, hyphenated string (default None).

    Returns:
        A dictionary with call status, and list of nid dicts of the form {"ssd_enable": val, "nid": id}

    Notes:
        Consult CAPMC v1.2 or later documentation for details on 'get_ssd_enable' call for more information.

    '''
    args = ['get_ssd_enable']
    if nid_list is not None:
        args.extend(['-n', nid_list])
    return _call_sys_forker_capmc(CAPMC_PATH, args)

def fetch_ssd_diags(nid_list=None, raw=False):
    '''Get static SSD information from CAPMC.

    Args:
        nid_list - optional list of nodes as a comma-delimited, hyphenated string (default None).
        raw - If true, do not make records consistient with other CAPMC calls output. (default False).

    Returns:
        A dictionary with call status, Consult CAPMC documentation for details

    Notes:
        Consult CAPMC v1.2 or ls' call for more information.

        This call to CAPMC, unlike others, returns 'ssd_diags' as a list of dictionaries as a top-level
            object, not 'nids'.  Size is in GB (10^3 not 2^10) instead of bytes. 'serial_num' is equivalent
            to 'serial_number' in CAPMC's get_ssds call.  Both keys are converted to match 'get_ssds' output.

    '''
    args = ['get_ssd_diags']
    if nid_list is not None:
        args.extend(['-n', nid_list])
    ret_info = _call_sys_forker_capmc(CAPMC_PATH, args)
    if not raw: # Not all consistency is foolish.
        fixed_ret_info = {}
        fixed_ret_info['e'] = ret_info['e']
        fixed_ret_info['err_msg'] = ret_info['err_msg']
        fixed_ret_info['ssd_diags'] = []
        diag_info = ret_info['ssd_diags']
        for info in diag_info:
            fixed_diag_info = {}
            for diag_key, diag_val in info.items():
                if diag_key not in ['serial_num', 'size']:
                    fixed_diag_info[diag_key] = diag_val
                elif diag_key == 'serial_num':
                    fixed_diag_info['serial_number'] = diag_val
                elif diag_key == 'size':
                    # It's storage so apparently we're using 10^3 instead of 2^10
                    # Going from GB back to bytes
                    fixed_diag_info[diag_key] = int(1000000000 * int(diag_val))
            fixed_ret_info['ssd_diags'].append(fixed_diag_info)
        ret_info = fixed_ret_info
    return ret_info

def _log_xmlrpc_error(runid, fault):
    '''Log an xmlrpc error.

    Args:
        runid: integer id of the current run in system_script_forker
        fault: xmlrpclib.Fault object raised by a component call

    Returns:
        None

    '''
    _logger.error('XMLRPC Fault recieved while fetching child %s status:', runid)
    _logger.error('Child %s: Fault code: %s', runid, fault.faultCode)
    _logger.error('Child %s: Fault string: %s', runid,
            fault.faultString)
    _logger.debug('Traceback information: for runid %s', runid,
           exc_info=True)

def _call_sys_forker(path, tag, label, args=None, in_str=None):
    '''Make a call through the system_script_forker to get output from a cray command.

    Args:
        path - path to the command
        tag - string tag for call
        label - label for logging on call
        args - arguments to command (default None)
        in_str - string to send to stdin of command (default None)

    Returns:
        stdout as a string

    Exceptions:
        Will raise a xmlrpclib.Fault if communication with the bridge
        and/or system component fails completely at startup.

     Notes:
        This is currently a blocking call until command completion.

    '''

    runid = None #_RUNID_GEN.next()
    resp = None
    cmd = [path]
    if args is not None:
        cmd.extend(args)
    try:
        child = ComponentProxy(FORKER).fork(cmd, 'apbridge',
                'alps', None, None, runid, in_str, True)
        runid = child
    except Exception:
        _logger.critical("error communicating with bridge", exc_info=True)
        raise

    while True:
        #Is a timeout needed here?
        try:
            children = ComponentProxy(FORKER).get_children('apbridge', [runid])
        except xmlrpclib.Fault as fault:
            _log_xmlrpc_error(runid, fault)
        complete = False
        for child in children:
            if child['complete']:
                if child['lost_child'] and resp is None:
                    continue # Use the original response.  This child object is
                             # invalid.  If we never got one, then let the
                             # caller handle the error.
                if child['exit_status'] != 0:
                    _logger.error("%s returned a status of %s, stderr: %s",
                            cmd, child['exit_status'], "\n".join(child['stderr']))
                resp = child['stdout_string']
                try:
                    ComponentProxy(FORKER).cleanup_children([runid])
                except xmlrpclib.Fault as fault:
                    _log_xmlrpc_error(runid, fault)
                else:
                    complete = True
        if complete:
            break
        sleep(CHILD_SLEEP_TIMEOUT)
    return resp

def _call_sys_forker_basil(basil_path, in_str):
    '''Make a  call through to BASIL wait until we get output and clean up
    child info.

    Args:
        basil_path: path to the BAISL executable. May be overriden for
                    test environments.
        in_str: A string of XML to send to 'apbasil'

    Returns:
        The XML response parsed into a Python dictionary.

    Exceptions:
        Will raise a xmlrpclib.Fault if communication with the bridge
        and/or system component fails completely at startup.

    Notes:
        This will block until 'apbasil' completion.  'apbasil' messages can
        be failrly large for things sent to stdout.

    '''

    resp = _call_sys_forker(basil_path, 'apbridge', 'alps', in_str=in_str)
    parsed_resp = {}
    try:
        parsed_resp = parse_response(resp)
    except xml.etree.ElementTree.ParseError as exc:
        _logger.error('Error parsing response "%s"', resp)
        raise exc
    return parsed_resp

def _call_sys_forker_capmc(capmc_path, args):
    '''Call a CAPMC command and recieve response'''
    resp = _call_sys_forker(capmc_path, 'apbridge', 'capmc_ssd', args=args)
    parsed_response = {}
    try:
        parsed_response = json.loads(resp)
    except TypeError:
        _logger.error("Bad type recieved for CAPMC response, expected %s got %s.", type(""), type(resp))
        raise
    except ValueError:
        _logger.error("Invalid JSON string returned: %s", resp)
    else:
        err_code = parsed_response.get('e', None)
        err_msg = parsed_response.get('err_msg', None)
        if err_code is None:
            raise ValueError('Error code in CAPMC response not provided.  Invalid response recieved. %s', resp)
        if int(err_code) != 0:
            raise ValueError('Error Code %s recieved.  Message: %s', err_code, err_msg)
    return parsed_response


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
