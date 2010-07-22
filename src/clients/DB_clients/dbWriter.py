import db2util


#Class for handling database output
class DatabaseWriter(object):

   def __init__(self, dbName, username, password, schema):

      self.db = db2util.db()
      self.db.connect(dbName, username, password)
      self.schema = schema

      #Handle tables, There is probably a better way to do this.
      self.tables = {}
      self.tables['entry'] = db2util.table(self.db, schema, 'COBALT_ENTRY')
      self.tables['log_entry'] = db2util.table(self.db, schema, 'COBALT_LOG_ENTRY')
      self.tables['reservation_state'] = db2util.table(self.db, schema, 'COBALT_RESERVATION_STATE')
      
      self.daos = {}
      for key in self.tables.keys():
         if key == 'entry':
            self.daos[key] = EntryTableData(self.db, schema,
                                       self.tables[key].table)
         else:   
            self.daos[key] = db2util.dao(self.db, schema,
                                         self.tables[key].table)
      
      

   def addMessage(self, logMsg):

      if logMsg.item_type == 'reservation':
         self.__addResMsg(logMsg)
      
      return


   def __addResMsg(self, logMsg):

      #unpack reservation Message.
      #see if we already have an entry in COBALT_ENTRY table

      record = self.daos['entry'].table.getRecord()
      record.v.ENTRY_TYPE = logMsg.item_type
      record.v.COBALTID = logMsg.item.res_id
      match = self.daos['entry'].search(record)
      if not match:
         self.daos['entry'].insert(record)
      else:
         record.v.ID = match[0]['ID']

      #LOG_ENTRY
      log_entry_record = self.daos['log_entry'].table.getRecord({'ENTRY_ID':record.v.ID,
                                                                 'LOG_MESSAGE':logMsg.message,
                                                                 'EXEC_USER': logMsg.exec_id})
      log_entry_id = self.daos['log_entry'].insert(log_entry_record)

      
      #Add COBALT_RESERVATION_STATE

      res_entry_record = self.daos['reservation_state'].table.getRecord({'LOG_ENTRY_ID': log_entry_id,
                                                            'NAME':logMsg.item.name,
                                                            'CYCLE':int(logMsg.item.cycle),
                                                            'CREATED_QUEUE':int(logMsg.item.createdQueue),
                                                            'DURATION': logMsg.item.duration,
                                                            'PARTITIONS': logMsg.item.partitions,
                                                            'QUEUE': logMsg.item.queue,
                                                            'RES_USERS': logMsg.item.users,
                                                            'RUNNING': int(logMsg.item.running),
                                                            'START': logMsg.item.start})

      print logMsg.item
      res_entry_record.stdout()
      
      self.daos['reservation_state'].insert(res_entry_record)

      return

   def close(self):
      self.db.close()
      

class EntryTableData(db2util.dao):

   def search (self, record):

      """override for the dao's unimplemented search.  Looks to see if an
      entry already exists for a given record. We want the id, if it exists.
      if not then we get to insert a new set of messages.

      Return a list of dicts that correspond to record values"""

      SQL = "select id from cobalt_entry where entry_type = ? and cobaltid = ?"

      result = self.db.getDict(SQL, (record.v.ENTRY_TYPE, record.v.COBALTID))

      print "\n########################\n"
      print result
      print "\n########################\n"
      
      return result

   
