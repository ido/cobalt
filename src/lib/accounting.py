"""PBS-style accounting logs."""

import logging
from datetime import datetime

logger = logging.getLogger("accounting")

def job_abort (job):
    return log("A", job.jobid)

def job_checkpoint (job):
    return log("C", job.jobid)

def job_delete (job, requester):
    return log("D", job.jobid, {'requester':requester})

def job_end (job):
    return log("D", job.jobid)

def job_queue (job): pass
def job_rerun (job): pass
def job_start (job): pass
def reservation_begin (reservation): pass
def reservation_finished (reservation): pass
def reservation_killed_by_system (reservation): pass
def reservation_killed_by_client (reservation): pass
def reservation_unconfirmed (reservation): pass
def reservation_confirmed (reservation): pass

def log (record_type, id_string, messages=None):
    """Log an arbitrarily-typed PBS action."""
    dt = datetime.now()
    assert record_type in record_types, "%s is not an allowed record_type" % (
        record_type)
    if messages:
        messages = messages.copy()
        for key in messages:
            if " " in str(messages[key]):
                messages[key] = "\"%s\"" % (messages[key], )
        message_text = " ".join("%s=%s" % (key, value)
            for (key, value) in messages.iteritems())
    else:
        message_text = ""
    return "%s;%s;%s;%s" % (
        dt.strftime("%m/%d/%Y %H:%M:%S"), record_type, id_string, message_text)

record_types = \
    ("A", "B", "C", "D", "E", "F", "K", "k", "Q", "R", "S", "T", "U", "Y")
 
