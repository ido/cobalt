#
# cqparse.py
# Cobalt Queue Parser
#
# Matthew Woitaszek
# 21 November 2006
#
# Portions of this file are based on the existing Cobalt qhist script developed
# by Argonne National Laboratory. Special thanks to Theron Voran for his
# assistance!
#
# This script parses the Cobalt logs and presents a data structure
# representing user jobs.
#
__revision__ = '$Revision$'

import commands
import datetime
import os
import re
import logging
import string
import sys
import time
import ConfigParser
import math

import Cobalt
import Cobalt.Proxy
import Cobalt.Data
import Cobalt.Logging

#
# Configuration
#

# Choose the default log directory. If we have /var/log/cobalt, use that
# (as in a production system). If debugging from SVN, use the local logs.
# Otherwise, panic!
# read log_dir from [cqm] in cobalt.conf
CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)
try:
    DEFAULT_LOG_DIRECTORY = CP.get('cqm', 'log_dir')
except ConfigParser.NoOptionError:
    DEFAULT_LOG_DIRECTORY = '/var/log/cobalt-accounting'

# if os.path.exists( "/var/log/cobalt" ):
#     DEFAULT_LOG_DIRECTORY = "/var/log/cobalt"
# elif os.path.exists( os.path.join( os.path.curdir + "/logs" ) ):
#     DEFAULT_LOG_DIRECTORY = os.path.join( os.path.curdir + "/logs" )
# else:
#     raise IOError, "No Cobalt log directory found. Please edit cqparse.py"

# Default number of previous days to include when examining logs. This must
# be greater than the maximum walltime in days + 1 so we are sure to catch the
# start and the end of every job.
DEFAULT_DAYS = 3

#
# Create a logger
#

# Python 2.4 style:
#logging.basicConfig( level=logging.DEBUG,
#    format='%(name)-16.16s %(levelname)-8s : %(message)s')

# Create a logger Python 2.3-style:
# formatter = logging.Formatter('%(name)-9.9s %(levelname)-8s : %(message)s')
# console = logging.StreamHandler()
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

# # Get a logger for the main program
# logger = logging.getLogger( "cqparse" )
# logger.setLevel( logging.DEBUG )
#Cobalt.Logging.setup_logging('cqm', level=logging.INFO)
logger = logging.getLogger('cqm')

# ----------------------------------------------------------------------------
#
# Regular Expression Definitions
#
# ----------------------------------------------------------------------------

# Log filename regular expression
# qm-2007_02_05.log
re_filename = re.compile( """
    qm-
    (?P<year>\d\d\d\d)_
    (?P<month>\d\d)_
    (?P<day>\d\d)
    \.log
    """, re.VERBOSE)

# Submit job regular expression
#       2007-02-05 22:09:06 Q;25592;voran;default
re_submit = re.compile( """
    (?P<submit_time>
    \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
    \d+:\d+:\d+)\s+                         # hh:nn:ss
    Q;                                      # S;
    (?P<jobid>\d+);                         # jobid;
    (?P<username>\S+);                      # username;
    (?P<queue>\S+)                          # queue
    """, re.VERBOSE )

# pre-0.97 Start job regular expression
#       Nov  6 08:14:32 fr0105en cqm[16293]:
#       S;31572;muszala;N/A;31;31;62;vn;10.0
re_start_old = re.compile( """
    (?P<start_time>
    \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
    \d+:\d+:\d+)\s+                         # hh:nn:ss

    S;                                      # S;
    (?P<jobid>\d+);                         # jobid;
    (?P<username>\S+);                      # username;
    (?P<location>\S+);                      # location;
    (\d+);                                  # unknown
    (?P<nodes>\d+);                         # nodes
    (?P<processors>\d+);                    # processors
    (?P<mode>\S+);                          # mode
    (?P<walltime>\d+[\.\d+]*)$              # walltime
    """, re.VERBOSE )

# Start job regular expression
#       Nov  6 08:14:32 fr0105en cqm[16293]:
#       S;31572;muszala;N/A;31;62;vn;10.0
re_start = re.compile( """
    (?P<start_time>
    \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
    \d+:\d+:\d+)\s+                         # hh:nn:ss

    S;                                      # S;
    (?P<jobid>\d+);                         # jobid;
    (?P<username>[^;]+);                    # username;
    (?P<location>[^;]+);                    # location;
    (?P<nodes>\d+);                         # nodes
    (?P<processors>\d+);                    # processors
    (?P<mode>[^;]+);                        # mode
    (?P<walltime>\d+[\.\d+]*)$              # walltime
    """, re.VERBOSE )

# Running job regular expression:
#       Nov  6 08:14:32 fr0105en cqm[16293]:
#       Job 31572/muszala/Q:debug: Running job on 32_R000_J104_N1
re_run = re.compile( """
    \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
    \d+:\d+:\d+\s+                          # hh:nn:ss

    Job\s+                                  # Job
    (?P<jobid>\d+)/(?P<username>\S+)/Q:     # nnnnnn/username/Q:
    (?P<queue>\S+):\s+                      # queue:
    Running\sjob\son\s                      # Running job on
    (?P<partition>\S+)                      # partition
    """, re.VERBOSE )

# re_freeing = re.compile( """
#     (?P<finish_time>
#     \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
#     \d+:\d+:\d+)\s+                         # hh:nn:ss

#     Job\s+                                  # Job
#     (?P<jobid>\d+):\s+                      # nnnnnn:
#     Freeing\spartition\s                    # Freeing partition
#     \S+                                     # partition_name
#     """, re.VERBOSE )


# Job stats regular expression:
#       Nov  6 08:15:56 fr0105en cqm[16293]:
#       Job 31572/muszala on 31 nodes done. queue:7.59s user:82.79s 
re_stats = re.compile( """
    (?P<finish_time>
    \d\d\d\d-\d\d-\d\d\s+                   # Mon 0
    \d+:\d+:\d+)\s+                         # hh:nn:ss
    
    Job\s+                                  # Job
    (?P<jobid>\d+)/(?P<username>\S+)\s+     # nnnnnn/username
    on\s+                                   # on
    (?P<nodes>\d+)\s+                       # nn
    nodes\s+done\.\s+                       # nodes done.
    queue:(?P<queuetime>\d+\.\d+)s\s+       # queue:_.__s
    user:(?P<usertime>\d+\.\d+)s\s+         # user:_.__s
    (exit:(?P<exitcode>\d+)\s+)?
    """, re.VERBOSE )

# Job done regex
#
#
re_done = re.compile("""
    (?P<finish_time>
    \d\d\d\d-\d\d-\d\d\s+
    \d+:\d+:\d+)\s+                         # hh:nn:ss

    E;
    (?P<jobid>\d+);                         # jobid;
    (?P<username>\S+);                      # username;
    (?P<usertime>\d+)
    """, re.VERBOSE)

# Job deleted regex
# 2007-02-16 15:09:07 D;22;voran
#
re_deleted = re.compile("""
    (?P<finish_time>
    \d\d\d\d-\d\d-\d\d\s+
    \d+:\d+:\d+)\s+                         # hh:nn:ss

    D;
    (?P<jobid>\d+);                         # jobid;
    (?P<username>\S+)\s*                    # username
    """, re.VERBOSE)

# kernel regex
# 2007-04-19 22:32:34 Job 49/voran using kernel default
re_kernel = re.compile("""
    \d\d\d\d-\d\d-\d\d\s+                   # yyyy-mm-dd
    \d+:\d+:\d+\s+                          # hh:nn:ss
    Job\s+
    (?P<jobid>\d+)/(?P<username>\S+)\s+     # nnnnnn/username
    using\s+kernel\s+
    (?P<kernel>\S+)\s*
    """, re.VERBOSE)

# ----------------------------------------------------------------------------
#
# Cobalt Job Object
#
# ----------------------------------------------------------------------------

class CobaltJob(Cobalt.Data.Data):
    
    """A single job run through the Cobalt scheduling system."""
    
    fields = Cobalt.Data.Data.fields.copy()
    fields.update(dict(
        
        jobid = None,
        
        # Job submission
        submit_time = None,
        
        # User and job info
        username = None,
        nodes = None,
        processors = None,
        mode = None,
        walltime = None,
        start_time = None,
        
        # Job assignment
        queue = None,
        partition = None,
        partition_size = None,
        
        # Final job times
        finish_time = None,
        queue_time = None,
        user_time = None,
        deleted_time = None,
        
        # Job state and misc.
        state = None, # queued, running, done, None (invalid)
        usertime_formatted = None,
        queuetime_formatted = None,
        finishtime_formatted = None,
        exitcode = None,
        kernel = "default",
    ))
    
    def __init__(self, jobid):
        
        """Initialize a new empty CobaltJob."""
        
        Cobalt.Data.Data.__init__(self)
        self.tag = "job"
        self.jobid = long(jobid)
        
        # Job submission information
        self._submit = False
        
        # Basic user and job information
        self._start = False
        
        # Job assignment information
        self._run = False
        
        # Final job times
        self._done = False
        self._deleted = False

    def __str__(self):
        return "<CobaltJob %i>" % (self.jobid)
    
    def get(self, *args, **kwargs):
        """Extend Cobalt.Data.Data.get.
        
        Automatically convert datetime values to a corresponding
        timestamp value.
        """
        value = Cobalt.Data.Data.get(self, *args, **kwargs)
        if isinstance(value, datetime.datetime):
            return time.mktime(value.timetuple())
        return value

    def finalize(self):
        """
        Check this log record for proper formatting. Return True if the record
        is properly formatted, or False if there is a problem.
        """
        
        logger = logging.getLogger('cqm') 
        
        #
        # First, determine the state. The state is defined by which log messages
        # we have observed for this job. If we get a bogus combination, mark
        # the job as invalid
        #
        if self._start and self._run and (self._done or self._deleted):
            self.state = "done"
        elif self._submit and self._start and self._run and (not self._done):
            self.state = "running"
        elif self._submit and not self._start and not self._run and not self._done:
            self.state = "queued"

        # If we have only the tail end states, that means the job started before
        # our analysis period. Ignore those silently!
        elif not self._submit and not self._start and self._run and self._done:
            self.state = None
        elif not self._submit and not self._start and not self._run and self._done:
            self.state = None
#         elif self._submit and self._start and self._done:
#             self.state = "done"
        else:
            self.state = None
            logger.error("Job %i has a bogus state: %i %i %i %i" % (self.jobid,
                self._submit, self._start, self._run, self._done ))
            return False

        # If the job is queued or running, the completion statistics will not
        # be available. Leave now.
        if self.state != "done":
            return True
        
        #
        # Now that we have verified that all four log events were recorded,
        # check the interpreted parameters for sanity
        #
        result = True
        
        # Make sure that we have a username
        if self.username is None:
            logger.error("Job %i has an empty username" % (self.jobid))
            result = False
        
        # Check that the finish time is after the start time
        if self.start_time > self.finish_time and not self._deleted:
            logger.error("Job %i finishes before it starts (%s, %s)" %
                (self.jobid, self.start_time, self.finish_time))
            result = False
        
#         # Verify that the partition size is sane for a BG/L system
#         if self.get('partition_size') <= 0:
#             logger.error("Job %i partition %s size decoded as %i" %
#                 (self.get('jobid'), self.get('partition'), self.get('partition_size')))
#             result = False
#         if self.get('partition_size') % 32 != 0:
#             logger.error("Job %i partition size %i is not a multiple of 32" %
#                 (self.get('jobid'), self.get('partition_size')))
#             result = False
        
#         # Verify that the number of nodes fits within the paritition
#         if self.get('nodes') > self.get('partition_size'):
#             logger.error("Job %i fits %i nodes on a %i-node partition" %
#                 (self.get('jobid'), self.get('nodes'), self.get('partition_size')))
#             result = False

        # hack for a job that is forcibly deleted (cqadm.py --delete)
        # job stats are not produced, only D; line
        if self.finish_time is None and self._deleted:
            # definitely has start_time and deleted_time at this point
            if self.submit_time is not None:
                self.queue_time = self.start_time - self.submit_time
            else:
                self.queue_time = 0
            self.user_time = self.deleted_time - self.start_time
            self.finish_time = self.deleted_time
        
        # Make sure that the queue and user times are positive
        if self.queue_time < 0:
            logger.error("Job %i has negative queue time" % (self.jobid))
            self.queue_time = 0
            result = False
        if self.user_time < 0:
            logger.error("Job %i has negative user time" % (self.jobid))
            self.user_time = 0
            result = False
        
        #
        # Now, calculate the derived parameters
        #
        
        # We have usertime seconds but want hh:nn:ss     
        def format_time(seconds):
            if not seconds:
                (hours, minutes, seconds) = (0, 0, 0)
            else:
                hours = int( seconds / 3600 )
                seconds = seconds - (hours * 3600)
                minutes = int( seconds / 60 )
                seconds = seconds - (minutes * 60)
            return "%02i:%02i:%02i" % (hours, minutes, seconds)
        
        self.usertime_formatted = format_time(self.user_time)
        self.queuetime_formatted = format_time(self.queue_time)
        self.finishtime_formatted = self.finish_time.strftime("%Y-%m-%d %H:%M:%S")

        if self.exitcode is None or self.exitcode == "N/A":
            self.exitcode = "N/A"
        elif int(self.exitcode) > 255:
            self.exitcode = int(self.exitcode) / 256
        
        return result


class CobaltLogParser(Cobalt.Data.DataSet):
    """
    The CobaltLogParser contains a processed list of Cobalt jobs.
    
    Logfiles are processed by calling parse_file, and a directory of logfiles
    may be processed in any order. 
    """
    __object__ = CobaltJob
    
    def __init__(self):
        """
        Create a new CobaltLogParser.
        """
        Cobalt.Data.DataSet.__init__(self)
        self._jobs = {}
        #self.comms = Cobalt.Proxy.CommDict()
    
    # ----------------------------------------
    # Generators
    # ----------------------------------------
    def finished_jobs(self):
        """
        Return the jobs that are fully logged; the job's queue, run, and done
        events were present during the analysis period.
        """
        for jobid in self._jobs:
            job = self._jobs[jobid]
            if job.state == "done":
                yield(job)

    def running_jobs(self):
        """
        Return the jobs that are probably running.
        """
        for jobid in self._jobs:
            job = self._jobs[jobid]
            if job.state == "running":
                yield(job)

    def queued_jobs(self):
        """
        Return the jobs that are probably running.
        """
        for jobid in self._jobs:
            job = self._jobs[jobid]
            if job.state == "queued":
                yield(job)


    # ----------------------------------------
    # Logfile parsing
    # ----------------------------------------
    def __prepare_time(self, year_hint, log_time_string):
        """
        Given a year hint and a log time string, return a complete date.
        
        We use this procedure when parsing syslog log files. The log events
        do not include the year, but the filenames are named with the year.
        This procedure turns a time string from the logfile, adds the year,
        and returns a valid Python time.
        """
        if str(year_hint) in log_time_string:
            return datetime.datetime(
                *time.strptime(log_time_string, "%Y-%m-%d %H:%M:%S")[0:6])
        else:
            return datetime.datetime(
                *time.strptime(
                    "%s %i" % (log_time_string, year_hint),"%b %d %H:%M:%S %Y")[0:6])
    

    def parse_file(self, filename):
        """
        Parse the specified log file and retrieve the included job information.
        Make sure to call finalize_parse() after parsing all of the logfiles!
        """
        
        # Verify that the specified log file exists
        if not os.path.exists(filename):
            raise IOError("Log file %s not found" % (filename))      
        
        # Based on the log filename, guess the year. We need the years for the
        # complete database specification! :-/        
        basename = os.path.basename( filename )
        if basename == "cobalt.log":
            year_hint = datetime.datetime.now().year
        else:
            # Get the year, month, and day from the logfile
            m = re_filename.match(basename)
            if not m:
                assert False, \
                    "Filename %s was not 'cobalt.log' or 'cobalt.log-yyyymmdd'" % \
                    (filename)
            filetime = datetime.date(int(m.group("year")),
                int(m.group("month")), int(m.group("day")))
            
            # The file times are one day in advance; that is, the logfile for
            # 01 Nov is really 31 Oct. Subtract a single day and save the year.
            filetime = filetime - datetime.timedelta(days=1)
            year_hint = filetime.year
        
        # Read the log file        
        file = open( filename, "r" )
        for line in file:
            # Try the line against the three regular expressions we're looking
            # for. We don't require the logs to be parsed in order, so any of
            # the lines may appear first.
            
            # If the line matches the regular expressions, extact the jobid.
            # This is a bit kludgy, but we'll want separate match objects
            # later so we can set parameters.
            jobid = None
            m_submit = re_submit.match(line)
            if m_submit:
                jobid = long(m_submit.group("jobid"))
            m_start = re_start.match(line)
            if m_start:
                jobid = long(m_start.group("jobid"))
            m_start_old = re_start_old.match(line)
            if m_start_old:
                jobid = long(m_start_old.group("jobid"))
                m_start = m_start_old
            m_run = re_run.match(line)
            if m_run:
                jobid = long(m_run.group("jobid"))
#             m_freeing = re_freeing.match(line)
#             if m_freeing:
#                 jobid = long(m_freeing.group("jobid"))
            m_done = re_done.match(line)
            if m_done:
                jobid = long(m_done.group("jobid"))
            m_deleted = re_deleted.match(line)
            if m_deleted:
                jobid = long(m_deleted.group("jobid"))
            m_stats = re_stats.match(line)
            if m_stats:
                jobid = long(m_stats.group("jobid"))
            m_kernel = re_kernel.match(line)
            if m_kernel:
                jobid = long(m_kernel.group("jobid"))
            
            # If none matched, then get the next line
            if not jobid:
                continue
            
            # Now, get or create the record            
            if jobid not in self._jobs:
                job = CobaltJob(jobid)
                self._jobs[jobid] = job
            else:
                job = self._jobs[jobid]
            
            # Set the object's parameters
            if m_submit:
                job._submit = True
                job.submit_time = self.__prepare_time(
                    year_hint, m_submit.group("submit_time"))
            if m_start:
                job._start = True
                job.start_time = self.__prepare_time(
                    year_hint, m_start.group("start_time"))
                job.username = m_start.group("username")
                job.nodes = int(m_start.group("nodes"))
                job.processors = int(m_start.group("processors"))
                job.mode = m_start.group("mode")
                job.walltime = m_start.group("walltime")
            if m_run:
                job._run = True
                job.queue = m_run.group("queue")
                job.partition = m_run.group("partition")
                part = [p for p in self._partitions if p.get('name') == job.partition]
                if part:
                    job.partition_size = int(part[0].get('size'))
#                     print 'size of %s is %s' % (job.partition, job.partition_size)
                else:
                # We have to manually size full racks! They don't start with
                # sizes! :-/ This makes it hard to be portable.
                    nums = re.findall(r"\d+", m_run.group("partition"))
                    for n in nums:
                        if int(n) > 1 and math.log(int(n), 2) % 1 == 0:
                            job.partition_size = int(n)

                    if job.partition_size is None:
                        logger.debug("While parsing log line '%s': Could not determine size of partition '%s'." % (line, job.partition))
                        job.partition_size = 0

            # Most of the time, we get freeing following by done. In some
            # crashes, we get freeing without the done. Flag those jobs as
            # done anyway. This is a hack. :-/
#             if m_freeing and job._submit and job._start and job._run:
#                 #job._done = True
#                 job.freed_partitions.append(m_freeing.group("partition"))
#                 if not job.finish_time:
#                     job.finish_time = self.__prepare_time(
#                         year_hint, m_freeing.group("finish_time"))
#                 if not job.queuetime:
#                     job.queuetime = 0
#                 if not job.usertime:
#                     job.usertime = 0
            
            if m_stats:
                job._done = True
                job.queue_time = float(m_stats.group("queuetime"))
                job.user_time = float(m_stats.group("usertime"))
                job.exitcode = m_stats.group("exitcode")

            if m_done:
                job._done = True
                job.finish_time = self.__prepare_time(
                    year_hint, m_done.group("finish_time"))
                job.user_time = float(m_done.group("usertime"))

            if m_deleted:
                job._deleted = True
                job.deleted_time = self.__prepare_time(
                    year_hint, m_deleted.group("finish_time"))

            if m_kernel:
                job.kernel = m_kernel.group("kernel")
        
        file.close()
    
    def finalize_parse(self):
        """
        Finalize the parsing operation, deriving job state and other
        information for all of the jobs that were recorded.
        """
        
        # First, calculate derived job state for all of the jobs
        #print dir(self.data)
        for job in self._jobs.itervalues():
            job.finalize()
    
        self.data = self._jobs.values()
    
    # ----------------------------------------
    # Log folder parsing
    # ----------------------------------------
    def perform_default_parse(self):
        """
        Perform the default parse, looking in the default directory
        for logfiles. (See the configuration at the top!)
        """
        
#         try:
#             self._partitions = self.comms['sched'].GetPartition([{'tag':'partition', 'name':'*', 'size':'*'}])
#         except Cobalt.Proxy.CobaltComponentError:
#             print "Failed to connect to scheduler"
#             self._partitions = []
#             #raise SystemExit, 1
        self._partitions = []
        
        # Verify that the log directory exists
        logdir = os.path.abspath( DEFAULT_LOG_DIRECTORY )
        if not os.path.exists( logdir ):
            raise IOError("Log directory %s not found. Check the " % (logdir) + \
                "log_dir parameter for [cqm] in cobalt.conf." )
        
        # Make sure that the directory contains a current cobalt.log
#         if not os.path.exists( os.path.join( logdir + "/cobalt.log" )):
#             raise IOError("Log directory %s does not contain cobalt.log. " % (logdir) + \
#                 "Check the DEFAULT_LOG_DIRECTORY parameter in cqparse.py." )
        
        # Get a list of all of the cobalt log files in that directory.
        # Start with the archive files of format "cobalt.log-yyyymmdd", and
        # then add the cobalt.log file we already checked for
        files = [ filename for filename in os.listdir( logdir )
                  if filename.startswith( "qm-" ) and
                  os.path.isfile( os.path.join( logdir + "/" + filename ))]
        files.sort()
        files = files[-DEFAULT_DAYS:]
#         files.append( "cobalt.log")
        
        # Now, parse all of the files
        for file in files:
            self.parse_file( os.path.join( logdir + "/" + file ))
        
        # Finalize the parse
        self.finalize_parse()
    

