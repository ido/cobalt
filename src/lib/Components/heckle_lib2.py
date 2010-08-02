# -*- coding: utf-8 -*-







import heckle.lib.models as HM
from heckle.lib.heckle_reservations import *
from heckle.lib.heckle_images import list_image
from heckle.lib.heckle_hardware import findHardwareByProperty, list_hardware
from heckle.lib.heckle_allocations import allocate
from heckle.lib.heckle_users import get_current_user
from heckle.lib.util import createSessionInstance
from heckle.lib.heckle_nodes import list_node



#if HICCUP in cobalt configs:
	#get HW fields from cobalt configs
#else
	#Use these hw fields
HW_FIELDS = ["GPU", "MEM", "DISK", "NET", "IB", "CORES"]

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


	def get_hw_criteria( self, attrs ):
          """
          Converts dictionary in options to query-language required
               for Heckle Hardware Criteria
          """
          logger.debug("HICCUP: Debug: get_hw_criteria: opts are: %s " % opts )
          hw_criteria = []
          options = {}
		for field in in_kwargs:
			if field in self.HW_FIELDS and value in self.glossary[field]:
				#print "Found: In HW: ", field, ":", in_kwargs[field]
				hw_criteria.append(str(field) + str("==") + str(in_kwargs[field]))
			else:
				#print "Excluded: ", field, ":" , in_kwargs[field]
				options[field] = in_kwargs[field]
          logger.debug("HICCUP: Debug: get_hw_criteria: HW Criteria is:%s, Remaining Options are %s." % (hw_criteria, options) )
          if options:
			raise Exception( "HICCUP: get_hw_criteria: Bad hardware criteria %s" % options )
		else:
			return hw_criteria


     def find_job_location( self, attrs, nodes=0, walltime, start ):
          """
          This function returns a list of nodes which match the attributes that are free for the appropriate time
          attrs is a dictionary of string pairs, key:value, for hardware
          nodes is integer count of number of nodes desired
          walltime is time, in seconds, for reservation
          
          To Do:
               Schedule future start times
          """
          node_criteria = {}
          node_criteria['session']=self.session
          node_criteria['start']=datetime.now()
          node_criteria['end']=datetime.now() + timedelta(int(walltime))
          node_criteria['node_num'] = int(nodes)
          node_criteria['hardware_criteria']=self.get_hw_criteria( attrs )
          logger.debug("HICCUP: find_job_location: Find_Node_Criteria is %s" % find_node_criteria)
          if nodes > 0:
               appropriate_nodes = findNodes( **find_node_criteria )
               logger.debug( "HICCUP: find_job_location: appropriate nodes are %s" % appropriate_nodes )
               return appropriate_nodes
          else:
               return []



	def list_available_nodes( self, start=None, end=None, kernel='default', attrs ):
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
		opts['hardware_criteria'] = self.get_hw_criteria( in_kwargs=kwargs )
          if kernel and not hw_criteria:
               opts['image_criteria'] = kernel
          print "List Options are: ", opts
          
          nodes = findNodes( **opts )
          return nodes


     def Valid_Kernel( self, kernel ):
          """
          Checks to see if the kernel specified is within the list of current images
          """
          logger.debug("HICCUP: Debug: Valid Kernel: Image Name is: %s" % image_name )
          image_val = list_image( session=self.session, name=image_name)          
          return image_val


     def Valid_HW( self, attrs={} ):
          """
          Checks to see if the hardware specified matches any existing HW class
          """
          logger.debug("HICCUP: Valid_HW: kwargs are: %s" % kwargs )
          baddict = {}
          badlist = []
          hw_dict = self.GLOSSARY
          for attr in attrs:
			if attr not in HW_FIELDS:
				badlist.update(attr)
               if kwargs[attr] not in hw_dict[attr]:
				baddict[attr] = attrs[attr]
		if badlist or baddict:
			raise Exception( "HICCUP: Valid_HW: The following are bad variables: keys %s, value %s" % (badlist, baddict) )
          return True


	def Valid_Job( self, num_nodes=None, kernel=None, **kwargs ):
		"""
		This is a bounds check:  Will the job ever run on the system, as-is.
		"""
		valid_kernel = self.Valid_Kernel( something )
		valid_hw = self.Valid_HW( something )
		valid_job = len(self.list_available_nodes( something )) >= num_nodes
		if valid_kernel and valid_hw and valid_job:
			return True
		return False

     
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
		Note: This is specific to Breadboard.
			For real installation, this would need to read from config file.
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
          self.NODELIST = self.get_all_nodes()
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





























