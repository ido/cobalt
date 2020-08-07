#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
'''Super-Simple Scheduler for BG/L'''

import logging
import sys
import time
import ConfigParser
import xmlrpclib
import math
import os
import traceback
import itertools

import Cobalt.Logging
import Cobalt.Util
from Cobalt.Util import expand_num_list
from Cobalt.Data import Data, DataDict, ForeignData, ForeignDataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ReservationError, ComponentLookupError
import Cobalt.accounting as accounting
import Cobalt.SchedulerPolicies

__revision__ = '$Revision: 2156 $'

logger = logging.getLogger("Cobalt.Components.scheduler")
config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('bgsched'):
    logger.critical('''"bgsched" section missing from cobalt config file''')
    sys.exit(1)

SLOP_TIME = 180
DEFAULT_RESERVATION_POLICY = "default"

bgsched_id_gen = None
bgsched_cycle_id_gen = None

DEFAULT_ACCOUNTING_LOG_PREFIX = 'reservation'
_accounting_logger = logging.getLogger("bgsched.accounting")

def _init_accounting_log():
    '''Initialize PBS-style accounting log for this module'''
    reservation_filename = "%s-%%Y%%m%%d" % get_bgsched_config("accounting_log_prefix", DEFAULT_ACCOUNTING_LOG_PREFIX)
    accounting_logdir = os.path.expandvars(get_bgsched_config("log_dir", Cobalt.DEFAULT_LOG_DIRECTORY))
    _accounting_logger.addHandler(accounting.DatetimeFileHandler(os.path.join(accounting_logdir, reservation_filename)))

def _write_to_accounting_log(msg):
    '''Send to PBS-style accounting log for this module to accounting log and syslog'''
    logger.info(msg)
    _accounting_logger.info(msg)

def get_bgsched_config(option, default):
    '''fetch configuration variables for bgsched

    '''
    #Note: should be replaced by get config functions from Cobalt.util
    try:
        value = config.get('bgsched', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

def get_histm_config(option, default):
    '''fetch configuration variables for history manager (part of walltime prediction)

    '''
    #Note: should be replaced by get config functions from Cobalt.util
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

class Reservation (Data):
#pylint: disable=R0902
    '''Cobalt scheduler reservation.

    '''
    #Notes:
    #ctime -- the time of the creation of the active res_id.  On a cyclic reservation,
    #         this will be updated when cycling is complete.

    fields = Data.fields + [
        "tag", "name", "start", "duration", "cycle", "users", "partitions",
        "active", "queue", "res_id", "cycle_id", 'project', "block_passthrough",
        "resource_list", "active_id", "ctime", "stime",
    ]
    required = ["name", "start", "duration"]

    def __init__ (self, spec):
        '''initialize a reservation according to a spec dictionary'''
        Data.__init__(self, spec)
        self.name = spec['name']
        self.start = spec['start']
        self.duration = spec['duration']
        self.tag = spec.get("tag", "reservation")
        self.cycle = spec.get("cycle")
        self.users = spec.get("users", "")
        self.created_queue = False
        self.partitions = spec.get("partitions", "")
        self.queue = spec.get("queue", "R.%s" % self.name)
        self.res_id = spec.get("res_id")
        self.cycle_id_gen = bgsched_cycle_id_gen
        if self.cycle:
            self.cycle_id = spec.get("cycle_id", self.cycle_id_gen.get())
        else:
            self.cycle_id = None
        self.active_id_gen = IncrID()
        self.active_id_gen.idnum = int(spec.get("active_id", 1)) - 1
        self.active_id = self.active_id_gen.get()

        self.running = False
        self.project = spec.get("project", None)
        self.block_passthrough = spec.get("block_passthrough", False)
        self.ctime = spec.get("ctime", int(time.time()))
        self.stime = spec.get('stime', None)
        self.resource_list = spec['resource_list']
        self.deleting = False

    def _get_active(self):
        return self.is_active()

    active = property(_get_active)

    def update (self, spec):
        '''Update reservations with changes based on a dictionary.  This
        dictionary is generated from received XMLRPC. This provides provides
        reservation-specific validation for data prior to insertion into the
        actual data entry for the reservation.

        '''
        if spec.has_key("users"):
            qm = ComponentProxy("queue-manager")
            try:
                qm.set_queues([{'name':self.queue,}], {'users':spec['users']}, "bgsched")
            except ComponentLookupError:
                logger.error("unable to contact queue manager when updating reservation users")
                raise
        # try the above first -- if we can't contact the queue-manager,
        # don't update the users
        if spec.has_key('cycle') and not self.cycle:
            #just turned this into a cyclic reservation and need a cycle_id
            spec['cycle_id'] = self.cycle_id_gen.get()
        #get the user name of whoever issued the command
        user_name = None
        if spec.has_key('__cmd_user'):
            user_name = spec['__cmd_user']
            del spec['__cmd_user']

        #if we're defering, pull out the 'defer' entry and send a cobalt db
        #message.  There really isn't a corresponding field to update
        deferred = False
        if spec.has_key('defer'):
            logger.info("Res %s/%s: Deferring cyclic reservation: %s", self.res_id, self.cycle_id, self.name)
            dbwriter.log_to_db(user_name, "deferred", "reservation", self)
            del spec['defer']
            deferred = True

        if spec.has_key('partitions'):
            self.resource_list = ComponentProxy("system").get_location_statistics(spec['partitions'])

        if self.running:
            #if we are modifying a reservation's start time for an actively running reservation, then
            #we need to emit a specific set of records so an accounting system can sanely determine holds.
            #The reservation will have to "system remove (stop), modify, and then begin"  the active id will
            #be incremented for the new begin.  Our normal mechanisms don't catch this in the is_active check
            #since the reservation will never actually go inactive.
            logger.warning("Res %s/%s/%s: WARNING: modification of a currently active reservation.",
                    self.res_id, self.cycle_id, self.name)
            if (spec.has_key('start') and
                int(spec['start']) > int(self.start) and
                int(spec['start']) < (int(self.start) + int(self.duration))):
                logger.warning("Res %s/%s/%s: WARNING: start time changed during reservation to time within duration.",
                        self.res_id, self.cycle_id, self.name)
            # the etime (when this really ended) is now.
            _write_to_accounting_log(accounting.system_remove(self.res_id, "Scheduler", self.ctime, self.stime,
                int(time.time()), int(self.start), int(self.start) + int(self.duration), self.name, self.queue,
                self.resource_list, self.active_id, self.duration, self.partitions, self.users, self.project))
            #have to increment here, since we will not actually trigger from going inactive.
            self.active_id = self.active_id_gen.get()
            Data.update(self, spec)
            _write_to_accounting_log(accounting.reservation_altered(self.res_id, user_name, self.start, self.duration,
               self.resource_list, self.ctime, self.stime, None, self.active_id, self.partitions, self.queue, self.name,
               self.users,  self.project))
            _write_to_accounting_log(accounting.begin(self.res_id, self.users, self.queue, self.ctime, self.stime,
                int(self.start), int(self.start) + int(self.duration), int(self.duration),
                self.partitions, self.users, self.resource_list, self.active_id, name=self.name, account=self.project,
                authorized_groups=None, authorized_hosts=None))
        else:
            Data.update(self, spec)
            _write_to_accounting_log(accounting.reservation_altered(self.res_id, user_name, self.start, self.duration,
               self.resource_list, self.ctime, self.stime, None, self.active_id, self.partitions, self.queue, self.name,
               self.users,  self.project))
        if not deferred or not self.running:
            #we only want this if we aren't deferring.  If we are, the cycle will
            #take care of the new data object creation.
            dbwriter.log_to_db(user_name, "modifying", "reservation", self)


    def overlaps(self, start, duration):
        '''check job overlap with reservations'''
        #TODO: see if this can be simplified a bit --PMR
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
        '''Return true if the job fits within this reservation, otherwise,
        return false.

        '''
        if not self.is_active():
            return False

        if job.queue == self.queue:

            res_end  = self.start + self.duration
            cur_time = time.time()

            # if the job is non zero then just use the walltime as is else give the max reservation time possible
            _walltime = float(job.walltime)

            _walltime = _walltime if _walltime > 0 else (res_end - cur_time - 300)/60
            logger.info('Walltime: %s', str(_walltime))

            job_end = cur_time + 60 * _walltime + SLOP_TIME
            if not self.cycle:
                if job_end < res_end:
                    job.walltime = _walltime
                    return True
                else:
                    return False
            else:
                if 60 * _walltime + SLOP_TIME > self.duration:
                    return False

                relative_start = (cur_time - self.start) % self.cycle
                relative_end = relative_start + 60 * _walltime + SLOP_TIME
                if relative_end < self.duration:
                    job.walltime = _walltime
                    return True
                else:
                    return False
        else:
            return False

    def __cycle_reservation(self, deferral_while_active=False):
        '''Take actions to generate a new res_id, and log that a reservation
        has cycled

        '''
        # Write finish while we have the original id.
        _write_to_accounting_log(accounting.finish(self.res_id, "Scheduler", self.ctime, self.stime, None,
            int(self.start), int(self.start) + int(self.duration), self.name, self.queue, self.resource_list,
            self.active_id, self.duration, self.partitions, self.users, self.project))
        self.res_id = bgsched_id_gen.get()
        self.ctime = int(time.time())
        self.active_id_gen = IncrID()
        self.active_id = self.active_id_gen.get()
        logger.info("Res %s/%s: Cycling reservation: %s", self.res_id,
                self.cycle_id, self.name)
        self.stime = None
        if not deferral_while_active:
            #if we are deferring while active, don't increment the time.  That's already happened.
            self.set_start_to_next_cycle()
        self.running = False
        _write_to_accounting_log(accounting.confirmed(self.res_id,
            "Scheduler", self.start, self.duration,
            self.resource_list,self.ctime, self.stime, None, self.active_id,
            self.partitions, self.queue, self.name, self.users, self.project))
        dbwriter.log_to_db(None, "cycling", "reservation", self)


    def is_active(self, stime=False):
        '''Determine if the reservation is active.  A reservation is active
        if we are between it's start time and its start time + duration.

        '''

        if not stime:
            stime = time.time()

        if stime < self.start:
            etime = int(time.time())
            if self.running:
                self.running = False
                if self.cycle:
                    #handle a deferral of a cyclic reservation while active, should not increment normally
                    #Time's already tweaked at this point.
                    logger.info("Res %s/%s: Active reservation %s deactivating: Deferred and cycling.",
                        self.res_id, self.cycle_id, self.name)
                    _write_to_accounting_log(accounting.system_remove(self.res_id, "Scheduler", self.ctime, self.stime,
                        etime, int(self.start), int(self.start) + int(self.duration), self.name, self.queue,
                        self.resource_list, self.active_id, self.duration, self.partitions, self.users, self.project))
                    dbwriter.log_to_db(None, "deactivating", "reservation", self, etime)
                    dbwriter.log_to_db(None, "instance_end", "reservation", self)
                    self.__cycle_reservation(True)
                else:
                    logger.info("Res %s/%s: Active reservation %s deactivating: start time in future.",
                        self.res_id, self.cycle_id, self.name)
                    _write_to_accounting_log(accounting.system_remove(self.res_id, "Scheduler", self.ctime, self.stime,
                        etime, int(self.start), int(self.start) + int(self.duration), self.name, self.queue,
                        self.resource_list, self.active_id, self.duration, self.partitions, self.users, self.project))
                    dbwriter.log_to_db(None, "deactivating", "reservation", self, etime)
                    self.active_id = self.active_id_gen.get()
            return False

        if self.cycle:
            now = (stime - self.start) % self.cycle
        else:
            now = stime - self.start

        if now <= self.duration:
            if not self.running:
                self.running = True
                self.stime = int(time.time())
                logger.info("Res %s/%s: Activating reservation: %s", self.res_id, self.cycle_id, self.name)
                user = None
                if self.users is not None:
                    user = self.users
                _write_to_accounting_log(accounting.begin(self.res_id, user, self.queue, self.ctime, self.stime,
                    int(self.start), int(self.start) + int(self.duration), int(self.duration),
                    self.partitions, self.users, self.resource_list, self.active_id, name=self.name, account=self.project,
                    authorized_groups=None, authorized_hosts=None))
                dbwriter.log_to_db(None, "activating", "reservation", self)
            return True
        else:
            return False
    active = property(is_active)

    def is_over(self):
        '''Determine if a reservation is over and initiate cleanup.

        '''
        stime = time.time()
        etime = int(time.time())
        # reservations with a cycle time are never "over"
        if self.cycle:
            #but it does need a new res_id, cycle_id remains constant.
            if((((stime - self.start) % self.cycle) > self.duration)
               and self.running):
                #do this before incrementing id.
                logger.info("Res %s/%s: Deactivating reservation: %s: Reservation Cycling",
                    self.res_id, self.cycle_id, self.name)
                _write_to_accounting_log(accounting.system_remove(self.res_id, "Scheduler", self.ctime, self.stime,
                    etime, int(self.start), int(self.start) + int(self.duration), self.name, self.queue,
                    self.resource_list, self.active_id, self.duration, self.partitions, self.users, self.project))
                dbwriter.log_to_db(None, "deactivating", "reservation", self, etime)
                dbwriter.log_to_db(None, "instance_end", "reservation", self, etime)
                self.__cycle_reservation()
            return False

        if (self.start + self.duration) <= stime:
            if self.running == True:
                #The active reservation is no longer considered active
                #do this only once to prevent a potential double-deactivate
                #depending on how/when this check is called.
                logger.info("Res %s/%s: Deactivating reservation: %s",
                             self.res_id, self.cycle_id, self.name)
                _write_to_accounting_log(accounting.system_remove(self.res_id, "Scheduler", self.ctime, self.stime,
                    etime, int(self.start), int(self.start) + int(self.duration), self.name, self.queue,
                    self.resource_list, self.active_id, self.duration, self.partitions, self.users, self.project))
                dbwriter.log_to_db(None, "deactivating", "reservation", self, etime)
            self.running = False
            return True
        else:
            return False

    def set_start_to_next_cycle(self):
        '''Set the time of the reservation, when it would next go active,
        to the next start time based on it's cycle time.  The new time is the
        current reservation start time + the cycle time interval.

        '''
        if self.cycle:
            new_start = self.start
            now = time.time()
            periods = int(math.floor((now - self.start) / float(self.cycle)))
            #so here, we should always be coming out of a reservation.  The
            #only time we wouldn't be is if for some reason the scheduler was
            #disrupted.
            if now < self.start:
                new_start += self.cycle
            else:
                #this is not going to start during a reservation, so we only
                #have to go periods + 1.
                new_start += (periods + 1) * self.cycle
            self.start = new_start


class ReservationDict (DataDict):
    '''DataDict-style dictionary for reservation data.
    Ensures that there is a queue in the queue manager associated with a new
    reservation, by either associating with an extant queue, or creating a new
    one for this reservation's use.

    Will also kill a created queue on reservation deactivation and cleanup,
    though the queue will remain if it still has jobs in it.  These jobs will
    not run, but may be moved to other queues/subject to another reservation.

    '''
    item_cls = Reservation
    key = "name"


    def q_add (self, *args, **kwargs):
        '''Add a reservation to tracking.
        Side Effects:
            -Add a queue to be tracked
            -If no cqm associated queue, create a reservation queue
            -set policies for new queue
            -emit numerous creation messages

        '''

        qm = ComponentProxy("queue-manager")
        try:
            queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        except ComponentLookupError:
            logger.error("unable to contact queue manager when adding reservation")
            raise

        try:
            specs = args[0]
            for spec in specs:
                logger.debug("SPECS %s", spec)
                spec['resource_list'] = ComponentProxy("system").get_location_statistics(spec['partitions'])
                if "res_id" not in spec or spec['res_id'] == '*':
                    spec['res_id'] = bgsched_id_gen.get()
            reservations = Cobalt.Data.DataDict.q_add(self, *args, **kwargs)

        except KeyError, err:
            raise ReservationError("Error: a reservation named %s already exists" % err)

        for reservation in reservations:
            if reservation.queue not in queues:
                try:
                    qm.add_queues([{'tag': "queue", 'name':reservation.queue,
                        'policy':DEFAULT_RESERVATION_POLICY}], "bgsched")
                except Exception, err:
                    logger.error("unable to add reservation queue %s (%s)",
                                 reservation.queue, err)
                else:
                    reservation.created_queue = True
                    logger.info("added reservation queue %s", reservation.queue)
            try:
                # we can't set the users list using add_queues, so we want to
                # call set_queues even if bgsched just created the queue
                qm.set_queues([{'name':reservation.queue}],
                              {'state':"running", 'users':reservation.users}, "bgsched")
            except Exception, err:
                logger.error("unable to update reservation queue %s (%s)",
                             reservation.queue, err)
            else:
                logger.info("updated reservation queue %s", reservation.queue)

        return reservations

    def q_del (self, *args, **kwargs):
        '''Delete a reservation from tracking.
        Side Effects: Removes a queue from tracking.
                      Logs that the reservation has terminated.
                      Emits a terminated database record
                      Attempts to mark the queue dead in the queue-manager.
                      Marks the reservation as dying

        '''
        etime = int(time.time())
        reservations = Cobalt.Data.DataDict.q_del(self, *args, **kwargs)
        qm = ComponentProxy('queue-manager')
        queues = [spec['name'] for spec in qm.get_queues([{'name':"*"}])]
        spec = [{'name': reservation.queue} for reservation in reservations \
                if reservation.created_queue and reservation.queue in queues \
                and not self.q_get([{'queue':reservation.queue}])]
        try:
            qm.set_queues(spec, {'state':"dead"}, "bgsched")
        except Exception, err:
            logger.error("problem disabling reservation queue (%s)" % err)

        for reservation in reservations:
            reservation.deleting = True #Do not let the is_active check succeed.
            #This should be the last place we have handles to reservations,
            #after this they're heading to GC.
            # This seems redundant, but there is a race condition where is_over
            # may not have been invoked yet, but the reservation is no longer
            # active.  In this case, if is over would be true, but hadn't bene
            # invoked yet, is_active would be false and we would miss this.  So,
            # this should coerce the right behavior.
            if (not reservation.is_over()) and reservation.running:
                #if we are active, then drop a deactivating message.
                _write_to_accounting_log(accounting.system_remove(reservation.res_id, "Scheduler", reservation.ctime, reservation.stime,
                    etime, int(reservation.start), int(reservation.start) + int(reservation.duration), reservation.name, reservation.queue,
                    reservation.resource_list, reservation.active_id, reservation.duration, reservation.partitions, reservation.users, reservation.project))
                dbwriter.log_to_db(None, "deactivating", "reservation",
                        reservation)
                if reservation.cycle:
                    dbwriter.log_to_db(None, "instance_end", "reservation", reservation)
            _write_to_accounting_log(accounting.finish(reservation.res_id, "Scheduler", reservation.ctime, reservation.stime, None,
                int(reservation.start), int(reservation.start) + int(reservation.duration), reservation.name, reservation.queue, reservation.resource_list,
                reservation.active_id, reservation.duration, reservation.partitions, reservation.users, reservation.project))
            dbwriter.log_to_db(None, "terminated", "reservation", reservation)
        return reservations


class Job (ForeignData):
    """A field for the job metadata cache from cqm.  Used for finding a job
    location.

    """

    fields = ForeignData.fields + [
        "nodes", "location", "jobid", "state", "index", "walltime", "queue",
        "user", "submittime", "starttime", "project", 'is_runnable',
        'is_active', 'has_resources', "score", 'attrs', 'walltime_p',
        'geometry'
    ]

    def __init__ (self, spec):
        ForeignData.__init__(self, spec)
        spec = spec.copy()
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
        self.geometry = spec.pop("geometry", None)

        logger.info("Job %s/%s: Found job" % (self.jobid, self.user))

class JobDict(ForeignDataDict):
    """Dictionary of job metadata from cqm for job location purposes.

    """
    item_cls = Job
    key = 'jobid'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (job)")
    __function__ = ComponentProxy("queue-manager").get_jobs
    __fields__ = ['nodes', 'location', 'jobid', 'state', 'index',
                  'walltime', 'queue', 'user', 'submittime', 'starttime',
                  'project', 'is_runnable', 'is_active', 'has_resources',
                  'score', 'attrs', 'walltime_p','geometry']

class Queue(ForeignData):
    """Cache of queue data for scheduling decisions and reservation
    association.

    """
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
    """Dictionary for the queue metadata cache.

    """
    item_cls = Queue
    key = 'name'
    __oserror__ = Cobalt.Util.FailureMode("QM Connection (queue)")
    __function__ = ComponentProxy("queue-manager").get_queues
    __fields__ = ['name', 'state', 'policy', 'priority']

class BGSched (Component):
    """The scheduler component interface and driver functions.

    """
    #TODO: fix usage of global, probably not needed.
    implementation = "bgsched"
    name = "scheduler"
    logger = logging.getLogger("Cobalt.Components.scheduler")


    _configfields = ['utility_file']
    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgsched'):
        logger.critical('''"bgsched" section missing from cobalt config file''')
        sys.exit(1)
    config = _config._sections['bgsched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        logger.critical("Missing option(s) in cobalt config file [bgsched] section: %s",
                (" ".join(mfields)))
        sys.exit(1)
    if config.get("default_reservation_policy"):
        global DEFAULT_RESERVATION_POLICY
        DEFAULT_RESERVATION_POLICY = config.get("default_reservation_policy")

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        _init_accounting_log()
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
        state = {}
        state.update(Component.__getstate__(self))
        state.update({
                'sched_version':1,
                'reservations':self.reservations,
                'active':self.active,
                'next_res_id':self.id_gen.idnum + 1,
                'next_cycle_id':self.cycle_id_gen.idnum + 1,
                'msg_queue': dbwriter.msg_queue,
                'overflow': dbwriter.overflow})
        return state

    def __setstate__(self, state):
        Component.__setstate__(self, state)
        _init_accounting_log()

        self.reservations = state['reservations']
        if 'active' in state.keys():
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
        '''Automatic method for saving off the component statefile

        '''
        Component.save(self)
    save_me = automatic(save_me,
            float(get_bgsched_config('save_me_interval', 10)))

    #user_name in this context is the user setting/modifying the res.
    def add_reservations (self, specs, user_name):
        '''Exposed method for adding a reservation via setres.

        '''
        self.logger.info("%s adding reservation: %r", user_name, specs)
        for spec in specs:
            spec['resource_list'] = ComponentProxy("system").get_location_statistics(spec['partitions'])
        added_reservations =  self.reservations.q_add(specs)
        for added_reservation in added_reservations:
            self.logger.info("Res %s/%s: %s adding reservation: %r", added_reservation.res_id, added_reservation.cycle_id,
                user_name, specs)
            _write_to_accounting_log(accounting.confirmed(added_reservation.res_id,
                user_name, added_reservation.start, added_reservation.duration,
                added_reservation.resource_list,added_reservation.ctime, added_reservation.stime, None, added_reservation.active_id,
                added_reservation.partitions, added_reservation.queue, added_reservation.name, added_reservation.users, added_reservation.project))
            dbwriter.log_to_db(user_name, "creating", "reservation", added_reservation)
        return added_reservations

    add_reservations = exposed(query(add_reservations))

    def del_reservations (self, specs, user_name):
        '''Exposed method for terminating a reservation from releaseres.

        '''
        self.logger.info("%s releasing reservation: %r", user_name, specs)
        del_reservations = self.reservations.q_del(specs)
        for del_reservation in del_reservations:
            _write_to_accounting_log(accounting.remove(del_reservation.res_id, user_name, del_reservation.ctime,
                del_reservation.stime, None, int(del_reservation.start), int(del_reservation.start) + int(del_reservation.duration),
                del_reservation.name, del_reservation.queue, del_reservation.resource_list, del_reservation.active_id,
                del_reservation.duration, del_reservation.partitions, del_reservation.users, del_reservation.project))
            self.logger.info("Res %s/%s/: %s releasing reservation: %r", del_reservation.res_id,
                              del_reservation.cycle_id, user_name, specs)
            #database logging moved to the ReservationDict q_del method
            #the expected message is "terminated"
        return del_reservations

    del_reservations = exposed(query(del_reservations))

    def get_reservations (self, specs):
        '''Exposed method to get reservaton information.

        '''
        return self.reservations.q_get(specs)
    get_reservations = exposed(query(get_reservations))

    def set_reservations(self, specs, updates, user_name):
        '''Exposed method for resetting reservation information from setres.
        Must target an extant reservation.

        '''
        log_str = "%s modifying reservation: %r with updates %r" % (user_name, specs, updates)
        self.logger.info(log_str)
        # handle defers as a special case:  have to log these,
        # they are frequent enough we don't want a full a mod record
        def _set_reservations(res, newattr):
            '''callback to apply update to all modified reservations'''
            # Modification records are written from the update.  There are potentially a number of records
            # that can be written in the event of active reservation modification
            res.update(newattr)
        updates['__cmd_user'] = user_name
        mod_reservations = self.reservations.q_get(specs, _set_reservations, updates)
        for mod_reservation in mod_reservations:
            self.logger.info("Res %s/%s: %s modifying reservation: %r", mod_reservation.res_id, mod_reservation.cycle_id,
                    user_name, specs)
        return mod_reservations

    set_reservations = exposed(query(set_reservations))


    def release_reservations(self, specs, user_name):
        '''Exposed method used by releaseres for user-release of reserved resources.

        '''
        self.logger.info("%s requested release of reservation: %r", user_name, specs)
        self.logger.info("%s releasing reservation: %r", user_name, specs)
        rel_res = self.get_reservations(specs)
        for res in rel_res:
            _write_to_accounting_log(accounting.remove(res.res_id, user_name, res.ctime,
                res.stime, None, int(res.start), int(res.start) + int(res.duration),
                res.name, res.queue, res.resource_list, res.active_id,
                res.duration, res.partitions, res.users, res.project))
            dbwriter.log_to_db(user_name, "released", "reservation", res)
        del_reservations = self.reservations.q_del(specs)
        for del_reservation in del_reservations:
            self.logger.info("Res %s/%s/: %s releasing reservation: %r", del_reservation.res_id,
                              del_reservation.cycle_id, user_name, specs)
        return del_reservations

    release_reservations = exposed(query(release_reservations))

    def check_reservations(self):
        '''Validation for reservation resources.  Complain if reservations
        overlap, since dueling reservation behavior is undefined.

        '''
        implementation =  ComponentProxy("system").get_implementation()
        ret = ""
        reservations = self.reservations.values()
        for i in range(len(reservations)):
            for j in range(i+1, len(reservations)):
                # if at least one reservation is cyclic, we want *that*
                # reservation to be the one getting its overlaps method called
                if reservations[i].cycle is not None:
                    res1 = reservations[i]
                    res2 = reservations[j]
                else:
                    res1 = reservations[j]
                    res2 = reservations[i]

                # we subtract a little bit because the overlaps method isn't
                # really meant to do this it will report warnings when one
                # reservation starts at the same time another ends
                if res1.overlaps(res2.start, res2.duration - 0.00001):
                    # now we need to check for overlap in space
                    if implementation in ['alps_system']:
                        # no parent or children overlaps can happen in this mode.
                        # This test is now entirely local
                        res1_locs = set(itertools.chain.from_iterable(
                            [expand_num_list(hunk) for hunk in res1.partitions.split(':')]))
                        res2_locs = set(itertools.chain.from_iterable(
                            [expand_num_list(hunk) for hunk in res2.partitions.split(':')]))
                        intersect = res1_locs & res2_locs
                        if len(intersect) != 0:
                            ret += "Warning: reservation '%s' overlaps reservation '%s'\n" % (res1.name, res2.name)

                    else:
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
        #FIXME: Get some logging in here so we know what job is being picked.
        # handle each reservation separately, as they shouldn't be competing for resources
        for cur_res in reservations_cache.itervalues():
            #print "trying to run res jobs in", cur_res.name, self.started_jobs
            queue = cur_res.queue
            #FIXME: this should probably check reservation active rather than just queue
            # running.
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
            #FIXME: make sure job_location_args is ordered.
            for job in active_jobs:
                job_location_args.append(
                    { 'jobid': str(job.jobid),
                      'nodes': job.nodes,
                      'queue': job.queue,
                      'required': cur_res.partitions.split(":"),
                      'utility_score': job.score,
                      'walltime': job.walltime,
                      'attrs': job.attrs,
                      'user': job.user,
                      'geometry':job.geometry
                    } )

            # there's no backfilling in reservations. Run whatever we get in
            # best_partition_dict.  There is no draining, backfill windows are
            # meaningless within reservations.
            try:
                best_partition_dict = ComponentProxy("system").find_job_location(job_location_args, [])
            except:
                self.logger.error("failed to connect to system component")
                best_partition_dict = {}

            for jobid in best_partition_dict:
                job = self.jobs[int(jobid)]
                self.logger.info("Starting job %d/%s in reservation %s",
                        job.jobid, job.user, cur_res.name)
                self._start_job(job, best_partition_dict[jobid], {str(job.jobid):cur_res.res_id})

    def _start_job(self, job, partition_list, resid=None):
        """Get the queue manager to start a job."""

        cqm = ComponentProxy("queue-manager")

        try:
            self.logger.info("trying to start job %d on partition %r" % (job.jobid, partition_list))
            cqm.run_jobs([{'tag':"job", 'jobid':job.jobid}], partition_list, None, resid, job.walltime)
        except ComponentLookupError:
            self.logger.error("failed to connect to queue manager")
            return

        self.started_jobs[job.jobid] = self.get_current_time()



    def schedule_jobs (self):
        '''look at the queued jobs, and decide which ones to start
        This entire method completes prior to the job's timer starting
        in cqm.

        '''

        if not self.active:
            return

        self.sync_data()

        # if we're missing information, don't bother trying to schedule jobs
        if not (self.queues.__oserror__.status and
                self.jobs.__oserror__.status):
            self.sync_state.Fail()
            return
        self.sync_state.Pass()

        self.component_lock_acquire()
        try:
            # cleanup any reservations which have expired
            for res in self.reservations.values():
                if res.is_over():
                    self.logger.info("reservation %s has ended; removing" %
                            (res.name))
                    self.logger.info("Res %s/%s: Ending reservation: %r" %
                             (res.res_id, res.cycle_id, res.name))
                    #dbwriter.log_to_db(None, "ending", "reservation",
                    #        res)
                    del_reservations = self.reservations.q_del([
                        {'name': res.name}])

            # FIXME: this isn't a deepcopy.  it copies references to each reservation in the reservations dict.  is that really
            # sufficient?  --brt
            reservations_cache = self.reservations.copy()
        except:
            # just to make sure we don't keep the lock forever
            self.logger.error("error in schedule_jobs", exc_info=True)
        self.component_lock_release()

        # clean up the started_jobs cached data
        # TODO: Make this tunable.
        # started_jobs are jobs that bgsched has prompted cqm to start
        # but may not have had job.run has been completed.
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
        pt_blocking_res = []
        for cur_res in reservations_cache.values():
            res_info[cur_res.name] = cur_res.partitions
            if cur_res.block_passthrough:
                pt_blocking_res.append(cur_res.name)

        try:
            equiv = ComponentProxy("system").find_queue_equivalence_classes(
                    res_info, [q.name for q in active_queues + spruce_queues],
                    pt_blocking_res)
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
                pt_blocking_locations = set()

                for res_name in eq_class['reservations']:
                    cur_res = reservations_cache[res_name]
                    if cur_res.overlaps(self.get_current_time(), 60 * float(job.walltime) + SLOP_TIME):
                        forbidden_locations.update(cur_res.partitions.split(':'))
                        if cur_res.block_passthrough:
                            pt_blocking_locations.update(cur_res.partitions.split(':'))
                job_info = { 'jobid': str(job.jobid),
                             'nodes': job.nodes,
                             'queue': job.queue,
                             'forbidden': list(forbidden_locations),
                             'pt_forbidden': list(pt_blocking_locations),
                             'utility_score': job.score,
                             'walltime': job.walltime,
                             'walltime_p': job.walltime_p, #*AdjEst*
                             'attrs': job.attrs,
                             'user': job.user,
                             'geometry':job.geometry,
                           }
                for eq_class in equiv:
                    if job.queue in eq_class['queues']:
                        job_info['queue_equivalence'] = eq_class['queues']
                        break
                job_location_args.append(job_info)

            try:
                best_partition_dict = ComponentProxy("system").find_job_location(job_location_args, end_times)
            except:
                self.logger.error("failed to connect to system component")
                self.logger.debug("%s", traceback.format_exc())
                best_partition_dict = {}

            for jobid in best_partition_dict:
                job = self.jobs[int(jobid)]
                self._start_job(job, best_partition_dict[jobid])


    schedule_jobs = locking(automatic(schedule_jobs,
        float(get_bgsched_config('schedule_jobs_interval', 10))))

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

    def sched_status(self):
        return self.active
    sched_status = exposed(sched_status)

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
        """Override the id-generator and change the resid to id_num"""
        self.id_gen.idnum = id_num - 1
        logger.warning("Forced res_id generator to %s." % id_num)

    force_res_id = exposed(force_res_id)

    def force_cycle_id(self, id_num):
        """Override the id-generator and change the cycleid to id_num"""
        self.cycle_id_gen.idnum = id_num - 1
        logger.warning("Forced cycle_id generator to %s." % id_num)

    force_cycle_id = exposed(force_cycle_id)

    def get_next_res_id(self):
        """Get what the next resid number would be"""
        return self.id_gen.idnum + 1
    get_next_res_id = exposed(get_next_res_id)

    def get_next_cycle_id(self):
        """get what the next cycleid number would be"""
        return self.cycle_id_gen.idnum + 1
    get_next_cycle_id = exposed(get_next_cycle_id)

    def __flush_msg_queue(self):
        """Send queued messages to the database-writer component"""
        return dbwriter.flush_queue()
    __flush_msg_queue = automatic(__flush_msg_queue,
                float(get_bgsched_config('db_flush_interval', 10)))
