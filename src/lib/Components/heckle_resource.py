#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Heckle-Cobalt Interface Resource Object Collection
Contains the ResourceDict, Resource object, Glossary object, and Attribute object.
Encapsulates Node information, together with the methods to change and compare them.

"""




#############################
### 
### Future Work:
### 1)  Change string to xml
### 2)  Change save to xml
### 3)  Improve the scoring algorithm
### 
#############################



from types import *
import re
import os

try:
     from Cobalt.Components.heckle_lib import *
except:
     pass


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

class ResourceDict(object):
     """
     Object to contain and encapsulate the Resources in the system
     """
     def __init__( self, in_dict=None ):
          self.resource_dict = {}
          self.glossary = Glossary()
          print "RD:__INIT__: type %s, value %s" % (type(in_dict), in_dict)
          if type(in_dict) is NoneType:
               pass
          elif type(in_dict) is DictType:
               #print "Incomming: %s" % in_dict
               for key in in_dict:
                    self.add(in_dict[key])
          elif type(in_dict) is ListType:
               #print "Incomming: %s" % in_dict
               for val in in_dict:
                    self[val['name']]=val
          elif type(in_dict) is Resource:
               name = in_dict['name']
               print "RD:__INIT__: Resource, name is %s" % name
               self.resource_dict[name] = in_dict
               print "Resources are now: " % self.resource_dict
          elif type(in_dict) == ResourceDict:
               #print "Incomming: %s" % in_dict
               for name in in_dict.keys():
                    self[name] = in_dict[name]
          else:
               raise Exception( "RD: Incorrect assignment type %s; only takes Resource or Dictionary, or list therein." % type(in_dict) )
          #self.update()
     def __str__( self ):
          """
          Returns a string representation of all resources in the system
          """
          retstr = "Resources: ["
          res_len = str(self.resource_dict)
          retstr += "]\nGlossary: "
          retstr += str(self.glossary)
          return retstr
     def _get_dict( self, glossary=True, resources=True ):
          """
          Returns a dictionary version of the entire Resource Dictionary
          
          """
          if glossary and not resources:
               return self.glossary._get_dict()
          elif resources and not glossary:
               return self.resource_dict
          retdict = {}
          if glossary:
               retdict['Glossary'] = self.glossary._get_dict()
          if resources:
               retdict['Resources'] = self.resource_dict
          return retdict
     def __getitem__( self, name ):
          """
          Finds one particular resource by name
          Returns that resource, or False if no resource by that name.
          """
          print "RD: __getitem__: Looking for name %s of type %s" % (name, type(name) )
          if name in self.keys():
               print "RD: __getitem__: Found name %s" % name
               print "Index is %s" % self.keys().index(name)
               print "Index is %s" % self.resource_dict.keys().index(name)
               print "Resource Dict is %s" % self.resource_dict
               resource = self.resource_dict[name]
               print "RD:__getitem__: Returning type %s, value %s" % (type(resource), resource)
               return resource
          else:
               raise Exception ( "RD: GetItem: No resource named %s exists." % name )
     def __getattr__( self, name ):
          """
          """
          print "RD:_getattr_: %s" % name
          return self.__dict__[name]
     def keys( self ):
          """
          Returns a list of strings containing the names of all the nodes
          Node names must be unique
          """
          return self.resource_dict.keys()
     def name_list( self ):
          """
          Returns a list of strings containing the names of all the nodes
          Node names must be unique
          """
          return self.resource_dict.keys()
     def node_count( self ):
          """
          returns the number of resources / nodes in the current system
          """
          return len(self.resource_dict)
     def __add__( self, attributes=None, resource=None ):
          """
          Mathmatical / symbolic addition
          Adds a new Resource to the system
          Attributes is a dictionary of strings, key:value
          MUST contain a Name field, and names MUST be unique across the system
          """
          return self.add(attributes=attributes, resource=resource)
     def add( self, attributes ):
          """
          Adds a new Resource to the system
          Attributes is a dictionary of strings, key:value
          MUST contain a Name field, and names MUST be unique across the system
          """
          print "RD:Add: Attributes of type %s are %s" % (type(attributes), attributes)
          if type(attributes) == ListType:
               for att in attributes:
                    self.add(att)
          if type(attributes) == DictType:
               attributes = Resource( attributes )
          if type(attributes) == Resource:
               name = attributes.name
               print "RD:Add: Looking for %s" % name
               if name in self.keys():
                    print "RD:Add: %s is found, updating" % name
                    self.resource_dict[name].update( attributes )
               else:
                    print "RD:Add: %s not found, adding to list" % name
                    self.resource_dict[name]= attributes
                    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Done &&&&&&&&&&&&&&&&&&&&&"
               print "RD1:%s" % self.resource_dict[name]
               print "RD2:%s" % self.keys()
               print "%s" % self[name]
          else:
               raise Exception( "Resource Dictionary: Add: Something else happened... %s" % attributes )
     def update( self, attributes=None, nodelist=None ):
          """
          Changes the resource with the attributes named
          If attributes is a list or a dictionary, pass on to the set_item function
          If attributes is None, then call on Heckle to get an updated node status
          else, return an error.
          """
          #try:
          #     print "RD: Updating: Resource %s of type %s" % ( attributes['name'], type(attributes) )
          #except:
          #     pass
          att_type = type(attributes)
          if att_type is DictType:
               new_resource = Resource( attributes )
               self.update( new_resource )
          elif att_type is Resource:
               print "RD: Update: Resource is %s" % attributes
               name = attributes['name'].value
               if name in self.keys():
                    print "RD: Update: Keys are %s" % self.keys()
                    print "RD: Update: Going to update %s" % name
                    self[name].update( attributes )
               else:
                    print "RD: Update: Goind to add %s" % name
                    self.add( attributes )
          elif att_type is ListType:
               for att in attributes:
                    resource = Resource( att )
                    self.update( resource )
          elif att_type is NoneType:
               self.get_heckle_list( nodelist=nodelist )
               return True
          else:
               raise Exception( "ResourceDict:Update: Attributes must be dictionary or lists of dictionaries; your attribute set for this is %s." % att_type )
     def __setitem__( self, attributes, name=None ):
          """
          Sets the resource indicated to the value indicated
          Attributes is to be a dictionary, or list of dictionaries with each resource having one dictionary.
          Algorythm:
               If attributes is a list of resources, then iterate through the list, setting each.
               If attributes is a dictionary of key:value pair(s), where the key is a resource name
                    and the value is a dictionary of key:value pairs for attributes, then set these.
               else, return an error.
               ###
               ###   For now, assume name matches attribute['name']
               ###
          """
          if name:
 #              #print "RD: SetItem: Name is %s" % name
               pass
          if attributes:
 #              #print "RD: SetItem:  Attributes is %s" % attributes
               pass
          att_type = type(attributes)
 #         #print "Attributes type is %s" % att_type
          if att_type == Resource:
               self.resource_dict[attribute['name']].update(attribute)
          if att_type == ListType:              # if we're dealing with a list of resources to set
               for resource in attributes:
                    self.update(attributes[resource])
                    self.glossary.append(attributes[resource])
          elif att_type == DictType:            # if we're dealing with a dictionary for one resource
  #             #print "Add %s as dictionary" % attributes['name']
               name = attributes['name']
               if name not in self.keys():
                    self.glossary.append(attributes)    #Add to glossary if new
                    self.resource_dict[name] = Resource( attributes )
               else:
                    self.resource_dict[name].update( attributes )
          return True
     def __sub__(self, attributes=None, resource=None ):
          """
          Removes a resource from the current system
          Accepts either a dictionary of attributes, or a resource object
          """
          return self.remove(attributes=attributes, resource=resource)
     def remove( self, attributes ):
          """
          Removes a resource from the current system
          Accepts either a dictionary of attributes, or a resource object
          """
          try:
               name = attributes['name']
               if name in self.keys():
                    del(self.resource_dict[name])
               return True
          except:
               return False
     def getfreenodes( self ):
          """
          This function returns a list of nodes marked free in the system
          """
          name_list = []
          ##print "Resource Dict is: %s" % self.resource_dict
#          #print "#####  Type is %s" % type(self.resource_dict)
          for res in self.resource_dict:
#               #print "getfreenodes: res is %s of type %s" % (res, type(res))
#               #print "self.res is %s with values %s" % (type(self[res]), self[res])
               if self[res].isfree():
                    name_list.append(res)
          return sorted(name_list)
     def allocate( self, nodes, job_id=None):
          """
          Sets the node to allocated; i.e., sets reservation to true
          This marks a node as unavailable, and will not be chosen in the future.
          nodes is a list of strings, containing the node names.
          """
          if not job_id:
               job_id = BUSY_NODE
          for node in nodes:
               #print "&&&&&&&&&&&      Found it!  Node %s is %s, switch to %s" % (node, self[node][FREE_VAR], job_id)
               old_resource = self[node]
               #print "Type of old resource is %s, for value %s" % (type(old_resource), old_resource[FREE_VAR])
               new_att = Attribute()
               new_att.name = FREE_VAR
               new_att.value = job_id
               att2 = Attribute( FREE_VAR, job_id )
               #print "Allocate: comparing them yeilds %s" % (new_att == att2)
               old_resource.update( att2 )
#               old_resource[FREE_VAR] = job_id
               #print "Old resource now reads %s" % old_resource[FREE_VAR]
               self[node].update(old_resource)
               #print "Node %s now reads %s" % (node, self[node][FREE_VAR])
          return True
     def free( self, nodes, job_id=None):
          """
          Sets the nodes(s) to unallocated; i.e., sets reservation to None
          This marks the node as available.
          nodes is a list of strings, containing the node names.
          """
          for node in nodes:
               self[node][FREE_VAR] = FREE_NODE
          return True
     def __eq__( self, attributes, scored=False ):
          """
          Returns a list of nodes which match the attributes
          Attributes is a dictionary of strings
          """
          retlist = []
          other = Resource( attributes )
          #print "RD: __eq__: Attributes are %s, and of type %s" % (other, type(other))
          for key in self.keys():
               if self[key] == other:
                    retlist.append(key)
          #print "RD: __eq__:  Returning %s" % retlist
          if scored:
               retlist = self.Glossary.scorelist( retlist )
          else:
               def resourcesort( key2 ):
                    print "Key is %s, Name is: %s" % (key2, self[key2].name)
                    return self[key].name
               retlist.sort( key2=resourcesort )
               #pass
          return retlist
     def __ge__( self, attributes, scored=False ):
          """
          Returns a list of nodes which are greater than or equal to the attributes
          Attributes is a dictionary of strings
          """
          retlist = []
          #print "RD:__ge__:Attributes are %s, and of type %s" % (attributes, type(attributes))
          other = Resource( attributes )
          print "RD:__ge__:Other is %s, and of type %s" % (other, type(other))
          for key in self.keys():
               retval = self[key]
               print "RD:__ge__: Comparing to node %s" % self[key]
               if self[key] >= other:
                    #print "RD: __ge__: Found Node %s with free variable %s versus %s" % (key, self[key][FREE_VAR], attributes[FREE_VAR])
#                    #print "RD: __ge__: Type self[key] is %s, other is %s" % ( type(self[key]), type(other) )
                    retlist.append(key
)
          print "__ge__: Returning %s" % retlist
          if scored:
               retlist = self.Glossary.scorelist( retlist )
          else:
               def resourcesort( key2 ):
                    newres = self[key2]
                    print "Key is %s, Name is: %s" % (key2, newres.name)
                    return newres.name
               retlist.sort( key=resourcesort )
               #pass
          return retlist
     def backup( self ):
          """
          Saves the current state to a file
          """
          FILENAME = "~/backup.txt"
          outfile = os.open(FILENAME, 'w')
          for res in self.resource_dict:
               outfile.write(str(res))
          outfile.close()
     def restore_from_backup( self ):
          """
          Restores the status from backup
          Useful for either BreadBoard-style setup or testing
          """
          FILENAME = "~/backup.txt"
          infile = os.open(FILENAME, 'r')
          for line in infile:
               self.add( Resource( line ))
          outfile.close()
     def get_heckle_list( self, nodelist=None ):
          """
          Gets the current state and status of everything in Heckle
          """
          print "\n\nUpdating from Heckle...\n\n"
          HICCUP = Heckle_Interface()
          if not nodelist:
               node_list = HICCUP.NODE_LIST
          node_list.sort()
          print "RD: GHL: Node List is: %s" % node_list
          keylist = self.keys()
          print "RD: GHL: current node list is %s" % keylist
          for node_name in node_list:
               node_value = HICCUP.get_node_properties( node_name )
               print "Type of values is %s" % type(node_value)
               print "RD: GHL: %s has value %s" % ( node_name, node_value )
               print "Name is %s" % node_value['name']
               if str(node_value[FREE_VAR]) == 'None':
                    #print "Bingo!"
                    node_value[FREE_VAR] = FREE_NODE
               elif not node_value[FREE_VAR]:
                    #print "Other One!"
                    node_value[FREE_VAR] = FREE_NODE
               resource = Resource( node_value )                         
               print "RD: GHL: Resource %s / %s is now %s" % ( resource['name'], resource.name, resource )
               resource_keylist = resource.keys()
               for res_key in resource_keylist:
                    print "Value %s is %s" % (res_key, resource[res_key])
               if node_name in keylist:
                    print "RD:GHD: Nodename %s in keylist, updating" % node_name
                    self.update( resource )
               else:
                    print "RD:GHD: Nodename %s not in keylist, adding" % node_name
                    self.add( resource )
               print "RD: get_heckle_list: node now reads %s" % self[node_name]
          print "RD: Update from Heckle: %s" % nodelist
          return True






class Resource(object):
     """
     Representation of a single Node in the Heckle System
     Also acts as a dictionary for attributes it contains
     """
     def __init__( self, attributes=None ):
          """
          Initializes values
          Attributes is a dictionary of key:value for each attribute
          KISS
          """
          self.attribute_list = []
          self.attribute_list.append( Attribute( 'name', 'Default' ) )
          #print "Attributes are: %s" % attributes
          if not attributes:
               pass
          else:
               if type(attributes) == Attribute:
                    self.__setitem__( attributes )
               elif type( attributes ) == Resource:
                    keylist = attributes.keys()
                    print "Resource:__INIT__:Resource: keys are %s" % keylist
                    for key in keylist:
                         new_att = Attribute( key, attributes[key] )
                         print "Resource:__INIT__:Resource: Adding Attribute %s:%s:%s" % (new_att.name, type(new_att), new_att.value)
                         self.__setitem__( new_att )
                         print "Resource:__INIT__:Resource: That attribute now reads %s" % self[key]
               elif type( attributes ) == DictType:
                    print "Resource: __INIT__:Dict: attribute is %s" % attributes
                    keylist = attributes.keys()
                    print "Resource:__INIT__:Dict: keylist is %s" % keylist
                    for key in keylist:
                         new_att = Attribute( key, attributes[key] )
                         print "Resource: __INIT__:Dict: attribute now reads %s" % new_att
                         if key in self.keys():
                              self.attribute_list.remove( self.attribute_list[ self.get_index( key ) ] )
                         self.attribute_list.append( new_att )
                         print "Resource:__INIT__:Dict: Resource attribute now reads %s" % self[key]
                         if not self[key] == new_att:
                              print "Resource:__INIT__:Dict: #### WARNING ##### Values %s and %s do not match!" % (self[key], new_att)
     def get_index( self, name):
          """
          Returns the index of the key in the resource list
          """
          for att in self.attribute_list:
               if att.name == name:
                    #print "Found it!"
                    return self.attribute_list.index(att)
          else:
               return -1
     def __str__( self ):
          """
          Returns a string representation of the object
          """
          return str(self._get_dict())
     def _get_dict( self ):
          """
          Returns a dictionary representation of the object
          """
          retdict = {}
          for att in self.attribute_list:
               retdict[att['name']] = att.value
          return retdict
     def __getitem__( self, name ):
          """
          Allows getting an item directly by subscription
          """
#         #print "Debug: Name is %s" % name
          try:
               index = self.get_index(name)
               #print "RD: Get Item: Found %s at %s" % (name, index)
               return self.attribute_list[index]
          except Exception as ee:
               raise Exception("RD: GetItem: Value %s does not exist: %s" % (name, ee))
     def __setitem__( self, key, value=None):
          """
          Direct Assignment of key-value pairs
          Adds the key:value pair to the attributes
          Will not add duplicate keys
          """
          if type(key) == Attribute:
               new_att = key
               key = new_att.name
          elif type(key) == DictType:
               new_att = Attribute( key['name'], key['value'] )
               key = key['name']
          else:
               new_att = Attribute( key, value )
          index = self.get_index( key )
          if index:
               self.attribute_list[index] = new_att
          else:
               self.attribute_list.append( new_att )
          return True
     def __add__(self, key, value ):
          """
          Absolutely adds the key:value pair to the attributes
          Will add duplicate values
          """
          new_attribute = Attribute( key, value )
          return self.add_attribute( new_attribute )
     def add_attribute( self, attribute ):
          """
          Absolutely adds the key:value pair to the attributes
          Will add duplicate values
          """
          #print "Resource:Add_attribute: New Attribute is %s -- %s" % ( attribute.name, attribute.value )
          key = attribute.name
          index = self.get_index( attribute.name )
          print "Index is: %s" % index
          if index >-1:
               print "Resource:Add_attribute: Pre: Exists, is %s of type %s" % (self[key], type(self[key]))
               self[key].add( attribute.value )
          else:
               print "Resource:Add_attribute: %s Does not currently exist, adding..." % key
               self.attribute_list.append( attribute )
          print "Resource: Add_attribute: POST: Key is %s, value is now %s" % (key, self[key].value)
          return True
     def update( self, attributes ):
          """
          Updates an item in the current resource
          Attributes is a dictionary or resource object, with key:value pairs
          """
          #print "Resource: Update: attributes are %s" % attributes
          newRes = Resource( attributes )
          #print "Resource: Update: New resource is %s" % newRes
          keylist = newRes.keys()
          print "Resource: Update: Keylist is %s" % keylist
          for key in newRes.keys():
               if key == 'name':
                    pass
               elif key in self.keys():
                    self.__setitem__( newRes[key] )
               else:
                    self.add_attribute(newRes[key])
          return True
     def del_attribute( self, key ):
          """
          Removes a given attribute from the resource
          """
          try:
               attribute = self[key]
               self.attribute_list.remove(attribute)
          except:
               pass
     def __getattr__ ( self, key ):
          """
          Gets all attribute objects for a given key
          """
          #print "get attribute Key is %s" % key
          return self[key]
     def keys( self ):
          """
          Returns a list of unique keys for the attributes in this Resource
          """
          return_list = []
          for attribute in self.attribute_list:
               return_list.append( attribute.name )
          return return_list
     def _get_value( self, key ):
          """
          Gets all the attribute values for a given key
          """
          return self[key]
     def isfree( self ):
          """
          This function simply returns those nodes listed as free
          """
          return self[FREE_VAR] == FREE_NODE
     def __eq__( self, other ):
          """
          Compares the resource to see if they match
          Can check against another Resource or a Dictionary of attributes
          """
  #        print "Resource: __eq__: %s" % other
          other_resource = Resource(other)
          for key in other_resource.keys():
               if key == 'name':
                    pass
               else:
                    try:
                         if self[key] == other_resource[key]:
                              pass
                         else:
                              return False
                    except:
                         return False
          #print "Resource: __eq__: %s == %s reads True" % (self[FREE_VAR], other_resource[FREE_VAR])
          return True
                    
     def __ge__( self, other ):
          """
          Compares this resource, attribute-by-attribute, against
          another Resource or a Dictionary of attributes.
          Determines if this resource is greater than or equal to the other
          """
  #        print "Resource: __ge__: %s" % other
          other_resource = Resource(other)
          keylist = other_resource.keys()
          for key in keylist:
               if key == 'name':
                    pass
               else:
                    try:
                         if self[key] >= other[key]:
                              pass
                         else:
                              return False
                    except:
                         return False
          #print "Resource: __ge__: %s >= %s reads True" % (self[FREE_VAR], other[FREE_VAR])
          return True
     



class Attribute(object):
     """
     Object which encapsulates any one value of a resource.
     It takes care of its own comparisons and representations
     Accepts strings, or list of strings
     """
     def __init__( self, name="Default", value="" ):
          self.name = ""
          self.value = ""
          if type(name) == Attribute:
               self.name = name.name
               self.value = name.value
          else:
               self.__setitem__( name, value )
     def __repr__( self ):
          """
          """
          return str(self.value)
     def __str__( self ):
          """
          Returns the string representation of the current object
          """
          return str(self.value)
          #return "'%s':'%s'" % (self.name, self.value)
     def __getitem__( self, name ):
          """
          Allows getting an item by subscription
          """
          try:
               return self.__dict__[name]
          except:
               raise Exception("No value %s in attribute, only %s" % (name, self))
     def __getattr__( self, name ):
          """
          """
          try:
               return self.__dict__[name]
          except:
               return False
     def __setitem__( self, name, value=None ):
          """
          Direct assignment of an item
          """
          try:
               if self.name == name:
                    if type(value) == ListType:
                         self.value = []
                         for val in value:
                              self.value.append(str(val))
                    else:
                         self.value = str(value)
               else:
                    raise Exception( "You're trying to turn a %s into a %s!" % (self.name, name) )
          except:
               self.name = name
               self.value = str(value)
          return True
     def __setattr__( self, name, value ):
          """
          ABSOLUTELY replaces the value with the intended value
          """
          if type(value) == ListType:
               for val in value:
                    val = str(val)
          else:
               value = str(value)
          self.__dict__[name] = value
     def add( self, attribute ):
          """
          Adds an attribute to the current, if it matches.
          """
          #print "Attribute: Add: Adding %s of type %s" % ( attribute, type(attribute))
          if type(attribute) == Attribute or type(attribute) == DictType:
               return self.__add__( attribute['value'] )
          else:
               return self.__add__( attribute )
                    
     def __add__( self, value):
          """
          Adds the value to the current value, turning it into a list.
          """
          if type(value) == ListType:
               if len(value) == 1:
                    self.__add__(value[0])
               else:
                    for val in value:
                         val = str(val)
                    value.extend(self.value)
                    self.value = value
          else:
               if not self.value:
                    self.value = str(value)
               elif type(self.value) == ListType:
                    self.value.extend(value)
               else:
                    self.value = [self.value, str(value)]
          if type(self.value) == ListType:
               self.value.sort()
     def setvalue( self, name, value=None ):
          """
          Sets the value of the current attribute to the one passed in.
          """
          return self.__setitem__( name, value )
     def getvalue( self ):
          """
          Returns the value contained in the attribute
          """
          return self.value
     def __eq__( self, other ):
          """
          Compares to see if the other attribute is equal to this one
          """
          if type(other) == Attribute:
               return other.value == self.value
          if type(other) == type(self.value):
               return other == self.value
          else:
               return False
#          print "Attribut: EQ: Equating Self %s with Other %s yeilds %s" % (self.value, other.value, yei)
          return other.value == self.value
     def __ge__( self, other ):
          """
          Evaluates to see if the other attribute is greater than or equal to this one
          Logic:
               Each value of this must be >= some value of that
          Example:
               [2,3] >= [2,1] = (2>=2 or 2>=1) and (3>=2 or 3>=1) = True and True = True
               [1,2] >= [2,3] = (1>=2 or 1>=3) and (2>=2 or 2>=3) = False and True = False
          """
          #print "Attribute: __ge__: Other is %s of type %s" % ( other, type(other) )
          selfvalue = self.value
          othervalue = other.value
          if selfvalue == othervalue:
               return True

          def eval(sval, oval):
               """ Evaluates using the sorted_nicely function"""
               #print "Comparing %s with %s" % (sval, oval)
               #print "Types are %s and %s" % (type(sval), type(oval))
               slist = sorted_nicely([sval, oval])
               sindex = slist.index(sval)
               oindex = slist.index(oval)
               retval = (sindex <= oindex)
               #print "Self Index %s >= other index %s yeilds %s" % (sindex, oindex, retval)
               #print "Evaluates as %s" % retval
               return retval

          def eval_list(key, list):
               """ Evaluates or(key>=list member)"""
               for val in list:
                    if eval(key, list):
                         #print "Is True!"
                         return True
               #print "Is False"
               return False

          if type(selfvalue) == ListType:          # loop through self and 'And' all the evaluations
               for sval in selfvalue:
                    if type(othervalue) == ListType and not eval_list(sval, othervalue): # Check for failure
                         return False
                    elif not sval >= othervalue: # Check for failure
                         return False
          else:
               if type(othervalue) == ListType and not eval(sval, othervalue):  #evaluate self against list, return failure
                    return False
               elif not eval(selfvalue, othervalue):     # Evaluate self against other, singly
                    return False
          return True


def sorted_nicely( l ): 
    """
    Sort the given iterable in the way that humans expect.
    code from Jeff Atwood at his blog:
    http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html
    """
#    print "Sort is: %s" % l
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

          

def transform( instr ):
     """
     Changes any string into datatypes, suitable for transformation
     """
     retvalue = instr.partition((re.search( '[a-zA-z]+', instr )).group(0))
     newvalue = []
     for value in retvalue:
          try:
               newvalue.append(int(value))
          except:
               newvalue.append(value)
     return newvalue


def toString( invalue ):
     """
     Changes any data type to string type, suitable for returning
     """
     intype = type(invalue)
     outstring = ""
     if intype is StringType:
          outstring = invalue
     elif intype is ListType or intype is TupleType:
          for value in invalue:
               outstring += toString(value)
     elif intype is IntType or intype is FloatType:
          outstring = str( invalue )
     return outstring


def transformlist( inlist ):
     """
     Transforms a list of strings to their transformed and sorted components
     """
     newlist = []
     for value in inlist:
          newlist.append(transform(value))
     newlist.sort()
     return newlist


class Glossary():
     """
     Contains glossary data in an easy-to-access list form
     """
     SCORED_LIST = HW_FIELDS
     def __init__(self):
          self.lists = {}
     def __str__(self):
          #print "__str__"
          retstr = "{"
          key_list = self.keys()
          key_length = len(key_list)
          for key in key_list:
              #print "key is %s" % key
               retstr+="'%s':" % key
               val_list = self[key]
               val_length = len(val_list)
               retstr += "["
               for val in val_list:
                   #print "vals are %s" % val
                    retstr += "'" + str(val) + "'"
                    if (val_list.index(val) < val_length - 1):
                         retstr += ", "
               retstr+="]"
               if (key_list.index(key) < key_length - 1):
                         retstr += ", "
          retstr+="}"
          return retstr
     def _get_dict(self):
          """
          Returns a dictionary representation of the entire glossary
          """
          return self.lists
     def keys(self):
          #print "keys"
          return self.lists.keys()
     def append(self, attributes):
         #print "1)  append:  %s" % attributes
          for att in attributes:
               key = att
               value = attributes[key]
               if key in self.keys():
                    if value in self.lists[key]:
                         pass
                    else:
                        #print "2)  Appending %s to %s" % (value, self.lists[key])
                         self.lists[key].append(value)
               else:
                    self.lists[key]=[value]
          return True
     def __setitem__( self, name, value=None ):
          #print "__setitem__:  %s=%s" % (name, value)
          #print "Existing: %s" % self[name]
          self.lists[name]=[value,]
          #print "\n\nsetitem is done ************\n\n"
          #print "Now as: %s" % self[name]
          return True
     def __getitem__( self, name ):
         #print "__getitem__: %s" % name
          if name in self.keys():
              #print "Found: %s" % self.lists[name]
               return self.lists[name]
          else:
               return []
     def name_list( self ):
          """
          Returns a list of all names in the system
          """
          try:
               return self.lists['name']
          except:
               return []
     def weight(self, key):
          """
          Assigns a weight on the key
          ############################
          ####  Future Work:
          ####  Think about how to assign weights from config
          ####  Think about how to dynamically assign weights
          ############################
          """
          return 1
     def score( self, resource ):
          """
          Scores the current resource object 'other' based upon relative values
          Currently only uses the HW Values
          ############################
          ####  Future Work
          ####  1)  Improve, or allow for weights, on particular fields
          ####           Examples:
          ####                If memory is cheap, score += (memory score * .5)
          ####                if GPU costs 4, score = (score + 4)
          ####                If CORES are expensive, score += (cores score * 3)
          ####  2)  Allow for inclusion of various sets of values (hwfields, etc.)
          ####           Set from config file
          ####           put into checked_from list
          ####  3)  Possibly weight depending on:
          ####           % of total used, or % of remaining used
          ####           # free
          ####           some other computed metric
          ############################
          Uses the sorted_nicely algorithm from Jeff Atwood
          """
          #print "Evaluating %s" % resource
          score = 0
          #print "_______________________Scored list is: %s" % self.SCORED_LIST
          keyset = resource.keys()
          #print "_________________________5_____Score: Keyset is %s" % keyset
          for key in keyset:
               #print "^^^^_______Score_____________________Checking out Key %s" % key
               if key in self.SCORED_LIST:
                    #print "Found: %s in %s" % (key, self.SCORED_LIST)
                    vals = resource[key]
                    #print "_______________________Score: Key is %s, vals are %s" % (key, vals)
                    rawlist = self[key]
                    #print "_______________________Score: rawlist is %s" % rawlist
                    indexed_list = sorted_nicely(rawlist)
                    #print "_______________________Score: Indexed List is %s" % indexed_list
                    score = score + self.makescore( vals, indexed_list, key )
          return score

     def makescore(self, to_be_scored, indexed_list, key ):
          """
          Scores the actual 
          """
         #print "Scoring: %s in %s::%s" % (to_be_scored, key, indexed_list)
          tempscore = 0
          testtype = type(to_be_scored)
         #print "Eval type is %s" % testtype
          if testtype == ListType:
              #print "Drilling down"
               for val in to_be_scored:
                   #print "Val is %s" % val
                    partial_score = self.makescore( val, indexed_list, key )
                    tempscore = tempscore + partial_score
                   #print "List: partial score is %s, total is %s" % (partial_score, tempscore)
          else:
              #print "Score Here: %s" % to_be_scored
               ival = indexed_list.index( to_be_scored ) + 1
               weight = self.weight(key)
               tempscore = ival * weight
              #print "ival is %s, weight is %s, so partial score is %s" % (ival, weight, tempscore)
          print "This place %s has Temp Score of %s" % ( to_be_scored['name'] , tempscore)
          return tempscore
     def scorelist( self, inlist ):
          """
          Takes in a list, and returns it sorted by score
          """
          scorelist = []
          for resource in inlist:
               score = self.score(resource)
               scorelist.append( (resource, score) )
          scorelist.sort( key=lambda x: x[1] )
          # Randomize?
          return scorelist


def make_big( key, value ):
     retdict = {}
     retdict['name']=key
     retdict['value']=value
     return retdict

def make_small( indict ):
     #print "make_small: indict=%s" % indict
     name = indict['name']
     value = indict['value']
     return name, value

def make_atts( invalues ):
     #print "make_atts: invalues=%s" % invalues
     newdict = {}
     for val in invalues:
          key, value = make_small(val)
          newdict[key] = value
     return newdict




#ivalue = 0
#class bclass():
     #def __init__(self, value,):
          #self.ivalue = ivalue
          #ivalue += 1
          #self.value = str(value)
          #print "Init: %s:%s" % (self.value, self.ivalue)
     #def __repr__(self):
          #print "Repr: %s:%s" % (self.value, self.ivalue)
          #return self.value
     #def __eq__(self, other):
          #print "EQ: %s:%s" % (self.value, self.ivalue)
          #return (self.value == other.value )
     #def __setitem__( self, value ):
          #print "set: %s:%s" % (self.value, self.ivalue)
          #self.valueue = valueue
          #return True
#list1 = ['a', 'b', 'c']
#list2 = ['1', 'b', '3']
#blist1 = blist2 = []
#for el1 in list1:
     #blist1.append(bclass(el1, ivalue))
#for el2 in list2:
     #blist2.append(bclass(el2, ivalue))
#tempb = bclass('c', ivalue)
#for key in blist1:
     #existing_att = key
     #print "Comparing %s with %s" % (existing_att, tempb)
     #if not existing_att == tempb:
          #inde = blist1.index(tempb)
          #blist1[inde] = tempb
          #print "Replaced %s with %s" % (existing_att, tempb)
          #print "blist1 is now: %s" % blist1
     #else:
          #print "True"

class tempclass( object ):
     def __init__( self, other=None ):
          othertype = type(other)
          if othertype is tempclass:
               self.__dict__ = other.__dict__
          elif othertype is Resource:
               name = other.name
               self.__dict__[name] = other
          elif othertype is ListType:
               for element in other:
                    element = Resource( element )
                    name = element.name
                    self.__dict__[name] = element
          elif othertype is DictType:
               other = Resource( other )
               name = other.name
               self.__dict__[name] = other
          elif othertype is NoneType:
               pass
          else:
               raise Exception( "RD:__init__: Invalid Type %s for value %s" % (type(other), other) )
          self.Glossary = Glossary()
     def __str__( self ):
          return str(self.__dict__)
     def keys( self ):
          keylist = self.__dict__.keys()
          keylist.remove('Glossary')
          return keylist
     def __getattr__( self, name ):
          return self.__dict__[name]
     def __getitem__( self, name ):
          return self.__dict__[name]
     def __setattr__( self, name, value ):
          self.__dict__[name] = value
     def __setitem__( self, name, value ):
          self.__dict__[name] = value
                                  



if __name__=="__main__":
     tc = tempclass()
     print "TC is %s" % tc
     i1 = {'name':'bb01', 'val':'oogie'}
     i2 = {'name':'bb02', 'val':'boogie'}
     r1 = Resource( i1 )
     print "R1 is %s: %s" % ( r1.name, r1.val )
     r2 = Resource( i2 )
     print "R2 is %s: %s" % ( r2.name, r2.val )
     tc2 = tempclass( [r1, r2] )
     print "TC2 is now %s" % tc2
     print tc2.keys()
     print tc2['r1']
     print tc2['r2']
     print tc2.r1
     print tc2.r2
     
     
     ############   Setup  #######################
#     invalue1 = {'name':'alpha', 'value':'ALPHA'}
#     invalue2 = {'name':'alpha', 'value':'BETA'}
#     invalue3 = {'name':'CORES', 'value':'1'}
#     invalue4 = {'name':'CORES', 'value':'4'}
#     invalue5 = {'name':'MEM', 'value':'4gb'}
#     invalue6 = {'name':'MEM', 'value':'12gb'}
#     invalue7 = {'name':'NET', 'value':'1'}
#     invalue8 = {'name':'NET', 'value':'2'}
#     invalue10 = {'name':'name', 'value':'bb01'}
#     invalue11 = {'name':'name', 'value':'bb02'}
#     invalue12 = {'name':'name', 'value':'bb03'}
#     invalue13 = {'name':'name', 'value':'bb04'}
#     invalue14 = {'name':'GPU', 'value':'true'}


#     att1 = {'name':'bb01', 'MEMORY':'4G', 'DISK':'1'}
#     att2 = {'name':'bb02', 'MEMORY':'4G', 'DISK':'4'}
#     att3 = {'name':'bb03', 'MEMORY':'12G', 'DISK':'1'}
#     att4 = {'name':'bb04', 'MEMORY':'12G', 'DISK':'4'}

#     indict = [('alpha', 'ALPHA'), ('alpha', 'BETA'), ('CORES', '1'), ('CORES', '4'), ('MEM', '4gb'), ('MEM', '12gb'), ('NET', '1'), ('NET', '2')]
#     inlist = [invalue1, invalue2, invalue3, invalue4, invalue5, invalue6, invalue7, invalue8]
#     alist = []
#     for value in inlist:
#          alist.append(Attribute(**value))
#     attsetup4 = [invalue10, invalue1, invalue3, invalue5, invalue7]
#     attsetup2 = [invalue11, invalue1, invalue3, invalue5, invalue7]
#     attsetup3 = [invalue12, invalue2, invalue4, invalue6, invalue8]
#     attsetup1 = [invalue13, invalue1, invalue3, invalue5, invalue7, invalue14]

     #att1 = make_atts( attsetup1 )
     #print "att1 is %s" % att1
     #att2 = make_atts( attsetup2 )
     #print "att2 is %s" % att2
     #att3 = make_atts( attsetup3 )
     #print "att3 is %s" % att3
     #att4 = make_atts( attsetup4 )
     #print "att4 is %s" % att4

#     res1 = Resource(att1)
#     res2 = Resource(att2)
#     res3 = Resource(att3)
#     res4 = Resource(att4)
#     reslist = [res1, res2, res3, res4]





#     applist = []
#     appdict1 = {'name':'bb01', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict1)
#     appdict2 = {'name':'bb02', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict2)
#     appdict3 = {'name':'bb03', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict3)
#     appdict4 = {'name':'bb04', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict4)
#     appdict5 = {'name':'bb05', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict5)
#     appdict6 = {'name':'bb06', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict6)
#     appdict7 = {'name':'bb07', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'kernel':"ubuntu-lucid-amd64"}
#     applist.append(appdict7)
#     appdict11 = {'name':'bb11', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
#     applist.append(appdict11)
#     appdict12 = {'name':'bb12', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
#     applist.append(appdict12)
#     appdict13 = {'name':'bb13', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
#     applist.append(appdict13)
#     appdict14 = {'name':'bb14', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'GPU':'true'}
#     applist.append(appdict14)
#     appdict15 = {'name':'bb15', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'GPU':'true'}
#     applist.append(appdict15)
#     appdict16 = {'name':'bb16', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'GPU':'true'}
#     applist.append(appdict16)
#     appdict17 = {'name':'bb17', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'GPU':'true'}
#     applist.append(appdict17)

#     appdict21 = {'name':'bb21', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
#     applist.append(appdict21)
#     appdict22 = {'name':'bb22', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
#     applist.append(appdict22)
#     appdict23 = {'name':'bb23', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
#     applist.append(appdict23)
#     appdict24 = {'name':'bb24', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'kernel':"eucalyptus"}
#     applist.append(appdict24)
#     appdict25 = {'name':'bb25', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'kernel':"eucalyptus"}
#     applist.append(appdict25)
#     appdict26 = {'name':'bb26', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'kernel':"eucalyptus"}
#     applist.append(appdict26)
     appdict27 = {'name':'bb27', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'kernel':"eucalyptus"}
#     applist.append(appdict27)

#     maxapp = {'name':'bb99', 'CPU':'nahalem', 'CORES':'16', 'MEM':'16GB', 'DISK':'4', 'NET':'ib', 'IB':['sdr', 'qdr'], 'GPU':'true', 'kernel':"eucalyptus"}



     print "Good"
     #print "Step 1:  Test the attributes"
     
     #for eachvalue in alist:
          #print "Attribute is: %s" % eachvalue
          
     #for value in alist:
          #for othervalue in alist:
               #print "Trying %s == %s yeilds %s" % (value, othervalue, value == othervalue)
               #print "Trying %s >= %s yeilds %s" % (value, othervalue, value >= othervalue)

     #print "\n\n\n\n ######################### \n\n"
     #print "Step 2:  Test the Resources"
     #for r1 in reslist:
          #ind = reslist.index(r1)
          #for r2 in reslist[ind+1:]:
               #if r1 == r2:
                    #print "Failure: %s == %s" % (r1, r2)
               #if r1 >= r2:
                    #print "Failure: %s >= %s" % (r1, r2)
               #if not r2 >= r1:
                    #print "Failure: %s >= %s" % (r2, r1)
     
     
     
     print "Step 3:  Test the Resource Dictionary"
     print "3a)  Assignment"
 #    print "Type of appdict27 is %s" % type(appdict27)
 #    appres = Resource( appdict27)
 #    print "Type of appres is %s, value %s" % (type(appres), appres)
 #    rd = ResourceDict( appres )
 #    print "RD is now %s" % rd


#     print "\n\n\n\n\n"

#     bb01 = {'status': 'READY FOR USE', 'disabled': 'False', 'compatable_images': "['lucid-clone', 'ubuntu-lucid-amd64-pxe', 'ubuntu-hardy-amd64', 'ubuntu-hardy-amd64-cuda31', 'ubuntu-lucid-xen', 'ubuntu-lucid-cuda', 'ubuntu-lucid-amd64', 'ubuntu-hardy-i386', 'ubuntu-gridftp', 'eucalyptus', 'eucalyptus-dev', 'legacy-pxelinux-pxe', 'centos-5.4-x86_64', 'lucid-amd64-cuda31-ib']", 'DISKS': "['4']", 'name': 'bb01.mcs.anl.gov', 'bootstate': 'COMPLETED', 'MEM': "['4G']", 'reservations': '[915L]', 'image': 'ubuntu-hardy-amd64', 'allocatable': 'True', 'CPU': "['opteron']", 'hardware': 'phase1', 'held': 'True', 'mac': '00:17:31:F9:C8:7F', 'address': '140.221.37.31', 'CORES': "['4']", 'NET': "['myrinet', 'ib']", 'IB': "['sdr']", 'power_interfaces': "[{'controller': 'radix-pwr11', 'port': '.AA3'}]", 'current reservation': '915', 'stage': 'boot'}
#     bb01res = Resource( bb01 )
#     print "bb01res is now %s" % bb01res
#     rd.add( bb01res )
#     print "rd is now %s" % rd

     


#     outres = rd['bb01.mcs.anl.gov']
#     if outres == bb01res:
#          print "Matches"
#     else:
#          print "Does not Match:"
#          print "Outres is  :%s" % outres
#          print "bb01res is :%s" % bb01res
#     rd.update()
#     print "RD is now %s" % rd





















     #print "RD is now: %s" % rd
     #for res in reslist:
     #     rd.add(res)
     #     print "RD is now: %s" % rd
     #     print "RD Name List is now: %s" % rd.name_list()
     #     print "Glossary NameList is now %s " % rd.glossary.name_list()
     #     print "\n\n\n"
          
          
     #print "RD as dictionary:  "
     #print rd._get_dict()
     #print "Done"
     #print "\n\n\n"
     #print "Test:  Assignment of Resource Dictionary"
     #r2 = rd
     #print "RD is: %s" % rd._get_dict()
     #print "\n\n\n"
     #print "R2 is: %s" % r2._get_dict()
     #print "\n\n\n"
     
     #namelist1 = rd.keys()
     #namelist2 = r2.name_list()
     #for name in namelist1:
     #     print "dict RD name %s value %s" % (name, rd[name])
     #for name in namelist2:
     #     print "dict RD name %s value %s" % (name, r2[name])
          
          
          
     #print "3b)  Find"
     #print "3c)  Assignment"
     #print "\n\n\n\n ######################### \n\n"
     #print "Step 4:  Test the Glossary"
     #g = Glossary()
     #print "Testing Append"
     #g.append(appdict1)
     #print "G is %s" % g
     #for app in applist:
          #g.append(app)
          #print "G is %s" % g
     #print "\n\n\n"
     #print "Testing each value: "
     #for key in g.keys():
          #print "%s is %s" % (key, g[key])
     #print "\n\n\n"
     #print "Testing Assignment"
     #print "Testing one:  Name = 'orinoco'"
     #g['name']='orinoco'
     #print "G is %s" % g
     
     #appdict0 = {'age':15, 'weight':'225', 'likes':'oranges', 'name':'bb99', 'CPU':'Rubber Chicken', 'CORES':'9', 'MEM':'32GB'}
     #print "Testing Two:  %s" % appdict0
     #for key in appdict0:
          #print "BASE: Key is: %s" % key
          #val = appdict0[key]
          #print "ASSIGNMENT:  KEY is %s; VAL is %s " % (key, val)
          #g[key] = val
          #print "G is %s" % g



     #print "\n\n\n\n ######################### \n\n"
     #print "Step 5:  Test the Glossary Score\n\n"
     #g = None
     #g = Glossary()
     #print "Baseline:  G is %s" % g
     #for key,vals in [('CPU',CPU), ('GPU',GPU), ('MEM',MEM), ('DISK',DISK), ('NET',NET), ('IB',IB), ('PACKAGE',PACKAGE), ('GROUP',GROUP), ('VINTAGE',VINTAGE), ('IMAGES',IMAGES), ('CORES',CORES)]:
          #print "***********************   Key is %s *****************************" % key
          #print "***********************   Vals are %s *****************************" % vals
          #for val in vals:
               #print "***********************   Val is %s *****************************" % val
               #g.append({key:val})
               #print "G is %s" % g

     #print "\n\n\n\n"
     #print "Loaded: G is %s" % g
     #scorelist = []
     #for app in applist:
          #print "Scoring %s" % app
          #score = g.score(app)
          #print "Score is: %s" % score
          #scorelist.append((app, score))
     #scorelist.sort(key=lambda x: x[1])
     #print "Total Scores:"
     #for entry in scorelist:
          #print "Score %s for %s" % (entry[1], entry[0])
     #maxscore = g.score(maxapp)
     #print "MaxApp is %s " % maxscore
     





     #print "Test:  Copying"
     #value = {'name':'bb99', 'oogie':'boogie'}
     #name = value['name']
     #r2[name] = value
     #print "R2 is: %s" % r2._get_dict()
     #print "\n\n\n"

     #r3 = ResourceDict(r2)
     #print "R3 is: %s" % r3._get_dict()
     #print "\n\n\n"
     #print "R3 type is %s" %type(r3)
     #print "That matches ResourceDict type: %s" % (type(r3) == ResourceDict)
     
     #print "Test:  Initialize by a dictionary"
     #dict2 = r2._get_dict(glossary=False)
     #print "Verification:  Type(dict2) is %s" % type(dict2)
     #print "Dict is %s\n\n\n" % dict2
     #r4 = ResourceDict(dict2)
     #print "\n\n"
     #print "R2 is: %s" % r2._get_dict()
     #print "\n\n\n"
     #print "R4 is: %s" % r4._get_dict()
     #print "\n\n\n"
     
     #print "R4 glossary is %s" % r4.glossary
     
