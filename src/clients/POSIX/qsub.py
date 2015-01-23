#!/usr/bin/env python
"""
Submit jobs to the queue manager for execution.

Usage: %prog --help
Usage: %prog [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.

version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-v','--verbose',dest='verbose',help='not used',action='store_true'
'-h','--held',dest='user_hold',help='hold this job once submitted',action='store_true'
'--preemptable',dest='preemptable',help='make this job preemptable',action='store_true'
'--run_project',dest='run_project',help='set run project flag for this job',action='store_true'
'--disable_preboot',dest='script_preboot',help='disable script preboot',action='store_false'
'-I','--interactive',help='run qsub in interactive mode',callback=cb_interactive

Option with values:

'-n','--nodecount',dest='nodes',type='int',help='set job node count',callback=cb_nodes
'--proccount',dest='procs',type='int',help='set job proc count',callback=cb_gtzero
'-A','--project',dest='project',type='string',help='set project name'
'--cwd',dest='cwd',type='string',help='set current working directory'
'-q','--queue',dest='queue',type='string',help='set queue name'
'-M','--notify',dest='notify',type='string',help='set notification email address'
'--env',dest='envs',type='string', help='Set env variables. Refer to man pages for more detail information.', callback=cb_env
'-t','--time',dest='walltime',type='string',help='set walltime (minutes or HH:MM:SS). For max walltime enter 0.',callback=cb_time
'-u','--umask',dest='umask',type='string',help='set umask: octal number default(022)',callback=cb_umask
'-O','--outputprefix',dest='outputprefix',type='string',help='output prefix for error,output or debuglog files',callback=cb_path
'-e','--error',dest='errorpath',type='string',help='set error file path',callback=cb_path
'-o','--output',dest='outputpath',type='string',help='set output file path',callback=cb_path
'-i','--inputfile',dest='inputfile',type='string',help='set input file',callback=cb_path
'--debuglog',dest='cobalt_log_file',type='string',help='set debug log path file',callback=cb_path
'--dependencies',dest='all_dependencies',type='string',help='set job dependencies (jobid1:jobid2:...:jobidN)',callback=cb_dep
'--attrs',dest='attrs',type='string',help='set attributes (attr1=val1:attr2=val2:...:attrN=valN)',callback=cb_attrs
'--user_list','--run_users',dest='user_list',type='string',help='set user list (user1:user2:...:userN)',callback=cb_user_list
'--jobname',dest='jobname',type='string', /
   help='Sets Jobname. If this option is not provided then Jobname will be set to whatever -o option specified.'

The following options are only valid on IBM BlueGene architecture platforms:

'--kernel',dest='kernel',type='string',help='set a compute node kernel profile'
'-K','--kerneloptions',dest='kerneloptions',type='string',help='set compute node kernel options'
'--ion_kernel',dest='ion_kernel',type='string',help='set an IO node kernel profile'
'--ion_kerneloptions',dest='ion_kerneloptions',type='string',help='set IO node kernel options'
'--mode', dest='mode', type='string', help='select system mode',callback=cb_mode
'--geometry', dest='geometry', type='string', help='set geometry (AxBxCxDxE)',callback=cb_geometry

"""
import logging
import time
import string
import os
import sys
import signal
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_env, cb_nodes, cb_time, cb_umask, cb_path, cb_dep, \
    cb_attrs, cb_user_list, cb_geometry, cb_gtzero, cb_mode, cb_interactive
from Cobalt.arg_parser import ArgParse
from Cobalt.Util import get_config_option, init_cobalt_config, sleep
from Cobalt.Proxy import ComponentProxy
import xmlrpclib

__revision__ = '$Revision: 559 $'
__version__  = '$Version$'

#init cobalt config file for setting default kernels.
init_cobalt_config()
SYSMGR           = client_utils.SYSMGR
QUEMGR           = client_utils.QUEMGR
CN_DEFAULT_KERNEL  = get_config_option('bgsystem', 'cn_default_kernel', 'default')
ION_DEFAULT_KERNEL = get_config_option('bgsystem', 'ion_default_kernel', 'default')

def on_interrupt(sig, func=None):
    """
    Interrupt Handler to cleanup the interactive job if the user interrupts
    Will contain two static variables: count and exit.
    'count' will keep track how many interruptions happened and 
    'exit' flags whether we completely exit once the interrupt occurs.
    """
    on_interrupt.count += 1
    if on_interrupt.exit:
        sys.exit(1)

# Initializing on_interrupt static variables
on_interrupt.count = 0
on_interrupt.exit  = True

def exit_on_interrupt():
    """
    Set to exit when interrupt occurs
    """
    on_interrupt.exit = True
    if on_interrupt.count > 0:
        sys.exit(1)

def not_exit_on_interrupt():
    """
    Set to not exit on interrupt
    """
    on_interrupt.exit = False

# Reset sigint and sigterm interrupt handlers to deal with interactive failures
signal.signal(signal.SIGINT, on_interrupt)
signal.signal(signal.SIGTERM, on_interrupt)
signal.signal(signal.SIGQUIT, on_interrupt)
signal.signal(signal.SIGABRT, on_interrupt)
signal.signal(signal.SIGXCPU, on_interrupt)
signal.signal(signal.SIGPIPE, on_interrupt)

def exit_interactive_job(deljob, jobid, user):
    """
    Exit job normally or delete job
    """
    not_exit_on_interrupt()
    # If no jobid assigned yet return
    if not jobid:
        return
    if deljob:
        job_to_del = [{'tag':'job', 'jobid':jobid, 'user':user}]
        client_utils.logger.info("Deleting interactive job %s", str(jobid))
        client_utils.component_call(QUEMGR, False, 'del_jobs', (job_to_del, False, user))
    else:
        client_utils.logger.info("Exiting interactive job %d", int(jobid))
        client_utils.component_call(SYSMGR, False, 'interactive_job_complete', (jobid,))

def validate_args(parser, spec):
    """
    If the argument is a script job it will validate it, and get the Cobalt directives
    """

    #an executable cannot be specified for interactive jobs
    if parser.options.mode == 'interactive' and (not parser.no_args()):
        client_utils.logger.error("An executable may not be specified if using the interactive option.")
        sys.exit(1)
    elif parser.options.mode == 'interactive':
        #Bypass the rest of the checks for interactive jobs.
        return

    # if no excecutable specified then flag it an exit
    if parser.no_args():
        client_utils.print_usage(parser, "No executable or script specified")
        sys.exit(1)

    # Check if it is a valid executable/file
    cmd = parser.args[0].replace(' ','')
    if cmd[0] != '/':
        cmd = spec['cwd'] + '/' + cmd

    if not os.path.isfile(cmd):
        client_utils.logger.error("command %s not found, or is not a file" % cmd)
        sys.exit(1)

    if not os.access(cmd, os.X_OK | os.R_OK):
        client_utils.logger.error("command %s is not executable" % cmd)
        sys.exit(1)

    # if there are any arguments for the specified command store them in spec
    spec['command'] = cmd
    if len(parser.args) > 1:
        spec['args'] = parser.args[1:]
    else:
        spec['args'] = []

    tag         = '#COBALT '
    len_tag     = len(tag)
    fd          = open(cmd, 'r')
    line        = fd.readline()
    reparse    = False
    if line[0:2] == '#!':
        line                = fd.readline()
        new_argv            = []
        while len(line) > len_tag:
            if line[:len_tag] != tag:
                break
            if new_argv == []:
                new_argv = ['--mode','script']
                reparse   = True
            new_argv += line[len_tag:].split()
            line      = fd.readline()
        sys.argv = [sys.argv[0]] + new_argv + sys.argv[1:]
    fd.close()

    # check for multiple --env options specified
    if sys.argv.count('--en') + sys.argv.count('--env') > 1:
        # consolidate the --env options (this will update sys.argv)
        env_union()
        reparse = True

    return reparse

def validate_options(parser, opt_count):
    """
    Validate qsub arguments
    """

    # Check if any required option entered
    if opt_count == 0:
        client_utils.print_usage(parser, "No required options provided")
        sys.exit(1)

    # If no time supplied flag it and exit
    if parser.options.walltime == None:
        client_utils.logger.error("'time' not provided")
        sys.exit(1)

    # If no nodecount give then flag it an exit
    if parser.options.nodes == None:
        client_utils.logger.error("'nodecount' not provided")
        sys.exit(1)

def update_outputprefix(parser,spec):
    """
    Update the the appropriate paths with the outputprefix path
    """
    # If the paths for the error log, output log, or the debuglog are not provided
    # then update them with what is provided in outputprefix.
    if parser.options.outputprefix != None:
        # pop the value for outputrefix
        op = spec.pop('outputprefix')

        # if error path, cobalt log path or output log path not provide then update them wiht outputprefix
        if parser.options.errorpath == None:
            spec['errorpath'] = op + ".error"
        if parser.options.cobalt_log_file == None:
            spec['cobalt_log_file'] = op + ".cobaltlog"
        if parser.options.outputpath == None:
            spec['outputpath'] = op + ".output"

def update_paths(spec):
    """
    This functiojn will update all the paths in spec that need the current working directory.
    """
    for key in spec:
        value = spec[key]
        # if path needs current working directory then
        if type(value) == type(""):
            if value.find(client_utils.CWD_TAG) != -1:
                if 'cwd' in spec:
                    _cwd = spec['cwd']
                else:
                    _cwd = client_utils.getcwd()
                _path = spec[key].replace(client_utils.CWD_TAG,_cwd)
                # validate the path
                if not os.path.isdir(os.path.dirname(_path)):
                    client_utils.logger.error("directory %s does not exist" % _path)
                    sys.exit(1)
                spec[key] = _path

def check_inputfile(parser, spec):
    """
    Verify the input file is an actual file
    """
    if parser.options.inputfile != None:
        if parser.options.mode == 'interactive':
            client_utils.logger.error("Cannot specify an input file for interactive jobs.")
            sys.exit(1)
        inputfile = spec['inputfile']
        if not os.path.isfile(inputfile):
            client_utils.logger.error("file %s not found, or is not a file" % inputfile)
            sys.exit(1)

def update_spec(parser, opts, spec, opt2spec):
    """
    This function will update the appropriate spec values with the opts values
    """
    # Get the key validated values into spec dictionary
    for opt in ['mode', 'proccount', 'nodecount']:
        spec[opt2spec[opt]] = opts[opt]
    
    # Hack until the Cluster Systems get re-written.
    if parser.options.mode == 'interactive' and 'command' in opts and 'args' in opts:
        spec['command'] = opts['command']
        spec['args']    = opts['args']


def logjob(jobid, spec, logToConsole):
    """
    log job info
    """
    # log jobid to stdout
    if jobid:
        if logToConsole:
            client_utils.logger.info(jobid)
        if spec.has_key('cobalt_log_file'):
            filename = spec['cobalt_log_file']
            t = string.Template(filename)
            filename = t.safe_substitute(jobid=jobid)
        else:
            filename = "%s/%s.cobaltlog" % (spec['outputdir'], jobid)

        try:
            cobalt_log_file = open(filename, "a")
            
            print >> cobalt_log_file, "Jobid: %s" % jobid
            print >> cobalt_log_file, "qsub %s" % (" ".join(sys.argv[1:]))
            print >> cobalt_log_file, "%s submitted with cwd set to: %s" % ( client_utils.sec_to_str(time.time()), spec['cwd'])
            cobalt_log_file.close()
        except Exception, e:
            client_utils.logger.error("WARNING: failed to create cobalt log file at: %s: %s", filename, e)
    else:
        client_utils.logger.error("failed to create the job.  Maybe a queue isn't there?")

def env_union():
    """
    Take all env options and their values in sys.argv and make the union of them to create one consolidated --env.
    """
    try:
        ndx = 0
        new_args    = []
        env_values  = []
        env_val_ndx = -1
        skip_next   = False
        for arg in sys.argv:
            if arg == '--en' or arg == '--env':
                env_values.append(sys.argv[ndx+1])
                if env_val_ndx == -1:
                    env_val_ndx = ndx+1
                    new_args.append('--env')
                    new_args.append('<PLACE HOLDER>')
                skip_next = True
            elif not skip_next:
                new_args.append(sys.argv[ndx])
            else:
                skip_next = False
            ndx += 1
        new_args[env_val_ndx] = ':'.join(env_values)
        sys.argv = new_args
    except Exception, e:
        client_utils.logger.error( "No values specified or invalid usage of --env option: %s --> %s", str(sys.argv), e)
        sys.exit(1)

def parse_options(parser, spec, opts, opt2spec, def_spec):
    """
    Will initialize the specs and then parse the command line options
    """
    opts.clear()
    for item in def_spec:
        spec[item] = def_spec[item]

    parser.parse_it() # parse the command line
    opt_count               = client_utils.get_options(spec, opts, opt2spec, parser)
    opts['disable_preboot'] = not spec['script_preboot']
    return opt_count

def run_interactive_job(jobid, user, disable_preboot, nodes, procs):
    """
    This will create the shell or ssh session for user
    """
    not_exit_on_interrupt()
    # save whether we are running on a cluster system
    impl =  client_utils.component_call(SYSMGR, False, 'get_implementation', ())
    exit_on_interrupt()

    deljob = True if impl == "cluster_system" else False

    def start_session(loc, resid, nodes, procs):
        """
        start ssh or shell session
        """
        # Create necesary env vars
        os.putenv("COBALT_NODEFILE", "/var/tmp/cobalt.%s" % (jobid))
        os.putenv("COBALT_JOBID", "%s" % (jobid))
        if resid:
            os.putenv("COBALT_RESID", "%s" % (resid))
        os.putenv("COBALT_PARTNAME", loc)
        os.putenv("COBALT_BLOCKNAME", loc)
        os.putenv("COBALT_JOBSIZE", str(procs))
        os.putenv("COBALT_BLOCKSIZE",str(nodes))
        os.putenv("COBALT_PARTSIZE", str(nodes))
        client_utils.logger.info("Opening interactive session to %s", loc)
        if deljob:
            os.system("/usr/bin/ssh -o \"SendEnv COBALT_NODEFILE COBALT_JOBID\" %s" % (loc))
        else:
            os.system(os.environ['SHELL'])

    # Wait for job to start
    query = [{'tag':'job', 'jobid':jobid, 'location':'*', 'state':"*", 'resid':"*"}]
    client_utils.logger.info("Wait for job %s to start...", str(jobid))

    while True:
        # If we get a ssl timeout error or component lookup error try again
        try:
            not_exit_on_interrupt()
            response =  client_utils.component_call(QUEMGR, False, 'get_jobs', (query, ), False)
            exit_on_interrupt()
            # if jobid not found flag an error and exit
            if not response:
                client_utils.logger.error("Jobid %s not found after submission", str(jobid))
                sys.exit()
        except (xmlrpclib.Fault, ComponentProxy) as fault:
            # This can happen if the component is down so try again
            client_utils.logger.error('Error getting job info: %s. Try again', fault)
            sleep(2)
        state    = response[0]['state']
        location = response[0]['location']
        resid    = response[0]['resid']
        if state == 'running' and location:
            start_session(location[0], resid, nodes, procs)
            break
        client_utils.logger.debug('Current State "%s" for job %s', str(state), str(jobid))
        sleep(2)

    return deljob

def run_job(parser, user, spec, opts):
    """
    run the job
    """
    jobid        = None
    deljob       = True
    exc_occurred = False
    try:
        not_exit_on_interrupt()
        jobs  =  client_utils.component_call(QUEMGR, False, 'add_jobs',([spec],), False)
        jobid = jobs[0]['jobid']
        exit_on_interrupt()

        if parser.options.envs:
            client_utils.logger.debug("Environment Vars: %s", parser.options.envs)

        # If this is an interactive job, wait for it to start, then start user shell
        if parser.options.mode == 'interactive':
            logjob(jobid, spec, False)
            deljob = run_interactive_job(jobid, user,  opts['disable_preboot'], opts['nodecount'], opts['proccount'])
        else:
            logjob(jobid, spec, True)
    except Exception, e:
        client_utils.logger.error(e)
        exc_occurred = True
    finally:
        if parser.options.mode == 'interactive':
            exit_interactive_job(deljob, jobid, user)
        if exc_occurred: 
            sys.exit(1)

def main():
    """
    qsub main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}
    def_spec = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_interactive  , () ),
        ( cb_env          , (opts,) ),
        ( cb_nodes        , (False,) ), # return string
        ( cb_gtzero       , (False,) ), # return string
        ( cb_time         , (False, False, False) ), # no delta time, minutes, return string
        ( cb_umask        , () ),
        ( cb_path         , (opts, True) ), # use CWD
        ( cb_dep          , () ),
        ( cb_attrs        , () ),
        ( cb_mode         , () ),
        ( cb_user_list    , (opts,) ),
        ( cb_geometry     , (opts,) )]

    # Get the version information
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    user = client_utils.getuid()

    def_spec['tag']            = 'job'
    def_spec['user']           = user
    def_spec['outputdir']      = client_utils.CWD_TAG
    def_spec['jobid']          = '*'
    def_spec['path']           = client_utils.getpath()
    def_spec['mode']           = False
    def_spec['cwd']            = client_utils.getcwd()
    def_spec['kernel']         = CN_DEFAULT_KERNEL
    def_spec['ion_kernel']     = ION_DEFAULT_KERNEL
    def_spec['queue']          = 'default'
    def_spec['umask']          = 022
    def_spec['run_project']    = False
    def_spec['user_list']      = [user]
    def_spec['procs']          = False
    def_spec['script_preboot'] = True

    parser    = ArgParse(opt_def, callbacks)
    opt_count = parse_options(parser, spec, opts, opt2spec, def_spec)
    reparse  = validate_args(parser, spec)

    if reparse:
        # re-parse with new sys.argv
        # note: the first parse is necessary to make sure that
        #       the env syntax is correct for every --env option provided
        #       If not parsed prior to the union then the union could result
        #       in a valid syntax, but it would not be what the user would want.
        opt_count = parse_options(parser, spec, opts, opt2spec, def_spec)

    client_utils.setumask(spec['umask'])
    validate_options(parser, opt_count)
    update_outputprefix(parser, spec)
    update_paths(spec)
    check_inputfile(parser, spec)

    not_exit_on_interrupt()
    opts = client_utils.component_call(SYSMGR, False, 'validate_job',(opts,))
    exit_on_interrupt()

    filters = client_utils.get_filters()
    client_utils.process_filters(filters, spec)
    update_spec(parser, opts, spec, opt2spec)

    run_job(parser, user, spec, opts)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, exc:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", exc)
        sys.exit(1)
