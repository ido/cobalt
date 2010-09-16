#!/usr/bin/env python

'''Tool for reading out and auditing the cobalt log databse state.
   generates some basic useful statistics for records in range'''

__revision__ = '$Revision: 1'


#TODO:
#Dump the lifetime of a job
#  --do this in an actually readable way.
#Generate time statistics like Queued time, run-time, cleanup-time,
#  Total time for job, if ran at all, and if killed what was the state.


import os.path
import sys
import time
import optparse

from cdbaccess import cdbaccess, AccessOnlyDAO, JobSummaryData


__helpmsg__ = """Usage: cdbdump.py [options] start_jobid [end_jobid]
                 options:
                    -s, --summarize: provide summaries of the job lifetime"""


def parse_options():
   
   opt_parser = optparse.OptionParser()

   opt_parser.add_option('-s', '--summarize', action='store_true', 
                         dest='summarize')


   opt_parser.set_defaults(summarize=False)

   return opt_parser.parse_args()


class JobData(object):
   pass

class JobEvents(object):

   pass




def get_full_job(jobid, daos):

   """takes a job id and list of data access objects (daos) and 
      extracts a job's full information."""

   pass


class eventTimes(object):
   
   def __init__(self):
      initString = "Not Yet Occurred."
      self.creating = initString
      self.starting = initString
      self.running = initString
      self.run_ended = initString
      self.resource_epi_end = initString
      self.job_end = initString

      self.hasStarted = False
      self.deleted = False
      self.del_time = None
      self.user_delete = None

   def __str__(self):

      retStr = ["Created: %s" % self.creating,
                "Started: %s" % self.starting,
                "Run Start: %s" %self.running,
                "Run End: %s" % self.run_ended,
                "Resouce Epilogue End: %s" % self.resource_epi_end,
                "Job Ended: %s" % self.job_end]

      if self.deleted:
         retStr.append(" ")
         retStr.append("Deleted by User %s at %s" % (self.user_delete, 
                                                     self.del_time))

      return '\n'.join(retStr)


def summary_str(jobRecords):
   
   
   events = eventTimes()

   for record in jobRecords:
      
     
      if record.v.EVENT_TYPE in ['creating', 'starting', 'running']:
         events.__setattr__(record.v.EVENT_TYPE, record.v.ENTRY_TIME)
      
      if record.v.EVENT_TYPE == 'starting':
         events.hasStarted = True
      elif record.v.EVENT_TYPE == 'killing':
         events.del_time = record.v.ENTRY_TIME
         events.user_delete = record.v.EXEC_USER
         events.deleted = True
         if not events.hasStarted:
            events.running = "N/A"
            events.run_ended = "N/A"
            events.resource_epi_end = "N/A"
            events.job_end = record.v.ENTRY_TIME
      elif record.v.EVENT_TYPE == 'resource_epilogue_start':
         events.run_ended = record.v.ENTRY_TIME
      elif record.v.EVENT_TYPE == 'resource_epilogue_finished':
         events.resource_epi_end = record.v.ENTRY_TIME
      elif record.v.EVENT_TYPE == 'job_epilogue_finished':
         events.job_end = record.v.ENTRY_TIME
      
   return str(events)
         
          
         

   
      

   




if __name__ == '__main__':

   #Command line options.  If conflict with config, these win.
   opts, args = parse_options()

   #open a connection to the database and grab requested records.  

   start_jobid = None
   end_jobid = None

   if (len(args) < 1 or len(args) > 2):
      print "Usage: cdbdump start [end]"

   start_jobid = int(args[0])
   if len(args) > 1:
      end_jobid = int(args[1]) + 1
   else:
      end_jobid = start_jobid + 1

   database = 'COBALT_D'
   user = 'cobaltdev'
   pwd = 
   schema = 'cobalt_log_db'

   db = cdbaccess(database, user, pwd, schema)

   js_dao = JobSummaryData(db.db, schema, 'JOB_SUMMARY')

   for jobid in xrange(start_jobid, end_jobid):

      print '*' * 80
      histList = js_dao.get_job_history(jobid)
      tot_time = db.daos['JOB_PROG'].get_total_time(jobid)
      tqt_time = db.daos['JOB_PROG'].get_total_queued_time(jobid)
      #queue_wait_time
      wait_time = 0
      hold_times = db.daos['JOB_PROG'].get_hold_times(jobid)
      #print hold_times
      in_hold = False
      if hold_times == None:
         print "Could not determine wait time due to error."
         wait_time = "Error"
      elif hold_times[0] == 0:
         wait_time = tqt_time
      elif hold_times[len(hold_times)-1] == None:
         wait_time = "Job still in hold"
         in_hold = True
      else:
         if tqt_time == None:
            wait_time = 'Undefined'
         else:
            wait_time = tqt_time - sum(hold_times)
      
      


      #Output ******************************************************
      
      print "Summary for Cobalt Job ID: %d" % (jobid)

      
      
      #print '\n'.join([str(hist.v.EVENT_TYPE) for hist in histList])
      print summary_str(histList)
      print (' ')

      print "Total Runtime: %d sec" % tot_time
      if tqt_time == None:
         print "Total Queued Time: Did Not Run" 
      else:
         print "Total Queued Time: %d sec" % tqt_time
      if in_hold:
         print "Wait Time: %s" % wait_time
      else:
         print "Wait Time: %s sec" % wait_time
   
   print '*' * 80

   db.close()
   
                         
