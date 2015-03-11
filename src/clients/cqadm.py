#!/usr/bin/env python
"""
Administrative interface for queue manager. Allowsone to hold, run, kill, and set 
the queue for jobs in the queue manager. Can also add/del queues and set queue properties.

Usage: %prog --help
Usage: %prog [options] <jobid> <jobid> OR <queue> <queue>
version: "%prog " + __revision__ + , Cobalt  + __version__

OPTIONS DEFINITIONS:

Options with no values and no arguments:

'-d','--debug',dest='debug',help='turn on communication debugging',callback=cb_debug
'-f','--force',dest='force',default=False,help='force flag used by some options',action='store_true'
'--getq',dest='getq',help='get information for all queues',action='store_true'

Options with values but no arguments:

'-j','--setjobid',dest='setjobid',type='int',help='set next jobid',callback=cb_gtzero
'--savestate',dest='savestate',type='string',help='save state to specified filename',callback=cb_path

Options with no values but with queue arguments:

'--addq',dest='addq',help='add queues in args',action='store_true'
'--delq',dest='delq',help='delete queues in args',action='store_true'
'--drainq',help='drain queues in args',callback=cb_setqueues
'--killq',help='kill queues in args',callback=cb_setqueues
'--startq',help='start queues in args',callback=cb_setqueues
'--stopq',help='stop queues in args',callback=cb_setqueues

Option with values and queue arguments:

'--policy',dest='qdata',type='string',help='set policy for queues in args',callback=cb_setqueues

'--setq',dest='qdata',type='string',help='props for queues in args ("prop1=val1 prop2=val2 ... propN=valN")', /
  callback=cb_setqueues

'--unsetq',dest='qdata',type='string',help='unset props for queues in args ("prop1 prop2 ... prop3")', /
  callback=cb_setqueues

Options with no values but with jobid arguments:

'--kill',dest='kill',help='kill jobids in args',action='store_true'
'--preempt',dest='preempt',help='preempt jobids in args',action='store_true'
'--hold', help='Deprecated use --admin-hold instead', callback=cb_hold
'--release', help='Deprecated use --admin-release instead', callback=cb_hold
'--admin-hold', help='apply admin hold to jobids in args',callback=cb_hold
'--admin-release', help='release admin hold for jobids in args', callback=cb_hold
'--user-hold', help='apply user hold to jobids in args', callback=cb_hold
'--user-release', help='release user hold for jobids in args', callback=cb_hold

Option with values and jobid arguments:

'--queue',dest='queue',type='string',help='modify queue name for jobids in args'
'--run',dest='run',type='string',help='modify run location for jobids in args'

'--time',dest='walltime',type='string',help='modify walltime for jobids in args (minutes or HH:MM:SS)', /
  callback=cb_time

"""
import logging
import sys
from Cobalt import client_utils
from Cobalt.client_utils import \
    cb_debug, cb_time, cb_path, cb_gtzero, cb_setqueues, cb_hold
from Cobalt.arg_parser import ArgParse

    
__revision__ = '$Revision: 559 $'
__version__  = '$Version$'

SYSMGR = client_utils.SYSMGR
QUEMGR = client_utils.QUEMGR

def check_option_conflicts(opt_count, parser):
    """
    check mutually exclusive options
    """
    errmsg = '' # init error msessage to empty string
    # Check mutually exclusive options
    if opt_count > 1:
        if parser.options.setjobid  != None: 
            errmsg += ' setjobid'
        if parser.options.savestate != None: 
            errmsg += ' savestate'
        if parser.options.run       != None: 
            errmsg += ' run'
        if parser.options.addq      != None: 
            errmsg += ' addq'
        if parser.options.getq      != None: 
            errmsg += ' getq'
        if parser.options.delq      != None: 
            errmsg += ' delq'
        if parser.options.qdata     != None: 
            errmsg += ' ' + parser.options.setq_opt # set queue options
        if parser.options.preempt   != None: 
            errmsg += ' preempt'
        if parser.options.kill      != None: 
            errmsg += ' kill'

    if errmsg != '':
        errmsg = 'Option combinations not allowed with: %s option(s)' % errmsg[1:].replace(' ', ', ')
        client_utils.logger.error(errmsg)
        sys.exit(1)


def validate_args(parser, spec, opt_count):
    """
    Validate qalter arguments
    """
    opts_wo_args = ['debug', 'getq', 'savestate', 'setjobid'] # no argument options

    # handle release or hold options
    if hasattr(parser.options, 'admin_hold'):
        opt_count += 1
        spec['admin_hold'] = parser.options.admin_hold

    if hasattr(parser.options, 'user_hold'):
        opt_count += 1
        spec['user_hold'] = parser.options.user_hold
    
    # Make sure jobid or queue is supplied for the appropriate commands
    if parser.no_args() and not [opt for opt in spec if opt in opts_wo_args]:
        client_utils.print_usage(parser)
        sys.exit(1)

    # Check required options
    if opt_count == 0:
        client_utils.logger.error("At least one option must be specified")
        sys.exit(1)

    check_option_conflicts(opt_count, parser)

    if parser.options.addq   != None or \
       parser.options.delq   != None or \
       parser.options.getq   != None or \
       parser.options.qdata  != None: # set queue options
        # queue job change request
        jobs = [{'tag':'queue', 'name':qname} for qname in parser.args]
    else:
        # get jobids from the argument list
        jobids = client_utils.get_jobids(parser.args)
        jobs = [{'tag':'job', 'jobid':int(jobid), 'location':'*', 'walltime':'*'} for jobid in jobids]

    return jobs

def getq(info):
    """
    get queue
    """
    response = client_utils.component_call(QUEMGR, True, 'get_queues', (info,))
    for que in response:
        if que['maxtime'] is not None:
            que['maxtime'] = "%02d:%02d:00" % (divmod(int(que.get('maxtime')), 60))
        if que['mintime'] is not None:
            que['mintime'] = "%02d:%02d:00" % (divmod(int(que.get('mintime')), 60))
    header = [('Queue', 'Users', 'Groups', 'MinTime', 'MaxTime', 'MaxRunning',
               'MaxQueued', 'MaxUserNodes', 'MaxNodeHours', 'TotalNodes',
               'AdminEmail', 'State', 'Cron', 'Policy', 'Priority')]
    datatoprint = [(que['name'], que['users'], que['groups'],
                    que['mintime'], que['maxtime'],
                    que['maxrunning'], que['maxqueued'],
                    que['maxusernodes'], que['maxnodehours'], 
                    que['totalnodes'],
                    que['adminemail'], que['state'],
                    que['cron'], que['policy'], que['priority'])
                   for que in response]
    datatoprint.sort()
    client_utils.print_tabular(header + datatoprint)
    return response

def setjobs(jobs, parser, spec, user):
    """
    set jobs 
    """
    if hasattr(parser.options,'admin_hold'):
        for job in jobs:
            job.update({'admin_hold': not parser.options.admin_hold})

    if hasattr(parser.options,'user_hold'):
        for job in jobs:
            job.update({'user_hold': not parser.options.user_hold})

    return client_utils.component_call(QUEMGR, False, 'set_jobs', (jobs, spec, user))

def process_cqadm_options(jobs, parser, spec, user):
    """
    This function will process any command argument and options passed to cqadm
    """

    force = parser.options.force # force flag. 

    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*', 'groups':'*', 'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxusernodes':'*', 'maxqueued':'*', 'maxrunning':'*', 'maxnodehours':'*', 'adminemail':'*', 
             'totalnodes':'*', 'cron':'*', 'policy':'*', 'priority':'*'}]

    response = []
    if parser.options.setjobid != None:
        response = client_utils.component_call(QUEMGR, True, 'set_jobid', (parser.options.setjobid, user))

    elif parser.options.savestate != None:
        response = client_utils.component_call(QUEMGR, True, 'save', (parser.options.savestate,))

    elif parser.options.kill != None:
        response = client_utils.component_call(QUEMGR, False, 'del_jobs', (jobs, force, user))

    elif parser.options.run != None:
        response = client_utils.run_jobs(jobs, parser.options.run, user)

    elif parser.options.addq != None:
        response = client_utils.add_queues(jobs, parser, user, info)

    elif parser.options.getq != None:
        response = getq(info)

    elif parser.options.delq != None:
        response = client_utils.del_queues(jobs, force, user)

    elif parser.options.qdata != None:
        response = client_utils.component_call(QUEMGR, True, 'set_queues', (jobs, parser.options.qdata, user))

    elif parser.options.preempt != None:
        response = client_utils.component_call(QUEMGR, True, 'preempt_jobs', (jobs, user, force))

    else:
        response = setjobs(jobs, parser, spec, user)

    if not response:
        client_utils.logger.error("Failed to match any jobs or queues")
    else:
        client_utils.logger.debug(response)

def main():
    """
    cqadm main function.
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
        ( cb_gtzero       , (True,) ), # return int
        ( cb_time         , (False, False, False) ), # no delta time, minutes, return string
        ( cb_path         , (opts, False) ), # do not use CWD
        ( cb_setqueues    , () ),
        ( cb_hold         , () ) ]

    # Get the version information
    opt_def =  __doc__.replace('__revision__', __revision__)
    opt_def =  opt_def.replace('__version__', __version__)

    parser = ArgParse(opt_def, callbacks)

    user = client_utils.getuid()

    # Set required default values: None

    parser.parse_it() # parse the command line
    opt_count = client_utils.get_options(spec, opts, opt2spec, parser)

    jobs = validate_args(parser, spec, opt_count)

    process_cqadm_options(jobs, parser, spec, user)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        client_utils.logger.fatal("*** FATAL EXCEPTION: %s ***", e)
        sys.exit(1)
