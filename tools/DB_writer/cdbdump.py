#!/usr/bin/env python

'''Database Writer for Cobalt, a BG-job scheculer'''
__revision__ = '$Revision: 1'


#TODO:

# - Implement Partition DB logging

# - *** INPUT VALIDATION ***

# - "Recovery mode": read from a file before handling what is 
#    in the pipe.


# (Should I request retransmit?)

import os.path
import sys
import json
import time
import ConfigParser
import optparse

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


def parse_options():
   
   opt_parser = optparse.OptionParser()

   opt_parser.add_option('-r', '--recovery_file', action='store', 
                         dest='recovery_file')

   opt_parser.set_defaults(recovery_file=None)

   return opt_parser.parse_args()


__helpmsg__ = """Usage: cdbdump.py"""

if __name__ == '__main__':
   
   #Configuration file handling
   con_file = ConfigParser.ConfigParser()
   con_file.read(os.path.join("/Users/paulrich/cobalt-dev/tools/DB_writer/DB_writer_config"))

   fifo_name = con_file.get('cdbdump', 'fifo')
   login = con_file.get('cdbdump', 'login')
   pwd = con_file.get('cdbdump', 'pwd')
   database = con_file.get('cdbdump', 'database')
   schema = con_file.get('cdbdump', 'schema')
   
   #Command line options.  If conflict with config, these win.
   opts, args = parse_options()


   database = DatabaseWriter(database, login, pwd, schema)

   LogMsgDecoder = LogMessageDecoder()

   #recovery handling.
   if opts.recovery_file:
      try:
         f = open(os.path.join(opts.recovery_file), "r")
      except IOError as e:
         database.close()
         print "Error openting file: %s.\n  Caught Exception: %s!\n" % (opts.recovery_file, e)
      else:   
         cobalt_msgs = []
         for line in f.readlines():
            cobalt_msgs.append(LogMsgDecoder.decode(line))
            
            f.close()
            
            cobalt_msgs.sort()
            
         for msg in cobalt_msgs:
            database.addMessage(msg)

   
   
   #starting listener.  This may become more sophistocated later
   
   # try:
   pipe = PipeListener(fifo_name)
   # except:
   
   
   
   print "Begin database logging."
   while(True):
      
      cobaltJSONmessage = pipe.readData()
      
      if cobaltJSONmessage != '':
         logMsg =  LogMsgDecoder.decode(cobaltJSONmessage)
         database.addMessage(logMsg)
      else:
         time.sleep(5)
         
        #Wash. Rinse. Repeat
         

                         
