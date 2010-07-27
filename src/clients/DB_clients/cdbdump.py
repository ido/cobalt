#!/usr/bin/env python

'''Database Writer for Cobalt, a BG-job scheculer'''
__revision__ = '$Revision: 1'


#TODO:
# - Implement Reservation DB logging
# - Implement Partition DB logging
# - Implement Job DB logging
# - *** INPUT VALIDATION ***

# (Should I request retransmit?)

import os.path
import sys
import json
import ConfigParser

from dbWriter import DatabaseWriter
from cdbMessages import LogMessage, LogMessageDecoder


class PipeListener (object):

   def  __init__(self, fifoname):

       self.__openPipe(fifoname)

       return

   def __del__(self):

       self.__closePipe()
       return


   def __openPipe(self, fifoname):

       self.fifo = open(os.path.join(fifoname), 'r')
   
       return

   def __closePipe(self):

       self.fifo.close()

       return


   def readData(self):

       return self.fifo.readline()



__helpmsg__ = "Usage: cdbwriter [options] file"

if __name__ == '__main__':
    
    

    #Database Connection

#    database = db2util.db()
    
#    database.connect('COBALT_D', 'richp', 'Bo7[addy')
#    schema = 'RICHP'
    

#    tables = {}
#    tables['entry'] = db2util.table(database, schema, 'COBALT_ENTRY')
#    tables['log_entry'] = db2util.table(database, schema, 'COBALT_LOG_ENTRY')
#    tables['reservation_state'] = db2util.table(database, schema, 'COBALT_RESERVATION_STATE')
  
#    daos = {}
#    for key in tables.keys():
#        daos[key] = db2util.dao(database, schema, tables[key].table)
#        print daos[key].table.table + ' ' + daos[key].table.schema


    #insert dummy data:

   # records = {}
   # records['entry'] = daos['entry'].table.getRecord()
   # print records['entry']

   # records['entry'].v.ENTRY_TYPE = 'reservation'
   # records['entry'].v.COBALTID = 1

   # daos['entry'].insert(records['entry'])

    
#    database.close()


    con_file = ConfigParser.ConfigParser()
    con_file.read(os.path.join("DB_writer_config"))

    fifo_name = con_file.get('cdbdump', 'fifo')
    login = con_file.get('cdbdump', 'login')
    pwd = con_file.get('cdbdump', 'pwd')
    database = con_file.get('cdbdump', 'database')
    schema = con_file.get('cdbdump', 'schema')

    database = DatabaseWriter(database, login, pwd, schema)
    
    #starting listener.  This may become more sophistocated later

    pipe = PipeListener(fifo_name)


    LogMsgDecoder = LogMessageDecoder()
    print "Begin database logging."
    while(True):
        #loop forever
        
        #listen on the pipe
        cobaltJSONmessage = pipe.readData()
        
        if cobaltJSONmessage != "":
            print cobaltJSONmessage
            logMsg =  LogMsgDecoder.decode(cobaltJSONmessage)
            
            #Add to Database

            print logMsg
            database.addMessage(logMsg)
            print "Message Added to DB!"
            

        #Wash. Rinse. Repeat
