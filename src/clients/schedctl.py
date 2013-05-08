#!/usr/bin/env python
"""
Commands to control job scheduling.

Usage: %prog [--stop | --start | --status | --reread-policy | --savestate]
Usage: %prog [--score | --inherit] jobid1 .. jobidN

version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'--stop',action='store_true',dest='stop',help='stop scheduling jobs'
'--start',action='store_true',dest='start',help='resume scheduling jobs'
'--status',action='store_true',dest='stat',help='query scheduling status'
'--reread-policy',action='store_true',dest='reread',help='reread the utility function definition file'
'--savestate',dest='savestate',type='string',help='write the current state to the specified file',callback=cb_path
'--score',dest='adjust',type='string',help='<jobid> <jobid> adjust the scores of the arguments',callback=cb_score

'--inherit',dest='dep_frac',type='float', /
  help='<jobid> <jobid> control the fraction of the score inherited by jobs which depend on the arguments'

"""
import logging
import sys

from Cobalt import client_utils
from Cobalt.client_utils import cb_debug, cb_path, cb_score

from Cobalt.arg_parser import ArgParse

__revision__ = 'TBD'
__version__  = 'TBD'

def validate_args(parser, args):
    """
    Validate arguments
    """
    spec     = {} 
    opts     = {} 
    opt2spec = {}
    
    opt_count = client_utils.get_options(spec, opts, opt2spec, parser)

    if opt_count == 0:
        parser.parser.print_help()
        client_utils.logger.error("Need at least one option")
        sys.exit(1)

    # Make sure jobid or queue is supplied for the appropriate commands
    args_opts =  [opt for opt in spec if opt in ['adjust','dep_frac']]
    if parser.no_args() and args_opts:
        client_utils.logger.error("At least one jobid must be supplied")
        sys.exit(1)

    elif not parser.no_args():
        if not args_opts:
            client_utils.logger.info("No arguments needed")
        else:
            for i in range(len(args)):
                if args[i] == '*':
                    continue
                try:
                    args[i] = int(args[i])
                except:
                    client_utils.logger.error("jobid must be an integer, found '%s'" % args[i])
                    sys.exit(1)

    optc = 0 # init option count
    errmsg = '' # init error msessage to empty string
    # Check mutually exclusive options
    if opt_count > 1:
        if parser.options.stop != None: 
            errmsg += ' stop'
            optc += 1
        if parser.options.start != None: 
            errmsg += ' start'
            optc += 1
        if parser.options.stat != None: 
            errmsg += ' stat'
            optc += 1
        if parser.options.reread != None: 
            errmsg += ' reread'
            optc += 1
        if parser.options.savestate != None: 
            errmsg += ' savestate'
            optc += 1
        if parser.options.adjust != None or parser.options.dep_frac != None:
            errmsg += ' adjust/dep_frac'
            optc += 1

    if optc > 1:
        errmsg = 'Option combinations not allowed with: %s option(s)' % errmsg[1:].replace(' ',', ')
        client_utils.logger.error(errmsg)
        sys.exit(1)

def main():
    """
    schedctl main function.
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # read the cobalt config files
    client_utils.read_config()

    use_cwd = False
    options = {}

    # list of callback with its arguments
    callbacks = [
        # <cb function>     <cb args (tuple) >
        [ cb_debug        , () ],
        [ cb_score        , () ],
        [ cb_path         , (options, use_cwd) ] ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    parser = ArgParse(opt_def, callbacks)

    # Set required default values: None

    parser.parse_it() # parse the command line
    args  = parser.args
    opt   = parser.options

    whoami = client_utils.getuid()

    validate_args(parser, args)

    sched = client_utils.client_data.scheduler_manager(False)

    if opt.stop != None:
        sched.disable(whoami)
        client_utils.logger.info("Job Scheduling: DISABLED")
        sys.exit(0)
    elif opt.start != None:
        sched.enable(whoami)
        client_utils.logger.info("Job Scheduling: ENABLED")
        sys.exit(0)
    elif opt.stat != None:
        if sched.sched_status():
            client_utils.logger.info("Job Scheduling: ENABLED")
        else:
            client_utils.logger.info("Job Scheduling: DISABLED")
        sys.exit(0)
    elif opt.reread != None:
        client_utils.logger.info("Attempting to reread utility functions.")
        client_utils.define_user_utility_functions(whoami)
        sys.exit(0)
    elif opt.savestate != None:
        response = client_utils.save(opt.savestate,'scheduler')
        client_utils.logger.info(response)
        sys.exit(0)

    if opt.adjust != None:
        client_utils.set_scores(opt.adjust, args, whoami)

    if opt.dep_frac != None:
        specs = [{'jobid':jobid} for jobid in args]
        response = client_utils.set_jobs(specs, {"dep_frac": opt.dep_frac}, whoami)

        if not response:
            client_utils.logger.info("no jobs matched")
        else:
            dumb = [str(r["jobid"]) for r in response]
            client_utils.logger.info("updating inheritance fraction for jobs: %s" % ", ".join(dumb))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", str(sys.exc_info()))
        raise
