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

import datetime
import os
import os.path
import re
import logging
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

# Find the default log directory. Check config file, and default to
# /var/log/cobalt-accounting.
CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)
try:
    DEFAULT_LOG_DIRECTORY = os.path.expandvars(CP.get('cqm', 'log_dir'))
except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
    DEFAULT_LOG_DIRECTORY = Cobalt.DEFAULT_LOG_DIRECTORY

# Default number of previous days to include when examining logs. This must
# be greater than the maximum walltime in days + 1 so we are sure to catch the
# start and the end of every job.
DEFAULT_DAYS = 3

#
# Create a logger
#

logger = logging.getLogger('cqm')

# ----------------------------------------------------------------------------
#
# Regular Expression Definitions
#
# ----------------------------------------------------------------------------

# PBS Log filename regular expression
# 20090203
re_filename = re.compile( """(?P<year>\d\d\d\d)
                             (?P<month>\d\d)
                             (?P<day>\d\d)""", re.VERBOSE)

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
    (current_queue:(?P<current_queuetime>\d+\.\d+)s\s+)?  # current_queue:_.__s
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

# PBS-style exit log record
re_pbs_e = re.compile("""(?P<date>\d\d/\d\d/\d\d\d\d\s+
                         \d\d:\d\d:\d\d);
                         E;
                         (?P<jobid>\d+);
                         (?P<attributes>.*)$""", re.VERBOSE)

def _time_property(time_field):
    """
    The "private" time_field attribute of an object may contain some sort of time object.
    Or maybe a string.  Or a float.  Who knows?  
    
    Whatever it is, you're not getting a time object from the "public" attribute.
    """
    def _get_helper(self):
        value = getattr(self, time_field)
        if isinstance(value, datetime.datetime):
            return time.mktime(value.timetuple())
        else:
            return value
    
    def _set_helper(self, value):
        setattr(self, time_field, value)
        
    return property(_get_helper, _set_helper)

# ----------------------------------------------------------------------------
#
# Cobalt Job Object
#
# ----------------------------------------------------------------------------
class CobaltJob (Cobalt.Data.Data):
    
    """A single job run through the Cobalt scheduling system."""
    
    fields = Cobalt.Data.Data.fields + [
        "jobid", "submit_time", 
        "user", "nodes", "procs", "mode", "walltime", "start_time", 
        "queue", "location", "partition_size",
        "end_time", "endtime", "queued_time", "queuedtime", "run_time", "runtime", "deleted_time", 
        "state", "usertime_formatted", "queuetime_formatted", "finishtime_formatted",
        "exit", "kernel", "account",
    ]
    required = Cobalt.Data.Data.required + ["jobid"]

    def __init__(self, spec):
        
        """Initialize a new empty CobaltJob."""
        Cobalt.Data.Data.__init__(self, spec)

        self.tag = "job"
        
        for item in spec:
            setattr(self, item, spec[item])
        
    def __str__(self):
        return "<CobaltJob %i>" % (self.jobid)
    
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
        self.state = "done"
        
        #
        # Now that we have verified that all four log events were recorded,
        # check the interpreted parameters for sanity
        #
        result = True
        
        # Make sure that we have a username
        if self.user is None:
            logger.error("Job %i has an empty username" % (self.jobid))
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
        
        self.queuedtime = format_time(self.queued_time)
        self.endtime = datetime.datetime.fromtimestamp(
            self.end_time).strftime("%Y-%m-%d %H:%M:%S")

        if not self.exit.isdigit():
            self.exit = 'N/A'
        elif int(self.exit) > 255:
            self.exit = int(self.exit) / 256
        
        return result


class CobaltLogParser(Cobalt.Data.DataDict):
    """
    The CobaltLogParser contains a processed list of Cobalt jobs.
    
    Logfiles are processed by calling parse_file, and a directory of logfiles
    may be processed in any order. 
    """
    item_cls = CobaltJob
    key = "jobid"

#     def __init__(self):
#         """
#         Create a new CobaltLogParser.
#         """
#         Cobalt.Data.DataDict.__init__(self)
# #         self._jobs = {}
#         #self.comms = Cobalt.Proxy.CommDict()
    
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
    def __prepare_time(self, log_time_string):
        """
        Given a log time string, return a Python date.
        """
        return datetime.datetime(
            *time.strptime(log_time_string, "%Y-%m-%d %H:%M:%S")[0:6])
    

    def parse_file(self, filename):
        """
        Parse the specified log file and retrieve the included job information.
        Make sure to call finalize_parse() after parsing all of the logfiles!
        """
        
        # Verify that the specified log file exists
        if not os.path.exists(filename):
            raise IOError("Log file %s not found" % (filename))      

        # Verify that the filename is named in the format produced by
        # the logging utility. If not, we don't want to bother parsing it.
        basename = os.path.basename( filename )
        m = re_filename.match(basename)
        assert m is not None, \
            "Filename %s was not in format 'qm-yyyy_mm_dd'" % \
            (filename)
        
        # Read the log file
        logfile = open( filename, "r" )
        for line in logfile:
            # Try the line against the regular expressions we're looking
            # for. Currently just looking for the PBS exit line.
            
            # If the line matches the regular expressions, extract the jobid.
            # This is a bit kludgy, but we'll want separate match objects
            # later so we can set parameters.
            jobid = None
            m_pbs_e = re_pbs_e.match(line)
            if m_pbs_e:
                jobid = long(m_pbs_e.group("jobid"))
            
            # If none matched, then get the next line
            if not jobid:
                continue
            
            job = {'jobid':jobid}
            
            # the attributes regex group consists of all the job attributes
            # listed after the jobid on the log line
            job_attributes = m_pbs_e.group("attributes")
            attribute_dict = dict()
            for item in re.split(r'\s+(?=[a-zA-Z0-9_.]+=)', job_attributes):
                attribute_dict.update([item.split("=", 1)])
            job['user'] = attribute_dict['user']
            job['nodes'] = attribute_dict['Resource_List.nodect']
            job['procs'] = attribute_dict['Resource_List.ncpus']
            job['mode'] = attribute_dict['mode']
            job['runtime'] = attribute_dict['resources_used.walltime']
            job['walltime'] = attribute_dict['Resource_List.walltime']
            job['queue'] = attribute_dict['queue']
            job['location'] = attribute_dict['exec_host']
            job['account'] = attribute_dict.get('account', 'N/A')
            job['exit'] = attribute_dict.get('Exit_status', 'N/A')
            
            # stats
            job['submit_time'] = float(attribute_dict['ctime'])
            job['start_time'] = float(attribute_dict['start'])
            job['queued_time'] = float(attribute_dict['start']) - float(attribute_dict['ctime'])
            job['end_time'] = float(attribute_dict['end'])
            
            self.q_add([job])
        
        logfile.close()
    
    def finalize_parse(self):
        """
        Finalize the parsing operation, deriving job state and other
        information for all of the jobs that were recorded.
        """
        
        # Calculate derived job state for all of the jobs
        for job in self.itervalues():
            job.finalize()
    
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
                  if re.match("^\d{8,8}$", filename) and
                  os.path.isfile( os.path.join( logdir + "/" + filename ))]
        files.sort()
        files = files[-DEFAULT_DAYS:]
        
        # Now, parse all of the files
        for logfile in files:
            self.parse_file( os.path.join( logdir + "/" + logfile ))
        
        # Finalize the parse
        self.finalize_parse()
    

