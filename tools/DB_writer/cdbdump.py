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

   """since we're not in the business of losing data, the data from
   a pipe gets read to a temp file, and we go from there. I am beginning
   to think that a pickle is in order-ish"""

   def  __init__(self, fifoname):
       self.pendingMessages = []
       self.fifo = None

   def __del__(self):
      if self.fifo:
         self.close()


   def open(self, fifoname):
      self.fifo = open(os.path.join(fifoname), 'r')
   

   def close(self):
      if not self.fifo.closed:
         self.fifo.close()


   def read(self):

      try:
         newlines = self.fifo.readlines()
         if newlines:
            self.pendingMessages.extend(newlines)
      except IOError as e:
         print e
         print "Error reading from cobalt fifo."
         self.close()
   
   def get_next_message(self):
      self.read()
      if not len(self.pendingMessages):
         return None
      else:
         return self.pendingMessages.pop(0)
   
   def save_msgs(self):
      f = open ('cdbdump.json', 'w+')
      json.dump(self.pendingMessages, f)
      f.close()
      
   def load_msgs(self):
      f = open ('cdbdump.json', 'r')
      self.pendingMessages = json.load(f)
      f.close()


def parse_options():
   
   opt_parser = optparse.OptionParser()

   opt_parser.add_option('-r', '--recovery_file', action='store', 
                         dest='recovery_file')
   opt_parser.add_option('-l', '--load_msgs', action='store_true', 
                         dest='load_msgs')

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

   #starting listener.  This may become more sophistocated later
   
   pipe = PipeListener(fifo_name)

   #recovery handling.
   if opts.load_msgs:
      pipe.load_msgs()
      for msg in pipe.pendingMessages:
         print LogMsgDecoder.decode(msg)
         database.addMessage(msg)

      pipe.pendingMessages = []
      pipe.save_msgs()

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

   #Normal operation.
   pipe.open(fifo_name)
   
   
   
   print "Begin database logging."
   justRead = True
   while(True):
      
      cobaltJSONmessage = pipe.get_next_message()
      

      if cobaltJSONmessage:
         justRead = True
         pipe.save_msgs()

         logMsg =  LogMsgDecoder.decode(cobaltJSONmessage)
         database.addMessage(logMsg)
         
      else:
         if justRead:
            justRead = False
            pipe.save_msgs()
         #no pending messages, snooze so we don't
         #spin the core to death poking the file.
         time.sleep(5)
         
        #Wash. Rinse. Repeat
   pipe.close()

                         
