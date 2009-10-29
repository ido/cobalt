#!/usr/bin/env python
# $Id$

'''Cobalt Queue Manager'''
__revision__ = '$Revision$'

#
# TODO:
#
# - modify progress routine to catch exceptions and report them using __sm_log_exception.  should some or all exceptions cause
#   the job to be terminated?
#
# - make a pass through the __sm_log calls and decide the correct error levels
#
# Changes:
#
# - (Job) the system_state and user_state fields no longer exist.
#
# - (Job) the admin_hold and user_hold fields are now set to True or False to respective hold or release a job.
#
# - (Job) setting the preemptable field to true specifies that a task associate with the job may be preempted.
#
# - (Job) the is_runnable field is true when the job is able to run (ready or preempted states) and false otherwise.
#
# - (Job) the is_active field is set to true when the job is in any state other than ready (queued), held, preempted or completed
#   (terminal).
#
# - (Job) the has_resources field is set to true if resources are assigned to the job.  this assumes that resources may not be
#   deallocated until after the resource epilogue scripts have been run and thus remains true until those scripts have completed.
#   in reality, the system component may reacquire control of the resources and possibly reassign them as soon as the task
#   terminates.  this may occur even before cqm is notices that the task has ended.  unfortunately, this is the best we can do
#   without acquiring resource state from the system component.
#
# - (Job) the has_completed field is set to true only once the job has finished (reached the terminal state).  a value of true
#   does not imply that the job completed successfully, only that it is not active and may never be run again.
#
# - (Job) the preempts field contains a count of the number of times a task associated with the job has been
#   preempted.  this field is read-only and only exists if the job is preemptable.
#
# - (Job) the maxcptime field specifies the time needed for a task to checkpoint.  if maxcptime is greater than zero, the task
#   will first be signaled to checkpoint (SIGUSR1).  after the specified amount of time elapses, the task will then be signaled
#   to terminate (SIGTERM).  if maxcptime is zero, the task will immediately be signaled to terminate.  (BRT: is this the right
#   thing to do?  how will the job know the difference between being preempted and killed?  is it necessary for it to know the
#   difference no checkpoint time is requested?)
#
# - (Job) the mintasktime field specifies the minimum amount of time a task must run before it may be preempted.  any
#   preemption requests made prior to the specified amount of time elapsing will be recorded and processed once the specified
#   amount of time has elapsed.  notification to checkpoint will be made prior to preemption as indicated by the maxcptime.
#
# - (Job) the maxtasktime field specifies the maximum amount of time a task will be allowed to run before being preempted.
#   after the specified amount of time has elasped the task will be signaled to terminate (SIGTERM).  notification to checkpoint
#   will be made prior to preemption as indicated by maxcptime.
#
# - (Job) setting the walltime field is no longer required (at least by the cqm component).  instead, the maxtasktime field
#   may be used to specify repeated timeslices to be given to the job until it terminates.  (BRT: this is a first stab at
#   timeslicing.  eventually, we may want the scheduler component to have some say in whether a job gets preempted after the
#   maximum amount of time has been reached, allowing a job to continue to run past it's specified timeslice if no resource
#   contention exists.)
#
# - (Job) the 'force_kill_delay' field specifies the time that must elapse before a task being preempted or killed should be
#   forcibly terminated (with SIGKILL).  if the field is not set in the job instance, the value of 'force_kill_delay' in the cqm
#   section of the config file will be used.  if 'force_kill_delay' is not found in the cqm section of the config file, then the
#   module attribute DEFAULT_FORCE_KILL_DELAY is used (see below).
#
# Assumptions:
#
# - (Job/CQM) the system component will return a non-zero exit status if the task was killed by a signal.  'None' is considered
#   to be non-zero and thus would be a valid exit status if the task was terminated.
#

DEFAULT_FORCE_KILL_DELAY = 5  # (in minutes)

import errno
import logging
import os
import pwd
import sys
import time
import math
import types
import xmlrpclib
import ConfigParser
import sets
import signal
import thread
from threading import Thread, Lock
import traceback

import Cobalt
import Cobalt.Util
from Cobalt.Util import Timer, pickle_data, unpickle_data, PickleAwareThread
import Cobalt.Cqparse
from Cobalt.Data import Data, DataList, DataDict, IncrID
from Cobalt.StateMachine import StateMachine
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import (QueueError, ComponentLookupError, DataStateError, DataStateTransitionError, StateMachineError,
    StateMachineIllegalEventError, StateMachineNonexistentEventError, ThreadPickledAliveException, JobProcessingError,
    JobRunError, JobPreemptionError, JobDeleteError)
from Cobalt import accounting
from Cobalt.Statistics import Statistics


logger = logging.getLogger('cqm')

cqm_id_gen = None

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('cqm'):
    print '''"cqm" section missing from cobalt config file'''
    sys.exit(1)

def get_cqm_config(option, default):
    try:
        value = config.get('cqm', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

def get_bgsched_config(option, default):
    try:
        value = config.get('bgsched', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

accounting_logdir = os.path.expandvars(get_cqm_config("log_dir", Cobalt.DEFAULT_LOG_DIRECTORY))
accounting_logger = logging.getLogger("cqm.accounting")
accounting_logger.addHandler(
    accounting.DatetimeFileHandler(os.path.join(accounting_logdir, "%Y%m%d")))

def str_elapsed_time(elapsed_time):
    return "%d:%02d:%02d" % (elapsed_time / 3600, elapsed_time / 60 % 60, elapsed_time % 60)

def has_private_attr(obj, attr):
    assert attr[0:2] == "__"
    return hasattr(obj, "_" + obj.__class__.__name__ + attr)

class Signal_Map (object):
    checkpoint = 'SIGUSR1'
    terminate = 'SIGTERM'
    force_kill = 'SIGKILL'

class Signal_Info (object):
    class Reason (object):
        delete = 'delete'
        preempt = 'preempt'
        time_limit = 'time limit'

    def __init__(self, reason = None, signame = None, user = None, pending = False):
        self.__reason = reason
        self.__signal = signame
        self.__user = user
        self.__pending = pending

    def __get_reason(self):
        return self.__reason

    def __set_reason(self, reason):
        if reason in ('delete', 'preempt', 'time_limit'):
            self.__reason = reason
        else:
            raise ValueError, "illegal signal reason: %s" % (reason,)

    reason = property(__get_reason, __set_reason)

    def __get_signal(self):
        return self.__signal

    def __set_signal(self, signame):
        if signame == None:
            self.__signal = None
        if not isinstance(signame, str):
            raise TypeError, "signal name must be a string"
        if signame[0:3] == "SIG" and hasattr(signal, signame):
            self.__signal = signame
        else:
            raise ValueError, "unknown signal name: %s" % (signame,)

    signal = property(__get_signal, __set_signal)

    def __get_user(self):
        return self.__user

    def __set_user(self, user):
        if isinstance(user, str) or user == None:
            self.__user = user
        else:
            raise TypeError, "user name must be a string or None"

    user = property(__get_user, __set_user)

    def __get_pending(self):
        return self.__pending

    def __set_pending(self, pending):
        if isinstance(pending, bool):
            self.__pending = pending
        else:
            raise TypeError, "pending flag must be a boolean value"

    pending = property(__get_pending, __set_pending)


class RunScriptsThread (PickleAwareThread):
    '''object to run a set of prologue and epilogue scripts in a separate thread'''

    def __init__(self, scripts, data_object, attrs):
        '''
        construct the thread object in which to run the scripts, and package up the parameters to be passed to the scripts from the
        attributes in the supplied data object.
        '''
        PickleAwareThread.__init__(self)
        self.__scripts = scripts
        self.__params = []
        for attr in attrs:
            if not hasattr(data_object, attr):
                continue
            value = getattr(data_object, attr)
            if isinstance(value, list):
                self.__params.append('%s=%s' % (attr, ':'.join([Cobalt.Util.escape_string(str(v), ":") for v in value])))
            else:
                self.__params.append('%s=%s' % (attr, str(value)))
        self.__results = []

    def __getstate__(self):
        return pickle_data(self)

    def __setstate__(self, data):
        unpickle_data(self, data)

    def run(self):
        '''
        routine that runs the scripts and collects their results
        '''
        for script in self.__scripts:
            if script == "":
                continue
            results = {}
            results['script'] = script
            try:
                rc, out, err = Cobalt.Util.runcommand(script, self.__params)
                results['rc'] = rc
                results['out'] = out
                results['err'] = err
            except Exception, e:
                results['exception'] = e
            self.__results.append(results)

    def __get_results(self):
        '''
        return exit codes and output accumulated from the scripts.  this should only be called after start() has been called and
        isAlive() subsequently returns False.
        '''
        return self.__results

    results = property(__get_results)

    def __get_scripts_provided(self):
        '''return the list of scripts that was provided when the object was initialized'''
        return self.__scripts

    scripts_provided = property(__get_scripts_provided)

    def __get_scripts_completed(self):
        '''
        return a list of the script known to have completed.  once the thread has finished, this list returned should be the same
        as the list provided during initialization.  the exception would be if the object was pickled and the reconstituted
        before the last script finished.
        '''
        return [result['script'] for result in results]

    scripts_completed = property(__get_scripts_completed)


class Job (StateMachine):
    """
    The job tracks a job, driving it at a high-level.  Actual operations on the job, such as execution or termination, are
    the responsibility of the system component
    """
    
    acctlog = Cobalt.Util.AccountingLog('qm')
    
    # properties for easier accounting logging
    ctime = property(lambda self: self.__timers['queue'].start_times[0])
    qtime = property(lambda self:
        self.__timers['current_queue'].start_times[0])
    start = property(lambda self: self.__timers['user'].start_times[-1])
    exec_host = property(lambda self: ":".join(self.__locations[-1]))
    end = property(lambda self: self.__timers['user'].stop_times[-1])
    
    fields = Data.fields + [
        "jobid", "jobname", "state", "attribute", "location", "starttime", "submittime", "endtime", "queue", "type", "user",
        "walltime", "procs", "nodes", "mode", "cwd", "command", "args", "outputdir", "project", "lienID", "stagein", "stageout",
        "reservation", "host", "port", "url", "stageid", "envs", "inputfile", "kernel", "kerneloptions", "admin_hold",
        "user_hold", "dependencies", "notify", "adminemail", "outputpath", "errorpath", "path", "preemptable", "preempts",
        "mintasktime", "maxtasktime", "maxcptime", "force_kill_delay", "is_runnable", "is_active",
        "has_completed", "sm_state", "score", "attrs", "has_resources", "exit_status",
    ]

    _states = [
        'Ready',
        'Hold',
        'Prologue',
        'Release_Resources_Retry',
        'Run_Retry',
        'Running',
        'Kill_Retry',
        'Killing',
        'Preempt_Retry',
        'Preempting',
        'Preempt_Finalize_Retry',
        'Preempt_Epilogue',
        'Preempted',
        'Preempted_Hold',
        'Finalize_Retry',
        'Resource_Epilogue',
        'Job_Epilogue',
        ] + StateMachine._states
    _transitions = [
        ('Ready', 'Hold'),                                  # user/admin hold
        ('Ready', 'Prologue'),                              # run
        ('Ready', 'Terminal'),                              # kill
        ('Hold', 'Ready'),                                  # user/admin release, no holds
        ('Hold', 'Terminal'),                               # kill
        ('Prologue', 'Release_Resources_Retry'),            # kill; error contacting system component to release resource
        ('Prologue', 'Run_Retry'),                          # prologue scripts complete; error contacting system component
        ('Prologue', 'Running'),                            # prologue scripts complete; system component starting task
        ('Prologue', 'Resource_Epilogue'),                  # kill; system component released resource
        ('Release_Resources_Retry', 'Resource_Epilogue'),   # resource successfully released
        ('Run_Retry', 'Running'),                           # system component starting task
        ('Run_Retry', 'Resource_Epilogue'),                 # kill
        ('Running', 'Kill_Retry'),                          # kill; error contacting system component
        ('Running', 'Killing'),                             # kill; system component signaling task
        ('Running', 'Preempt_Retry'),                       # preempt; error contacting system component
        ('Running', 'Preempting'),                          # preempt; system component signaling task
        ('Running', 'Finalize_Retry'),                      # task execution complete; error finalizing task and obtaining exit
                                                            #     status
        ('Running', 'Resource_Epilogue'),                   # task execution complete; task finalized and exit status obtained
        ('Kill_Retry', 'Kill_Retry'),                       # handle multiple task signaling failures
        ('Kill_Retry', 'Killing'),                          # system component signaling task
        ('Kill_Retry', 'Finalize_Retry'),                   # task execution complete/terminated; task finalization failed
        ('Kill_Retry', 'Resource_Epilogue'),                # task execution completed/terminated successfully
        ('Killing', 'Kill_Retry'),                          # new signal, or kill timer expired; error contacting system component
        ('Killing', 'Killing'),                             # kill timer expired; escalating to a forced kill
        ('Killing', 'Finalize_Retry'),                      # task execution complete/terminated; task finalization failed
        ('Killing', 'Resource_Epilogue'),                   # task execution complete/terminated; task finalization successful
        ('Preempt_Retry', 'Kill_Retry'),                    # kill; error contacting system component
        ('Preempt_Retry', 'Killing'),                       # kill; system component signaling task
        ('Preempt_Retry', 'Preempt_Retry'),                 # hasndle multiple task signaling failures
        ('Preempt_Retry', 'Preempting'),                    # system component signaling task
        ('Preempt_Retry', 'Preempt_Finalize_Retry'),        # task execution terminated, task finalization failed
        ('Preempt_Retry', 'Preempt_Epilogue'),              # task execution terminated successfully
        ('Preempt_Retry', 'Finalize_Retry'),                # task execution completed, task finalization failed
        ('Preempt_Retry', 'Resource_Epilogue'),             # task execution completed successfully
        ('Preempting', 'Kill_Retry'),                       # kill; new signal, error contacting system component
        ('Preempting', 'Killing'),                          # kill; new signal and system component signaling task,
                                                            #     same signal used for preempt, or attempted signal demotion
        ('Preempting', 'Preempting'),                       # preemption timer expired, escalating to the next signal level
        ('Preempting', 'Preempt_Retry'),                    # preemption timer expired, error contacting system component
        ('Preempting', 'Preempt_Finalize_Retry'),           # task execution terminated, task finalization failed
        ('Preempting', 'Preempt_Epilogue'),                 # task execution complete/terminated; task finalization successful
        ('Preempt_Finalize_Retry', 'Preempt_Epilogue'),     # task finalization failed successful
        ('Preempt_Epilogue', 'Preempted'),                  # task execution complete/terminated, no holds pending
        ('Preempt_Epilogue', 'Preempted_Hold'),             # task execution complete/terminated, holds pending
        ('Preempt_Epilogue', 'Job_Epilogue'),               # task execution complete/terminated, kill pending
        ('Preempted', 'Prologue'),                          # run
        ('Preempted', 'Preempted_Hold'),                    # user/admin hold
        ('Preempted', 'Job_Epilogue'),                      # kill
        ('Preempted_Hold', 'Preempted'),                    # user/admin release, no holds
        ('Preempted_Hold', 'Job_Epilogue'),                 # kill
        ('Finalize_Retry', 'Resource_Epilogue'),            # task finalized and exit status obtained (if applicable)
        ('Resource_Epilogue', 'Job_Epilogue'),              # resource epilogue scripts complete
        ('Job_Epilogue', 'Terminal'),                       # job epilogue scripts complete
        ]
    _initial_state = 'Ready'
    _events = ['Run', 'Hold', 'Release', 'Preempt', 'Kill', 'Task_End'] + StateMachine._events

    # return codes to improve typo detection.  by using the return codes in condition statements, a typo will result in a key
    # error rather than an incorrectly followed path.
    __rc_success = "success"
    __rc_retry = "retry"
    __rc_pg_create = "pg_create"
    __rc_xmlrpc = "xmlrpc"
    __rc_unknown = "unknown"

    def __init__(self, spec):
        seas = {
            ('Ready', 'Run') : [self.__sm_ready__run],
            ('Ready', 'Hold') : [self.__sm_ready__hold],
            ('Ready', 'Release') : [self.__sm_ready__release],
            ('Ready', 'Kill') : [self.__sm_ready__kill],
            ('Hold', 'Hold') : [self.__sm_hold__hold],
            ('Hold', 'Release') : [self.__sm_hold__release],
            ('Hold', 'Kill') : [self.__sm_hold__kill],
            ('Prologue', 'Progress') : [self.__sm_prologue__progress],
            ('Prologue', 'Hold') : [self.__sm_common__pending_hold],
            ('Prologue', 'Release') : [self.__sm_common__pending_release],
            ('Prologue', 'Preempt') : [self.__sm_common__pending_preempt],
            ('Prologue', 'Kill') : [self.__sm_common__pending_kill],
            ('Release_Resources_Retry', 'Progress') : [self.__sm_release_resources_retry__progress],
            ('Release_Resources_Retry', 'Hold') : [self.__sm_exit_common__hold],
            ('Release_Resources_Retry', 'Release') : [self.__sm_exit_common__release],
            ('Release_Resources_Retry', 'Preempt') : [self.__sm_exit_common__preempt],
            ('Release_Resources_Retry', 'Kill') : [self.__sm_exit_common__kill],
            ('Run_Retry', 'Progress') : [self.__sm_run_retry__progress],
            ('Run_Retry', 'Hold') : [self.__sm_common__pending_hold],
            ('Run_Retry', 'Release') : [self.__sm_common__pending_release],
            ('Run_Retry', 'Preempt') : [self.__sm_common__pending_preempt],
            ('Run_Retry', 'Kill') : [self.__sm_run_retry__kill],
            ('Running', 'Progress') : [self.__sm_running__progress],
            ('Running', 'Hold') : [self.__sm_common__pending_hold],
            ('Running', 'Release') : [self.__sm_common__pending_release],
            ('Running', 'Preempt') : [self.__sm_common__pending_preempt],
            ('Running', 'Kill') : [self.__sm_running__kill],
            ('Running', 'Task_End') : [self.__sm_running__task_end],
            ('Kill_Retry', 'Progress') : [self.__sm_kill_retry__progress],
            ('Kill_Retry', 'Hold') : [self.__sm_kill_common__hold],
            ('Kill_Retry', 'Release') : [self.__sm_kill_common__release],
            ('Kill_Retry', 'Preempt') : [self.__sm_kill_common__preempt],
            ('Kill_Retry', 'Kill') : [self.__sm_kill_retry__kill],
            ('Kill_Retry', 'Task_End') : [self.__sm_kill_retry__task_end],
            ('Killing', 'Progress') : [self.__sm_killing__progress],
            ('Killing', 'Hold') : [self.__sm_kill_common__hold],
            ('Killing', 'Release') : [self.__sm_kill_common__release],
            ('Killing', 'Preempt') : [self.__sm_kill_common__preempt],
            ('Killing', 'Kill') : [self.__sm_killing__kill],
            ('Killing', 'Task_End') : [self.__sm_killing__task_end],
            ('Preempt_Retry', 'Progress') : [self.__sm_preempt_retry__progress],
            ('Preempt_Retry', 'Hold') : [self.__sm_common__pending_hold],
            ('Preempt_Retry', 'Release') : [self.__sm_common__pending_release],
            ('Preempt_Retry', 'Kill') : [self.__sm_preempt_retry__kill],
            ('Preempt_Retry', 'Task_End') : [self.__sm_preempt_retry__task_end],
            ('Preempting', 'Progress') : [self.__sm_preempting__progress],
            ('Preempting', 'Hold') : [self.__sm_common__pending_hold],
            ('Preempting', 'Release') : [self.__sm_common__pending_release],
            ('Preempting', 'Kill') : [self.__sm_preempting__kill],
            ('Preempting', 'Task_End') : [self.__sm_preempting__task_end],
            ('Preempt_Finalize_Retry', 'Progress') : [self.__sm_preempt_finalize_retry__progress],
            ('Preempt_Finalize_Retry', 'Hold') : [self.__sm_common__pending_hold],
            ('Preempt_Finalize_Retry', 'Release') : [self.__sm_common__pending_release],
            ('Preempt_Finalize_Retry', 'Kill') : [self.__sm_common__pending_kill],
            ('Preempt_Epilogue', 'Progress') : [self.__sm_preempt_epilogue__progress],
            ('Preempt_Epilogue', 'Hold') : [self.__sm_common__pending_hold],
            ('Preempt_Epilogue', 'Release') : [self.__sm_common__pending_release],
            ('Preempt_Epilogue', 'Kill') : [self.__sm_common__pending_kill],
            ('Preempted', 'Run') : [self.__sm_preempted__run],
            ('Preempted', 'Hold') : [self.__sm_preempted__hold],
            ('Preempted', 'Release') : [self.__sm_preempted__release],
            ('Preempted', 'Kill') : [self.__sm_preempted__kill],
            ('Preempted_Hold', 'Hold') : [self.__sm_preempted_hold__hold],
            ('Preempted_Hold', 'Release') : [self.__sm_preempted_hold__release],
            ('Preempted_Hold', 'Kill') : [self.__sm_preempted_hold__kill],
            ('Finalize_Retry', 'Progress') : [self.__sm_finalize_retry__progress],
            ('Finalize_Retry', 'Hold') : [self.__sm_exit_common__hold],
            ('Finalize_Retry', 'Release') : [self.__sm_exit_common__release],
            ('Finalize_Retry', 'Preempt') : [self.__sm_exit_common__preempt],
            ('Finalize_Retry', 'Kill') : [self.__sm_exit_common__kill],
            ('Resource_Epilogue', 'Progress') : [self.__sm_resource_epilogue__progress],
            ('Resource_Epilogue', 'Hold') : [self.__sm_exit_common__hold],
            ('Resource_Epilogue', 'Release') : [self.__sm_exit_common__release],
            ('Resource_Epilogue', 'Preempt') : [self.__sm_exit_common__preempt],
            ('Resource_Epilogue', 'Kill') : [self.__sm_exit_common__kill],
            ('Job_Epilogue', 'Progress') : [self.__sm_job_epilogue__progress],
            ('Job_Epilogue', 'Hold') : [self.__sm_exit_common__hold],
            ('Job_Epilogue', 'Release') : [self.__sm_exit_common__release],
            ('Job_Epilogue', 'Preempt') : [self.__sm_exit_common__preempt],
            ('Job_Epilogue', 'Kill') : [self.__sm_exit_common__kill],
            }
        # StateMachine.__init__(self, spec, seas = seas, terminal_actions = [(self.__sm_terminal, {})])
        StateMachine.__init__(self, spec, seas = seas)
        
        self.jobid = spec.get("jobid")
        self.umask = spec.get("umask")
        self.jobname = spec.get("jobname", "N/A")
        self.attribute = spec.get("attribute", "compute")
        self.starttime = spec.get("starttime", "-1")
        self.submittime = spec.get("submittime", time.time())
        self.endtime = spec.get("endtime", "-1")
        self.type = spec.get("type", "mpish")
        self.user = spec.get("user")
        self.__walltime = int(float(spec.get("walltime", 0)))
        self.procs = spec.get("procs")
        self.nodes = spec.get("nodes")
        self.cwd = spec.get("cwd")
        self.command = spec.get("command")
        self.args = spec.get("args", [])
        self.project = spec.get("project")
        self.lienID = spec.get("lienID")
        self.stagein = spec.get("stagein")
        self.stageout = spec.get("stageout")
        self.reservation = spec.get("reservation", False)
        self.host = spec.get("host")
        self.port = spec.get("port")
        self.url = spec.get("url")
        self.stageid = spec.get("stageid")
        self.inputfile = spec.get("inputfile")
        self.tag = spec.get("tag", "job")
        self.kernel = spec.get("kernel", "default")
        self.kerneloptions = spec.get("kerneloptions")
        self.notify = spec.get("notify")
        self.adminemail = spec.get("adminemail")
        self.location = spec.get("location")
        self.__locations = []
        self.outputpath = spec.get("outputpath")
        if self.outputpath:
            jname = self.outputpath.split('/')[-1].split('.output')[0]
            if jname and jname != str(self.jobid):
                self.jobname = jname
        self.outputdir = spec.get("outputdir")
        self.errorpath = spec.get("errorpath")
        self.cobalt_log_file = spec.get("cobalt_log_file")
        if not self.cobalt_log_file:
            self.cobalt_log_file = "%s/%s.cobaltlog" % (self.outputdir, self.jobid)
        self.path = spec.get("path")
        self.mode = spec.get("mode", "co")
        self.envs = spec.get("envs", {})
        self.force_kill_delay = spec.get("force_kill_delay", get_cqm_config('force_kill_delay', DEFAULT_FORCE_KILL_DELAY))
        self.attrs = spec.get("attrs", {})

        self.all_dependencies = spec.get("all_dependencies")
        if self.all_dependencies:
            self.all_dependencies = self.all_dependencies.split(":")
        else:
            self.all_dependencies = []
        self.satisfied_dependencies = []

        self.preemptable = spec.get("preemptable", False)
        self.__preempts = 0
        if self.preemptable:
            self.mintasktime = int(float(spec.get("mintasktime", 0)))
            self.maxtasktime = int(float(spec.get("maxtasktime", 0)))
            self.maxcptime = int(float(spec.get("maxcptime", 0)))

        self.taskid = None
        self.task_running = False
        self.exit_status = None
        self.max_running = False

        self.__admin_hold = False
        self.__user_hold = False
        
        self.score = float(spec.get("score", 0.0))

        self.__resource_nodects = []
        self.__timers = dict(
            queue = Timer(),
            current_queue = Timer(),
            user = Timer(),
        )

        # setting the queue with cause updated accounting records to be written and the current queue timer to be restarted, so
        # this needs to be done only after the object has been initialized
        self.queue = spec.get("queue", "default")
        self.__timers['queue'].start()
        self.etime = time.time()

        # setting the hold flags will automatically cause the appropriate hold events to be triggered, so this needs to be done
        # only after the object has been completely initialized
        if spec.get("admin_hold", False):
            self.admin_hold = True
        if spec.get("user_hold", False):
            self.user_hold = True
    # end def __init__()

    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['log', 'comms', 'acctlog']:
                data[key] = value
        return data

    def __setstate__(self, state):
        self.__dict__.update(state)
        # BRT: why is the current queue timer being reset?  if cqm is restarted, the job remained in the queue during that time,
        # so I would think that timer should continue to run during the restart rather than been reset.
        if not self.__timers.has_key('current_queue'):
            self.__timers['current_queue'] = Timer()
            self.__timers['current_queue'].start()
    
    def __task_signal(self, retry = True):
        '''send a signal to the managed task'''
        # BRT: this routine should probably check if the task could not be signaled because it was no longer running
        try:
            self.__sm_log_info("instructing the system component to send signal %s" % (self.__signaling_info.signal,))
            pgroup = ComponentProxy("system").signal_process_groups([{'id':self.taskid}], self.__signaling_info.signal)
        except (ComponentLookupError, xmlrpclib.Fault), e:
            #
            # BRT: will a ComponentLookupError ever be raised directly or will it always be buried in a XML-RPC fault?
            #
            # BRT: shouldn't we be checking the XML-RPC fault code?  which fault codes are valid for this operation?  at the
            # very least unexpected fault code should be reported as such and the retry loop broken.
            #
            if retry:
                self.__sm_log_warn("failed to communicate with the system component (%s); retry pending" % (e,))
                return Job.__rc_retry
            else:
                self.__sm_log_warn("failed to communicate with the system component (%s); manual cleanup may be required" % \
                    (e,))
                return Job.__rc_xmlrpc
        except:
            traceback.print_exc()
            self.__sm_raise_exception("unexpected error from the system component; manual cleanup may be required")
            return Job.__rc_unknown

        self.__signaled_info = self.__signaling_info
        del self.__signaling_info
        return Job.__rc_success

    def __task_run(self):
        walltime = self.walltime
        if self.preemptable and self.maxtasktime < walltime:
            walltime = self.maxtasktime
        try:
            self.__sm_log_info("instructing the system component to begin executing the task")
            pgroup = ComponentProxy("system").add_process_groups([{
                'id':"*",
                'jobid':self.jobid,
                'user':self.user,
                'stdin':self.inputfile,
                'stdout':self.outputpath,
                'stderr':self.errorpath,
                'cobalt_log_file':self.cobalt_log_file,
                'size':self.procs,
                'nodect':"*",
                'mode':self.mode,
                'cwd':self.outputdir,
                'executable':self.command,
                'args':self.args,
                'env':self.envs,
                'location':self.location,
                'umask':self.umask,
                'kernel':self.kernel,
                'kerneloptions':self.kerneloptions,
                'walltime':walltime
            }])
            if pgroup[0].has_key('id'):
                self.taskid = pgroup[0]['id']
                if pgroup[0].has_key('nodect') and pgroup[0]['nodect'] != None:
                    self.__resource_nodects.append(pgroup[0]['nodect'])
                else:
                    self.__resource_nodects.append(self.nodes)
            else:
                self.__sm_log_error("process group creation failed", cobalt_log = True)
                return Job.__rc_pg_create
        except (ComponentLookupError, xmlrpclib.Fault), e:
            self.__sm_log_warn("failed to execute the task (%s); retry pending" % (e,))
            return Job.__rc_retry
        except:
            self.__sm_raise_exception("unexpected error returned from the system component when attempting to add task",
                cobalt_log = True)
            return Job.__rc_unknown

        return Job.__rc_success

    def __task_finalize(self):
        '''get exit code from system component'''
        try:
            result = ComponentProxy("system").wait_process_groups([{'id':self.taskid, 'exit_status':'*'}])
            if result:
                self.exit_status = result[0].get('exit_status')
            else:
                self.__sm_log_warn("system component was unable to locate the task; exit status not obtained")
        except (ComponentLookupError, xmlrpclib.Fault), e:
            self.__sm_log_warn("failed to communicate with the system component (%s); retry pending" % (e,))
            return Job.__rc_retry
        except:
            self.__sm_raise_exception("unexpected error returned from the system component while finalizing task")
            return Job.__rc_unknown

        self.taskid = None
        return Job.__rc_success

    def __release_resources(self):
        '''release computing resources that may still be reserved by the job'''
        try:
            ComponentProxy("system").reserve_resources_until(self.location, None, self.jobid)
            return Job.__rc_success
        except (ComponentLookupError, xmlrpclib.Fault), e:
            self.__sm_log_warn("failed to communicate with the system component (%s); retry pending" % (e,))
            return Job.__rc_retry
        except:
            self.__sm_raise_exception("unexpected error returned from the system component while releasing resources")
            return Job.__rc_unknown

    def __sm_log_debug(self, msg, cobalt_log = False):
        '''write an informational message to the CQM log that includes state machine status'''
        if self.__sm_event != None:
            event_msg = "; Event=%s" % (self.__sm_event,)
        else:
            event_msg = ""
        logger.debug("Job %s/%s: State=%s%s; %s" % (self.jobid, self.user, self.__sm_state, event_msg, msg))
        if cobalt_log:
            self.__write_cobalt_log("Debug: %s" % (msg,))

    def __sm_log_info(self, msg, cobalt_log = False):
        '''write an informational message to the CQM log that includes state machine status'''
        if self.__sm_event != None:
            event_msg = "; Event=%s" % (self.__sm_event,)
        else:
            event_msg = ""
        logger.info("Job %s/%s: State=%s%s; %s" % (self.jobid, self.user, self.__sm_state, event_msg, msg))
        if cobalt_log:
            self.__write_cobalt_log("Info: %s" % (msg,))

    def __sm_log_warn(self, msg, cobalt_log = False):
        '''write a warning message to the CQM log that includes state machine status'''
        if self.__sm_event != None:
            event_msg = "; Event=%s" % (self.__sm_event,)
        else:
            event_msg = ""
        logger.warning("Job %s/%s: State=%s%s; %s" % (self.jobid, self.user, self.__sm_state, event_msg, msg))
        if cobalt_log:
            self.__write_cobalt_log("Warning: %s" % (msg,))

    def __sm_log_error(self, msg, tb_flag = True, skip_tb_entries = 1, cobalt_log = False):
        '''write an error message to the CQM log that includes state machine status and a stack trace'''
        if self.__sm_event != None:
            event_msg = "; Event=%s" % (self.__sm_event,)
        else:
            event_msg = ""
        full_msg = "Job %s/%s: State=%s%s; %s" % (self.jobid, self.user, self.__sm_state, event_msg, msg)
        if tb_flag:
            stack = traceback.format_stack()
            last_tb_entry = len(stack) - skip_tb_entries
            for entry in stack[:last_tb_entry]:
                full_msg += "\n    " + entry[:-1]
        logger.error(full_msg)
        if cobalt_log:
            self.__write_cobalt_log("ERROR: %s" % (msg,))

    def __sm_log_exception(self, msg, cobalt_log = False):
        '''write an error message to the CQM log that includes state machine status and a stack trace'''
        if self.__sm_event != None:
            event_msg = "; Event=%s" % (self.__sm_event,)
        else:
            event_msg = ""
        full_msg = "Job %s/%s: State=%s%s; %s" % (self.jobid, self.user, self.__sm_state, event_msg, msg)
        (exc_cls, exc, tb) = sys.exc_info()
        exc_str = traceback.format_exception_only(exc_cls, exc)[0]
        full_msg += "\n    Exception: %s" % (exc_str)
        stack = traceback.format_tb(tb)
        for entry in stack:
            full_msg += "\n    " + entry[:-1]
        logger.error(full_msg)
        if cobalt_log:
            self.__write_cobalt_log("EXCEPTION: %s" % (full_msg,))

    def __sm_raise_exception(self, msg, cobalt_log = False):
        self.__sm_log_error(msg, skip_tb_entries = 2, cobalt_log = cobalt_log)
        raise JobProcessingError(msg, self.jobid, self.user, self.state, self.__sm_state, self.__sm_event)

    def __sm_log_user_delete(self, signame, user = None, pending = False):
        if user != None:
            umsg = " by user %s" % (user,)
        else:
            umsg = ""
        if pending == True:
            pmsg = " now pending"
        else:
            pmsg = ""
        self.__sm_log_info("user delete requested with signal %s%s%s" % (signame, umsg, pmsg), cobalt_log = True)

    def __sm_signaling_info_set_user_delete(self, signame = Signal_Map.terminate, user = None, pending = False):
        self.__signaling_info = Signal_Info(Signal_Info.Reason.delete, signame, user, pending)
        self.__sm_log_user_delete(signame, user, pending)

    def __sm_check_job_timers(self):
        if self.__max_job_timer.has_expired:
            # if the job execution time has exceeded the wallclock time, then inform the task that it must terminate
            self.__sm_log_info("maximum execution time exceeded; initiating job terminiation")
            accounting_logger.info(accounting.abort(self.jobid))
            return Signal_Info(Signal_Info.Reason.time_limit, Signal_Map.terminate)
        else:
            return None

    def __sm_kill_task(self):
        '''initiate the user deletion of a task by signaling it and then changing to the appropriate state'''
        # BRT: this routine should probably check if the task could not be signaled because it was no longer running
        rc = self.__task_signal()
        if rc == Job.__rc_success:
            # start the signal timer so that the state machine knows when to escalate to sending a force kill signal
            if self.__signaled_info.signal != Signal_Map.force_kill:
                self.__sm_log_debug("setting force kill signal timer to %d seconds" % (self.force_kill_delay * 60,))
                self.__signal_timer = Timer(self.force_kill_delay * 60)
            else:
                self.__signal_timer = Timer()
            self.__signal_timer.start()
            self.__sm_state = 'Killing'
            return True
        else:
            self.__sm_state = 'Kill_Retry'
            return False

    def __sm_check_preempt_timers(self):
        '''
        if maximum resource timer has expired, or a preemption is pending and the minimum resource time has been exceeded, then
        inform the task it's time to checkpoint and terminate
        '''
        if self.__maxtasktimer.has_expired:
            self.__sm_log_info("maximum resource time exceeded; initiating job preemption")
            if self.maxcptime > 0:
                return Signal_Info(Signal_Info.Reason.preempt, Signal_Map.checkpoint)
            else:
                return Signal_Info(Signal_Info.Reason.preempt, Signal_Map.terminate)
        elif has_private_attr(self, '__signaling_info') and self.__signaling_info.reason == Signal_Info.Reason.preempt and \
                self.__signaling_info.pending and self.__mintasktimer.has_expired:
            self.__sm_log_info("preemption pending and resource time exceeded; initiating job preemption")
            sig_info = self.__signaling_info
            sig_info.pending = False
            return sig_info
        else:
            return None

    def __sm_preempt_task(self):
        '''initiate the preemption of a task by signaling it and then changing to the appropriate state'''
        # BRT: this routine should probably check if the task could not be signaled because it was no longer running
        rc = self.__task_signal()
        if rc == Job.__rc_success:
            if self.__signaled_info.signal == Signal_Map.checkpoint:
                # start the signal timer so that the state machine knows when to escalate to sending a terminate signal
                self.__signal_timer = Timer(self.maxcptime * 60)
                self.__sm_log_debug("setting terminate signal timer to %d seconds" % (self.maxcptime * 60,))
            elif self.__signaled_info.signal == Signal_Map.terminate:
                # start the signal timer so that the state machine knows when to escalate to sending a force kill signal
                self.__signal_timer = Timer(self.force_kill_delay * 60)
                self.__sm_log_debug("setting force kill signal timer to %d seconds" % (self.force_kill_delay * 60,))
            else:
                self.__signal_timer = Timer()
            self.__signal_timer.start()
            self.__sm_state = 'Preempting'
            return True
        else:
            self.__sm_state = 'Preempt_Retry'
            return False

    def __sm_start_resource_epilogue_scripts(self, new_state = 'Resource_Epilogue'):
        resource_scripts = get_cqm_config('resource_postscripts', "").split(':')
        self.__sm_scripts_thread = RunScriptsThread(resource_scripts, self, self.fields)
        self.__sm_scripts_thread.start()
        self.__sm_state = new_state

    def __sm_start_job_epilogue_scripts(self, new_state = 'Job_Epilogue'):
        job_scripts = get_cqm_config('job_postscripts', "").split(':')
        self.__sm_scripts_thread = RunScriptsThread(job_scripts, self, self.fields)
        self.__sm_scripts_thread.start()
        self.__sm_state = new_state

    def __sm_scripts_are_finished(self, type):
        try:
            if self.__sm_scripts_thread.isAlive():
                return False
        except ThreadPickledAliveException:
            if not has_private_attr(self, "__sm_scripts_state_unknown"):
                self.__sm_log_error(("restart of cqm left running scripts in an unknown state; job has been frozen; " + \
                    "scripts=%s; scripts_completed=%s") % (":".join(self.__sm_scripts_thread.scripts_provided), \
                    ":".join(self.__sm_scripts_thread.scripts_completed)), cobalt_log = True)
                self.__sm_scripts_state_unknown = True

        self.__sm_scripts_thread.join()

        for result in self.__sm_scripts_thread.results:
            if result.has_key('exception'):
                self.__sm_log_warn("exception with %s %s, error is %s" % (type, result['script'], result['exception']))
            elif result['rc'] != 0:
                err_msg = ("\n" + result['err']).replace("\n", "\n    ").rstrip()
                self.__sm_log_warn("return code from %s %s was %d; error text follows:%s" % \
                    (type, result['script'], result['rc'], err_msg))
        return True

    def __sm_common_queued__hold(self, hold_state, args):
        '''place a hold on a job in the queued state'''
        if self.__admin_hold:
            self.__sm_raise_exception("admin hold set on a job in the '%s' state", self.__sm_state)
            return
        if self.__user_hold:
            self.__sm_raise_exception("user hold set on a job in the '%s' state", self.__sm_state)
            return

        if args['type'] == 'admin':
            self.__admin_hold = True
        elif args['type'] == 'user':
            self.__user_hold = True
        else:
            self.__sm_raise_exception("hold type of '%s' is not valid; type must be 'admin' or 'user'" % (args['type'],))
            return

        if not self.__timers.has_key('hold'):
            self.__timers['hold'] = Timer()
        self.__timers['hold'].start()
        self.__sm_log_info("%s hold placed on job" % (args['type'],), cobalt_log = True)
        self.__sm_state = hold_state

    def __sm_common_queued__release(self, args):
        '''handle attempt to erroneously release a job in the queued state'''
        if self.__admin_hold:
            self.__sm_raise_exception("admin hold set on a job in the '%s' state", self.__sm_state)
            return
        if self.__user_hold:
            self.__sm_raise_exception("user hold set on a job in the '%s' state", self.__sm_state)
            return

        self.__sm_log_info("job is not being held; ignoring release request", cobalt_log = True)

    def __sm_common_hold__hold(self, args):
        '''place another hold on a job that is already in a hold state'''
        activity = False

        if args['type'] == 'admin':
            if not self.__admin_hold:
                self.__admin_hold = True
                activity = True
        elif args['type'] == 'user':
            if not self.__user_hold:
                self.__user_hold = True
                activity = True
        else:
            self.__sm_raise_exception("hold type of '%s' is not valid; type must be 'admin' or 'user'" % (args['type'],))
            return

        if activity:
            self.__sm_log_info("%s hold set" % (args['type'],), cobalt_log = True)
        else:
            self.__sm_log_info("%s hold already present; ignoring hold request" % (args['type'],), cobalt_log = True)

        '''release a hold previous placed on a job'''
        activity = False

    def __sm_common_hold__release(self, queued_state, args):
        '''release a hold previous placed on a job in a hold state'''
        activity = False

        if args['type'] == 'admin':
            if self.__admin_hold:
                self.__admin_hold = False
                activity = True
        elif args['type'] == 'user':
            if self.__user_hold:
                self.__user_hold = False
                activity = True
        else:
            self.__sm_raise_exception("hold type of '%s' is not valid; type must be 'admin' or 'user'" % (args['type'],))
            return

        if activity:
            self.__sm_log_info("%s hold released" % (args['type'],), cobalt_log = True)
        else:
            self.__sm_log_info("%s hold not present; ignoring release request" % (args['type'],), cobalt_log = True)
            
        if not self.__admin_hold and not self.__user_hold:
            self.__sm_log_info("no holds remain; releasing job", cobalt_log = True)
            self.__timers['hold'].stop()
            self.etime = time.time()
            self.__sm_state = queued_state

    def __sm_ready__run(self, args):
        '''prepare a job for execution'''
        self.__sm_log_info("preparing job for execution")

        # stop queue timers
        self.__timers['queue'].stop()
        self.__timers['current_queue'].stop()

        # start job and resource timers
        self.__timers['user'].start()
        if self.walltime > 0:
            self.__max_job_timer = Timer(self.walltime * 60)
        else:
            self.__max_job_timer = Timer()
        self.__max_job_timer.start()
        if self.preemptable:
            self.__mintasktimer = Timer(max((self.mintasktime - self.maxcptime) * 60, 0))
            self.__mintasktimer.start()
            if self.maxtasktime > 0:
                self.__maxtasktimer = Timer(max((self.maxtasktime - self.maxcptime) * 60, 0))
            else:
                self.__maxtasktimer = Timer()
            self.__maxtasktimer.start()

        self.starttime = str(time.time())

        self.location = args['nodelist']
        self.__locations.append(self.location)

        # write job start and project information to CQM and accounting logs
        if self.reservation:
            logger.info('R;%s;%s;%s' % (self.jobid, self.queue, self.user))
            self.acctlog.LogMessage('R;%s;%s;%s' % (self.jobid, self.queue, self.user))
        else:
            logger.info('S;%s;%s;%s;%s;%s;%s;%s' % (self.jobid, self.user, self.jobname, self.nodes, self.procs, self.mode, \
                self.walltime))
            self.acctlog.LogMessage('S;%s;%s;%s;%s;%s;%s;%s' % (self.jobid, self.user, self.jobname, self.nodes, self.procs, \
                self.mode, self.walltime))
        if self.project:
            logger.info("Job %s/%s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.project, self.queue, \
                ":".join(self.location)))
            self.acctlog.LogMessage("Job %s/%s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.project, self.queue, \
                ":".join(self.location)))
        else:
            logger.info("Job %s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.queue, ":".join(self.location)))
            self.acctlog.LogMessage("Job %s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.queue, \
                ":".join(self.location)))

        optional = {}
        if self.project:
            optional['account'] = self.project
        # group and session are unknown
        accounting_logger.info(accounting.start(self.jobid, self.user,
            "unknown", self.jobname, self.queue,
            self.outputdir, self.command, self.args, self.mode,
            self.ctime, self.qtime, self.etime, self.start, self.exec_host,
            {'ncpus':self.procs, 'nodect':self.nodes,
             'walltime':str_elapsed_time(self.walltime * 60)},
            "unknown", **optional))

        # notify the user that the job is starting; a separate thread is used to send the email so that cqm does not block
        # waiting for the smtp server to respond
        if self.notify:
            mailserver = get_cqm_config('mailserver', None)
            if mailserver == None:
                mserver = 'localhost'
            else:
                mserver = mailserver
            subj = 'Cobalt: Job %s/%s starting - %s/%s' % (self.jobid, self.user, self.queue, self.location[0])
            mmsg = ("Job %s/%s, in the '%s' queue, starting at %s.\nJobName: %s\nCWD: %s\nCommand: %s\nArgs: %s\n" + \
                    "Project: %s\nWallTime: %s\nSubmitTime: %s\nResources allocated: %s") % \
                    (self.jobid, self.user, self.queue, time.strftime('%c', time.localtime()), self.jobname, self.cwd,
                     self.command, self.args, self.project, str_elapsed_time(self.walltime), time.ctime(self.submittime),
                     ":".join(self.location))
            toaddr = []
            if self.adminemail:
                toaddr = toaddr + self.adminemail.split(':')
            if self.notify:
                toaddr = toaddr + self.notify.split(':')
            thread.start_new_thread(Cobalt.Util.sendemail, (toaddr, subj, mmsg), {'smtpserver':mserver})

        # set the output and error filenames (BRT: why is this not done in __init__?)
        if not self.outputpath:
            self.outputpath = "%s/%s.output" % (self.outputdir, self.jobid)
        if not self.errorpath:
            self.errorpath = "%s/%s.error" % (self.outputdir, self.jobid)

        # add the cobolt job id to the list of environment variables
        self.envs['COBALT_JOBID'] = str(self.jobid)

        # start job and resource prologue scripts
        job_scripts = get_cqm_config('job_prescripts', "").split(':')
        resource_scripts = get_cqm_config('resource_prescripts', "").split(':')
        self.__sm_scripts_thread = RunScriptsThread(job_scripts + resource_scripts, self, self.fields)
        self.__sm_scripts_thread.start()

        self.__sm_state = 'Prologue'

    def __sm_ready__hold(self, args):
        '''place a hold on a job in the queued state'''
        self.__sm_common_queued__hold('Hold', args)

    def __sm_ready__release(self, args):
        '''handle attempt to erroneously release a job in the ready state'''
        self.__sm_common_queued__release(args)

    def __sm_ready__kill(self, args):
        '''delete a job in the ready state'''
        self.__sm_log_info("user delete requested; removing job from the queue", cobalt_log = True)
        self.__signaled_info = Signal_Info(Signal_Info.Reason.delete, args['signal'], args['user'])
        self.__sm_state = 'Terminal'

    def __sm_hold__hold(self, args):
        '''place another hold on a job that is already in the hold state'''
        self.__sm_common_hold__hold(args)

    def __sm_hold__release(self, args):
        '''release a hold previous placed on a job'''
        self.__sm_common_hold__release('Ready', args)

    def __sm_hold__kill(self, args):
        '''delete a job in the hold state'''
        self.__sm_log_info("user delete requested; removing job from the queue", cobalt_log = True)
        self.__signaled_info = Signal_Info(Signal_Info.Reason.delete, args['signal'], args['user'])
        self.__sm_state = 'Terminal'

    def __sm_common__pending_hold(self, args):
        '''place a pending hold to a preemptable job that is active'''
        if not self.preemptable:
            self.__sm_log_info("non-preemptable job has already started; hold request ignored", cobalt_log = True)
            return

        activity = False

        if args['type'] == 'admin':
            if not self.__admin_hold:
                self.__admin_hold = True
                activity = True
        elif args['type'] == 'user':
            if not self.__user_hold:
                self.__user_hold = True
                activity = True
        else:
            self.__sm_raise_exception("hold type of '%s' is not valid; type must be 'admin' or 'user'" % (args['type'],))
            return

        if activity:
            self.__sm_log_info("pending %s hold set" % (args['type'],), cobalt_log = True)
        else:
            self.__sm_log_info("pending %s hold already present; ignoring hold request" % \
                (args['type'],), cobalt_log = True)

    def __sm_common__pending_release(self, args):
        '''remove a pending hold from a preemptable job that is active'''
        if not self.preemptable:
            self.__sm_log_info("non-preemptable job has already started; release request ignored", cobalt_log = True)
            return

        activity = False

        if args['type'] == 'admin':
            if self.__admin_hold:
                self.__admin_hold = False
                activity = True
        elif args['type'] == 'user':
            if self.__user_hold:
                self.__user_hold = False
                activity = True
        else:
            self.__sm_raise_exception("hold type of '%s' is not valid; type must be 'admin' or 'user'" % (args['type'],))
            return

        if activity:
            self.__sm_log_info("pending %s hold removed" % (args['type'],), cobalt_log = True)
        else:
            self.__sm_log_info("pending %s hold not present; ignoring release request" % (args['type'],), cobalt_log = True)

    def __sm_common__pending_kill(self, args):
        '''place a pending user delete request on a job whose current state does not permit immediately signaling the job'''
        if has_private_attr(self, '__signaling_info') and self.__signaling_info.reason == Signal_Info.Reason.delete and \
                self.__signaling_info.signal == args['signal']:
            self.__sm_log_info("user delete request already pending with signal %s; ignoring user delete request", \
                cobalt_log = True)
            return
        self.__sm_signaling_info_set_user_delete(args['signal'], args['user'], pending = True)
    
    def __sm_common__pending_preempt(self, args):
        '''place a pending preemption on a job whose current state does not permit immediately signaling the job'''
        if not self.preemptable:
            self.__sm_log_warn("preemption requests may only be made for preemptable jobs", cobalt_log = True)
            try:
                user = args['user']
            except KeyError:
                user = self.user
            try:
                force = args['force']
            except KeyError:
                force = False
            raise JobPreemptionError("Only preemptable jobs may be preempted.", self.jobid, user, force)

        # if a delete is already pending, then ignore preemption request
        if has_private_attr(self, '__signaling_info') and self.__signaling_info.reason == Signal_Info.Reason.delete:
            self.__sm_log_info("user delete request already pending; ignoring preemption request", cobalt_log = True)
            return

        # if preemption is being forced, reset the time limit on the minimum task timer so that the preemption request will be
        # processed the next time a progress event is triggered
        if args.has_key('force'):
            self.__mintasktimer.max_time = 0
        if self.maxcptime > 0:
            self.__signaling_info = Signal_Info(Signal_Info.Reason.preempt, Signal_Map.checkpoint, None, True)
        else:
            self.__signaling_info = Signal_Info(Signal_Info.Reason.preempt, Signal_Map.terminate, None, True)
        if args.has_key('user'):
            self.__signaling_info.user = args['user']
        if args.has_key('force'):
            user_msg = ""
            if args.has_key('user'):
                user_msg = " by user %s" % (args['user'],)
            self.__sm_log_info("preemption forced%s" % (user_msg,), cobalt_log = True)
        else:
            self.__sm_log_info("preemption request now pending", cobalt_log = True)
    
    def __sm_prologue__progress(self, args):
        '''
        wait for prologue scripts to complete.  once they have completed, execute the task if no user delete requests are pending.
        '''
        # wait for the prologue scripts to complete; report any errors
        if not self.__sm_scripts_are_finished("prescript"):
            return
        self.__sm_log_debug("prologue scripts have completed")

        # if a user delete is pending, then release any resources that have been reserved, and start job cleanup so that it may
        # terminate
        if has_private_attr(self, '__signaling_info')  and self.__signaling_info.pending and \
                self.__signaling_info.reason == Signal_Info.Reason.delete:
            self.__signaled_info = self.__signaling_info
            self.__signaled_info.pending = False
            del self.__signaling_info
            self.__sm_log_info("pending user delete; releasing resources", cobalt_log = True)
            rc = self.__release_resources()
            if rc == Job.__rc_success:
                self.__sm_log_info("resources released; initiating job cleanup and removal", cobalt_log = True)
                self.__sm_start_resource_epilogue_scripts()
            else:
                self.__sm_state = 'Release_Resources_Retry'
            return
            
        # attempt to run task
        rc = self.__task_run()
        if rc == Job.__rc_success:
            self.__sm_state = 'Running'
            self.task_running = True
        elif rc == Job.__rc_retry:
            self.__sm_state = 'Run_Retry'
        else:
            # if the task failed to run, then proceed with job termination by starting the resource prologue scripts
            self.__sm_log_error("execution failure; initiating job cleanup and removal", cobalt_log = True)
            self.__sm_start_resource_epilogue_scripts()

    def __sm_release_resources_retry__progress(self, args):
        self.__sm_log_info("retrying release of resources")
        rc = self.__release_resources()
        if rc == Job.__rc_success:
            self.__sm_log_info("resources released; initiating job cleanup and removal", cobalt_log = True)
            self.__sm_start_resource_epilogue_scripts()

    def __sm_run_retry__progress(self, args):
        '''previous attempt to execute the task failed; attempt to run it again'''
        rc = self.__task_run()
        if rc == Job.__rc_success:
            self.__sm_state = 'Running'
            self.task_running = True
        elif rc != Job.__rc_retry:
            # if the task failed to run, then proceed with job termination by starting the resource prologue scripts
            self.__sm_log_error("execution failure; initiating job cleanup and removal", cobalt_log = True)
            self.__sm_start_resource_epilogue_scripts()

    def __sm_run_retry__kill(self, args):
        '''user delete requested while job was waiting to retry executing task'''
        self.__sm_log_info("user delete with signal %s requested by user %s; initiating job cleanup and removal" % \
            (args['signal'], args['user']), cobalt_log = True)

        # set signal information so that the terminal state handler knows to write the delete record
        self.__signaled_info = Signal_Info(Signal_Info.Reason.delete, args['signal'], args['user'])

        # start the resource epilogue scripts
        self.__sm_start_resource_epilogue_scripts()

    def __sm_running__progress(self, args):
        '''
        periodically verify that the job has not exceeded its maximum execution time and determine if the task needs to be
        preempted
        '''
        sig_info = self.__sm_check_job_timers()
        if sig_info != None:
            self.__signaling_info = sig_info
            self.__sm_kill_task()
        elif self.preemptable:
            sig_info = self.__sm_check_preempt_timers()
            if sig_info != None:
                self.__signaling_info = sig_info
                self.__sm_preempt_task()

    def __sm_running__kill(self, args):
        '''user delete requested while job is executing a task'''
        self.__sm_signaling_info_set_user_delete(args['signal'], args['user'])
        self.__sm_kill_task()

    def __sm_running__task_end(self, args):
        '''task completed normally'''
        # finalize the task and obtain the exit status
        self.__sm_log_info("task completed normally; finalizing task and obtaining exit code")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            self.__sm_state = 'Finalize_Retry'
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task completed normally with an exit code of %s; initiating job cleanup and removal" % \
            (self.exit_status,), cobalt_log = True)
        self.__sm_start_resource_epilogue_scripts()

    def __sm_kill_common__hold(self, args):
        '''attempt to add a hold to a preemptable job that is being killed'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of being killed; hold request ignored", cobalt_log = True)
        else:
            self.__sm_log_info("non-preemptable job has already started; hold request ignored", cobalt_log = True)

    def __sm_kill_common__release(self, args):
        '''attempt to remove a hold from a preemptable job that is being killed'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of being killed; release request ignored", cobalt_log = True)
        else:
            self.__sm_log_info("non-preemptable job has already started; release request ignored", cobalt_log = True)

    def __sm_kill_common__preempt(self, args):
        '''attempt to preempt a preemptable job that is being killed'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of being killed; preemption request ignored", cobalt_log = True)
        else:
            self.__sm_log_warn("preemption requests may only be made for preemptable jobs", cobalt_log = True)
            try:
                user = args['user']
            except KeyError:
                user = self.user
            try:
                force = args['force']
            except KeyError:
                force = False
            raise JobPreemptionError("Only preemptable jobs may be preempted.", self.jobid, user, force)

    def __sm_kill_retry__progress(self, args):
        '''previous attempt to signal the task to terminate failed; attempt to signal again'''
        # note: signaling_info is still set and should not be set again
        self.__sm_kill_task()

    def __sm_kill_retry__kill(self, args):
        '''
        process a user delete request on a job which already has an outstanding delete request.  only modify the existing request
        if the signal to be sent is a promotion of the one pending.
        '''
        if self.__signaling_info.reason == Signal_Info.Reason.time_limit:
            self.__sm_log_info("job is already being terminated for exceeding a time limit; ignoring user delete request", \
                cobalt_log = True)
            return

        if self.__signaling_info.reason != Signal_Info.Reason.delete:
            self.__sm_log_error("signal reason is expected to be %s but is %s" % \
                (Signal_Info.Reason.delete, self.__signaling_info.reason))
            return

        if self.__signaling_info.signal == args['signal']:
            self.__sm_log_info("user delete request already pending with signal %s; ignoring user delete request" % \
               (args['signal'],), cobalt_log = True)
            return

        if self.__signaling_info.signal == Signal_Map.force_kill:
            self.__sm_log_info("job is already being forced to terminate; ignoring user delete request", cobalt_log = True)
            return

        if self.__signaling_info.signal == Signal_Map.terminate and args['signal'] != Signal_Map.force_kill:
            self.__sm_log_warn("signal demotion attempted; only %s may be specified once %s has been sent; ignoring request" % \
                (Signal_Map.force_kill, Signal_Map.terminate))
            return

        self.__sm_signaling_info_set_user_delete(args['signal'], args['user'])
        self.__sm_kill_task()

    def __sm_kill_retry__task_end(self, args):
        '''task completed/terminated while waiting to retry signaling the task'''
        # delete signal information since the signal was never sent
        del self.__signaling_info

        # finalize the task and obtain the exit status
        if has_private_attr(self, '__signaled_info'):
            self.__sm_log_info("task terminated; finalizing task")
        else:
            self.__sm_log_info("task completed normally; finalizing task and obtaining exit code")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            self.__sm_state = 'Finalize_Retry'
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task completed normally with an exit code of %s; initiating job cleanup and removal" % \
            (self.exit_status,), cobalt_log = True)
        self.__sm_start_resource_epilogue_scripts()

    def __sm_killing__progress(self, args):
        '''check if the signal timer; if it has expired, promote signal to a force kill and signal the task again'''
        if self.__signal_timer.has_expired:
            self.__sm_log_info("job deletion timer has expired; forcibly terminating task")
            self.__signaling_info = self.__signaled_info
            self.__signaling_info.signal = Signal_Map.force_kill
            self.__sm_kill_task()

    def __sm_killing__kill(self, args):
        '''
        process a user delete request on a job which is already being deleted.  only modify the existing request if the signal to
        be sent is a promotion of the one already sent.
        '''
        if self.__signaled_info.reason == Signal_Info.Reason.time_limit:
            self.__sm_log_info("job is already being terminated for exceeding a time limit; ignoring user delete request", \
                cobalt_log = True)
            return

        if self.__signaled_info.reason != Signal_Info.Reason.delete:
            self.__sm_log_error("signal reason is expected to be %s but is %s" % \
                (Signal_Info.Reason.delete, self.__signaled_info.reason))
            return

        if self.__signaled_info.signal == args['signal']:
            self.__sm_log_info("user delete request already pending with signal %s; ignoring user delete request" % \
               (args['signal'],), cobalt_log = True)
            return

        if self.__signaled_info.signal == Signal_Map.force_kill:
            self.__sm_log_info("job is already being forced to terminate; ignoring user delete request", cobalt_log = True)
            return

        if self.__signaled_info.signal == Signal_Map.terminate and args['signal'] != Signal_Map.force_kill:
            self.__sm_log_warn("signal demotion attempted; only %s may be specified once %s has been sent; ignoring request" % \
                (Signal_Map.force_kill, Signal_Map.terminate))
            return

        self.__sm_signaling_info_set_user_delete(args['signal'], args['user'])
        self.__sm_kill_task()

    def __sm_killing__task_end(self, args):
        '''task terminated (presumably from signal)'''
        self.__signal_timer.stop()

        # finalize the task and obtain the exit status
        self.__sm_log_info("task terminated; finalizing task")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            self.__sm_state = 'Finalize_Retry'
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task terminated; initiating resource cleanup")
        self.__sm_start_resource_epilogue_scripts()

    def __sm_preempt_retry__progress(self, args):
        '''previous attempt to signal the task failed; attempt to signal again'''
        self.__sm_preempt_task()

    def __sm_preempt_retry__kill(self, args):
        '''
        process a user delete request on a job which is being preempted.  only modify the existing signal if the signal to be
        sent is a promotion of the one pending.
        '''
        if self.__signaling_info.signal == Signal_Map.terminate and args['signal'] != Signal_Map.force_kill:
            self.__sm_log_warn(("job is already being preempted with %s; only %s may be specified once %s has been sent; " + \
                "switching to job deletion") % (Signal_Map.terminate, Signal_Map.force_kill, Signal_Map.terminate))
            sig = Signal_Map.terminate
        else:
            sig = args['signal']
        self.__sm_signaling_info_set_user_delete(sig, args['user'])
        self.__sm_kill_task()

    def __sm_preempt_retry__task_end(self, args):
        '''task completed/terminated while waiting to retry signaling the task'''
        # delete signal information since the signal was never sent
        del self.__signaling_info

        # finalize the task and obtain the exit status
        if has_private_attr(self, '__signaled_info'):
            self.__sm_log_info("task terminated; finalizing task")
            new_epilogue_state = 'Preempt_Epilogue'
        else:
            self.__sm_log_info("task completed normally; finalizing task and obtaining exit code")
            new_epilogue_state = 'Resource_Epilogue'
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            if has_private_attr(self, '__signaled_info'):
                self.__sm_state = 'Preempt_Finalize_Retry'
            else:
                # if the task terminated before the signal was ever sent, then treate this as a normal end-of-job not a preemption
                self.__sm_state = 'Finalize_Retry'
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task terminated; initiating resource cleanup")
        self.__sm_start_resource_epilogue_scripts(new_epilogue_state)

    def __sm_preempting__progress(self, args):
        '''check if the signal timer; if it has expired, promote signal to a force kill and signal the task again'''
        if self.__signal_timer.has_expired:
            self.__signaling_info = self.__signaled_info
            if self.__signaled_info.signal == Signal_Map.terminate:
                self.__sm_log_info("job preemption timer has expired; forcibly terminating task")
                self.__signaling_info.signal = Signal_Map.force_kill
            else:
                self.__sm_log_info("job preemption timer has expired; signaling the task to terminate")
                self.__signaling_info.signal = Signal_Map.terminate
            self.__sm_preempt_task()

    def __sm_preempting__kill(self, args):
        '''
        process a user delete request on a job which is already being preempted.  only modify the existing signal if the signal
        to be sent is a promotion of the one pending.
        '''
        if self.__signaled_info.signal == args['signal']:
            self.__sm_log_info("job is already being preempted with %s; switching to job deletion" % (args['signal'],), \
                cobalt_log = True)
            self.__sm_state = 'Killing'
            return

        if self.__signaled_info.signal == Signal_Map.force_kill:
            self.__sm_log_info("job is already being preempted and forced to terminate; switching to job deletion",
                cobalt_log = True)
            self.__sm_state = 'Killing'
            return

        if self.__signaled_info.signal == Signal_Map.terminate and args['signal'] != Signal_Map.force_kill:
            self.__sm_log_warn(("job is already being preempted with %s; only %s may be specified once %s has been sent; " + \
                "switching to job deletion") % (Signal_Map.terminate, Signal_Map.force_kill, Signal_Map.terminate))
            self.__sm_state = 'Killing'
            return

        self.__sm_signaling_info_set_user_delete(args['signal'], args['user'])
        self.__sm_kill_task()

    def __sm_preempting__task_end(self, args):
        '''task preemption completed'''
        # finalize the task and obtain the exit status
        self.__sm_log_info("task preemption completed; finalizing task")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            self.__sm_state = 'Preempt_Finalize_Retry'
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task terminated; initiating resource cleanup")
        self.__sm_start_resource_epilogue_scripts('Preempt_Epilogue')

    def __sm_preempt_finalize_retry__progress(self, args):
        '''previous attempt to finalize the task and extract the exit status failed; make another attempt'''
        # make another attempt to finalize the task
        self.__sm_log_info("previous attempt to finalize the task failed; trying again")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task terminated; initiating resource cleanup")
        self.__sm_start_resource_epilogue_scripts('Preempt_Epilogue')

    def __sm_preempt_epilogue__progress(self, args):
        # wait for the resource epilogue scripts to complete, and report any errors
        if not self.__sm_scripts_are_finished("resource postscript"):
            return

        # if a user delete is pending, then start job cleanup so that it may terminate
        if has_private_attr(self, '__signaling_info')  and self.__signaling_info.pending:
            self.__signaled_info = self.__signaling_info
            self.__signaled_info.pending = False
            del self.__signaling_info
            self.__sm_log_info("pending user delete; initiating job cleanup and removal", cobalt_log = True)
            self.__sm_start_job_epilogue_scripts()
            return
            
        # stop the execution timer, clear the location where the job is being run, and output accounting log entry
        self.__timers['user'].stop()
        self.__max_job_timer.stop()
        self.location = None
        if self.__max_job_timer.has_expired:
            # if the job execution time has exceeded the wallclock time, then proceed to cleanup and remove the job
            self.__sm_log_info("maximum execution time exceeded; initiating job cleanup and removal", cobalt_log = True)
            accounting_logger.info(accounting.abort(self.jobid))
            self.__sm_start_job_epilogue_scripts()
            return

        # write job preemption information to CQM and accounting logs
        if self.project:
            logger.info("Job %s/%s/%s/Q:%s: Preempted job" % (self.jobid, self.user, self.project, self.queue))
            self.acctlog.LogMessage("Job %s/%s/%s/Q:%s: Preempted job" % (self.jobid, self.user, self.project, self.queue))
        else:
            logger.info("Job %s/%s/Q:%s: Preempted job" % (self.jobid, self.user, self.queue))
            self.acctlog.LogMessage("Job %s/%s/Q:%s: Preempted job" % (self.jobid, self.user, self.queue))

        accounting_logger.info(accounting.rerun(self.jobid))

        self.__sm_log_info("job successfully preempted", cobalt_log = True)
        self.__preempts += 1

        # start the queue timers
        self.__timers['queue'].start()
        self.__timers['current_queue'].start()

        # reset the job's score to 0 after preempting it
        self.score = 0.0
        
        # if a pending hold exists, then change to the preempted hold state; otherwise change to the preempted state
        if self.admin_hold or self.user_hold:
            if not self.__timers.has_key('hold'):
                self.__timers['hold'] = Timer()
            self.__timers['hold'].start()
            self.__sm_state = 'Preempted_Hold'
        else:
            self.__sm_state = 'Preempted'

    def __sm_preempted__run(self, args):
        # stop queue timers
        self.__timers['queue'].stop()
        self.__timers['current_queue'].stop()

        # start job and resource timers
        self.__timers['user'].start()
        self.__max_job_timer.start()
        if self.preemptable:
            self.__mintasktimer = Timer(max((self.mintasktime - self.maxcptime) * 60, 0))
            self.__mintasktimer.start()
            if self.maxtasktime > 0:
                self.__maxtasktimer = Timer(max((self.maxtasktime - self.maxcptime) * 60, 0))
            else:
                self.__maxtasktimer = Timer()
            self.__maxtasktimer.start()

        # set the list of resources being used
        self.location = args['nodelist']
        self.__locations.append(self.location)

        # write job restart and project information to CQM and accounting logs
        if self.reservation:
            logger.info('R;%s;%s;%s' % (self.jobid, self.queue, self.user))
            self.acctlog.LogMessage('R;%s;%s;%s' % (self.jobid, self.queue, self.user))
        else:
            logger.info('S;%s;%s;%s;%s;%s;%s;%s' % (self.jobid, self.user, self.jobname, self.nodes, self.procs, self.mode, \
                self.walltime))
            self.acctlog.LogMessage('S;%s;%s;%s;%s;%s;%s;%s' % (self.jobid, self.user, self.jobname, self.nodes, self.procs, \
                self.mode, self.walltime))
        if self.project:
            logger.info("Job %s/%s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.project, self.queue, \
                ":".join(self.location)))
            self.acctlog.LogMessage("Job %s/%s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.project, self.queue, \
                ":".join(self.location)))
        else:
            logger.info("Job %s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.queue, ":".join(self.location)))
            self.acctlog.LogMessage("Job %s/%s/Q:%s: Running job on %s" % (self.jobid, self.user, self.queue, \
                ":".join(self.location)))

        optional = {}
        if self.project:
            optional['account'] = self.project
        # group and session are unknown
        accounting_logger.info(accounting.start(self.jobid, self.user,
            "unknown", self.jobname, self.queue,
            self.outputdir, self.command, self.args, self.mode,
            self.ctime, self.qtime, self.etime, self.start, self.exec_host,
            {'ncpus':self.procs, 'nodect':self.nodes,
             'walltime':str_elapsed_time(self.walltime * 60)},
            "unknown", **optional))

        # start resource prologue scripts
        resource_scripts = get_cqm_config('resource_prescripts', "").split(':')
        self.__sm_scripts_thread = RunScriptsThread(resource_scripts, self, self.fields)
        self.__sm_scripts_thread.start()

        self.__sm_state = 'Prologue'

    def __sm_preempted__hold(self, args):
        '''place a hold on a job in the preempted state'''
        self.__sm_common_queued__hold('Preempted_Hold', args)

    def __sm_preempted__release(self, args):
        '''handle attempt to erroneously release a job in the preempted state'''
        self.__sm_common_queued__release(args)

    def __sm_preempted__kill(self, args):
        '''user delete requested while job was preempted'''
        self.__sm_log_info("user delete with signal %s requested by user %s; initiating job cleanup and removal" % \
            (args['signal'], args['user']), cobalt_log = True)

        # set signal information so that the terminal state handler knows to write the delete record
        self.__signaled_info = Signal_Info(Signal_Info.Reason.delete, args['signal'], args['user'])

        # start the job epilogue scripts
        self.__sm_start_job_epilogue_scripts()

    def __sm_preempted_hold__hold(self, args):
        '''place another hold on a job that is already in the preempted hold state'''
        self.__sm_common_hold__hold(args)

    def __sm_preempted_hold__release(self, args):
        '''release a hold previous placed on a job'''
        self.__sm_common_hold__release('Preempted', args)

    def __sm_preempted_hold__kill(self, args):
        '''user delete requested while job was preempted and held'''
        self.__sm_log_info("user delete with signal %s requested by user %s; initiating job cleanup and removal" % \
            (args['signal'], args['user']), cobalt_log = True)

        # set signal information so that the terminal state handler knows to write the delete record
        self.__signaled_info = Signal_Info(Signal_Info.Reason.delete, args['signal'], args['user'])

        # start the job epilogue scripts
        self.__sm_start_job_epilogue_scripts()

    def __sm_exit_common__hold(self, args):
        '''attempt to add a hold to a job that is exiting'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of exiting; hold request ignored", cobalt_log = True)
        else:
            self.__sm_log_info("non-preemptable job has already started; hold request ignored", cobalt_log = True)

    def __sm_exit_common__release(self, args):
        '''attempt to release a hold to a job that is exiting'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of exiting; release request ignored", cobalt_log = True)
        else:
            self.__sm_log_info("non-preemptable job has already started; release request ignored", cobalt_log = True)

    def __sm_exit_common__preempt(self, args):
        '''attempt to preempt a job that is exiting'''
        if self.preemptable:
            self.__sm_log_info("job is in the process of exiting; preemption request ignored", cobalt_log = True)
        else:
            self.__sm_log_warn("preemption requests may only be made for preemptable jobs", cobalt_log = True)
            try:
                user = args['user']
            except KeyError:
                user = self.user
            try:
                force = args['force']
            except KeyError:
                force = False
            raise JobPreemptionError("Only preemptable jobs may be preempted.", self.jobid, user, force)

    def __sm_exit_common__kill(self, args):
        '''attempt to perform a user delete on a job that is exiting'''
        self.__sm_log_info("job is in the process of exiting; user delete request ignored", cobalt_log = True)

    def __sm_finalize_retry__progress(self, args):
        '''previous attempt to finalize the task and extract the exit status failed; make another attempt'''
        # make another attempt to finalize the task and obtain the exit status
        self.__sm_log_info("previous attempt to finalize the task and obtain exit code failed; trying again")
        rc = self.__task_finalize()
        if rc == Job.__rc_retry:
            return

        # start the resource epilogue scripts
        self.__sm_log_info("task completed normally with an exit code of %s; initiating job cleanup and removal" % \
            (self.exit_status,), cobalt_log = True)
        self.__sm_start_resource_epilogue_scripts()

    def __sm_resource_epilogue__progress(self, args):
        '''wait for resource epilogue scripts to complete.  once they have completed, start the job epilogue scripts.'''
        # wait for the resource epilogue scripts to complete, and report any errors
        if not self.__sm_scripts_are_finished("resource postscript"):
            return

        # start job epilogue scripts
        self.__sm_start_job_epilogue_scripts()
    
    def __sm_job_epilogue__progress(self, args):
        '''wait for job epilogue scripts to complete.  once they have completed, write out end-of-job accounting logs'''
        # wait for the job epilogue scripts to complete, and report any errors
        if not self.__sm_scripts_are_finished("job postscript"):
            return

        # stop the execution timer and get the stats; NOTE: the execution timer may not be running if the job was preempted
        if self.__timers['user'].is_active:
            self.__timers['user'].stop()
        stats = self.__get_stats()

        # notify the user that the job has completed; a separate thread is used to send the email so that cqm does not block
        # waiting for the smtp server to respond
        if self.notify:
            mailserver = get_cqm_config('mailserver', None)
            if mailserver == None:
                mserver = 'localhost'
            else:
                mserver = mailserver
            subj = 'Cobalt: Job %s/%s finished - %s/%s %s' % (self.jobid, self.user, self.queue, self.location[0], stats)
            mmsg = ("Job %s/%s, in the '%s' queue, finished at %s\nJobName: %s\nCWD: %s\nCommand: %s\nArgs: %s\n" + \
                    "Project: %s\nWallTime: %s\nSubmitTime: %s\nStats: %s\nExit code: %s\nResources used: %s") % \
                    (self.jobid, self.user, self.queue, time.strftime('%c', time.localtime()), self.jobname, self.cwd,
                     self.command, self.args, self.project, str_elapsed_time(self.walltime), time.ctime(self.submittime),
                     stats, self.exit_status, ",".join([":".join(l) for l in self.__locations]))
            toaddr = []
            if self.adminemail:
                toaddr = toaddr + self.adminemail.split(':')
            if self.notify:
                toaddr = toaddr + self.notify.split(':')
            thread.start_new_thread(Cobalt.Util.sendemail, (toaddr, subj, mmsg), {'smtpserver':mserver})

        # write end of job information to CQM and accounting logs
        used_time = 0
        for index in xrange(len(self.__locations)):
            used_time += int(self.__timers['user'].elapsed_times[index]) * len(self.__locations[index])
        logger.info('E;%s;%s;%s' % (self.jobid, self.user, str(used_time)))
        self.acctlog.LogMessage('E;%s;%s;%s' % (self.jobid, self.user, str(used_time)))
        self.endtime = str(time.time())

        optional = {}
        if self.project:
            optional['account'] = self.project
        if self.exit_status != None:
            exit_status = self.exit_status
        else:
            exit_status = "unknown"
        # group and session are unknown
        accounting_logger.info(accounting.end(self.jobid, self.user,
            "unknown", self.jobname, self.queue,
            self.outputdir, self.command, self.args, self.mode,
            self.ctime, self.qtime, self.etime, self.start, self.exec_host,
            {'ncpus':self.procs, 'nodect':self.nodes,
             'walltime':str_elapsed_time(self.walltime * 60)},
            "unknown", self.end, exit_status,
            {'location':",".join([":".join(l) for l in self.__locations]),
             'nodect':",".join([str(n) for n in self.__resource_nodects]),
             'walltime':",".join([str_elapsed_time(t) for t in self.__timers['user'].elapsed_times])},
            **optional))
        
        logger.info("Job %s/%s on %s nodes done. %s" % (self.jobid, self.user, self.nodes, stats))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit:%s" % \
            (self.jobid, self.user, self.nodes, stats, str(self.exit_status)))

        self.__sm_state = 'Terminal'

    # def __sm_terminal(self, args):
    #     try:
    #         reason = self.__signaled_info.reason
    #     except AttributeError:
    #         return
    #     else:
    #         if reason == Signal_Info.Reason.delete:
    #             accounting_logger.info(accounting.delete(self.jobid,
    #                 self.__signaled_info.user))
    #             logger.info('D;%s;%s' % (self.jobid, self.user))
    #             self.acctlog.LogMessage('D;%s;%s' % (self.jobid, self.user))

    def __sm_get_state(self):
        return StateMachine._state.__get__(self)

    def __sm_set_state(self, state):
        self.__sm_log_info("transitioning to the '%s' state" % (state,))
        StateMachine._state.__set__(self, state)

    __sm_state = property(__sm_get_state, __sm_set_state)
    sm_state = property(__sm_get_state, __sm_set_state)

    def __sm_get_event(self):
        return StateMachine._event.__get__(self)

    __sm_event = property(__sm_get_event)

    def __get_queue(self):
        return self.__queue

    def __set_queue(self, queue):
        logger.info('Q;%s;%s;%s' % (self.jobid, self.user, queue))
        self.acctlog.LogMessage('Q;%s;%s;%s' % (self.jobid, self.user, queue))
        accounting_logger.info(accounting.queue(self.jobid, queue))
        self.__timers['current_queue'] = Timer()
        self.__timers['current_queue'].start()
        self.__queue = queue

    queue = property(__get_queue, __set_queue)

    def __get_walltime(self):
        return self.__walltime

    def __set_walltime(self, walltime):
        walltime = int(float(walltime))
        if self.__sm_state == 'Running':
            remaining_time = walltime - int(self.__timers['user'].elapsed_time) / 60
            if remaining_time > 0:
                ComponentProxy("system").reserve_resources_until(self.location, time.time() + remaining_time * 60, self.jobid)
        self.__walltime = int(float(walltime))
        try:
            self.__max_job_timer.max_time = walltime * 60
        except AttributeError:
            pass
        self.__sm_log_info("walltime adjusted to %d minutes" % (self.__walltime,))

    walltime = property(__get_walltime, __set_walltime)

    def __get_admin_hold(self):
        return self.__admin_hold

    def __set_admin_hold(self, hold_flag):
        if hold_flag:
            self.trigger_event('Hold', {'type' : 'admin'})
        else:
            self.trigger_event('Release', {'type' : 'admin'})

    admin_hold = property(__get_admin_hold, __set_admin_hold)

    def __get_user_hold(self):
        return self.__user_hold

    def __set_user_hold(self, hold_flag):
        if hold_flag:
            self.trigger_event('Hold', {'type' : 'user'})
        else:
            self.trigger_event('Release', {'type' : 'user'})

    user_hold = property(__get_user_hold, __set_user_hold)

    def __has_dep_hold(self):
        return self.all_dependencies and not sets.Set(self.all_dependencies).issubset(sets.Set(self.satisfied_dependencies))

    has_dep_hold = property(__has_dep_hold)

    def __get_job_state(self):
        if self.__sm_state in ('Ready', 'Preempted'):
            if self.has_dep_hold:
                return "dep_hold"
            if self.max_running:
                return "maxrun_hold"
        if self.__sm_state == 'Ready':
            return "queued"
        if self.__sm_state in ['Hold', 'Preempted_Hold']:
            if self.user_hold:
                return "user_hold"
            else:
                return "admin_hold"
        if self.__sm_state in ['Prologue', 'Run_Retry']:
            return "starting"
        if self.__sm_state == 'Running':
            return "running"
        if self.__sm_state in ['Kill_Retry', 'Killing']:
            return "killing"
        if self.__sm_state in ['Preempt_Retry', 'Preempting', 'Preempt_Finalize_Retry', 'Preempt_Epilogue']:
            return 'preempting'
        if self.__sm_state == 'Preempted':
            return 'preempted'
        if self.__sm_state in ['Release_Resources_Retry', 'Finalize_Retry', 'Resource_Epilogue', 'Job_Epilogue']:
            return "exiting"
        if self.__sm_state == 'Terminal':
            return "done"
        raise DataStateError, "unknown state: %s" % (self.__sm_state,)

    state = property(__get_job_state)
    
    def __get_short_job_state(self):
        if self.__sm_state in ('Ready', 'Preempted') and (self.has_dep_hold or self.max_running):
            return "H"
        if self.__sm_state == 'Ready':
            return "Q"
        if self.__sm_state in ['Hold', 'Preempted_Hold']:
            return "H"
        if self.__sm_state in ['Prologue', 'Run_Retry', 'Running']:
            return "R"
        if self.__sm_state in ['Kill_Retry', 'Killing']:
            return "K"
        if self.__sm_state in ['Preempt_Retry', 'Preempting', 'Preempt_Finalize_Retry', 'Preempt_Epilogue', 'Preempted']:
            return 'P'
        if self.__sm_state in ['Release_Resources_Retry', 'Finalize_Retry', 'Resource_Epilogue', 'Job_Epilogue', 'Terminal']:
            return 'E'
        raise DataStateError, "unknown state: %s" % (self.__sm_state,)

    short_state = property(__get_short_job_state)

    def __is_runnable(self):
        '''returns true if the job is runnable'''
        if self.__sm_state in ('Ready', 'Preempted'):
            if self.has_dep_hold or self.max_running:
                return False
            return True
        else:
            return False

    is_runnable = property(__is_runnable)

    def __has_resources(self):
        '''
        returns true if the job has resources assigned to it.  the running of resource epilogue scripts is included in the set of
        state considered as active since they may be responsible for cleaning up and releasing the resources.  the running of the
        job epilogue scripts is not included since the resources should have been released no later than by the time the resource
        epilogue scripts complete.  the running of the job prologue scripts are included since resources would have been
        allocated and assigned to the job prior to the 'Run' event being triggered in the 'Ready' state, which is what initiates
        the running of the job scripts.
        '''
        return self.__sm_state not in ('Ready', 'Hold', 'Preempted', 'Preempted_Hold', 'Job_Epilogue', 'Terminal')

    has_resources = property(__has_resources)

    def __is_active(self):
        '''returns true if the job is not queued or held, and has not completed'''
        return self.__sm_state not in ('Ready', 'Hold', 'Preempted', 'Preempted_Hold', 'Terminal')

    is_active = property(__is_active)

    def __has_completed(self):
        '''returns true if the job has completed, whether successfully or not'''
        return self.__sm_state == 'Terminal'

    has_completed = property(__has_completed)

    def __get_dependencies(self):
        ret = ""
        for dep in self.all_dependencies:
            ret += dep
            if dep in self.satisfied_dependencies:
                ret += "*"
            ret += ", "
        
        ret = ret[:-2]    
        return ret

    dependencies = property(__get_dependencies)

    def __get_preempts(self):
        return self.__preempts

    preempts = property(__get_preempts)

    # def __get_eligible_run_time(self):
    #     '''Return the time the job was first eligible to run'''
    #     # if self.__preempts > 0 or not self.__timers.has_key('hold'):
    #     try:
    #         return self.__timers['hold'].stop_times[-1] # job became eligible at end of last hold
    #     except KeyError:
    #         return self.__timers['queue'].start_times[0] # job has always been eligible to run
    # 
    # etime = property(__get_eligible_run_time)

    def __get_stats(self):
        '''Get job execution statistics from timers'''
        result = ''
        for (name, timer) in self.__timers.iteritems():
            try:
                result += "%s:%.02fs " % (name, timer.elapsed_time)
            except Exception, mmsg:
                logger.error("timer: %s wasn't started: %s" % (name, mmsg))
        return result

    def __write_cobalt_log(self, message):
        try:
            uid = pwd.getpwnam(self.user)[2]
        except KeyError:
            logger.error("Job %s/%s: user name is not valid; skipping output to cobaltlog file" % (self.jobid, self.user))
            return
        except Exception, e:
            logger.exception("Job %s/%s: obtaining the user id failed" % (self.jobid, self.user))
            return

        try:
            file_uid = os.stat(self.cobalt_log_file).st_uid
            if file_uid != uid:
                logger.error("Job %s/%s: user does not own cobaltlog file %s" % (self.jobid, self.user, self.cobalt_log_file))
                return
        except OSError, e:
            if e.errno != errno.ENOENT:
                logger.error("Job %s/%s: cannot stat cobaltlog file %s" % (self.jobid, self.user, self.cobalt_log_file))
                return
        except Exception, e:
            logger.exception("Job %s/%s: stat of cobaltlog file %s failed" % (self.jobid, self.user, self.cobalt_log_file))
            return
        
        try:    
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, message
            cobalt_log_file.close()
        except:
            logger.error("Job %s/%s: unable to open cobaltlog file %s" % (self.jobid, self.user, self.cobalt_log_file))

    def progress(self):
        '''Run next job step'''
        try:
            self.trigger_event('Progress')
        except:
            self.__sm_log_exception(None, "an exception occurred during a progress event")

    def run(self, nodelist):
        try:
            self.trigger_event("Run", {'nodelist' : nodelist})
        except StateMachineIllegalEventError:
            raise JobRunError("Jobs in the '%s' state may not be started." % (self.state,), self.jobid,
                self.state, self.__sm_state)
        except:
            self.__sm_log_exception(None, "an unexpected exception occurred while attempting to start the task")
            raise JobRunError("An unexpected exception occurred while attempting to start the job.  See log for details.", 
                self.jobid, self.state, self.__sm_state)

    def preempt(self, user = None, force = False):
        '''process a preemption request for a job'''
        args = {}
        if user is not None:
            args['user'] = user
        if force:
            args['force'] = True
        try:
            self.trigger_event('Preempt', args)
        except JobPreemptionError:
            raise
        except StateMachineIllegalEventError:
            raise JobPreemptionError("Jobs in the '%s' state may not be preempted." % (self.state,), self.jobid, user, force)
        except:
            self.__sm_log_exception(None, "an unexpected exception occurred while attempting to preempt the task")
            raise JobPreemptionError("An unexpected exception occurred while attempting to preempt the job.  See log for details.",
                self.jobid, user, force)

    def kill(self, user = None, signame = Signal_Map.terminate, force = False):
        '''process a user delete request for a job'''
        if user is None:
            user = self.user

        # write job delete information to CQM and accounting logs
        accounting_logger.info(accounting.delete(self.jobid, user))
        logger.info('D;%s;%s' % (self.jobid, self.user))
        self.acctlog.LogMessage('D;%s;%s' % (self.jobid, self.user))

        if not force:
            try:
                self.trigger_event('Kill', {'user' : user, 'signal' : signame})
            except:
                self.__sm_log_exception(None, "an unexpected exception occurred while attempting to kill the task")
                raise JobDeleteError("An unexpected exception occurred while attempting to delete the job.  See log for details.",
                    self.jobid, user, force, self.state, self.__sm_state)
        else:
            self.__sm_log_info(("forced delete requested by user '%s'; initiating job termination and removal of job " + \
                "from the queue") % (user,), cobalt_log = True)
            self.__signaling_info = Signal_Info(Signal_Info.Reason.delete, signame, user)
            try:
                if self.taskid != None:
                    self.__task_signal(retry = False)
            except:
                self.__sm_log_exception(None, "an exception occurred while attempting to forcibly kill the task")
                raise JobDeleteError(("An error occurred while forcibly killing the job.  The job has been removed from " + \
                    "the queue; however, resouces may not have been released.  Manual clean up may be required."),
                    self.jobid, user, force, self.state, self.__sm_state)
            finally:
                # if the job is running or has run at some point, then collect and output end of job information
                if self.__sm_state not in ('Ready', 'Hold'):
                    # stop the execution timer and get the stats
                    if self.__timers['user'].is_active:
                        self.__timers['user'].stop()
                    stats = self.__get_stats()
                    
                    # write end of job information to CQM and accounting logs
                    used_time = 0
                    for index in xrange(len(self.__locations)):
                        used_time += int(self.__timers['user'].elapsed_times[index]) * len(self.__locations[index])
                    logger.info('E;%s;%s;%s' % (self.jobid, self.user, str(used_time)))
                    self.acctlog.LogMessage('E;%s;%s;%s' % (self.jobid, self.user, str(used_time)))
                    self.endtime = str(time.time())
                    
                    optional = {}
                    if self.project:
                        optional['account'] = self.project
                    # group, session and exit_status are unknown
                    accounting_logger.info(accounting.end(self.jobid, self.user,
                        "unknown", self.jobname, self.queue,
                        self.outputdir, self.command, self.args, self.mode,
                        self.ctime, self.qtime, self.etime, self.start, self.exec_host,
                        {'ncpus':self.procs, 'nodect':self.nodes,
                         'walltime':str_elapsed_time(self.walltime * 60)},
                         "unknown", self.end, "unknown",
                        {'location':",".join([":".join(l) for l in self.__locations]),
                         'nodect':",".join([str(n) for n in self.__resource_nodects]),
                         'walltime':",".join([str_elapsed_time(t) for t in self.__timers['user'].elapsed_times])},
                        **optional))
                    
                    logger.info("Job %s/%s on %s nodes forcibly terminated by user %s. %s" % \
                        (self.jobid, self.user, self.nodes, user, stats))
                    self.acctlog.LogMessage("Job %s/%s on %s nodes forcibly terminated by user %s. %s" % \
                        (self.jobid, self.user, self.nodes, user, stats))

    def task_end(self):
        '''handle the completion of a task'''
        self.task_running = False
        self.trigger_event('Task_End')


class JobList(DataList):
    item_cls = Job
    
    def __init__(self, q):
        self.queue = q
        self.id_gen = cqm_id_gen
    
    def q_add (self, specs, callback = None, cargs = {}):
        for spec in specs:
            if "jobid" not in spec or spec['jobid'] == "*":
                spec['jobid'] = self.id_gen.next()
        return DataList.q_add(self, specs, callback, cargs)
    

class Restriction (Data):
    
    '''Restriction object'''
    
    fields = Data.fields + ["name", "type", "value"]

    __checks__ = {'maxtime':'maxwalltime', 'users':'usercheck',
                  'maxrunning':'maxuserjobs', 'mintime':'minwalltime',
                  'maxqueued':'maxqueuedjobs', 'maxusernodes':'maxusernodes',
                  'totalnodes':'maxtotalnodes'}

    def __init__(self, spec, queue=None):
        '''info could be like
        {tag:restriction, jparam:walltime, qparam:maxusertime,
        value:x, operator:op}
        how about {tag:restriction, name:name, value:x}
        myqueue is a reference to the queue that this restriction is associated
        with
        '''
        Data.__init__(self, spec)
        self.name = spec.get("name")
        if self.name in ['maxrunning', 'maxusernodes', 'totalnodes']:
            self.type = 'run'
        else:
            self.type = spec.get("type", "queue")
        self.value = spec.get("value")
        self.queue = queue
        logger.debug('created restriction %s with type %s' % (self.name, self.type))

    def maxwalltime(self, job, _=None):
        '''checks walltime of job against maxtime of queue'''
        if float(job['walltime']) <= float(self.value):
            return (True, "")
        else:
            return (False, "Walltime greater than the '%s' queue max walltime of %s" % (job['queue'], "%02d:%02d:00" % \
                (divmod(int(self.value), 60))))

    def minwalltime(self, job, _=None):
        '''limits minimum walltime for job'''
        if float(job['walltime']) >= float(self.value):
            return (True, "")
        else:
            return (False, "Walltime less than the '%s' queue min walltime of %s" % (job['queue'], "%02d:%02d:00" % \
                (divmod(int(self.value), 60))))

    def usercheck(self, job, _=None):
        '''checks if job owner is in approved user list'''
        #qusers = self.queue.users.split(':')
        qusers = self.value.split(':')
        if '*' in qusers or job['user'] in qusers:
            return (True, "")
        else:
            return (False, "You are not allowed to submit to the '%s' queue" % self.queue.name)

    def maxuserjobs(self, job, queuestate=None):
        '''limits how many jobs each user can run by checking queue state
        with potential job added'''
        userjobs = [j for j in queuestate if j.user == job.user and j.has_resources and j.queue == job['queue']]
        if len(userjobs) >= int(self.value):
            return (False, "Maxuserjobs limit reached")
        else:
            return (True, "")

    def maxqueuedjobs(self, job, _=None):
        '''limits how many jobs a user can have in the queue at a time'''
        userjobs = [j for j in self.queue.jobs if j.user == job['user']]
        if len(userjobs) >= int(self.value):
            return (False, "The limit of %s jobs per user in the '%s' queue has been reached" % (self.value, job['queue']))
        else:
            return (True, "")

    def maxusernodes(self, job, queuestate=None):
        '''limits how many nodes a single user can have running'''
        usernodes = 0
        for j in [qs for qs in queuestate if qs.user == job['user']
                  and qs.state == 'running'
                  and qs.queue == job.queue]:
            usernodes = usernodes + int(j.nodes)
        if usernodes + int(job['nodes']) > int(self.value):
            return (False, "Job exceeds MaxUserNodes limit")
        else:
            return (True, "")

    def maxtotalnodes(self, job, queuestate=None):
        '''limits how many total nodes can be used by jobs running in
        this queue'''
        totalnodes = 0
        for j in [qs for qs in queuestate if qs.state == 'running'
                  and qs.queue == job['queue']]:
            totalnodes = totalnodes + int(j.nodes)
        if totalnodes + int(job['nodes']) > int(self.value):
            return (False, "Job exceeds MaxTotalNodes limit")
        else:
            return (True, "")

    def CanAccept(self, job, queuestate=None):
        '''Checks if this object will allow the job'''
        logger.debug('checking restriction %s' % self.name)
        func = getattr(self, self.__checks__[self.name])
        return func(job, queuestate)


class RestrictionDict(DataDict):
    item_cls = Restriction
    key = "name"


def dexpr(daystr):
    if '-' in daystr:
        dmin, dmax = map(int, daystr.split('-', 1))
        return dmin <= time.localtime()[6] <= dmax
    else:
        return int(daystr) == time.localtime()[6]

def hexpr(hstr):
    if '-' in hstr:
        hmin, hmax = map(int, hstr.split('-', 1))
        return hmin <= time.localtime()[3] <= hmax
    else:
        return int(hstr) == time.localtime()[3]

def cronmatch(pattern):
    '''match cron setting with current TOD'''
    # cron format is d-d,d:h-h
    (day, hour) = pattern.split(':', 1)
    if True in \
       [dexpr(dstr) for dstr in day.split(',')] and \
       True in \
       [hexpr(hstr) for hstr in hour.split(',')]:
        return True
    else:
        return False


class Queue (Data):
    '''queue object, subs JobSet and Data, which gives us:
       self is a Queue object (with restrictions and stuff)
       self.data is a list of Job objects'''
    
    fields = Data.fields + ["cron", "name", "state", "adminemail", "policy", "maxuserjobs",] + Restriction.__checks__.keys()
    explicit = Restriction.__checks__.keys()

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.cron = spec.get("cron")
        self.name = spec.get("name")
        self.state = spec.get("state", "stopped")
        self.adminemail = spec.get("adminemail", None)
        self.policy = spec.get("policy", "default")
        self.maxuserjobs = spec.get("maxuserjobs")
        self.priority = spec.get("priority", 0)
        self.jobs = JobList(self)
        self.restrictions = RestrictionDict()
    
    def _get_smartstate (self):
        if self.cron:
            if cronmatch(self.cron):
                return "running"
            else:
                return "stopped"
        else:
            return self.state
    smartstate = property(_get_smartstate)
    
    def can_queue(self, spec):
        # check if queue is dead or draining
        if self.state in ['draining', 'dead']:
            raise QueueError, "The '%s' queue is %s" % (self.name, self.state)

        # test job against queue restrictions
        probs = ''
        for restriction in [r for r in self.restrictions.itervalues() if r.type == 'queue']:
            result = restriction.CanAccept(spec)
            if not result[0]:
                probs = probs + result[1] + '\n'
        if probs:
            raise QueueError, probs
        else:
            return (True, probs)

    def update_max_running(self):
        '''In order to keep the max_running property of jobs up to date, this function needs
        to be called when a job starts running, or a new job appears in a queue.'''
        
        if not self.restrictions.has_key("maxrunning"):
            # if it *was* there and was removed, we better clean up
            for job in self.jobs:
                job.max_running = False
            return
        unum = dict()
        for job in self.jobs.q_get([{'has_resources':True}]):
            if job.user not in unum:
                unum[job.user] = 1
            else:
                unum[job.user] = unum[job.user] + 1

        for job in self.jobs:
            job.max_running = False
            if unum.get(job.user, 0) >= int(self.restrictions["maxrunning"].value):
                if not job.has_resources:
                    job.max_running = True


class QueueDict(DataDict):
    item_cls = Queue
    key = "name"
    
    def add_queues(self, specs, callback=None, cargs={}):
        return self.q_add(specs, callback, cargs)

    def get_queues(self, specs, callback=None, cargs={}):
        return self.q_get(specs, callback, cargs)
    
    def can_queue(self, spec):
        '''Check that job meets criteria of the specified queue'''
        # if queue doesn't exist, don't check other restrictions
        if spec['queue'] not in [q.name for q in self.itervalues()]:
            raise QueueError, "Queue '%s' does not exist" % spec['queue']

        [testqueue] = [q for q in self.itervalues() if q.name == spec['queue']]

        return testqueue.can_queue(spec)

    def del_queues(self, specs, callback=None, cargs={}):
        return self.q_del(specs, callback, cargs)
        
    def add_jobs(self, specs, callback=None, cargs={}):
        queue_names = self.keys()
        
        failed = False
        for spec in specs:
            if spec['queue'] not in queue_names:
                logger.error("trying to add job to non-existant queue %s" % spec['queue'])
                failed = True
            if not self.can_queue(spec)[0]:
                logger.error("job %r cannot be added to queue" % spec)
                failed = True
        results = []
        if failed:
            return results
        
        # we know all of the queues exist, so add the jobs to the appropriate JobList
        for spec in specs:
            results += self[spec['queue']].jobs.q_add([spec], callback, cargs)
            self[spec['queue']].update_max_running()
            
        return results
    
    def get_jobs(self, specs, callback=None, cargs={}):
        results = []
        for q in self.itervalues():
            results += q.jobs.q_get(specs, callback, cargs)

        return results
        
    def del_jobs(self, specs, callback=None, cargs={}):
        results = []
        for q in self.itervalues():
            results += q.jobs.q_del(specs, callback, cargs)
            
        return results


class QueueManager(Component):
    '''Cobalt Queue Manager'''

    implementation = 'cqm'
    name = 'queue-manager'

    logger = logger

    __statefields__ = ['Queues']
    
    def __init__(self, *args, **kwargs):
        self.Queues = QueueDict()
        Component.__init__(self, *args, **kwargs)
        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.cqp = Cobalt.Cqparse.CobaltLogParser()
        self.id_gen = IncrID()
        global cqm_id_gen
        cqm_id_gen = self.id_gen
        
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}

        self.define_builtin_utility_functions()
        self.define_user_utility_functions()


    def __getstate__(self):
        return {'Queues':self.Queues, 'next_job_id':self.id_gen.idnum+1, 'version':3}
                
    def __setstate__(self, state):
        self.Queues = state['Queues']
        self.id_gen = IncrID()
        self.id_gen.set(state['next_job_id'])
        global cqm_id_gen
        cqm_id_gen = self.id_gen
        
        for q in self.Queues.values():
            q.jobs.id_gen = self.id_gen
        
        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.cqp = Cobalt.Cqparse.CobaltLogParser()
        self.lock = Lock()
        self.statistics = Statistics()
        
        self.user_utility_functions = {}
        self.builtin_utility_functions = {}

        self.define_builtin_utility_functions()
        self.define_user_utility_functions()


    def __save_me(self):
        Component.save(self)
    __save_me = automatic(__save_me, float(get_cqm_config('save_me_interval', 10)))
        
    def __progress(self):
        '''Process asynchronous job work'''
        [job.progress() for queue in self.Queues.itervalues() for job in queue.jobs]

        # enforce the maxrunning queue attribute (HACK ALERT)
        for queue in self.Queues.itervalues():
            queue.update_max_running()
                            
        for (name, q) in self.Queues.items():
            if q.state == 'dead' and q.name.startswith('R.') and not q.jobs:
                del self.Queues[name]

        return 1

    __progress = automatic(__progress, float(get_cqm_config('progress_interval', 10)))

    def __poll_process_groups (self):
        '''Resynchronize with the system'''
        
        try:
            pgroups = ComponentProxy("system").get_process_groups([{'id':'*', 'state':'running'}])
        except (ComponentLookupError, xmlrpclib.Fault):
            logger.error("Failed to communicate with the system component when attempting to acquire a list of active " + \
                "process groups")
            return

        self.lock.acquire()
        try:
            live = [item['id'] for item in pgroups]
            for job in [j for queue in self.Queues.itervalues() for j in queue.jobs]:
                if job.task_running and job.taskid not in live:
                    logger.info("Job %s/%s: process group no longer executing" % (job.jobid, job.user))
                    job.task_end()
        finally:
            self.lock.release()
    __poll_process_groups = locking(automatic(__poll_process_groups, float(get_cqm_config('poll_process_groups_interval', 10))))

    #
    # job operations
    #
    def set_jobid(self, jobid):
        '''Set next jobid for new job'''
        self.id_gen.set(jobid)
        # print "self : ", self.id_gen.idnum
        # print "module : ", cqm_id_gen.idnum
        return True
    set_jobid = exposed(set_jobid)

    def __job_terminal_action(self, args):
        '''job terminal action routine that handles updating dependency information and removing the job from the queue'''
        job = args['job']

        # if the job exited cleanly, then update dependency information for jobs that depended on this one
        #
        # NOTE: this assumes that the system component will return a non-zero exit status if the task was killed by a signal.
        # 'None' is considered to be non-zero and thus would be a valid exit status if the task was terminated.
        if job.exit_status == 0:
            for waiting_job in self.Queues.get_jobs([{'state':"dep_hold"}]):
                if str(job.jobid) in waiting_job.all_dependencies:
                    waiting_job.satisfied_dependencies.append(str(job.jobid))
                    
                    if sets.Set(waiting_job.all_dependencies).issubset(sets.Set(waiting_job.satisfied_dependencies)):
                        waiting_job.score = max(waiting_job.score, float(get_cqm_config('dep_frac', 0.5))*job.score)

        # remove the job from the queue
        #
        # BRT: it seems somewhat silly to use q_del() which searches for the job object to which we already have a reference.
        # could "job.queue.jobs.remove(job)" be used instead or would that make an inappropriate assumption about the
        # implementation of the JobList/DataList?
        self.Queues[job.queue].jobs.q_del([{'jobid':job.jobid}])

        # update state of jobs held because the user exceeded the maximum number of running jobs allowed by the queue
        self.Queues[job.queue].update_max_running()

    def __add_job_terminal_action(self, job, args):
        '''add the terminal action handler to the each job added to the queue'''
        job.add_terminal_action(self.__job_terminal_action, {'job':job})

    def add_jobs(self, specs):
        '''Add a job, throws in adminemail'''

        queue_names = self.Queues.keys()
        
        failed = False
        for spec in specs:
            if spec['queue'] in self.Queues:
                spec.update({'adminemail':self.Queues[spec['queue']].adminemail})
            else:
                failure_msg = "trying to add job to non-existant queue '%s'" % spec['queue']
                logger.error(failure_msg)
                failed = True
        if failed:
            raise QueueError, failure_msg
        
        response = self.Queues.add_jobs(specs, self.__add_job_terminal_action)
        return response
    add_jobs = exposed(query(add_jobs))

    def get_jobs(self, specs):
        return self.Queues.get_jobs(specs)
    get_jobs = exposed(query(get_jobs))

    def set_jobs(self, specs, updates):
        def _set_jobs(job, newattr):
            test = job.to_rx()
            test.update(newattr)
            #if update "user_hold" alone, do not check MaxQueued restriction
            if newattr.keys() == ['user_hold']:            
                job.update(newattr)
            elif self.Queues[job.queue].can_queue(test):
                job.update(newattr)
        return self.Queues.get_jobs(specs, _set_jobs, updates)
    set_jobs = exposed(query(set_jobs))

    def move_jobs(self, specs, new_q_name):
        if new_q_name not in self.Queues:
            logger.error("attempted to move a job to non-existent queue '%s'" % new_q_name)
            raise QueueError, "Error: queue '%s' does not exist" % new_q_name
        new_q = self.Queues[new_q_name]
        
        for job in self.Queues.get_jobs(specs):
            if job.queue == new_q_name:
                raise QueueError, "job %d already in queue '%s'" % (job.jobid, new_q_name)
            if job.is_active or job.has_completed:
                raise QueueError, "job %d is running; it cannot be moved" % job.jobid   
        
        results = []
        for q in self.Queues.itervalues():
            # don't look in the target queue.  you'll go blind.
            if q.name == new_q_name:
                continue
            
            movelist = []
            for job in q.jobs.q_get(specs):
                if new_q.can_queue(job.to_rx()):
                    movelist.append(job)
                else:
                    logger.error("attempted to move a job to queue'%s' which will not accept it" % new_q_name)
                    raise QueueError, "Error: queue '%s' will not accept job %r" % (new_q_name, job.to_rx())
                    
            for job in movelist:
                q.jobs.remove(job)
                job.queue = new_q.name
                new_q.jobs.append(job)
                results.append(job)
                new_q.update_max_running()
        return results
    move_jobs = exposed(query(move_jobs))

    def run_jobs(self, specs, nodelist):
        def _run_jobs(job, nodes):
            job.run(nodes)
            self.Queues[job.queue].update_max_running()
        return self.Queues.get_jobs(specs, _run_jobs, nodelist)
    run_jobs = exposed(query(run_jobs))

    def preempt_jobs(self, specs, user = None, force = False):
        def _preempt_jobs(job, args):
            job.preempt(user, force)
        return self.Queues.get_jobs(specs, _preempt_jobs)
    preempt_jobs = exposed(query(preempt_jobs))

    def del_jobs(self, specs, force = False, user = None, signame = Signal_Map.terminate):
        '''Delete a job'''
        ret = []
        for spec in specs:
            for job, q in [(job, queue) for queue in self.Queues.itervalues() for job in queue.jobs if job.match(spec)]:
                ret.append(job)
                job.kill(user, signame, force)
                if force:
                    self.__job_terminal_action({'job':job})
        return ret
    del_jobs = exposed(query(del_jobs))

    #
    # queue operations
    #
    def add_queues(self, specs):
        return self.Queues.add_queues(specs)
    add_queues = exposed(query(add_queues))
    
    def get_queues(self, specs):
        return self.Queues.get_queues(specs)
    get_queues = exposed(query(get_queues))

    def can_queue(self, job_spec):
        return self.Queues.can_queue(job_spec)
    can_queue = exposed(can_queue)

    def set_queues(self, specs, updates):
        def _setQueues(queue, newattr):
            if 'priority' in newattr:
                if newattr['priority'] is None:
                    newattr['priority'] = 0
                else:
                    try:
                        newattr['priority'] = int(newattr['priority'])
                    except ValueError:
                        raise QueueError("%s is not a valid queue priority" % newattr['priority'])
            queue.update(newattr)
            for key in newattr:
                if key in Restriction.__checks__:
                    if newattr[key] is None and queue.restrictions.has_key(key):
                        del queue.restrictions[key]
                    elif newattr[key] is not None:
                        queue.restrictions[key] = Restriction({'name':key, 'value':newattr[key]}, queue)
        return self.Queues.get_queues(specs, _setQueues, updates)
    set_queues = exposed(query(set_queues))

    def del_queues(self, specs, force = False):
        '''Delete queue(s), but check if there are still jobs in the queue'''
        if force:
            return self.Queues.del_queues(specs)

        queues = self.Queues.get_queues(specs)
        
        failed = []
        for queue in queues[:]:
            jobs = queue.jobs.q_get([{'tag':"job"}])
            if len(jobs) > 0:
                failed.append(queue.name)
                queues.remove(queue)
        response = []
        if len(queues) > 0:
            response = self.Queues.del_queues([queue.to_rx() for queue in queues])
        if failed:
            raise QueueError, ("The %s queue(s) contains jobs. Either move the jobs to another queue, or \n" + \
                "use 'cqadm -f --delq' to delete the queue(s) and the jobs.\n\nDeleted Queues\n================\n%s") % \
                (",".join(failed), "\n".join([q.name for q in response]))
        else:
            return response
    del_queues = exposed(query(del_queues))

    def get_history(self, data):
        '''Fetches queue history from acct log'''
        self.cqp.perform_default_parse()
        return self.cqp.q_get(data)
    get_history = exposed(get_history)



    def define_user_utility_functions(self):
        self.logger.info("building user utility functions")
        self.user_utility_functions.clear()
        filename = os.path.expandvars(get_bgsched_config("utility_file", ""))
        try:
            f = open(filename)
        except:
            self.logger.error("Can't read utility function definitions from file %s" % get_bgsched_config("utility_file", ""))
            return
        
        str = f.read()
        
        try:
            code = compile(str, filename, 'exec')
        except:
            self.logger.error("Problem compiling utility function definitions.", exc_info=True)
            return
        
        globals = {'math':math, 'time':time}
        locals = {}
        try:
            exec code in globals, locals
        except:
            self.logger.error("Problem executing utility function definitions.", exc_info=True)
            
        for thing in locals.values():
            if type(thing) is types.FunctionType:
                if thing.func_name in self.builtin_utility_functions:
                    self.logger.error("Attempting to overwrite builtin utility function '%s'.  User version discarded." % \
                        thing.func_name)
                else:
                    self.user_utility_functions[thing.func_name] = thing
    define_user_utility_functions = exposed(define_user_utility_functions)
    
    def adjust_job_scores(self, specs, score):
        if score[0] in ["-", "+"]:
            absolute = False
        else:
            absolute = True
        
        delta = float(score)
        
        results = []    
        for job in self.Queues.get_jobs(specs):
            if absolute:
                job.score = delta
            else:
                job.score += delta
            results.append(job.jobid)
        
        return results
    adjust_job_scores = exposed(adjust_job_scores)
            
    def define_builtin_utility_functions(self):
        self.logger.info("building builtin utility functions")
        self.builtin_utility_functions.clear()
        
        # I think this duplicates cobalt's old scheduling policy
        # higher queue priorities win, with jobid being the tie breaker
        def default():
            val = queue_priority + 0.1
            return val
    
        def high_prio():
            val = 1.0
            return val
    
        self.builtin_utility_functions["default"] = default
        self.builtin_utility_functions["high_prio"] = high_prio
        
        
    def compute_utility_scores (self):
        utility_scores = []
        current_time = time.time()
            
        for job in self.Queues.get_jobs([{'is_runnable':True}]):    
            utility_name = self.Queues[job.queue].policy
            args = {'queued_time':current_time - float(job.submittime), 
                    'wall_time': 60*float(job.walltime), 
                    'size': float(job.nodes),
                    'user_name': job.user,
                    'project': job.project,
                    'queue_priority': int(self.Queues[job.queue].priority),
                    #'machine_size': max_nodes,
                    'jobid': int(job.jobid),
                    'score': job.score,
                    'state': job.state,
                    }
            try:
                if utility_name in self.builtin_utility_functions:
                    utility_func = self.builtin_utility_functions[utility_name]
                else:
                    utility_func = self.user_utility_functions[utility_name]
                utility_func.func_globals.update(args)
                score = utility_func()
            except KeyError:
                # do something sensible when the requested utility function doesn't exist
                # probably go back to the "default" one
                
                # and if we get here, try to fix it and throw away this scheduling iteration
                self.logger.error("cannot find utility function '%s' named by queue '%s'" % (utility_name, job.queue))
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
            except:
                # do something sensible when the requested utility function explodes
                # probably go back to the "default" one
                
                # and if we get here, try to fix it and throw away this scheduling iteration
                self.logger.error("error while executing utility function '%s' named by queue '%s'" % (utility_name, job.queue), \
                    exc_info=True)
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return
            
            try:
                job.score += score
            except:
                self.logger.error("utility function '%s' named by queue '%s' returned a non-number" % (utility_name, job.queue), \
                    exc_info=True)
                self.user_utility_functions[utility_name] = self.builtin_utility_functions["default"]
                self.logger.error("falling back to 'default' policy to replace '%s'" % utility_name)
                return

    compute_utility_scores = automatic(compute_utility_scores, float(get_cqm_config('compute_utility_interval', 10)))
