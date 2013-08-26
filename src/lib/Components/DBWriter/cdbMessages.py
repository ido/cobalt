import datetime
try:
    import json
except ImportError:
    import simplejson as json


from db2util.ts import SectoTS, TStoST, TSconform, TSFMT

DB2FORMAT = '%Y-%m-%d-%H.%M.%S.%f'

def db2time_to_datetime(db2time):
    '''Convert a db2 timestamp into a datetime object'''
    return datetime.datetime.strptime(db2time, DB2FORMAT)

class LogMessage(object):
    '''General message to the logging database. Hold the payload as the "item"
    Timestamp based on when message was generated.  This can be overridden by passing a timestamp
    to the spec dictionary.

    '''
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
        return

    def __str__(self):

        return "Message: %s\n" % self.message + "Message_type: %s\n" % self.item_type + "exec_id: %s\n" % self.exec_user +\
                "timestamp: %s\n" % self.timestamp + "%s\n" % self.item

    #so these can be sorted, ordering based on time rec'd.
    def __lt__(self, other):
        return self.raw_time < other.raw_time

class ReservationStatus(object):

    """Cobalt reservation state as reconstructed from JSON data."""

    def __init__(self, spec):
        print spec
        self.tag = spec.get("tag", "reservation")
        if spec.get("cycle") == None:
            self.cycle = 0
        else:
            self.cycle = int(spec.get("cycle"))
        self.cycle_id = spec.get("cycle_id")
        self.users = spec.get("users")
        self.partitions = spec.get("partitions")
        self.name = spec.get("name")
        self.start = spec.get('start')
        self.queue = spec.get("queue")
        self.duration = int(spec.get("duration"))
        self.res_id = int(spec.get("res_id"))
        if spec.get("block_passthrough") == None:
            self.block_passthrough = None
        else:
            self.block_passthrough = int(spec.get("block_passthrough"))
        if spec.get("project") == None:
            self.project = None
        else:
            self.project = spec.get("project")


        return

    def encode(self):
        """return a dict of everything in object"""
        return self.__dict__

    def __str__(self):
        return "Tag: %s\n" % self.tag + "Cycle: %s\n" % self.cycle + \
               "Users: %s\n" % self.users +\
               "partitions: %s\n" % self.partitions +\
               "name: %s\n" % self.name + "start: %s\n" % self.start +\
               "queue: %s\n" % self.queue + "duration: %s\n" % self.duration +\
               "res_id: %s\n" % self.res_id + "cycle_id: %s\n" % self.cycle_id

class JobStatus(object):
    '''Carrier class for general job status update.'''

    def __init__(self, spec):
        for entry in spec:
            self.__setattr__(entry, spec[entry])

    def __str__(self):
        output = []
        for entry in self.__dict__:
            output.append("%s : %s" % (entry, str(self.__dict__[entry])))
        return '\n'.join(output)

    def encode(self):
        '''Convert this class to a JSON string'''
        return self.__dict__

    def set_types(self):
        '''Stub for set types override for special type conversions into the db'''
        raise NotImplementedError("JobStatus.set_types() not implemented.")

class JobProgStatus(JobStatus):
    '''Job progress status update object.'''

    def set_types(self):
        if hasattr(self, 'envs'):
            self.envs = dict_to_plain_strs(self.envs)
        if hasattr(self, 'location'):
            self.location = list_to_plain_strs(self.location)
        if hasattr(self, 'dep_frac'):
            if self.dep_frac != None:
                self.dep_frac = float(self.dep_frac)

    def encode(self):
        ret_dict = self.__dict__
        if hasattr(self, 'location'):
            if self.location == None:
                ret_dict['location'] = []
            else:
                ret_dict['location'] = str_to_list(self.location)
        if hasattr(self, 'envs'):
            if self.envs == None:
                ret_dict['envs'] = {}
            else:
                ret_dict['envs'] = str_to_dict(self.envs)
        if hasattr(self, 'dep_frac'):
            if self.dep_frac != None:
                self.dep_frac = float(self.dep_frac)
        return ret_dict


class JobDataStatus(JobStatus):
    '''Job data update message.'''

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
        ret_dict = self.__dict__
        if self.args == None:
            ret_dict['args'] = []
        else:
            ret_dict['args'] = self.args.split(' ')

        if self.location == None:
             ret_dict['location'] = []
        else:
             ret_dict['location'] = str_to_list(self.location)
        if self.envs == None:
             ret_dict['envs'] = {}
        else:
             ret_dict['envs'] = str_to_dict(self.envs)
        #ret_dict['job_user_list'] = str_to_list(self.job_user_list)
        ret_dict['job_prog_msg'] = self.job_prog_msg.encode()
        return ret_dict

class PartitionStatus(object):
    '''Partition data stub.  Not implemetned yet.'''
    def __init__(self, spec):
        pass


class LogMessageDecoder(json.JSONDecoder):
    '''Subclass for JSON message decoder for DB writer messages'''

    def decode(self, string):
        spec = json.loads(string)
        return LogMessage(spec)


class LogMessageEncoder(json.JSONEncoder):
    '''Subclass of the JSON encoder to use for DB writer messages.'''

    def default(self, obj):
        encoded_obj = {'message': obj.message,
                    'item_type': obj.item_type,
                    'exec_user': obj.exec_user,
                    'timestamp': obj.timestamp,
                    'state': obj.state,
                    'item': obj.item.encode()}
        return encoded_obj


def dict_to_plain_strs(d):
    '''Helper to convert a dict to strings for database storage of arguments.'''
    if d == None:
        return None
    return ':'.join(['='.join([str(e), str(d[e])]) for e in d])

def list_to_plain_strs(l):
    '''Helper to convert a list to strings for Database storagg of arguments.'''
    if l == None:
        return None
    return ':'.join([str(e) for e in l])

def str_to_dict(s):
    '''Convert argument style strings to a proper dict.'''

    if s == None: 
        return {}
    entries = s.split(':')
    key_vals = [entry.split('=') for entry in entries] 
    ret_dict = {}
    for key_val in key_vals:
        ret_dict[key_val[0]] = key_val[1]
    return ret_dict

def str_to_list(s):
    '''Split up an argumnent string into it's component list.'''

    if s == None: 
        return []
    return s.split(':')


