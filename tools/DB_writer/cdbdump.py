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

import pipelistener

from dbWriter import DatabaseWriter
from cdbMessages import LogMessage, LogMessageDecoder



def parse_options():
   
   opt_parser = optparse.OptionParser()

   opt_parser.add_option('-r', '--recovery_file', action='store', 
                         dest='recovery_file')
   opt_parser.add_option('-l', '--load_msgs', action='store_true', 
                         dest='load_msgs')
   opt_parser.add_option('-f', '--fifo', action='store',
                         dest='user_fifo')
   opt_parser.add_option('-c', '--config_file', action='store',
                         dest='config_filename')

   opt_parser.set_defaults(recovery_file=None)
   opt_parser.set_defaults(load_msgs=False)
   opt_parser.set_defaults(user_fifo=None)
   opt_parser.set_defaults(config_filename=None)

   return opt_parser.parse_args()


__helpmsg__ = """Usage: cdbdump.py"""

if __name__ == '__main__':

   #Command line options.  If conflict with config, these win.
   opts, args = parse_options()

   
   #Configuration file handling
   con_file = ConfigParser.ConfigParser()
   config_filename = "/Users/paulrich/cobalt-dev/tools/DB_writer/DB_writer_config"
   if opts.config_filename:
      config_filename = opts.config_filename

   con_file.read(os.path.join(config_filename))

   fifo_name = con_file.get('cdbdump', 'default_fifo')
   login = con_file.get('cdbdump', 'login')
   pwd = con_file.get('cdbdump', 'pwd')
   database = con_file.get('cdbdump', 'database')
   schema = con_file.get('cdbdump', 'schema')
   queue_state_file = con_file.get('cdbdump','queue_state_file')
   pipe_poll_interval = con_file.get('cdbdump','pipe_poll_interval')
   
   database = DatabaseWriter(database, login, pwd, schema)

   LogMsgDecoder = LogMessageDecoder()

   #starting listener.  This may become more sophistocated later
   if opts.user_fifo:
      fifo_name = os.path.join(opts.user_fifo)

   pipe = pipelistener.pipelistener(fifo_name, queue_state_file)

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
   print "opening %s " % fifo_name
   #pipe.open()
   
   
   
   print "Begin database logging."
   justRead = True
   while(True):
      
      cobaltJSONmessage = pipe.get_next_message()

      if cobaltJSONmessage:
         justRead = True
         pipe.save_msgs()
         logMsg = None
         try:
            logMsg =  LogMsgDecoder.decode(cobaltJSONmessage)
         except ValueError:
            #just drop the message.  It's a loss, but came 
            #in malformed.  No way to call back, yet.
            print "dropped bad message."
            continue
         database.addMessage(logMsg)
         
      else:
         if justRead:
            justRead = False
            pipe.save_msgs()
         #no pending messages, snooze so we don't
         #spin the core to death poking the file.
         time.sleep(float(pipe_poll_interval))
         pipe.read()
         
        #Wash. Rinse. Repeat
   pipe.close()

                         
