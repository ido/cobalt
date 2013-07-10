#!/usr/bin/env python
"""
Submit jobs to the queue manager for execution.

Usage: %prog --help
Usage: %prog [options] <executable> [<excutable options>]
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-v','--verbose',dest='verbose',help='not used',action='store_true'
'-h','--held',dest='user_hold',help='hold this job once submitted',action='store_true'
'--preemptable',dest='preemptable',help='make this job preemptable',action='store_true'
'--run_project',dest='run_project',help='set run project flag for this job',action='store_true'
'--disable_preboot',dest='script_preboot',help='disable script preboot',action='store_false'

Option with values:

'-n','--nodecount',dest='nodes',type='int',help='set job node count',callback=cb_nodes
'--proccount',dest='procs',type='int',help='set job proc count',callback=cb_gtzero
'-A','--project',dest='project',type='string',help='set project name'
'--cwd',dest='cwd',type='string',help='set current working directory'
'-q','--queue',dest='queue',type='string',help='set queue name'
'-M','--notify',dest='notify',type='string',help='set notification email address'
'--env',dest='envs',type='string',help='set env variables (envvar1=val1:envvar2=val2:...:envvarN=valN)',callback=cb_env
'-t','--time',dest='walltime',type='string',help='set walltime (minutes or HH:MM:SS)',callback=cb_time
'-u','--umask',dest='umask',type='string',help='set umask: octal number default(022)',callback=cb_umask
'-O','--outputprefix',dest='outputprefix',type='string',help='output prefix for error,output or debuglog files',callback=cb_path
'-e','--error',dest='errorpath',type='string',help='set error file path',callback=cb_path
'-o','--output',dest='outputpath',type='string',help='set output file path',callback=cb_path
'-i','--inputfile',dest='inputfile',type='string',help='set input file',callback=cb_path
'--debuglog',dest='cobalt_log_file',type='string',help='set debug log path file',callback=cb_path
'--dependencies',dest='all_dependencies',type='string',help='set job dependencies (jobid1:jobid2:...:jobidN)',callback=cb_dep
'--attrs',dest='attrs',type='string',help='set attributes (attr1=val1:attr2=val2:...:attrN=valN)',callback=cb_attrs
'--user_list','--run_users',dest='user_list',type='string',help='set user list (user1:user2:...:userN)',callback=cb_user_list

The following options are only valid on IBM BlueGene architecture platforms:

'--kernel',dest='kernel',type='string',help='set kernel profile'
'-K','--kerneloptions',dest='kerneloptions',type='string',help='set kernel options'
'--mode',dest='mode',type='string',help='select system mode'
'--geometry',dest='geometry',type='string',help='set geometry (AxBxCxDxE)',callback=cb_geometry

"""
import logging
import string
import os
import sys
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_env, cb_nodes, cb_time, cb_umask, cb_path, \
    cb_dep, cb_attrs, cb_user_list, cb_geometry, cb_gtzero
from Cobalt.arg_parser import ArgParse

    
__revision__ = '$Revision: 559 $'
__version__  = '$Version$'

SYSMGR = client_utils.SYSMGR
QUEMGR = client_utils.QUEMGR

def validate_args(parser, spec, opt_count):
    """
    Validate qsub arguments
    """

    # Check if any required option entered
    if opt_count == 0:
        client_utils.print_usage(parser, "No required options provided")
        sys.exit(1)

    # if no excecutable specified then flag it an exit
    if parser.no_args():
        client_utils.print_usage(parser, "No executable specified")
        sys.exit(1)

    # If no time supplied flag it and exit
    if parser.options.walltime == None:
        client_utils.logger.error("'time' not provided")
        sys.exit(1)

    # If no nodecount give then flag it an exit
    if parser.options.nodes == None:
        client_utils.logger.error("'nodecount' not provided")
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

def check_inputfile(parser,spec):
    """
    Verify the input file is an actual file
    """
    if parser.options.inputfile != None:
        inputfile = spec['inputfile']
        if not os.path.isfile(inputfile):
            client_utils.logger.error("file %s not found, or is not a file" % inputfile)
            sys.exit(1)

def update_spec(opts,spec,opt2spec):
    """
    This function will update the appropriate spec values with the opts values
    """
    # Get the key validated values into spec dictionary
    for opt in ['mode','proccount', 'nodecount']:
        spec[opt2spec[opt]] = opts[opt]

def logjob(job,spec):
    """
    log job info
    """
    # log jobid to stdout
    if job:
        client_utils.logger.info(job['jobid'])
        if spec.has_key('cobalt_log_file'):
            filename = spec['cobalt_log_file']
            t = string.Template(filename)
            filename = t.safe_substitute(jobid=job['jobid'])
        else:
            filename = "%s/%s.cobaltlog" % (spec['outputdir'], job['jobid'])

        try:
            cobalt_log_file = open(filename, "a")
            print >> cobalt_log_file, "%s\n" % (" ".join(sys.argv))
            print >> cobalt_log_file, "submitted with cwd set to: %s\n" % spec['cwd']
            cobalt_log_file.close()
        except Exception, e:
            client_utils.logger.error("WARNING: failed to create cobalt log file at: %s" % filename)
            client_utils.logger.error("         %s" % e.strerror)
    else:
        client_utils.logger.error("failed to create the job.  Maybe a queue isn't there?")

def main():
    """
    qsub main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)
    
    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_env          , (opts,) ),
        ( cb_nodes        , (False,) ), # return string
        ( cb_gtzero       , (False,) ), # return string
        ( cb_time         , (False, False, False) ), # no delta time, minutes, return string
        ( cb_umask        , () ),
        ( cb_path         , (opts, True) ), # use CWD
        ( cb_dep          , () ),
        ( cb_attrs        , () ),
        ( cb_user_list    , (opts,True) ), # add current user
        ( cb_geometry     , (opts,) )]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    user = client_utils.getuid()

    # Set required default values
    spec['tag']            = 'job'
    spec['user']           = user
    spec['outputdir']      = client_utils.CWD_TAG
    spec['jobid']          = '*'
    spec['path']           = client_utils.getpath()
    spec['mode']           = False
    spec['cwd']            = client_utils.getcwd()
    spec['kernel']         = 'default'
    spec['queue']          = 'default'
    spec['umask']          = 022
    spec['run_project']    = False
    spec['user_list']      = [user]
    spec['procs']          = False
    spec['script_preboot'] = True

    parser.parse_it() # parse the command line
    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)
    opts['disable_preboot'] = not spec['script_preboot']

    client_utils.setumask(spec['umask'])
    validate_args(parser,spec,opt_count)
    update_outputprefix(parser,spec)
    update_paths(spec)
    check_inputfile(parser,spec)
    opts = client_utils.component_call(SYSMGR, False, 'validate_job',(opts,))
    filters = client_utils.get_filters()
    client_utils.process_filters(filters,spec)
    update_spec(opts,spec,opt2spec)
    jobs = client_utils.component_call(QUEMGR, False, 'add_jobs',([spec],))
    logjob(jobs[0],spec)
    

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
