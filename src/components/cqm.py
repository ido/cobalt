#!/usr/bin/env python
# $Id: cqm.py 1.35 05/10/07 16:04:16-05:00 desai@topaz.mcs.anl.gov $

'''Cobalt Queue Manager'''
__revision__ = '$Revision: 1.35 $'

from logging import getLogger, FileHandler, Formatter, INFO

import logging, os, sys, time, xml.sax.saxutils, xmlrpclib, ConfigParser, copy, types
import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util

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

class Logger(object):
    '''This logger object writes out accounting log records'''
    def __init__(self):
        _configfields = ['log_dir']
        _config = ConfigParser.ConfigParser()
        if '-C' in sys.argv:
            _config.read(sys.argv[sys.argv.index('-C') + 1])
        else:
            _config.read('/etc/cobalt.conf')
        if not _config._sections.has_key('cqm'):
            print '''"%s" section missing from cobalt config file''' % ('cqm')
            raise SystemExit, 1
        self.config = _config._sections['cqm']
        mfields = [field for field in _configfields if not self.config.has_key(field)]
        if mfields:
            print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
            raise SystemExit, 1

        self.logger = getLogger('cqm')
        self.hdlr = FileHandler('%s/%s-%s.log' % (
            self.config['log_dir'], 'cqm', time.strftime("%m-%d-%y", time.localtime())))
        self.formatter = Formatter('%(asctime)s;%(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(INFO)

    def ChangeLog(self):
        '''Implement log rotation'''
        self.logger.removeHandler(self.hdlr)
        self.hdlr.close()
        self.hdlr = FileHandler('%s/%s-%s.log' % (
            self.config['log_dir'], 'cqm', time.strftime("%m-%d-%y", time.localtime())))
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.prevdate = time.strftime("%m-%d-%y", time.localtime())

    def LogMessage(self, message):
        '''record accounting message'''
        self.logger.info(message)


class CommDict(dict):
    '''CommDict is a dictionary that automatically instantiates a component proxy upon access'''
    commnames = {'pm':'process_manager', 'fs':'file_stager', 'am':'allocation_manager'}

    def __getitem__(self, name):
        if not self.has_key(name):
            self.__setitem__(name, getattr(Cobalt.Proxy, self.commnames[name])())
        return dict.__getitem__(self, name)

class Job(Cobalt.Data.Data):
    '''The Job class is an object corresponding to the qm notion of a queued job, including steps'''

    acctlog = Logger()

    def __init__(self, data, jobid):
        Cobalt.Data.Data.__init__(self, data)
        self.comms = CommDict()
        self.set('jobid', str(jobid))
        self.set('state', 'queued')
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
        self.steps = ['StageInit', 'FinishStage', 'RunPrologue',
                      'RunUserJob', 'RunEpilogue', 'FinishUserPgrp', 'FinalizeStage', 'Finish']
        #self.steps=['StageInit','FinishStage','RunPrologue','RunUserJob','RunEpilogue','FinalizeStage','Finish']
        self.stageid = None
        self.reservation = False
        if not self.get('type', False):
            self.set('type', 'mpish')
        #AddEvent("queue-manager", "job-submitted", self.get('jobid'))
        self.SetActive()
        self.acctlog.LogMessage('Q;%s;%s;%s' % (self.get('jobid'), self.get('user'), self.get('queue')))

    def __getstate__(self):
        data = {}
        for key, value in self.__dict__.iteritems():
            if key not in ['log', 'comms', 'acctlog']:
                data[key] = value
        return data

    def __setstate__(self, state):
        self.__dict__.update(state)
        #self.acctlog = Logger()
        self.comms = CommDict()

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
        self.acctlog.LogMessage('E;%s;%s;%s' % (self.get('jobid'), self.get('user'), str(used_time)))

    def Progress(self):
        '''Run next job step'''
        if not self.steps:
            logger.error("Manually setting passive for job %s" % (self.get('jobid')))
            self.SetPassive()
            return
        logger.info("Job %s/%s: running step %s" % (self.get('jobid'), self.get('user'), self.steps[0]))
        try:
            getattr(self, self.steps[0])()
        except:
            logger.error("Unexpected failure jobid:%s step:%s" % (self.get('jobid'), self.steps[0]),
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
            self.acctlog.LogMessage('R;%s;%s;%s' % (self.get('jobid'), self.get('queue'), self.get('user')))
        else:
            self.acctlog.LogMessage('S;%s;%s;%s;%s;%s;%s;%s;%s' % (
                self.get('jobid'), self.get('user'), self.get('name', 'N/A'), self.get('nodes'), self.get('nodes'),
                self.get('procs'), self.get('mode'), self.get('walltime')))
        self.set('location', ":".join(nodelist))
        self.set('starttime', str(time.time()))
        self.SetActive()
        if self.get('project', 'XX') != 'XX':
            logger.info("Job %s/%s/%s/Q:%s: Running job on %s" % (self.get('jobid'), self.get('user'),
                                                             self.get('project'), self.get('queue'), ":".join(nodelist)))
        else:
            logger.info("Job %s/%s/Q:%s: Running job on %s" % (self.get('jobid'),
                                                          self.get('user'), self.get('queue'), ":".join(nodelist)))

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
                pgroups = self.comms['pm'].WaitProcessGroup([{'tag':'process-group', 'pgid':self.spgid['user'], 'output':'*', 'error':'*'}])
                #self.output = pgroups[0]['output']
                #self.error = pgroups[0]['error']
            except xmlrpclib.Fault, fault:
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
        if self.get('location') == 'none':
            # requeue if not ready
            self.steps = ['RunPrologue'] + self.steps
            self.SetPassive()
            return
        self.set('state', 'prologue')
        os.system("/master/bcfg/generators/account/setaccess.py -a %s %s" % (self.get('user'),
                                                                             " ".join(self.get('location').split(':'))))
        self.timers['/usr/sbin/prologue'].Start()
        self.AdminStart('/usr/sbin/prologue')
        self.SetPassive()

    def RunEpilogue(self):
        '''Run the job epilogue'''
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
        if self.get("host", None):
            args = ["-i", "-h", self.get('host'), "-p", self.get('port')]
        if self.get("url", None):
            args += ["-b", self.url]
        if self.get("stageid", None):
            args += ["-n", self.stageid]
        else:
            args += ["-c", self.get('script')]
        if self.get("stageout", None):
            args += ["-s", self.get('stageout')]
        if self.get("type", None) == 'pbs':
            args.append("-P")
        args.append("-t")
        args.append(str(60 * float(self.get('walltime'))))
        try:
            pgroup = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'user':self.get('user'), 'pgid':'*', 'executable':'/usr/bin/mpish',
                 'size':self.get('nodes'), 'args':args, 'envs':self.get('envs'),
                 'location':self.get('location'), 'cwd':'/', 'path':"/bin:/usr/bin:/usr/local/bin"})
        except xmlrpclib.Fault, fault:
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
                logger.error("Failed to delete lien id %s for project %s" % (self.get('lienID'), self.get('project')))
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
 
        self.acctlog.LogMessage('D;%s;%s' % (self.get('jobid'), self.get('user')))

    def AdminStart(self, cmd):
        '''Run an administrative job step'''
        try:
            pgrp = self.comms['pm'].CreateProcessGroup(
                {'tag':'process-group', 'pgid':'*', 'user':'root', 'size':self.get('nodes'),
                 'path':"/bin:/usr/bin:/usr/local/bin", 'cwd':'/', 'executable':cmd, 'envs':{},
                 'args':[self.get('user')], 'location':self.get('location')})
        except xmlrpclib.Fault, fault:
            print fault.code
        except:
            logger.error("Unexpected failure in administrative process start", exc_info=1)
            self.set('state', 'pm-error')
            return
        
        self.pgid[cmd] = pgrp['pgid']

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
            pgroup = self.comms['pm'].KillProcessGroup({'tag':'process-group', 'pgid':pgid})
        except xmlrpclib.Fault, fault:
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
            result += "%s:%.02fs " % (name, timer.Check())
        return result

    def LogFinish(self):
        '''Log end of job data'''
        logger.info("Job %s/%s on %s nodes done. %s" % (self.get('jobid'),
                                                        self.get('user'), self.get('nodes'), self.GetStats()))
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
        if self.get('notify', False):
            self.steps = ['NotifyAtStart', 'RunBGUserJob', 'NotifyAtEnd', 'FinishUserPgrp', 'Finish']
        else:
            self.steps = ['RunBGUserJob', 'FinishUserPgrp', 'Finish']
        if self.config.get('bgkernel', 'false') == 'true':
            self.steps.insert(0, 'SetBGKernel')
        self.SetPassive()
#         self.acctlog.LogMessage('Q;%s;%s;%s' % (self.get('jobid'), self.get('user'), self.get('queue')))
        
    def SetBGKernel(self):
        '''Ensure that the kernel is set properly prior to job launch'''
        current = os.readlink('/%s/%s' % (self.config.get('partitionboot'), self.get('location')))
        if current != "/%s/%s" % (self.config.get('bootprofiles'), self.get('kernel')):
            logger.info("Updating boot image for %s" % (self.get('location')))
            logger.info("Set to %s should be %s" % (current.split('/')[-1], self.get('kernel')))
            try:
                os.unlink('/%s/%s' % (self.config.get('partitionboot'), self.get('location')))
                os.symlink('/%s/%s' % (self.config.get('bootprofiles'), self.get('kernel')),
                           '/%s/%s' % (self.config.get('partitionboot'), self.get('location')))
            except OSError:
                logger.error("Failed to reset boot location for partition for %s" % (self.get('location')))

    def NotifyAtStart(self):
        '''Notify user when job has started'''
        subj = 'Cobalt: job %s started' % self.get('jobid')
        msg = 'Job %s starting on partition %s, at %s' % (self.get('jobid'), self.get('location'), time.strftime('%c', time.localtime()))
        Cobalt.Util.sendemail(self.get('notify'), subj, msg)

    def NotifyAtEnd(self):
        '''Notify user when job has ended'''
        subj = 'Cobalt: job %s finished' % self.get('jobid')
        msg = 'Job %s finished at %s\nStats: %s' %  (self.get('jobid'), time.strftime('%c', time.localtime()), self.GetStats())
        Cobalt.Util.sendemail(self.get('notify'), subj, msg)

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
                 'args':self.get('args'), 'envs':self.get('envs', {}), 'location':[self.get('location')]})
        except xmlrpclib.Fault, fault:
            raise ProcessManagerError
        except Cobalt.Proxy.CobaltComponentError:
            raise ProcessManagerError
        if not pgroup[0].has_key('pgid'):
            logger.error("Process Group creation failed for Job %s" % self.get('jobid'))
            self.set('state', 'pm-failure')
        else:
            self.pgid['user'] = pgroup[0]['pgid']
        self.SetPassive()

class JobSet(Cobalt.Data.DataSet):
    '''Set of currently queued jobs'''
    __object__ = BGJob

    def __init__(self):
        Cobalt.Data.DataSet.__init__(self)
        #self.__id__ = Cobalt.Data.IncrID()

class Queue(Cobalt.Data.Data, JobSet):
    '''queue object, subs JobSet and Data, which gives us:
       self is a Queue object (with restrictions and stuff)
       self.data is a list of BGJob objects'''

    def __init__(self, info, id=None):
        Cobalt.Data.Data.__init__(self, info)
        JobSet.__init__(self)

        # set defaults if not set already
        defaults = {'drain':False, 'users':['*'], 'maxtime':0}
        for d in defaults:
            if d not in self._attrib:
                self.set(d, defaults[d])

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
            except DataCreationError, missing:
                print "returning fault"
                raise xmlrpclib.Fault(8, str(missing))
            #return xmlrpclib.dumps(xmlrpclib.Fault(8, str(missing)))
            # uniqueness test goes here
            self.data.append(iobj)
            if callback:
                apply(callback, (iobj, ) + cargs)
            retval.append(iobj.to_rx(item))
        return retval

    def GetJobs(self, data, callback=None, cargs={}):
        '''Uses the Data.Get method to retrieve Jobs from Queues'''
        joblist = [Q.Get(data, callback, cargs) for Q in self.data]
        for j in joblist[1:]:
            joblist[0].extend(j)
        if joblist:
            return joblist[0]
        else:
            return []

    def DelJobs(self, data):
        for Q in self.data:
            Q.Del([data])
            
    def CanRun(self, _, job):
        '''Check that job meets criteria of the specified queue'''

        # restriction list
        rlist = [ [(job, self.data), (lambda j, queuelist: j.get('queue') in [q.get('qname') for q in queuelist]), 'Queue does not exist'],
                  [(job, self.data), (lambda wtime, maxtime: job.get('walltime') <= [q.get('maxtime') for q in self.data if q.get('qname') == job.get('queue')][0]), 'Walltime greater than queue maxtime'] ]

        for qfunc in rlist:
            result = apply(qfunc[1], qfunc[0])
            if result == False:
                return qfunc[2]
             
#         if not (lambda j, queuelist: j.get('queue') in [q.get('qname') for q in queuelist])(job, self.data):
#                #job.get('queue') not in [q.get('qname') for q in self.data]:
#             return 'queue \'' + job.get('queue') + '\' does not exist in queue_manager'

        # TODO: check job against restrictions
        """
        (lambda job, self.data: job.get('qname') in [q.get('qname') for q in self.data])
        (lambda jspec, rlist: jspec.get('user') in rlist.get('users'))(jobspec, {'users':['voran', 'vinnie']})
        (lambda x: x in people)(120)
        (lambda x, name, y: x[name] < y)(jobspec,'time', 9000)
        """

        return 'True'

class CQM(Cobalt.Component.Component):
    '''Cobalt Queue Manager'''
    __implementation__ = 'cqm'
    __name__ = 'queue-manager'
    __statefields__ = ['Queues']
    async_funcs = ['assert_location', 'progress', 'pm_sync']

    def __init__(self, setup):
        self.Queues = QueueSet()
        Cobalt.Component.Component.__init__(self, setup)
        self.drain = False

        self.prevdate = time.strftime("%m-%d-%y", time.localtime())
        self.comms = CommDict()
        self.register_function(lambda  address, data:self.Queues.GetJobs(data), "GetJobs")
        self.register_function(lambda  address, data:[Q for Q in self.Queues if Q.get('qname') == data.get('queue')][0].Add(data), "AddJob")
        self.register_function(self.handle_job_del, "DelJobs")
        self.register_function(lambda  address, data:self.Queues.Get(data), "GetQueues")
#         self.register_function(self.handle_get_queue, "GetQueues")
        self.register_function(lambda  address, data:self.Queues.Add(data), "AddQueue")
        self.register_function(lambda  address, data:self.Queues.Del(data), "DelQueues")
        self.register_function(lambda  address, data, updates:self.Queues.Get(data, lambda queue, newattr:queue.update(newattr), updates), "SetQueues")
        self.register_function(self.Queues.CanRun, "CanRun")
        self.register_function(self.drain_func, "Drain")
        self.register_function(self.resume_func, "Resume")
        self.register_function(lambda address, data, nodelist:
                               self.Queues.GetJobs(data, lambda job, nodes:job.Run(nodes), nodelist),
                               'RunJobs')
        self.register_function(lambda address, data, updates:
                               self.Queues.GetJobs(data, lambda job, newattr:job.update(newattr), updates),
                               'SetJobs')
        self.register_function(self.set_jobid, 'SetJobID')

    def set_jobid(self, _, jobid):
        '''Set next jobid for new job'''
        self.Queues.__id__.idnum = jobid-1
        return True

    def progress(self):
        '''Process asynchronous job work'''
        [j.Progress() for j in [j for queue in self.Queues for j in queue] if j.active]
        [j.Kill("Job %s Overtime, Killing") for j in [j for queue in self.Queues for j in queue] if j.over_time()]
        [j.LogFinish() for j in [j for queue in self.Queues for j in queue] if j.get('state') == 'done']
        [queue.remove(j) for (j,queue) in [(j,queue) for queue in self.Queues for j in queue] if j.get('state') == 'done']
        newdate = time.strftime("%m-%d-%y", time.localtime())
        [j.acctlog.ChangeLog() for j in [j for queue in self.Queues for j in queue] if newdate != self.prevdate]
        Job.acctlog.ChangeLog()
        return 1

    def drain_func(self, _):
        '''Stop accepting new jobs'''
        self.drain = True

    def resume_func(self, _):
        '''Resume accepting new jobs'''
        self.drain = False

    def addjob(self, address, spec):
        '''Add new job (respecting self.drain)'''
        if not self.drain:
            self.Jobs.Add(address, spec)
        else:
            return xmlrpclib.Fault(31, 'System Draining')

    def handle_get_queue(self, _, data):

        print data
        print self.Queues.__object__, self.Queues.data
        #print self.Queues.Get(data)
        return []

    def handle_job_del(self, _, data, force=False):
        '''Delete a job'''
        ret = []
        for spec in data:
            for job,q in [(job,queue) for queue in self.Queues for job in queue if job.match(spec)]:
                ret.append(job.to_rx(spec))
                if job.get('state') in ['queued', 'ready'] or force or (job.get('state') == 'hold' and not job.pgid):
                    #q.remove(job)
                    q.Del(spec)
                else:
                    job.Kill("Job %s killed based on user request")
        return ret

    def HandleEvent(self, event):
        '''Process incoming events'''
        (c, m, d) = tuple([event.get(field) for field in ['component', 'msg', 'data']])
        if c == 'node-stage-manager':
            # jobs gate on nsm up message for all nodes in job
            j = [j for j in self.Jobs if d in j.nodelist]
            if len(j) == 1:
                j[0].booted += 1                    
            else:
                pass
        elif c == 'build-system':
            # jobs gate on bs state change for action = boot set
            j = [j for j in self.Jobs if d in j.nodelist]
            if len(j) == 1:
                j[0].built += 1                    
            else:
                pass
        elif c == 'fslave':
            # d is the stageid
            jl = [j for j in self.Jobs if j.stageid == d]
            if len(jl) == 0:
                self.logger.info("Got unknown stage id %s" % (d))
            elif len(jl) == 1:
                if m == 'stage-setup':
                    self.logger.debug("Got stage completed for stageid %s, jobid %s" %
                                      (d, jl[0].attr['jobid']))
                    if jl[0].attr['state'] == 'stage-pending':
                        jl[0].SetActive()
                    #AddEvent("queue-manager", "job-ready", str(jl[0].attr['jobid']))
                    jl[0].staged = 1
                elif m == 'stage-failed':
                    jl[0].attr['state'] = 'stage-error'
                else:
                    self.logger.error("Unexpected fslave event")
            else:
                self.logger.error("Got multiple matches for stageid %s" % (d))
        elif c == 'process-manager':
            # Something has exited
            if m == 'process_end':
                jlist = [j for j in self.Jobs if j.HasPG(d)]
                self.logger.info("Got process_end for PGID %s" % (d))
                self.logger.info("Matched %s jobs for PGID %s: %s" % (len(jlist), d,
                                                                      [j.element.get('jobid') for j in jlist]))
                [j.CompletePG(d) for j in jlist]

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
        daemon = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        daemon = False
    level = 10
    if len([x for x in opts if x[0] == '-d']):
        level = 0
    Cobalt.Logging.setup_logging('cqm', level=20)
    server = CQM({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    server.serve_forever()
