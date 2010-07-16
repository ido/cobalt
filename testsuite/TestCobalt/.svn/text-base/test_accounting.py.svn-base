import logging
from datetime import datetime
import time

import Cobalt.accounting as accounting
from Cobalt.Components.cqm import Job

from StringIO import StringIO

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
        log_entry = accounting.log("A", 123,
            {'val1':1, 'val2':"foo", 'val3':"bar baz"})
        assert log_entry == \
            "01/01/2000 00:00:00;A;123;val3=\"bar baz\" val2=foo val1=1", \
            log_entry
    
    def test_job_abort (self):
        job = Job({'jobid':123})
        log_entry = accounting.job_abort(job)
        assert log_entry == \
            "01/01/2000 00:00:00;A;123;", log_entry
    
    def test_job_checkpoint (self):
        job = Job({'jobid':123})
        log_entry = accounting.job_checkpoint(job)
        assert log_entry == \
            "01/01/2000 00:00:00;C;123;", log_entry
    
    def test_job_delete (self):
        job = Job({'jobid':123})
        log_entry = accounting.job_delete(job, "me@mydomain.net")
        assert log_entry == \
            "01/01/2000 00:00:00;D;123;requester=me@mydomain.net", log_entry
    
    def test_job_end (self):
        job = Job({'jobid':123})
        log_entry = accounting.job_end(job)
        assert False, log_entry

