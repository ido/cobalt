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

    def __init__(self, data, jobid):
        Cobalt.Data.Data.__init__(self, data)
        self.comms = Cobalt.Proxy.CommDict()
        self.set('jobid', str(jobid))
        self.set('state', 'queued')
        if not self.get('attribute', False):
            self.set('attribute', 'compute')
        self.set('location', 'N/A')
        self.set('starttime', '-1')
        if not self.get('queue', False):
            self.set('queue', 'default')
        self.staged = 0
        self.killed = False
        self.timers = {}
        self.timers['queue'] = Timer()
        self.timers['queue'].Start()
        #self.timers['/usr/sbin/prologue'] = Timer()
        self.timers['user'] = Timer()
        #self.timers['/usr/sbin/epilogue'] = Timer()
        self.pgid = {}
        self.spgid = {}
        #self.steps = ['StageInit', 'FinishStage', 'RunPrologue', 'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'FinalizeStage', 'Finish']
        #self.steps = ['StageInit', 'FinishStage', 'RunPrologue',
        #              'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'FinalizeStage', 'Finish']
        #self.steps=['StageInit','FinishStage','RunPrologue','RunUserJob','RunEpilogue','FinalizeStage','Finish']
        self.steps = ['RunPrologue', 'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'Finish']
        self.stageid = None
        self.reservation = False
        if not self.get('type', False):
            self.set('type', 'mpish')
        #AddEvent("queue-manager", "job-submitted", self.get('jobid'))
        self.SetPassive()
        # acctlog
        logger.info('Q;%s;%s;%s' % \
                    (self.get('jobid'), self.get('user'), self.get('queue')))
        self.acctlog.LogMessage('Q;%s;%s;%s' % \
                                (self.get('jobid'), self.get('user'), self.get('queue')))

    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['log', 'comms', 'acctlog']:
                data[key] = value
        return data

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.acctlog = Cobalt.Util.AccountingLog('qm')
        self.comms = Cobalt.Proxy.CommDict()

    def fail_job(self, state):
        '''Signal complete job failure, resulting in specified state'''
        self.set('state', state)
        self.steps = []

    def WriteOutput(self):
        '''Write user output to the file system'''
        try:
            open("%s/%s.output" % (self.get('outputdir'), self.get('jobid')), 'w').write(self.output)
            open("%s/%s.error" % (self.get('outputdir'), self.get('jobid')), 'w').write(self.error)
        except IOError:
            logger.error("Failed to write to userdir for job %s writing to /tmp instead" % self.get('jobid'))
            open("%s/%s.output" % ('/tmp', self.get('jobid')), 'w').write(self.output)
            open("%s/%s.error" % ('/tmp', self.get('jobid')), 'w').write(self.error)

    def CheckProject(self):
        '''Check that a user is part of the supplied project'''
        try:
            proj = self.comms['am'].GetProject([{'tag':'project', 'name':self.get('project'), 'users':'*'}])
        except:
            logger.error("Failed to contact allocation manager")
            self.fail_job('am-error')
            return
        if len(proj) < 1 or self.get('user') not in proj[0]['user']:
            if len(proj) == 0:
                logger.error("Project specification error for user %s, project %s. (no such project)" % (
                    self.get('user'), self.get('project')))
            else:
                logger.error("User %s not in project %s" % (self.get('user'), self.get('project')))
            self.fail_job('am-error')
            return
        try:
            lien = self.comms['am'].AddLien(self.get('project'), self.get('user'),
                                            float(self.get('walltime')) * 60 * int(self.get('nodes')))
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
        used_time = int(self.timers['user'].Check()) * len(self.get('location').split(':'))
        try:
            self.comms['am'].CommitLien(self.get('lienID'), used_time)
        except:
            pass
                                                                
        self.set('state', 'done')
        self.SetPassive()
        #AddEvent("queue-manager", "job-completed", self.get('jobid'))
        # acctlog
        logger.info('E;%s;%s;%s' % \
                    (self.get('jobid'), self.get('user'), str(used_time)))
        self.acctlog.LogMessage('E;%s;%s;%s' % \
                                (self.get('jobid'), self.get('user'), str(used_time)))

    def Progress(self):
        '''Run next job step'''
        if not self.steps:
            logger.error("Manually setting passive for job %s" % (self.get('jobid')))
            self.SetPassive()
            return
        logger.info("Job %s/%s: running step %s" % (self.get('jobid'), self.get('user'), self.steps[0]))
        currentstep = self.steps[0]
        try:
            getattr(self, self.steps[0])()
        except:
            logger.error("Unexpected failure jobid:%s step:%s" % (self.get('jobid'), currentstep),
                         exc_info=1)
            self.SetPassive()
            return

        if len(self.steps) > 1:
            self.steps = self.steps[1:]
        else:
            self.set('state', 'done')
            
    def Run(self, nodelist):
        '''Run a job'''
        if self.get('state') not in ['ready', 'queued', 'stage-pending', 'prologue']:
            logger.info("Got multiple run commands for job %s" % self.get('jobid'))
            return
        self.timers['queue'].Stop()
        if self.get('reservation', False):
            # acctlog
            logger.info('R;%s;%s;%s' % \
                        (self.get('jobid'), self.get('queue'), self.get('user')))
            self.acctlog.LogMessage('R;%s;%s;%s' % \
                                    (self.get('jobid'), self.get('queue'), self.get('user')))
        else:
            # acctlog
            logger.info('S;%s;%s;%s;%s;%s;%s;%s' % (
                self.get('jobid'), self.get('user'), self.get('name', 'N/A'),
                self.get('nodes'), self.get('procs'), self.get('mode'),
                self.get('walltime')))
            self.acctlog.LogMessage('S;%s;%s;%s;%s;%s;%s;%s' % (
                self.get('jobid'), self.get('user'), self.get('name', 'N/A'),
                self.get('nodes'), self.get('procs'), self.get('mode'),
                self.get('walltime')))
        self.set('location', ":".join(nodelist))
        self.set('starttime', str(time.time()))
        self.SetActive()
        if self.get('project', 'XX') != 'XX':
            logger.info("Job %s/%s/%s/Q:%s: Running job on %s" % \
                                    (self.get('jobid'), self.get('user'),
                                     self.get('project'), self.get('queue'),
                                     ":".join(nodelist)))
            self.acctlog.LogMessage("Job %s/%s/%s/Q:%s: Running job on %s" % \
                                    (self.get('jobid'), self.get('user'),
                                     self.get('project'), self.get('queue'),
                                     ":".join(nodelist)))
        else:
            logger.info("Job %s/%s/Q:%s: Running job on %s" % \
                        (self.get('jobid'), self.get('user'),
                         self.get('queue'), ":".join(nodelist)))
            self.acctlog.LogMessage("Job %s/%s/Q:%s: Running job on %s" % \
                                    (self.get('jobid'), self.get('user'),
                                     self.get('queue'), ":".join(nodelist)))

    def FinishStage(self):
        '''Complete a stage'''
        self.set('state', 'stage-pending')
        if not self.staged:
            self.SetPassive()
            self.steps = ['FinishStage'] + self.steps
        else:
            self.set('state', 'ready')
            #AddEvent("queue-manager", "job-ready", self.get('jobid'))
            self.SetActive()     

    def FinishUserPgrp(self):
        '''Complete a process group for the user job'''
        self.timers['user'].Stop()
        if self.spgid.has_key('user'):
            try:
                #pgroups = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'output':'*', 'error':'*'}])
                result = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'exit-status':'*'}])
                self.set('exit-status', result[0].get('exit-status'))
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
            logger.error("No record of pgid for user job %s" % (self.get('jobid')))
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
            stagespec = {'tag':'stage', 'outputdir':self.get('outputdir'), 'name':self.get('jobid'),
                         'size':self.get('nodes'), 'user':self.get('user'),
                         'script':xml.sax.saxutils.escape(self.get('script'))}
            if self.get('stagein', None):
                stagespec['in'] = self.get('stagein')
            if self.get('stageout', None):
                stagespec['out'] = self.get('stageout')
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
        logger.debug("Got stageid %s for job %s" % (self.stageid, self.get('jobid')))

    def RunPrologue(self):
        '''Run the job prologue'''
        self.timers['/usr/sbin/prologue'] = Timer()
        if self.get('location') == 'none':
            # requeue if not ready
            self.steps = ['RunPrologue'] + self.steps
            self.SetPassive()
            return
        self.set('state', 'prologue')
        #this path and executable should be pulled from cfg file
        try:
            os.system("/master/bcfg/generators/account/setaccess.py -a %s %s" % (self.get('user'),
                                                                                 " ".join(self.get('location'))))
        except:
            logger.info("access control not enabled")
        self.timers['/usr/sbin/prologue'].Start()
        self.AdminStart('/usr/sbin/prologue')
        self.SetPassive()

    def RunEpilogue(self):
        '''Run the job epilogue'''
        self.timers['/usr/sbin/epilogue'] = Timer()
        self.set('state', 'epilogue')
        os.system("/master/bcfg/generators/account/setaccess.py -r %s %s" % (self.get('user'),
                                                                             " ".join(self.get('location').split(':'))))
        self.timers['/usr/sbin/epilogue'].Start()
        self.AdminStart('/usr/sbin/epilogue')
        self.SetPassive()

    def RunUserJob(self):
        '''Run the user job'''
        self.set('state', 'running')
        self.timers['user'].Start()
        args = []
        if self.get("host", False):
            args = ["-i", "-h", self.get('host'), "-p", self.get('port')]
        if self.get("url", False):
            args += ["-b", self.url]
        if self.get("stageid", False):
            args += ["-n", self.stageid]
        elif self.get("command", False):
            args += ["-f", self.get('command')]
        if self.get("stageout", False):
            args += ["-s", self.get('stageout')]
        if self.get("type", '') == 'pbs':
            args.append("-P")
        args.append("-t")
        args.append(str(60 * float(self.get('walltime'))))
        location = self.get('location').split(':')
        outputfile = "%s/%s.output" % (self.get('outputdir'), self.get('jobid'))
        errorfile = "%s/%s.error" % (self.get('outputdir'), self.get('jobid'))
        cwd = self.get('cwd', self.get('envs')['data']['PWD'])
        env = self.get('envs')['data']
        try:
            pgroup = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'user':self.get('user'), 'pgid':'*', 'executable':'/usr/bin/mpish',
                 'size':self.get('procs'), 'args':args, 'envs':env, 'errorfile':errorfile,
                 'outputfile':outputfile, 'location':location, 'cwd':cwd, 'path':"/bin:/usr/bin:/usr/local/bin"})
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
        logger.info(killmsg % (self.get('jobid')))
        if self.get('state') in ['epilogue', 'cleanup']:
            logger.info("Not killing job %s during recovery" % (self.get('jobid')))
        elif self.get('state') in ['setup', 'prologue', 'stage-pending', 'stage-error', 'pm-error']:
            # first kill the lien
            try:
                self.comms['am'].DelLien({'tag':'lien', 'id':self.get('lienID')})
            except:
                logger.error("Failed to delete lien id %s for project %s" % (self.get('lienID', ""), self.get('project')))
            # then perform step manipulation
            if self.get('state') in ['setup', 'prologue']:
                self.steps.remove('RunUserJob')
            # then activate if needed
            if self.get('state') in ['stage-pending']:
                self.SetActive()
            else:
                self.SetPassive()
            if self.get('state') in ['stage-error', 'pm-error']:
                self.set('state', 'done')
        elif self.get('state') == 'running':
            if not self.pgid.has_key('user'):
                logger.error("Job %s has no pgroup associated with it" % self.get('jobid'))
            else:
                self.KillPGID(self.pgid['user'])
        elif self.get('state') == 'hold':  #job in 'hold' and running
            self.KillPGID(self.pgid['user'])
        else:
            logger.error("Got qdel for job %s in unexpected state %s" % (self.get('jobid'), self.get('state')))
 
        # acctlog
        logger.info('D;%s;%s' % (self.get('jobid'), self.get('user')))
        self.acctlog.LogMessage('D;%s;%s' % (self.get('jobid'), self.get('user')))

    def AdminStart(self, cmd):
        '''Run an administrative job step'''
        location = self.get('location').split(':')
        try:
            pgrp = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'pgid':'*', 'user':'root', 'size':self.get('nodes'),
                 'path':"/bin:/usr/bin:/usr/local/bin", 'cwd':'/', 'executable':cmd, 'envs':{},
                 'args':[self.get('user')], 'location':location})
        except xmlrpclib.Fault, fault:
            print fault
        except:
            logger.error("Unexpected failure in administrative process start", exc_info=1)
            self.set('state', 'pm-error')
            return
        
        self.pgid[cmd] = pgrp[0]['pgid']

    def CompletePG(self, pgid):
        '''Finish accounting for a completed jobid'''
        for (t, pg) in [item for item in self.pgid.iteritems() if item[1] == pgid]:
            logger.info("Job %s/%s: %s completed" % (self.get('jobid'), self.get('user'), t))
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
        if self.get('state') == 'running':
            runtime = self.timers['user'].Check()/60.0
            if float(self.get('walltime')) < runtime:
                return 1
        return 0

#     # Here begins the testbed stuff
#     def StartRebuild(self):
#         self.Rebuild(self.get('image'), self.get('kernel'))

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
#         if not ((self.built >= 2 * int(self.get('nodes'))) and (self.booted >= 2 * int(self.get('nodes')))):
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
                    (self.get('jobid'), self.get('user'),
                     self.get('nodes'), self.GetStats()))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit code %s" % \
                                (self.get('jobid'), self.get('user'),
                                 self.get('nodes'), self.GetStats()))
        
        #AddEvent("queue-manager", "job-done", self.get('jobid'))

class BGJob(Job):
    '''BG Job is a Blue Gene/L job'''
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
        if self.get('notify', False) or self.get('adminemail', '*') != '*':
            self.steps = ['NotifyAtStart', 'RunBGUserJob', 'NotifyAtEnd', 'FinishUserPgrp', 'Finish']
        else:
            self.steps = ['RunBGUserJob', 'FinishUserPgrp', 'Finish']
        if self.config.get('bgkernel', 'false') == 'true':
            self.steps.insert(0, 'SetBGKernel')
        self.SetPassive()
#         self.acctlog.LogMessage('Q;%s;%s;%s' % \
#                                 (self.get('jobid'), self.get('user'), self.get('queue')))
        
    def SetBGKernel(self):
        '''Ensure that the kernel is set properly prior to job launch'''
        try:
            current = os.readlink('%s/%s' % (self.config.get('partitionboot'), self.get('location')))
        except OSError:
            logger.error("Failed to read partitionboot location %s/%s" % (self.config.get('partitionboot'), self.get('location')))
            logger.info("Job %s/%s using kernel %s" % (self.get('jobid'), self.get('user'), 'N/A'))
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

    def NotifyAtStart(self):
        '''Notify user when job has started'''
        mailserver = self.config.get('mailserver', 'false')
        if mailserver == 'false':
            mserver = 'localhost'
        else:
            mserver = mailserver
        subj = 'Cobalt: Job %s/%s starting - %s/%s' % (self.get('jobid'), self.get('user'), self.get('queue'), self.get('location'))
        mmsg = "Job %s/%s starting on partition %s, in the '%s' queue , at %s" % (self.get('jobid'), self.get('user'), self.get('location'), self.get('queue'), time.strftime('%c', time.localtime()))
        toaddr = []
        if self.get('adminemail') != '*':
            toaddr = toaddr + self.get('adminemail').split(':')
        if self.get('notify', False):
            toaddr = toaddr + self.get('notify').split(':')
        Cobalt.Util.sendemail(toaddr, subj, mmsg, smtpserver=mserver)

    def NotifyAtEnd(self):
        '''Notify user when job has ended'''
        mailserver = self.config.get('mailserver', 'false')
        if mailserver == 'false':
            mserver = 'localhost'
        else:
            mserver = mailserver
        subj = 'Cobalt: Job %s/%s finished - %s/%s %s' % (self.get('jobid'), self.get('user'), self.get('queue'), self.get('location'), self.GetStats())
        mmsg = "Job %s/%s finished on partition %s, in the '%s' queue, at %s\nStats: %s" %  (self.get('jobid'), self.get('user'), self.get('location'), self.get('queue'), time.strftime('%c', time.localtime()), self.GetStats())
        toaddr = []
        if self.get('adminemail') != '*':
            toaddr = toaddr + self.get('adminemail').split(':')
        if self.get('notify', False):
            toaddr = toaddr + self.get('notify').split(':')
        Cobalt.Util.sendemail(toaddr, subj, mmsg, smtpserver=mserver)

    def RunBGUserJob(self):
        '''Run a Blue Gene Job'''
        self.set('state', 'running')
        self.timers['user'].Start()
        if not self.get('outputpath', False):
            self.set('outputpath', "%s/%s.output" % (self.get('outputdir'), self.get('jobid')))
        if not self.get('errorpath', False):
            self.set('errorpath', "%s/%s.error" % (self.get('outputdir'), self.get('jobid')))

        try:
            pgroup = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'user':self.get('user'), 'pgid':'*', 'outputfile':self.get('outputpath'),
                 'errorfile':self.get('errorpath'), 'path':self.get('path'), 'size':self.get('procs'),
                 'mode':self.get('mode', 'co'), 'cwd':self.get('outputdir'), 'executable':self.get('command'),
                 'args':self.get('args'), 'envs':self.get('envs', {}), 'location':[self.get('location')],
                 'jobid':self.get('jobid')})
        except xmlrpclib.Fault:
            raise ProcessManagerError
        except Cobalt.Proxy.CobaltComponentError:
            raise ProcessManagerError
        if not pgroup[0].has_key('pgid'):
            logger.error("Process Group creation failed for Job %s" % self.get('jobid'))
            self.set('state', 'pm-failure')
        else:
            self.pgid['user'] = pgroup[0]['pgid']
        self.SetPassive()

    def LogFinish(self):
        '''Log end of job data'''
        logger.info("Job %s/%s on %s nodes done. %s" % \
                    (self.get('jobid'), self.get('user'),
                     self.get('nodes'), self.GetStats()))
        self.acctlog.LogMessage("Job %s/%s on %s nodes done. %s exit:%s" % \
                                (self.get('jobid'), self.get('user'),
                                 self.get('nodes'), self.GetStats(),
                                 self.get('exit-status').get('BG/L', 'N/A')))

class JobSet(Cobalt.Data.DataSet):
    '''Set of currently queued jobs'''
    __object__ = BGJob

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        #self.__id__ = Cobalt.Data.IncrID()

class Restriction(Cobalt.Data.Data):
    '''Restriction object'''

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

        if info.get('name', None) in ['maxrunning', 'maxusernodes', 'totalnodes']:
            self.set('type','run')
        else:
            self.set('type','queue')
        logger.debug('created restriction %s with type %s' % (self.get('name'), self.get('type')))

    def maxwalltime(self, job, _=None):
        '''checks walltime of job against maxtime of queue'''
        if float( job.get('walltime') ) <= float( self.get('value') ):
            return (True, "")
        else:
            return (False, "Walltime greater than the '%s' queue max walltime of %s" % (job.get('queue'), "%02d:%02d:00" % (divmod(int(self.get('value')), 60))))

    def minwalltime(self, job, _=None):
        '''limits minimum walltime for job'''
        if float( job.get('walltime') ) >= float( self.get('value') ):
            return (True, "")
        else:
            return (False, "Walltime less than the '%s' queue min walltime of %s" % (job.get('queue'), "%02d:%02d:00" % (divmod(int(self.get('value')), 60))))

    def usercheck(self, job, _=None):
        '''checks if job owner is in approved user list'''
        #qusers = self.queue.get('users').split(':')
        qusers = self.get('value').split(':')
        if '*' in qusers or job.get('user') in qusers:
            return (True, "")
        else:
            return (False, "You are not allowed to submit to the '%s' queue" % job.get('queue'))

    def maxuserjobs(self, job, queuestate=None):
        '''limits how many jobs each user can run by checking queue state
        with potential job added'''
        userjobs = [j for j in queuestate if j.get('user') == job.get('user') and j.get('state') == 'running' and j.get('queue') == job.get('queue')]
        if len(userjobs) >= int(self.get('value')):
            return (False, "Maxuserjobs limit reached")
        else:
            return (True, "")

    def maxqueuedjobs(self, job, _=None):
        '''limits how many jobs a user can have in the queue at a time'''
        userjobs = [j for j in self.queue if j.get('user') == job.get('user')]
        if len(userjobs) >= int(self.get('value')):
            return (False, "The limit of %s jobs per user in the '%s' queue has been reached" % (self.get('value'), job.get('queue')))
        else:
            return (True, "")

    def maxusernodes(self, job, queuestate=None):
        '''limits how many nodes a single user can have running'''
        usernodes = 0
        for j in [qs for qs in queuestate if qs.get('user') == job.get('user')
                  and qs.get('state') == 'running'
                  and qs.get('queue') == job.get('queue')]:
            usernodes = usernodes + int(j.get('nodes'))
        if usernodes + int(job.get('nodes')) > int(self.get('value')):
            return (False, "Job exceeds MaxUserNodes limit")
        else:
            return (True, "")

    def maxtotalnodes(self, job, queuestate=None):
        '''limits how many total nodes can be used by jobs running in
        this queue'''
        totalnodes = 0
        for j in [qs for qs in queuestate if qs.get('state') == 'running'
                  and qs.get('queue') == job.get('queue')]:
            totalnodes = totalnodes + int(j.get('nodes'))
        if totalnodes + int(job.get('nodes')) > int(self.get('value')):
            return (False, "Job exceeds MaxTotalNodes limit")
        else:
            return (True, "")

    def CanAccept(self, job, queuestate=None):
        '''Checks if this object will allow the job'''
        logger.debug('checking restriction %s' % self.get('name'))
        func = getattr(self, self.__checks__[self.get('name')])
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
            toupdate = [r for r in self.data if r.get('name') == item.get('name')]
            if toupdate:
                # just update the value
                toupdate[0].set('value', item.get('value'))
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
                    response.update({r.get('name'):r.get('value')})

        return [response]

#     def Test(self, job):
#         '''Test queue restrictions'''
#         probs = ''
#         for restriction in [r for r in self.data if r.get('type') == 'queue']:
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

    def __init__(self, info, _=None):
        Cobalt.Data.Data.__init__(self, info)
        JobSet.__init__(self)

        # set defaults if not set already
        defaults = {'state':'stopped', 'adminemail':'*'}
        for d in defaults:
            if d not in self._attrib:
                self.set(d, defaults[d])

        self.restrictions = RestrictionSet(self)

    def get(self, field, default=None):
        '''Overload Queue get for smartstate'''
        if field == 'smartstate':
            if self.get('cron', False):
                if cronmatch(self.get('cron')):
                    return 'running'
                else:
                    return 'stopped'
            else:
                return self.get('state')
        else:
            return Cobalt.Data.Data.get(self, field, default)

class QueueSet(Cobalt.Data.DataSet):
    '''Set of queues
    self.data is the list of queues known'''
    __object__ = Queue

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
        
        rdata = copy.deepcopy(cdata)
        for rd in rdata:
            rd.update({'tag':'restriction', 'value':'*'})
            if rd.has_key('state'):
                del(rd['state'])

        # get restrictions for each queue that match cdata
        # (not sure what'll happen here with multiple specs in cdata)
        qrestrictions = {}
        for q in self.data:
            if [c for c in cdata if q.match(c)]:
                qrestriction = q.restrictions.Get(rdata, cargs=rupdates)
                qrestrictions.update({q.get('name'):qrestriction[0]})

        # update response with queue restrictions, will probably fail if
        # queue name is not requested
        for queue in normalget:
            queue.update(qrestrictions[queue.get('name')])

        return normalget

    def GetJobs(self, data, callback=None, cargs={}):
        '''Uses the Data.Get method to retrieve Jobs from Queues
        Also supports moving job objects between Queue objects,
        respecting queue restrictions'''
        failed = []  #messages for jobs that failed to switch queues
        if isinstance(cargs, types.DictType) and cargs.has_key('queue'):
            jobs = [q.Get(data) for q in self.data]
            newqueue = [q for q in self.data if q.get('name') == cargs['queue']]
            if not newqueue:
                raise xmlrpclib.Fault(30, "Queue '%s' doesn't exist" % (cargs['queue']))
            for j in jobs[1:]:
                jobs[0].extend(j)
            for job in jobs[0]:
                [(oldjob, oldqueue)] = [(j, q) for q in self.data for j in q if j.get('jobid') == job.get('jobid')]
                newjob = copy.deepcopy(oldjob)
                newjob.set('queue', cargs['queue'])
                try:
                    self.CanQueue(None, newjob)
                    oldjob.set('queue', cargs['queue'])
                    newqueue[0].append(oldjob)
                    oldqueue.remove(oldjob)
                except xmlrpclib.Fault, flt:
                    if flt.faultCode == 30:
                        failed.append("Job %s moved to '%s' queue, even though it does not pass all restrictions:\n%s" % (oldjob.get('jobid'), cargs['queue'], flt.faultString))
                    oldjob.set('queue', cargs['queue'])
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
            
    def CanQueue(self, _, job):
        '''Check that job meets criteria of the specified queue'''
        # if queue doesn't exist, don't check other restrictions
        if job.get('queue') not in [q.get('name') for q in self.data]:
            raise xmlrpclib.Fault(30, "Queue '%s' does not exist" % job.get('queue'))

        [testqueue] = [q for q in self.data if q.get('name') == job.get('queue')]

        # check if queue is dead or draining
        if testqueue.get('state') in ['draining', 'dead']:
            raise xmlrpclib.Fault(30, "The '%s' queue is %s" % (testqueue.get('name'), testqueue.get('state')))

        # test job against queue restrictions
        probs = ''
        for restriction in [r for r in testqueue.restrictions if r.get('type') == 'queue']:
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
        if newjob.get('queue') not in [q.get('name') for q in self.data]:
            raise xmlrpclib.Fault(30, "Queue '%s' does not exist" % newjob.get('queue'))

        [testqueue] = [q for q in self.data if q.get('name') == newjob.get('queue')]
        probs = ''
        for restriction in [r for r in testqueue.restrictions if r.get('type') == 'run']:
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
    async_funcs = ['assert_location', 'progress', 'pm_sync']

    def __init__(self, setup):
        self.Queues = QueueSet()
        Cobalt.Component.Component.__init__(self, setup)

        # make sure default queue exists
#         if not [q for q in self.Queues if q.get('name') == 'default']:
#             self.Queues.Add([{'tag':'queue', 'name':'default'}])

        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.comms = Cobalt.Proxy.CommDict()
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
        self.register_function(self.set_jobid, 'SetJobID')
        self.register_function(self.handle_queue_history, "GetHistory")

    def set_jobid(self, _, jobid):
        '''Set next jobid for new job'''
        self.Queues.__id__.idnum = jobid-1
        return True

    def progress(self):
        '''Process asynchronous job work'''
        [j.Progress() for j in [j for queue in self.Queues for j in queue] if j.active]
        [j.Kill("Job %s Overtime, Killing") for j in [j for queue in self.Queues for j in queue] if j.over_time()]
        [j.LogFinish() for j in [j for queue in self.Queues for j in queue] if j.get('state') == 'done']
        [queue.remove(j) for (j, queue) in [(j, queue) for queue in self.Queues for j in queue] if j.get('state') == 'done']
        #newdate = time.strftime("%m-%d-%y", time.localtime())
        #[j.acctlog.ChangeLog() for j in [j for queue in self.Queues for j in queue] if newdate != self.prevdate]
        #Job.acctlog.ChangeLog()
        return 1

    def handle_job_add(self, _, data):
        '''Add a job, throws in adminemail'''
        [thequeue] = [q for q in self.Queues if q.get('name') == data.get('queue')]
        data.update({'adminemail':thequeue.get('adminemail')})
        response = thequeue.Add(data)
        return response

    def handle_job_del(self, _, data, force=False):
        '''Delete a job'''
        ret = []
        for spec in data:
            for job, q in [(job, queue) for queue in self.Queues for job in queue if job.match(spec)]:
                ret.append(job.to_rx(spec))
                if job.get('state') in ['queued', 'ready'] or force or (job.get('state') == 'hold' and not job.pgid):
                    #q.remove(job)
                    q.Del(spec)
                else:
                    job.Kill("Job %s killed based on user request")
        return ret

    def handle_queue_del(self, _, data, force=False):
        '''Delete queue(s), but check if there are still jobs in the queue'''
        if force:
            return self.Queues.Del(data)

        failed = []
        queues = self.Queues.Get(data)
        for queue in queues[:]:
            jobs = [j for q in self.Queues for j in q if q.get('name') == queue.get('name')]
            if len(jobs) > 0:
                failed.append(queue.get('name'))
                queues.remove(queue)
        response = self.Queues.Del(queues)
        if failed:
            raise xmlrpclib.Fault(31, "The %s queue(s) contains jobs. Either move the jobs to another queue, or \nuse 'cqadm -f --delq' to delete the queue(s) and the jobs.\n\nDeleted Queues\n================\n%s" % (",".join(failed), "\n".join([q.get('name') for q in response])))
        else:
            return response

    def handle_queue_history(self, _, data):
        '''Fetches queue history from acct log'''
        print 'data is', data
        cqp = Cobalt.Cqparse.CobaltLogParser()
        cqp.perform_default_parse()
        return cqp.Get(data)

    def pm_sync(self):
        '''Resynchronize with the process manager'''
        try:
            pgs = self.comms['pm'].GetProcessGroup([{'tag':'process-group', 'pgid':'*', 'state':'running'}])
        except Cobalt.Proxy.CobaltComponentError:
            self.logger.error("Failed to connect to the process manager")
            return
        live = [item['pgid'] for item in pgs]
        for job in [j for queue in self.Queues for j in queue]:
            for pgtype in job.pgid.keys():
                pgid = job.pgid[pgtype]
                if pgid not in live:
                    self.logger.info("Found dead pg for job %s" % (job.get('jobid')))
                    job.CompletePG(pgid)

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
