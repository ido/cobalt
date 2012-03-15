#!/usr/bin/env python

"""A set of helper methods to access data from the database.
These are intentionally read-only.

"""

import os
import sys

import db2util
__revision__ = '$Revision: 1 $'


class AccessOnlyDAO(db2util.dao):
   def insert (self, record):
      pass
   def update (self, record):
      pass
   def delete (self, record):
      pass


#Class for handling database output
class cdbaccess(object):

   def __init__(self, dbName, username, password, schema):

      self.db = db2util.db()
      
      try:
         self.db.connect(dbName, username, password)
      except:
         #logger.error("Failed to open a connection to database %s as user %s" %(dbName, username))
         raise

      self.schema = schema

      table_names = ['RESERVATION_DATA', 'RESERVATION_PARTS',
                     'RESERVATION_EVENTS', 'RESERVATION_USERS',
                     'RESERVATION_PROG', 'JOB_DATA', 'JOB_ATTR',
                     'JOB_DEPS', 'JOB_EVENTS','JOB_COBALT_STATES', 'JOB_PROG',
                     'JOB_SUMMARY']

      #Handle tables, There is probably a better way to do this.
      self.tables = {}
      self.daos = {}
      try:
         for table_name in table_names:
            #logger.info("Accessing table: %s" % table_name)
            self.tables[table_name] = db2util.table(self.db, schema, table_name)
         
            if table_name in ['RESERVATION_EVENTS', 'JOB_EVENTS', 'JOB_COBALT_STATES']:
               self.daos[table_name] = StateTableData(self.db, schema, 
                                                      self.tables[table_name].table)
            elif table_name == 'RESERVATION_DATA':
               self.daos[table_name] = ResDataData(self.db, schema, 
                                                   self.tables[table_name].table)
            
            elif table_name == 'JOB_DATA':
               self.daos[table_name] = JobDataData(self.db, schema, 
                                                   self.tables[table_name].table)
            elif table_name == 'JOB_DEPS':
               self.daos[table_name] = JobDepsData(self.db, schema, 
                                                   self.tables[table_name].table)
            elif table_name == 'JOB_PROG':
               self.daos[table_name] = JobProgData(self.db, schema, 
                                                   self.tables[table_name].table)
            elif table_name == 'JOB_SUMMARY':
                self.daos[table_name] = JobSummaryData(self.db, schema,
                                                    self.tables[table_name].table)
            else:
               self.daos[table_name] = AccessOnlyDAO(self.db, schema, 
                                                   self.tables[table_name].table)
      except:
         #logger.error("Error accessing table %s!" % table_name)
         self.db.close()
         raise
         
      
      #we opened with a schema, let's make that the default for now.
      self.db.prepExec("set current schema %s" % schema)
      

   def get_job_data_ids_from_jobid(self, jobid):
      job_data_record = self.daos['JOB_DATA'].table.getRecord()
      job_data_record.v.JOBID = jobid
      ids = self.daos['JOB_DATA'].search_most_recent(job_data_record)
      
     
      return ids[0].get('ID', None)


   def __get_most_recent_data_id(self, table, logMsg):
      """Takes a table name and ID.  Right now reservation specific.
         Returns an id if one found, if not returns None.
         Will expand to other record types as they are implemented.
         Meant to extract ids from x_DATA records."""

      data_record = self.daos[table].table.getRecord({
            'RESID': logMsg.item.res_id})
      res_ids = self.daos[table].search_most_recent(data_record)
      
      if not res_ids:
         return None
      
      return res_ids[0].get('ID', None)

   
   def close(self):
      self.db.close()
      
   
   
class StateTableData(AccessOnlyDAO):
   
   def getStatesDict(self):

      """Returns a dict mapping the name field to the id for that name for 
         all states in this table."""

      SQL = "select * from %s.%s" % (self.table.schema, self.table.table)
      
      result_list = self.db.getDict(SQL)
      
      ret_dict = {}
      for item in result_list:
         ret_dict[item['ID']] = item['NAME']

      return ret_dict

   def search (self, record):
      """look up the id for a given state-change identifier.  
      This had better be in this table."""

      SQL = "select ID from %s.%s where NAME = '%s'" % (self.table.schema, self.table.table, record.v.NAME)
      
      return self.db.getDict(SQL)
      

class ResDataData(AccessOnlyDAO):

   def search_most_recent (self, record):

      """Find the most recent version of a reservation data entry."""

      SQL = ("select reservation_data.id" ,
             "from reservation_prog, reservation_data",
             "where reservation_data.id = reservation_prog.res_data_id",
             "and reservation_data.resid = %d" % record.v.RESID,
             "order by entry_time DESC") 
      
      return self.db.getDict(' '.join(SQL))
   
   def search (self, record):
      
      SQL = "select ID from %s.%s where resid = %s" % (self.table.schema, 
                                                        self.table.table,
                                                        record.v.RESID)
      return self.db.getDict(SQL)



class JobDataData(AccessOnlyDAO):


   def find_dummy(self, jobid):
      """returns a dummy record.  If there is none for this job, returns None"""
      SQL = ("select id",
             "from job_data",
             "where jobid = %d" % jobid,
             "and isdummy != 0")
      job_data_id = self.db.getDict(' '.join(SQL))

      if not job_data_id:
         return None
      
      return self.getID(job_data_id[0]['ID'])
   

   def find_all_after_jobid(self, jobid):
      """gets all records with a jobid >= the passed jobid, joined
      with the job_progress table."""
        
      SQL = ("select job_prog.id jpid, job_data.id jdid, job_events.name " ,
             "from job_prog, job_data, job_events",
             "where job_data.id = job_prog.job_data_id",
             "and job_prog.event_type = job_events.id",
             "and job_data.jobid >= %d" % jobid,
             "order by jobid, entry_time") 
      
      return self.db.getDict(' '.join(SQL))

   def search_most_recent (self, record):

      """Find the most recent version of a reservation data entry."""

      SQL = ("select job_data.id" ,
             "from job_prog, job_data",
             "where job_data.id = job_prog.job_data_id",
             "and job_data.jobid = %d" % record.v.JOBID,
             "order by entry_time DESC") 
      
      return self.db.getDict(' '.join(SQL))
      

   def search (self, record):
      
      SQL = "select ID from %s.%s where jobid = %s" % (self.table.schema, 
                                                        self.table.table,
                                                        record.v.JOB_DATA_ID)
      return self.db.getDict(SQL)

   def search_by_jobid(self, jobid):

      """get a list of job_data entry ids that share the same jobid"""
      SQL = "select ID from %s.%s where jobid = %s" % (self.table.schema, 
                                                        self.table.table,
                                                        jobid)

      resultdicts = self.db.getDict(SQL)
      
      if resultdicts:
         return [entry['ID'] for entry in resultdicts] 
      return None

   

      
class JobProgData(AccessOnlyDAO):

   """helpers for getting at job progress data
      ordered by jobid and then entry time in the database"""
   
   def extract_range(self, jobid_start, jobid_end):
      """Gets a set of progress records, based on a range of jobid's
         These are record objects."""
      
      SQL = ("select job_prog.id",
             "from job_prog, job_data",
             "where job_data.id = job_prog.job_data_id",
             "and jobid >= %d" % jobid_start,
             "and jobid <= %d" % jobid_end,
             "order by jobid, entry_time")
      
      resultdict = self.db.getDict(' '.join(SQL))
      if not resultdicts:
         return []
      return [self.getID(result['ID']) for result in resultdicts]

   def get_list_by_data_id(self, job_data_id):

      """gets a list of all of the progress objects pointing to
         a job_data entry."""

      SQL = ("select id" ,
             "from job_prog",
             "where job_prog.job_data_id = %d" % job_data_id,
             "order by entry_time")

      resultdicts = self.db.getDict(' '.join(SQL))
      if not resultdicts:
         return []

      return [self.getID(result['ID']) for result in resultdicts]

   def get_list_by_jobid(self, jobid):

      """gets a list of all of the progress objects pointing to
         a job_data entry."""

      SQL = ("select job_prog.id" ,
             "from job_prog, job_data",
             "where job_prog.jog_data_id = job_data.id",
             "where job_prog.job_data_id = %d" % job_data_id,
             "order by entry_time")

      resultdicts = self.db.getDict(' '.join(SQL))
      if not resultdicts:
         return []

      return [self.getID(result['ID']) for result in resultdicts]


   def job_exists(self, jobid):
      
      """Returns a boolean value if this job actually exists."""
      SQL = ["select id",
             "from job_data",
             "where jobid = %d" % jobid]
      idList = self.db.getList(' '.join(SQL))
      return len(idList) > 0
         

   def find_job_events(self, jobid, events=None):
      
      if not self.job_exists(jobid):
         return None
      SQL = ["select job_prog.id jpid, name, entry_time, job_prog.job_data_id",
             "from job_events, job_data, job_prog",
             "where job_prog.job_data_id = job_data.id",
             "and job_events.id = job_prog.event_type", 
             "and jobid = %d" % jobid,
             "order by entry_time"]
      eventList = self.db.getDict(' '.join(SQL))

      if events == None:
         return eventList
      return [event for event in eventList if event['NAME'] in events] 

   def job_started(self, jobid):
      
      """Did this job run?  Returns bool value.  Returns None if 
      the job isn't found at all."""

      startEntry = self.find_job_events(jobid, ['starting'])
                                       
      if startEntry == None:
         return None
      elif startEntry == []:
         return (False, None, None)

      return (True,startEntry[0]['JPID'],startEntry[0]['ENTRY_TIME'])

   def job_created(self, jobid):
      
      createdEntry = self.find_job_events(jobid,['creating'])
      
      if createdEntry == None:
         return None
      elif createdEntry == []:
         #Yes, something has probably gone wrong in the database, or job was in queue 
         #when writer started.
         return (False, None, None)
      return (True, createdEntry[0]['JPID'],createdEntry[0]['ENTRY_TIME'])


   def get_total_time(self, jobid):
      
      """Gets total time for a job from database.
      Returns None if the job doesn't exist."""

      SQL = ["select job_prog.entry_time",
             "from job_prog, job_data",
             "where job_prog.job_data_id = job_data.id",
             "and job_data.jobid = %d" %(jobid),
             "order by entry_time"]

      timelist = self.db.getList(' '.join(SQL))
      start = int(db2util.ts.TStoSec(timelist[0]))
      end = int(db2util.ts.TStoSec(timelist[len(timelist) - 1]))
      return end - start



   def get_total_queued_time(self, jobid):
      
      """if the job ran, then get its time in the queue."""
      created, cJpid, cTime = self.job_created(jobid)
      started, sJpid, sTime = self.job_started(jobid)
      
      if not created:
         print "unable to get a creation time for jobid: %d"%jobid
         return None
      if not started:
         #print "Jobid: %d never started"
         #Look for a killing message.  This would be when it should be 
         #considered out of the queue.
         deleteRecord = self.find_job_events(jobid, 'killing')
         if deleteRecord != []:
            sTime = deleteRecord[0]['ENTRY_TIME']
         else:
            return None

      start = int(db2util.ts.TStoSec(cTime))
      end = int(db2util.ts.TStoSec(sTime))   

      return end - start

   def get_hold_times(self, jobid):
      
      """return the list of the times a job was in hold.
         returns zero if no holds exist.  Returns None
         if an error is encountered.  If a hold has not 
         released (deletion is considered a release)
         The list will have a None in it's last element if a final
         release condition could not be found."""

      hold_events = ['user_hold', 'admin_hold', 'dep_hold', 'maxrun_hold']
      release_events = [(event + '_release') for event in hold_events]
      clear_events = ['all_holds_clear']
      terminal_events = ['killing', 'job_epilogue_finished']
      run_start_events = ['starting']

      events_to_check = []
      events_to_check.extend(hold_events)
      events_to_check.extend(release_events)
      events_to_check.extend(clear_events)
      events_to_check.extend(run_start_events)
      
      
      eventList = self.find_job_events(jobid, events_to_check)
      
      hold_start_times = []
      hold_end_times = []
      holding = False

      for event in eventList:
         if not holding:
            if event['NAME'] in hold_events:
               #print event['NAME']
               hold_start_times.append(event['ENTRY_TIME'])
               holding = True
            if event['NAME'] in run_start_events:
               break
            if event['NAME'] in terminal_events:
               break
         else:
            if event['NAME'] in clear_events:
               #print "clear found"
               hold_end_times.append(event['ENTRY_TIME'])
               holding = False
            if event['NAME'] in terminal_events:
               hold_end_times.append(event['ENTRY_TIME'])
               holding = False
               break
      
      hold_start_times = [int(db2util.ts.TStoSec(time)) for time in hold_start_times]
      hold_end_times = [int(db2util.ts.TStoSec(time)) for time in hold_end_times]

      #print hold_start_times, hold_end_times
      if len(hold_start_times) == 0:
         return [0]
      if len(hold_start_times) == len(hold_end_times):
         return [sum((end,-start)) for start, end in zip(hold_start_times, hold_end_times)]
         
      elif len(hold_start_times) < len(hold_end_times):
         #wow something has gone wrong
         return None
      else:
         #print "Hold end < hold start"

         retList = [sum((end,-start)) 
                    for start, end in zip(hold_start_times, hold_end_times)]
         retList.append(None)
         return retList
                      
                            
      
   
class JobDepsData(AccessOnlyDAO):

   def search (self, record):
      
      """Find a dependency record and update it to show its success.
      None of these jobs are satisfied, so, only try and update if 
      something new comes in."""

      SQL = ("select id, dep_on_id, satisfied",
             "from job_deps",
             "where job_data_id = %d" % (record.v.JOB_DATA_ID),
             "and satisfied = 0")

      return self.db.getDict(' '.join(SQL))


class JobSummaryData(AccessOnlyDAO):
   
    def get_job_history(self, jobid):
      
      SQL = "select * from %s.%s where jobid = %d" % (self.table.schema, self.table.table, jobid)

      entryDicts = self.db.getDict(SQL)
      
      return [self.table.getRecord(entry) for entry in entryDicts]

    def get_job_ids_in_date_range(self, start = None, end = None):


        if start == None:
            pass
        elif end == None:
            pass
        else:
            SQL = [ "select unique(jobid)",
                    "from %s.job_summary" % self.table.schema, 
                    "where entry_time >= '%s'" % start,
                    "and entry_time <= '%s'" % end ]
        print " ".join(SQL)
        return [int(i) for i in self.db.getList(" ".join(SQL))]

    def find_event(self, jobid, event):
        
        pass
