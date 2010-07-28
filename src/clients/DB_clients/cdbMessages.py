import json

from db2util.ts import SectoTS, TStoST, TSconform, TSFMT

class LogMessage(object):

   def __init__(self, spec):
      
      self.message = spec.get("message")
      self.item_type = spec.get("item_type")
      self.exec_user = spec.get("exec_user")
      self.timestamp = TSconform(SectoTS(float(spec.get("timestamp"))),
                                               format=TSFMT.DB2_NOUSEC )
      self.state = spec.get("state")
      self.item = None
      if self.item_type == 'reservation':
         self.item = ReservationStatus(spec.get('item'))
      #elif self.message_type == 'partition':
      #elif self.message_type == 'job':
      #else:
      #handle bad message, non-fatal exception?
      return
     
   def __str__(self):
      
      return "Message: %s\n" % self.message + "Message_type: %s\n" % self.item_type + "exec_id: %s\n" % self.exec_user + "timestamp: %s\n" % self.timestamp + "%s\n" % self.item

   
class ReservationStatus(object):
   
   """Cobalt reservation state as reconstructed from JSON data."""
   
   def __init__(self, spec):
      
      self.tag = spec.get("tag", "reservation")
      self.cycle = bool(spec.get("cycle"))
      self.cycle_id = spec.get("cycle_id")
      self.users = spec.get("users")
      self.partitions = spec.get("partitions")
      self.name = spec.get("name")
      self.start = TSconform(SectoTS(float(spec.get('start'))), 
                             format=TSFMT.DB2_NOUSEC )
      self.queue = spec.get("queue")
      self.duration = int(spec.get("duration"))
      self.res_id = int(spec.get("res_id"))
      
      return
   
   def __str__(self):
      return "Tag: %s\n" % self.tag + "Cycle: %s\n" % self.cycle + "Users: %s\n" % self.users + "partitions: %s\n" % self.partitions + "name: %s\n" % self.name + "start: %s\n" % self.start + "queue: %s\n" % self.queue + "duration: %s\n" % self.duration + "res_id: %s\n" % self.res_id + "cycle_id: %s\n" % self.cycle_id
   
   



class LogMessageDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
      return LogMessage(spec)
   
class ReservationStateDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
#class JobStatus(LogMessage):

#class PartitionStatus(LogMessage):
