'''Data builds up datatype definitions on top of XML-RPC serializable python types'''
__revision__ = '$Revision$'

import time, types, xmlrpclib, random

class DataCreationError(Exception):
    '''Used when a new object cannot be created'''
    pass

class IncrID(object):
    '''Autoincrementing id generator'''
    def __init__(self):
        self.idnum = 0

    def get(self):
        '''Return new ID'''
        self.idnum += 1
        return self.idnum

class RandomID(object):
    '''Somewhat randomly selected unique ID pool'''
    def __init__(self):
        self.used = []
        self.rand = random.Random(int(time.time()))

    def get(self):
        '''Return new random id'''
        idnum = str(self.rand.randrange(0, 2147483639)) + str(self.rand.randrange(0, 2147483639))
        while idnum in self.used:
            idnum = str(self.rand.randrange(0, 2147483639)) + \
            str(self.rand.randrange(0, 2147483639))
        self.used.append(idnum)
        return idnum

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
            if default:
                return default
            raise

    def set(self, field, value):
        '''set attribute'''
        self._attrib[field] = value
        self._attrib['stamp'] = time.time()

    def update(self, attrdict):
        '''update attributes based on attrdict'''
        for item in attrdict.iteritems():
            self.set(item[0], item[1])
            
    def match(self, spec):
        '''Implement datatype matching'''
        fields_delta = [field for field in spec
            if spec[field] != '*'
            and (self.get(field) != spec[field])
        ]
        return not fields_delta
        
    def to_rx(self, spec):
        '''return transmittable version of instance'''
        rxval = dict()
        rx_fields = [field for field in spec.keys() if self._attrib.has_key(field)]
        for field in rx_fields:
            rxval[field] = self.get(field)
        return rxval

class DataSet(object):
    '''DataSet provides storage, iteration, and matching across sets of Data instances'''
    __object__ = Data
    __id__ = None
    __unique__ = False

    def __init__(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)

    def append(self, x):
        '''add a new element to the set'''
        return self.data.append(x)

    def remove(self, x):
        '''remove an element from the set'''
        return self.data.remove(x)

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
            # uniqueness test goes here
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
            for item in [datum for datum in self.data if datum.match(spec)]:
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
