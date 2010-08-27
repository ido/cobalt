#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Heckle-Cobalt Interface Resource Simulator
Duplicates the effects of the Heckle 

"""


HW_FIELDS = ["GPU", "MEM", "DISK", "NET", "IB", "CORES"]  #, "VINTAGE" ]

CPU = [ "intel", "opteron", "nahalem"]
GPU = [ "true" ]
MEM = [ "4GB", "12GB", "16GB" ]
DISK = [ "1", "4" ]
NET = [ "myrinet", "ib" ]
IB = [ "qdr", "sdr" ]
PACKAGE = [ "CUDA", "LINPACK" ]
GROUP = [ "cuda", "nimbus" ]
VINTAGE = []
CORES = ['1', '4', '16']

#these are mine
IMAGES = [
     "ubuntu-lucid-amd64",
     "ubuntu-hardy-amd64",
     "legacy-pxelinux",
     "eucalyptus"
     "default-bad"
     ]

FREE_NODE = str(9999999)
BUSY_NODE = str(0)
FREE_VAR = 'current reservation'

class Heckle_Interface( object ):
     """
     
     """

	_transitions = [
		('UNASSIGNED', 'POWERCYCLING'),
		('POWERCYCLING', 'BUILDING'),
		('BUILDING', 'BOOTING'),
		('BOOTING', 'COMPLETE'),
		
     def __init__( self ):
		"""
		"""
		self.NODE_LIST = NODE_LIST
		self.HW_FIELDS = HW_FIELDS
	def get_node_properties( self, name ):
		"""
		"""

class Node( object ):
	"""
	"""
     initial_state = 'UNASSIGNED'
     states = [
			'UNASSIGNED',
			'POWERCYCLING',
			'BUILDING',
			'BOOTING',
			'COMPLETE'
			]
	failure = 'CRITFAIL'
	
	def __init__( self, name ):
		"""
		"""
		self.name = name
		self.state = initial_state
		#Load from File
	def load_from_xml_file( self, filename ):
		"""
		"""
		#read in xml from file
		for child in root:
			value = self.xml_to_dict( child )
			name = child.tag
			self[name] = value
	def save_to_xml_file( self, values ):
		"""
		"""
		xml save to filename
	def _get_from_file( self, filename ):
		"""
		"""
		infile = open(filename, 'r')
		while infile:
			node = infile.readline()
			node = self.xml_to_dict( node )
			name = node['name']
			self.__setitem__( name, node )
			
	def xml_to_dict( self, in_xml ):
		"""
		"""
		key = in_xml.tag
		children = in_xml.children
		if not children:
			outval = { key: in_xml.text }
		else:
			outlist = []
			for child in children:
				outlist.append( self.xml_to_dict( child ) )
			outval = { key: outlist }
		return outval
	def dict_to_xml( self, in_dict ):
		"""
		"""
		if not root:
			#make root
		for key in in_dict.keys():
			value = in_dict[key]
			if type( value ) == ListType:
				for val in value:
					root.append( self.dict_to_xml( val )
			elif type( value ) == DictType:
				root.append( self.dict_to_xml( value ) )
			elif type( value ) == ToupleType:
				for val in value:
					root.append( self.dict_to_xml( val ) )
			else:
				root.text = str( value )
		return root
	def _to_dict( self, in_string ):
		"""
		"""
		if type(in_string) == StringType:
			outval = {}
			#strip beginning and end whitespace
			if in_string[0] == '{' and in_string[len(in_string)] == '}':
				#strip leftmost {
				#strip rightmost }
				in_list = in_string.split(',')
				for name, value in in_list:
					outval[name] = self.string_to_dict( value )
			elif in_string[0] == '[' and in_string[len(in_string)] == ']':
				outval = []
				in_list = in_string.split(',')
				for val in in_list:
					outval.append( self.string_to_dict( val )
			else:
				outval = in_string
			return outval
		elif type(in_string) == ListType:
			return in_string
		elif type(in_string) == DictType:
			return in_string
		else:
			return str(in_string)
	def __getattr__( self, name ):
		return self.__dict__[name]
	def __setattr__( self, name, value ):
		self.__dict__[name] = value
	def __getitem__( self, name ):
		return self.__dict__[name]
	def __setitem__( self, name, value ):
		self.__dict__[name] = value
	def initialize( self ):
		self.state = _initial_state
	def increment( self, name ):
		state = self.name['state']
		if state == failure:
			pass
		else:
			index = states.index( state )
			if index < len( states ):
				state = states[index + 1]
			else:
				state = failure
		self.name['state'] = state
	def get_node_properties( self, name ):
		"""
		"""
		if type(name) == ListType:
			retlist = []
			for nom in name:
				self.increment( nom )
				retlist.append( self[nom] )
			return retlist
		else:
			return self[name]
	








