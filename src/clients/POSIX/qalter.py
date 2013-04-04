#!/usr/bin/env python
"""
Cobalt qalter command

Usage: %prog [options] <jobids1> ... <jobidsN>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Option with no values:

'-d','--debug',dest='debug',help='turn non communication debugging',callback=cb_debug
'-v','--verbose',dest='verbose',help='not used',action='store_true'
'-h','--held',dest='user_hold',help='hold jobs in args',action='store_true'
'--run_project',dest='run_project',help='set run project flag for jogids in args',action='store_true'
'--enable_preboot',dest='script_preboot',help='enable script preboot',action='store_true'
'--disable_preboot',dest='script_preboot',help='enable script preboot',action='store_false'

Option with values:

'-n','--nodecount',dest='nodes',type='int',help='modify job node count for jobs in args',callback=cb_nodes
'--proccount',dest='procs',type='int',help='modify job proc count for jobs in args',callback=cb_gtzero
'-A','--project',dest='project',type='string',help='modify project name for jobs in args'
'-M','--notify',dest='notify',type='string',help='modify notification email address for jobs in args'
'-t','--time',dest='walltime',type='string',help='modify walltime for jobs in args ([+/-]minutes or [+/-]HH:MM:SS',callback=cb_time
'-e','--error',dest='errorpath',type='string',help='modify error file path for jobs in args'
'-o','--output',dest='outputpath',type='string',help='modify output file path for jobs in args'
'--dependencies',dest='all_dependencies',type='string',help='for jobs in args (jobid1:jobid2:..)',callback=cb_upd_dep
'--attrs',dest='attrs',type='string',help='modify attributes for jobs in args(attr1=val1:attr2=val2:...',callback=cb_attrs
'--run_users',dest='user_list',type='string',help='modify user list for jobs in args (user1:user2:...)',callback=cb_user_list

The following optins are only valid on IBM BlueGene architecture platforms:

'--mode',dest='mode',type='string',help='modify system mode for jobs in args',callback=cb_mode
'--geometry',dest='geometry',type='string',help='modify geometry for jobs in args (AxBxCxDxE)',callback=cb_geometry

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_nodes, cb_time, cb_mode, \
    cb_upd_dep, cb_attrs, cb_user_list, cb_geometry, cb_gtzero

from Cobalt.arg_parser import ArgParse

__revision__ = '$Revision: 559 $' # TBC may go away.
__version__ = '$Version$'

def validate_args(parser,opt_count,user):
    """
    Validate qalter arguments
    """
    # Check if any altering options entered
    if opt_count == 0:
        client_utils.logger.error("No job altering options entered")
        sys.exit(1)

    # get jobids from the argument list
    jobids = client_utils.validate_jobid_args(parser)
    return [{'tag':'job', 'user':user, 'jobid':jobid, 'project':'*', 'notify':'*', 'walltime':'*',
             'procs':'*', 'nodes':'*', 'is_active':"*", 'queue':'*'} for jobid in jobids]

def get_jobdata(jobs,parser):
    """
    Will get the jobdata for the specified jobs
    """
    jobdata = client_utils.get_jobs(jobs)
    job_running = False

    # verify no job is running
    for job in jobdata:
        if job['is_active']:
            job_running = True

    _quit = False
    if job_running:
        if parser.options.nodes != None:
            client_utils.logger.error( "cannot change node count of a running job")
            _quit = True
        if parser.options.procs != None:
            client_utils.logger.error( "cannot change processor count of a running job")
            _quit = True
        if parser.options.project != None:
            _quit = True
        if parser.options.notify != None:
            _quit = True
        if parser.options.mode != None:
            client_utils.logger.error( "cannot change mode of a running job")
            _quit = True
        if parser.options.walltime != None:
            client_utils.logger.error( "cannot change wall time of a running job")
            _quit = True
        if parser.options.errorpath != None:
            client_utils.logger.error( "cannot change the error path of a running job")
            _quit = True
        if parser.options.outputpath != None:
            client_utils.logger.error( "cannot change the output path of a running job")
            _quit = True
        if parser.options.all_dependencies != None:
            _quit = True
        if parser.options.attrs != None:
            client_utils.logger.error( "cannot change the attributes of a running job")
            _quit = True
        if parser.options.geometry != None:
            client_utils.logger.error( "cannot change the node geometry of a running job")
            _quit = True

        if _quit:
            sys.exit(1)
    return jobdata

def update_time(orig_job,new_spec,parser):
    """
    Update the new time. This will do delta time if specified.
    """
    minutes = new_spec['walltime']
    add_dt = False
    sub_dt = False

    if hasattr(parser.parser,'__timeop__'):
        if parser.parser.__timeop__ == '+': 
            add_dt = True
        elif parser.parser.__timeop__ == '-':
            sub_dt = True

    if add_dt:    # Add time to original job then
        new_spec['walltime'] = str(float(orig_job['walltime']) + minutes)

    elif sub_dt:  # Subtract time to original job and verify it is not less than 0
        new_time = float(orig_job['walltime']) - minutes
        if new_time <= 0:
            client_utils.logger.error( "invalid wall time: " + str(new_time))
        else:
            new_spec['walltime'] = str(new_time)

    else:         # change to an absolute time
        new_spec['walltime'] = minutes

def update_procs(spec,parser):
    """
    Will update 'proc' according to what system we are running on given the number of nodes
    """
    sysinfo = client_utils.system_info()

    if parser.options.nodes != None and parser.options.procs == None:
        if parser.options.mode == 'vn':
            # set procs to 2 x nodes
            if sysinfo[0] == 'bgl':
                spec['procs'] = 2 * spec['nodes']
            elif sysinfo[0] == 'bgp':
                spec['procs'] = 4 * spec['nodes']
            else:
                client_utils.logger.error("Unknown bgtype %s" % (sysinfo[0]))
                sys.exit(1)
        else:
            spec['procs'] = spec['nodes']
    
def main():
    """
    qalter main
    """
    # setup logging for client. The clients should call this before doing anything else.
    client_utils.setup_logging(logging.INFO)

    # read the cobalt config files
    client_utils.read_config()
                               
    spec     = {} # map of destination option strings and parsed values
    opts     = {} # old map
    opt2spec = {}

    dt_allowed = True  # delta time allowed
    add_user   = True  # add current user to the list
    seconds    = False # do not convert to seconds

    # list of callback with its arguments
    callbacks = [
        # <cb function>           <cb args>
        [ cb_debug               , () ],
        [ cb_gtzero              , () ],
        [ cb_nodes               , () ],
        [ cb_time                , (dt_allowed,seconds) ],
        [ cb_upd_dep             , () ],
        [ cb_attrs               , () ],
        [ cb_user_list           , (opts,add_user) ],
        [ cb_geometry            , (opts,) ],
        [ cb_mode                , () ]]

    # Get the version information
    opt_def =  __doc__.replace('__revision__',__revision__)
    opt_def =  opt_def.replace('__version__',__version__)

    parser = ArgParse(opt_def,callbacks)

    user = client_utils.getuid()

    # Set required default values: None

    parser.parse_it() # parse the command line
    opt_count = client_utils.get_options(spec,opts,opt2spec,parser)

    # if run_project set then set run users to current user
    if parser.options.run_project != None:
        spec['user_list'] = [user]

    jobs = validate_args(parser,opt_count,user)
    filters = client_utils.get_filters()

    jobdata = get_jobdata(jobs,parser)

    response = []
    # for every job go update the spec info
    for job in jobdata:
        # append the parsed spec to the updates list
        new_spec          = spec.copy()
        new_spec['jobid'] = job['jobid']

        if parser.options.walltime != None:
            update_time(job,new_spec,parser)
        if parser.options.nodes != None:
            update_procs(new_spec,parser)
        if parser.options.geometry != None:
            client_utils.validate_geometry(opts['geometry'],job['nodes'])

        del job['is_active']
        orig_job = job.copy()
        job.update(new_spec)

        client_utils.process_filters(filters,job)
        response = client_utils.set_jobs([orig_job],job,user)

        # do some logging
        for key in job:
            if not orig_job.has_key(key):
                if key == "all_dependencies":
                    if parser.options.all_dependencies != None:
                        client_utils.logger.info("dependencies set to %s" % ":".join(job[key]))
                else:
                    client_utils.logger.info("%s set to %s" % (key, job[key]))
            elif job[key] != orig_job[key]:
                client_utils.logger.info("%s changed from %s to %s" % (key, orig_job[key], job[key]))

    if not response:
        client_utils.logger.error("Failed to match any jobs or queues")
    else:
        client_utils.logger.debug(response)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
