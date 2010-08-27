'''JSON encoding objects for transmitting data to the logging database.'''
__revision__ = '$Revision: 1 $'

import time
import json
import Cobalt.Components



#allow us to dump relevant data to JSON.  
#let the database importer figure out what to do with the data.
class ReportObject(object):
    
    def __init__(self, message, exec_user, state, item_type, item):

        self.message = message #reason for the change
        self.exec_user = exec_user #id of what is causing change None is cobalt
        self.state = state #Current state causing message 
        self.item_type = item_type #the type of item being changed
        self.item = item #this should contain the current state of changed
        self.timestamp = time.time()
        
        return

    def __str__(self):
        return self.reason + self.exec_id + self.item_type + self.item.__repr__()
    def encode(self): #encode into a JSON object, return a string rep of it.       
        return json.dumps(self, cls=ReportObjectEncoder)

class ReportObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ReportObject):

            r = None
            if obj.item_type.lower() == 'reservation':
                r = ReservationStateEncoder()
            elif obj.item_type.lower().find('job_') >= 0 :
                r = JobStateEncoder()
            else:
                raise TypeError("No decoder set for %s of item." % obj.item_type)

            return {'message' : obj.message, 
                    'exec_user' : obj.exec_user, 
                    'item_type' : obj.item_type,
                    'timestamp' : obj.timestamp,
                    'state' : obj.state,
                    'item' : r.default(obj.item)}
        return json.JSONEncoder.default(self, obj)


class ReservationStateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Cobalt.Components.bgsched.Reservation):
            return {'cycle' : obj.cycle,
                    'cycle_id' : obj.cycle_id,
                    'duration' : obj.duration,
                    'partitions': obj.partitions,
                    'name' : obj.name,
                    'queue' : obj.queue,
                    'res_id' : obj.res_id,
                    'start' : obj.start,
                    'tag': obj.tag,
                    'users' : obj.users}    
        else:
            return json.JSONEncoder.default(self, obj)


class JobStateEncoder(json.JSONEncoder):
    
    def default(self, obj):

        #elif isinstance(obj, Cobalt.Components
        #elif isinstance(obj, Cobalt.Components.cqm.Job):
        #    exclude_keys = ['_StateMachine__seas', 'stageid', 
        #                    'stagein', 'stageout', 'url']
        #    classAttrTable = {}
        #    for key in obj.__dict__.keys():
        #        if key not in exclude_keys:
        #            classAttrTable[key] = obj.__dict__[key].__str__()
                    
            #Anything as a property.
        #    classAttrTable['dep_hold'] = obj.has_dep_hold

        #    return classAttrTable
        if isinstance(obj, Cobalt.Components.cqm.JobProgMsg):
            return obj.__dict__
            
        elif isinstance(obj, Cobalt.Components.cqm.JobDataMsg):
            retDict = dict(obj.__dict__)
            retDict['job_prog_msg'] = self.default(obj.job_prog_msg)
            return retDict
        
        return  json.JSONEncoder.default(self, obj)
              
        
