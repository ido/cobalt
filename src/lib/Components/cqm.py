#!/usr/bin/env python
# $Id$

'''Cobalt Queue Manager'''
__revision__ = '$Revision$'

import logging
import os
import sys
import time
import xmlrpclib
import ConfigParser
import sets

import Cobalt
import Cobalt.Util
import Cobalt.Cqparse
from Cobalt.Data import Data, DataList, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import TimerException, QueueError, ComponentLookupError


logger = logging.getLogger('cqm')
cqm_id_gen = None

class Timer(object):
    '''The timer object keeps track of elapsed times for jobs'''
    def __init__(self):
        self.start = 0
        self.stop = 0
    
    def Start(self):
        '''Begin time tracking'''
        self.start = time.time()
        
    def Stop(self):
        '''Stop time tracking'''
        self.stop = time.time()
        
    def Check(self):
        '''Check length of time measured (will return elapsed if still active)'''
        if not self.start:
            raise TimerException, "NotStarted"
        if not self.stop:
            return time.time() - self.start
        return self.stop - self.start

class Job (Data):
    '''BG Job is a Blue Gene/L job'''
    
    
    _configfields = ['bgkernel']
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('cqm'):
        print '''"cqm" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['cqm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        sys.exit(1)
    if config.get("bgkernel") == 'true':
        for param in ['partitionboot', 'bootprofiles']:
            if config.get(param, 'nothere') == 'nothere':
                print "Missing option in cobalt config file: %s." % (param)
                print "This is required only if dynamic kernel support is enabled"
                sys.exit(1)

    acctlog = Cobalt.Util.AccountingLog('qm')
    
    fields = Data.fields + [
        "jobid", "jobname", "state", "attribute", "location", "starttime",
        "submittime", "endtime", "queue", "type", "user", "walltime",
        "procs", "nodes", "mode", "cwd", "command", "args", "outputdir",
        "project", "lienID", "exit_status", "stagein", "stageout",
        "reservation", "host", "port", "url", "stageid", "envs", "inputfile",
        "kerneloptions", "system_state", "user_state", "dependencies",
        "bgkernel", "kernel", "notify", "adminemail", "outputpath", 
        "errorpath", "path", 
    ]


    def __init__(self, spec):
        Data.__init__(self, spec)
        
        # __setattr__ is going to try to refer to this, so we better build it first
        self.timers = dict(
            queue = Timer(),
            current_queue = Timer(),
            user = Timer(),
        )

        self.jobid = spec.get("jobid")
        self.jobname = spec.get("jobname", "N/A")
        
        self.system_state = spec.get("system_state", "ready")
        self.user_state = spec.get("user_state", "ready")
        self.job_step = None
        
        self.submit_command = spec.get("submit_command")
        self.attribute = spec.get("attribute", "compute")
        self.starttime = spec.get("starttime", "-1")
        self.submittime = spec.get("submittime", time.time())
        self.endtime = spec.get("endtime", "-1")
        self.queue = spec.get("queue", "default")
        self.type = spec.get("type", "mpish")
        self.user = spec.get("user")
        self.walltime = spec.get("walltime")
        self.procs = spec.get("procs")
        self.nodes = spec.get("nodes")
        self.cwd = spec.get("cwd")
        self.command = spec.get("command")
        self.args = spec.get("args")
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
        self.kerneloptions = spec.get("kerneloptions")
        self.tag = spec.get("tag", "job")
        
        self.all_dependencies = spec.get("all_dependencies")
        if self.all_dependencies:
            self.all_dependencies = self.all_dependencies.split(":")
        else:
            self.all_dependencies = []
        self.satisfied_dependencies = []

        self.max_running = False
        
        self.bgkernel = spec.get("bgkernel")
        self.kernel = spec.get("kernel", "default")
        self.notify = spec.get("notify")
        self.adminemail = spec.get("adminemail")
        self.location = spec.get("location")
        self.outputpath = spec.get("outputpath")
        if self.outputpath:
            jname = self.outputpath.split('/')[-1].split('.output')[0]
            if jname and jname != str(self.jobid):
                self.jobname = jname
        self.outputdir = spec.get("outputdir")
        self.errorpath = spec.get("errorpath")
        self.cobalt_log_file = spec.get("cobalt_log_file")
        self.path = spec.get("path")
        self.mode = spec.get("mode", "co")
        self.envs = spec.get("envs", {})
        self.exit_status = spec.get("exit_status")


        self.timers['queue'].Start()
        self.timers['current_queue'].Start()
        self.staged = 0
        self.killed = False
        self.pgid = {}
        self.spgid = {}

        if self.notify or self.adminemail:
            self.steps = ['NotifyAtStart', 'RunBGUserJob', 'NotifyAtEnd', 'FinishUserPgrp', 'Finish']
        else:
            self.steps = ['RunBGUserJob', 'FinishUserPgrp', 'Finish']
        if self.config.get('bgkernel') == 'true':
            self.steps.insert(0, 'SetBGKernel')
        self.SetPassive()
        
        # acctlog
        self.pbslog = Cobalt.Util.PBSLog(self.jobid)
        logger.info(
            'Q;%s;%s;%s' % (self.jobid, self.user, self.queue))
        self.acctlog.LogMessage(
            'Q;%s;%s;%s' % (self.jobid, self.user, self.queue))
    
    def _get_job_state(self):
        if self.all_dependencies:
            if not sets.Set(self.all_dependencies).issubset(sets.Set(self.satisfied_dependencies)):
                return "dependency hold"
        
        if self.max_running:
            return "MaxRunning hold"
        
        if self.system_state == "ready":
            if self.user_state == "ready":
                return "queued"
            else:
                return "user " + self.user_state
        elif self.system_state == "running":
            return "running - %s" % self.job_step
        elif self.system_state == "hold":
            return "admin hold"
    state = property(_get_job_state)
    
    def _get_dependencies(self):
        ret = ""
        for dep in self.all_dependencies:
            ret += dep
            if dep in self.satisfied_dependencies:
                ret += "*"
            ret += ", "
        
        ret = ret[:-2]    
        return ret
    dependencies = property(_get_dependencies)
    
    def __setattr__ (self, name, value):
        if name == "state":
            if value == "hold":
                self.timers['hold'] = Timer()
                self.timers['hold'].Start()
            elif getattr(self, "state", None) == "hold":
                self.timers['hold'].Stop()
        return Cobalt.Data.Data.__setattr__(self, name, value)
    
    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['log', 'comms', 'acctlog', 'pbslog']:
                data[key] = value
        return data

    def __setstate__(self, state):
        self.__dict__.update(state)
        if not self.timers.has_key('current_queue'):
            self.timers['current_queue'] = Timer()
            self.timers['current_queue'].Start()
        #self.acctlog = Cobalt.Util.AccountingLog('qm')
        self.pbslog = Cobalt.Util.PBSLog(self.jobid)
    
    def _get_etime (self):
        try:
            return self.timers['hold'].stop # job became eligible at end of last hold
        except KeyError:
            return self.timers['queue'].start # job has always been eligible to run
    etime = property(_get_etime)
    
    def LogStart (self):
        def len2 (input):
            input = str(input)
            if len(input) == 1:
                return "0" + input
            else:
                return input
        
        walltime_minutes = len2(int(float(self.walltime)) % 60)
        walltime_hours = len2(int(float(self.walltime)) // 60)
        
        self.pbslog.log("S",
            user = self.user, # the user name under which the job will execute
            #group = , # the group name under which the job will execute
            jobname = self.jobname, # the name of the job
            queue = self.queue, # the name of the queue in which the job resides
            ctime = self.timers['queue'].start, # time in seconds when job was created (first submitted)
            qtime = self.timers['current_queue'].start, # time in seconds when job was queued into current queue
            etime = self.etime, # time in seconds when job became eligible to run; no holds, etc.
            start = self.timers['user'].start, # time in seconds when job execution started
            exec_host = self.location, # name of host on which the job is being executed (location is a :-separated list of nodes)
            #Resource_List__dot__RES = , # limit for use of RES
            Resource_List__dot__ncpus = self.procs, # max number of cpus
            Resource_List__dot__nodect = self.nodes, # max number of nodes
            #Resource_List__dot__nodes = , # 6:ppn=4
            #Resource_List__dot__place = , # scatter
            #Resource_List__dot__select = , # 6:ncpus=4
            Resource_List__dot__walltime = "%s:%s:00" % (walltime_hours, walltime_minutes),
            #session = , # session number of job
            #accountint_id = , # identifier associated with system-generated accounting data
            mode = self.mode,
            cwd = self.cwd,
            exe = self.command,
            args = " ".join(self.args),
        )

    def SetActive(self):
        '''set job info active mode'''
        self.active = True

    def SetPassive(self):
        '''set job into passive mode'''
        self.active = False
        
    def Finish(self):
        '''Finish up accounting for job, also adds postscript ability'''
        used_time = int(self.timers['user'].Check()) * len(self.location.split(':'))
                                                                
        self.job_step = "done"
        self.SetPassive()
        #AddEvent("queue-manager", "job-completed", self.jobid)
        # acctlog
        logger.info('E;%s;%s;%s' % \
                    (self.jobid, self.user, str(used_time)))
        self.acctlog.LogMessage('E;%s;%s;%s' % \
                                (self.jobid, self.user, str(used_time)))
        self.endtime = str(time.time())


        if self.config.get('bgkernel') == 'true':
            try:
                os.unlink('%s/%s' % (self.config.get('partitionboot'), self.location))
                os.symlink('%s/%s' % (self.config.get('bootprofiles'), 'default'),
                           '%s/%s' % (self.config.get('partitionboot'), self.location))
            except OSError:
                logger.error("Failed to reset boot location at job end for partition for %s" % (self.location))

        if self.config.get('postscript'):
            postscripts = self.config.get('postscript').split(':')
            extra = []
            for field in self.fields:
                fdata = getattr(self, field)
                if isinstance(fdata, list):
                    extra.append('%s="%s"' % (field, ':'.join(fdata)))
                elif isinstance(fdata, dict):
                    extra.append('%s="{%s}"' % (field, str(fdata)))
                else:
                    extra.append('%s="%s"' % (field, fdata))
            for p in postscripts:
                try:
                    rc, out, err = Cobalt.Util.runcommand("%s %s" % (p, " ".join(extra)))
                    if rc != 0:
                        logger.info("Job %s/%s: return of postscript %s was %d, error message is %s" %
                                     (self.jobid, self.user, p, rc, "\n".join(err)))
                except Exception, e:
                    logger.info("Job %s/%s: exception with postscript %s, error is %s" %
                                 (self.jobid, self.user, p, e))



    def Progress(self):
        '''Run next job step'''
        if not self.steps:
            logger.error("Manually setting passive for job %s" % (self.jobid))
            self.SetPassive()
            return
        logger.info("Job %s/%s: running step %s" % (self.jobid, self.user, self.steps[0]))
        currentstep = self.steps[0]
        try:
            getattr(self, self.steps[0])()
        except:
            logger.error("Unexpected failure jobid:%s step:%s" % (self.jobid, currentstep),
                         exc_info=1)
            self.SetPassive()
            return

        if len(self.steps) > 1:
            self.steps = self.steps[1:]
        else:
            self.job_state = "done"
            
    def Run(self, nodelist):
        '''Run a job'''
        if self.system_state == "running":
            logger.info("Got multiple run commands for job %s" % self.jobid)
            return
        self.timers['queue'].Stop()
        self.timers['current_queue'].Stop()
        if self.reservation:
            # acctlog
            logger.info('R;%s;%s;%s' % \
                        (self.jobid, self.queue, self.user))
            self.acctlog.LogMessage('R;%s;%s;%s' % \
                                    (self.jobid, self.queue, self.user))
        else:
            # acctlog
            logger.info('S;%s;%s;%s;%s;%s;%s;%s' % (
                self.jobid, self.user, self.jobname,
                self.nodes, self.procs, self.mode,
                self.walltime))
            self.acctlog.LogMessage('S;%s;%s;%s;%s;%s;%s;%s' % (
                self.jobid, self.user, self.jobname,
                self.nodes, self.procs, self.mode,
                self.walltime))
        self.location = ":".join(nodelist)
        self.system_state = "running"
        self.job_step = "starting"
        self.starttime = str(time.time())
        self.SetActive()
        if self.project:
            logger.info("Job %s/%s/%s/Q:%s: Running job on %s" % \
                                    (self.jobid, self.user,
                                     self.project, self.queue,
                                     ":".join(nodelist)))
            self.acctlog.LogMessage("Job %s/%s/%s/Q:%s: Running job on %s" % \
                                    (self.jobid, self.user,
                                     self.project, self.queue,
                                     ":".join(nodelist)))
        else:
            logger.info("Job %s/%s/Q:%s: Running job on %s" % \
                        (self.jobid, self.user,
                         self.queue, ":".join(nodelist)))
            self.acctlog.LogMessage("Job %s/%s/Q:%s: Running job on %s" % \
                                    (self.jobid, self.user,
                                     self.queue, ":".join(nodelist)))

    def FinishUserPgrp(self):
        '''Complete a process group for the user job'''
        self.timers['user'].Stop()
        if self.spgid.has_key('user'):
            try:
                #pgroups = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'output':'*', 'error':'*'}])
                if self.mode == 'script':
                    result = ComponentProxy("script-manager").wait_jobs([{'id':self.spgid['user'], 'exit_status':'*'}])
                else:
                    result = ComponentProxy("system").wait_process_groups([{'id':self.spgid['user'], 'exit_status':'*'}])
                if result:
                    self.exit_status = result[0].get('exit_status')
                #this seems needed to get the info back into the object so it can be handed back to the filestager.
                #self.output = pgroups[0]['output']
                #self.error = pgroups[0]['error']
            except (ComponentLookupError, xmlrpclib.Fault):
                logger.error("Error contacting the system for finalize, requeueing")
                self.steps = ['FinishUserPgrp'] + self.steps
                self.SetActive()
                return
            except:
                logger.error("Unexpected error finalizing process group", exc_info=1)
                self.SetPassive()
                return
        else:
            logger.error("No record of pgid for user job %s" % (self.jobid))
        self.SetActive()


    def Kill(self, killmsg):
        '''Kill a job'''
        if self.killed == True:
            return
        self.killed = True
        logger.info(killmsg % (self.jobid))
        if self.state in ['epilogue', 'cleanup']:
            logger.info("Not killing job %s during recovery" % (self.jobid))
        elif self.system_state == 'running':
            if not self.pgid.has_key('user'):
                logger.error("Job %s has no pgroup associated with it" % self.jobid)
            else:
                self.killed = self.KillPGID(self.pgid['user'])
        elif self.system_state == 'hold':  #job in 'hold' and running
            self.killed = self.KillPGID(self.pgid['user'])
        else:
            logger.error("Got qdel for job %s in unexpected state %s" % (self.jobid, self.state))
 

    def CompletePG(self, pgid):
        '''Finish accounting for a completed jobid'''
        for (t, pg) in [item for item in self.pgid.iteritems() if item[1] == pgid]:
            logger.info("Job %s/%s: %s completed" % (self.jobid, self.user, t))
            self.spgid[t] = self.pgid[t]
            del self.pgid[t]
            self.timers[t].Stop()
            self.SetActive()
            return
        raise KeyError, pgid

    def KillPGID(self, pgid):
        '''Kill a process group'''
        
        self.job_step = "killing"
        
        if self.mode == 'script':
            try:
                pgroup = ComponentProxy("script-manager").signal_jobs([{'id':pgid}], "SIGTERM")
            except (ComponentLookupError, xmlrpclib.Fault):
                logger.error("Failed to communicate with script manager when killing job")
                return False
        else:
            try:
                pgroup = ComponentProxy("system").signal_process_groups([{'id':pgid}], "SIGTERM")
            except ComponentLookupError:
                logger.error("Failed to communicate with the system when killing job")
                return False

        return True

    def over_time(self):
        '''Check if a job has run over its time'''
        if self.system_state == 'running' and self.job_step != "starting":
            runtime = self.timers['user'].Check()/60.0
            if float(self.walltime) < runtime:
                return 1
        return 0

#     # Here begins the testbed stuff
#     def StartRebuild(self):
#         self.Rebuild(self.image, self.kernel)

#     def CleanUpRebuild(self):
#         #self.Rebuild(defaultimage, defaultkernel)
#         pass

#     def Rebuild(self, image, kernel):
#         # send a message to the build system starting rebuild
#         self.built = 0
#         self.booted = 0
#         # send the message to the build system
#         h = comm.ClientInit("build-system")
#         i = comm.ClientInit("cluster-hardware")
#         for node in self.nodelist:
#             comm.SendMessage(h, "<set-node-software image='%s' kernel='%s' action='build'>
# <node-software node='%s'/></set-node-software>" % (image, kernel, node))
#             comm.SendMessage(i, "<power-control type='reboot'>
# <node-hardware node='%s'/></power-control>" % (node))
#             r = comm.RecvMessage(h)
#             r = comm.RecvMessage(i)
#         comm.ClientClose(h)
#         comm.ClientClose(i)
#         self.steps = ["BuildWait"] + self.steps
#         self.SetPassive()

#     def BuildWait(self):
#         if not ((self.built >= 2 * int(self.nodes)) and (self.booted >= 2 * int(self.nodes))):
#             self.steps = ["BuildWait"] + self.steps
#             self.SetPassive()
#         else:
#             self.SetActive()

    def GetStats(self):
        '''Get job execution statistics from timers'''
        result = ''
        for (name, timer) in self.timers.iteritems():
            try:
                result += "%s:%.02fs " % (name, timer.Check())
            except Exception, mmsg:
                logger.error("timer: %s wasn't started" % name)
                print mmsg
        return result

    def LogFinish(self):
        '''Log end of job data, specific for BG/L exit status'''
        exit_status = self.exit_status
        try:
            exit_status = exit_status.get('BG/L')
            exit_status = int(exit_status)/256
        except:
            pass
        logger.info("Job %s/%s on %s nodes done. %s" % \
                    (self.jobid, self.user,
                     self.nodes, self.GetStats()))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit:%s" % \
                                (self.jobid, self.user,
                                 self.nodes, self.GetStats(),
                                 str(exit_status)))
        self.LogFinishPBS()
        
    def LogFinishPBS (self):
        def len2 (input):
            input = str(input)
            if len(input) == 1:
                return "0" + input
            else:
                return input
        
        req_walltime_minutes = len2(int(float(self.walltime)) % 60)
        req_walltime_hours = len2(int(float(self.walltime)) // 60)
        
        runtime = int(self.timers['user'].Check())
        walltime_seconds = len2(runtime % (60))
        walltime_minutes = len2(runtime % (60 * 60) // 60)
        walltime_hours = len2(runtime // (60 * 60))
        
        optional_pbs_data = dict()
        try:
            optional_pbs_data['account'] = self.project # if job has an "account name" string
        except KeyError:
            pass
        
        self.pbslog.log("E",
            user = self.user, # the user name under which the job executed
            #group = , # the group name under which the job executed
            #account = , # if job has an "account name" string
            jobname = self.jobname, # the name of the job
            queue = self.queue, # the name of the queue in which the job executed
            #resvname = , # the name of the resource reservation, if applicable
            #resvID = , # the id of the resource reservation, if applicable
            ctime = self.timers['queue'].start, # time in seconds when job was created (first submitted)
            qtime = self.timers['current_queue'].start, # time in seconds when job was queued into current queue
            etime = self.etime, # time in seconds when job became eligible to run
            start = self.timers['user'].start, # time in seconds when job execution started
            exec_host = self.location, # name of host on which the job is being executed
            #Resource_List__dot__RES = , # limit for use of RES
            Resource_List__dot__ncpus = self.procs, # max number of cpus
            Resource_List__dot__nodect = self.nodes, # max number of nodes
            Resource_List__dot__walltime = "%s:%s:00" % (req_walltime_hours, req_walltime_minutes),
            #session = , # session number of job
            #alt_id = , # optional alternate job identifier
            end = self.timers['user'].stop, # time in seconds when job ended execution
            #Exit_status = , # the exit status of the top process of the job
            #resources_used__dot__RES = , # total RES used for job
            resources_used__dot__walltime = "%s:%s:%s" % (walltime_hours, walltime_minutes, walltime_seconds),
            #accounting_id = , # CSA JID job id
            mode = self.mode,
            cwd = self.cwd,
            exe = self.command,
            args = " ".join(self.args),
            **optional_pbs_data
        )
        
        #AddEvent("queue-manager", "job-done", self.jobid)

    def SetBGKernel(self):
        '''Ensure that the kernel is set properly prior to job launch'''
        try:
            current = os.readlink('%s/%s' % (self.config.get('partitionboot'), self.location))
        except OSError:
            logger.error("Failed to read partitionboot location %s/%s" % (self.config.get('partitionboot'), self.location))
            logger.info("Job %s/%s using kernel %s" % (self.jobid, self.user, self.kernel))
            self.acctlog.LogMessage("Job %s/%s using kernel %s" % (self.jobid, self.user, 'N/A'))
            return
        switched = current.split('/')[-1]
        if current != "%s/%s" % (self.config.get('bootprofiles'), self.kernel):
            logger.info("Updating boot image for %s" % (self.location))
            logger.info("Set to %s should be %s" % (current.split('/')[-1], self.kernel))
            try:
                os.unlink('%s/%s' % (self.config.get('partitionboot'), self.location))
                os.symlink('%s/%s' % (self.config.get('bootprofiles'), self.kernel),
                           '%s/%s' % (self.config.get('partitionboot'), self.location))
                switched = self.kernel
            except OSError:
                logger.error("Failed to reset boot location for partition for %s" % (self.location))

        logger.info("Job %s/%s using kernel %s" % (self.jobid, self.user, switched))
        self.acctlog.LogMessage("Job %s/%s using kernel %s" % (self.jobid, self.user, switched))

    def NotifyAtStart(self):
        '''Notify user when job has started'''
        mailserver = self.config.get('mailserver', 'false')
        if mailserver == 'false':
            mserver = 'localhost'
        else:
            mserver = mailserver
        subj = 'Cobalt: Job %s/%s starting - %s/%s' % (self.jobid, self.user, self.queue, self.location)
        mmsg = "Job %s/%s starting on partition %s, in the '%s' queue , at %s" % (self.jobid, self.user, self.location, self.queue, time.strftime('%c', time.localtime()))
        toaddr = []
        if self.adminemail:
            toaddr = toaddr + self.adminemail.split(':')
        if self.notify:
            toaddr = toaddr + self.notify.split(':')
        Cobalt.Util.sendemail(toaddr, subj, mmsg, smtpserver=mserver)

    def NotifyAtEnd(self):
        '''Notify user when job has ended'''
        mailserver = self.config.get('mailserver', 'false')
        if mailserver == 'false':
            mserver = 'localhost'
        else:
            mserver = mailserver
        subj = 'Cobalt: Job %s/%s finished - %s/%s %s' % (self.jobid, self.user, self.queue, self.location, self.GetStats())
        mmsg = "Job %s/%s finished on partition %s, in the '%s' queue, at %s\nStats: %s" %  (self.jobid, self.user, self.location, self.queue, time.strftime('%c', time.localtime()), self.GetStats())
        toaddr = []
        if self.adminemail:
            toaddr = toaddr + self.adminemail.split(':')
        if self.notify:
            toaddr = toaddr + self.notify.split(':')
        Cobalt.Util.sendemail(toaddr, subj, mmsg, smtpserver=mserver)

    def RunBGUserJob(self):
        '''Run a Blue Gene Job'''
        self.system_state = 'running'
        self.job_step = "executing"
        self.timers['user'].Start()
        self.LogStart()
        if not self.outputpath:
            self.outputpath = "%s/%s.output" % (self.outputdir, self.jobid)
        if not self.errorpath:
            self.errorpath = "%s/%s.error" % (self.outputdir, self.jobid)
        if not self.cobalt_log_file:
            self.cobalt_log_file = "%s/%s.cobaltlog" % (self.outputdir, self.jobid)

        cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
        print >> cobalt_log_file, "%s\n" % self.submit_command
        print >> cobalt_log_file, "submitted with cwd set to: %s\n" % self.cwd
        cobalt_log_file.close()

        if 'COBALT_JOBID' not in self.envs:
            self.envs['COBALT_JOBID'] = str(self.jobid)
            
        if self.config.get('prescript'):
            prescripts = self.config.get('prescript').split(':')
            extra = []
            for key in self.fields:
                value = getattr(self, key)
                if isinstance(value, list):
                    extra.append("%s=%s" % (key, ':'.join(value)))
                elif isinstance(value, dict):
                    extra.append("%s={%s}" % (key, str(value)))
                else:
                    extra.append("%s=%s" % (key, value))
            for p in prescripts:
                try:
                    rc, out, err = Cobalt.Util.runcommand("%s %s" % \
                                                          (p, " ".join(extra)))
                    if rc != 0:
                        logger.info("Job %s/%s: return of prescript %s was %d, error is %s" %
                                    (self.jobid, self.user, p, rc, "\n".join(err)))
                except Exception, e:
                    logger.info("Job %s/%s: exception with prescript %s, error is %s" %
                                (self.jobid, self.user, p, e))

        if self.mode == 'script':
            try:
                pgroup = ComponentProxy("script-manager").add_jobs([{'tag':'process-group', 'user':self.user, 
                     'outputfile':self.outputpath, 'cobalt_log_file':self.cobalt_log_file,
                     'errorfile':self.errorpath, 'path':self.path, 'size':self.procs,
                     'mode':self.mode, 'cwd':self.outputdir, 'executable':self.command,
                     'args':self.args, 'envs':self.envs, 'location':[self.location],
                     'id':"*", 'inputfile':self.inputfile, 'kerneloptions':self.kerneloptions,
                     'jobid':self.jobid, }])
            except (ComponentLookupError, xmlrpclib.Fault):
                logger.error("Job %s: Failed to start up user script job; requeueing" \
                             % (self.jobid))
                self.steps = ['RunBGUserJob'] + self.steps
                return

            
            if not pgroup[0].has_key('id'):
                logger.error("Process Group creation failed for Job %s" % self.jobid)
                self.state = 'sm-failure'
            else:
                self.pgid['user'] = pgroup[0]['id']
        else:
            try:
                pgroup = ComponentProxy("system").add_process_groups([{
                    'user':self.user,
                    'stdin':self.inputfile,
                    'stdout':self.outputpath,
                    'stderr':self.errorpath,
                    'cobalt_log_file':self.cobalt_log_file,
                    'size':self.procs,
                    'mode':self.mode,
                    'cwd':self.outputdir,
                    'executable':self.command,
                    'args':self.args,
                    'env':self.envs,
                    'location':[self.location],
                    'id':"*",
                    'kerneloptions':self.kerneloptions,
                }])
            except (ComponentLookupError, xmlrpclib.Fault):
                logger.error("Job %s: Failed to start up user job; requeueing" \
                             % (self.jobid))
                self.steps = ['RunBGUserJob'] + self.steps
                return
            
            if not pgroup[0].has_key('id'):
                logger.error("Process Group creation failed for Job %s" % self.jobid)
                self.state = 'pm-failure'
            else:
                self.pgid['user'] = pgroup[0]['id']
            
        self.SetPassive()

    
class JobList(DataList):
    item_cls = Job
    
    def __init__(self, q):
        self.queue = q
        self.id_gen = cqm_id_gen
        
    def add_helper(self, job, *cargs):
        job.pbslog.log("Q",
            queue = self.queue.name, # the queue into which the job was placed
        )
        job.timers['current_queue'].Start()

    def q_add (self, specs, callback=None, cargs={}):
        for spec in specs:
            if "jobid" not in spec or spec['jobid'] == "*":
                spec['jobid'] = self.id_gen.next()
        return DataList.q_add(self, specs, self.add_helper)
    
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
            return (False, "Walltime greater than the '%s' queue max walltime of %s" % (job['queue'], "%02d:%02d:00" % (divmod(int(self.value), 60))))

    def minwalltime(self, job, _=None):
        '''limits minimum walltime for job'''
        if float(job['walltime']) >= float(self.value):
            return (True, "")
        else:
            return (False, "Walltime less than the '%s' queue min walltime of %s" % (job['queue'], "%02d:%02d:00" % (divmod(int(self.value), 60))))

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
        userjobs = [j for j in queuestate if j.user == job.user and j.system_state == 'running' and j.queue == job['queue']]
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
    
    fields = Data.fields + [
        "cron", "name", "state", "adminemail",
        "policy", "maxuserjobs",
    ]
    
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
        for job in self.jobs.q_get([{'system_state':"running"}]):
            if job.user not in unum:
                unum[job.user] = 1
            else:
                unum[job.user] = unum[job.user] + 1

        for job in self.jobs:
            job.max_running = False
            if unum.get(job.user, 0) >= int(self.restrictions["maxrunning"].value):
                if job.system_state != "running":
                    job.max_running = True


class QueueDict(DataDict):
    item_cls = Queue
    key = "name"
    
    def add_queues(self, specs, callback=None, cargs={}):
        return self.q_add(specs, callback, cargs)

    def get_queues(self, specs, callback=None, cargs={}):
        return self.q_get(specs, callback, cargs)
    
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
    
    def del_queues(self, specs, callback=None, cargs={}):
        return self.q_del(specs, callback, cargs)
        
    def can_queue(self, spec):
        '''Check that job meets criteria of the specified queue'''
        # if queue doesn't exist, don't check other restrictions
        if spec['queue'] not in [q.name for q in self.itervalues()]:
            raise QueueError, "Queue '%s' does not exist" % spec['queue']

        [testqueue] = [q for q in self.itervalues() if q.name == spec['queue']]

        return testqueue.can_queue(spec)


class QueueManager(Component):
    '''Cobalt Queue Manager'''
    implementation = 'cqm'
    name = 'queue-manager'
    __statefields__ = ['Queues']
    
    logger = logger

    def __init__(self, *args, **kwargs):
        self.Queues = QueueDict()
        Component.__init__(self, *args, **kwargs)
        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.cqp = Cobalt.Cqparse.CobaltLogParser()
        self.id_gen = IncrID()
        global cqm_id_gen
        cqm_id_gen = self.id_gen

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

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)
        
        
    def set_jobid(self, jobid):
        '''Set next jobid for new job'''
        self.id_gen.set(jobid)
        print "self : ", self.id_gen.idnum
        print "module : ", cqm_id_gen.idnum
        return True
    set_jobid = exposed(set_jobid)

    def progress(self):
        '''Process asynchronous job work'''
        [j.Progress() for j in [j for queue in self.Queues.itervalues() for j in queue.jobs] if j.active]
        overtime_jobs = [j for j in [j for queue in self.Queues.itervalues() for j in queue.jobs] if j.over_time() and not j.killed]
        for job in overtime_jobs:
            job.Kill("Job %s Overtime, Killing")
            job.pbslog.log("A",
                # No attributes.
            )
            try:
                cobalt_log_file = open(job.cobalt_log_file or "/dev/null", "a")
                print >> cobalt_log_file, "job killed because walltime exceeded"
                cobalt_log_file.close()
            except:
                self.log.error("Job %s/%s:  unable to open cobaltlog file %s" % (job.jobid, job.user, job.cobalt_log_file))

        finished_jobs = [j for j in [j for queue in self.Queues.itervalues() for j in queue.jobs] if j.job_step == 'done']
        for job in finished_jobs:
            job.LogFinish()
        for (j, queue) in [(j, queue) for queue in self.Queues.itervalues() for j in queue.jobs]:
            if j.job_step == 'done':
                # check to see if somebody depended on this
                if j.exit_status == 0:
                    for waiting_job in self.Queues.get_jobs([{'state':"dependency hold"}]):
                        if str(j.jobid) in waiting_job.all_dependencies:
                            waiting_job.satisfied_dependencies.append(str(j.jobid))
                queue.jobs.q_del([{'jobid':j.jobid}])

        # enforce the maxrunning queue attribute (HACK ALERT)
        for queue in self.Queues.itervalues():
            queue.update_max_running()
                            
        for (name, q) in self.Queues.items():
            if q.state == 'dead' and q.name.startswith('R.') and not q.jobs:
                del self.Queues[name]
        #newdate = time.strftime("%m-%d-%y", time.localtime())
        #[j.acctlog.ChangeLog() for j in [j for queue in self.Queues for j in queue] if newdate != self.prevdate]
        #Job.acctlog.ChangeLog()
        return 1
    progress = automatic(progress)

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
        
        response = self.Queues.add_jobs(specs)
        return response
    add_jobs = exposed(query(add_jobs))

    def del_jobs(self, data, force=False, user=None):
        '''Delete a job'''
        ret = []
        for spec in data:
            for job, q in [(job, queue) for queue in self.Queues.itervalues() for job in queue.jobs if job.match(spec)]:
                ret.append(job)
                if job.system_state != "running":
                    #q.remove(job)
                    q.jobs.q_del([spec])
                elif job.system_state == "running" and job.job_step == "starting":
                    q.jobs.q_del([spec])
                elif force:
                    # Need acct log message for forced delete, 
                    # otherwise can't tell if job ever ended
                    job.Kill("Job %s killed based on admin request")
                    
                    try:
                        cobalt_log_file = open(job.cobalt_log_file or "/dev/null", "a")
                        print >> cobalt_log_file, "job killed based on admin request"
                        cobalt_log_file.close()
                    except:
                        self.log.error("Job %s/%s:  unable to open cobaltlog file %s" % (job.jobid, job.user, job.cobalt_log_file))
                    
                    # FIXME
                    # i think the below *shouldn't* be there -- it seems like job.Kill will eventually make it happen
                    q.jobs.q_del([spec])
                else:
                    job.Kill("Job %s killed based on user request")
                    
                    try:
                        cobalt_log_file = open(job.cobalt_log_file or "/dev/null", "a")
                        print >> cobalt_log_file, "job killed based on user request"
                        cobalt_log_file.close()
                    except:
                        self.log.error("Job %s/%s:  unable to open cobaltlog file %s" % (job.jobid, job.user, job.cobalt_log_file))

                # It's my understanding that the above code draws a distinction
                # between killing a running job and killing a job that hasn't started yet.
                # I don't think PBS logs draw this distionction.
                job.pbslog.log("D",
                    requester = user or job.user, # who deleted the job
                )
                logger.info('D;%s;%s' % (job.jobid, job.user))
                job.acctlog.LogMessage('D;%s;%s' % (job.jobid, job.user))

        return ret
    del_jobs = exposed(query(del_jobs))

    def del_queues(self, specs, force=False):
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
        response = self.Queues.del_queues([queue.to_rx() for queue in queues])
        if failed:
            raise QueueError, "The %s queue(s) contains jobs. Either move the jobs to another queue, or \nuse 'cqadm -f --delq' to delete the queue(s) and the jobs.\n\nDeleted Queues\n================\n%s" % (",".join(failed), "\n".join([q.name for q in response]))
        else:
            return response
    del_queues = exposed(query(del_queues))

    def get_history(self, data):
        '''Fetches queue history from acct log'''
        self.cqp.perform_default_parse()
        return self.cqp.q_get(data)
    get_history = exposed(get_history)

    def poll_process_groups (self):
        '''Resynchronize with the system'''
        
        try:
            pgroups = ComponentProxy("system").get_process_groups([{'id':'*', 'state':'running'}])
        except (ComponentLookupError, xmlrpclib.Fault):
            logger.error("Failed to communicate with the system")
            return
        
        live = [item['id'] for item in pgroups]
        for job in [j for queue in self.Queues.itervalues() for j in queue.jobs if j.mode!='script']:
            for pgtype in job.pgid.keys():
                pgid = job.pgid[pgtype]
                if pgid not in live:
                    self.logger.info("Found dead pg for job %s" % (job.jobid))
                    job.CompletePG(pgid)
    poll_process_groups = automatic(poll_process_groups)

    def sm_sync(self):
        '''Resynchronize with the script manager'''
        try:
            pgroups = ComponentProxy("script-manager").get_jobs([{'id':'*', 'state':'running'}])
        except (ComponentLookupError, xmlrpclib.Fault):
            logger.error("Failed to communicate with script manager")
            return
        live = [item['id'] for item in pgroups]
        for job in [j for queue in self.Queues.itervalues() for j in queue.jobs if j.mode=='script']:
            for pgtype in job.pgid.keys():
                pgid = job.pgid[pgtype]
                if pgid not in live:
                    self.logger.info("Found dead pg for job %s" % (job.jobid))
                    job.CompletePG(pgid)
    sm_sync = automatic(sm_sync)

    def get_jobs(self, specs):
        return self.Queues.get_jobs(specs)
    get_jobs = exposed(query(get_jobs))

    def get_queues(self, specs):
        return self.Queues.get_queues(specs)
    get_queues = exposed(query(get_queues))

    def add_queues(self, specs):
        return self.Queues.add_queues(specs)
    add_queues = exposed(query(add_queues))
    
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
        

    def run_jobs(self, specs, nodelist):
        def _run_jobs(job, nodes):
            job.Run(nodes)
            self.Queues[job.queue].update_max_running()
        return self.Queues.get_jobs(specs, _run_jobs, nodelist)
    run_jobs = exposed(query(run_jobs))

    def set_jobs(self, specs, updates):
        def _set_jobs(job, newattr):
            test = job.to_rx()
            test.update(newattr)
            if self.Queues[job.queue].can_queue(test):
                job.update(newattr)
        return self.Queues.get_jobs(specs, _set_jobs, updates)
    set_jobs = exposed(query(set_jobs))

    def move_jobs(self, specs, new_q_name):
        if new_q_name not in self.Queues:
            logger.error("attempted to move a job to non-existent queue '%s'" % new_q_name)
            raise QueueError, "Error: queue '%s' does not exist" % new_q_name
        new_q = self.Queues[new_q_name]
        
        for job in self.Queues.get_jobs(specs):
            if job.queue==new_q_name:
                raise QueueError, "job %d already in queue '%s'" % (job.jobid, new_q_name)
            if job.system_state == "running":
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
                results += new_q.jobs.q_add([job.to_rx()])
                new_q.update_max_running()
        return results
    move_jobs = exposed(query(move_jobs))
                    
