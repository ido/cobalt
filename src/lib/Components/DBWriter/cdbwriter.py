import db2util
import xmlrpclib
import os, sys
import logging
import ConfigParser
import threading
import traceback

import Cobalt.Logging, Cobalt.Util
from Cobalt.Statistics import Statistics
from Cobalt.Components.DBWriter.cdbMessages import LogMessage, LogMessageDecoder
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Proxy import ComponentProxy


__revision__ = '$Revision: 1$'

logger = logging.getLogger("Cobalt.Components.cdbwriter")
config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('cdbwriter'):
   logger.error('"cdbwriter" section missing from config file.')
   sys.exit(1)

def get_cdbwriter_config(option, default):
   try:
      value = config.get('cdbwriter', option)
   except ConfigParser.NoOptionError:
      value = default
   return value


class MessageQueue(Component):
   
   name = "cdbwriter"
   implementation = "cdbwriter"
   logger = logging.getLogger("Cobalt.Components.cdbwriter")

   _configfields = ['user', 'pwd', 'database', 'schema']
   _config = ConfigParser.ConfigParser()
   _config.read(Cobalt.CONFIG_FILES)
   if not config._sections.has_key('cdbwriter'):
      logger.error('"cdbwriter" section missing from config file.')
   config = _config._sections['cdbwriter']
   mfields = [field for field in _configfields if not config.has_key(field)]
   if mfields:
      logger.error("Missing option(s) in cobalt config file [cdbwriter] section: %s" % (" ".join(mfields)))
      sys.exit(1)
      
      
   def __init__(self, *args, **kwargs):
      Component.__init__(self, *args, **kwargs)
      self.sync_state = Cobalt.Util.FailureMode("Foreign Data Sync")
      self.connected = False
      self.msg_queue = []
      self.lock = threading.Lock()
      self.statistics = Statistics()
      self.decoder = LogMessageDecoder()
      

   def __setstate__(self, state):
      self.msg_queue = state['msg_queue']
      self.connected = False
      self.lock = threading.Lock()
      self.statistics = Statistics()
      self.decoder = LogMessageDecoder()

   def __getstate__(self):
      return {'msg_queue': self.msg_queue}
     
             
   def init_database_connection(self):
      user = get_cdbwriter_config('user', None)
      pwd =  get_cdbwriter_config('pwd', None)
      database =  get_cdbwriter_config('database', None)
      schema =  get_cdbwriter_config('schema', None)
      
      try:
         self.database_writer = DatabaseWriter(database, user, pwd, schema)
      except:
         #make this a log statement
         logging.error("Unable to connect to %s as %s" % (database, user))
         self.connected = False
         logging.debug(traceback.format_exc())
      else:
         self.connected = True

   def iterate(self):
      """Go through the messages that are sitting on the queue and
      load them into the database."""
      
      #if we're not connected, try to reconnect to the database
      if not self.connected:
         logger.debug("Attempting reconnection.")
         self.init_database_connection()
      
      while self.msg_queue and self.connected:
         msg = self.msg_queue[0]
            
         try:
            self.database_writer.addMessage(msg)
         except db2util.adapterError:
            logger.error ("Error updating databse.  Unable to add message.")
            logging.debug(traceback.format_exc())
            self.msg_queue.pop(0)
         except:
            logger.error ("Error updating databse.  Unable to add message.")
            logging.debug(traceback.format_exc())
            self.connected = False
            break
         else:
            #message added
            self.msg_queue.pop(0)


   iterate = automatic(iterate)


   def add_message(self, msg):
     
      msgDict = None
      try:
         msgDict = self.decoder.decode(msg)
      except ValueError:
         logger.error("Bad message recieved.  Failed to decode string %s" % msg)
         return
      except:
         logging.debug(traceback.format_exc())
      self.msg_queue.append(msgDict) 
      

   add_message = exposed(add_message)
   
   
   def save_me(self):
      Component.save(self)
   save_me = automatic(save_me)

#TODO: Make this follow Cobalt xmlrpc conventions and work like a component
#in general.


#Class for handling database output
class DatabaseWriter(object):

   def __init__(self, dbName, username, password, schema):

      self.db = db2util.db()
      
      try:
         self.db.connect(dbName, username, password)
      except:
         logger.error("Failed to open a connection to database %s as user %s" %(dbName, username))
         raise

      self.schema = schema

      table_names = ['RESERVATION_DATA', 'RESERVATION_PARTS',
                     'RESERVATION_EVENTS', 'RESERVATION_USERS',
                     'RESERVATION_PROG', 'JOB_DATA', 'JOB_ATTR',
                     'JOB_DEPS', 'JOB_EVENTS','JOB_COBALT_STATES', 'JOB_PROG']

      #Handle tables, There is probably a better way to do this.
      self.tables = {}
      self.daos = {}
      try:
         for table_name in table_names:
            logger.info("Accessing table: %s" % table_name)
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
            else:
               self.daos[table_name] = db2util.dao(self.db, schema, 
                                                   self.tables[table_name].table)
      except:
         logger.error("Error accessing table %s!" % table_name)
         self.db.close()
         raise
         
      
      #we opened with a schema, let's make that the default for now.
      self.db.prepExec("set current schema %s" % schema)
      
   def addMessage(self, logMsg):

      logger.info("Inserting Data message of type: %s.%s " % (logMsg.item_type, logMsg.state))

      if logMsg.item_type == 'reservation':
         if logMsg.state == 'creating':
            self.__addResMsg(logMsg)
         else:
            self.__modifyResMsg(logMsg)
      #elif logMsg.item_type == 'partition':
       #  print "Not yet implemented."
      elif logMsg.item_type == 'job_prog':
         self.__addJobProgMsg(logMsg, logMsg.item)
      elif logMsg.item_type == 'job_data':
         #modifying and creating messages are handled
         #a bit differently 
         self.__addJobDataMsg(logMsg)


      #else something has gone screw-ball.
      else:
         raise RuntimeError("Support for %s type of message not implemented." % logMsg.item_type)
      return


   def __addResMsg(self, logMsg):

      """Unpack a Reservation Message when a Reservation is created."""


      res_data_record = self.daos['RESERVATION_DATA'].table.getRecord({
         'CYCLE': int(logMsg.item.cycle),
         'CYCLEID': logMsg.item.cycle_id,
         'DURATION': logMsg.item.duration,
         'NAME':logMsg.item.name,
         'QUEUE': logMsg.item.queue,
         'RESID': logMsg.item.res_id,
         'START': logMsg.item.start
         })
      
      res_data_id = 1
      res_data_id = self.daos['RESERVATION_DATA'].insert(res_data_record)
      
      part_list = logMsg.item.partitions.split(':')
      
      if part_list[0] != '':
         for partition in part_list:
            res_partitions_record = self.daos['RESERVATION_PARTS'].table.getRecord({
               'RES_DATA_ID': res_data_id,
               'NAME': partition
               })
            self.daos['RESERVATION_PARTS'].insert(res_partitions_record)
      

      if logMsg.item.users:
         user_list = logMsg.item.users.split(':')

         if user_list[0] != '':
            for user in user_list:
               res_users_record = self.daos['RESERVATION_USERS'].table.getRecord({
                     'RES_DATA_ID': res_data_id,
                     'NAME': user #eventually a FK into users from cbank?
                     }) 
               self.daos['RESERVATION_USERS'].insert(res_users_record)

            
      reservation_event_record = self.daos['RESERVATION_EVENTS'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['RESERVATION_EVENTS'].search(reservation_event_record)
      if not match:
         logger.warning("Received message with a nonexistent event for resid %s.  Event was: %s" %
                        (logMsg.item.res_id, logMsg.state))
      else:
         reservation_event_record.v.ID = match[0]['ID']
         
         

      reservation_prog_record = self.daos['RESERVATION_PROG'].table.getRecord({
            'ENTRY_TIME': logMsg.timestamp,
            'EVENT_TYPE':reservation_event_record.v.ID,
            'EXEC_USER': logMsg.exec_user,
            'RES_DATA_ID' : res_data_id
            })
      
      self.daos['RESERVATION_PROG'].insert(reservation_prog_record)


      return
     
   def __modifyResMsg(self, logMsg):
   
      #get state.  No matter what we need this.
      reservation_event_record = self.daos['RESERVATION_EVENTS'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['RESERVATION_EVENTS'].search(reservation_event_record)
      if not match:
         logger.warning("Received message with a nonexistent event for resid %s.  Event was: %s" %
                        (logMsg.item.res_id, logMsg.state))
      else:
         reservation_event_record.v.ID = match[0]['ID']
         
         
      res_id = self.__get_most_recent_data_id('RESERVATION_DATA', logMsg)      
 
      if ((not res_id) or 
          ((logMsg.state == 'modifying') or 
           (logMsg.state == 'cycling'))): 
         
         #we've gone from modify to add.
         self.__addResMsg(logMsg)
         return
     
      
      else: #attach a new reservation_progress entry to an extant 
            #reservation_data entry
         
         #this had better be here.  If there are no records, cobalt hasn't caught on that
         #its modifying nothing yet.  TODO: Add message if not found.
            
         
         reservation_prog_record = self.daos['RESERVATION_PROG'].table.getRecord({
               'RES_DATA_ID' : res_id,
               'EVENT_TYPE' : reservation_event_record.v.ID,
               'ENTRY_TIME' : logMsg.timestamp,
               'EXEC_USER' : logMsg.exec_user
               })
         self.daos['RESERVATION_PROG'].insert(reservation_prog_record)


   def __addJobDataMsg(self, logMsg):

      """We have to create the "data" objects for a job.
         These are supposed to be relatively static through
         job's lifetime and the data set here should not be
         changed during normal execution."""
      #create the job_data entry.  
      #This will be modified as the job goes through its life, 
      #where some null fields will have values added, such as on
      #execution.
      job_data_record = self.daos['JOB_DATA'].table.getRecord()

      #if we have a "dummy" object, and we get a message that
      #indicates job creation, replace the dummy.
      updateDummy = False
      if logMsg.state == "creating":
         possible_record = self.daos['JOB_DATA'].find_dummy(logMsg.item.jobid)
         if possible_record: 
            job_data_record = possible_record
            updateDummy  = True

      specialObjects = {}
      

      for key in logMsg.item.__dict__:
         #print "adding %s value %s" %( key, logMsg.item.__dict__[key])
         if key in ['nodects', 'attrs', 'all_dependencies', 
                    'satisfied_dependencies', 'job_prog_msg']:
            specialObjects[key] = logMsg.item.__dict__[key]
         else:
            job_data_record.v.__setattr__(key.upper(),
                                   logMsg.item.__dict__[key])
      job_data_record.v.ISDUMMY = 0
      
      job_data_id = job_data_record.v.ID
      if updateDummy:
         jod_data_id = self.daos['JOB_DATA'].update(job_data_record)
      else:
         job_data_id = self.daos['JOB_DATA'].insert(job_data_record)
      
      #populate job_attrs, if needed.
      for key in specialObjects['attrs'].keys():
         job_attr_record = self.daos['JOB_ATTR'].table.getRecord({
               'JOB_DATA_ID' : job_data_id,
               'KEY' : key,
               'VALUE' : str(specialObjects['attrs'][key])})
         self.daos['JOB_ATTR'].insert(job_attr_record)
      

      #populate job_deps
      for dep in specialObjects['all_dependencies']:
         job_deps_record = self.daos['JOB_DEPS'].table.getRecord({
               'JOB_DATA_ID' : job_data_id,
               'DEP_ON_ID' : int(dep),
               'SATISFIED' : 0})
         self.daos['JOB_DEPS'].insert(job_deps_record)


      self.__addJobProgMsg(logMsg, logMsg.item.job_prog_msg, job_data_id)


      
   def __addJobProgMsg(self, logMsg, job_prog_msg, job_data_id=None):

      """Set the frequently changing data of a job.  Several
         of these records are likely to be created during a
         single job's run."""
   
      #this is always a part of an incoming job message.
      #may have to update some other fields as run progresses in job_data

      if job_data_id == None:
         job_data_id = self.get_job_data_ids_from_jobid(job_prog_msg.jobid)      

      job_event_record = self.daos['JOB_EVENTS'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['JOB_EVENTS'].search(job_event_record)
      if not match:
         logger.warning("Received message with a nonexistent event for jobid %s.  Event was: %s" %
                        (job_data_id, logMsg.state))
      else:
         job_event_record.v.ID = match[0]['ID']

      

      job_cobalt_states_record = self.daos['JOB_COBALT_STATES'].table.getRecord({'NAME': job_prog_msg.cobalt_state})
      match = self.daos['JOB_COBALT_STATES'].search(job_cobalt_states_record)
      if not match:
         logger.warning("Received message with a nonexistent cobalt state for jobid %s.  Event was: %s" %
                        (job_data_id, job_prog_msg.cobalt_state))
      else:
         job_cobalt_states_record.v.ID = match[0]['ID']



      updateAtRun = {}
      job_prog_record = self.daos['JOB_PROG'].table.getRecord()
      for fieldName in job_prog_msg.__dict__.keys():
         if fieldName in ['envs', 'location',
                          'priority_core_hours','satisfied_dependencies']:
            updateAtRun[fieldName] = job_prog_msg.__getattribute__(fieldName)
         else:
            if fieldName not in ['jobid', 'cobalt_state']:
               job_prog_record.v.__setattr__(fieldName.upper(), 
                                             job_prog_msg.__getattribute__(fieldName))
         
      job_prog_record.v.EVENT_TYPE = job_event_record.v.ID
      job_prog_record.v.COBALT_STATE = job_cobalt_states_record.v.ID
      job_prog_record.v.JOB_DATA_ID = job_data_id

      job_prog_record.v.EXEC_USER = logMsg.exec_user
      job_prog_record.v.ENTRY_TIME = logMsg.timestamp

      self.daos['JOB_PROG'].insert(job_prog_record)
      
      job_data_record = None
      job_data_record = self.daos['JOB_DATA'].getID(job_data_id)
      #These are updated in JOB_DATA at run-start.
      if len(updateAtRun) > 0:
         fieldValue = updateAtRun.pop('envs', None)
         if fieldValue:
            job_data_record.v.ENVS = str(fieldValue)
         fieldValue = updateAtRun.pop('priority_core_hours', None)
         if fieldValue:
            job_data_record.v.PRIORITY_CORE_HOURS = int(fieldValue)
         fieldValue = updateAtRun.pop('location', None)
         if fieldValue:
            job_data_record.v.LOCATION = str(fieldValue)
         fieldValue = updateAtRun.pop('satisfied_dependencies', None)
         
         #find dependencies that have been satisfied and mark as such.
         #I really don't like how I am doing this.  I have a feeling
         #I can consolidate this.  
         if fieldValue:
            job_deps_record = self.daos['JOB_DEPS'].table.getRecord({'JOB_DATA_ID': job_data_id})
            deps_to_satisfy = self.daos['JOB_DEPS'].search(job_deps_record)
            job_deps_record = None
            
            for dep in deps_to_satisfy:
               if str(dep['DEP_ON_ID']) in fieldValue:
                  job_deps_record = self.daos['JOB_DEPS'].getID(dep['ID'])
                  job_deps_record.v.SATISFIED = 1
                  self.daos['JOB_DEPS'].update(job_deps_record)
                  job_deps_record = None
               
               
         #fieldValue = updateAtRun.pop('nodects', None)

         self.daos['JOB_DATA'].update(job_data_record)

   def get_job_data_ids_from_jobid(self, jobid):
      job_data_record = self.daos['JOB_DATA'].table.getRecord()
      job_data_record.v.JOBID = jobid
      ids = self.daos['JOB_DATA'].search_most_recent(job_data_record)
      
      if not ids:
         #For one reason or another we do not have job_data object
         #to tie to.  Create a "dmmy" one for now. This will contain
         #only the jobid and placeholders that indicate this is a dummy. 
         #Integer values of -1, strings of COBALT_DUMMY should be a good
         #start.

         for field in job_data_record.m.__dict__:

            if field in ['isfield']:
               continue
            if job_data_record.m.__dict__[field].nullallowed:
               #Null is the ultimate dummy data.
               pass
            
            else:
              if field == 'ID':
                 pass #gets set on insert
              elif field == 'ISDUMMY':
                 job_data_record.v.ISDUMMY = 1
              elif db2util.dbtype.typeMap[job_data_record.m.__dict__[field].datatype] in [ 'SMALLINT', 'INTEGER',
                                                                                   'BIGINT','DECIMAL'
                                                                                   'REAL', 'DOUBLE']:
                 job_data_record.v.__dict__[field] = int(0)
              elif db2util.dbtype.typeMap[job_data_record.m.__dict__[field].datatype] in ['TIMESTAMP']:
                 job_data_record.v.__dict__[field] = '1970-01-01-00.00.00'
              else:
                 job_data_record.v.__dict__[field] = 'COBALT_DUMMY'[0:job_data_record.m.__dict__[field].maxlen]
                 
         
         job_data_record.v.JOBID = jobid
         
         return self.daos['JOB_DATA'].insert(job_data_record)

      else:   
         return ids[0].get('ID', None)

      
      return None

   def __get_most_recent_data_id(self, table, logMsg):
      """Takes a table name and ID.  Right now reservation specific.
         Returns an id if one found, if not returns None.
         Will expand to other record types as they are implemented.
         Meant to extract ids from x_DATA records."""

      #TODO: make RES_ID generic.
      data_record = self.daos[table].table.getRecord({
            'RESID': logMsg.item.res_id})
      res_ids = self.daos[table].search_most_recent(data_record)
      
      if not res_ids:
         return None
      
      return res_ids[0].get('ID', None)

   
   def close(self):
      self.db.close()
      
   
   
class StateTableData(db2util.dao):
   
   def getStatesDict(self):
      SQL = "select * from %s.%s" % (self.table.schema, self.table.table)
      
      result_list = self.db.getDict(SQL)
      
      ret_dict = {}
      for item in result_list:
         ret_dict[item['NAME']] = item['ID']

      return ret_dict

   def search (self, record):
      """look up the id for a given state-change identifier.  
      This had better be in this table."""

      SQL = "select ID from %s.%s where NAME = '%s'" % (self.table.schema, self.table.table, record.v.NAME)
      
      return self.db.getDict(SQL)
      

class ResDataData(db2util.dao):

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



class JobDataData(db2util.dao):


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
        
      SQL = ("select job_prog.id jpid, job_data.id jdid, job_states.name " ,
             "from job_prog, job_data, job_states",
             "where job_data.id = job_prog.job_data_id",
             "and job_prog.reason = job_states.id",
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


      
class JobProgData(db2util.dao):

   """helpers for getting at job progress data"""
   
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



      
class JobDepsData(db2util.dao):

   def search (self, record):
      
      """Find a dependency record and update it to show its success.
      None of these jobs are satisfied, so, only try and update if 
      something new comes in."""

      SQL = ("select id, dep_on_id, satisfied",
             "from job_deps",
             "where job_data_id = %d" % (record.v.JOB_DATA_ID),
             "and satisfied = 0")

      return self.db.getDict(' '.join(SQL))
