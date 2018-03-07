#!/usr/bin/env python
"""Module for generating and parsing Cray ALPS messages to and from BASIL

"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import traceback

ALPS_VERSION = '1.7'
VALID_METHODS = ['RESERVE', 'CONFIRM', 'RELEASE', 'SWITCH', 'QUERY']
DEFAULT_ARCHITECTURE = 'XT'
RESERVATION_MODES = ['EXCLUSIVE', 'SHARED']


def pretty_print_xml(etree_xml):
    '''string of XML with 4-space indents'''
    xml_str = ET.tostring(etree_xml.to_xml())
    return minidom.parseString(xml_str).toprettyxml(indent='    ')

def condense_numeric_list(nums):
    '''Return a condensed list of numbers from an unordered list. Consecutive
    numbers are in the form of x-y.  Gaps are separated by "," characters. This
    is what ALPS expects for a list of numbers.

    '''
    current = []
    grouped = []
    for i in sorted(nums):
        if current == []:
            current.append(i)
            continue
        if i != (current[len(current)-1] + 1):
            if len(current) > 1:
                grouped.append([min(current), max(current)])
            else:
                grouped.append([current[0]])
            current = [i]
        else:
            current.append(i)
    #make sure we get the last set added to grouped.
    if len(current) > 1:
        grouped.append([min(current), max(current)])
    elif len(current) == 1:
        grouped.append([current[0]])
    return grouped

def expand_numeric_list(num_list_str):
    '''take a list of values of the form of [x, y-z, ...]
    where y-z are a contiguous group of integers.  Expand into a  list of the
    actual values.

    '''
    retlist = []
    for entry in num_list_str.split(','):
        if entry.isdigit():
            retlist.append(int(entry))
        else: #have to unpack a list
            vals = entry.split('-')
            retlist.extend(range(int(vals[0]), int(vals[1])+1))
    return retlist

class XMLGeneratorMixin(object):
    '''Generic XML generator for Cray ALPS messages.  This uses instance
    variables that are a part of this module's various subclasses.  Only
    variables that are included in attributes will be added as attributes.

    '''
    hyphened = [] #These need to have '_' converted to '-'.
    required = [] #Exception out if we don't have these present
    attributes = {} #variables with default values are set

    def __init__(self, params):
        '''Default initializer.  Raise a KeyError if required parameters are
        omitted, otherwise, add attributes with defaults to the class
        dictionary.  Subelements need to be explicitly set in the child
        subclasses.

        '''
        #May raise key errors.  Let caller handle those
        for key, val in self.attributes.items():
            if key in self.required and key not in params.keys():
                raise KeyError("Required key %s not found in params." % key)
            setattr(self, key, params.get(key, val))
        self.subelements = []
        self.empty_subelements = []
        self.text = None

    def to_xml(self):
        '''Convert to an expected xml_message'''
        retxml = ET.Element(self.__class__.__name__)
        for key in self.attributes.keys():  #fetch off of instance dict
            val = self.__dict__[key]
            if val is None:
                continue
            if key not in self.hyphened:
                retxml.set(key, str(val))
            elif key in self.hyphened:
                retxml.set(key.replace('_','-'), val)
        for subelem in self.subelements:
            retxml.append(subelem.to_xml())
        if self.text is not None:
            retxml.text = self.text
        return retxml

    def __str__(self):
        return pretty_print_xml(self)

#Exceptions
class InvalidBasilMethodError(Exception):
    '''An invalid ALPS Basil method was requested.'''
    pass

class ALPSError(Exception):
    '''Exception for an ALPS'''

    def __init__(self, msg, severity, status=None, error_class=None,
            error_source=None):
        super(ALPSError, self).__init__(msg)
        self.severity = severity
        self.status = status
        self.error_class = error_class
        self.error_source = error_source
        self.msg = msg

def gen_request(method, params, type=None):
    '''generate a BASIL request xml string'''
    return BasilRequest(method, type, params).to_xml()

#Request marshaller
class BasilRequest(XMLGeneratorMixin):
    '''Wrapper class for request messages for BASIL.  Once generated, this may
    be used to generate the proper XML to send to BASIL's stdin'''

    #Note: admin cookie corresponds to pagg_id.
    #job_name is intentionally omitted. We are not supporting 1.0 at this time.
    attributes = {'protocol': ALPS_VERSION, 'method': None, 'type': None,
            'reservation_id': None, 'admin_cookie': None, 'pagg_id': None}

    def __init__(self, method=None, type=None, params=None):
        if params is None:
            params = {}
        super(self.__class__, self).__init__(params)
        self.pagg_id = None
        self.reservation_id = None
        self.method = method.upper()
        if self.method not in VALID_METHODS:
            raise InvalidBasilMethodError("%s is not a valid method" % \
                    self.method)
        if 'QUERY' == self.method:
            if type is None:
                raise ValueError('type must be specified for QUERY requests.')
            self.type = type.upper()
            getattr(self, self.type.lower())(params)
        else:
            getattr(self, self.method.lower())(params)

    def system(self, params):
        '''Generate QUERY SYSTEM message for BASIL'''
        pass #all done at top-level

    def reserve(self, params):
        '''Generate RESERVATION message for BASIL'''
        self.subelements.append(ReserveParamArray(params))

    def confirm(self, params):
        '''confirm an ALPS reservation'''
        for key in ['pagg_id', 'reservation_id']:
            if key not in params.keys():
                raise KeyError("%s required key for confirm not found. %s" %
                        (key, params))
        self.pagg_id = params['pagg_id']
        self.reservation_id = params['reservation_id']


    def release(self, params):
        '''release an ALPS reservation'''
        for key in ['reservation_id']:
            if key not in params.keys():
                raise KeyError("%s required key for release not found." % key)
        self.reservation_id = params['reservation_id']

    #QUERY Methods
    def inventory(self, params):
        if params is None:
            params = {}
        self.empty_subelements = ['Inventory']
        self.subelements.append(Inventory(params))

    def status(self, params):
        #top level
        pass

    def topology(self, params):
        self.empty_subelements = ['Topology']
        self.subelements.append(Topology(params))

    def summary(self, params):
        #all is at the top level
        pass

    def engine(self, params):
        #all is at the top level
        pass

    def reservednodes(self, params):
        #all handled at top level
        pass

class ReserveParamArray(XMLGeneratorMixin):

    required = ['user_name', 'batch_id']
    attributes = {'user_name': None, 'batch_id': None}

    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        self.subelements.append(ReserveParam(params))
        self.attributes = {'user_name': params['user_name'],
                           'batch_id': params['batch_id']}
        account_name = params.get('account_name', None)
        if account_name is not None:
            self.attributes['account_name'] = account_name

class ReserveParam(XMLGeneratorMixin):

    hyphened = ['p_state', 'p_govenor']
    required = ['width',]
    attributes = {'architecture': DEFAULT_ARCHITECTURE, 'width': None,
            'depth':None, 'nppn': None, 'nnpn': None, 'nnps': None, 'nspn': None,
            'oscpn': None, 'reservation_mode': None, 'gpc_mode': None,
            'nncpu': None, 'p_state': None, 'p_govenor': None}

    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        if 'node_list' in params:
            self.subelements.append(NodeParamArray(params))

class NodeParamArray(XMLGeneratorMixin):
    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        self.subelements.append(NodeParam(params))

class NodeParam(XMLGeneratorMixin):

    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        #Raise key errors if information not valid
        self._node_list = params['node_list']
        self.text = self.node_list

    @property
    def node_list(self):
        '''Convert a list of nodes into something that ALPS expects'''
        grouped = condense_numeric_list(self._node_list)
        return ','.join(['-'.join(
            [str(i) for i in group]) for group in grouped])

    def __str__(self):
        return ET.tostring(self.to_xml())

class Application(XMLGeneratorMixin):
    '''Application instructions for the "SWITCH" query method'''
    required = ['application_id', 'action']
    attributes = {'application_id': None, 'action': None}

    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        if params['action'] not in ['IN', 'OUT']:
            raise ValueError('application action must be one of "IN" or "OUT".')

class Inventory(XMLGeneratorMixin):

    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        na_params = {}
        if 'changecount' in params:
            na_params['changecount'] = params['changecount']
        if not 'nonodes' in params:
            self.subelements.append(NodeArray(na_params))
        if 'resinfo' in params and params['resinfo']:
            #sending an empty ReservationArray in this message is how you query
            #the system for ongoing ALPS reservations, apparently.
            self.subelements.append(ReservationArray({}))

class NodeArray(XMLGeneratorMixin):

    attributes = {'changecount': None}
    def __init__(self, params):
        super(self.__class__, self).__init__(params)

class ReservationArray(XMLGeneratorMixin):
    def __init__(self, params):
        super(self.__class__, self).__init__(params)

class Topology(XMLGeneratorMixin):
    attributes = {'name':None}
    def __init__(self, params):
        super(self.__class__,  self).__init__(params)
        if 'topology_name' in params:
            self.name = params['topology_name']
        self.subelements.append(FilterArray(params))

class FilterArray(XMLGeneratorMixin):
    def __init__(self, params):
        super(self.__class__, self).__init__(params)
        if 'filters' not in params:
            raise KeyError("No filters specified for filter array.")
        for filter_params in params['filters']:
            self.subelements.append(Filter(filter_params))

class Filter(XMLGeneratorMixin):
    attributes = {'name': None}
    def __init__(self, params):
        super(self.__class__, self).__init__(params)

#Response parsing
def parse_engine_response(xml, retdict):
    '''Parse the ENGINE query response.

    The key information returned is the protocol versions in use, and whether
    ALPS is in-use as well as the ALPS version in-use.

    '''
    retdict.update(xml.find('Engine').attrib)
    return retdict

def parse_reserved_response(xml, retdict):
    '''Parse RESERVED messages.

    Note: the ReservedNodeArray is returned as a list 'reserved_nodes' where
    each element is the id of each reserved node.  This list is expanded from
    compact Cray representations.

    '''
    retdict.update(xml.find('Reserved').attrib)
    reserved_array = xml.find('Reserved/ReservedNodeArray')
    retdict['reserved_nodes'] = []
    if reserved_array is None:
        #handle version >=1.6
        reserved_nodes = xml.find('Reserved/ReservedNodes').text
        retdict['reserved_nodes'] = [str(i) for i in
                expand_numeric_list(reserved_nodes.strip())]
    else:
        for reserved_node in reserved_array:
            retdict['reserved_nodes'].append(reserved_node.attrib['node_id'])
    return retdict

def parse_confirmed_response(xml, retdict):
    '''Parse a confirmed message.

    This message may or may not include a reservation_id and pagg_id.  The specs
    contradict themselves here.

    '''
    retdict.update(xml.find('Confirmed').attrib)
    return retdict

def parse_released_response(xml, retdict):
    '''Parse a released message.

    There really isn't much to this message.  The important bit is the check to
    make sure that the message was processed successfully.  The attribute
    addition is future-proofing, but may have a reservation_id and a "claim"
    count against the current reservation.

    '''
    retdict.update(xml.find('Released').attrib)
    return retdict

def parse_system_response(xml, retdict):
    '''parse system response from QUERY SYSTEM request'''
    retdict.update(xml.find('System').attrib)
    nodeinfo_list = []
    for child in xml.find('System'):
        nodeinfo = {}
        nodeinfo.update(child.attrib)
        nodeinfo['node_ids'] = child.text.strip()
        nodeinfo_list.append(nodeinfo)
    retdict['nodes'] = nodeinfo_list
    return retdict


def parse_inventory_response(xml, retdict):
    '''Parse inventory response query.

    This will return information about system hardware and reservations.

    '''
    retdict.update(xml.find('Inventory').attrib)
    node_array = xml.find('Inventory/NodeArray')
    if node_array is not None:
        retdict.update(node_array.attrib)
        node_array = node_array.getchildren()
    reservation_array = xml.find('Inventory/ReservationArray')
    if reservation_array is not None:
        retdict.update(reservation_array.attrib)
        reservation_array = reservation_array.getchildren()
    if node_array is not None:
        retdict['nodes'] = []
        for node in node_array:
            retdict['nodes'].append(get_info(node))
    if reservation_array is not None:
        retdict['reservations' ] = []
        for reservation in  reservation_array:
            retdict['reservations'].append(get_info(reservation))
    return retdict


def get_socket_info(xml_nodes):
    retdict = {'segments': []}
    retdict.update(xml_nodes.attrib)
    segment_array = xml_nodes.find('SegmentArray').getchildren()
    for segment in segment_array:
        parsed_seg = dict(segment.attrib)
        parsed_seg.update(get_processor_info(segment.find('ProcessorArray')))
        parsed_seg.update(get_memory_info(segment.find('MemoryArray')))
        parsed_seg.update(get_label_info(segment.find('LabelArray')))
        retdict['segments'].append(parsed_seg)
    return retdict

def get_info(elem):
    retdict = {}
    if elem.attrib is not None and elem.attrib != {}:
        retdict.update(elem.attrib)
    if elem.text is not None and not elem.text.isspace() and elem.text != '':
        retdict['text'] = elem.text
    for subelem in elem:
        if retdict.get(subelem.tag) is None:
            retdict[subelem.tag] = [get_info(subelem)]
        else:
            retdict[subelem.tag].append(get_info(subelem))
    return retdict


def get_node_info(xml_nodes):
    retdict = {'sockets': []}
    retdict.update(xml_nodes.attrib)
    segment_array = xml_nodes.find('SocketArray').getchildren()
    for segment in segment_array:
        parsed_seg = dict(segment.attrib)
        parsed_seg.update(get_processor_info(segment.find('ProcessorArray')))
        parsed_seg.update(get_memory_info(segment.find('MemoryArray')))
        parsed_seg.update(get_label_info(segment.find('LabelArray')))
        retdict['segments'].append(parsed_seg)
    return retdict

def get_processor_info(xml_procs):
    retdict = {'processors': []}
    for proc in xml_procs.getchildren():
        parsed_proc = dict(proc.attrib)
        proc_allocation = proc.find('ProcessorAllocation')
        if proc_allocation is not None:
            parsed_proc['processor_allocation'] = dict(proc_allocation.attrib)
        retdict['processors'].append(parsed_proc)
    return retdict

def get_memory_info(xml_mem):
    retdict = {'memory': []}
    for mem in xml_mem.getchildren():
        parsed_mem = dict(mem.attrib)
        mem_allocation = mem.find('MemoryAllocation')
        if mem_allocation is not None:
            parsed_mem['memory_allocation'] = dict(mem_allocation.attrib)
        retdict['memory'].append(parsed_mem)
    return retdict

def get_label_info(xml_labels):
    #The spec disagrees with the XML test sample from Cray.
    retdict = {'labels': []}
    if xml_labels.text is not None:
        retdict['label_text'] = xml_labels.text
    for label in xml_labels.getchildren():
        parsed_label = dict(label.attrib)
        parsed_label['text'] = label.text
        retdict['labels'].append(parsed_label)
    return retdict

def get_reservation_info(xml_res):
    retdict = dict(xml_res.attrib)
    retdict['applications'] = []
    for app in xml_res.find('ApplicationArray'):
        retdict['applications'].append(get_app_info(app))
    return retdict

def get_app_info(xml_app):
    retdict = dict(xml_app.attrib)
    retdict['commands'] = []
    for cmd in xml_app.find('CommandArray'):
        retdict['commands'].append(get_cmd_info(cmd))
    return retdict

def get_cmd_info(xml_app):
    retdict = dict(xml_app.attrib)
    return retdict


def detect_error_message(xml):
    '''find any error message, package up and raise as exception.

    text is exception text. Other information as vars in exception itself.

    '''
    msg = xml.find('Message')
    if msg is not None:
        raise ALPSError(msg.text, msg.get('severity'),
                xml.get('status'), xml.get('error_class'),
                xml.get('error_source'))
    return

def parse_response(response):
    '''Generate a dictionary summary of an ALPS message for use elsewhere in
    Cobalt.  It should be noted that every value in here is a string, and this
    function does not attempt to coerce to whatever the correct type is.
    Converting to correct types is the responsibility of the caller.

    Input:
        response: The XML response string from BASIL.  This may be any method.

    Output:
        A dictionary.  The following fields must exist:
        protocol - the protocol version of the message.
        method - the BASIL method that generated the message.
        status - the status of the call.  SUCCESS indicates normal return.

        * "Array" elements will come back as lists of subelements
        * subelements with attributes will be returned as a dictionary of
            attributes with a 'text' member for any text
        * subelements without attributes will be the text string
        * All values are returned as strings.

    Exceptions:
        A ValueError may be raised for malformed messages from BASIL.

    '''

    msg_xml = ET.fromstring(response)
    retdict = {}
    retdict['protocol'] = msg_xml.attrib['protocol']
    msg_xml = msg_xml.find('ResponseData')
    retdict.update(msg_xml.attrib)
    detect_error_message(msg_xml)
    if len(msg_xml) == 1:
        for subelem in msg_xml:
            retdict['type'] = subelem.tag
    else:
        raise ValueError("Unknown Response from ALPS")
    parse_map = {'Engine': parse_engine_response,
                 'Reserved': parse_reserved_response,
                 'Confirmed': parse_confirmed_response,
                 'Released': parse_released_response,
                 'Inventory': parse_inventory_response,
                 'System': parse_system_response,
                }
    return parse_map[retdict['type']](msg_xml, retdict)


if __name__ == '__main__':
    with open('/home/richp/alps-simulator/tester/systemreq') as f:
    #with open('inventory.xml') as f:
        xml_str = ''.join([l for l in f])
        xml = ET.fromstring(xml_str)

    print get_info(xml)


    EXEC = '/home/richp/alps-simulator/apbasil.sh'
    import subprocess
    basil_str = BasilRequest('query', 'system')
    print '*'*80
    print basil_str
    p = subprocess.Popen(EXEC, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE)
    out, err = p.communicate(str(basil_str))
    print "stdin: ", basil_str
    print "stdout: ", out
    print "stderr: ", err

    print parse_response(out)
