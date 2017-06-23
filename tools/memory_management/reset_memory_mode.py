#!/usr/bin/env python2.7
'''Reset MCDRAM configuration and NUMA mode on KNL nodes. If we are on a Cray,
this will use CAPMC controls, otherwise we're using Intel controls.

Must run at sufficient privilege to access memory mode modification commands and
node reboot commands (CAPMC or IPMI needed)

The CAPMC module should be loaded on Cray systems.

'''
import sys
import ast
from subprocess import Popen, PIPE
import time
import json
import logging
import logging.handlers
import os.path
from Cobalt.Util import expand_num_list, compact_num_list

SUCCESS = 0
RESET_FAILURE = 3
BOOT_FAILURE = 4
BAD_ARGS = 5

DEFAULT_MCDRAM = 'cache'
DEFAULT_NUMA = 'quad'

AVAILABLE_MCDRAM = ['cache', 'split', 'equal', 'flat']
AVAILABLE_NUMA = ['a2a', 'snc2', 'snc4', 'hemi', 'quad']

INITIALIZATION_TIMEOUT = 600.0 #defaulting to 10 minutes.  Reboots are slow.  Time to wait for reboot to start.
TIMEOUT = 2700 # reboot timeout in seconds
POLL_INT = 1.00 # Polling interval once we start checking for reboot completion

CAPMC_CMD = '/opt/cray/capmc/default/bin/capmc'

#syslog setup
LOG_DATEFMT = '%Y-%d-%m %H:%M:%S'
BASE_FMT = '%(asctime)s %(message)s'
SYSLOG_FMT = '%(name)s[%(process)d]: %(asctime)s %(message)s'

logging.basicConfig(format=BASE_FMT, datefmt=LOG_DATEFMT)
logger = logging.getLogger('reset_memory_mode')
logger.setLevel(logging.INFO)
syslog = logging.handlers.SysLogHandler('/dev/log')
syslog.setFormatter(logging.Formatter(SYSLOG_FMT, datefmt=LOG_DATEFMT))
logger.addHandler(syslog)

ACCOUNTING_LOG_PATH = '/var/log/pbs/boot'
ACCOUNTING_MSG_FMT = "%s;%s;%s;%s" # Date, Type, Jobid, keyvals
ACCOUNTING_DATE_FMT = "%m/%d/%Y %H:%M:%S"

def dict_to_keyval_str(dct):
    '''put a record keyval dict into a string format for pbs logging'''
    ret_pairs = []
    for key, val in dct.iteritems():
        ret_pairs.append("%s=%s" % (key, val))
    return " ".join(ret_pairs)

def get_current_modes(node_list):
    '''Fetch the current memory mode of the listed nodes

    Args:
        node_list - A list of nodes to fetch current information for.
                    May be cray compact notation
    Returns:
        A dictonary of the requested nids.  The value is dictonary of MCDRAM and NUMA
        modes tuple.
    '''
    # Short of going out to the nodes and reading secret sauce in /proc we are
    # assuming that the nodes mode have not been changed for the next reboot
    # (i.e. that this script and the scheduler are the only things changing
    # memory modes on this system for now.  The value we get out of CAPMC here
    # is for the next reboot.

    # The moral of this story: Do not change the memory mode unless the next
    # thing you do is reboot the node.

    #exp_nodelist = expand_num_list(node_list)
    node_cfgs = {}

    mcdram_raw_info, err = exec_fetch_output(CAPMC_CMD, ['get_mcdram_cfg',
                                            '--nids', node_list])
    numa_raw_info, err = exec_fetch_output(CAPMC_CMD, ['get_numa_cfg',
                                            '--nids', node_list])

    mcdram_info = json.loads(mcdram_raw_info)
    numa_info = json.loads(numa_raw_info)

    for info in mcdram_info['nids']:
        node_cfgs[info['nid']] = {'mcdram_mode': info['mcdram_cfg']}
    for info in numa_info['nids']:
        node_cfgs[info['nid']]['numa_mode'] = info['numa_cfg']

    return node_cfgs

def exec_fetch_output(cmd, args, timeout=None):
    '''execute commands and return stdout/stderr tuple.

    Raise exception in the event of a nonzero return.

    '''
    endtime = None
    timeout_trip = False
    if timeout is not None:
        endtime = int(time.time()) + int(timeout)
    cmd_list = [cmd]
    cmd_list.extend(args)
    proc = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    stdout = ""
    stderr = ""
    while True:
        curr_stdout, curr_stderr = proc.communicate()
        stdout += curr_stdout
        stderr += curr_stderr
        if endtime is not None and int(time.time()) >= endtime:
            #signal and kill
            timeout_trip = True
            proc.terminate()
            break
        #check to see if the process has terminated.
        if proc.poll() is not None:
            break
        time.sleep(POLL_INT)
    try:
        curr_stdout, curr_stderr = proc.communicate()
        stdout += curr_stdout
        stderr += curr_stderr
    except ValueError:
        pass # Everything is closed and terminated.
    if timeout_trip:
        raise RuntimeError("%s timed out!" % cmd)
    if handle_capmc_error(stdout):
        #error strings from capmc come back on stdout
        logger.error('Error running cmd: %s args:%s.\nStdout: %s\nStderr: %s', cmd, args, stdout, stderr)
        raise RuntimeError("%s failed with internal err status" % (cmd))
    if proc.returncode != 0:
        logger.error('Error running cmd: %s args:%s.\nStdout: %s\nStderr: %s', cmd, args, stdout, stderr)
        raise RuntimeError("%s failed with an exit status of %s" % (cmd, proc.returncode))
    return (stdout, stderr)


def handle_capmc_error(capmc_json_str, label=None):
    '''extract error status from CAPMC.  If nonzero, dump the entire message.'''

    error = False
    try:
        response = json.loads(capmc_json_str)
    except ValueError:
        logger.error('Unable to parse json string %s', capmc_json_str)
        error = True
    else:
        if int(response.get('e', '0')) != 0:
            error = True
            logger.error('Status %s detected.  Message: %s', response['e'], response['err_msg'])
    return error

def reset_modes(node_list, mcdram_mode, numa_mode, label):
    '''execute commands to reconfigure KNLs'''
    try:
        stdout, stderr = exec_fetch_output(CAPMC_CMD,
            ['set_mcdram_cfg', '--mode', mcdram_mode, '--nids', node_list])
    except RuntimeError:
        print >> sys.stderr, "Could not reset mcdram_mode"
        return False
    try:
        stdout, stderr = exec_fetch_output(CAPMC_CMD,
            ['set_numa_cfg', '--mode', numa_mode, '--nids', node_list])
    except RuntimeError:
        print >> sys.stderr, "Could not reset numa_mode"
        return False
    logger.info('%s: Reset mcdram/numa mode to %s/%s on nodes %s', label, mcdram_mode,
                numa_mode, node_list)
    return True

def reboot_nodes(node_list, mcdram_mode, numa_mode, label):
    '''Initiate reboot of node list.  This call doesn't block.  Check with
    reboot complete.

    '''
    logger.info('%s: Rebooting nodes %s', label, node_list)
    try:
        stdout, stderr = exec_fetch_output(CAPMC_CMD,
            ['node_reinit', '--nids', node_list, '--reason',
                '%s: Reset MCDRAM/NUMA mode to %s/%s' % (label, mcdram_mode, numa_mode, )])
    except RuntimeError:
        print >> sys.stderr, "Unable to initiate node reboot"
        return False
    return True

def reboot_complete(node_list, timeout, label):
    '''determine if reboot completed'''
    endtime = int(time.time()) + int(timeout)
    exp_nodelist = set(expand_num_list(node_list))
    while True:
        if int(time.time()) > endtime:
            logger.error("%s: Reboot of %s timed out.", label, node_list)
            return False
        try:
            stdout, stderr = exec_fetch_output(CAPMC_CMD,
                    ['node_status', '--nids', node_list, '--filter', 'show_ready'])
        except RuntimeError as exc:
            logger.error("%s: Unable to complete reboot: %s", label, exc.message)
            return False
        node_info = json.loads(stdout)
        if 'ready' not in node_info.keys():
            pass
        if not set(exp_nodelist) - set(node_info.get('ready', [])):
            break
        time.sleep(1.0)

    logger.info('%s: Reboot of nodes %s complete', label, node_list)
    return True

def main():
    '''driver for reboot'''
    mcdram_mode = DEFAULT_MCDRAM
    numa_mode = DEFAULT_NUMA
    node_list = ''
    jobid = None
    user = None
    for arg in sys.argv:
        try:
            splitarg = arg.split('=')
            key = splitarg[0]
            val = '='.join(splitarg[1:])
        except (IndexError, ValueError, TypeError):
            print >> sys.stderr, "Missing or badly formatted args."
            return BAD_ARGS
        if key == 'attrs':
            attr_dict = ast.literal_eval(val)
            for akey, aval in attr_dict.items():
                if akey == 'mcdram':
                    if not  aval.lower() in AVAILABLE_MCDRAM:
                        print >> sys.stderr, "%s is an invalid MCDRAM mode" % aval
                        return BAD_ARGS
                    else:
                        mcdram_mode = aval.lower()
                elif akey == 'numa':
                    if not aval.lower() in AVAILABLE_NUMA:
                        print >> sys.stderr, "%s is an invalid NUMA mode" % aval
                        return BAD_ARGS
                    else:
                        numa_mode = aval.lower()
                else:
                    pass
        elif key == 'location':
            #string compact cray nodelist
            node_list = val
        elif key == 'user':
            user = val
        elif key == 'jobid':
            jobid = val
            bootid = val #boot id matches jobid for now.
        else:
            pass

    label = "%s/%s/%s" % (user, jobid, bootid)
    accounting_log_filename = '%s-%s' % (time.strftime('%Y%m%d-boot', time.gmtime()), bootid)
    current_node_cfg = get_current_modes(node_list)
    nodes_to_modify = []
    initial_modes = {}
    for nid, node in current_node_cfg.items():
        if (mcdram_mode.lower() != node['mcdram_mode'].lower() or
            numa_mode.lower() != node['numa_mode'].lower()):
            # node needs a reboot
            mode = '%s:%s' % (node['mcdram_mode'].lower(), node['numa_mode'].lower())
            if initial_modes.get(mode, None) is not None:
                initial_modes[mode].append(int(nid))
            else:
                initial_modes[mode] = [int(nid)]
            nodes_to_modify.append(int(nid))
    initial_mode_list = []
    for mode, mod_node_list in initial_modes.items():
        initial_mode_list.append('%s:%s' % (mode, compact_num_list(mod_node_list)))
    # assuming that mode change is immediately followed by reboot.  Modify when
    # current setting inspection available.

    success = True
    exit_status = SUCCESS
    reboot_info = {'bootid': bootid,
                   'boot_time': 'N/A',
                   'rebooted': compact_num_list(nodes_to_modify),
                   'blocked': node_list,
                   'from_mode': ','.join(initial_mode_list),
                   'to_mode': '%s:%s:%s' % (mcdram_mode, numa_mode, node_list),
                   'successful': False,
                   'start': None,
                   'end': None,
                   }
    if len(nodes_to_modify) != 0: #if we don't have to reboot, don't go through this.
        accounting_start_msg = ACCOUNTING_MSG_FMT % (time.strftime(ACCOUNTING_DATE_FMT, time.gmtime()), 'BS', jobid,
                "bootid=%s blocked=%s" % (bootid, reboot_info['blocked']))
        with open(os.path.join(ACCOUNTING_LOG_PATH, accounting_log_filename), "a+") as acc_file:
            acc_file.write(accounting_start_msg + '\n')
        logger.info("%s", accounting_start_msg)
        start = time.time()
        reboot_info['start'] = start
        compact_nodes_to_modify = compact_num_list(nodes_to_modify)
        try:
            if not reset_modes(compact_nodes_to_modify, mcdram_mode, numa_mode,
                    label):
                print >> sys.stderr, "Failed to reset memory mode"
                success = False
                exit_status = RESET_FAILURE
            if success and not reboot_nodes(compact_nodes_to_modify, mcdram_mode, numa_mode,
                    label):
                print >> sys.stderr, "Failed to initiate node reboot"
                success = False
                exit_status = BOOT_FAILURE
            if success:
                #wait for boot intialization so that we can see reboot starting.
                time.sleep(INITIALIZATION_TIMEOUT)
            if success and not reboot_complete(compact_nodes_to_modify, TIMEOUT,
                    label):
                logger.error("%s: Node reboot failed to complete, nodes: %s", label, compact_nodes_to_modify)
                success = False
                exit_status = BOOT_FAILURE

            reboot_info['successful'] = success
        finally:
            end = time.time()
            reboot_info['end'] = end
            reboot_info['boot_time'] = int(end - start)
            accounting_end_msg = ACCOUNTING_MSG_FMT % (time.strftime(ACCOUNTING_DATE_FMT, time.gmtime()), 'BE', jobid,
                    dict_to_keyval_str(reboot_info))
            with open(os.path.join(ACCOUNTING_LOG_PATH, accounting_log_filename), "a+") as acc_file:
                acc_file.write(accounting_end_msg + '\n')
            logger.info("%s", accounting_end_msg)

    return exit_status

if __name__ == '__main__':
    sys.exit(main())
