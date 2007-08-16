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

    def __init__(self, info):
        if info.has_key('tag'):
            self.tag = info['tag']
            del info['tag']
        missing = [field for field in self.required_fields if not info.has_key(field)]
        if missing:
            raise DataCreationError, missing
        self._attrib = {}
        self.set('stamp', time.time())
        self._attrib.update(info)

    def get(self, field, default=None):
        '''return attribute'''
        if self._attrib.has_key(field):
            return self._attrib[field]
        if default != None:
            return default
        raise KeyError, field

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
        fields = [field for field in spec if field != 'tag']
        return self.tag == spec['tag'] and not [field for field in fields if spec[field] != '*' and (self.get(field) != spec[field])]
        
    def to_rx(self, spec):
        '''return transmittable version of instance'''
        rxval = {'tag':self.tag}
        for field in [field for field in spec.keys() if field != 'tag' and self._attrib.has_key(field)]:
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

    def Add(self, cdata, callback=None, cargs=()):
        '''Implement semantics of operations that add new item(s) to the DataSet'''
        retval = []
        if type(cdata) != types.ListType:
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
            self.data.append(iobj)
            if callback:
                apply(callback, (iobj, ) + cargs)
            retval.append(iobj.to_rx(item))
        return retval

    def Get(self, cdata, callback=None, cargs={}):
        '''Implement semantics of operations that get item(s) from the DataSet'''
        retval = []
        for spec in cdata:
            for item in [datum for datum in self.data if datum.match(spec)]:
                if callback:
                    callback(item, cargs)
                retval.append(item.to_rx(spec))
        return retval

    def Del(self, cdata, callback=None, cargs={}):
        '''Implement semantics of operations that delete item(s) from the DataSet'''
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
    def Sync(self, data):
        upd = [(k, v) for (k, v) in data.iteritems() \
               if k != 'tag' and self.get(k) != v]
        if upd:
            logger.info("Resetting job %s parameters %s" % \
                        (self.get('jobid'), ':'.join([u[0] for u in upd])))
            for (k, v) in upd:
                self.set(k, v)

class ForeignDataSet(DataSet):
    __failname__ = 'QM Connection'
    __oserror__ = Cobalt.Util.FailureMode(__failname__)
    
    def Sync(self):
        try:
            spec = [dict([(key, '*') for key in self.__osource__[2]])]
            func = getattr(comm[self.__osource__[0]],
                           self.__osource__[1])
            data = func(spec)
        except xmlrpclib.Fault:
            self.__oserror__.Fail()
            return
        except:
            self.logger.error("Unexpected fault during data sync",
                              exc_info=1)
            return
        self.__oserror__.Pass()
        exists = [item.get(self.__oidfield__) for item in self]
        active = [item.get(self.__oidfield__) for item in data]
        syncd = dict([(item.get(self.__oidfield__), item) \
                      for item in self \
                      if item.get(self.__oidfield__) in active])
        done = [item for item in exists if item not in active]
        new_o = [item for item in data \
                 if item.get(self.__oidfield__) not in exists]
        # remove finished jobs
        [self.data.remove(item) for item in self \
         if item.get(self.__oidfield__) in done]
        # create new jobs
        [self.data.append(self.__object__(data)) for data in new_o]
        # sync existing jobs
        for item in [item for item in self \
                     if item.get(self.__oidfield__) in syncd]:
            item.Sync(syncd[item.get(self.__oidfield__)])
