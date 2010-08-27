import json

from db2util.ts import SectoTS, TStoST, TSconform, TSFMT

class LogMessage(object):

   def __init__(self, spec):
      
      self.message = spec.get("message")
      self.item_type = spec.get("item_type")
      self.exec_user = spec.get("exec_user")
      self.timestamp = TSconform(SectoTS(float(spec.get("timestamp"))),
                                               format=TSFMT.DB2 )
      self.raw_time = spec.get("timestamp")

      self.state = spec.get("state")
      self.item = None
      if self.item_type == 'reservation':
         self.item = ReservationStatus(spec.get('item'))
      elif self.item_type == 'partition':
         raise NotImplementedError("partition logging not yet implemented.")
      elif self.item_type == 'job_prog':
         self.item = JobProgStatus(spec.get('item'))
         self.item.set_types()
      elif self.item_type == 'job_data':
         self.item = JobDataStatus(spec.get('item'))
         self.item.set_types()
      else:
         #handle bad message, non-fatal exception?
         raise RuntimeError("Bad or Malformed message caught.")
         pass
      return
     
   def __str__(self):
      
      return "Message: %s\n" % self.message + "Message_type: %s\n" % self.item_type + "exec_id: %s\n" % self.exec_user + "timestamp: %s\n" % self.timestamp + "%s\n" % self.item

   #so these can be sorted, ordering based on time rec'd.
   def __lt__(self, other):
      return self.raw_time < other.raw_time
      
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
   
class JobStatus(object):

   def __init__(self, spec):
      for entry in spec:
         self.__setattr__(entry, spec[entry])

   def __str__(self):
      output = []
      for entry in self.__dict__:
         output.append("%s : %s\n" % (entry, str(self.__dict__[entry])))
      return ''.join(output)

   def set_types(self):
      raise NotImplementedError("JobStatus.set_types() not implemented.")
      
class JobProgStatus(JobStatus):

   def set_types(self):
      pass
   
   
class JobDataStatus(JobStatus):
   
   def __init__(self, spec):
      JobStatus.__init__(self,spec)
      self.job_prog_msg = JobProgStatus(spec.get('job_prog_msg'))
      
   def set_types(self):
      self.procs = int(self.procs)
      self.args = ' '.join(self.args)
      if self.args == '' : self.args = None
      self.envs = str(self.envs)
      self.preemptable = int(self.preemptable)
      self.project = str(self.project)
      if self.priority_core_hours: 
         self.priority_core_hours = int(self.priority_core_hours)
      else: 
         self.priority_core_hours = None
      self.location = str(self.location)
      self.job_prog_msg.set_types()


class PartitionStatus(object):
   
   def __init__(self, spec):
      
      pass


class LogMessageDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
      return LogMessage(spec)
   
#class ReservationStaeDecoder(json.JSONDecoder):
#
#   def decode(self, string):
#      spec = json.loads(string)
#
#class JobStateDecoder(LogMessage):
#   def decode(self, string):
#      spec = json.loads(string)
#
#class PartitionStateDecoder(LogMessage):
