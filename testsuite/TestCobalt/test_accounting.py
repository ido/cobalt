import logging
from datetime import datetime
import time

# Config options must be initialized prior to importing accounting.
from Cobalt.Util import init_cobalt_config
init_cobalt_config()

import Cobalt.accounting as accounting
from Cobalt.Components.cqm import Job

from StringIO import StringIO

from testsuite.TestCobalt.Utilities.assert_functions import assert_match

def dt_strptime (date_string, format):
    return datetime(*(time.strptime(date_string, format)[0:6]))


class FakeDatetime (datetime):

    @classmethod
    def now (cls):
        return cls(2000, 1, 1)


class TestAccounting (object):

    def setup (self):
        #logging.basicConfig()
        #self.stream = StringIO()
        #self.handler = logging.StreamHandler(self.stream)
        #accounting.logger.addHandler(self.handler)
        #accounting.logger.setLevel(logging.INFO)
        accounting.datetime = FakeDatetime

    def teardown (self):
        #accounting.logger.removeHandler(self.handler)
        #accounting.logger.setLevel(logging.NOTSET)
        accounting.datetime = datetime

    def test_log (self):
        log_entry = accounting.entry("A", 123,
            {'val1':1, 'val2':"foo", 'val3':"bar baz"})
        assert log_entry == \
            "01/01/2000 00:00:00;A;123;val1=1 val2=foo val3=\"bar baz\"", \
            log_entry

    def test_job_abort (self):
        job = Job({'jobid':123})
        resource_list = {'foo':'bar', 'nodect':'256'}
        user = 'frodo'
        log_entry = accounting.abort(job.jobid, user, resource_list)
        expected = "01/01/2000 00:00:00;A;123;Resource_List.foo=bar Resource_List.nodect=256 resource=NOTSET user=frodo"
        assert_match(log_entry, expected, "Abort record mismatch.")

    def test_job_abort_account (self):
        job = Job({'jobid':123})
        resource_list = {'foo':'bar', 'nodect':'256'}
        user = 'frodo'
        log_entry = accounting.abort(job.jobid, user, resource_list, account='MyProject')
        expected = "01/01/2000 00:00:00;A;123;Resource_List.foo=bar Resource_List.nodect=256 account=MyProject resource=NOTSET user=frodo"
        assert_match(log_entry, expected, "Account not properly added.")

    def test_job_abort_resource (self):
        job = Job({'jobid':123})
        resource_list = {'foo':'bar', 'nodect':'256'}
        user = 'frodo'
        log_entry = accounting.abort(job.jobid, user, resource_list, resource='bigmachine')
        expected = "01/01/2000 00:00:00;A;123;Resource_List.foo=bar Resource_List.nodect=256 resource=bigmachine user=frodo"
        assert_match(log_entry, expected, "Incorrect resource.")

    def test_job_checkpoint (self):
        job = Job({'jobid':123})
        expected = "01/01/2000 00:00:00;C;123;resource=NOTSET"
        log_entry = accounting.checkpoint(job.jobid)
        assert_match(log_entry, expected, "Bad Checkpoint Messagge")

    def test_job_delete (self):
        job = Job({'jobid':123})
        resource_list = {'foo':'bar', 'nodect':'256'}
        requester = 'me@mydomain.net'
        user = 'frodo'
        expected = "01/01/2000 00:00:00;D;123;Resource_List.foo=bar Resource_List.nodect=256 force=False requester=me@mydomain.net resource=NOTSET user=frodo"
        log_entry = accounting.delete(job.jobid, requester, user, resource_list)
        assert_match(log_entry, expected, "Bad delete entry.")

    def test_job_end (self):
        job = Job({'jobid':123})
        #group and session are unknown
        log_entry = accounting.end(job.jobid, job.user,
            "unknown", job.jobname, job.queue,
            job.outputdir, job.command, job.args, job.mode,
            0.1, 0.2, 0.3, -1.0, None,
            {'ncpus':job.procs, 'nodect':job.nodes,
             'walltime':str(job.walltime * 60)},
            "unknown", -2.0, 255,
            {'location':"ANL",
             'nodect':job.nodes,
             'walltime':"0.0"})
        expected = "01/01/2000 00:00:00;E;123;Exit_status=255 Resource_List.ncpus=None Resource_List.nodect=None Resource_List.walltime=0 args= ctime=0.1 cwd=None end=-2.0 etime=0.3 exe=None exec_host=None group=unknown jobname=N/A mode=co priority_core_hours=0 qtime=0.2 queue=default resource=NOTSET resources_used.location=ANL resources_used.nodect=None resources_used.walltime=0.0 session=unknown start=-1.0 user=None"
        assert_match(log_entry, expected, "Bad End Message.")

#from accounting.py

def demo ():
    from datetime import timedelta
    import logging

    class FakeDatetime (object):

        datetime = datetime

        def __init__ (self, now):
            self.start = self.datetime.now()
            self.epoch = now

        def now (self):
            return self.epoch + (self.datetime.now() - self.start)

    global datetime
    datetime_ = datetime
    datetime = FakeDatetime(datetime_(2000, 1, 1))

    logger = logging.getLogger("accounting")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(DatetimeFileHandler("%Y%m%d"))

    logger.info(abort(1))

    logger.info(begin(1, owner="janderso", queue="default",
        ctime=datetime.now(), start=datetime.now(),
        end=datetime.now()+timedelta(hours=1),
        duration=timedelta(hours=1), exec_host="ANL-R00-M0-512",
        authorized_users=["janderso", "acherry"],
        resource_list={'nodes':512}))

    logger.info(checkpoint(1))

    logger.info(delete(1, "janderso@login1.surveyor.alcf.anl.gov"))

    logger.info(end(1, "janderso", "users", "foojob", "default",
        datetime.now(), datetime.now(), datetime.now(), datetime.now(),
        "ANL-R00-M0-512", {'nodes':512}, 123,
        datetime.now()+timedelta(hours=1), 0,
        {'nodes':512, 'time':timedelta(hours=1)}, account="myproject"))

    logger.info(finish(1))

    datetime = FakeDatetime(datetime_(2000, 1, 2))

    logger.info(system_remove(1, "root@sn1"))

    logger.info(remove(1, "janderso@login1"))

    logger.info(queue(1, "default"))

    logger.info(rerun(1))

    logger.info(start(1, "janderso", "users", "foojob", "default",
        datetime.now(), datetime.now(), datetime.now(), datetime.now(),
        "ANL-R00-M0-512", {'nodes':512}, 123))

    logger.info(unconfirmed(1, "janderso@alcf.anl.gov"))

    logger.info(confirmed(1, "janderso@alcf.anl.gov"))


if __name__ == "__main__":
    demo()
