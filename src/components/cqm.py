#!/usr/bin/env python
# $Id$

'''Cobalt Queue Manager'''
__revision__ = '$Revision$'

from logging import getLogger, FileHandler, Formatter

import logging, os, sys, time, xml.sax.saxutils, xmlrpclib, ConfigParser, copy, types
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util, Cobalt.Cqparse

logger = logging.getLogger('cqm')

class ProcessManagerError(Exception):
    '''This error occurs when communications with the process manager fail'''
    pass

class TimerException(Exception):
    '''This error occurs when timer methods are called in the wrong order'''
    pass

class ScriptManagerError(Exception):
    '''This error occurs when communications with the script manager fail'''
    pass

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

class Job(Cobalt.Data.Data):
    '''The Job class is an object corresponding to the qm notion of a queued job, including steps'''

    acctlog = Cobalt.Util.AccountingLog('qm')
    
    fields = Cobalt.Data.Data.fields.copy()
    fields.update(dict(
        jobid = None,
        jobname = "N/A",
        state = "queued",
        attribute = "compute",
        location = "N/A",
        starttime = "-1",
        submittime = None,
        endtime = "-1",
        queue = "default",
        type = "mpish",
        user = None,
        walltime = None,
        procs = None,
        nodes = None,
        mode = None,
        cwd = None,
        command = None,
        args = None,
        outputdir = None,
        project = None,
        lienID = None,
        exit_status = None,
        stagein = None,
        stageout = None,
        reservation = None,
        host = None,
        port = None,
        url = None,
        stageid = None,
        envs = None,
        inputfile = None,
        kerneloptions = None,
    ))

    def __init__(self, data, jobid):
        self.timers = dict(
            queue = Timer(),
            current_queue = Timer(),
            user = Timer(),
        )
        self.timers['queue'].Start()
        self.timers['current_queue'].Start()
        
        Cobalt.Data.Data.__init__(self, data)
        
        self.comms = Cobalt.Proxy.CommDict()
        if self.jobid is None or self.jobid == '*':
            self.jobid = str(jobid)
        if self.submittime is None:
            self.submittime = time.time()
        self.staged = 0
        self.killed = False
        self.pgid = {}
        self.spgid = {}
        #self.steps = ['StageInit', 'FinishStage', 'RunPrologue', 'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'FinalizeStage', 'Finish']
        #self.steps = ['StageInit', 'FinishStage', 'RunPrologue',
        #              'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'FinalizeStage', 'Finish']
        #self.steps=['StageInit','FinishStage','RunPrologue','RunUserJob','RunEpilogue','FinalizeStage','Finish']
        self.steps = ['RunPrologue', 'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'Finish']
        self.stageid = None
        self.reservation = False
        #AddEvent("queue-manager", "job-submitted", self.jobid)
        self.SetPassive()
        # acctlog
        self.pbslog = Cobalt.Util.PBSLog(self.jobid)
        logger.info(
            'Q;%s;%s;%s' % (self.jobid, self.user, self.queue))
        self.acctlog.LogMessage(
            'Q;%s;%s;%s' % (self.jobid, self.user, self.queue))
    
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
        Cobalt.Data.Data.__setstate__(self, state)
        if not self.timers.has_key('current_queue'):
            self.timers['current_queue'] = Timer()
            self.timers['current_queue'].Start()
        #self.acctlog = Cobalt.Util.AccountingLog('qm')
        self.comms = Cobalt.Proxy.CommDict()
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

    def fail_job(self, state):
        '''Signal complete job failure, resulting in specified state'''
        self.state = None
        self.steps = []

    def WriteOutput(self):
        '''Write user output to the file system'''
        try:
            open("%s/%s.output" % (self.outputdir, self.jobid), 'w').write(self.output)
            open("%s/%s.error" % (self.outputdir, self.jobid), 'w').write(self.error)
        except IOError:
            logger.error("Failed to write to userdir for job %s writing to /tmp instead" % self.jobid)
            open("%s/%s.output" % ('/tmp', self.jobid), 'w').write(self.output)
            open("%s/%s.error" % ('/tmp', self.jobid), 'w').write(self.error)

    def CheckProject(self):
        '''Check that a user is part of the supplied project'''
        try:
            proj = self.comms['am'].GetProject([{'tag':'project', 'name':self.project, 'users':'*'}])
        except:
            logger.error("Failed to contact allocation manager")
            self.fail_job('am-error')
            return
        if len(proj) < 1 or self.user not in proj[0]['user']:
            if len(proj) == 0:
                logger.error("Project specification error for user %s, project %s. (no such project)" % (
                    self.user, self.project))
            else:
                logger.error("User %s not in project %s" % (self.user, self.project))
            self.fail_job('am-error')
            return
        try:
            lien = self.comms['am'].AddLien(self.project, self.user,
                                            float(self.walltime) * 60 * int(self.nodes))
        except xmlrpclib.Fault:
            # handle fault here
            pass
        except:
            logger.error("Unexpected lien creation failure", exc_info=1)
        self.lienID = lien['id']

    def SetActive(self):
        '''set job info active mode'''
        self.active = True

    def SetPassive(self):
        '''set job into passive mode'''
        self.active = False
        
    def HasPG(self, pgid):
        '''Check if a job has a pgroup'''
        if pgid in self.pgid.values():
            return 1
        return 0

    def Finish(self):
        '''Finish up accounting for job'''
        used_time = int(self.timers['user'].Check()) * len(self.location.split(':'))
        try:
            self.comms['am'].CommitLien(self.lienID, used_time)
        except:
            pass
                                                                
        self.state = "done"
        self.SetPassive()
        #AddEvent("queue-manager", "job-completed", self.jobid)
        # acctlog
        logger.info('E;%s;%s;%s' % \
                    (self.jobid, self.user, str(used_time)))
        self.acctlog.LogMessage('E;%s;%s;%s' % \
                                (self.jobid, self.user, str(used_time)))
        self.endtime = str(time.time())

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
            self.state = "done"
            
    def Run(self, nodelist):
        '''Run a job'''
        if self.state not in ['ready', 'queued', 'stage-pending', 'prologue']:
            logger.info("Got multiple run commands for job %s" % self.jobid)
            return
        self.timers['queue'].Stop()
        self.timers['current_queue'].Stop()
        if self.reservation is not None:
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

    def FinishStage(self):
        '''Complete a stage'''
        self.state = 'stage-pending'
        if not self.staged:
            self.SetPassive()
            self.steps = ['FinishStage'] + self.steps
        else:
            self.state = 'ready'
            #AddEvent("queue-manager", "job-ready", self.jobid)
            self.SetActive()     

    def FinishUserPgrp(self):
        '''Complete a process group for the user job'''
        self.timers['user'].Stop()
        if self.spgid.has_key('user'):
            try:
                #pgroups = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'output':'*', 'error':'*'}])
                if self.mode == 'script':
                    result = self.comms['sm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'exit_status':'*'}])
                else:
                    result = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'exit_status':'*'}])
                if result:
                    self.exit_status = result[0].get('exit_status')
                #this seems needed to get the info back into the object so it can be handed back to the filestager.
                #self.output = pgroups[0]['output']
                #self.error = pgroups[0]['error']
            except xmlrpclib.Fault:
                logger.error("Error contacting process manager for finalize, requeueing")
                self.steps = ['FinalizeStage'] + self.steps
                self.SetActive()
                return
            except:
                logger.error("Unexpected error finalizing process group", exc_info=1)
                self.SetPassive()
                return
        else:
            logger.error("No record of pgid for user job %s" % (self.jobid))
        self.SetActive()

    def FinalizeStage(self):
        '''Write output streams to the file stager'''
        try:
            self.comms['fs'].WriteStreams(self.stageid, self.output, self.error)
            self.comms['fs'].FinalizeState(self.stageid)
        except:
            logger.error("Failed to contact %s for finalize, requeuing" % (self.scomp))
            self.steps = ['FinalizeStage'] + self.steps
        self.SetActive()

    def StageInit(self):
        '''Initialize staging for jobs that need it'''
        # we need to assess which parts of stage need to complete
        try:
            stagespec = {'tag':'stage', 'outputdir':self.outputdir, 'name':self.jobid,
                         'size':self.nodes, 'user':self.user,
                         'script':xml.sax.saxutils.escape(self.script)}
            if self.stagein:
                stagespec['in'] = self.stagein
            if self.stageout:
                stagespec['out'] = self.stageout
            stage = self.comms['fs'].SetupStage(stagespec)
        except xmlrpclib.Fault, fault:
            logger.error("Failed to initialize stage")
            self.fail_job('stage-error')
            print fault
            return
        except Cobalt.Proxy.CobaltComponentError:
            logger.error("couldn't contact the File Stager")
            return
        except:
            logger.error("Unexpected failure during stage initialization", exc_info=1)
            self.fail_job('stage-error')
            return
        self.url = stage['uri']
        self.stageid = stage['id']
        self.scomp = stage['component']
        logger.debug("Got stageid %s for job %s" % (self.stageid, self.jobid))

    def RunPrologue(self):
        '''Run the job prologue'''
        self.timers['/usr/sbin/prologue'] = Timer()
        if self.location == 'none':
            # requeue if not ready
            self.steps = ['RunPrologue'] + self.steps
            self.SetPassive()
            return
        self.state = 'prologue'
        #this path and executable should be pulled from cfg file
        try:
            os.system("/master/bcfg/generators/account/setaccess.py -a %s %s" % (self.user,
                                                                                 " ".join(self.location)))
        except:
            logger.info("access control not enabled")
        self.timers['/usr/sbin/prologue'].Start()
        self.AdminStart('/usr/sbin/prologue')
        self.SetPassive()

    def RunEpilogue(self):
        '''Run the job epilogue'''
        self.timers['/usr/sbin/epilogue'] = Timer()
        self.state = 'epilogue'
        os.system("/master/bcfg/generators/account/setaccess.py -r %s %s" % (self.user,
                                                                             " ".join(self.location.split(':'))))
        self.timers['/usr/sbin/epilogue'].Start()
        self.AdminStart('/usr/sbin/epilogue')
        self.SetPassive()

    def RunUserJob(self):
        '''Run the user job'''
        self.state = 'running'
        self.timers['user'].Start()
        self.LogStart()
        args = []
        if self.host:
            args = ["-i", "-h", self.host, "-p", self.port]
        if self.url:
            args += ["-b", self.url]
        if self.stageid is not None:
            args += ["-n", self.stageid]
        elif self.command:
            args += ["-f", self.command]
        if self.stageout:
            args += ["-s", self.stageout]
        if self.type == 'pbs':
            args.append("-P")
        args.append("-t")
        args.append(str(60 * float(self.walltime)))
        location = self.location.split(':')
        outputfile = "%s/%s.output" % (self.outputdir, self.jobid)
        errorfile = "%s/%s.error" % (self.outputdir, self.jobid)
        cwd = self.cwd or self.envs['data']['PWD']
        env = self.envs['data']
        try:
            pgroup = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'user':self.user, 'pgid':'*', 'executable':'/usr/bin/mpish',
                 'size':self.procs, 'args':args, 'envs':env, 'errorfile':errorfile,
                 'outputfile':outputfile, 'location':location, 'cwd':cwd, 'path':"/bin:/usr/bin:/usr/local/bin",
                 'inputfile':self.inputfile, 'kerneloptions':self.kerneloptions})
        except xmlrpclib.Fault:
            logger.error("Failed to communicate with process manager")
            raise ProcessManagerError
        self.pgid['user'] = pgroup[0]['pgid']
        self.SetPassive()

    def Kill(self, killmsg):
        '''Kill a job'''
        if self.killed == True:
            return
        self.killed = True
        logger.info(killmsg % (self.jobid))
        if self.state in ['epilogue', 'cleanup']:
            logger.info("Not killing job %s during recovery" % (self.jobid))
        elif self.state in ['setup', 'prologue', 'stage-pending', 'stage-error', 'pm-error']:
            # first kill the lien
            try:
                self.comms['am'].DelLien({'tag':'lien', 'id':self.lienID})
            except:
                logger.error("Failed to delete lien id %s for project %s" % (self.lienID, self.project))
            # then perform step manipulation
            if self.state in ['setup', 'prologue']:
                self.steps.remove('RunUserJob')
            # then activate if needed
            if self.state in ['stage-pending']:
                self.SetActive()
            else:
                self.SetPassive()
            if self.state in ['stage-error', 'pm-error']:
                self.state = 'done'
        elif self.state == 'running':
            if not self.pgid.has_key('user'):
                logger.error("Job %s has no pgroup associated with it" % self.jobid)
            else:
                self.KillPGID(self.pgid['user'])
        elif self.state == 'hold':  #job in 'hold' and running
            self.KillPGID(self.pgid['user'])
        else:
            logger.error("Got qdel for job %s in unexpected state %s" % (self.jobid, self.state))
 
        # acctlog
        logger.info('D;%s;%s' % (self.jobid, self.user))
        self.acctlog.LogMessage('D;%s;%s' % (self.jobid, self.user))

    def AdminStart(self, cmd):
        '''Run an administrative job step'''
        location = self.location.split(':')
        try:
            pgrp = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'pgid':'*', 'user':'root', 'size':self.nodes,
                 'path':"/bin:/usr/bin:/usr/local/bin", 'cwd':'/', 'executable':cmd, 'envs':{},
                 'args':[self.user], 'location':location, 'inputfile':self.inputfile,
                 'kerneloptions':self.kerneloptions})
        except xmlrpclib.Fault, fault:
            print fault
        except:
            logger.error("Unexpected failure in administrative process start", exc_info=1)
            self.state = 'pm-error'
            return
        
        self.pgid[cmd] = pgrp[0]['pgid']

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
        try:
            self.comms['pm'].KillProcessGroup({'tag':'process-group', 'pgid':pgid})
        except xmlrpclib.Fault:
            logger.error("Failed to kill process group %s" % (pgid))
            raise ProcessManagerError

    def over_time(self):
        '''Check if a job has run over its time'''
        if self.state == 'running':
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
        '''Log end of job data'''
        logger.info("Job %s/%s on %s nodes done. %s" % \
                    (self.jobid, self.user,
                     self.nodes, self.GetStats()))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit code %s" % \
                                (self.jobid, self.user,
                                 self.nodes, self.GetStats()))
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

class BGJob(Job):
    
    '''BG Job is a Blue Gene/L job'''
    
    fields = Job.fields.copy()
    fields.update(dict(
        bgkernel = None,
        kernel = "default",
        notify = None,
        adminemail = None,
        location = None,
        outputpath = None,
        outputdir = None,
        errorpath = None,
        path = None,
        mode = "co",
        envs = None,
        exit_status = None,
    ))
    
    _configfields = ['bgkernel']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
        if not _config._sections.has_key('cqm'):
            print '''"cqm" section missing from cobalt config file'''
            raise SystemExit, 1
    config = _config._sections['cqm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1
    if config.get("bgkernel") == 'true':
        for param in ['partitionboot', 'bootprofiles']:
            if config.get(param, 'nothere') == 'nothere':
                print "Missing option in cobalt config file: %s." % (param)
                print "This is required only if dynamic kernel support is enabled"
                raise SystemExit, 1

    def __init__(self, data, jobid):
        Job.__init__(self, data, jobid)
        #AddEvent("queue-manager", "job-submitted", self.jobid)
        if self.notify or self.adminemail:
            self.steps = ['NotifyAtStart', 'RunBGUserJob', 'NotifyAtEnd', 'FinishUserPgrp', 'Finish']
        else:
            self.steps = ['RunBGUserJob', 'FinishUserPgrp', 'Finish']
        if self.config.get('bgkernel'):
            self.steps.insert(0, 'SetBGKernel')
        self.SetPassive()
#         self.acctlog.LogMessage('Q;%s;%s;%s' % \
#                                 (self.jobid, self.user, self.queue))
        
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
        if self.adminemail != '*':
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
        if self.adminemail != '*':
            toaddr = toaddr + self.adminemail.split(':')
        if self.notify:
            toaddr = toaddr + self.notify.split(':')
        Cobalt.Util.sendemail(toaddr, subj, mmsg, smtpserver=mserver)

    def RunBGUserJob(self):
        '''Run a Blue Gene Job'''
        self.state = 'running'
        self.timers['user'].Start()
        self.LogStart()
        if not self.outputpath:
            self.outputpath = "%s/%s.output" % (self.outputdir, self.jobid)
        if not self.errorpath:
            self.errorpath = "%s/%s.error" % (self.outputdir, self.jobid)

        if self.mode == 'script':
            try:
                pgroup = self.comms['sm'].CreateProcessGroup({'tag':'process-group', 'user':self.user, 'pgid':'*', 'outputfile':self.outputpath,
                     'errorfile':self.errorpath, 'path':self.path, 'size':self.procs,
                     'mode':self.mode, 'cwd':self.outputdir, 'executable':self.command,
                     'args':self.args, 'envs':self.envs, 'location':[self.location],
                     'jobid':self.jobid, 'inputfile':self.inputfile, 'kerneloptions':self.kerneloptions})            
            except xmlrpclib.Fault:
                raise ScriptManagerError
            except Cobalt.Proxy.CobaltComponentError:
                raise ScriptManagerError
            if not pgroup[0].has_key('pgid'):
                logger.error("Process Group creation failed for Job %s" % self.jobid)
                self.state = 'sm-failure'
            else:
                self.pgid['user'] = pgroup[0]['pgid']
        else:
            try:
                pgroup = self.comms['pm'].CreateProcessGroup(
                    {'tag':'process-group', 'user':self.user, 'pgid':'*', 'outputfile':self.outputpath,
                     'errorfile':self.errorpath, 'path':self.path, 'size':self.procs,
                     'mode':self.mode, 'cwd':self.outputdir, 'executable':self.command,
                     'args':self.args, 'envs':self.envs, 'location':[self.location],
                     'jobid':self.jobid, 'inputfile':self.inputfile, 'kerneloptions':self.kerneloptions})
            except xmlrpclib.Fault:
                raise ProcessManagerError
            except Cobalt.Proxy.CobaltComponentError:
                raise ProcessManagerError
            if not pgroup[0].has_key('pgid'):
                logger.error("Process Group creation failed for Job %s" % self.jobid)
                self.state = 'pm-failure'
            else:
                self.pgid['user'] = pgroup[0]['pgid']
            
        self.SetPassive()

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
    
    def Finish(self):
        '''Finish up accounting for job, also adds postscript ability'''
        Job.Finish(self)

        if self.config.get('postscript'):
            postscripts = self.config.get('postscript').split(':')
            extra = []
            for field in self.fields:
                if isinstance(self.get(field), list):
                    extra.append("%s=%s" % (field, ':'.join(self.get(field))))
                elif isinstance(self.get(field), dict):
                    extra.append("%s={%s}" % (field, str(self.get(field))))
                else:
                    extra.append("%s=%s" % (field, self.get(field)))
            for p in postscripts:
                try:
                    rc, out, err = Cobalt.Util.runcommand("%s %s" % (p, " ".join(extra)))
                    if rc != 0:
                        logger.info("Job %s/%s: return of postscript %s was %d, error message is %s" %
                                     (self.jobid, self.user, p, rc, "\n".join(err)))
                except Exception, e:
                    logger.info("Job %s/%s: exception with postscript %s, error is %s" %
                                 (self.jobid, self.user, p, e))

class ScriptMPIJob(Job):
    '''ScriptMPIJob is an mpirun command issued from a user script.'''
    _configfields = ['bgkernel']
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
        if not _config._sections.has_key('cqm'):
            print '''"cqm" section missing from cobalt config file'''
            raise SystemExit, 1
    config = _config._sections['cqm']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1
    if config.get('bgkernel') == 'true':
        for param in ['partitionboot', 'bootprofiles']:
            if config.get(param, 'nothere') == 'nothere':
                print "Missing option in cobalt config file: %s." % (param)
                print "This is required only if dynamic kernel support is enabled"
                raise SystemExit, 1

    def __init__(self, data, jobid):
        Job.__init__(self, data, jobid)
        if not self.get('kernel', False):
            self.set('kernel', 'default')
        #AddEvent("queue-manager", "job-submitted", self.get('jobid'))
        self.SetPassive()
                
    def SetBGKernel(self):
        '''Ensure that the kernel is set properly prior to job launch'''
        try:
            current = os.readlink('%s/%s' % (self.config.get('partitionboot'), self.get('location')))
        except OSError:
            logger.error("Failed to read partitionboot location %s/%s" % (self.config.get('partitionboot'), self.get('location')))
            logger.info("Job %s/%s using kernel %s" % (self.get('jobid'), self.get('user'), 'N/A'))
            self.acctlog.LogMessage("Job %s/%s using kernel %s" % (self.get('jobid'), self.get('user'), 'N/A'))
            return
        switched = current.split('/')[-1]
        if current != "%s/%s" % (self.config.get('bootprofiles'), self.get('kernel')):
            logger.info("Updating boot image for %s" % (self.get('location')))
            logger.info("Set to %s should be %s" % (current.split('/')[-1], self.get('kernel')))
            try:
                os.unlink('%s/%s' % (self.config.get('partitionboot'), self.get('location')))
                os.symlink('%s/%s' % (self.config.get('bootprofiles'), self.get('kernel')),
                           '%s/%s' % (self.config.get('partitionboot'), self.get('location')))
                switched = self.get('kernel')
            except OSError:
                logger.error("Failed to reset boot location for partition for %s" % (self.get('location')))

        logger.info("Job %s/%s using kernel %s" % (self.get('jobid'), self.get('user'), switched))
        self.acctlog.LogMessage("Job %s/%s using kernel %s" % (self.get('jobid'), self.get('user'), switched))

    def RunScriptMPIJob(self):
        '''Run an mpirun job that was invoked by a script.'''
        if self.config.get('bgkernel', 'false') == 'true':
            SetBGKernel()

        self.set('state', 'running')
        self.timers['user'].Start()
        self.LogStart()
        if not self.get('outputpath', False):
            self.set('outputpath', "%s/%s.output" % (self.get('outputdir'), self.get('jobid')))
        if not self.get('errorpath', False):
            self.set('errorpath', "%s/%s.error" % (self.get('outputdir'), self.get('jobid')))

        try:
            pgroup = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'user':self.get('user'), 'pgid':'*', 'outputfile':self.get('outputpath', ''),
                 'errorfile':self.get('errorpath', ''), 'path':self.get('path', ''), 'cwd':self.get('outputdir', ''), 'location':[self.get('location')],
                 'jobid':self.get('jobid'), 'inputfile':self.get('inputfile', ''), 'true_mpi_args':self.get('true_mpi_args'), 'envs':{}})
        except xmlrpclib.Fault:
            raise ScriptManagerError
        except Cobalt.Proxy.CobaltComponentError:
            raise ScriptManagerError
        if not pgroup[0].has_key('pgid'):
            logger.error("Process Group creation failed for Job %s" % self.get('jobid'))
            self.set('state', 'sm-failure')
        else:
            self.pgid['user'] = pgroup[0]['pgid']
        self.SetPassive()
        self.LogFinish()

    def LogFinish(self):
        '''Log end of job data, specific for BG/L exit status'''
        exitstatus = self.get('exit-status', 'N/A')
        try:
            exitstatus = exitstatus.get('BG/L')
            exitstatus = int(exitstatus)/256
        except:
            pass
        logger.info("Job %s/%s on %s nodes done. %s" % \
                    (self.get('jobid'), self.get('user'),
                     self.get('nodes'), self.GetStats()))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit:%s" % \
                                (self.get('jobid'), self.get('user'),
                                 self.get('nodes'), self.GetStats(),
                                 str(exitstatus)))
        self.LogFinishPBS()


class JobSet(Cobalt.Data.DataSet):
    '''Set of currently queued jobs'''
    __object__ = BGJob

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        #self.__id__ = Cobalt.Data.IncrID()

class Restriction(Cobalt.Data.Data):
    
    '''Restriction object'''
    
    fields = Cobalt.Data.Data.fields.copy()
    fields.update(dict(
        name = None,
        type = "queue",
        value = None,
    ))

    __checks__ = {'maxtime':'maxwalltime', 'users':'usercheck',
                  'maxrunning':'maxuserjobs', 'mintime':'minwalltime',
                  'maxqueued':'maxqueuedjobs', 'maxusernodes':'maxusernodes',
                  'totalnodes':'maxtotalnodes'}

    def __init__(self, info, myqueue=None):
        '''info could be like
        {tag:restriction, jparam:walltime, qparam:maxusertime,
        value:x, operator:op}
        how about {tag:restriction, name:name, value:x}
        myqueue is a reference to the queue that this restriction is associated
        with
        '''
        Cobalt.Data.Data.__init__(self, info)
        self.queue = myqueue

        if info.get('name') in ['maxrunning', 'maxusernodes', 'totalnodes']:
            self.type = 'run'
        logger.debug('created restriction %s with type %s' % (self.name, self.type))

    def maxwalltime(self, job, _=None):
        '''checks walltime of job against maxtime of queue'''
        if float(job.walltime) <= float(self.value):
            return (True, "")
        else:
            return (False, "Walltime greater than the '%s' queue max walltime of %s" % (job.queue, "%02d:%02d:00" % (divmod(int(self.value), 60))))

    def minwalltime(self, job, _=None):
        '''limits minimum walltime for job'''
        if float(job.walltime) >= float(self.value):
            return (True, "")
        else:
            return (False, "Walltime less than the '%s' queue min walltime of %s" % (job.queue, "%02d:%02d:00" % (divmod(int(self.value), 60))))

    def usercheck(self, job, _=None):
        '''checks if job owner is in approved user list'''
        #qusers = self.queue.users.split(':')
        qusers = self.value.split(':')
        if '*' in qusers or job.user in qusers:
            return (True, "")
        else:
            return (False, "You are not allowed to submit to the '%s' queue" % job.queue)

    def maxuserjobs(self, job, queuestate=None):
        '''limits how many jobs each user can run by checking queue state
        with potential job added'''
        userjobs = [j for j in queuestate if j.user == job.user and j.state == 'running' and j.queue == job.queue]
        if len(userjobs) >= int(self.value):
            return (False, "Maxuserjobs limit reached")
        else:
            return (True, "")

    def maxqueuedjobs(self, job, _=None):
        '''limits how many jobs a user can have in the queue at a time'''
        userjobs = [j for j in self.queue if j.user == job.user]
        if len(userjobs) >= int(self.value):
            return (False, "The limit of %s jobs per user in the '%s' queue has been reached" % (self.value, job.queue))
        else:
            return (True, "")

    def maxusernodes(self, job, queuestate=None):
        '''limits how many nodes a single user can have running'''
        usernodes = 0
        for j in [qs for qs in queuestate if qs.user == job.user
                  and qs.state == 'running'
                  and qs.queue == job.queue]:
            usernodes = usernodes + int(j.nodes)
        if usernodes + int(job.nodes) > int(self.value):
            return (False, "Job exceeds MaxUserNodes limit")
        else:
            return (True, "")

    def maxtotalnodes(self, job, queuestate=None):
        '''limits how many total nodes can be used by jobs running in
        this queue'''
        totalnodes = 0
        for j in [qs for qs in queuestate if qs.state == 'running'
                  and qs.queue == job.queue]:
            totalnodes = totalnodes + int(j.nodes)
        if totalnodes + int(job.nodes) > int(self.value):
            return (False, "Job exceeds MaxTotalNodes limit")
        else:
            return (True, "")

    def CanAccept(self, job, queuestate=None):
        '''Checks if this object will allow the job'''
        logger.debug('checking restriction %s' % self.name)
        func = getattr(self, self.__checks__[self.name])
        return func(job, queuestate)

class RestrictionSet(Cobalt.Data.DataSet):
    """RestrictionSet.Get would check all it's restrictions, if the name
    matches the field, then add it's name and value to the return list

    RestrictionSet.Set would be something like if that restriction already
    exists, then update the value, otherwise create the restriction
    """
    __object__ = Restriction

    def __init__(self, myqueue):
        Cobalt.Data.DataSet.__init__(self)
#         self.__id__ = Cobalt.Data.IncrID()
        self.queue = myqueue

    def Add(self, cdata, _=None, cargs=()):
        '''Add restriction(s)'''
        retval = []
        for item in cdata:
            toupdate = [r for r in self.data if r.name == item.name]
            if toupdate:
                # just update the value
                toupdate[0].value = item.value
            else:
                iobj = self.__object__(item, self.queue)
                self.data.append(iobj)
                retval.append(iobj.to_rx(item))
        return retval

    def Get(self, cdata, _=None, cargs={}):
        '''Returns restrictions in single dict'''
        for c in cargs:
            if cargs[c] == '*':  #delete restriction
                self.Del({'tag':'restriction', 'name':c})
            else:
                self.Add([{'tag':'restriction', 'name':c, 'value':cargs[c]}])
        response = {}
        for spec in cdata:  #query
            for r in self.data:  #restrictions
                if r.match(spec):  #restriction matches
                    response.update({r.name:r.value})
        return [response]

#     def Test(self, job):
#         '''Test queue restrictions'''
#         probs = ''
#         for restriction in [r for r in self.data if r.type == 'queue']:
#             result = restriction.CanAccept(job, type='queue')
#             if not result[0]:
#                 probs = probs + result[1] + '\n'

#         if probs:
#             return (False, probs)
#         else:
#             return (True, probs)

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

class Queue(Cobalt.Data.Data, JobSet):
    '''queue object, subs JobSet and Data, which gives us:
       self is a Queue object (with restrictions and stuff)
       self.data is a list of BGJob objects'''
    
    fields = Cobalt.Data.Data.fields.copy()
    fields.update(dict(
        cron = None,
        name = None,
        state = "stopped",
        adminemail = "*",
        policy = "default",
        maxuserjobs = None,
    ))
    
    def __init__(self, info, _=None):
        Cobalt.Data.Data.__init__(self, info)
        JobSet.__init__(self)

        self.restrictions = RestrictionSet(self)
    
    def _get_smartstate (self):
        if self.cron:
            if cronmatch(self.cron):
                return "running"
            else:
                return "stopped"
        else:
            return self.state
    smartstate = property(_get_smartstate)
    
    def append (self, job):
        job.pbslog.log("Q",
            queue = self.name, # the queue into which the job was placed
        )
        job.timers['current_queue'].Start()
        super(Queue, self).append(job)

class QueueSet(Cobalt.Data.DataSet):
    '''Set of queues
    self.data is the list of queues known'''
    __object__ = Queue
    
    __unique__ = "name"

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        self.__id__ = Cobalt.Data.IncrID()

    def Add(self, cdata, callback=None, cargs=()):
        '''Add new Queue to QueueSet

        overloaded from DataSet.Add() for adding queues, specifically
        for passing along an IncrID object instead of a number, so that each
        JobSet has the same __id__ ref
        '''
        retval = []
        if type(cdata) != types.ListType:
            cdata = [cdata]
        for item in cdata:
            #first update cargs with restriction elements, and remove any restrictions
            #from item, so they aren't created as normal attributes of iobj
            rupdates = {}  #restriction updates
            for datum in item.keys():
                if datum in Restriction.__checks__:
                    rupdates.update({datum:item.get(datum)})
                    del item[datum]

            #create new queue
            try:
                if self.__id__:
                    iobj = self.__object__(item)
                    iobj.__id__ = self.__id__
                else:
                    iobj = self.__object__(item)
            except Cobalt.Data.DataCreationError, missing:
                print "returning fault"
                raise xmlrpclib.Fault(8, str(missing))
            #return xmlrpclib.dumps(xmlrpclib.Fault(8, str(missing)))
            # uniqueness test goes here
            self.data.append(iobj)

            #now add restrictions through the Get function
            if rupdates:
                self.Get([iobj.to_rx(item)], cargs=rupdates)

            if callback:
                apply(callback, (iobj, ) + cargs)
            retval.append(iobj.to_rx(item))
        return retval

    def Get(self, cdata, callback=None, cargs={}):
        '''Overloading DataSet.Get to check for restriction fields

        does not support a callback function for restrictions'''
        # split cargs into normal properties and checks
        rupdates = {}
        cupdates = {}
        for c in cargs:
            if c in Restriction.__checks__:
                rupdates.update({c:cargs[c]})
            else:
                cupdates.update({c:cargs[c]})

        normalget = Cobalt.Data.DataSet.Get(self, cdata, callback, cupdates)
        
        # rdata is used to query q.restrictions.Get, so copy cdata, and
        # filter for anything that isn't a restriction
        rdata = copy.deepcopy(cdata)
        for rd in rdata:
            for f in rd.keys():
                if f not in Restriction.__checks__:
                    del rd[f]
            rd.update({'tag':'restriction', 'value':'*'})
        # get restrictions for each queue that match cdata
        # (not sure what'll happen here with multiple specs in cdata)
        qrestrictions = {}
        for q in self.data:
            qrestrictions[q.name] = {}
            if [c for c in cdata if q.match(c)]:
                qrestriction = q.restrictions.Get(rdata, cargs=rupdates)
                for r in qrestriction[0]:
                    for cd in cdata:
                        if r in cd:
                            qrestrictions[q.name].update({r:qrestriction[0][r]})

        # update response with queue restrictions, will fail if a
        # queue name is not requested
        for queue in normalget:
            if queue['name'] in qrestrictions.keys():
                queue.update(qrestrictions[queue['name']])

        return normalget

    def GetJobs(self, data, callback=None, cargs={}):
        '''Uses the Data.Get method to retrieve Jobs from Queues
        Also supports moving job objects between Queue objects,
        respecting queue restrictions'''
        failed = []  #messages for jobs that failed to switch queues
        if isinstance(cargs, types.DictType) and cargs.has_key('queue'):
            jobs = [q.Get(data) for q in self.data]
            newqueue = [q for q in self.data if q.name == cargs['queue']]
            if not newqueue:
                raise xmlrpclib.Fault(30, "Queue '%s' doesn't exist" % (cargs['queue']))
            for j in jobs[1:]:
                jobs[0].extend(j)
            for job in jobs[0]:
                [(oldjob, oldqueue)] = [(j, q) for q in self.data for j in q if j.jobid == job.jobid]
                if oldjob.state == 'running':
                    failed.append("Job %s not moved to queue '%s' because job is running" % (oldjob.jobid, cargs['queue']))
                    continue
                newjob = copy.deepcopy(oldjob)
                newjob.queue = cargs['queue']
                try:
                    self.CanQueue(None, newjob)
                    oldjob.queue = cargs['queue']
                    newqueue[0].append(oldjob)
                    oldqueue.remove(oldjob)
                except xmlrpclib.Fault, flt:
                    if flt.faultCode == 30:
                        failed.append("WARNING: Job %s moved to '%s' queue, even though the job does not pass these restrictions:\n%s\nThe job will run if the '%s' queue is running." % (oldjob.jobid, cargs['queue'], flt.faultString, cargs['queue']))
                    oldjob.queue = cargs['queue']
                    newqueue[0].append(oldjob)
                    oldqueue.remove(oldjob)
            del cargs['queue']
        joblist = [Q.Get(data, callback, cargs) for Q in self.data]

        if failed:
            raise xmlrpclib.Fault(30, ('\n').join(failed))
                
        for j in joblist[1:]:
            joblist[0].extend(j)
        if joblist:
            return joblist[0]
        else:
            return []

    def DelJobs(self, data):
        for Q in self.data:
            Q.Del([data])
            
    def CanQueue(self, _, jobspec):
        '''Check that job meets criteria of the specified queue'''
        # if queue doesn't exist, don't check other restrictions
        if jobspec['queue'] not in [q.name for q in self.data]:
            raise xmlrpclib.Fault(30, "Queue '%s' does not exist" % jobspec['queue'])

        [testqueue] = [q for q in self.data if q.name == jobspec['queue']]

        # check if queue is dead or draining
        if testqueue.state in ['draining', 'dead']:
            raise xmlrpclib.Fault(30, "The '%s' queue is %s" % (testqueue.name, testqueue.state))

        # test job against queue restrictions
        probs = ''
        for restriction in [r for r in testqueue.restrictions if r.type == 'queue']:
            result = restriction.CanAccept(job)
            if not result[0]:
                probs = probs + result[1] + '\n'
        if probs:
            raise xmlrpclib.Fault(30, probs)
        else:
            return (True, probs)

    def CanRun(self, _, qstate, newjob):
        '''Checks if newjob can run with current state of queue'''
        # if queue doesn't exist, don't check other restrictions
        if newjob.queue not in [q.name for q in self.data]:
            raise xmlrpclib.Fault(30, "Queue '%s' does not exist" % newjob.queue)

        [testqueue] = [q for q in self.data if q.name == newjob.queue]
        probs = ''
        for restriction in [r for r in testqueue.restrictions if r.type == 'run']:
            result = restriction.CanAccept(newjob, qstate)
            if not result[0]:
                probs = probs + result[1] + '\n'
        if probs:
            raise xmlrpclib.Fault(30, probs)
        else:
            return (True, probs)

class CQM(Cobalt.Component.Component):
    '''Cobalt Queue Manager'''
    __implementation__ = 'cqm'
    __name__ = 'queue-manager'
    __statefields__ = ['Queues']
    async_funcs = ['assert_location', 'progress', 'pm_sync', 'sm_sync']

    def __init__(self, setup):
        self.Queues = QueueSet()
        Cobalt.Component.Component.__init__(self, setup)

        # make sure default queue exists
#         if not [q for q in self.Queues if q.name == 'default']:
#             self.Queues.Add([{'tag':'queue', 'name':'default'}])

        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.comms = Cobalt.Proxy.CommDict()
        self.cqp = Cobalt.Cqparse.CobaltLogParser()
        
        self.register_function(lambda  address, data:self.Queues.GetJobs(data), "GetJobs")
        self.register_function(self.handle_job_add, "AddJob")
        self.register_function(self.handle_job_del, "DelJobs")
        self.register_function(lambda  address, data:self.Queues.Get(data), "GetQueues")
        self.register_function(lambda  address, data:self.Queues.Add(data), "AddQueue")
        self.register_function(self.handle_queue_del, "DelQueues")
        self.register_function(lambda  address, data, updates:self.Queues.Get(data, lambda queue, newattr:queue.update(newattr), updates), "SetQueues")
        self.register_function(self.Queues.CanQueue, "CanQueue")
        self.register_function(self.Queues.CanRun, "CanRun")
        self.register_function(lambda address, data, nodelist:
                               self.Queues.GetJobs(data, lambda job, nodes:job.Run(nodes), nodelist),
                               'RunJobs')
        self.register_function(lambda address, data, updates:
                               self.Queues.GetJobs(data, lambda job, newattr:job.update(newattr), updates),
                               'SetJobs')
        self.register_function(self.get_jobid, 'GetJobID')
        self.register_function(self.set_jobid, 'SetJobID')
        self.register_function(self.handle_queue_history, "GetHistory")
        self.register_function(self.invoke_mpi_from_script, "ScriptMPI")


    def get_jobid(self, _):
        '''Get next jobid'''
        return self.Queues.__id__.idnum + 1

    def set_jobid(self, _, jobid):
        '''Set next jobid for new job'''
        self.Queues.__id__.idnum = jobid-1
        return True

    def progress(self):
        '''Process asynchronous job work'''
        [j.Progress() for j in [j for queue in self.Queues for j in queue] if j.active]
        overtime_jobs = [j for j in [j for queue in self.Queues for j in queue] if j.over_time() and not j.killed]
        for job in overtime_jobs:
            job.Kill("Job %s Overtime, Killing")
            job.pbslog.log("A",
                # No attributes.
            )
        finished_jobs = [j for j in [j for queue in self.Queues for j in queue] if j.state == 'done']
        for job in finished_jobs:
            job.LogFinish()
        [queue.remove(j) for (j, queue) in [(j, queue) for queue in self.Queues for j in queue] if j.state == 'done']
        [self.Queues.remove(q) for q in self.Queues.data[:]
         if q.state == 'dead' and q.name.startswith('R.')
         and len(q.data) == 0]
        #newdate = time.strftime("%m-%d-%y", time.localtime())
        #[j.acctlog.ChangeLog() for j in [j for queue in self.Queues for j in queue] if newdate != self.prevdate]
        #Job.acctlog.ChangeLog()
        return 1

    def handle_job_add(self, _, jobspec):
        '''Add a job, throws in adminemail'''
        [queue] = [q for q in self.Queues if q.name == jobspec['queue']]
        jobspec.update({'adminemail':queue.adminemail})
        response = queue.Add(jobspec)
        return response

    def handle_job_del(self, _, data, force=False, user=None):
        '''Delete a job'''
        ret = []
        for spec in data:
            for job, q in [(job, queue) for queue in self.Queues for job in queue if job.match(spec)]:
                ret.append(job.to_rx(spec))
                if job.state in ['queued', 'ready'] or (job.state == 'hold' and not job.pgid):
                    #q.remove(job)
                    q.Del(spec)
                elif force:
                    # Need acct log message for forced delete, 
                    # otherwise can't tell if job ever ended
                    job.Kill("Job %s killed based on admin request")
                    q.Del(spec)
                else:
                    job.Kill("Job %s killed based on user request")
                # It's my understanding that the above code draws a distinction
                # between killing a running job and killing a job that hasn't started yet.
                # I don't think PBS logs draw this distionction.
                job.pbslog.log("D",
                    requester = user or job.user, # who deleted the job
                )
        return ret

    def handle_queue_del(self, _, cdata, force=False):
        '''Delete queue(s), but check if there are still jobs in the queue'''
        if force:
            return self.Queues.Del(cdata)
        
        queues = [self.Queues[spec["name"]] for spec in self.Queues.Get(cdata)]
        
        failed = []
        for queue in queues[:]:
            jobs = list(iter(queues))
            if len(jobs) > 0:
                failed.append(queue.name)
                queues.remove(queue)
        response = self.Queues.Del([queue.to_rx() for queue in queues])
        if failed:
            raise xmlrpclib.Fault(31, "The %s queue(s) contains jobs. Either move the jobs to another queue, or \nuse 'cqadm -f --delq' to delete the queue(s) and the jobs.\n\nDeleted Queues\n================\n%s" % (",".join(failed), "\n".join([q.name for q in response])))
        else:
            return response

    def handle_queue_history(self, _, data):
        '''Fetches queue history from acct log'''
        self.cqp.perform_default_parse()
        return self.cqp.Get(data)

    def pm_sync(self):
        '''Resynchronize with the process manager'''
        try:
            pgs = self.comms['pm'].GetProcessGroup([{'tag':'process-group', 'pgid':'*', 'state':'running'}])
        except Cobalt.Proxy.CobaltComponentError:
            self.logger.error("Failed to connect to the process manager")
            return
        live = [item['pgid'] for item in pgs]
        for job in [j for queue in self.Queues for j in queue if j.mode!='script']:
            for pgtype in job.pgid.keys():
                pgid = job.pgid[pgtype]
                if pgid not in live:
                    self.logger.info("Found dead pg for job %s" % (job.jobid))
                    job.CompletePG(pgid)

    def sm_sync(self):
        '''Resynchronize with the script manager'''
        try:
            pgs = self.comms['sm'].GetProcessGroup([{'tag':'process-group', 'pgid':'*', 'state':'running'}])
        except Cobalt.Proxy.CobaltComponentError:
            self.logger.error("Failed to connect to the script manager")
            return
        live = [item['pgid'] for item in pgs]
        for job in [j for queue in self.Queues for j in queue if j.mode=='script']:
            for pgtype in job.pgid.keys():
                pgid = job.pgid[pgtype]
                if pgid not in live:
                    self.logger.info("Found dead pg for job %s" % (job.jobid))
                    job.CompletePG(pgid)

    def invoke_mpi_from_script(self, _, data):
        '''Invoke the real mpirun on behalf of a script being executed by the script manager.'''
        d = {'tag':'job', 'pgid':'*'}
        d.update(data)
        j = ScriptMPIJob(d, d.get('jobid'))
        j.RunScriptMPIJob()
        
        return j.pgid['user']


if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        opts = getopt(sys.argv[1:], 'dC:D:', [])[0]
    except GetoptError, msg:
        print "%s\nUsage:\ncqm.py [-d] [-C <configfile>] [-D <pidfile>]" % (msg)
        raise SystemExit, 1
    try:
        __daemon__ = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        __daemon__ = False
    __dlevel__ = logging.INFO
    if len([x for x in opts if x[0] == '-d']):
        __dlevel__ = logging.DEBUG
    Cobalt.Logging.setup_logging('cqm', level=__dlevel__)
    logger = logging.getLogger('cqm')
    __server__ = CQM({'configfile':'/etc/cobalt.conf', 'daemon':__daemon__})
    __server__.serve_forever()
