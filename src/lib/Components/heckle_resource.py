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



class ResourceDict(object):
     """
     Object to contain and encapsulate the Resources in the system
     """
     def __init__( self, in_dict=None ):
          self.resource_list = []
          self.glossary = Glossary()
          if type(in_dict) is DictType:
               print "Incomming: %s" % in_dict
               for key in in_dict:
                    self.add(in_dict[key])
          if type(in_dict) is ListType:
               print "Incomming: %s" % in_dict
               for val in in_dict:
                    self[val['name']]=val
          elif type(in_dict) == ResourceDict:
               print "Incomming: %s" % in_dict
               for name in in_dict.keys():
                    self[name] = in_dict[name]
          else:
               print "Nothing to do?"
     def __str__( self ):
          """
          Returns a string representation of all resources in the system
          """
          retstr = "Resources: ["
          res_len = len(self.resource_list)
          for res in self.resource_list:
               retstr += str(res)
               if self.resource_list.index(res) < res_len-1:
                    retstr += ", "
          retstr += "]"
          retstr += "\nGlossary: "
          retstr += str(self.glossary)
          return retstr
     def _get_dict( self, glossary=True, resources=True ):
          """
          Returns a dictionary version of the entire Resource Dictionary
          
          """
          if glossary and not resources:
               return self.glossary._get_dict()
          elif resources and not glossary:
               retdict = []
               for res in self.resource_list:
                    retdict.append(res._get_dict())
               return retdict
          retdict = {}
          if glossary:
               retdict['Glossary'] = self.glossary._get_dict()
          if resources:
               retdict['Resources'] = []
               for res in self.resource_list:
                    retdict['Resources'].append(res._get_dict())
          return retdict
     def __getitem__( self, name=None ):
          """
          Finds one particular resource by name
          Returns that resource, or False if no resource by that name.
          """
          for res in self.resource_list:
               if res['name'] == name:
                    print "Returning %s" % res
                    return res._get_dict()
          return False
     def keys( self ):
          """
          Returns a list of strings containing the names of all the nodes
          Node names must be unique
          """
          return self.name_list()
     def name_list( self ):
          """
          Returns a list of strings containing the names of all the nodes
          Node names must be unique
          """
          #return self.resource_list.keys()
          name_list = []
          for res in self.resource_list:
               name_list.append(res['name'])
          return name_list
     def node_count( self ):
          """
          returns the number of resources / nodes in the current system
          """
          return len(self.resource_list)
     def __add__( self, attributes=None, resource=None ):
          """
          Mathmatical / symbolic addition
          Adds a new Resource to the system
          Attributes is a dictionary of strings, key:value
          MUST contain a Name field, and names MUST be unique across the system
          """
          return self.add(attributes=attributes, resource=resource)
     def add( self, attributes=None, resource=None ):
          """
          Adds a new Resource to the system
          Attributes is a dictionary of strings, key:value
          MUST contain a Name field, and names MUST be unique across the system
          """
          try:
               print "Attributes are %s" % attributes
          except:
               pass
          try:
               print "Resource is %s" % resource
          except:
               pass
          if (resource and attributes) or not (resource or attributes):
               retstr = "Object: " + str(resource) + " and Dictionary " + str(attributes)
               raise Exception("Need ONE thing to compare against!  You gave me %s " % retstr)
          elif attributes:
               if attributes['name'] in self.name_list():
                    raise Exception( "Error: Node %s already in the list" % attributes['name'] )
               else:
                    newResource = Resource( attributes )
                    self.resource_list.append(newResource)
                    self.glossary.append( attributes )
               return True
          elif resource:
               if not resource['name']:
                    raise Exception( "Bad Resource: %s " % resource )
               try:
                    inlist1 = resource['name'] in self.name_list()
               except:
                    inlist1 = None
               try:
                    inlist2 = self.resource_list.index(resource)
               except:
                    inlist2 = None
               if inlist1 or inlist2:
                    raise Exception( "Error: Node already in the list: %s" % resource )
               else:
                    self.resource_list.append( resource )
                    self.glossary.append( resource._get_dict() )
          return True
     def update( self, attributes=None ):
          """
          Changes the resource with the attributes named
          If attributes is a list or a dictionary, pass on to the set_item function
          If attributes is None, then call on Heckle to get an updated node status
          else, return an error.
          """
          att_type = type(attributes)
          if att_type is DictType or att_type is ListType:
               return self.__setitem__(attributes)
          elif att_type is NoneType:
               #get attributes from Heckle as list of node dictionaries
               #self.update(HeckleList)
               return True
          else:
               raise Exception( "ResourceDict:Update only accepts dictionaries or lists of dictionaries; your attribute set for this is %s." % att_type )
     def __setitem__( self, name=None, attributes=None ):
          """
          Sets the resource indicated to the value indicated
          Attributes is to be a dictionary, or list of dictionaries with each resource having one dictionary.
          Algorythm:
               If attributes is a list of resources, then iterate through the list, setting each.
               If attributes is a dictionary of key:value pair(s), where the key is a resource name
                    and the value is a dictionary of key:value pairs for attributes, then set these.
               else, return an error.
          """
          if name:
               print "RD: SetItem: Name is %s" % name
          if attributes:
               print "RD: SetItem:  Attributes is %s" % attributes
          att_type = type(attributes)
          if att_type == ListType: 
               for resource in attributes:
                    self.update(attributes[resource])
                    self.glossary.append(attributes[resource])
          elif att_type == DictType: #if we're dealing with a dictionary for one resource
               name = attributes['name']
               if name in self.keys():
                    index = self.keys().index(name)
                    self.resource_list[index].update(attributes)
               else:
                    self.resource_list.append(Resource(attributes))
               self.glossary.append(attributes)
          self.resource_list.sort(key=lambda x: x['name'])
          return True
     def __sub__(self, attributes=None, resource=None ):
          """
          Removes a resource from the current system
          Accepts either a dictionary of attributes, or a resource object
          """
          return self.remove(attributes=attributes, resource=resource)
     def remove( self, attributes=None, resource=None ):
          """
          Removes a resource from the current system
          Accepts either a dictionary of attributes, or a resource object
          """
          if (resource and attributes) or not (resource or attributes):
               retstr = "Object: " + str(resource) + " and Dictionary " + str(attributes)
               raise Exception("Need ONE thing to compare against!  You gave me %s " % retstr)
          elif attributes:
               try:
                    resource = self[attributes['name']]
               except:
                    raise Exception("Unknown Resource: %s" % attributes)
          elif resource:
               if resource in self.resource_list:
                    pass
               else:
                    raise Exception("Unknown Resource: %s" % resource)
          self.resource_list.remove( resource )
          return True
     def __eq__( self, attributes=None ):
          """
          Returns a list of nodes which match the attributes
          Attributes is a dictionary of strings
          """
          retlist = []
          for res in self.resource_list:
               if res == (attributes):
                    retlist.append(res)
          return retlist
     def __ge__( self, attributes=None ):
          """
          Returns a list of nodes which are greater than or equal to the attributes
          Attributes is a dictionary of strings
          """
          retlist = []
          for res in self.resource_list:
               if res == (attributes):
                    retlist.append(res)
          return retlist
     def backup( self ):
          """
          Saves the current state to a file
          """
          FILENAME = "~/backup.txt"
          outfile = os.open(FILENAME, 'w')
          for res in self.resource_list:
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
               newResource = Resource(line)
               self.add(newResource)
          outfile.close()






class Resource(object):
     """
     Representation of a single Node in the Heckle System
     Also acts as a dictionary for attributes it contains
     """
     typestr = "Resource"
     def __init__( self, attributes=None ):
          """
          Initializes values
          Attributes is a dictionary of key:value for each attribute
          KISS
          """
          self.attribute_list = []
          #print "Attributes are: %s" % attributes
          try:
               for att in attributes:
                    val = attributes[att]
               #print "Setting %s:%s" % (att, val)
                    self.__setitem__(att, val)
          except:
               self.name = None
     def __str__( self ):
          """
          Returns a string representation of the object
          """
          retstring = "{"
          att_len = len(self.attribute_list)
          for att in self.attribute_list:
               retstring += str(att)
               if self.attribute_list.index(att) < att_len - 1:
                    retstring += ", "
          retstring += "}"
          return retstring
     def _get_dict( self ):
          """
          Returns a dictionary representation of the object
          """
          retdict = {}
          for att in self.attribute_list:
               retdict[att['name']] = att['value']
          return retdict
     def __getitem__( self, name ):
          """
          Allows getting an item directly by subscription
          """
#         #print "Debug: Name is %s" % name
          retvalue = []
          for att in self.attribute_list:
               #print "Debug:  att is %s" % att
               attname = att['name']
              #print "Attname is %s" % attname
              #print "Name is %s" % name
               if attname == name:
                    retvalue.append(att['value'])
          if retvalue:
               return retvalue
          else:
               raise Exception("No value %s in attribute, only %s" % (name, self))
     def __setitem__( self, key, value=None):
          """
          Direct Assignment of key-value pairs
          Adds the key:value pair to the attributes
          Will not add duplicate keys
          """
          if key in self.keys():
               existing_att = self._get_attribute(key)
               new_att = Attribute(key, value)
               if existing_att == new_att:
                    return True
               else:
                    existing_att = new_att
                    return True
          else:
               return self.add_attribute(key, value)
     def __add__(self, key, value=None):
          """
          Absolutely adds the key:value pair to the attributes
          Will add duplicate values
          """
          return self.add_attribute( key=key, value=value)
     def add_attribute( self, key, value=None):
          """
          Absolutely adds the key:value pair to the attributes
          Will add duplicate values
          """
          try:
               if value not in self._get_value(key):
                    self.attribute_list.append(Attribute(key, value))
          except:
               self.attribute_list.append(Attribute(key, value))
          return True
     def update( self, attributes ):
          """
          Updates an item in the current resource
          Attributes is a dictionary, with key:value pairs
          """
          keylist = attributes.keys()
          for key in keylist:
               value = attributes[key]
               self[key] = values
          return True
     def del_attribute( self, key, value=None):
          """
          Removes a given attribute from the resource
          """
          if value:
               try:
                    self.attribute_list.remove(Attribute(key, value))
               except:
                    pass
          else:
               try:
                    remove_list = self._get_attribute(key)
                    for att in remove_list:
                         self.attribute_list.remove(att)
               except:
                    pass
     def _get_attribute( self, key, value=None ):
          """
          Gets all attribute objects for a given key
          """
          #print "get attribute Key is %s" % key
          #print "get attribute Value is %s" % value
          retvalue = []
          for att in self.attribute_list:
               attname = att['name']
               if attname == key:
                    if value:
                         if att['value'] == value:
                              retvalue.append(att)
                    else:
                         retvalue.append(att)
          #for val in retvalue:
               #print "retvalue is %s" % val
          return retvalue
     def _get_attributes( self ):
          """
          Returns the attribute list of this resource
          """
          return self.attribute_list
     def keys( self ):
          """
          Returns a list of unique keys for the attributes in this Resource
          """
          retvalue = []
          for att in self.attribute_list:
               if att['name'] not in retvalue:
                    retvalue.append(att['name'])
          return retvalue
     def _get_value( self, key ):
          """
          Gets all the attribute values for a given key
          """
          retvalue = []
          for att in self.attribute_list:
               if att['name'] == key:
                    retvalue.append(att['value'])
          return retvalue
     def __eq__( self, other ):
          """
          Compares the resource to see if they match
          Can check against another Resource or a Dictionary of attributes
          """
          if type(other) == Resource:
               return self.attribute_list == other._get_attributes()
          elif type(other) == DictType:
               equal = True
               for att in attributes:
                    if attributes[att] not in self[att]:
                         equal = False
               return equal
          
     def __ge__( self, other ):
          """
          Compares this resource, attribute-by-attribute, against
          another Resource or a Dictionary of attributes.
          Determines if this resource is greater than or equal to the other
          """
          retvalue = True
          if type(other) == Resource:
               for that in other._get_attributes():
                    #print "That: name is %s, val is %s" % (that.name, that.value)
                    if that['name'] is 'name':
                         pass
                    else:
                         name = that['name']
                         thislist = self._get_attribute(name)
                         for this in thislist:
                              #print "This name %s is value %s" % (this['name'], this['value'])
                              yei = this >= that
                             #print "Resource GE: Comparing this %s with that %s yeilds %s" % (this, that, yei)
                              
                              if yei:
                                   pass
                              else:
                                   retvalue = False
          elif type(other) == DictType:
               #print "GE: in attributes"
               for att in attributes:
                    val = attributes[att]
                    that = Attributes(att, val)
                    this = self[att]
                    if not this >= that:
                         retvalue = False
          return retvalue



class Attribute(object):
     """
     Object which encapsulates any one value of a resource.
     It takes care of its own comparisons and representations
     """
     def __init__( self, name, value=None ):
          self.name = name
          self.value = value
     def __str__( self ):
          """
          Returns the string representation of the current object
          """
          return "'%s':'%s'" % (self.name, self.value)
     def __getitem__( self, name ):
          """
          Allows getting an item by subscription
          """
          try:
               return self.__dict__[name]
          except:
               raise Exception("No value %s in attribute, only %s" % (name, self))
     def __setitem__( self, name, value=None ):
          """
          Direct assignment of an item
          """
          if self.name == name:
               self.value = value
          else:
               raise Exception( "You're trying to turn a %s into a %s!" % (self.key, key) )
     def setvalue( self, name, value=None ):
          """
          Sets the value of the current attribute to the one passed in.
          """
          self.__setitem__( name, value )
     def getvalue( self ):
          """
          Returns the value contained in the attribute
          """
          return self.value
     def __eq__( self, other ):
          """
          Compares to see if the other attribute is equal to this one
          """
          yei = other.value == self.value
         #print "Equating Self %s with Other %s yeilds %s" % (self.value, other.value, yei)
          return other.value == self.value
     def __ge__( self, other ):
          """
          Evaluates to see if the other attribute is greater than or equal to this one
          Uses the sorted_nicely algorithm from Jeff Atwood
          """
          #print "Other is: %s", other
          othervalue = other.getvalue()
          raw_list = [othervalue, self.value]
          sorted_list = sorted_nicely([othervalue, self.value])
          yei = ( sorted_list.index(self.value) >= sorted_list.index(othervalue) )
         #print "GE: Comparing Self %s with Other %s yeilds %s" % (self.value, othervalue, yei)
          return yei
          
          
def sorted_nicely( l ): 
    """
    Sort the given iterable in the way that humans expect.
    code from Jeff Atwood at his blog:
    http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html
    """
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
         #print "This place has Temp Score of %s" % tempscore
          return tempscore


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






if __name__=="__main__":
     
     
     
     ############   Setup  #######################
     invalue1 = {'name':'alpha', 'value':'ALPHA'}
     invalue2 = {'name':'alpha', 'value':'BETA'}
     invalue3 = {'name':'CORES', 'value':'1'}
     invalue4 = {'name':'CORES', 'value':'4'}
     invalue5 = {'name':'MEM', 'value':'4gb'}
     invalue6 = {'name':'MEM', 'value':'12gb'}
     invalue7 = {'name':'NET', 'value':'1'}
     invalue8 = {'name':'NET', 'value':'2'}
     invalue10 = {'name':'name', 'value':'bb01'}
     invalue11 = {'name':'name', 'value':'bb02'}
     invalue12 = {'name':'name', 'value':'bb03'}
     invalue13 = {'name':'name', 'value':'bb04'}
     invalue14 = {'name':'GPU', 'value':'true'}


     att1 = {'name':'bb01', 'MEMORY':'4G', 'DISK':'1'}
     att2 = {'name':'bb02', 'MEMORY':'4G', 'DISK':'4'}
     att3 = {'name':'bb03', 'MEMORY':'12G', 'DISK':'1'}
     att4 = {'name':'bb04', 'MEMORY':'12G', 'DISK':'4'}

     indict = [('alpha', 'ALPHA'), ('alpha', 'BETA'), ('CORES', '1'), ('CORES', '4'), ('MEM', '4gb'), ('MEM', '12gb'), ('NET', '1'), ('NET', '2')]
     inlist = [invalue1, invalue2, invalue3, invalue4, invalue5, invalue6, invalue7, invalue8]
     alist = []
     for value in inlist:
          alist.append(Attribute(**value))
     attsetup4 = [invalue10, invalue1, invalue3, invalue5, invalue7]
     attsetup2 = [invalue11, invalue1, invalue3, invalue5, invalue7]
     attsetup3 = [invalue12, invalue2, invalue4, invalue6, invalue8]
     attsetup1 = [invalue13, invalue1, invalue3, invalue5, invalue7, invalue14]

     #att1 = make_atts( attsetup1 )
     #print "att1 is %s" % att1
     #att2 = make_atts( attsetup2 )
     #print "att2 is %s" % att2
     #att3 = make_atts( attsetup3 )
     #print "att3 is %s" % att3
     #att4 = make_atts( attsetup4 )
     #print "att4 is %s" % att4

     res1 = Resource(att1)
     res2 = Resource(att2)
     res3 = Resource(att3)
     res4 = Resource(att4)
     reslist = [res1, res2, res3, res4]





     applist = []
     appdict1 = {'name':'bb01', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict1)
     appdict2 = {'name':'bb02', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict2)
     appdict3 = {'name':'bb03', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict3)
     appdict4 = {'name':'bb04', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict4)
     appdict5 = {'name':'bb05', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict5)
     appdict6 = {'name':'bb06', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict6)
     appdict7 = {'name':'bb07', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'kernel':"ubuntu-lucid-amd64"}
     applist.append(appdict7)
     appdict11 = {'name':'bb11', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
     applist.append(appdict11)
     appdict12 = {'name':'bb12', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
     applist.append(appdict12)
     appdict13 = {'name':'bb13', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'GPU':'true'}
     applist.append(appdict13)
     appdict14 = {'name':'bb14', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'GPU':'true'}
     applist.append(appdict14)
     appdict15 = {'name':'bb15', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'GPU':'true'}
     applist.append(appdict15)
     appdict16 = {'name':'bb16', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'GPU':'true'}
     applist.append(appdict16)
     appdict17 = {'name':'bb17', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'GPU':'true'}
     applist.append(appdict17)

     appdict21 = {'name':'bb21', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
     applist.append(appdict21)
     appdict22 = {'name':'bb22', 'CPU':'nahalem', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
     applist.append(appdict22)
     appdict23 = {'name':'bb23', 'CPU':'opteron', 'CORES':'1', 'MEM':'4GB', 'kernel':"eucalyptus"}
     applist.append(appdict23)
     appdict24 = {'name':'bb24', 'CPU':'nahalem', 'CORES':'4', 'MEM':'4GB', 'kernel':"eucalyptus"}
     applist.append(appdict24)
     appdict25 = {'name':'bb25', 'CPU':'nahalem', 'CORES':'16', 'MEM':'4GB', 'kernel':"eucalyptus"}
     applist.append(appdict25)
     appdict26 = {'name':'bb26', 'CPU':'nahalem', 'CORES':'1', 'MEM':'12GB', 'kernel':"eucalyptus"}
     applist.append(appdict26)
     appdict27 = {'name':'bb27', 'CPU':'nahalem', 'CORES':'1', 'MEM':'16GB', 'kernel':"eucalyptus"}
     applist.append(appdict27)

     maxapp = {'name':'bb99', 'CPU':'nahalem', 'CORES':'16', 'MEM':'16GB', 'DISK':'4', 'NET':'ib', 'IB':['sdr', 'qdr'], 'GPU':'true', 'kernel':"eucalyptus"}



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
     rd = ResourceDict()
     print "RD is now: %s" % rd
     for res in reslist:
          rd.add(resource=res)
          print "RD is now: %s" % rd
          print "RD Name List is now: %s" % rd.name_list()
          print "Glossary NameList is now %s " % rd.glossary.name_list()
          print "\n\n\n"
          
          
     print "RD as dictionary:  "
     print rd._get_dict()
     print "Done"
     print "\n\n\n"
     print "Test:  Assignment of Resource Dictionary"
     r2 = rd
     print "RD is: %s" % rd._get_dict()
     print "\n\n\n"
     print "R2 is: %s" % r2._get_dict()
     print "\n\n\n"
     
     namelist1 = rd.keys()
     namelist2 = r2.name_list()
     for name in namelist1:
          print "dict RD name %s value %s" % (name, rd[name])
     for name in namelist2:
          print "dict RD name %s value %s" % (name, r2[name])
          
          
          
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
     





     print "Test:  Copying"
     value = {'name':'bb99', 'oogie':'boogie'}
     name = value['name']
     r2[name] = value
     print "R2 is: %s" % r2._get_dict()
     print "\n\n\n"

     r3 = ResourceDict(r2)
     print "R3 is: %s" % r3._get_dict()
     print "\n\n\n"
     print "R3 type is %s" %type(r3)
     print "That matches ResourceDict type: %s" % (type(r3) == ResourceDict)
     
     print "Test:  Initialize by a dictionary"
     dict2 = r2._get_dict(glossary=False)
     print "Verification:  Type(dict2) is %s" % type(dict2)
     print "Dict is %s\n\n\n" % dict2
     r4 = ResourceDict(dict2)
     print "\n\n"
     print "R2 is: %s" % r2._get_dict()
     print "\n\n\n"
     print "R4 is: %s" % r4._get_dict()
     print "\n\n\n"
     
     print "R4 glossary is %s" % r4.glossary
     