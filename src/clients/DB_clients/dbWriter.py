import db2util


#Class for handling database output
class DatabaseWriter(object):

   def __init__(self, dbName, username, password, schema):

      self.db = db2util.db()
      self.db.connect(dbName, username, password)
      self.schema = schema

      table_names = ['RESERVATION_DATA', 'RESERVATION_PARTS',
                     'RESERVATION_STATES', 'RESERVATION_USERS',
                     'RESERVATION_PROG', 'JOB_DATA', 'JOB_ATTR',
                     'JOB_NODECTS', 'JOB_DEPS', 'JOB_STATES',
                     'JOB_PROG']

      #Handle tables, There is probably a better way to do this.
      self.tables = {}
      self.daos = {}
      for table_name in table_names:
         print "Accessing table: %s" % table_name
         self.tables[table_name] = db2util.table(self.db, schema, table_name)
         #I am so going to need new and exciting daos.
         if table_name in ['RESERVATION_STATES', 'JOB_STATES']:
            self.daos[table_name] = StateTableData(self.db, schema, 
                                             self.tables[table_name].table)
         elif table_name == 'RESERVATION_DATA':
            self.daos[table_name] = ResDataData(self.db, schema, 
                                                self.tables[table_name].table)
            
         elif table_name == 'JOB_DATA':
            self.daos[table_name] = JobDataData(self.db, schema, 
                                                self.tables[table_name].table)

         else:
            self.daos[table_name] = db2util.dao(self.db, schema, 
                                             self.tables[table_name].table)
      

      #we opened with a schema, let's make that the default for now.
      self.db.prepExec("set current schema %s" % schema)
      
   def addMessage(self, logMsg):

      if logMsg.item_type == 'reservation':
         if logMsg.state == 'created':
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

            
      reservation_state_record = self.daos['RESERVATION_STATES'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['RESERVATION_STATES'].search(reservation_state_record)
      if not match:
         self.daos['RESERVATION_STATES'].insert(reservation_state_record)
      else:
         reservation_state_record.v.ID = match[0]['ID']
         
         

      reservation_prog_record = self.daos['RESERVATION_PROG'].table.getRecord({
            'ENTRY_TIME': logMsg.timestamp,
            'STATE':reservation_state_record.v.ID,
            'EXEC_USER': logMsg.exec_user,
            'RES_DATA_ID' : res_data_id
            })
      
      self.daos['RESERVATION_PROG'].insert(reservation_prog_record)


      return
     
   def __modifyResMsg(self, logMsg):
   
      #get state.  No matter what we need this.
      reservation_state_record = self.daos['RESERVATION_STATES'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['RESERVATION_STATES'].search(reservation_state_record)
      if not match:
         self.daos['RESERVATION_STATES'].insert(reservation_state_record)
      else:
         reservation_state_record.v.ID = match[0]['ID']
         
         
      res_id = self.__get_most_recent_data_id('RESERVATION_DATA', logMsg)      
 
      if ((not res_id) or 
          ((logMsg.state == 'modified') or 
           (logMsg.state == 'cycled'))): 
         
         #we've gone from modify to add.
         self.__addResMsg(logMsg)
         return
     
      
      else: #attach a new reservation_progress entry to an extant 
            #reservation_data entry
         
         #this had better be here.  If there are no records, cobalt hasn't caught on that
         #its modifying nothing yet.  TODO: Add message if not found.
            
         
         reservation_prog_record = self.daos['RESERVATION_PROG'].table.getRecord({
               'RES_DATA_ID' : res_id,
               'STATE' : reservation_state_record.v.ID,
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

      specialObjects = {}

      for key in logMsg.item.__dict__:
         print "adding %s value %s" %( key, logMsg.item.__dict__[key])
         if key in ['nodects', 'attrs', 'all_dependencies', 
                    'satisfied_dependencies', 'job_prog_msg']:
            specialObjects[key] = logMsg.item.__dict__[key]
         else:
            job_data_record.v.__setattr__(key.upper(),
                                   logMsg.item.__dict__[key])

      job_data_id = self.daos['JOB_DATA'].insert(job_data_record)
      
      #populate job_attrs, if needed.
      for key in specialObjects['attrs'].keys():
         job_attr_record = self.daos['JOB_ATTR'].table.getRecord({
               'JOB_DATA_ID' : job_data_id,
               'KEY' : key,
               'VALUE' : str(specialObjects['attrs'][key])})
         self.daos['JOB_ATTR'].insert(job_attr_record)
      
      #populate job_nodects, if needed.
      for nodect in specialObjects['nodects']:
         job_nodects_record = self.daos['JOB_NODECTS'].table.getRecord({
            'JOB_DATA_ID': job_data_id,
            'VALUE': nodect})
         self.daos['JOB_NODECTS'].insert(job_nodects_record)
         

      #populate job_deps
      for dep in specialObjects['satisfied_dependencies']:
         job_deps_record = self.daos['JOB_DEPS'].table.getRecord({
               'JOB_DATA_ID' : job_data_id,
               'DEP_ON_ID' : dep,
               'SATISFIED' : 0})
         self.daos['JOB_DEPS'].insert(job_deps_record)


      self.__addJobProgMsg(logMsg, logMsg.item.job_prog_msg, job_data_id)


      
   def __addJobProgMsg(self, logMsg, job_prog_msg, job_data_id=None):

      """Set the frequently changing data of a job.  Several
         of these records are likely to be created during a
         single job's run."""
   
      print job_prog_msg
      #this is always a part of an incoming job message.
      #may have to update some other fields as run progresses in job_data
      job_state_record = self.daos['JOB_STATES'].table.getRecord({'NAME': logMsg.state})
      match = self.daos['JOB_STATES'].search(job_state_record)
      if not match:
         self.daos['JOB_STATES'].insert(job_state_record)
      else:
         job_state_record.v.ID = match[0]['ID']

      if job_data_id == None:
         job_data_record = self.daos['JOB_DATA'].table.getRecord()
         job_data_record.v.JOBID = job_prog_msg.jobid
         ids = self.daos['JOB_DATA'].search_most_recent(job_data_record)
         
         if not ids:
            pass #we have something severely wrong here.
         job_data_id = ids[0].get('ID', None)


      updateAtRun = {}
      job_prog_record = self.daos['JOB_PROG'].table.getRecord()
      for fieldName in job_prog_msg.__dict__.keys():
         if fieldName in ['env', 'nodects', 'location',
                          'priority_core_hours','satisfied_dependencies']:
            updateAtRun[fieldName] = job_prog_msg.__getattribute__(fieldName)
         else:
            if fieldName not in ['jobid']:
               job_prog_record.v.__setattr__(fieldName.upper(), 
                                             job_prog_msg.__getattribute__(fieldName))
         
      job_prog_record.v.REASON = job_state_record.v.ID
      job_prog_record.v.JOB_DATA_ID = job_data_id

      job_prog_record.v.EXEC_USER = logMsg.exec_user
      job_prog_record.v.ENTRY_TIME = logMsg.timestamp

      
      self.daos['JOB_PROG'].insert(job_prog_record)
      
      #These are updated in JOB_DATA at run-start.
     # if len(updateAtRun) > 0:
      #   fieldValue = updateAtRun.pop('env', None)
       #  if fieldValue:
            
            
      


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

   def search_most_recent (self, record):

      """Find the most recent version of a reservation data entry."""

      SQL = ("select job_data.id" ,
             "from job_prog, job_data",
             "where job_data.id = job_prog.job_data_id",
             "and job_data.jobid = %d" % record.v.JOBID,
             "order by entry_time DESC") 
      
      return self.db.getDict(' '.join(SQL))
   
   def search (self, record):
      
      SQL = "select ID from %s.%s where job_data_id = %s" % (self.table.schema, 
                                                        self.table.table,
                                                        record.v.JOB_DATA_ID)
      return self.db.getDict(SQL)


class JobDepsData(db2util.dao):

   def search (self, record):
      
      """Find a dependency record and update it to show its success."""

      SQL = ("select id",
             "from job_deps",
             "where job_data_id = %d and dep_on_id = %d" % (record.v.JOB_DATA_ID,
                                                            record.v.DEP_ON_ID))
      return self.db.getDict(' '.join(SQL))
