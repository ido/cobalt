import datetime
try:
    import json
except ImportError:
    import simplejson as json


from db2util.ts import SectoTS, TStoST, TSconform, TSFMT

db2format = '%Y-%m-%d-%H.%M.%S.%f'

def db2time_to_datetime(db2time):
   return datetime.datetime.strptime(db2time, db2format)

class LogMessage(object):

   def __init__(self, spec):
      
      self.message = spec.get("message")
      self.item_type = spec.get("item_type")
      self.exec_user = spec.get("exec_user")
      self.timestamp = spec.get("timestamp")
                
      self.raw_time = db2time_to_datetime(self.timestamp)

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
      self.start = spec.get('start')
      self.queue = spec.get("queue")
      self.duration = int(spec.get("duration"))
      self.res_id = int(spec.get("res_id"))
      
      return
   
   def encode(self):
      """return a dict of everything in object"""
      return self.__dict__

   def __str__(self):
      return "Tag: %s\n" % self.tag + "Cycle: %s\n" % self.cycle + "Users: %s\n" % self.users + "partitions: %s\n" % self.partitions + "name: %s\n" % self.name + "start: %s\n" % self.start + "queue: %s\n" % self.queue + "duration: %s\n" % self.duration + "res_id: %s\n" % self.res_id + "cycle_id: %s\n" % self.cycle_id
   
class JobStatus(object):

   def __init__(self, spec):
       for entry in spec:
         self.__setattr__(entry, spec[entry])

   def __str__(self):
      output = []
      for entry in self.__dict__:
         output.append("%s : %s" % (entry, str(self.__dict__[entry])))
      return '\n'.join(output)
   
   def encode(self):
      return self.__dict__
      
   def set_types(self):
      raise NotImplementedError("JobStatus.set_types() not implemented.")
      
class JobProgStatus(JobStatus):

   def set_types(self):
      if hasattr(self, 'envs'):
          self.envs = dict_to_plain_strs(self.envs)
      if hasattr(self, 'location'):
          self.location = list_to_plain_strs(self.location)
      if hasattr(self, 'dep_frac'):
          if self.dep_frac != None:
              self.dep_frac = float(self.dep_frac)
   
   def encode(self):
       retDict = self.__dict__
       if hasattr(self, 'location'):
           if self.location == None:
               retDict['location'] = []
           else:
               retDict['location'] = str_to_list(self.location)
       if hasattr(self, 'envs'):
           if self.envs == None:
               retDict['envs'] = {}
           else:
               retDict['envs'] = str_to_dict(self.envs)
       if hasattr(self, 'dep_frac'):
           if self.dep_frac != None:
               self.dep_frac = float(self.dep_frac)

       
       return retDict


class JobDataStatus(JobStatus):
   
   def __init__(self, spec):
      JobStatus.__init__(self,spec)
      self.job_prog_msg = JobProgStatus(spec.get('job_prog_msg'))
      
   def set_types(self):
      self.procs = int(self.procs)
      self.args = ' '.join(self.args)
      if self.args == '' : self.args = None
      self.envs = dict_to_plain_strs(self.envs) 
      self.preemptable = int(self.preemptable)
      self.project = str(self.project)
      if self.priority_core_hours: 
         self.priority_core_hours = int(self.priority_core_hours)
      else: 
         self.priority_core_hours = None
      self.location = list_to_plain_strs(self.location)
      if hasattr(self, 'dep_frac'):
          if self.dep_frac != None:
              self.dep_frac = float(self.dep_frac)
      #self.job_user_list = list_to_plain_strs(self.job_user_list)
      self.job_prog_msg.set_types()

   def encode(self):
      retDict = self.__dict__
      if self.args == None:
         retDict['args'] = []
      else:
         retDict['args'] = self.args.split(' ')
      
      if self.location == None:
          retDict['location'] = []
      else:
          retDict['location'] = str_to_list(self.location)
      if self.envs == None:
          retDict['envs'] = {}
      else:
          retDict['envs'] = str_to_dict(self.envs)
      #retDict['job_user_list'] = str_to_list(self.job_user_list)

      retDict['job_prog_msg'] = self.job_prog_msg.encode()

      return retDict

class PartitionStatus(object):
   
   def __init__(self, spec):
      
      pass


class LogMessageDecoder(json.JSONDecoder):

   def decode(self, string):
      spec = json.loads(string)
      return LogMessage(spec)
 

class LogMessageEncoder(json.JSONEncoder):
   
   def default(self, obj):
      encodedObj = {'message': obj.message,
                    'item_type': obj.item_type,
                    'exec_user': obj.exec_user,
                    'timestamp': obj.timestamp,
                    'state': obj.state,
                    'item': obj.item.encode()}
      

      return encodedObj


def dict_to_plain_strs(d):
    if d == None:
        return None
    return ':'.join(['='.join([str(e), str(d[e])]) for e in d])

def list_to_plain_strs(l):
    if l == None:
        return None
    return ':'.join([str(e) for e in l])

def str_to_dict(s):
    if s == None: 
        return {}
    entries = s.split(':')
    keyVals = [entry.split('=') for entry in entries] 
    retDict = {}
    for keyVal in keyVals:
        retDict[keyVal[0]] = keyVal[1]
    return retDict

def str_to_list(s):
    if s == None: 
        return []
    return s.split(':')


