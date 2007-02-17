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

import commands, datetime, os, re, logging, string, sys, time, ConfigParser, math
import Cobalt.Proxy, Cobalt.Data, Cobalt.Logging

#
# Configuration
#

# Choose the default log directory. If we have /var/log/cobalt, use that
# (as in a production system). If debugging from SVN, use the local logs.
# Otherwise, panic!
# read log_dir from [cqm] in cobalt.conf
CP = ConfigParser.ConfigParser()
CP.read(['/etc/cobalt.conf'])
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
Cobalt.Logging.setup_logging('cqp', level=logging.INFO)
logger = logging.getLogger('cqp')

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


# ----------------------------------------------------------------------------
#
# Cobalt Job Object
#
# ----------------------------------------------------------------------------

class CobaltJob(Cobalt.Data.Data):
    """
    The CobaltJob class represents a single job run through the Cobalt
    scheduling system.
    """
    
    def __init__(self, jobid):
        """
        Create a new empty CobaltJob object.
        """
        Cobalt.Data.Data.__init__(self, {'tag':'job'})
        self.set('jobid', long(jobid))
        
        # Job submission information
        self._submit = False
        self.set('submit_time', None)
        
        # Basic user and job information
        self._start = False
        self.set('start_time', None)
        self.set('username', None)
        self.set('nodes', None)
        self.set('processors', None)
        self.set('mode', None)
        self.set('walltime', None)
        
        # Job assignment information
        self._run = False
        self.set('queue', None)
        self.set('partition', None)
        self.set('partition_size', None)
        
        # Final job times
        self._done = False
        self.set('finish_time', None)
        self.set('queuetime', None)
        self.set('usertime', None)
        self._deleted = False
        self.set('deletedtime', None)
        
        # Derived job state and other information
        self.set('state', None)   # queued, running, done, None (invalid)
        self.set('usertime_formatted', None)
        self.set('queuetime_formatted', None)
        self.set('exitcode', None)
    

    def __str__(self):
        return "<CobaltJob %i>" % (self.get('jobid'))

    def get(self, field, default=None):
        '''return attribute (overloaded from Data)'''
        if self._attrib.has_key(field):
            if isinstance(self._attrib[field], datetime.datetime):
                return time.mktime(self._attrib[field].timetuple())
            return self._attrib[field]
        if default != None:
            return default
        raise KeyError, field

    def finalize(self):
        """
        Check this log record for proper formatting. Return True if the record
        is properly formatted, or False if there is a problem.
        """
        
        logger = logging.getLogger("cqparse.CobaltJob") 
        
        #
        # First, determine the state. The state is defined by which log messages
        # we have observed for this job. If we get a bogus combination, mark
        # the job as invalid
        #
        if self._start and self._run and (self._done or self._deleted):
            self.set('state', "done")
        elif self._submit and self._start and self._run and (not self._done):
            self.set('state', "running")
        elif self._submit and not self._start and not self._run and not self._done:
            self.set('state', "queued")

        # If we have only the tail end states, that means the job started before
        # our analysis period. Ignore those silently!
        elif not self._submit and not self._start and self._run and self._done:
            self.set('state', None)
        elif not self._submit and not self.start_time and not self._run and self._done:
            self.set('state', None)
#         elif self._submit and self._start and self._done:
#             self.state = "done"
        else:
            self.set('state', None)
            logger.error("Job %i has a bogus state: %i %i %i %i" % (self.jobid,
                self._submit, self._start, self._run, self._done ))
            return False

        # If the job is queued or running, the completion statistics will not
        # be available. Leave now.
        if self.get('state') != "done":
            return True
        
        #
        # Now that we have verified that all four log events were recorded,
        # check the interpreted parameters for sanity
        #
        result = True
        
        # Make sure that we have a username
        if not self.get('username'):
            logger.error("Job %i has an empty username" % (self.get('jobid')))
            result = False
        
        # Check that the finish time is after the start time
        if self.get('start_time') > self.get('finish_time') and not self._deleted:
            logger.error("Job %i finishes before it starts (%s, %s)" %
                (self.get('jobid'), self.get('start_time'), self.get('finish_time')))
            result = False
        
        # Verify that the partition size is sane for a BG/L system
        if self.get('partition_size') <= 0:
            logger.error("Job %i partition %s size decoded as %i" %
                (self.get('jobid'), self.get('partition'), self.get('partition_size')))
            result = False
        if self.get('partition_size') % 32 != 0:
            logger.error("Job %i partition size %i is not a multiple of 32" %
                (self.get('jobid'), self.get('partition_size')))
            result = False
        
        # Verify that the number of nodes fits within the paritition
        if self.get('nodes') > self.get('partition_size'):
            logger.error("Job %i fits %i nodes on a %i-node partition" %
                (self.get('jobid'), self.get('nodes'), self.get('partition_size')))
            result = False

        # hack for a job that is forcibly deleted (cqadm.py --delete)
        # job stats are not produced, only D; line
        if not self.get('finish_time') and self._deleted:
            self.set('queuetime', self.get('start_time') - self.get('submit_time'))
            self.set('usertime', self.get('deleted_time') - self.get('start_time'))
            self.set('finish_time', self._attrib['deleted_time'])
        
        # Make sure that the queue and user times are positive
        if self.get('queuetime') < 0:
            logger.error("Job %i has negative queue time" % (self.get('jobid')))
            result = False
        if self.get('usertime') < 0:
            logger.error("Job %i has negative user time" % (self.get('jobid')))
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
        
        self.set('usertime_formatted', format_time(self.get('usertime')))
        self.set('queuetime_formatted', format_time(self.get('queuetime')))
        self.set('finish_time_formatted', self._attrib['finish_time'].strftime("%Y-%m-%d %H:%M:%S"))
        if self.get('exitcode') == None:
            self.set('exitcode', 'N/A')
        
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
        try:
            sched = Cobalt.Proxy.scheduler()
            self._partitions = sched.GetPartition([{'tag':'partition', 'name':'*', 'size':'*'}])
        except Cobalt.Proxy.CobaltComponentError:
            print "Failed to connect to scheduler"
            self._partitions = []
            #raise SystemExit, 1
    
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
            if job.get('state') == "done":
                yield(job)

    def running_jobs(self):
        """
        Return the jobs that are probably running.
        """
        for jobid in self._jobs:
            job = self._jobs[jobid]
            if job.get('state') == "running":
                yield(job)

    def queued_jobs(self):
        """
        Return the jobs that are probably running.
        """
        for jobid in self._jobs:
            job = self._jobs[jobid]
            if job.get('state') == "queued":
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
                job.set('submit_time', self.__prepare_time(
                    year_hint, m_submit.group("submit_time")))
            if m_start:
                job._start = True
                job.set('start_time', self.__prepare_time(
                    year_hint, m_start.group("start_time")))
                job.set('username', m_start.group("username"))
                job.set('nodes', int(m_start.group("nodes")))
                job.set('processors', int(m_start.group("processors")))
                job.set('mode', m_start.group("mode"))
                job.set('walltime', m_start.group("walltime"))
            if m_run:
                job._run = True
                job.set('queue', m_run.group("queue"))
                job.set('partition', m_run.group("partition"))
                part = [p for p in self._partitions if p.get('name') == job.get('partition')]
                if part:
                    job.set('partition_size', int(part[0].get('size')))
#                     print 'size of %s is %s' % (job.partition, job.partition_size)
                else:
                # We have to manually size full racks! They don't start with
                # sizes! :-/ This makes it hard to be portable.
                    nums = re.findall(r"\d+", m_run.group("partition"))
                    for n in nums:
                        if int(n) > 1 and math.log(int(n), 2) % 1 == 0:
                            job.set('partition_size', int(n))

                    if not job.get('partition_size'):
                        print "While parsing log line '%s': Could not determine size of partition '%s'." % (line, job.partition)
                        job.set('partition_size', 0)

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
                job.set('finish_time', self.__prepare_time(
                    year_hint, m_stats.group("finish_time")))
                job.set('queuetime', float(m_stats.group("queuetime")))
                job.set('usertime', float(m_stats.group("usertime")))
                job.set('exitcode', m_stats.group("exitcode"))

            if m_done:
                job._done = True
                job.set('finish_time', self.__prepare_time(
                    year_hint, m_done.group("finish_time")))
                job.set('usertime', float(m_done.group("usertime")))

            if m_deleted:
                job._deleted = True
                job.set('deleted_time', self.__prepare_time(
                    year_hint, m_deleted.group("finish_time")))
        
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
    

