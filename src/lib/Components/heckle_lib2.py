# -*- coding: utf-8 -*-
"""
Heckle Interface
Library Adaptor / Interface for Heckle
Allows encapsulated reservation system using Heckle
"""

import re
import logging
from datetime import datetime, timedelta

from heckle.lib.heckle_reservations import reserve as heckle_reserve
from heckle.lib.heckle_reservations import unreserve as heckle_unreserve
from heckle.lib.heckle_reservations import findNodes as heckle_findNodes
from heckle.lib.heckle_reservations import list_reservations as\
    heckle_list_reservations
from heckle.lib.heckle_images import list_image as heckle_list_image
from heckle.lib.heckle_hardware import list_hardware as heckle_list_hardware
from heckle.lib.heckle_allocations import allocate as heckle_allocate
from heckle.lib.util import createSessionInstance \
    as heckle_createSessionInstance
from heckle.lib.heckle_nodes import list_node as heckle_list_node

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

LOGGER = logging.getLogger(__name__)

class HeckleConnector( object ):
    """
    Basic adaptor for Heckle
    Allows library-based interaction with Heckle
    """

    def __init__( self ):
        """
        Establishes SQLAlchemy session, which is then reused by all calls
        """
        try:
            self.session = heckle_createSessionInstance()
        except:
            LOGGER.exception("HICCUP:INIT: Problem Creating a Session.")
            raise Exception("HICCUP:INIT: Problem Creating a Session.")
        self.hw_fields = HW_FIELDS
        self.node_count = 0
        self.node_list = []
        self.glossary( )


    def __del__( self ):
        """
        """
        self.session.close()

    ################################################
    ###  These are external methods
    ###  They are involved in the making and killing of reservations
    ################################################


    #def make_reservation( self, location, kernel, walltime, user, \
    #    fakebuild, comment=None ):
    def make_reservation( self, job_dict ):
        """
        Adaptor to make a reservation
        Returns the Heckle Reservation object
        Variables in the job dict:
            location: list of strings,
                containing names of nodes to make reservation
            kernel: string, exact name of kernel image to use
            user: string, user name passed through Cobalt
            fakebuild: boolean, whether to actually build node or fake build it.
            comment: string, any comments to make in the reservation
            kwargs:  Any
        """
        LOGGER.debug("HICCUP:make_reservations: Options are %s"\
            % self.__dict__ )
        reservation_criteria = {} #Build reservation arguments
        reservation_criteria['session'] = self.session
        reservation_criteria['start'] = datetime.now()
        reservation_criteria['end'] = datetime.now() + \
            timedelta( minutes=int( job_dict['walltime'] ) )
        reservation_criteria['node_list'] = job_dict['location']
        reservation_criteria['usernames'] = [job_dict['user'], ]   #Fix this
        try:
            reservation_criteria['comment'] = job_dict['comment']
        except:
            reservation_criteria["comment"] = "Reserved by: %s" % \
                ', '.join( reservation_criteria['usernames'] )
        LOGGER.debug("HICCUP:make_reservation: Reservation Options: %s "\
            % reservation_criteria )
        reservation = heckle_reserve( **reservation_criteria )
        self.session.commit()
        LOGGER.debug("HICCUP:make_reservation: Reservation Made: %s "%\
            reservation )
        #Use Reservation to Allocate
        allocate_criteria = {}   #build allocation arguments
        allocate_criteria['session'] = self.session
        allocate_criteria['res_id'] = reservation.id
        allocate_criteria['nodes'] = job_dict['location']
        allocate_criteria['num_nodes'] = len( job_dict['location'] )
        allocate_criteria["users_and_keys"] = { job_dict['user']:None}
        allocate_criteria["properties"] = None
        allocate_criteria['image_name'] = job_dict['kernel']
        allocate_criteria['fakebuild'] = job_dict['fakebuild']
        LOGGER.debug("HICCUP:make_reservation: Allocate Properties: %s" %\
            allocate_criteria )
        allocated_nodes = heckle_allocate( **allocate_criteria )
        LOGGER.debug("HICCUP:make_reservation: Nodes Allocated: %s" %\
            allocated_nodes )
        self.session.commit()
        return reservation


    def free_reserved_node( self, uid=None, node_list=None, **kwargs ):
        """
        Removes reserved nodes from a Heckle reservation
        This will free only those nodes specified
        """
        LOGGER.debug(
            "HICCUP:free_reserved_nodes: Opts are %s "
            % self.__dict__)
        opts = {}
        opts["username"] = uid
        opts["session"] = self.session
        opts["node_names"] = node_list
        LOGGER.debug(
            "HICCUP:free_reserved_nodes: unreserve yeilds %s" %
            heckle_unreserve( **opts ) )
        self.session.commit()
        return True


    def kill_reservation( self, uid=None, res_id=None, **kwargs ):
        """
        Removes a reservation from the Heckle System
        This will free all nodes within the reservation
        """
        LOGGER.debug("HICCUP:kill_reservation: vals are %s" % self.__dict__ )
        opts = {}
        opts["session"] = self.session
        opts["username"] = uid
        opts["node_names"] = None
        opts["reservation"] = res_id
        opts["force"] = True
        print "Kill Res: Options Are:", opts
        LOGGER.debug(
            "HICCUP:kill_reservation:  unreserve yeilds %s" %
            heckle_unreserve( **opts ) )
        self.session.commit()
        return True


    def get_hw_criteria( self, attrs ):
        """
        Converts dictionary in options to query-language required
            for Heckle Hardware Criteria
        attrs is a dict of key:value pairs, of strings.
        Returns a string in query-language
        """
        LOGGER.debug("HICCUP:get_hw_criteria: opts are: %s " % attrs )
        hw_criteria = []
        options = {}
        if not attrs:
            return []
        for field in attrs:
            if field in self.hw_fields and attrs[field] in self.glossary[field]:
                if field is 'fakebuild':
                    pass
                else:
                    #print "Found: In HW: ", field, ":", in_kwargs[field]
                    hw_criteria.append(str(field) + str("==") + \
                        str(attrs[field]))
            else:
                #print "Excluded: ", field, ":" , in_kwargs[field]
                options[field] = attrs[field]
        LOGGER.debug(
            "HICCUP:get_hw_criteria: hwcriteria is:%s" % hw_criteria )
        if options:
            raise Exception( 
                "HICCUP:get_hw_criteria: Bad hardware criteria %s" % options )
        else:
            return hw_criteria


    def find_job_location( self, attrs, nodes, walltime, start=None, \
                               forbidden=None, **kwargs ):
        """
        This function returns a list of nodes which match the attributes

        attrs is a dictionary of string pairs, key:value, for hardware requirements
        nodes is an integer, the count of number of nodes desired
        walltime is an integer, representing the timetime, in seconds, for reservation
        forbidden is a list of strings, node names not to use.  (currently not used.)
        
        There may be many other arguments passed in by other functions, unused by this
        function, which have to be accepted and disregarded; this is accomplished by
        the **kwargs.
        """
        if not start:
            start = datetime.now()
        node_criteria = {}
        node_criteria['session'] = self.session
        node_criteria['start'] = start
        node_criteria['end'] = datetime.now() + timedelta(int(walltime))
        node_criteria['node_num'] = int(nodes).copy()
        node_criteria['hardware_criteria'] = self.get_hw_criteria( attrs )
        LOGGER.debug(
        "HICCUP:find_job_location: Find_Node_Criteria is %s" % node_criteria)
        bad_count = 1
        if nodes > 0:
            while bad_count > 0:
                appropriate_nodes = heckle_findNodes(**node_criteria )
                appropriate_nodes.sort()
                app_set = set( appropriate_nodes )
                bad_set = set( forbidden )
                bad_nodes = list( app_set.intersection( bad_set )
                bad_count = len( bad_nodes )
                node_criteria['node_num'] += bad_count
            LOGGER.debug( 
                "HICCUP:find_job_location: appropriate nodes are %s" %
                appropriate_nodes )
            return appropriate_nodes
        else:
            return []



    def list_available_nodes( self, start=None, end=None, kernel='default', \
        attrs=None ):
        """
        Returns a list of available nodes which match HW and Time criteria
        """
        #print "HICCUP:list_available_nodes: vals are ", self.__dict__
        opts = {}
        opts['session'] = self.session
        opts['start'] = start
        opts['end'] = end
        opts['hardware_criteria'] = self.get_hw_criteria( attrs=attrs )
        if kernel and not attrs:
            opts['image_criteria'] = kernel
        print "List Options are: ", opts
        nodes = heckle_findNodes(**opts )
        nodes.sort()
        return nodes


    def validkernel( self, kernel ):
        """
        Checks to see if the kernel specified is within 
        the list of current images
        """
        logstr = "HICCUP:validkernel:"
        LOGGER.debug( logstr + "Image Name is: %s" % kernel )
        if not heckle_list_image( session=self.session, name=kernel):
            raise Exception( logstr + "No valid kernel %s" % kernel )
        else:
            return True


    def validhw( self, attrs=None ):
        """
        Checks to see if the hardware specified matches any existing HW class
        """
        LOGGER.debug("HICCUP:validhw: attrs are: %s" % attrs )
        baddict = {}
        badlist = []
        if not attrs:
            return True
        for attr in attrs:
            if attr not in self.hw_fields:
                badlist.append(attr)
            if attrs[attr] not in self.glossary[attr]:
                baddict[attr] = attrs[attr]
        if badlist or baddict:
            raise Exception( 
                "HICCUP:validhw: The following are invalid:keys %s, value %s" \
                % (badlist, baddict) )
        return True


    def validjob( self, num_nodes=0, kernel='default', attrs=None ):
        """
        This is a bounds check:  Will the job ever run on the system, as-is.
        """
        valid_kernel = self.validkernel( kernel )
        valid_hw = self.validhw( attrs )
        valid_job = len(self.list_available_nodes( attrs )) >= int(num_nodes)
        if valid_kernel and valid_hw and valid_job:
            return True
        return False

    
    def getreservations( self ):
        """
        This gets all the current reservations in the Heckle system.
        """
        reservations = heckle_list_reservations( session=self.session )
        print reservations


    def list_all_nodes( self ):
        """
        Heckle Glossary Function
        Produces a basic list of all the nodes
        Note: This is specific to Breadboard.
        For real installation, this would need to read from config file.
        """
        regex = re.compile("bb\d{1,2}")
        all_nodes_list = []
        for node in heckle_list_node( self.session ):
            if regex.match(node['name']):
                all_nodes_list.append(node['name'])
        all_nodes_list.sort()
        return all_nodes_list


    def glossary( self ):
        """
        Heckle Glossary Function
        gets a basic glossary of all the hardware_criteria
        gets list of all nodes, all hardware
        """
        self.node_list = self.list_all_nodes( )
        self.node_count = len(self.node_list)
        hwlist = heckle_list_hardware(self.session)
        propdict = {}
        for name in self.node_list:
            for element in hwlist:
                if name in element['nodes']:
                    for prop in element['properties']:
                        val = element['properties'][prop][0]
                        if prop not in propdict.keys():
                            propdict[prop] = []
                        if val not in propdict[prop]:
                            propdict[prop].append( val )
        return propdict


    def get_node_properties( self, node_name ):
        """
        Heckle Glossary Function
        gets all the properties of one node
        """
        #hwlist = list_hardware(session, name=node_name)  #Use if it worked...
        #return hwlist['properties']
        logstr = "HICCUP:get_node_properties:"
        #          LOGGER.debug("HICCUP:get_node_properties    &&&&&&&&&&&&")
        self.session.expire_all()
        if node_name in self.node_list:
            properties = heckle_list_node( session=self.session, name=node_name )[0]
            properties.update( heckle_list_hardware( session=self.session, name=properties['hardware'] )[0] )
            properties['mac'] = properties['mac'].replace('-',':')
            properties['mac'] = ( properties['mac'].upper() )
            return properties
        else:
            raise Exception( logstr + "No node %s recognized" % node_name )
    
    
    def get_node_bootstate( self, node_name ):
        """
        Queries Heckle to get the boot state of a node from heckle
        Returns as string
        """
        LOGGER.debug("HICCUP: get_node_bootstate")
        node_info = self.get_node_properties( node_name )
        node_state = node_info["bootstate"]
        LOGGER.info("HICCUP: get_node_bootstate: bootstate for node %s is %s" % ( node_name, node_state ))
        return node_state


def choosenodes( in_list, in_numb, forbidden ):
    """
    For now, chooses only the first n nodes in the list
        regardless of other criteria
    in_list: list of strings, nodes to choose from
    in_numb: integer, or string rep of integer
    forbidden: list of strings, forbidden nodes
    """
    in_numb = int(in_numb)
    out_list = list( set( in_list ).difference( set( forbidden ) ) )
    try:
        return out_list[ :in_numb]
    except:
        return []





























