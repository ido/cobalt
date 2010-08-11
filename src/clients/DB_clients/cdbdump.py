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
import time
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



__helpmsg__ = """Usage: cdbdump.py"""

if __name__ == '__main__':
    

    con_file = ConfigParser.ConfigParser()
    con_file.read(os.path.join("/Users/paulrich/cobalt-dev/src/clients/DB_clients/DB_writer_config"))

    fifo_name = con_file.get('cdbdump', 'fifo')
    login = con_file.get('cdbdump', 'login')
    pwd = con_file.get('cdbdump', 'pwd')
    database = con_file.get('cdbdump', 'database')
    schema = con_file.get('cdbdump', 'schema')

    database = DatabaseWriter(database, login, pwd, schema)
    
    #starting listener.  This may become more sophistocated later

   # try:
    pipe = PipeListener(fifo_name)
   # except:
       

    LogMsgDecoder = LogMessageDecoder()
    print "Begin database logging."
    while(True):
        
        cobaltJSONmessage = pipe.readData()
        
        if cobaltJSONmessage != '':
            logMsg =  LogMsgDecoder.decode(cobaltJSONmessage)
            database.addMessage(logMsg)
        else:
           time.sleep(5)

        #Wash. Rinse. Repeat
