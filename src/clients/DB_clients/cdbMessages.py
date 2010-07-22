import json

from db2util.ts import SectoTS, TStoST, TSconform, TSFMT

class LogMessage(object):

   def __init__(self, spec):
      
      self.message = spec.get("reason")
      self.item_type = spec.get("item_type")
      self.exec_id = spec.get("exec_id")
      self.item = None
      if self.item_type == 'reservation':
         self.item = ReservationStatus(spec.get('item'))
      #elif self.message_type == 'partition':
      #elif self.message_type == 'job':
      #else:
      #handle bad message, non-fatal exception?
      return
     
   def __str__(self):
      
      return "Message: %s\n" % self.message + "Message_type: %s\n" % self.item_type + "exec_id: %s\n" % self.exec_id + "%s\n" % self.item

   
class ReservationStatus(object):
   
   """Cobalt reservation state as reconstructed from JSON data."""
   
   def __init__(self, spec):
      
      self.tag = spec.get("tag", "reservation")
      self.cycle = bool(spec.get("cycle"))
      self.users = spec.get("users")
      if not self.users:
         self.users = "None"
      self.createdQueue = bool(spec.get("createdQueue"))
      self.partitions = spec.get("partitions")
      self.name = spec.get("name")
      self.start = TSconform(SectoTS(float(spec.get('start'))), format=TSFMT.DB2_NOUSEC )
      self.queue = spec.get("queue")
      self.duration = int(spec.get("duration"))
      self.res_id = int(spec.get("res_id"))
      self.running = bool(spec.get("running"))
      
      return
   
   def __str__(self):
      return "Tag: %s/n" % self.tag + "Cycle: %s\n" % self.cycle + "Users: %s\n" % self.users + "createdQueue: %s\n" % self.createdQueue + "partitions: %s\n" % self.partitions + "name: %s\n" % self.name + "start: %s\n" % self.start + "queue: %s\n" % self.queue + "duration: %s\n" % self.duration + "res_id: %s\n" % self.res_id + "running: %s\n" % self.running
   
   
class LogMessageDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
      return LogMessage(spec)
   
class ReservationStateDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
#class JobStatus(LogMessage):

#class PartitionStatus(LogMessage):
