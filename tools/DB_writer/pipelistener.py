import os, json

class pipelistener (object):

   """since we're not in the business of losing data, the data from
   a pipe gets read to a temp file, and we go from there. I am beginning
   to think that a pickle is in order-ish"""

   def  __init__(self, fifoname, queue_state_file):
       self.pendingMessages = []
       self.fifo = None
       self.fifoname = fifoname
       self.queue_state_file = queue_state_file

   def __del__(self):
      if self.fifo:
         self.close()


   def open(self):
      self.fifo = open(os.path.join(self.fifoname), 'r')
   

   def close(self):
      if not self.fifo.closed:
         self.fifo.close()


   def read(self):

      try:
         self.open()
         newlines = self.fifo.readlines()
         if newlines:
            self.pendingMessages.extend(newlines)
         self.close()
      except IOError as e:
         print e
         print "Error reading from cobalt fifo."
         self.close()
   
   def get_next_message(self):
      
      if not len(self.pendingMessages):
         return None
      else:
         return self.pendingMessages.pop(0)
   
   def save_msgs(self):
      f = open (self.queue_state_file, 'w+')
      json.dump(self.pendingMessages, f)
      f.close()
      
   def load_msgs(self):
      f = open (os.path.join(self.queue_state_file), 'r')
      self.pendingMessages = json.load(f)
      f.close()

