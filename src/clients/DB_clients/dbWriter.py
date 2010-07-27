import db2util


#Class for handling database output
class DatabaseWriter(object):

   def __init__(self, dbName, username, password, schema):

      self.db = db2util.db()
      self.db.connect(dbName, username, password)
      self.schema = schema

      table_names = ['RESERVATION_DATA', 'RESERVATION_PARTS',
                  'RESERVATION_STATES', 'RESERVATION_USERS',
                  'RESERVATION_PROG']
      #Handle tables, There is probably a better way to do this.
      self.tables = {}
      self.daos = {}
      for table_name in table_names:
         print "Accessing table: %s" % table_name
         self.tables[table_name] = db2util.table(self.db, schema, table_name)
         #I am so going to need new and exciting daos.
         if table_name == 'RESERVATION_STATES':
            self.daos[table_name] = ResStateData(self.db, schema, 
                                             self.tables[table_name].table)
         elif table_name == 'RESERVATION_DATA':
            self.daos[table_name] = ResDataData(self.db, schema, 
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
      elif logMsg.item_type == 'partition':
         print "Not yet implemented."
      elif logMsg.item_type == 'job':
         print "Not yet implemented."
      #else something has gone screw-ball.

      return


   def __addResMsg(self, logMsg):

      """Unpack a Reservation Message when a Reservation is created."""


      res_data_record = self.daos['RESERVATION_DATA'].table.getRecord({
         'CYCLE': int(logMsg.item.cycle),
         'CYCLE_ID': logMsg.item.cycle_id,
         'DURATION': logMsg.item.duration,
         'NAME':logMsg.item.name,
         'QUEUE': logMsg.item.queue,
         'RES_ID': logMsg.item.res_id,
         'START': logMsg.item.start
         })
      
      res_data_id = 1
      res_data_id = self.daos['RESERVATION_DATA'].insert(res_data_record)
      
      part_list = []
      user_list = []
      
      (part,sep,tail) = logMsg.item.partitions.partition(':')
      part_list.append(part)

      while tail:
         part_list.add(part)
         (part,sep,tail) = logMsg.item.partitions.partition(':')

      (part,sep,tail) = logMsg.item.users.partition(':')
      user_list.append(part)

      while tail:
         user_list.add(part)
         (part,sep,tail) = logMsg.item.users.partition(':')

      if part_list:
         for partition in part_list:
            res_partitions_record = self.daos['RESERVATION_PARTS'].table.getRecord({
               'RES_ID': res_data_id,
               'NAME': partition
               })
            self.daos['RESERVATION_PARTS'].insert(res_partitions_record)
      
      if user_list:
         for user in user_list:
            res_users_record = self.daos['RESERVATION_USERS'].table.getRecord({
               'RES_ID': res_data_id,
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
            'RES_ID' : res_data_id
            })
      
      self.daos['RESERVATION_PROG'].insert(reservation_prog_record)


      return
     
   def __modifyResMsg(self, logMsg):
      print "This is a work in progress!"
   
      
      if logMsg.state == 'modified' or logMsg.state == 'cycled': #Most of a reservation can change, duplicate as much data as possible in advance
         print "Modification caught!"
      else: #the signifigantly easier case of a system message or deletion.
         
         #this had better be here.  If there are no records, cobalt hasn't caught 
         #its modifying nothing yet.
         reservation_data_record = self.daos['RESERVATION_DATA'].table.getRecord({
               'RES_ID': logMsg.item.res_id})
         res_ids = self.daos['RESERVATION_DATA'].search_most_recent(reservation_data_record)

         print res_ids
         
         #get state.  Move this up since it will be needed in all cases!
         reservation_state_record = self.daos['RESERVATION_STATES'].table.getRecord({'NAME': logMsg.state})
         match = self.daos['RESERVATION_STATES'].search(reservation_state_record)
         if not match:
            self.daos['RESERVATION_STATES'].insert(reservation_state_record)
         else:
            reservation_state_record.v.ID = match[0]['ID']
         
         reservation_prog_record = self.daos['RESERVATION_PROG'].table.getRecord({
               'RES_ID' : res_ids[0]['ID'],
               'STATE' : reservation_state_record.v.ID,
               'ENTRY_TIME' : logMsg.timestamp,
               'EXEC_USER' : logMsg.exec_user
               })
         self.daos['RESERVATION_PROG'].insert(reservation_prog_record)

   def close(self):
      self.db.close()
      

   
class ResStateData(db2util.dao):
   
   def search (self, record):
      """look up the id for a given state-change identifier.  
      This had better be in this table."""

      SQL = "select ID from %s.%s where NAME = '%s'" % (self.table.schema, self.table.table, record.v.NAME)
      
      return self.db.getDict(SQL)
      

class ResDataData(db2util.dao):
   def search_most_recent (self, record):
      print record.v.RES_ID
      SQL = "select reservation_data.id from reservation_prog, reservation_data where reservation_data.id = reservation_prog.res_id and reservation_data.res_id = %d order by entry_time DESC" %record.v.RES_ID
      
      return self.db.getDict(SQL)
   
   def search (self, record):
      
      SQL = "select ID from %s.%s where res_id = %s" % (self.table.schema, 
                                                        self.table.table,
                                                        record.v.RES_ID)
      return self.db.getDict(SQL)



#class ResProgData(db2util.dao):

#   def search_most_recent (self, record):
#      SQL = ("select RESERVATION_DATA.ID ",
#             "from reservation_data, reservation_prog ",
#             "where reservation_data.id = reservation_prog.res_id",
#             " and reservation_prog.RES_ID = %d " % record.v.RES_ID, 
#             " order by entry_time DESC")
#      
#      return self.db.getDict(''.join(SQL))
