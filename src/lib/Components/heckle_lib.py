# -*- coding: utf-8 -*-

#test

"""
Library Adaptor for use with Heckle Node Management System
"""

from inspect import getargspec
import re
from types import *
import logging
from datetime import datetime, timedelta

#from heckle_stub import HM, reserve, list_reservations, unreserve, findNodes, list_image, findHardwarebyProperty, list_hardware, allocate, get_current_user, createSessionInstance, list_node

import heckle.lib.models as HM
from heckle.lib.heckle_reservations import *
from heckle.lib.heckle_images import list_image
from heckle.lib.heckle_hardware import findHardwareByProperty, list_hardware
from heckle.lib.heckle_allocations import allocate
from heckle.lib.heckle_users import get_current_user
from heckle.lib.util import createSessionInstance
from heckle.lib.heckle_nodes import list_node


#from ChooseNodes import CN as ChooseNodes
#from Heckle_Glossary import *

# hardcoded glossary from Heckle of qualities
# To be replaced by get_glossary function
HW_FIELDS = ["CPU", "GPU", "MEMORY", "DISK", "NET"]  #, "VINTAGE" ]

CPU = [ "intel", "opteron", "nahalem"]
GPU = [ "true" ]
MEMORY = [ "4G", "12G", "16G" ]
DISK = [ "1", "4" ]
NET = [ "myrinet", "ib" ]
IB = [ "qdr", "sdr" ]
PACKAGE = [ "CUDA", "LINPACK" ]
GROUP = [ "cuda", "nimbus" ]
VINTAGE = []



IMAGES = [
     "ubuntu-lucid-amd64",
     "ubuntu-hardy-amd64",
     "legacy-pxelinux",
     "eucalyptus"
     "default-bad"
     ]

logger = logging.getLogger(__name__)

class Heckle_Interface():
     """
     Basic adaptor for Heckle
     Allows library-based interaction with Heckle
     """

     def __init__( self ):
          """
          Establishes SQLAlchemy session, which is then reused by all calls
          """
          try:
               self.session = createSessionInstance()
               #logger.debug("HICCUP: INIT: Session Created")
               #print "HICCUP:  Session Created."
          except:
               logger.exception("HICCUP: INIT: Problem Creating a Session.")
               raise Exception("HICCUP: INIT: Problem Creating a Session.")
          self.GLOSSARY = self.get_glossary( )
          self.HW_FIELDS = self.GLOSSARY.keys()
          self.NODE_LIST = self.get_all_nodes( )
          self.NODE_COUNT = len(self.NODE_LIST)


     def __del__( self ):
          """
          Cleans up the session objects
          """
          self.session.close()
          

#########################################
### These functions make things possible within this object
#########################################
     def get_usernames( self, uid=None , required=False, **kwargs ):
          """
          Returns the usernames object for any one user
          """
          #user_objs = self.session.query( HM.User).filter(HM.User.uid == uid ).one()
          #if user_objs:
          if uid:
               usernames = [uid, ]
          else:
               raise Exception("HICCUP:  No User Entered")
          return usernames


     def get_image( self, ret_type, kernel=None, required=False, **kwargs ):
          """
          Gets the image name from the options object
          Formats it in the way Heckle needs.
          """
          try:
               ker_type = type(kernel)
               if ker_type == ret_type:
                    if kernel == 'default':
                         kernel = None
                    return kernel
               elif ker_type == StringType and ret_type == ListType:
                    if kernel == 'default':
                         return None
                    else:
                         return [kernel]
               elif ker_type == ListType and ret_type == String_Type:
                    if kernel[0] == 'default':
                         return None
                    else:
                         return kernel[0]
               else:
                    raise Exception("HICCUP: get_image: Wrong Data Type for Kernel, need List of Strings.")
          except:
               if required:
                    raise Exception("HICCUP: get_image: No kernel specified")
               else:
                    return None
     

     def get_hw_criteria( self, in_kwargs=None, function=None, **kwargs ):
          """
          Converts dictionary in options to query-language required
               for Heckle Hardware Criteria
          """
          opts = str(in_kwargs) + " " + str(function) + " " + str(kwargs)
          logger.debug("HICCUP: Debug: get_hw_criteria: opts are: %s " % opts )
          hw_criteria = []
          options = {}
          try:
               for field in in_kwargs:
                    if field in self.HW_FIELDS:
                         #print "Found: In HW: ", field, ":", in_kwargs[field]
                         hw_criteria.append(str(field) + str("==") + str(in_kwargs[field]))
                    else:
                         #print "Excluded: ", field, ":" , in_kwargs[field]
                         options[field] = in_kwargs[field]
               if function:  #If you're checking agains a function...
                    new_opt = {}
                    base_arg_list = getargspec(function)[0]   #Get the function's param list
                    for arg in options:
                         if arg in base_arg_list:
                              new_opt[arg] = options[arg]
                    options = new_opt
          except:
               if function:
                    base_arg_list = getargspec(function)[0]   #Get the function's param list
                    for arg in base_arg_list:
                         options[arg]=None
          logger.debug("HICCUP: Debug: get_hw_criteria: HW Criteria is:%s, Remaining Options are %s." % (hw_criteria, options) )
          return options, hw_criteria
          
          
     def normalize(self, **kwargs):
          """
          Makes everything work, transforms from types of input to heckle-ready output
          """
          return_dict = {}

          if user:
               usernames = [user]
          elif uid:
               usernames = self.get_usernames(uid)
          else:
               usernames = None
               
          if time:
               print "Time is: ", time
               start=datetime.now()
               end=datetime.now() + timedelta(int(time))
          elif walltime:
               print "Wall Time is: ", walltime
               start=datetime.now()
               end=datetime.now() + timedelta( minutes=int(walltime) )
          elif start and end:
               pass
          else:
               start = end = None
          
          
          if nodelist or location:
               if location:
                    nodelist = location
          else:
               location = None
                    
          if kwargs or attrs:
               if attrs and kwargs:
                    kwargs.update(attrs)
               elif attrs:
                    kwargs=attrs
          else:
               kwargs = None
          
          return kwargs, location, start, end, usernames


#######################################
### These functions are the workhorses, doing things with Heckle
### They are intended to be called from outside
#######################################

     def find_job_location( self, attrs, nodes, walltime, start=None, **kwargs ):
          """
          This function returns a list of nodes which match the attributes that are free for the appropriate time
          attrs is a dictionary of string pairs, key:value, for hardware
          nodes is integer count of number of nodes desired
          walltime is time, in seconds, for reservation
          
          To Do:
               Schedule future start times
          """
          find_node_criteria = {}
          find_node_criteria['session']=self.session
          find_node_criteria['start']=datetime.now()
          find_node_criteria['end']=datetime.now() + timedelta(int(walltime))
          find_node_criteria['node_num'] = int(nodes)
          params, hw_criteria = self.get_hw_criteria( in_kwargs=attrs, function=findNodes )
          find_node_criteria['hardware_criteria']=hw_criteria
          logger.debug("HICCUP: find_job_location: Find_Node_Criteria is %s" % find_node_criteria)
          if nodes > 0:
               appropriate_nodes = findNodes( **find_node_criteria )
               logger.debug( "HICCUP: find_job_location: appropriate nodes are %s" % appropriate_nodes )
               return appropriate_nodes
          else:
               return []
     


     def make_reservation( self, uid=None, start=None, end=None, nodecount=None, nodelist=None, location=None, kernel=None, time=None, walltime=None, user=None, attrs=None, fakebuild=False, **kwargs ):
          """
          Adaptor to make a reservation
          Gameplan:
               Make session and user objects
               Get list of appropriate nodes from Heckle using options
               Get list of chosen nodes from Chooser with list, options
               If chosen nodes list exist
                    Reserve these nodes
                    Allocate those nodes
                    Un-Reserve unneeded nodes
                    Return Reservation ID and Nodes' info
               Else raise error
          """
          #Check for required fields in options:
          #opts = kwargs
          logger.debug("HICCUP: Debug: Make Reservations: Options are %s", self.__dict__ )
          
          reservation_criteria = {}
          if user:
               usernames = [user]
          elif uid:
               usernames = self.get_usernames(uid)
          else:
               raise Exception("HICCUP: Make Reservations:  Need either User Name or UID.")
          
          #Set up variables
          reservation_criteria['session']=self.session
          if time:
               #print "Time is: ", time
               reservation_criteria['start']=datetime.now()
               reservation_criteria['end']=datetime.now() + timedelta(int(time))
          elif walltime:
               #print "Wall Time is: ", walltime
               reservation_criteria['start']=datetime.now()
               reservation_criteria['end']=datetime.now() + timedelta( minutes=int(walltime) )
          elif start and end:
               reservation_criteria['start']=start
               reservation_criteria['end']=end
          else:
               raise Exception("HICCUP:  Need either a total running time or a start and end time.")
          
          find_node_criteria = {}
          find_node_criteria.update( reservation_criteria )
#Decide Criteria
          if kwargs or attrs:
               if attrs and kwargs:
                    kwargs.update(attrs)
               elif attrs:
                    kwargs=attrs
               params, hw_criteria = self.get_hw_criteria( in_kwargs=kwargs, function=findNodes )
               find_node_criteria['hardware_criteria']=hw_criteria
          else:
               find_node_criteria['image_criteria']=kernel
               params = None
#Use Criteria to choose Nodes
          logger.debug("HICCUP: Debug: Make Reservation: Find_Node_Criteria: %s" % find_node_criteria)
          logger.debug("HICCUP: Debug: Make Reservation: Opts: %s" % reservation_criteria)
          if nodelist or location:
               if location:
                    nodelist = location
               if nodecount and (nodecount > len(nodelist)):
                    logger.debug("HICCUP: Debug: Make Reservation: Finding additional nodes...")
                    node_num = nodecount - len(nodelist)
                    find_node_criteria['node_num'] = int(node_num)
                    appropriate_nodes = findNodes( **find_node_criteria )
                    logger.debug("HICCUP: Debug: Make Reservation: Appropriate Nodes: %s " % appropriate_nodes )
                    chosen_nodes = ChooseNodes( appropriate_nodes, node_num )
                    chosen_nodes += nodelist
               else:
                    logger.debug("HICCUP: Debug: Make Reservation: Using existing node list: %s" % nodelist)
                    chosen_nodes = nodelist
          else:
               logger.debug("HICCUP: Debug: Make Reservation: No Nodelist, straight calculation...")
               find_node_criteria['node_num']=nodecount
               logger.debug("HICCUP: Debug: Make Reservation: Find Node Criteria: %s" % find_node_criteria )
               appropriate_nodes = findNodes( **find_node_criteria )
               logger.debug("HICCUP: Debug: Make Reservation: Appropriate Nodes: %s "% appropriate_nodes )
               chosen_nodes = ChooseNodes( appropriate_nodes, nodecount )  #stub
          logger.debug("HICCUP: Debug: Make Reservation: Chosen Nodes: %s "% chosen_nodes )
#Use Chosen Nodes to Reserve Nodes
          reservation_criteria['node_list']=chosen_nodes
          reservation_criteria['usernames']=usernames
          try:
               reservation_criteria['comments']=kwargs['comments']
          except:
               reservation_criteria["comment"] = "Reserved by: %s" % ', '.join(usernames)
          logger.debug("HICCUP: Debug: Make Reservation: Reservation Options: %s " % reservation_criteria )
          try:
               reservation = reserve( **reservation_criteria )
               self.session.commit()
               logger.debug("HICCUP: Debug: Make Reservation: Reservation Made: %s "% reservation )
               #Use Reservation to Allocate
               allocate_criteria = {}
               allocate_criteria['session'] = self.session
               allocate_criteria['res_id'] = reservation.id
               allocate_criteria['nodes'] = chosen_nodes
               allocate_criteria['num_nodes'] = nodecount
               allocate_criteria["users_and_keys"]={usernames[0]:None}
               allocate_criteria["properties"]=self.GetBuildProperties( params )
               allocate_criteria['image_name'] = self.get_image(ret_type = StringType, kernel=kernel )
               allocate_criteria['fakebuild'] = fakebuild
               logger.debug("HICCUP: Debug: Make Reservation: Allocate Properties: %s" % allocate_criteria )
               allocated_nodes = allocate( **allocate_criteria )
               logger.debug("HICCUP: Debug: Make Reservation: Nodes Allocated: %s" % allocated_nodes )
               self.session.commit()
               return reservation
          except Exception as fromHeckle:
               raise Exception("HICCUP: Make Reservation: Per Heckle, Node %s not available.  Exact error is: %s" % (chosen_nodes, fromHeckle) )



     def free_reserved_node( self, uid=None, node_list=None, **kwargs ):
          """
          Removes reserved nodes from a Heckle reservation
          This will free only those nodes specified
          """
          logger.debug("HICCUP: Debug: Make Reservation: free_reserved_nodes: Opts are %s " % self.__dict__)
          username = (self.get_usernames(uid))[0]
          opts = {"username":username, "session":self.session, "node_names":node_list}
          logger.debug("HICCUP: Debug: free_reserved_nodes: Options are: %s " % opts )
          logger.debug("HICCUP: Debug: free_reserved_nodes:  unreserve yeilds %s" % unreserve( **opts ) )
          self.session.commit()
          return True


     def kill_reservation( self, uid=None, res_id=None, **kwargs ):
          """
          Removes a reservation from the Heckle System
          This will free all nodes within the reservation
          """
          logger.debug("HICCUP: Debug: kill_reservation: vals are %s" % self.__dict__ )
          opts = {}
          username = (self.get_usernames(uid))[0]
          opts["session"] = self.session
          opts["username"] = username
          opts["node_names"] = None
          opts["reservation"] = res_id
          opts["force"] = True
          print "Kill Res: Options Are:", opts
          unreserve( **opts )
          self.session.commit()
          return True


     def get_node_info( self, node_name ):
          """
          Queries Heckle to get node info
          Returns as dict
          """
          logger.debug( "HICCUP: get_node_info")
          #logger.debug( "HICCUP: get_node_info: vals are %s" % self.__dict__ )
          return self.get_node_properties( node_name )


     def get_node_bootstate( self, node_name ):
          """
          Queries Heckle to get the boot state of a node from heckle
          Returns as string
          """
          logger.debug("HICCUP: get_node_bootstate")
          node_info = self.get_node_info( node_name )
          node_state = node_info["bootstate"]
          logger.info("HICCUP: get_node_bootstate: bootstate for node %s is %s" % ( node_name, node_state ))
                                   #; vals are %s" % (node_state, self.__dict__))
          return node_state


     def list_available_nodes( self, start=None, end=None, kernel=None, **kwargs ):
          """
          Returns a list of available nodes which match HW and Time criteria
          Gameplan:
               Get list of all nodes
               Determine allocated nodes
               return list of unallocated nodes
          """
          #print "HICCUP: list_available_nodes: vals are ", self.__dict__
          opts = {}
          opts['session']=self.session
          opts['start']=start
          opts['end']=end
          if kwargs:
               opt, hw_criteria = self.get_hw_criteria( in_kwargs=kwargs, function=findNodes )
               opts['hardware_criteria'] = hw_criteria
          if kernel and not hw_criteria:
               image_name = self.get_image( ret_type=ListType, kernel=kernel )
               opts['image_criteria'] = image_name
          print "List Options are: ", opts
          
          nodes = findNodes( **opts )
          return nodes
          

     def list_all_nodes( self ):
          """
          Returns a list of all nodes
          Gameplan:
               Get list of all nodes
               Determine allocated nodes
               Unallocated nodes is allocated nodes minus allocated nodes
               return list of unallocated nodes
          """
          logger.debug("HICCUP: Debug: list_all_nodes:")# vals are %s" % self.__dict__)
          return self.NODE_LIST



     def Valid_Kernel( self, kernel, **kwargs ):
          """
          Checks to see if the kernel specified is within the list of current images
          """
          self.name="Valid Kernel"
          #logger.debug("HICCUP: Debug: Make Reservation: Valid_Kernel: vals are %s " % self.__dict__ )
          image_name = self.get_image( ret_type=StringType, kernel=kernel )
          logger.debug("HICCUP: Debug: Valid Kernel: Image Name is: %s" % image_name )
          
          image_val = list_image( session=self.session, name=image_name)
          
          return image_val


     def Valid_HW( self, **kwargs ):
          """
          Checks to see if the hardware specified matches any existing HW class
          """
          self.name="Valid HW"
          
          logger.debug("HICCUP: Valid_HW: kwargs are: %s" % kwargs )
          logger.debug("HICCUP: Debug: Valid HW")
          baddict = {}
          hw_dict = self.GLOSSARY
          for arg in kwargs:
               try:
                    if arg=='fakebuild':
                         continue
                    else:
                         if kwargs[arg] not in hw_dict[arg]:
                              return False
                         else:
                              continue
               except:
                    return False
          return True


     def Valid_Job( self, num_nodes=None, kernel=None, **kwargs ):
          """
          This is a bounds-check:  Will the job EVER work.
          
          Validates a current job against Heckle to see if it is
               ever possible with *current* node setup.
          Gameplan:
               Return list of all nodes from heckle which match HW and Image
               (doesn't matter, allocated or unallocated)
          """
          self.name="Valid Job"
          logger.debug("HICCUP: Debug: Valid_Job: vals are %s" % self.__dict__ )
          #Check for required fields in options:
          logger.debug("HICCUP: Debug: Valid Job: Options are: %s" % kwargs )
          opts, hw_criteria = self.Valid_HW( function=findNodes, **kwargs )
          image_name = self.get_image( ret_type=ListType, kernel=kernel )
          valid_job_criteria={}
          valid_job_criteria['session'] = self.session
          valid_job_criteria['hardware_criteria'] = hw_criteria
          valid_job_criteria.update(opts)
          logger.debug("HICCUP: Debug: Valid Job: Criteria is: %s" % valid_job_criteria)

          nodelist = findNodes( **valid_job_criteria )
          
          try:
               if len(nodelist) >= int(kwargs["nodect"]):
                    nodelist = []
          except:
               pass
          
          return nodelist


     def GetBuildProperties( self, *args ):
          pass
     
     
     def GetReservations( self ):
          """
          This gets all the current reservations in the Heckle system.
          """
          reservations = list_reservations( session=self.session )
          print reservations
     
     
     def get_all_nodes( self ):
          """
          Heckle Glossary Function
          Produces a basic list of all the nodes
          """
          p = re.compile("bb\d{1,2}")
          all_nodes_list = []
          for node in list_node( self.session ):
               if p.match(node['name']):
                    all_nodes_list.append(node['name'])
          return all_nodes_list


     def get_glossary( self ):
          """
          Heckle Glossary Function
          Gets a basic glossary of all the hardware_criteria
          Gets list of all nodes, all hardware
          """
          nodelist = self.get_all_nodes()
          hwlist = list_hardware(self.session)
          propdict = {}
          for name in nodelist:
               for element in hwlist:
                    if name in element['nodes']:
                         for prop in element['properties']:
                              val = element['properties'][prop][0]
                              if prop not in propdict.keys():
                                   propdict[prop]=[]
                              if val not in propdict[prop]:
                                   propdict[prop].append( val )
          return propdict
     
     
     def get_node_properties( self, node_name ):
          """
          Heckle Glossary Function
          Gets all the properties of one node
          """
          #hwlist = list_hardware(session, name=node_name)  #Use if it worked...
          #return hwlist['properties']
#          logger.debug("HICCUP: get_node_properties    &&&&&&&&&&&&")
          props = []
          self.session.expire_all()
          hwlist = list_hardware( self.session )
          for element in hwlist:
               if node_name in element['nodes']:
                    props = element['properties']
                    continue
          props.update(list_node(self.session, name=node_name)[0])
          return props
     
     
def ChooseNodes( in_list=None, in_numb=None ):
     """
     For now, chooses only the first n nodes in the list
     regardless of other criteria
     """
     in_numb = int(in_numb)
     try:
          return in_list[ :in_numb]
     except:
          return []
     
     



if __name__=="__main__":
     print "Begin"
     HICCUP=Heckle_Interface()
     print "1."
     HICCUP.list_all_nodes()
     print "2."

