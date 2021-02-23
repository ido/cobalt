#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""
Translates a Cobalt qsub command into the equivalent PBS qsub command.
By default outputs a command line;  Add --directives to get PBS directives to add to a script file

Usage: %prog --help
Usage: %prog [options] <executable> [<excutable options>]

Translates a Cobalt qsub command into the equivalent PBS qsub command.
By default outputs a command line;  Add --directives to get PBS directives to add to a script file
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
'--directives',dest='directives',help='output directives for a script rather than a command line',action='store_true'

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
import os
import sys
import socket
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_env, cb_nodes, cb_time, cb_umask, cb_path, cb_dep, \
    cb_attrs, cb_user_list, cb_geometry, cb_gtzero, cb_mode, cb_interactive
from Cobalt.arg_parser import ArgParse
from Cobalt.Util import get_config_option, init_cobalt_config

__revision__ = '$Revision: 559 $'
__version__  = '$Version$'

#init cobalt config file for setting default kernels.
init_cobalt_config()
SYSMGR           = client_utils.SYSMGR
QUEMGR           = client_utils.QUEMGR
CN_DEFAULT_KERNEL  = get_config_option('bgsystem', 'cn_default_kernel', 'default')
ION_DEFAULT_KERNEL = get_config_option('bgsystem', 'ion_default_kernel', 'default')
CRAY_MOM_QSUB      = get_config_option('alps', 'cray_mom_qsub', '/usr/bin/qsub')


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


def hhmmss(minutes_str):
    """ Cobalt stores the walltime in integer minutes. This converts it back 
        to hh:mm:ss for printing. I tried datetime.timedelta, but at 24 hours
        and above, it starts printing 1d and this was easy enough
    """
    total_minutes = int(minutes_str)
    hours = total_minutes // 60
    minutes = total_minutes - (hours * 60)
    #seconds dont work because they rae lost when the command line is processed
    seconds = total_minutes - (hours * 60) - minutes
    
    return('%02d:%02d:%02d' % (hours,minutes,seconds))


def convert_to_pbs(opts, spec):
    """ Uses the parsed dictionaries from the qsub command line processing and
        then maps all the items set to their PBS equivalent. There is an
        additional command line parameter added (--directives) which controls
        whether or not it prints out a command line or the requisite directives
        lines for inclusion in a script.
    """
    target = os.getenv('QSUB_TARGET_SYSTEM')
    if not target:
        print 'set QSUB_TARGET_SYSTEM to a hostname (like theta) to get something other than host=None'
    parms=[]
    parms.append('-l select %s:host=%s' % (opts['nodecount'], target))
    parms.append('-l walltime=%s' % (hhmmss(opts['time'])))
    # I realize there is a lot of very similar code in the if statements below
    # Given the limited duration I didn't think it was worth refactoring.
    if opts['attrs']:
        resources=[]
        for item in opts['attrs']:
            resources.append('%s=%s' % (item, opts['attrs'][item]))
        parms.append('-l ' + ','.join(resources))
    if opts['project']:
        parms.append('-A %s' % (opts['project']))
    if spec['queue'] not in ['default']:
        parms.append('-q %s' % (opts['queue']))
    # dependencies dont work on my laptop because it can't check the jobs; both use colon seperated lists
    if opts['dependencies']:
        parms.append('-W depend=afterok:%s' % (opts['dependencies']))
    if spec['mode'] in ['interactive']:
        parms.append('-I')
    if opts['error']:
        parms.append('-e %s' % (opts['error']))
    if opts['output']:
        parms.append('-o %s' % (opts['output']))
    if opts['notify']:
        parms.append('-M %s' % (opts['notify']))
        parms.append('-m be')
    if opts['held']:
        parms.append('-h')
    if opts['umask']:
        parms.append('-u %s' % (oct(opts['umask'])))
    if opts['env']:
        parms.append('-v %s' % (opts['env'].replace(':',',')))
    if opts['directives']:
        for i in range(len(parms)):
            print '#PBS ' + parms[i]
    else:
        parms.append(spec['command'])
        parms.append(' '.join(spec['args']))
        print(' '.join(['qsub'] + parms))
            
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
    def_spec['message']        = None

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

    validate_options(parser, opt_count)
    convert_to_pbs(opts,spec)
    
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, exc:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", exc)
        sys.exit(1)
