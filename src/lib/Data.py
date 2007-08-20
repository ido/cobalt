'''Data builds up datatype definitions on top of XML-RPC serializable python types'''
__revision__ = '$Revision$'

import time, types, xmlrpclib, random
import Cobalt.Util
import Cobalt.Proxy

class DataCreationError(Exception):
    '''Used when a new object cannot be created'''
    pass

class IncrID(object):
    
    """Generator for incrementing integer IDs."""
    
    def __init__(self):
        """Initialize a new IncrID."""
        self.idnum = 0

    def get(self):
        """Get the next id."""
        self.idnum += 1
        return self.idnum
    
    def next (self):
        """Iterator interface."""
        return self.get()

class RandomID(object):
    """Generator for non-repeating random integer IDs."""
    
    def __init__(self):
        """Initialize a new RandomID."""
        self.used = []
        self.rand = random.Random(int(time.time()))

    def get(self):
        """Get the next id."""
        idnum = str(self.rand.randrange(0, 2147483639)) + str(self.rand.randrange(0, 2147483639))
        while idnum in self.used:
            idnum = str(self.rand.randrange(0, 2147483639)) + \
            str(self.rand.randrange(0, 2147483639))
        self.used.append(idnum)
        return idnum
    
    def next (self):
        """Iterator interface."""
        return self.get()


class Data(object):
    '''Data takes nested dictionaries and builds objects analogous to sss.restriction.data objects'''
    required_fields = []
    
    def _get_tag (self):
        try:
            return self.get('tag')
        except KeyError, e:
            return None
    
    def _set_tag (self, value):
        self.set('tag', value)
    
    tag = property(_get_tag, _set_tag)

    def __init__(self, info):
        missing = [field for field in self.required_fields if not info.has_key(field)]
        if missing:
            raise DataCreationError, missing
        self._attrib = {}
        self.set('stamp', time.time())
        self._attrib.update(info)

    def get(self, field, default=None):
        '''return attribute'''
        try:
            return self._attrib[field]
        except KeyError:
            if default is not None:
                return default
            raise

    def set(self, field, value):
        '''set attribute'''
        self._attrib[field] = value
        self._attrib['stamp'] = time.time()

    def update(self, attrdict):
        '''update attributes based on attrdict'''
        for item in attrdict.iteritems():
            self.set(*item)
            
    def match(self, spec):
        '''Implement datatype matching'''
        matching_fields = [field for field in spec.keys()
            if spec[field] == '*'
            or (self.get(field, False) and self.get(field) == spec[field])
        ]
        return len(matching_fields) == len(spec.keys())
        
    def to_rx(self, spec):
        '''return transmittable version of instance'''
        return dict([(field, self.get(field)) for field in spec \
                     if field in self._attrib])

class DataSet(object):
    '''DataSet provides storage, iteration, and matching across sets of Data instances'''
    __object__ = Data
    __id__ = None
    __unique__ = None
    
    def keys (self):
        if not self.__unique__:
            raise KeyError("No unique key is set.")
        return [item.get(self.__unique__) for item in self.data]

    def __init__(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        if not self.__unique__:
            raise KeyError("No unique key is set.")
        for item in self:
            if item.get(self.__unique__) == key:
                return item
        raise KeyError(key)
    
    def __delitem__(self, key):
        self.remove(self[key])

    def append(self, item):
        '''add a new element to the set'''
        if self.__unique__ and item.get(self.__unique__) in self.keys():
            raise KeyError("duplicate: %s" % item.get(self.__unique__))
        self.data.append(item)

    def remove(self, x):
        '''remove an element from the set'''
        self.data.remove(x)

    def Add(self, cdata, callback=None, cargs={}):
        """Construct new items of type self.__object__ in the dataset.
        
        Arguments:
        cdata -- The first argument to be passed to the data constructor.
            If cdata is a list, construct multiple items.
        callback -- Applied to each new item after it is constructed. (optional)
        cargs -- A tuple of arguments to pass to callback after the new object.
        
        Returns a list of transmittable representations of the new items.
        """
        retval = []
        if not isinstance(cdata, types.ListType):
            cdata = [cdata]
        for item in cdata:
            try:
                if self.__id__:
                    iobj = self.__object__(item, self.__id__.get())
                else:
                    iobj = self.__object__(item)
            except DataCreationError, missing:
                print "returning fault"
                raise xmlrpclib.Fault(8, str(missing))
            #return xmlrpclib.dumps(xmlrpclib.Fault(8, str(missing)))
            self.append(iobj)
            if callback:
                callback(iobj, cargs)
            retval.append(iobj.to_rx(item))
        return retval

    def Get(self, cdata, callback=None, cargs={}):
        """Return a list of transmittable representations of items.
        
        Arguments:
        cdata -- A dictionary representing criteria to match.
            If cdata is a list, match against multiple sets of criteria.
        callback -- Applied to each matched item. (optional)
        cargs -- A tuple of arguments to pass to callback after the item.
        """
        retval = []
        if not isinstance(cdata, types.ListType):
            cdata = [cdata]
        for spec in cdata:
            for item in [datum for datum in self if datum.match(spec)]:
                if callback:
                    callback(item, cargs)
                retval.append(item.to_rx(spec))
        return retval

    def Del(self, cdata, callback=None, cargs={}):
        """Delete items from the dataset.
        
        Arguments:
        cdata -- A dictionary representing criteria to match.
            If cdata is a list, match against multiple sets of criteria.
        callback -- Applied to each matched item. (optional)
        cargs -- A tuple of arguments to pass to callback after the item.
        """
        retval = []
        if not isinstance(cdata, types.ListType):
            cdata = [cdata]
        for spec in cdata:
            for item in [datum for datum in self.data if datum.match(spec)]:
                self.data.remove(item)
                if callback:
                    callback(item, cargs)
                retval.append(item.to_rx(spec))
        return retval

    def Match(self, spec):
        return [item for item in self.data if item.match(spec)]

class ForeignData(Data):
    
    def Sync (self, spec):
        """directly update attributes based on spec.
        
        Specifically, this does not automatically update the stamp.
        """
        self._attrib.update(spec)

class ForeignDataSet(DataSet):
    __oserror__ = Cobalt.Util.FailureMode("ForeignData connection")
    __component__ = None
    __procedure__ = None
    __fields__ = []
    
    def Sync(self):
        comm = Cobalt.Proxy.CommDict()
        component = comm[self.__component__]
        procedure = getattr(component, self.__procedure__)
        spec = dict([(field, "*") for field in self.__fields__])
        try:
            foreign_data = procedure([spec])
        except xmlrpclib.Fault:
            self.__oserror__.Fail()
            return
        except:
            self.logger.error("Unexpected fault during data sync",
                              exc_info=1)
            return
        self.__oserror__.Pass()
        
        local_ids = [item.get(self.__unique__) for item in self]
        foreign_ids = [item_dict.get(self.__unique__) for item_dict in foreign_data]
        
        # sync removed items
        for item in self:
            if item.get(self.__unique__) not in foreign_ids:
                self.remove(item)
        
        # sync new items
        for item_dict in foreign_data:
            if item_dict.get(self.__unique__) not in local_ids:
                self.Add(item_dict)
        
        # sync all items
        for item_dict in foreign_data:
            self[item_dict.get(self.__unique__)].Sync(item_dict)
