#!/usr/bin/env python

'''Super-Simple Scheduler for BG/L'''
__revision__ = '$Revision$'

import logging
import os.path
import sys
import time
import ConfigParser
import threading
import xmlrpclib

import Cobalt.Logging, Cobalt.Util
from Cobalt.Data import Data, DataDict, ForeignData, ForeignDataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ReservationError, DataCreationError, ComponentLookupError
from Cobalt.Statistics import Statistics

import Cobalt.SchedulerPolicies

logger = logging.getLogger("Cobalt.Components.scheduler")
config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('bgsched'):
    print '''"bgsched" section missing from cobalt config file'''
    sys.exit(1)

SLOP_TIME = 180
DEFAULT_RESERVATION_POLICY = "default"

bgsched_id_gen = None
bgsched_cycle_id_gen = None

def get_bgsched_config(option, default):
    try:
        value = config.get('bgsched', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

def get_histm_config(option, default):
    try:
        value = config.get('histm', option)
    except ConfigParser.NoSectionError:
        value = default
    return value
running_job_walltime_prediction = get_histm_config("running_job_walltime_prediction", "False").lower()     #*AdjEst*
if running_job_walltime_prediction  == "true":
    running_job_walltime_prediction = True
else:
    running_job_walltime_prediction = False

#db writer initialization
dbwriter = Cobalt.Logging.dbwriter(logger)
use_db_logging = get_bgsched_config('use_db_logging', 'false')
if use_db_logging.lower() in ['true', '1', 'yes', 'on']:
   dbwriter.enabled = True
   overflow_filename = get_bgsched_config('overflow_file', None)
   max_queued = int(get_bgsched_config('max_queued_msgs', '-1'))
   if max_queued <= 0:
       max_queued = None
   if (overflow_filename == None) and (max_queued != None):
       logger.warning('No filename set for database logging messages, max_queued_msgs set to unlimited')
   if max_queued != None:
       dbwriter.overflow_filename = overflow_filename
       dbwriter.max_queued = max_queued

   #dbwriter.connect()


class Reservation (Data):
    
    """Cobalt scheduler reservation."""
    
    fields = Data.fields + [
        "tag", "name", "start", "duration", "cycle", "users", "partitions",
        "active", "queue", "res_id", "cycle_id" 
    ]
    
    required = ["name", "start", "duration"]

    global bgsched_id_gen
    global bgsched_cycle_id_gen

    def __init__ (self, spec):
        Data.__init__(self, spec)
        self.tag = spec.get("tag", "reservation")
        self.cycle = spec.get("cycle")
        self.users = spec.get("users", "")
        self.createdQueue = False
        self.partitions = spec.get("partitions", "")
        self.name = spec['name']
        self.start = spec['start']
        self.queue = spec.get("queue", "R.%s" % self.name)
        self.duration = spec.get("duration")
        self.res_id = spec.get("res_id")
        self.cycle_id_gen = bgsched_cycle_id_gen
        if self.cycle:
            self.cycle_id = spec.get("cycle_id",self.cycle_id_gen.get())
        else:
            self.cycle_id = None

        self.running = False
        
        self.id_gen = bgsched_id_gen
        

    def _get_active(self):
        return self.is_active()
    
    active = property(_get_active)
    
    def update (self, spec):
        #print "cycle check: %s, id: %s" % (self.cycle, self.cycle_id)
        if spec.has_key("users"):
            qm = ComponentProxy("queue-manager")
            try:
                qm.set_queues([{'name':self.queue,}], {'users':spec['users']}, "bgsched")
            except ComponentLookupError:
                logger.error("unable to contact queue manager when updating reservation users")
                raise
        # try the above first -- if we can't contact the queue-manager, don't update the users
        if spec.has_key('cycle') and not self.cycle:
            #we have just turned this into a cyclic reservation and need a cycle_id.
            spec['cycle_id'] = self.cycle_id_gen.get()
        Data.update(self, spec)
        #print "cycle check: %s, id: %s" % (self.cycle, self.cycle_id)

    
    def overlaps(self, start, duration):
        '''check job overlap with reservations'''
        if start + duration < self.start:
            return False

        if self.cycle and duration >= self.cycle:
            return True

        my_stop = self.start + self.duration
        if self.start <= start < my_stop:
            # Job starts within reservation 
            return True
        elif self.start <= (start + duration) < my_stop:
            # Job ends within reservation 
            return True
        elif start < self.start and (start + duration) >= my_stop:
            # Job starts before and ends after reservation
            return True
        if not self.cycle:
            return False
        
        # 3 cases, front, back and complete coverage of a cycle
        cstart = (start - self.start) % self.cycle
        cend = (start + duration - self.start) % self.cycle
        if cstart < self.duration:
            return True
        if cend < self.duration:
            return True
        if cstart > cend:
            return True
        
        return False

    def job_within_reservation(self, job):
        if not self.is_active():
            return False
        
        if job.queue == self.queue:
            job_end = time.time() + 60 * float(job.walltime) + SLOP_TIME
            if not self.cycle:
                res_end = self.start + self.duration
                if job_end < res_end:
                    return True
                else:
                    return False
            else:
                if 60 * float(job.walltime) + SLOP_TIME > self.duration:
                    return False
                
                relative_start = (time.time() - self.start) % self.cycle
                relative_end = relative_start + 60 * float(job.walltime) + SLOP_TIME
                if relative_end < self.duration:
                    return True
                else:
                    return False
        else:
            return False

    
    def is_active(self, stime=False):
        if not stime:
            stime = time.time()
            
        if stime < self.start:
            return False
        
        if self.cycle:
            now = (stime - self.start) % self.cycle
        else:
            now = stime - self.start    
        if now <= self.duration:
            if not self.running:
                self.running = True
                logger.info("Res %s/%s: Activating reservation: %r" % 
                             (self.res_id,
                              self.cycle_id)) 
                dbwriter.log_to_db(None, "activating", "reservation", self)
            return True

    def is_over(self):
        
        stime = time.time()
        # reservations with a cycle time are never "over"
        if self.cycle:
            #but it does need a new res_id, cycle_id remains constant.
            if((((stime - self.start) % self.cycle) > self.duration) 
               and self.running):
                self.running = False
                self.res_id = self.id_gen.get()
                logger.info("Res %s/%s: Cycling reservation: %r" % 
                             (self.res_id,
                              self.cycle_id)) 
                dbwriter.log_to_db(None, "cycling", "reservation", self)
            return False        
        
        if (self.start + self.duration) <= stime:
            self.running = False
            return True
        else:
            return False
        
        

class ReservationDict (DataDict):
    
    item_cls = Reservation
    key = "name"
    
    
    def q_add (self, *args, **kwargs):
        qm = ComponentProxy("queue-manager")
        try:
            queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        except ComponentLookupError:
            logger.error("unable to contact queue manager when adding reservation")
            raise
        
        try:
            specs = args[0]
            for spec in specs:
                if "res_id" not in spec or spec['res_id'] == '*':
                    spec['res_id'] = bgsched_id_gen.get()
            reservations = Cobalt.Data.DataDict.q_add(self, *args, **kwargs)

        except KeyError, e:
            raise ReservationError("Error: a reservation named %s already exists" % e)
                
        for reservation in reservations:
            if reservation.queue not in queues:
                try:
                    qm.add_queues([{'tag': "queue", 'name':reservation.queue, 'policy':DEFAULT_RESERVATION_POLICY}], "bgsched")
                except Exception, e:
                    logger.error("unable to add reservation queue %s (%s)" % \
                                 (reservation.queue, e))
                else:
                    reservation.createdQueue = True
                    logger.info("added reservation queue %s" % (reservation.queue))
            try:
                # we can't set the users list using add_queues, so we want to call set_queues even if bgsched
                # just created the queue
                qm.set_queues([{'name':reservation.queue}],
                              {'state':"running", 'users':reservation.users}, "bgsched")
            except Exception, e:
                logger.error("unable to update reservation queue %s (%s)" % \
                             (reservation.queue, e))
            else:
                logger.info("updated reservation queue %s" % reservation.queue)
    
        return reservations
        
    def q_del (self, *args, **kwargs):
        reservations = Cobalt.Data.DataDict.q_del(self, *args, **kwargs)
        qm = ComponentProxy('queue-manager')
        queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        spec = [{'name': reservation.queue} for reservation in reservations \
                if reservation.createdQueue and reservation.queue in queues and \
                not self.q_get([{'queue':reservation.queue}])]
        try:
            qm.set_queues(spec, {'state':"dead"}, "bgsched")
        except Exception, e:
            logger.error("problem disabling reservation queue (%s)" % e)
        return reservations


                

class Job (ForeignData):
    
    """A cobalt job."""
    
    fields = ForeignData.fields + [
        "nodes", "location", "jobid", "state", "index", "walltime", "queue", "user", "submittime", 
        "starttime", "project", 'is_runnable', 'is_active', 'has_resources', "score", 'attrs', 'walltime_p'
    ]
    
    def __init__ (self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        print spec
        self.partition = "none"
        self.nodes = spec.pop("nodes", None)
        self.location = spec.pop("location", None)
        self.jobid = spec.pop("jobid", None)
        self.state = spec.pop("state", None)
        self.index = spec.pop("index", None)
        self.walltime = spec.pop("walltime", None)
        self.walltime_p = spec.pop("walltime_p", None)   #*AdjEst*
        self.queue = spec.pop("queue", None)
        self.user = spec.pop("user", None)
        self.submittime = spec.pop("submittime", None)
        self.starttime = spec.pop("starttime", None)
        self.project = spec.pop("project", None)
        self.is_runnable = spec.pop("is_runnable", None)
        self.is_active = spec.pop("is_active", None)
        self.has_resources = spec.pop("has_resources", None)
        self.score = spec.pop("score", 0.0)
        self.attrs = spec.pop("attrs", {})
        
        logger.info("Job %s/%s: Found job" % (self.jobid, self.user))

class JobDict(ForeignDataDict):
    item_cls = Job
    key = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (job)")
    __function__ = ComponentProxy("queue-manager").get_jobs
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user', 'submittime', 'starttime', 'project',
                  'is_runnable', 'is_active', 'has_resources', 'score', 'attrs', 'walltime_p',]

class Queue(ForeignData):
    fields = ForeignData.fields + [
        "name", "state", "policy", "priority"
    ]

    def __init__(self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
        self.name = spec.pop("name", None)
        self.state = spec.pop("state", None)
        self.policy = spec.pop("policy", None)
        self.priority = spec.pop("priority", 0)
        
        

    def LoadPolicy(self):
        '''Instantiate queue policy modules upon demand'''
        if self.policy not in Cobalt.SchedulerPolicies.names:
            logger.error("Cannot load policy %s for queue %s" % \
                         (self.policy, self.name))
        else:
            pclass = Cobalt.SchedulerPolicies.names[self.policy]
            self.policy = pclass(self.name)


class QueueDict(ForeignDataDict):
    item_cls = Queue
    key = 'name'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (queue)")
    __function__ = ComponentProxy("queue-manager").get_queues
    __fields__ = ['name', 'state', 'policy', 'priority']

#    def Sync(self):
#        qp = [(q.name, q.policy) for q in self.itervalues()]
#        Cobalt.Data.ForeignDataDict.Sync(self)
#        [q.LoadPolicy() for q in self.itervalues() \
#         if (q.name, q.policy) not in qp]


class BGSched (Component):
    
    implementation = "bgsched"
    name = "scheduler"
    logger = logging.getLogger("Cobalt.Components.scheduler")


    _configfields = ['utility_file']
    _config = ConfigParser.ConfigParser()
    print Cobalt.CONFIG_FILES
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgsched'):
        print '''"bgsched" section missing from cobalt config file'''
        sys.exit(1)
    config = _config._sections['bgsched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file [bgsched] section: %s" % (" ".join(mfields))
        sys.exit(1)
    if config.get("default_reservation_policy"):
        global DEFAULT_RESERVATION_POLICY
        DEFAULT_RESERVATION_POLICY = config.get("default_reservation_policy")
    
    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.reservations = ReservationDict()
        self.queues = QueueDict()
        self.jobs = JobDict()
        self.started_jobs = {}
        self.sync_state = Cobalt.Util.FailureMode("Foreign Data Sync")
        self.active = True
    
        self.get_current_time = time.time
        self.id_gen = IncrID()
        global bgsched_id_gen
        bgsched_id_gen = self.id_gen
        
        self.cycle_id_gen = IncrID()
        global bgsched_cycle_id_gen
        bgsched_cycle_id_gen = self.cycle_id_gen
        
        

    def __getstate__(self):
        return {'reservations':self.reservations, 'version':1,
                'active':self.active, 'next_res_id':self.id_gen.idnum+1, 
                'next_cycle_id':self.cycle_id_gen.idnum+1, 
                'msg_queue': dbwriter.msg_queue, 
                'overflow': dbwriter.overflow}
    
    def __setstate__(self, state):
        self.reservations = state['reservations']
        if 'active' in state:
            self.active = state['active']
        else:
            self.active = True
        
        self.id_gen = IncrID()
        self.id_gen.set(state['next_res_id'])
        global bgsched_id_gen
        bgsched_id_gen = self.id_gen
        
        self.cycle_id_gen = IncrID()
        self.cycle_id_gen.set(state['next_cycle_id'])
        global bgsched_cycle_id_gen
        bgsched_cycle_id_gen = self.cycle_id_gen

        self.queues = QueueDict()
        self.jobs = JobDict()
        self.started_jobs = {}
        self.sync_state = Cobalt.Util.FailureMode("Foreign Data Sync")
        
        self.get_current_time = time.time
        self.lock = threading.Lock()
        self.statistics = Statistics()

        if state.has_key('msg_queue'):
            dbwriter.msg_queue = state['msg_queue']
        if state.has_key('overflow') and (dbwriter.max_queued != None):
            dbwriter.overflow = state['overflow']

    # order the jobs with biggest utility first
    def utilitycmp(self, job1, job2):
        return -cmp(job1.score, job2.score)
    
    def prioritycmp(self, job1, job2):
        """Compare 2 jobs first using queue priority and then first-in, first-out."""
        
        val = cmp(self.queues[job1.queue].priority, self.queues[job2.queue].priority)
        if val == 0:
            return self.fifocmp(job1, job2)
        else:
            # we want the higher priority first
            return -val
        
    def fifocmp (self, job1, job2):
        """Compare 2 jobs for first-in, first-out."""
        
        def fifo_value (job):
            if job.index is not None:
                return int(job.index)
            else:
                return job.jobid
            
        # Implement some simple variations on FIFO scheduling
        # within a particular queue, based on queue policy
        fifoval = cmp(fifo_value(job1), fifo_value(job2))
        if(job1.queue == job2.queue):
            qpolicy = self.queues[job1.queue].policy
            sizeval = cmp(int(job1.nodes), int(job2.nodes))
            wtimeval = cmp(int(job1.walltime), int(job2.walltime))
            if(qpolicy == 'largest-first' and sizeval):
                return -sizeval
            elif(qpolicy == 'smallest-first' and sizeval):
                return sizeval
            elif(qpolicy == 'longest-first' and wtimeval):
                return -wtimeval
            elif(qpolicy == 'shortest-first' and wtimeval):
                return wtimeval
            else:
                return fifoval
        else:
            return fifoval

        return cmp(fifo_value(job1), fifo_value(job2))

    def save_me(self):
        Component.save(self)
    save_me = automatic(save_me)

    #user_name in this context is the user setting/modifying the res.
    def add_reservations (self, specs, user_name):
        self.logger.info("%s adding reservation: %r" % (user_name, specs))
        added_reservations =  self.reservations.q_add(specs)
        for added_reservation in added_reservations:
            self.logger.info("Res %s/%s: %s adding reservation: %r" % 
                             (added_reservation.res_id,
                              added_reservation.cycle_id,
                              user_name, specs))
            dbwriter.log_to_db(user_name, "creating", "reservation", added_reservation)
        return added_reservations
    
    add_reservations = exposed(query(add_reservations))

    def del_reservations (self, specs, user_name):
        self.logger.info("%s releasing reservation: %r" % (user_name, specs))
        del_reservations = self.reservations.q_del(specs)
        for del_reservation in del_reservations:
            self.logger.info("Res %s/%s/: %s releasing reservation: %r" % 
                             (del_reservation.res_id,
                              del_reservation.cycle_id,
                              user_name, specs))
            dbwriter.log_to_db(user_name, "ending", "reservation", del_reservation) 
        return del_reservations

    del_reservations = exposed(query(del_reservations))

    def get_reservations (self, specs):
        return self.reservations.q_get(specs)
    get_reservations = exposed(query(get_reservations))

    def set_reservations(self, specs, updates, user_name):
        log_str = "%s modifying reservation: %r with updates %r" % (user_name, specs, updates)
        self.logger.info(log_str)
        def _set_reservations(res, newattr):
            res.update(newattr)
        mod_reservations = self.reservations.q_get(specs, _set_reservations, updates)
        for mod_reservation in mod_reservations:
            self.logger.info("Res %s/%s: %s modifying reservation: %r" % 
                             (mod_reservation.res_id,
                              mod_reservation.cycle_id,
                              user_name, specs))
            dbwriter.log_to_db(user_name, "modifying", "reservation", mod_reservation)
        return mod_reservations
        
    set_reservations = exposed(query(set_reservations))

    def check_reservations(self):
        ret = ""
        reservations = self.reservations.values()
        for i in range(len(reservations)):
            for j in range(i+1, len(reservations)):
                # if at least one reservation is cyclic, we want *that* reservation to be the one getting its overlaps method
                # called
                if reservations[i].cycle is not None:
                    res1 = reservations[i]
                    res2 = reservations[j]
                else:
                    res1 = reservations[j]
                    res2 = reservations[i]

                # we subtract a little bit because the overlaps method isn't really meant to do this
                # it will report warnings when one reservation starts at the same time another ends
                if res1.overlaps(res2.start, res2.duration - 0.00001):
                    # now we need to check for overlap in space
                    results = ComponentProxy("system").get_partitions(
                        [ {'name': p, 'children': '*', 'parents': '*'} for p in res2.partitions.split(":") ]
                    )
                    for p in res1.partitions.split(":"):
                        for r in results:
                            if p==r['name'] or p in r['children'] or p in r['parents']:
                                ret += "Warning: reservation '%s' overlaps reservation '%s'\n" % (res1.name, res2.name)

        return ret
    check_reservations = exposed(check_reservations)

    def sync_data(self):
        started = self.get_current_time()
        for item in [self.jobs, self.queues]:
            try:
                item.Sync()
            except (ComponentLookupError, xmlrpclib.Fault):
                # the ForeignDataDicts already include FailureMode stuff
                pass
        # print "took %f seconds for sync_data" % (time.time() - started, )
    #sync_data = automatic(sync_data)

    def _run_reservation_jobs (self, reservations_cache):
        # handle each reservation separately, as they shouldn't be competing for resources
        for cur_res in reservations_cache.itervalues():
            queue = cur_res.queue
            if not (self.queues.has_key(queue) and self.queues[queue].state == 'running'):
                continue
            
            temp_jobs = self.jobs.q_get([{'is_runnable':True, 'queue':queue}])
            active_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid) and cur_res.job_within_reservation(j):
                    active_jobs.append(j)
    
            if not active_jobs:
                continue
            active_jobs.sort(self.utilitycmp)
            
            job_location_args = []
            for job in active_jobs:
                job_location_args.append( 
                    { 'jobid': str(job.jobid), 
                      'nodes': job.nodes, 
                      'queue': job.queue, 
                      'required': cur_res.partitions.split(":"),
                      'utility_score': job.score,
                      'walltime': job.walltime,
                      'attrs': job.attrs,
                    } )

            # there's no backfilling in reservations
            try:
                best_partition_dict = ComponentProxy("system").find_job_location(job_location_args, [])
            except:
                self.logger.error("failed to connect to system component")
                best_partition_dict = {}
    
            for jobid in best_partition_dict:
                job = self.jobs[int(jobid)]
                self._start_job(job, best_partition_dict[jobid])

    def _start_job(self, job, partition_list):
        cqm = ComponentProxy("queue-manager")
        
        try:
            self.logger.info("trying to start job %d on partition %r" % (job.jobid, partition_list))
            cqm.run_jobs([{'tag':"job", 'jobid':job.jobid}], partition_list)
        except ComponentLookupError:
            self.logger.error("failed to connect to queue manager")
            return

        self.started_jobs[job.jobid] = self.get_current_time()



    def schedule_jobs (self):
        '''look at the queued jobs, and decide which ones to start'''

        started_scheduling = self.get_current_time()

        if not self.active:
            return
        
        self.sync_data()
        
        # if we're missing information, don't bother trying to schedule jobs
        if not (self.queues.__oserror__.status and self.jobs.__oserror__.status):
            self.sync_state.Fail()
            return
        self.sync_state.Pass()
        
        self.lock.acquire()
        try:
            # cleanup any reservations which have expired
            for res in self.reservations.values():
                if res.is_over():
                    self.logger.info("reservation %s has ended; removing" % res.name)
                    self.logger.info("Res %s/%s: Ending reservation: %r" % 
                             (res.res_id,
                              res.cycle_id,
                              res.name))

                    del_reservations = self.reservations.q_del([{'name': res.name}])
                    for del_reservation in del_reservations:
                        dbwriter.log_to_db(None, "ending", "reservation", del_reservation) 
    
            reservations_cache = self.reservations.copy()
        except:
            # just to make sure we don't keep the lock forever
            self.logger.error("error in schedule_jobs", exc_info=True)
        self.lock.release()
        
        # clean up the started_jobs cached data
        now = self.get_current_time()
        for job_name in self.started_jobs.keys():
            if (now - self.started_jobs[job_name]) > 60:
                del self.started_jobs[job_name]

        active_queues = []
        spruce_queues = []
        res_queues = set()
        for item in reservations_cache.q_get([{'queue':'*'}]):
            if self.queues.has_key(item.queue):
                if self.queues[item.queue].state == 'running':
                    res_queues.add(item.queue)

        for queue in self.queues.itervalues():
            if queue.name not in res_queues and queue.state == 'running':
                if queue.policy == "high_prio":
                    spruce_queues.append(queue)
                else:
                    active_queues.append(queue)
        
        # handle the reservation jobs that might be ready to go
        self._run_reservation_jobs(reservations_cache)

        # figure out stuff about queue equivalence classes
        res_info = {}
        for cur_res in reservations_cache.values():
            res_info[cur_res.name] = cur_res.partitions
        try:
            equiv = ComponentProxy("system").find_queue_equivalence_classes(res_info, [q.name for q in active_queues + spruce_queues])
        except:
            self.logger.error("failed to connect to system component")
            return
        
        for eq_class in equiv:
            # recall that is_runnable is True for certain types of holds
            temp_jobs = self.jobs.q_get([{'is_runnable':True, 'queue':queue.name} for queue in active_queues \
                if queue.name in eq_class['queues']])
            active_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid):
                    active_jobs.append(j)
    
            temp_jobs = self.jobs.q_get([{'is_runnable':True, 'queue':queue.name} for queue in spruce_queues \
                if queue.name in eq_class['queues']])
            spruce_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid):
                    spruce_jobs.append(j)
    
            # if there are any pending jobs in high_prio queues, those are the only ones that can start
            if spruce_jobs:
                active_jobs = spruce_jobs

            # get the cutoff time for backfilling
            #
            # BRT: should we use 'has_resources' or 'is_active'?  has_resources returns to false once the resource epilogue
            # scripts have finished running while is_active only returns to false once the job (not just the running task) has
            # completely terminated.  the difference is likely to be slight unless the job epilogue scripts are heavy weight.
            temp_jobs = [job for job in self.jobs.q_get([{'has_resources':True}]) if job.queue in eq_class['queues']]
            end_times = []
            for job in temp_jobs:
                # take the max so that jobs which have gone overtime and are being killed
                # continue to cast a small backfilling shadow (we need this for the case
                # that the final job in a drained partition runs overtime -- which otherwise
                # allows things to be backfilled into the drained partition)
                            
                ##*AdjEst*
                if running_job_walltime_prediction:
                    runtime_estimate = float(job.walltime_p)
                else:
                    runtime_estimate = float(job.walltime)
                
                end_time = max(float(job.starttime) + 60 * runtime_estimate, now + 5*60)
                end_times.append([job.location, end_time])
            
            for res_name in eq_class['reservations']:
                cur_res = reservations_cache[res_name]

                if not cur_res.cycle:
                    end_time = float(cur_res.start) + float(cur_res.duration)
                else:
                    done_after = float(cur_res.duration) - ((now - float(cur_res.start)) % float(cur_res.cycle))
                    if done_after < 0:
                        done_after += cur_res.cycle
                    end_time = now + done_after
                if cur_res.is_active():
                    for part_name in cur_res.partitions.split(":"):
                        end_times.append([[part_name], end_time])
    
            
            if not active_jobs:
                continue
            active_jobs.sort(self.utilitycmp)
            
            # now smoosh lots of data together to be passed to the allocator in the system component
            job_location_args = []
            for job in active_jobs:
                forbidden_locations = set()
                for res_name in eq_class['reservations']:
                    cur_res = reservations_cache[res_name]
                    if cur_res.overlaps(self.get_current_time(), 60 * float(job.walltime) + SLOP_TIME):
                        forbidden_locations.update(cur_res.partitions.split(":"))

                job_location_args.append( 
                    { 'jobid': str(job.jobid), 
                      'nodes': job.nodes, 
                      'queue': job.queue, 
                      'forbidden': list(forbidden_locations),
                      'utility_score': job.score,
                      'walltime': job.walltime,
                      'walltime_p': job.walltime_p, #*AdjEst*
                      'attrs': job.attrs,
                    } )

            try:
                best_partition_dict = ComponentProxy("system").find_job_location(job_location_args, end_times)
            except:
                self.logger.error("failed to connect to system component", exc_info=True)
                best_partition_dict = {}
    
            for jobid in best_partition_dict:
                job = self.jobs[int(jobid)]
                self._start_job(job, best_partition_dict[jobid])
    

        # print "took %f seconds for scheduling loop" % (time.time() - started_scheduling, )
    schedule_jobs = locking(automatic(schedule_jobs))

    
    def enable(self, user_name):
        """Enable scheduling"""
        self.logger.info("%s enabling scheduling", user_name)
        self.active = True
    enable = exposed(enable)

    def disable(self, user_name):
        """Disable scheduling"""
        self.logger.info("%s disabling scheduling", user_name)
        self.active = False
    disable = exposed(disable)

    def set_res_id(self, id_num):
        """Set the reservation id number."""
        self.id_gen.set(id_num)
        logger.info("Reset res_id generator to %s." % id_num)

    set_res_id = exposed(set_res_id)
    
    def set_cycle_id(self, id_num):
        """Set the cycle id number."""
        self.cycle_id_gen.set(id_num)
        logger.info("Reset cycle_id generator to %s." % id_num)

    set_cycle_id = exposed(set_cycle_id)

    def force_res_id(self, id_num):
        self.id_gen.idnum = id_num - 1
        logger.warning("Forced res_id generator to %s." % id_num)

    force_res_id = exposed(force_res_id)

    def force_cycle_id(self, id_num):
        self.cycle_id_gen.idnum = id_num - 1
        logger.warning("Forced cycle_id generator to %s." % id_num)

    force_cycle_id = exposed(force_cycle_id)

    def get_next_res_id(self):
        return self.id_gen.idnum + 1
    get_next_res_id = exposed(get_next_res_id)

    def get_next_cycle_id(self):
        return self.cycle_id_gen.idnum + 1
    get_next_cycle_id = exposed(get_next_cycle_id)

    def __flush_msg_queue(self):
        dbwriter.flush_queue()
    __flush_msg_queue = automatic(__flush_msg_queue, float(get_bgsched_config('db_flush_interval', 10)))
