# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
from datetime import datetime
from time import mktime
from logging.handlers import BaseRotatingHandler
import os
from Cobalt.Util import get_config_option

RESOURCE_NAME = get_config_option('system', 'resource_name', 'NOTSET')
RECORD_MAPPING = {'abort': 'A',
                  'begin': 'B',
                  'checkpoint': 'C',
                  'checkpoint_restart': 'T',
                  'delete': 'D',
                  'end': 'E',
                  'finish': 'F',
                  'system_remove': 'K',
                  'remove': 'k',
                  'queue': 'Q',
                  'rerun': 'R',
                  'start': 'S',
                  'unconfirmed': 'U',
                  'confirmed': 'Y',
                  'task_start': 'TS',
                  'task_end': 'TE',
                  'modify': 'QA',
                  'hold_acquire': 'HA',
                  'hold_release': 'HR',
                  'reservation_altered': 'YA',
                  }

__all__ = ["abort", "begin", "checkpoint", "delete", "end", "finish",
           "system_remove", "remove", "queue", "rerun", "start", "unconfirmed",
           "confirmed", "task_start", "task_end", "DatetimeFileHandler",
           "modify", 'hold_acquire', 'hold_release', 'reservation_altered']

def abort (job_id, user, resource_list, account=None, resource=RESOURCE_NAME):
    """Job was aborted by the server.
    Generally this is a job whose walltime has ended and Cobalt is initiating termination and cleanup.

    Arguments:
        job_id -- id of job that has been checkpointed
        user -- the user name under which the job has been submitted
        resource_list -- list of the specified resource limits
        account -- if submitter supplied a string for accounting
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """
    message = {'resource':resource, 'Resource_List':resource_list, 'user': user}
    if account is not None:
        message['account'] = account
    return entry("A", job_id, message)


def begin (id_string, users, queue, ctime, stime, start_time, end_time, duration, exec_host, authorized_users, resource_list, active_id,
           name=None, account=None, authorized_groups=None, authorized_hosts=None, resource=RESOURCE_NAME, requester="Scheduler"):
    """Beginning of reservation active period.

    Arguments:
        id_string -- reservation or reservation-job identifier
        requester -- requester for begin (always Scheduler)
        users -- list of users on the reservation.  If None, then any user may submit
        queue -- name of the associated queue
        ctime -- time at which the reservation was created
        stime -- time at which the reservation was started
        start_time -- time at which the reservation is to start
        end_time -- time at which the reservation is to end
        duration -- duration specified or computed for the reservation
        exec_host -- nodes and node-associated resources (see qrun -H)
        authorized_users -- list of acl_users on the reservation queue
        resource_list -- resources requested by the reservation
        active_id -- identifier for this active period of this reservation
        name -- if submitter supplied a name string for the reservation (Default: None)
        account -- if submitter supplied a string for accounting (default: None)
        authorized_groups -- the list of acl_groups in the reservation queue (default: None)
        authorized_hosts -- the list of acl_hosts on the reservation queue (default: None
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """


    message = {'users':users, 'queue':queue, 'ctime':ctime, 'stime':stime, 'etime':None, 'start':start_time, 'end':end_time,
            'duration':duration, 'exec_host':exec_host, 'authorized_users':authorized_users, 'Resource_List':resource_list,
            'active_id': active_id, 'resource':resource, 'requester': requester, 'name': name}
    if account is not None:
        message['account'] = account
    if authorized_groups is not None:
        message['authorized_groups'] = authorized_groups
    if authorized_hosts is not None:
        message['authorized_hosts'] = authorized_hosts
    return entry("B", id_string, message)


def checkpoint (job_id, resource=RESOURCE_NAME):
    """Job was checkpointed and held.

    Arguments:
        job_id -- id of job that has been checkpointed
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """
    return entry("C", job_id, {'resource':resource})


def delete (job_id, requester, user, resource_list, force=False, account=None, resource=RESOURCE_NAME):
    """Job was deleted by request.
    This may be from any authorized user on the job, the submitting user or an administrator.

    Arguments:
        job_id -- id of the deleted job
        requester -- identity of who deleted the job (user@host)
        user -- the user name under which the job has been submitted
        resource_list -- list of the specified resource limits
        force -- True if this delete request was a part of a force-delete by an administrator (default: False)
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """
    message = {'requester':requester, 'resource':resource, 'Resource_List':resource_list, 'user': user, 'force':force}
    if account is not None:
        message['account'] = account
    return entry("D", job_id, message)


def end (job_id, user, group, jobname, queue, cwd, exe, args, mode, ctime, qtime, etime, start, exec_host, resource_list, session,
         end, exit_status, resources_used, account=None, resvname=None, resv_id=None, alt_id=None, accounting_id=None,
         total_etime=None, priority_core_hours=None, resource=RESOURCE_NAME):

    """Job ended (terminated execution).
    This indicates that the job is no longer in the queue at all, and will not be restarted in case of preemption.

    Arguments:
        job_id -- identifier of the job that ended
        user -- the user name under which the job executed
        group -- the group name under which the job executed
        jobname -- the name of the job
        queue -- the name of the queue in which the job executed
        cwd -- the current working directory used by the job
        exe -- the executable run by the job
        args -- the arguments passsed to the executable
        mode -- the exection mode of the job
        ctime -- time when job was created
        qtime -- time when job was queued into current queue
        etime -- time in seconds when job became eligible to run
        start -- time when job execution started
        exec_host -- name of host on which the job is being executed
        resource_list -- list of the specified resource limits
        session -- session number of job
        end -- time when job ended execution
        exit_status -- exit status of the job
        resources_used -- aggregate amount (value) of resources used
        account -- if job has an "account name" string (default: None)
        accounting_id -- CSA JID, job ID (default: None)
        alt_id -- optional alternate job identifier (default: None)
        priority_core_hours -- core hours used. May be used for elevated priority accounting in the future. (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        resvname -- the name of the resource reservation, if applicable (default: None)
        resv_id -- the id of the resource reservation, if applicable (default: None)

    Returns
        A string accounting log message

    """

    message = {'user':user, 'group':group, 'jobname':jobname, 'queue':queue,
        'cwd':cwd, 'exe':exe, 'args':args, 'mode':mode,
        'ctime':ctime, 'qtime':qtime, 'etime':etime, 'start':start,
        'exec_host':exec_host, 'Resource_List':resource_list,
        'session':session, 'end':end, 'Exit_status':exit_status,
        'resources_used':resources_used, 'resource':resource}
    if account is not None:
        message['account'] = account
    if resvname is not None:
        message['resvname'] = resvname
    if resv_id is not None:
        message['resvID'] = resv_id
    if alt_id is not None:
        message['accounting_id'] = accounting_id
    if total_etime is not None:
        message['approx_total_etime'] = int(total_etime)

    if priority_core_hours is not None:
        message['priority_core_hours'] = int(priority_core_hours)
    else:
        message['priority_core_hours'] = 0

    return entry("E", job_id, message)


def finish(reservation_id, requester, ctime, stime, etime, start_time, end_time, name, queue, resource_list, active_id,
        duration, exec_host, authorized_users, account=None, resource=RESOURCE_NAME):
    """Resource reservation finished and removed from list.

    Arguments:
        reservation_id -- id of the reservation that was removed
        requester -- user@host to identify who deleted the resource reservation
        ctime -- creation time of reservation
        stime -- start time of reservation active period
        etime -- end time of reservation active period
        resource_list -- list of information on resources used.  Must be sufficient for charging for resources used.
        active_id -- identifier for which activation of the reservation this is.
        duration -- requested duration of the reservation
        exec_host -- name of host on which the reservation has been placed
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        start_time -- time at which the reservation is to start
        end_time -- time at which the reservation is to end
        queue -- name of the associated queue
        name -- if submitter supplied a name string for the reservation (Default: None)

    Returns:
        A string accounting log message

    """
    #Note: for charging purposes, this is closest to the 'E' record.  This
    #indicates the job data that should actually be charged.
    msg = {'requester':requester, 'ctime':ctime, 'stime': stime, 'etime': etime,
            'Resource_List':resource_list, 'active_id': active_id,
            'resource':resource, 'duration': duration, 'exec_host':exec_host,
            'authorized_users': authorized_users, 'users':authorized_users,
            'start': start_time, 'end': end_time, 'queue': queue, 'name': name}
    if account is not None:
        msg['account'] = account

    return entry("F", reservation_id, msg)


def system_remove (reservation_id, requester, ctime, stime, etime, start_time, end_time, name, queue, resource_list, active_id,
        duration, exec_host, authorized_users, account=None, resource=RESOURCE_NAME):
    """Scheduler or server requested removal of the reservation.  This marks an active to inactive transition.

    Arguments:
        reservation_id -- id of the reservation that was removed
        requester -- user@host to identify who deleted the resource reservation
        ctime -- creation time of reservation
        stime -- start time of reservation active period
        etime -- end time of reservation active period
        resource_list -- list of information on resources used.  Must be sufficient for charging for resources used.
        active_id -- identifier for which activation of the reservation this is.
        duration -- requested duration of the reservation
        exec_host -- name of host on which the reservation has been placed
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        start_time -- time at which the reservation is to start
        end_time -- time at which the reservation is to end
        queue -- name of the associated queue
        name -- if submitter supplied a name string for the reservation (Default: None)

    Returns:
        A string accounting log message

    """
    #Note: for charging purposes, this is closest to the 'E' record.  This
    #indicates the job data that should actually be charged.
    msg = {'requester':requester, 'ctime':ctime, 'stime':stime, 'etime': etime,
            'Resource_List':resource_list, 'active_id': active_id,
            'resource':resource, 'duration': duration, 'exec_host':exec_host,
            'authorized_users': authorized_users, 'users':authorized_users,
            'start': start_time, 'end': end_time, 'queue': queue, 'name': name}
    if account is not None:
        msg['account'] = account
    return entry("K", reservation_id, msg)

def remove (reservation_id, requester, ctime, stime, etime, start_time, end_time, name, queue, resource_list, active_id,
        duration, exec_host, authorized_users, account=None, resource=RESOURCE_NAME):
    """Resource reservation terminated by ordinary client.

    Arguments:
        reservation_id -- id of the reservation that was removed
        requester -- user@host to identify who deleted the resource reservation
        ctime -- creation time of reservation
        stime -- start time of reservation active period
        etime -- end time of reservation active period
        resource_list -- list of information on resources used.  Must be sufficient for charging for resources used.
        active_id -- identifier for which activation of the reservation this is.
        duration -- requested duration of the reservation
        exec_host -- name of host on which the reservation has been placed
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        start_time -- time at which the reservation is to start
        end_time -- time at which the reservation is to end
        queue -- name of the associated queue
        name -- if submitter supplied a name string for the reservation (Default: None)

    Returns:
        A string accounting log message

    """
    #Note: for charging purposes, this is closest to the 'E' record.  This
    #indicates the job data that should actually be charged.
    msg = {'requester':requester, 'ctime':ctime, 'stime':stime, 'etime':etime,
            'Resource_List':resource_list, 'active_id': active_id,
            'resource':resource, 'duration': duration, 'exec_host':exec_host,
            'authorized_users': authorized_users, 'users':authorized_users,
            'start': start_time, 'end': end_time, 'queue': queue, 'name': name}
    if account is not None:
        msg['account'] = account
    return entry("k", reservation_id, msg)

def queue (job_id, queue, user, resource_list, account=None, resource=RESOURCE_NAME):
    """Job entered a queue.

    Arguments:
        job_id -- id of the job that entered the queue
        queue -- the queue into which the job was placed
        user -- the user name under which the job will be executed
        resource_list -- a dictionary of specified resource limits
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """
    message = {'queue':queue, 'resource':resource, 'Resource_List':resource_list, 'user': user}
    if account is not None:
        message['account'] = account
    return entry("Q", job_id, message)

def modify (job_id, queue, user, resource_list, account=None, resource=RESOURCE_NAME):
    """Job was modified

    Arguments:
        job_id -- id of the job
        queue -- the queue into which the job was placed
        user -- the user name under which the job will be executed
        resource_list -- a dictionary of specified resource limits
        account -- submitter supplied a string for accounting (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message


    """
    message = {'queue':queue, 'resource':resource, 'Resource_List':resource_list, 'user': user}
    if account is not None:
        message['account'] = account
    return entry(RECORD_MAPPING['modify'], job_id, message)


def rerun (job_id):
    """Job was rerun.

    Arguments:
        job_id -- id of the job

    Returns:
        A string accounting log message

    """
    return entry("R", job_id)


def start (job_id, user, group, jobname, queue, cwd, exe, args, mode, ctime, qtime, etime, start, exec_host, resource_list, session,
           account=None, resvname=None, resv_id=None, alt_id=None, accounting_id=None, resource=RESOURCE_NAME):

    """Job started.
    At this point the queue manager has been instructed to start the job.  Preactions are taken, but control may not have been
    handed to the user yet.

    Arguments:
        job_id -- identifier of the job that started
        user -- the user name under which the job executed
        group -- the group name under which the job executed
        jobname -- the name of the job
        queue -- the name of the queue in which the job resides
        cwd -- the current working directory used by the job
        exe -- the executable run by the job
        args -- the arguments passsed to the executable
        mode -- the exection mode of the job
        ctime -- time when job was created
        qtime -- time when job was queued into current queue
        etime -- time in seconds when job became eligible to run
        start -- time when job execution started
        exec_host -- name of host on which the job is being executed
        resource_list -- list of the specified resource limits
        session -- session number of job
        account -- if job has an "account name" string (default: None)
        resvname -- the name of the resource reservation, if applicable (default: None)
        resv_id -- the id of the resource reservation, if applicable (default: None)
        alt_id -- optional alternate job identifier (default: None)
        accounting_id -- CSA JID, job ID (default: None)
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """

    message = {'user':user, 'group':group, 'jobname':jobname, 'queue':queue, 'cwd':cwd, 'exe':exe, 'args':args, 'mode':mode,
               'ctime':ctime, 'qtime':qtime, 'etime':etime, 'start':start, 'exec_host':exec_host, 'Resource_List':resource_list,
               'session':session, 'resource':resource}
    if account is not None:
        message['account'] = account
    if resvname is not None:
        message['resvname'] = resvname
    if resv_id is not None:
        message['resvID'] = resv_id
    if alt_id is not None:
        message['accounting_id'] = accounting_id
    return entry("S", job_id, message)

def unconfirmed (reservation_id, requester, active_id, resource=RESOURCE_NAME):
    """Created unconfirmed Cobalt reservation.

    Arguments:
        reservation_id -- id of the unconfirmed reservation
        requester -- user@host to identify who requested the resources reservation
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    """

    return entry("U", reservation_id, {'requester':requester, 'resource':resource, 'active_id':active_id})

def confirmed (reservation_id, requester, start_time, duration, resource_list,
        ctime, stime, etime, active_id, exec_host, queue, name, authorized_users,
        account=None, resource=RESOURCE_NAME):
    """Created confirmed Cobalt reservation.

    Arguments:
        reservation_id -- id of the confirmed reservation
        requester -- user@host to identify who requested the resources reservation
        start_time -- the time in seconds from Epoch (1970-01-01 00:00:00 UTC) that the reservation is to start.
        duration -- planned duration of reservation
        resource_list -- dictionary of resource information for charging for the planned resources of this reservation
        active_id -- identifier for this active period of this reservation
        exec_host -- name of host on which the reservation has been placed
        account -- string account identifier for this reservation.  None if not provided.
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        queue -- queue assigned to the reservation
        authorized_users -- list of users assigned to the reservation
        name -- name string of the reservation
        ctime -- creation time of reservation
        stime -- start time of reservation active period
        etime -- end time of reservation active period


    Returns:
        A string accounting log message

    """

    msg = {'requester':requester, 'start':int(start_time), 'duration':int(duration), 'end':int(start_time) + int(duration),
            'active_id':active_id, 'Resource_List':resource_list,
            'resource':resource, 'exec_host':exec_host,
            'authorized_users':authorized_users, 'users':authorized_users,
            'queue': queue, 'name': name, 'ctime':ctime, 'stime':stime, 'etime':etime}
    if account is not None:
        msg['account'] = account

    return entry("Y", reservation_id, msg)

def reservation_altered (reservation_id, requester, start_time, duration, resource_list,
        ctime, stime, etime, active_id, exec_host, queue, name, authorized_users,
        account=None, resource=RESOURCE_NAME):
    """Altered cobalt reservation.  Calling this "YA" to follow the same Q <-> QA relationship.

    Arguments:
        reservation_id -- id of the confirmed reservation
        requester -- user@host to identify who requested the resources reservation
        start_time -- the time in seconds from Epoch (1970-01-01 00:00:00 UTC) that the reservation is to start.
        duration -- planned duration of reservation
        resource_list -- dictionary of resource information for charging for the planned resources of this reservation
        active_id -- identifier for this active period of this reservation
        exec_host -- name of host on which the reservation has been placed
        account -- string account identifier for this reservation.  None if not provided.
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)
        queue -- queue assigned to the reservation
        authorized_users -- list of users assigned to the reservation
        name -- name string of the reservation
        ctime -- creation time of reservation
        stime -- start time of reservation active period
        etime -- end time of reservation active period

    """
    msg = {'requester':requester, 'start':int(start_time), 'duration':int(duration), 'end':int(start_time) + int(duration),
            'active_id':active_id, 'Resource_List':resource_list,
            'resource':resource, 'exec_host':exec_host,
            'authorized_users':authorized_users, 'users':authorized_users,
            'queue': queue, 'name': name, 'ctime':ctime, 'stime':stime, 'etime':etime}
    if account is not None:
        msg['account'] = account

    return entry("YA", reservation_id, msg)

def task_start(job_id, task_id, start_time, location, resource=RESOURCE_NAME):
    '''Indicate a task has started.  Typically this would indicate that add_process_groups has been called successfully.
    Control has been handed to the user

    Arguments:
        job_id -- id of job that this task belongs to
        task_id -- id of the task launched
        start_time -- time when the task started as seconds from epoch
        location -- a list of locations that this task is running on
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    '''
    return entry("TS", job_id, {'task_id': task_id, 'start': start_time, 'location': location, 'resource':resource})

def task_end(job_id, task_id, task_runtime, start_time, end_time, location, resource=RESOURCE_NAME):
    '''Indicate a task has ended.  Control has been handed back to Cobalt from the user.

    Arguments:
        job_id -- id of job that this task belongs to
        task_id -- id of the task launched
        task_runtime -- The running time of the task in seconds.  Start time for this is the task_start record timestamp.
        start_time -- time when the task started as seconds from epoch
        end_time -- tme when the task ended as seconds from epoch
        location -- a list of locations that this task is running on
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    '''
    return entry("TE", job_id, {'task_id': task_id, 'task_runtime': task_runtime, 'start': start_time, 'end': end_time,
                                'location': location, 'resource':resource})

def hold_acquire(job_id, hold_type, start_time, user, resource=RESOURCE_NAME):
    '''Indicate a hold has been acquired.
    Jobs cannot run until all holds have been released.

    Arguments:
        job_id -- id of job that this task belongs to
        hold_type -- the type of hold that has been placed on the job.
        start_time -- time when the task started as seconds from epoch
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    '''
    return entry("HA", job_id, {'hold_type': hold_type, 'start': start_time, 'resource': resource, 'user':user})

def hold_release(job_id, hold_type, end_time, user, resource=RESOURCE_NAME):
    '''Indicate a hold has been released.
    Jobs cannot run until all holds have been released.

    Arguments:
        job_id -- id of job that this task belongs to
        start_time -- time when the task started as seconds from epoch
        end_time -- tme when the task ended as seconds from epoch
        resource -- identifier of the resource that Cobalt is managing.  Usually the system name.
                    (default: as specified by the resource_name option in the [system] cobalt.conf section)

    Returns:
        A string accounting log message

    '''
    return entry("HR", job_id, {'hold_type': hold_type, 'end': end_time, 'resource': resource, 'user':user})



class DatetimeFileHandler (BaseRotatingHandler):

    """A log file handler that rotates logs based on the current date/time.

    This handler determines the intended file name by parsing a pattern
    with datetime.now().strftime(). To create a daily log file in /var/log:

        DatetimeFileHandler("/var/log/%Y-%m-%d")

    The log will be rotated any time the intended filename changes.

    Arguments:
    file_pattern -- the pattern to be passed to datetime.now().strftime()

    Keyword arguments:
    encoding -- see FileHandler
    """

    def __init__ (self, file_pattern, encoding=None):
        self.file_pattern = file_pattern
        BaseRotatingHandler.__init__(self, self.get_baseFilename(),
            "a", encoding)

    def get_baseFilename (self):
        return os.path.abspath(datetime.now().strftime(self.file_pattern))

    def doRollover (self):
        self.stream.close()
        self.baseFilename = self.get_baseFilename()
        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')

    def shouldRollover (self, record):
        return self.baseFilename != self.get_baseFilename()


def entry (record_type, id_string, message=None):

    """Generate an entry in a PBS accounting log.

    Arguments:
    record_type -- a single character indicating the type of record
    id_string -- the job, reservation, or reservation-job identifier
    message -- dictionary containing appropriate message data
    """

    if message is None:
        message = {}
    return entry_ (datetime.now(), record_type, id_string, message)


def entry_ (datetime_, record_type, id_string, message):

    """Generate an entry in a PBS accounting log.

    Arguments:
    datetime_ -- a date and time stamp
    record_type -- a single character indicating the type of record
    id_string -- the job, reservation, or reservation-job identifier
    message -- dictionary containing appropriate message data
    """

    assert record_type in RECORD_MAPPING.values(), "invalid record_type %r" % record_type
    datetime_s = datetime_.strftime("%m/%d/%Y %H:%M:%S")
    message_text = serialize_message(message)
    return "%s;%s;%s;%s" % (datetime_s, record_type, id_string, message_text)


def serialize_message (message):
    message = message.copy()
    for keyword, value in message.items():
        try:
            items = value.items()
        except AttributeError:
            pass
        else:
            del message[keyword]
            for keyword_, value_ in items:
                message['%s.%s' % (keyword, keyword_)] = value_
    for keyword, value in message.items():
        if isinstance(value, basestring):
            if ' ' in value or '"' in value or "," in value:
                message[keyword] = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
        else:
            for f in (serialize_list, serialize_dt, serialize_td):
                try:
                    message[keyword] = f(message[keyword])
                except ValueError:
                    continue
                else:
                    break
    return " ".join("%s=%s" % (keyword, value)
        for (keyword, value) in sorted(message.items()))


def serialize_list (list_):
    try:
        values = []
        for value in list_:
            if ' ' in value or '"' in value or "," in value:
                value = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
            values.append(value)
        return ",".join(str(i) for i in values)
    except TypeError, ex:
        raise ValueError(ex)


def serialize_dt (datetime_):
    try:
        return (mktime(datetime_.timetuple()) +
            (1.0 * datetime_.microsecond / 1000000))
    except AttributeError, ex:
        raise ValueError(ex)


def serialize_td (timedelta_):
    try:
        return ((1.0 * timedelta_.days * 24 * 60 * 60) + timedelta_.seconds
            + (timedelta_.microseconds / 1000000))
    except AttributeError, ex:
        raise ValueError(ex)


