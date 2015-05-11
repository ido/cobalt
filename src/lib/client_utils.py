"""
This module defines Cobalt Client utility functions.
The contents are:
   - Functions that abstract component interaction
   - Common client utility functions
   - Argument Parsing callback functions. These functions are prefixed by 'cb_' 
     and are defined at the end of the module.
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
import pwd
import os.path
import xmlrpclib
import ConfigParser
import re
import logging
import time

import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Util import parse_geometry_string
from Cobalt.arg_parser import ArgParse
from Cobalt.Exceptions import ComponentLookupError, JobValidationError

logger   = None # Logging instance. setup_logging needs to be called first thing.

#
# Constant used for tagging what needs to be replaced with the current working directory
CWD_TAG     =  "<REPLACE WITH CWD>"
SYSMGR      = 'system'
QUEMGR      = 'queue-manager'
SLPMGR      = 'service-location'
SCHMGR      = 'scheduler'

#
# env Tags
COL_TAG = "<<*COL*>>"
EQL_TAG = "<<*EQL*>>"
ESC_COL = "\:"
ESC_EQL = "\="

# posix return statuses 
AUTH_FAIL       = 2
BAD_OPTION_FAIL = 3
GENERAL_FAIL    = 1
SUCCESS         = 0

class Logger(object):
    """
    This class will handle logging to standard error or standard out
    for info will go to stdout everything else will go to standard error
    """

    def __init__(self, level):
        """
        Cobalt Client log commands
        """
        self.h_stdout = logging.StreamHandler(sys.stdout)
        self.h_stdout.setLevel(logging.INFO)
        self.stdout_logger = logging.getLogger('cobalt_client_stdout')
        self.stdout_logger.addHandler(self.h_stdout)
        self.stdout_logger.setLevel(level)

        self.h_stderr = logging.StreamHandler(sys.stderr)
        self.h_stderr.setLevel(logging.DEBUG)
        self.stderr_logger  = logging.getLogger('cobalt_client_stderr')
        self.stderr_logger.addHandler(self.h_stderr)
        self.stderr_logger.setLevel(level)

        Cobalt.Util.logger = self.stderr_logger

    def setLevel(self, level):
        """
        set logging level
        """
        self.stdout_logger.setLevel(level)
        self.stderr_logger.setLevel(level)

    def debug(self, msg, *args, **kwargs):
        """
        print debug message
        """
        self.stderr_logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """
        print info message
        """
        self.stdout_logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """
        print warning message
        """
        self.stderr_logger.warn(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        print warning message
        """
        self.stderr_logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        print error message
        """
        self.stderr_logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        print critical message
        """
        self.stderr_logger.critical(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """
        print fatal message
        """
        print str(kwargs)
        if not kwargs:
            self.stderr_logger.fatal(msg, *args, exc_info = True)
        else:
            self.stderr_logger.fatal(msg, *args, **kwargs)

class client_data(object):
    """
    This class defines global client data used for persistence.
    This class has no methods and is meant to be used as a singleton and not instances should be created.
    """
    curr_cmd = ''   # current client command 

    components = {
        QUEMGR : {'conn' : None, 'defer' : True}, 
        SYSMGR : {'conn' : None, 'defer' : True},
        SCHMGR : {'conn' : None, 'defer' : True}, 
        SLPMGR : {'conn' : None, 'defer' : True} }

def print_usage(parser, errmsg = "No arguments or options provided"):
    """
    Will print the usage and a specified error message if provided
    """
    parser.parser.print_usage()
    if errmsg is not None:
        logger.error(errmsg+'\n')

def component_call(comp_name, defer, func_name, args, exit_on_error = True):
    """
    This function is calls a function on another component and handle XML RPC faults
    gracefully, and other faults with something other than a traceback.
    The default is to EXIT ON ERROR.

    If exit_on_error is False then this function will raise and log only when debug level is set.
    """

    def component_error(msg, *args, **kwargs):
        """
        Common component_call error handling
        """
        errmsg    = 'component error: ' + msg
        if exit_on_error:
            logger.error(errmsg, *args, **kwargs)
            sys.exit(1)
        logger.debug(errmsg, *args, **kwargs)
        raise
        
    debug_msg = 'component: "%s.%s", defer: %s\n  %s(\n' % (comp_name, func_name, str(defer), func_name)

    for arg in args:
        debug_msg += '     %s,\n' % (str(arg),)
    debug_msg += '     )\n\n'
    logger.debug(debug_msg)

    if client_data.components[comp_name]['conn'] is None or \
       client_data.components[comp_name]['defer'] != defer:
        try:
            comp = ComponentProxy(comp_name, defer = defer)
        except ComponentLookupError:
            component_error("Failed to connect to %s\n", comp_name)
        except Exception, e:
            component_error("Following exception occured in %s: %s\n", comp_name, e)

        client_data.components[comp_name]['conn']  = comp
        client_data.components[comp_name]['defer'] = defer
    else:
        comp = client_data.components[comp_name]['conn']

    retVal = None
    try:
        func = getattr(comp,func_name)
        retVal = func(*args)
    except xmlrpclib.Fault, fault:
        component_error("XMLRPC failure %s in %s.%s\n", fault, comp_name, func_name)
    except Exception, e:
        component_error("Following exception occured while trying to execute %s.%s: %s\n", comp_name, func_name, e)

    return retVal

def run_jobs(jobs,location,user):
    """
    run jobs
    """
    part_list = component_call(SYSMGR, True, 'get_partitions', ([{'name': location}],))
    if len(part_list) != 1:
        logger.error("cannot find partition named '%s'" % location)
        sys.exit(1)
    return component_call(QUEMGR, True, 'run_jobs', (jobs, location.split(':'), user))

def add_queues(jobs,parser,user,info):
    """
    add queues
    """
    existing_queues = component_call(QUEMGR, True, 'get_queues', (info,))
    if [qname for qname in parser.args if qname in
        [q.get('name') for q in existing_queues]]:
        logger.error('queue already exists')
        sys.exit(1)
    elif len(parser.args) < 1:
        logger.error('Must specify queue name')
        sys.exit(1)
    response = component_call(QUEMGR, True, 'add_queues', (jobs, user))
    datatoprint = [('Added Queues', )] + [(q.get('name'), ) for q in response]
    print_tabular(datatoprint)
    return response

def del_queues(jobs,force,user):
    """
    delete queue
    """
    response = []
    
    response = component_call(QUEMGR, True, 'del_queues',(jobs, force, user))
    datatoprint = [('Deleted Queues', )] + \
                  [(q.get('name'), ) for q in response]
    print_tabular(datatoprint)
    return response

def set_scores(score, jobids, user):
    """
    reset the score of a job to zero to defer it.
    """
    specs = [{'jobid':jobid} for jobid in jobids]

    response = component_call(QUEMGR, True, 'adjust_job_scores', (specs, str(score), user))

    if not response:
        logger.info("no jobs matched")
    else:
        dumb = [str(_id) for _id in response]
        logger.info("updating scores for jobs: %s" % ", ".join(dumb))

def get_cp_option(section, option):
    """
    get a config parser option from the config parser 
    """
    try:
        CP = read_config()
        opt = CP.get(section, option)
    except ConfigParser.NoOptionError:
        opt = None
    except ConfigParser.NoSectionError:
        logger.error("No section %s in Cobalt config" % section)
        sys.exit(1)
    except:
        logger.error("Unknown error when getting config option")
        sys.exit(1)
    return opt

def get_cqm_option(cqm_option):
    """
    get a cqm option from the config parser 
    """
    cqm_opt = get_cp_option('cqm', cqm_option)
    return cqm_opt.split(":") if cqm_opt else None

class header_info(object):
    """
    Class to organize the header type information
    """
    # define headers, long_header is used to query the queue-manager
    default_header = ['JobID','User','WallTime','Nodes','State','Location']

    full_header = ['JobID','JobName','User','WallTime','QueuedTime','RunTime','TimeRemaining','Nodes','State',
                   'Location','Mode','Procs','Preemptable','Queue','StartTime','Index']

    long_header = ['JobID','JobName','User','WallTime','QueuedTime','RunTime','TimeRemaining','Nodes','State',
                   'Location','Mode','Procs','Preemptable','User_Hold','Admin_Hold','Queue','StartTime','Index',
                   'SubmitTime','Path','OutputDir','ErrorPath','OutputPath','Envs','Command','Args','Kernel',
                   'KernelOptions', 'ION_Kernel', 'ION_KernelOptions', 'Project','Dependencies','short_state','Notify','Score','Maxtasktime','attrs',
                   'dep_frac','user_list','Geometry']

    custom_header      = None
    custom_header_full = None

    header  = None

    def __init__(self,parser):
        """
        Get header information 
        """
        # check for custom header, first in cobalt.conf, env, then in --header
        self.custom_header      = get_cqm_option('cqstat_header')
        self.custom_header_full = get_cqm_option('cqstat_header_full')

        if 'CQSTAT_HEADER' in os.environ.keys():
            self.custom_header = os.environ['CQSTAT_HEADER'].split(':')
        elif 'QSTAT_HEADER' in os.environ.keys():
            self.custom_header = os.environ['QSTAT_HEADER'].split(':')
        if 'CQSTAT_HEADER_FULL' in os.environ.keys():
            self.custom_header_full = os.environ['CQSTAT_HEADER_FULL'].split(':')
        elif 'QSTAT_HEADER_FULL' in os.environ.keys():
            self.custom_header_full = os.environ['QSTAT_HEADER_FULL'].split(':')

        if parser.options.header != None:
            self.custom_header = parser.options.header

        if parser.options.Q != None:
            self.header = ['Name','Users','Groups','MinTime','MaxTime','MaxRunning',
                           'MaxQueued','MaxUserNodes','MaxNodeHours','TotalNodes','State']
        elif parser.options.full != None and parser.options.long != None:
            self.header = self.long_header
        elif parser.options.full and self.custom_header_full != None:
            self.header = self.custom_header_full
        elif parser.options.full and parser.options.long == None:
            self.header = self.full_header
        elif self.custom_header != None:
            self.header = self.custom_header
        else:
            self.header = self.default_header

def sleep(t):
    """
    Wrap the Util sleep function
    """
    Cobalt.Util.sleep(t)

def sec_to_str(t):
    """
    sec_to_str abstract the util verion incase we want to modify it.
    """
    return Cobalt.Util.sec_to_str(t)

def get_timeformat(runtime, dayf = False):
    """
    Return the seconds into time format
    """
    days = 0
    minutes, seconds = divmod(runtime, 60)
    hours, minutes   = divmod(minutes, 60)
    if dayf:
        days, hours      = divmod(hours,24)
    if days < 1:
        ret = ( "%02d:%02d:%02d" % (hours, minutes, seconds) )
    else:
        ret = ( "%dd %02d:%02d:%02d" % (days, hours, minutes, seconds))
    return ret

def get_elapsed_time(starttime, endtime, dayf = False):
    """
    returns hh:mm:ss elapsed time string from start and end timestamps
    """
    runtime = endtime - starttime
    return get_timeformat(runtime, dayf)

def print_tabular(rows):
    """
    print tabular abstract the util verion incase we want to modify it.
    """
    Cobalt.Util.print_tabular(rows)

def printTabular(rows, centered = None, with_header_info=True):
    """
    print tabular abstract the util verion incase we want to modify it.
    """
    _centered = [] if centered is None else centered
    Cobalt.Util.printTabular(rows, _centered, with_header_info)

def print_vertical(rows):
    """
    print veritical abstract the util verion incase we want to modify it.
    """
    Cobalt.Util.print_vertical(rows)

def merge_nodelist(nodelist):
    """
    merge nodelist abstract the util verion incase we want to modify it.
    """
    return Cobalt.Util.merge_nodelist(nodelist)

def validate_jobid_args(parser):
    """
    Validate jobids command line arguments.
    """
    if parser.no_args():
        print_usage(parser, "No Jobid(s) given")
        sys.exit(1)

    # get jobids from the argument list
    jobids = get_jobids(parser.args)

    return jobids

def hold_release_command(doc_str,rev_str,ver_str):
    """
    This function is used by qrls and qhold commands to release or hold jobs.
    """
    # setup logging for client 
    setup_logging(logging.INFO)

    # no other commands other than qhold and qrls can used this function
    if client_data.curr_cmd != 'qrls' and client_data.curr_cmd != 'qhold':
        logger.error('This function only works for "qhold" and "qrls" commands')
        sys.exit(1)

    # list of callback with its arguments
    callbacks = [ [ cb_debug, () ] ]

    # Get the version information
    opt_def =  doc_str.replace('__revision__',rev_str)
    opt_def =  opt_def.replace('__version__',ver_str)

    parser = ArgParse(opt_def,callbacks)

    user = getuid()

    # Set required default values: None

    parser.parse_it() # parse the command line

    all_jobs       = validate_jobid_args(parser)
    check_specs    = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':'*'} for jobid in all_jobs]
    check_response = component_call(QUEMGR, False, 'get_jobs', (check_specs,))
    jobs_existed   = [j.get('jobid') for j in check_response]
    all_jobs       = all_jobs.union(set(jobs_existed))
    update_specs   = [{'tag':'job', 'user':user, 'jobid':jobid, 'user_hold':"*", 'is_active':"*"} for jobid in jobs_existed]

    if client_data.curr_cmd == 'qhold':
        updates = {'user_hold':True}
    elif client_data.curr_cmd == 'qrls':
        if parser.options.deps != None:
            updates = {'all_dependencies': []}
        else:
            updates = {'user_hold':False}

    update_response = component_call(QUEMGR, False, 'set_jobs', (update_specs,updates,user))

    if client_data.curr_cmd == 'qrls':
        if parser.options.deps != None:
            logger.info("   Removed dependencies from jobs: ")
            for j in update_response:
                logger.info("      %s" % j.get("jobid"))
            return # We are done exit

    jobs_found     = [j.get('jobid') for j in update_response]
    jobs_not_found = list(all_jobs.difference(set(jobs_existed)))

    jobs_completed = [j.get('jobid') for j in update_response if j.get('has_completed')] + \
        list(set(jobs_existed).difference(set(jobs_found)))

    jobs_had_hold    = [j.get('jobid') for j in check_response if j.get('user_hold') and j.get('jobid') in jobs_found]
    jobs_active      = [j.get('jobid') for j in update_response if j.get('is_active')]

    # Initialize the following list as empty. The ones needed will not be empty after the following logic executes.
    pending_holds        = []
    jobs_no_hold         = []
    jobs_no_pending_hold = []

    if client_data.curr_cmd == 'qhold':

        pending_holds    = [j.get('jobid') for j in update_response if j.get('user_hold') and j.get('is_active')]
        unknown_failures = [j.get('jobid') for j in update_response if not j.get('user_hold') and 
                            j.get('jobid') not in jobs_completed + jobs_had_hold + jobs_active]

        # new holds and failed holds
        new_stuff    = [j.get('jobid') for j in update_response if j.get('user_hold') and j.get('jobid') not in jobs_had_hold]
        failed_stuff = list(all_jobs.difference(set(new_stuff)))
        msg_str1     = "Placed user hold on jobs: "
        msg_str2     = "   Failed to place user hold on jobs: "
        msg_str3     = "to place the 'user hold'"

    elif client_data.curr_cmd == 'qrls':

        jobs_no_hold         = list(set(jobs_found).difference(set(jobs_had_hold)))
        jobs_no_pending_hold = list(set(jobs_no_hold).intersection(set(jobs_active)))
        unknown_failures     = [j.get('jobid') for j in update_response if j.get('user_hold') and
                                j.get('jobid') not in jobs_completed + jobs_no_pending_hold + jobs_active]

        new_stuff    = [j.get('jobid') for j in update_response if not j.get('user_hold') and j.get('jobid') in jobs_had_hold]
        failed_stuff = list(all_jobs.difference(set(new_stuff)))
        msg_str1     = "   Removed user hold on jobs: "
        msg_str2     = "   Failed to remove user hold on jobs: "
        msg_str3     = "to release the 'user hold'"
        
        # set this back to a empty list so it does not get used 
        jobs_had_hold = []


    if not check_response and not update_response:
        logger.error("   No jobs found.")
        logger.error("Failed to match any jobs")
    else:
        logger.debug("Response: %s" % (update_response,))

    if len(failed_stuff) > 0:

        logger.info(msg_str2)

        for jobid in failed_stuff:

            if jobid in jobs_not_found:
                logger.info("      job %s not found" % (jobid,))

            elif jobid in jobs_completed:
                logger.info("      job %s has already completed" % (jobid,))

            elif jobid in jobs_had_hold:
                if jobid in pending_holds:
                    logger.info("      job %s already has a pending 'user hold'" % (jobid,))
                else:
                    logger.info("      job %s already in state 'user hold'" % (jobid,))

            elif jobid in jobs_no_pending_hold:
                logger.info("      job %s is already active and does not have a pending 'user hold'" % (jobid,))

            elif jobid in jobs_active:
                logger.info("      job %s is already active" % (jobid,))

            elif jobid in jobs_no_hold:
                logger.info("      job %s does not have a 'user hold'" % (jobid,))

            elif jobid in unknown_failures:
                logger.info("      job %s encountered an unexpected problem while attempting %s" % (jobid,msg_str3))

            else:
                logger.error("job %s not properly categorized" % (jobid,))
                sys.exit(1)

    if len(new_stuff) > 0:
        logger.info(msg_str1)
        for jobid in new_stuff:
            if client_data.curr_cmd == 'qhold':
                if jobid in pending_holds:
                    logger.info("      %s (pending)" % (jobid,))
                else:
                    logger.info("      %s" % (jobid,))
            else:
                logger.info("      %s" % (jobid,))


def get_options(spec,opts,opt2spec,parser):
    """
    Get the parser values and store them in opts and spec
    """
    # keep track of how many options the user specified
    opt_count = 0

    # opts defaults. these will not be put into spec
    opts['version'] = False
    opts['debug']   = False

    destdic = {} # keep track of options that point to the same destination string

    if client_data.curr_cmd == 'qsub':
        opts['forcenoval'] = False # not used at all, but assign it for old qsub

    # go through all the options
    for optstr, deststr, optval in parser:
        if optstr == 'help': continue # skip this option
        if optstr == 'debug':
            if optval != None: opts[optstr] = True
            continue # do not assign it to spec dictionary

        if optval != None: # Option in command line or has default value

            # opts already been assigned in a callback function or elsewhere, so do not overwrite
            if optstr not in opts: 
                opts[optstr]  = optval

            skip_list = ['verbose','version', 'force','res_id','cycle_id','force_id','modify_res']

            if (deststr not in destdic) and (optstr not in skip_list):
                spec[deststr]     = optval
                destdic[deststr]  = True
                opt_count        += 1

        else: # Option not in command line

            # need the default specified in spec for these options (qsub)
            if optstr in ['queue', 'kernel', 'ion_kernel', 'cwd'] and client_data.curr_cmd == 'qsub':
                opts[optstr] = spec[deststr]

            # for option attrs the default is an empty dictionary (qsub, qalter)
            elif optstr == 'attrs' and client_data.curr_cmd in ['qsub','qalter']: 
                opts[optstr] = {}

            # no option in the command line so assign opts to false
            else:
                opts[optstr] = False

        # opts to job spec keys
        opt2spec[optstr] = deststr

    return opt_count

def getuid():
    """
    Get current user id 
    """
    user = pwd.getpwuid(os.getuid())[0] 
    return user

def getcwd():
    """
    Get current working directory
    """
    return os.getcwd()

def getpath():
    """
    Get the environment variable PATH
    """
    return os.environ['PATH']

def setumask(umask):
    """
    This function will setup logging
    """
    # set umask
    os.umask(umask)

def setup_logging(level):
    """
    Will setup standard logging for the current client.
    """
    global logger

    if hasattr(logger, 'already_setup'):
        return

    logger               = Logger(level)
    logger.already_setup = True
    client_data.curr_cmd = os.path.split(sys.argv[0])[1].replace('.py','')

def read_config():
    """
    This function will read the Cobalt Config files
    """
    CP = ConfigParser.ConfigParser()
    CP.read(Cobalt.CONFIG_FILES)
    return CP

def validate_geometry(geometry,nodes):
    """
    This will validate the geometry for the specified job
    """
    try:
        Cobalt.Util.validate_geometry(geometry, nodes)
    except JobValidationError as err:
        logger.error(err.message)
        logger.error( "Jobs not altered.")
        sys.exit(1)
    except:
        logger.error("Invalid Geometry")
        sys.exit(1)

def system_info():
    """
    This function will return the system and and job types information
    """
    try:
        CP = read_config()
        sys_type = CP.get('bgsystem', 'bgtype')
    except:
        sys_type = 'bgl'
    
    if sys_type == 'bgp':
        job_types = ['smp', 'co', 'dual', 'vn', 'script']
    if sys_type == 'bgq':
        job_types = ['c1', 'c2', 'c4', 'c8', 'c16', 'c32', 'c64', 'script', 'interactive']
    else:
        job_types = ['co', 'vn', 'script', 'interactive']
    return (sys_type,job_types)

def get_jobids(args):
    """
    This function will return the list of jobids in the argument list
    """
    jobids = set()
    for i in range(len(args)):
        if args[i] == '*':
            jobid = args[i]
            continue
        try:
            jobid = int(args[i])
        except:
            logger.error("jobid must be an integer: %s",str(args[i]))
            sys.exit(1)
        jobids.add(jobid)
    return jobids

def get_filters():
    """
    This function current filters
    """
    filters = get_cqm_option('filters')
    if filters == None:
        filters = []
    return filters

def process_filters(filters, spec):
    """
    Process the specified filters to spec
    """
    for filt in filters:
        try:
            Cobalt.Util.processfilter(filt, spec)
        except Exception, e:
            logger.error("Filter failure: please contact Administrator: %s: %s", e, filt)
            sys.exit(1)

def validate_conflicting_options(parser, option_lists):
    """
    This function will validate that the list of passed options are mutually exclusive
    """
    errmsg = [] # init error msessage to empty string
    for mutex_option_list in option_lists:
        optc  = 0
        for mutex_option in mutex_option_list:
            if getattr(parser.options, mutex_option) != None:
                errmsg.append(mutex_option)
                optc += 1
        if optc > 1:
            errmsg = 'Option combinations not allowed with: %s option(s)' % ", ".join(errmsg[1:])
            logger.error(errmsg)
            sys.exit(1)

def parse_datetime(datetime_str):
    """
    wrapper for Util.parse_datetime
    """
    return Cobalt.Util.parse_datetime(datetime_str)

def cobalt_date(date):
    """
    Convert date to Cobalt format
    """
    return time.strftime('%Y_%m_%d-%H:%M', date)

def boot_block(block, user, jobid, resid=None):
    """
    utility to boot specified block.  This is always doing this on behalf of a process outside of Cobalt's server components.
    """
    #set a timeout pull from config file.  Default will be 5 mintues after termination.
    Cobalt.Util.init_cobalt_config()
    timeout = int(Cobalt.Util.get_config_option('bgsystem', 'terminal_boot_timeout' , 300))

    success = component_call(SYSMGR, False, 'initiate_proxy_boot', (block, user, jobid, resid, timeout), False)
    if not success:
        logger.error("Boot request for block %s failed authorization." % (block, ))
        return AUTH_FAIL
    #give the system component a moment to initiate the boot
    sleep(3)
    #wait for block to boot
    failed = SUCCESS
    found = False
    while True:
        boot_id, status, status_strings = component_call(SYSMGR, False, 'get_boot_statuses_and_strings', (block,))
        if not found:
            if boot_id != None:
                found = True
        else:
            if status_strings != [] and status_strings != None:
                print "\n".join(status_strings)
            if status in ['complete', 'failed']:
                component_call(SYSMGR, False, 'reap_boot', (block,))
                if status == 'failed':
                    failed = GENERAL_FAIL
                break
        sleep(1)
    if failed:
        logger.error("Boot for location %s failed."% (block,))
    else:
        logger.info("Boot for location %s complete."% (block,))
    return failed

#
# Callback fucntions for argument parsing defined below
#

def cb_debug(option, opt_str, value, parser, *args):
    """
    Set debug mode for logging
    """
    logger.setLevel(logging.DEBUG)

    # log the command line arguments for the current command
    cmdinfo = os.path.split(sys.argv[0])
    args    = '\n'+cmdinfo[1] + ' ' + ' '.join(sys.argv[1:])+'\n'
    logger.debug(args)

    setattr(parser.values, option.dest, True) # set the option

def cb_nodes(option, opt_str, value, parser, *args):
    """
    This callback will validate value is greater than zero and store it.
    """
    type_int = args[0]
    try:
        CP = read_config()
        sys_size = int(CP.get('system', 'size'))
    except:
        sys_size = 1024
    if not 0 < value <= sys_size:
        logger.error("node count out of realistic range")
        sys.exit(1)

    if type_int:
        _value = value
    else:
        _value = str(value)
    setattr(parser.values,option.dest,_value) # set the option

def cb_gtzero(option,opt_str,value,parser,*args):
    """
    Validate the value entered is greater than zero
    """
    type_int = args[0]
    if value <= 0:
        logger.error(opt_str + " is " + str(value) + " which is greater <= to zero")
        sys.exit(1)

    if type_int:
        _value = value
    else:
        _value = str(value)
    setattr(parser.values,option.dest,_value) # set the option



def cb_score(option, opt_str, value, parser, *args):
    """
    Validate the value entered is greater than zero
    """
    try:
        _value = float(value)
    except:
        logger.error('%s is %s which is not number value' % (opt_str,value))
        sys.exit(1)
    setattr(parser.values,option.dest,str(value)) # set the option

def cb_time(option,opt_str,value,parser,*args):
    """
    This callback will validate the time convert it to minutes and store it.
    """
    dt_allowed = args[0] # delta time flag
    seconds    = args[1] # convert to seconds if true
    type_int   = args[2] # return int
    _time      = value

    # default the flags to false
    if value[0] in ['+','-'] and dt_allowed:
        _time = value[1:]
        parser.__timeop__ = value[0]
            
    # ensure time is actually in minutes
    try:
        minutes = Cobalt.Util.get_time(_time)
    except Cobalt.Exceptions.TimeFormatError, e:
        logger.error("invalid time specification: %s" % e.args[0])
        sys.exit(1)

    if seconds:
        _time = 60*minutes
    else:
        _time = minutes

    if not type_int:
        _time = str(_time)

    setattr(parser.values, option.dest, _time) # set the option

def cb_umask(option,opt_str,value,parser,*args):
    """
    Convert the umask octal string value to int
    """
    try:
        um = int(value,8)
    except:
        logger.error("Invalid umask value %s",value)
        sys.exit(1)
    setattr(parser.values,option.dest,um) # set the option

def _check_dependencies(dependency_string):

    if dependency_string.lower() == 'none':
        #we are removing all job dependencies.
        logger.info("Removing job dependencies")
        return

    deps = set(dependency_string.split(":"))
    
    query = []
    for dep in deps:
        try:
            query.append({"jobid": int(dep)})
        except:
            pass
    
    jobs = component_call(QUEMGR, True, 'get_jobs', (query,))
    
    job_ids = set( [str(j["jobid"]) for j in jobs] )
    
    missing = deps.difference(job_ids)
    
    if missing:
        logger.error("WARNING: dependencies %s do not match jobs currently in the queue" % ":".join(missing))

def cb_upd_dep(option,opt_str,value,parser,*args):
    """
    check and update dependencies
    """
    _check_dependencies(value)
    deps = value.split(":")
    if deps[0].lower() == "none":
        deps = []
    setattr(parser.values,option.dest,deps) # set the option 

def cb_dep(option,opt_str,value,parser,*args):
    """
    check and set dependencies.
    """
    _check_dependencies(value)
    setattr(parser.values,option.dest,value) # set the option 

def cb_split(option,opt_str,value,parser,*args):
    """
    split string according to passed delimiter
    """
    delim = args[0] # delimiter to use for splitting the string value
    split_value = [field for field in value.split(delim)]

    setattr(parser.values,option.dest,split_value) # set the option 

def cb_env(option,opt_str,value,parser,*args):
    """
    This callback will validate the env variables and store them.
    """
    opts   = args[0]
    _env   = {}
    _value = value.replace(ESC_COL, COL_TAG).replace(ESC_EQL, EQL_TAG)
    key_value_pairs = [item.split('=', 1) for item in re.split(r':(?=\w+\b=)', _value)]
    for kv in key_value_pairs:
        if len(kv) != 2:
            logger.error( "Improperly formatted argument to env : %r" % kv)
            sys.exit(1)
    for key, val in key_value_pairs:
        _env.update({key:val.replace(COL_TAG,':').replace(EQL_TAG,'=')})
    
    setattr(parser.values,option.dest,_env) # set the option
    opts['env'] = value
 
def cb_path(option,opt_str,value,parser,*args):
    """
    This callback will validate the path and store it.
    """
    opts     = args[0]
    use_cwd  = args[1]
    _path = value
    if not _path.startswith('/') and use_cwd:
        _path = CWD_TAG + '/' + value
    else:
        # validate the path
        if not os.path.isdir(os.path.dirname(_path)):
            logger.error("directory %s does not exist" % _path)
            sys.exit(1)
    setattr(parser.values,option.dest,_path) # set the option
    optstr = option.get_opt_string().replace('-','')
    opts[optstr] = value

def cb_geometry(option,opt_str,value,parser,*args):
    """
    This callback will validate the geometry value and store it
    """
    opts = args[0]
    try:
        geom_str = ''
        geom_str = parse_geometry_string(value)
    except:
        logger.error("Invalid geometry entered: %s" % geom_str)
        sys.exit(1)
    setattr(parser.values,option.dest,geom_str) # set the option
    opts[option.dest] = value

def cb_bgq_geo(option,opt_str,value,parser,*args):
    """
    This callback will validate the bgq geometry value and store it
    """
    geo_list = None
    match = Cobalt.Util.bgq_node_geo_re.match(value)
    if match == None:
        logger.error("Invalid Geometry. Geometry must be in the form of AxBxCxDxE")
        sys.exit(1)
    geo_list = [int(nodect) for nodect in match.groups()]
    setattr(parser.values,option.dest,geo_list)

def cb_attrs(option,opt_str,value,parser,*args):
    """
    This callback will validate the attributes specified and store them.
    """
    _val = getattr(parser.values,option.dest)
    if _val != None:
        logger.error("Multiple --attrs options not supported.  Specify multiple attributes as follows: --attrs FOO=1:BAR=2")
        sys.exit(1)

    newoptsattrs = {}
    for attr in value.split(":"):
        if len(attr.split("=")) == 2:
            key, value = attr.split("=")
            newoptsattrs.update({key:value})
        elif len(attr.split("=")) == 1:
            if attr[:3] == "no_":
                newoptsattrs.update({attr[3:]:"false"})
            else:
                newoptsattrs.update({attr:"true"})
        else:
            logger.error( "Improperly formatted argument to attrs : %s" % attr)
            sys.exit(1)
    setattr(parser.values,option.dest,newoptsattrs) # set the option

def _validate_users(users):
    """
    This function will validate the user list
    """
    user_list = [auth_user for auth_user in users.split(':')]  
    for auth_user in user_list:
        try:
            pwd.getpwnam(auth_user)
        except KeyError:
            logger.error("user %s does not exist." % auth_user)
            sys.exit(1)
        except Exception, e:
            logger.error("UNKNOWN FAILURE: user %s." % (auth_user,),e)
            sys.exit(1)
    return user_list
    
def cb_user_list(option, opt_str, value, parser, *args):
    """
    This callback will validate the user list and store it.
    """
    opts = args[0] 
    user = getuid()
    user_list = _validate_users(value)
    if user not in user_list:
        user_list.insert(0, user)
    setattr(parser.values,option.dest,user_list)
    opts[option.dest] = value
    
def cb_res_users(option, opt_str, value, parser, *args):
    """
    This callback will validate resevation users list and store it.
    """
    if value != '*':
        _validate_users(value)
    users = value
    setattr(parser.values, option.dest, users)
    
def _set_mode(option, opt_str, value, parser, *args):
    """
    check mode
    """
    (sys_type,job_types) = system_info()

    if parser.values.mode is not None:
        if parser.values.mode != value:
            logger.error("Mode already set to '%s' and trying to set it again to '%s'", parser.values.mode, value)
            sys.exit(1)
        return

    mode = value

    if mode not in job_types:
        logger.error("Specifed mode '%s' not valid, valid modes are\n%s" % (mode, "\n".join(job_types)))
        sys.exit(1)
    if mode == 'co' and sys_type == 'bgp':
        mode = 'SMP'
    setattr(parser.values, 'mode', mode) # set the option

def cb_interactive(option, opt_str, value, parser, *args):
    """
    Callback to handle interactive mode
    """
    _set_mode(option, opt_str, 'interactive', parser, *args)

def cb_mode(option, opt_str, value, parser, *args):
    """
    This callback will validate an store the system mode.
    """
    _set_mode(option, opt_str, value, parser, *args)

def cb_cwd(option,opt_str,value,parser,*args):
    """
    validate current working directory
    """
    if not os.path.isdir(value):
        logger.error("dir '%s' is not a directory" % value)
        sys.exit(1)
    setattr(parser.values,option.dest,value)

def cb_setqueues(option,opt_str,value,parser,*args):
    """
    get the set queue data from specified option
    """
    optstr = opt_str.replace('-','')
    #  only one set queue option is allowed at a time
    if hasattr(parser.values,'setq_opt'):
        prev_opt = parser.values.setq_opt
        logger.error('Only one option that sets queue data is allowed: options %s and %s encountered' % 
                     (prev_opt,optstr))
        sys.exit(1)

    if optstr == 'stopq':
        qdata = {'state':'stopped'}
    elif optstr == 'startq':
        qdata = {'state':'running'}
    elif optstr == 'drainq':
        qdata = {'state':'draining'}
    elif optstr == 'killq':
        qdata = {'state':'dead'}
    elif optstr == 'policy':
        qdata = {'policy':value}
    elif optstr == 'unsetq':
        qdata = {}
        for prop in value.split(' '):
            qdata[prop.lower()] = None
    elif optstr == 'setq':
        props = [p.split('=') for p in value.split(' ')]
        for p in props:
            if len(p) != 2:
                logger.error("Improperly formatted argument to setq : %r" % p)
                sys.exit(1)
        qdata = {}
        for prop, val in props:
            if prop.lower() in ['maxtime', 'mintime']:
                if val.count(':') in [0, 2]:
                    t = val.split(':')
                    for i in t:
                        try:
                            if i != '*':
                                dummy = int(i)
                        except:
                            logger.error(prop + ' value is not a number')
                            sys.exit(1)
                    if val.count(':') == 2:
                        t = val.split(':')
                        val = str(int(t[0])*60 + int(t[1]))
                    elif val.count(':') == 0:
                        pass
                else:
                    logger.error('Time for ' + prop + ' is not valid, must be in hh:mm:ss or mm format')
                    sys.exit(1)
            qdata.update({prop.lower():val})
    parser.values.qdata    = qdata
    parser.values.setq_opt = optstr


def _setbool_attr(parser, opt_str, attr, true_opt_list):
    """
    Set the specified attr to true if opt string in the true option list.
    Will generate an error if the attr is already set.
    """
    if hasattr(parser.values,attr):
        val = getattr(parser.values,attr)
        if  val != None:
            logger.error("Attribute %s already set" % attr)
            sys.exit(1)
    if opt_str in true_opt_list:
        setattr(parser.values,attr,True)
    else:
        setattr(parser.values,attr,False)

def cb_hold(option,opt_str,value,parser,*args):
    """
    handles the (user | admin) hold and release attributes
    """
    hold_str = 'admin_hold'

    if opt_str.find('user') != -1:
        hold_str = 'user_hold'

    elif opt_str.find('admin') == -1:
        cp_opt = get_cp_option('client', 'allow_cqadm_hold_and_release_options')
        if cp_opt is None:
            allow = False
        else:
            allow = True if cp_opt.lower() == 'true' else False

        if not allow:
            logger.error('Options --hold and --release have been deprecated')
            sys.exit(1)

    _setbool_attr(parser, opt_str, hold_str, ['--hold', '--user-hold', '--admin-hold'])

def cb_passthrough(option,opt_str,value,parser,*args):
    """
    handles the block_passthrough attribute
    """
    _setbool_attr(parser,opt_str,'block_passthrough',['--block_passthrough'])

        
def cb_date(option,opt_str,value,parser,*args):
    """
    parse date
    """
    try:
        _value     = value
        if args is not ():
            if _value.lower() == 'now':
                allow_now = args[0]
                if not allow_now: 
                    raise
                _value = cobalt_date(time.localtime(time.time()))

        starttime = parse_datetime(_value)
        logger.info("Got starttime %s" % (sec_to_str(starttime)))

    except Exception, e:
        logger.error("start time '%s. Error: %s' is invalid", value, e)
        logger.error("start time is expected to be in the format: YYYY_MM_DD-HH:MM")
        sys.exit(1)
    setattr(parser.values,option.dest,starttime)

def cluster_display_node_info():
    '''fetch informaion for display in nodeadm and nodelist for cluster systems.

    returns:
    header - headers to print out for display
    output - data to be displayed about nodes on a cluster system

    '''

    statuses = component_call(SYSMGR, False, 'get_node_status', ())
    queue_data = component_call(SYSMGR, False, 'get_queue_assignments', ())
    end_times_to_nodes = component_call(SYSMGR, False, 'get_backfill_windows', ())
    reservations = component_call(SCHMGR, False, 'get_reservations', ([{'queue':'*', 'partitions':'*', 'active':True}],))

    header = [['Host', 'Queue', 'State', 'Backfill']]
    #build output list
    output = []
    for status in statuses:
        host_name = status[0]
        status = status[1]
        queues = []
        backfill_time = '-'
        for queue in queue_data:
            if host_name in queue_data[queue]:
                queues.append(queue)
        queues.sort()
        for res in reservations:
            if host_name in res['partitions'].split(':'):
                if res['queue'] not in queues:
                    queues.append(res['queue'])
        now = int(time.time()) #This comes back as a float in python
        for end_time in end_times_to_nodes:
            if int(end_time) == 0 or status != 'idle':
                pass
            elif host_name in end_times_to_nodes[end_time]:
                raw_backfill_time = max(0, int(end_time) - now)
                if raw_backfill_time <= 0:
                    backfill_time = "00:00:00"
                else:
                    backfill_time = "%02d:%02d:%02d" % (raw_backfill_time / 3600, (raw_backfill_time % 3600) / 60,
                            raw_backfill_time % 60)
        output.append([host_name, ":".join(queues), status, backfill_time])

    return header, output
