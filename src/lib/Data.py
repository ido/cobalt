'''Data builds up datatype definitions on top of XML-RPC serializable python types'''
__revision__ = '$Revision$'

import time, types, xmlrpclib, random
import warnings
import sets

import Cobalt.Util


def get_spec_fields (specs):
    """Given a list of specs, return the set of all fields used."""
    fields = sets.Set()
    for spec in specs:
        for field in spec.keys():
            fields.add(field)
    return fields


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


class Data (object):
    
    """A Cobalt entity manager.
    
    Setting a field attribute on a data updates the timestamp automatically.
    
    Class attributes:
    fields -- Public data fields for the entity.
    required_fields -- Fields that must be specified at initialization.
    
    Fields:
    tag -- Misc. label.
    stamp -- Timestamp of last field change (or last touch call).
    
    Methods:
    touch -- Update timestamp 'stamp'.
    update -- Set the value of multiple fields at once.
    match -- Test that a spec identifies a data.
    to_rx -- Convert a data to an explicit spec.
    """
    
    fields = dict(
        tag = None,
        stamp = None,
    )
    required_fields = []
    
    def __init__ (self, spec=None):
        
        """Initialize a new Data manager.
        
        Arguments:
        spec -- A dictionary specifying the values of fields on the entity.
        """
        
        if spec is None:
            spec = self.fields.copy()
        else:
            _spec = self.fields.copy()
            _spec.update(spec)
            spec = _spec
        
        for field, value in spec.iteritems():
            if getattr(self, field, None) is None:
                setattr(self, field, value)
        
        for field in self.required_fields:
            if getattr(self, field, None) is None:
                raise DataCreationError, field
        
        self.touch()
    
    def __setattr__ (self, name, value):
        if name in self.fields:
            object.__setattr__(self, "stamp", time.time())
        object.__setattr__(self, name, value)
    
    def __setstate__ (self, input_state):
        
        state = self.fields.copy()
        state.update(input_state)
        
        if "_attrib" in state:
            _attrib = state["_attrib"]
            
            for key, value in _attrib.iteritems():
                key = key.replace("-", "_")
                state[key] = value
            del state["_attrib"]
        
        self.__dict__ = state
    
    def touch (self):
        """Update the timestamp."""
        self.stamp = time.time()
    
    def match (self, spec):
        """True if every field in spec == the same field on the entity.
        
        Arguments:
        spec -- Dictionary specifying fields and values to match against.
        """
        for field, value in spec.iteritems():
            if not (value == "*" or (hasattr(self, field) and getattr(self, field) == value)):
                return False
        return True
    
    def to_rx (self, fields=None):
        """Return a transmittable version of an entity.
        
        Arguments:
        fields -- List of fields to include. (default self.fields.keys())
        """
        if fields is None:
            fields = self.fields.keys()
        return dict([(field, getattr(self, field, None)) for field in fields])
    
    # deprecated interface definition below here
    # ==========================================
    
    def update (self, spec):
        """Update the values of multiple fields on an entity.
        
        Though this method has not been officially deprecated, it should not
        be used in new code.
        
        Arguments:
        spec -- A dictionary specifying the values of fields to set.
        """
        for key, value in spec.iteritems():
            if not hasattr(self, key):
                warnings.warn("Creating new attribute '%s' on '%s' with update." % (key, self), RuntimeWarning, stacklevel=2)
            setattr(self, key, value)
    
    def get (self, field, default=None):
        """(deprecated) Get the value of field from the entity.
        
        Arguments:
        field -- The field to get the value of.
        default -- Value to return if field is not set. (default None)
        """
        warnings.warn("Use of Cobalt.Data.Data.get is deprecated. Use attributes in stead.", DeprecationWarning, stacklevel=2)
        return getattr(self, field, default)

    def set (self, field, value):
        """(deprecated) Set the value of field on the entity.
        
        Arguments:
        field -- The field to set the value of.
        value -- Value to set on the field.
        """
        warnings.warn("Use of Cobalt.Data.Data.set is deprecated. Use attributes in stead.", DeprecationWarning, stacklevel=2)
        if field not in self.fields:
            warnings.warn("Creating new field '%s' on '%s' with set." % (field, self), RuntimeWarning, stacklevel=2)
            self.fields[field] = None
        setattr(self, field, value)


class Job (Data):
    
    """The canonical definition of a Cobalt job.
    
    Attributes:
    tag -- "job"
    id -- unique id
    state -- current state of the job (queued, running, done)
    executable -- file to execute
    args -- arguments to pass to the executable
    stdin -- file to use for stdin
    stdout -- file to use for stdout
    stderr -- file to use for stderr
    cwd -- current working directory
    env -- environment variables for the job
    user -- user executing the job
    exit -- exit status of the job
    kerneloptions -- options to pass to the kernel
    size -- number of nodes/processes in the job
    location -- where to execute the job (partition?)
    mode -- execution mode of the job
    """
    
    fields = Data.fields.copy()
    fields.update(dict(
        tag = "job",
        id = None,
        state = None,
        executable = None,
        args = None,
        stdin = "/dev/null",
        stdout = "/dev/null",
        stderr = "/dev/null",
        cwd = None,
        env = None,
        user = None,
        exit = None,
        kerneloptions = None,
        size = None,
        location = None,
        mode = None,
    ))


class DataList (list):
    
    """A Python list with the Cobalt query interface.
    
    Class attributes:
    item_cls -- the class used to construct new items
    
    Methods:
    q_add -- construct new items in the list
    q_get -- retrieve items from the list
    q_del -- remove items from the list
    """
    
    item_cls = None
    
    def q_add (self, specs, callback=None, cargs={}):
        """Construct new items of type self.item_cls in the list.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to create
        callback -- applied to each new item after it is constructed (optional)
        cargs -- a tuple of arguments to pass to callback after the new item
        
        Returns a list of containing the new items.
        """
        new_items = []
        for spec in specs:
            new_item = self.item_cls(spec)
            new_items.append(new_item)
        if callback:
            for item in new_items:
                callback(new_item, cargs)
        self.extend(new_items)
        return new_items

    def q_get (self, specs, callback=None, cargs={}):
        """Retrieve items from the list.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to match
        callback -- applied to each matched item (optional)
        cargs -- a tuple of arguments to pass to callback after the item
        """
        matched_items = sets.Set()
        for item in self:
            for spec in specs:
                if item.match(spec):
                    matched_items.add(item)
                    break
        if callback:
            for item in matched_items:
                callback(item, cargs)
        return list(matched_items)

    def q_del (self, specs, callback=None, cargs={}):
        """Remove items from the list.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to delete
        callback -- applied to each matched item (optional)
        cargs -- a tuple of arguments to pass to callback after the item
        """
        matched_items = self.q_get(specs, callback, cargs)
        for item in matched_items:
            self.remove(item)
        return matched_items


class DataDict (dict):
    
    """A Python dict with the Cobalt query interface.
    
    Class attributes:
    item_cls -- the class used to construct new items
    key -- attribute name to use as a key in the dictionary
    
    Methods:
    q_add -- construct new items in the dict
    q_get -- retrieve items from the dict
    q_del -- remove items from the dict
    """
    
    item_cls = None
    key = None
    
    def q_add (self, specs, callback=None, cargs={}):
        """Construct new items of type self.item_cls in the dict.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to create
        callback -- applied to each new item after it is constructed (optional)
        cargs -- a tuple of arguments to pass to callback after the new item
        
        Returns a list containing the new items.
        """
        new_items = {}
        for spec in specs:
            new_item = self.item_cls(spec)
            key = getattr(new_item, self.key)
            if key in self or key in new_items:
                raise KeyError(key)
            new_items[key] = new_item
        if callback:
            for item in new_items.itervalues():
                callback(new_item, cargs)
        self.update(new_items)
        return new_items.values()

    def q_get (self, specs, callback=None, cargs={}):
        """Return a list of matching items.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to match
        callback -- applied to each matched item (optional)
        cargs -- a tuple of arguments to pass to callback after the item
        """
        matched_items = sets.Set()
        for item in self.itervalues():
            for spec in specs:
                if item.match(spec):
                    matched_items.add(item)
                    break
        if callback:
            for item in matched_items:
                callback(item, cargs)
        return list(matched_items)

    def q_del (self, specs, callback=None, cargs={}):
        """Remove items from the dict.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to delete
        callback -- applied to each matched item (optional)
        cargs -- a tuple of arguments to pass to callback after the item
        """
        matched_items = self.q_get(specs, callback, cargs)
        for item in matched_items:
            key = getattr(item, self.key)
            del self[key]
        return matched_items


class DataSet(object):
    """A collection of datas.
    
    Class attributes:
    __object__ -- The class used to construct new data instances.
    __id__ --
    __unique__ -- Data field to use as a unique identity. (like a primary key)
    
    A dataset behaves primarily like a list, providing iteration over the items
    in the set. However, set[key] access is available when __unique__ is set.
    
    Methods:
    keys -- The unique keys present in the collection.
    append -- Add an item to the set.
    remove -- Remove an item from the set.
    
    Strange methods:
    Add -- Create new items in the set from a spec (or list of specs).
    Get -- Return explicit specs that represent items in the set that match a spec (or list of specs).
    Del -- Remove items from the set that match a spec (or list of specs).
    Match -- Return items from the set that match a single spec.
    """
    __object__ = Data
    __id__ = None
    __unique__ = None
    
    def keys (self):
        if not self.__unique__:
            raise KeyError("No unique key is set.")
        return [getattr(item, self.__unique__) for item in self.data]

    def __init__(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        if not self.__unique__:
            raise KeyError("No unique key is set.")
        for item in self:
            if getattr(item, self.__unique__) == key:
                return item
        raise KeyError(key)
    
    def __delitem__(self, key):
        self.remove(self[key])

    def append(self, item):
        '''add a new element to the set'''
        if self.__unique__ and getattr(item, self.__unique__) in self.keys():
            raise KeyError("duplicate: %s" % getattr(item, self.__unique__))
        self.data.append(item)

    def remove(self, x):
        '''remove an element from the set'''
        self.data.remove(x)

    def Add(self, specs, callback=None, cargs={}):
        """Construct new items of type self.__object__ in the dataset.
        
        Arguments:
        specs -- a dictionary (or list of dictionaries) specifying the object(s) to create
        callback -- Applied to each new item after it is constructed. (optional)
        cargs -- A tuple of arguments to pass to callback after the new object.
        
        Returns a list of transmittable representations of the new items.
        """
        retval = []
        if not isinstance(specs, types.ListType):
            specs = [specs]
        for item in specs:
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

    def Get(self, specs, callback=None, cargs={}):
        """Return a list of transmittable representations of items.
        
        Arguments:
        specs -- a dictionary (or list of dictionaries) specifying the objects to match
        callback -- Applied to each matched item. (optional)
        cargs -- A tuple of arguments to pass to callback after the item.
        """
        retval = []
        if not isinstance(specs, types.ListType):
            specs = [specs]
        for spec in specs:
            for item in [datum for datum in self if datum.match(spec)]:
                if callback:
                    callback(item, cargs)
                retval.append(item.to_rx(spec))
        return retval

    def Del(self, specs, callback=None, cargs={}):
        """Delete items from the dataset.
        
        Arguments:
        specs -- a dictionary (or list of dictionaries) specifying the object(s) to create
        callback -- Applied to each matched item. (optional)
        cargs -- A tuple of arguments to pass to callback after the item.
        """
        retval = []
        if not isinstance(specs, types.ListType):
            specs = [specs]
        for spec in specs:
            for item in [datum for datum in self.data if datum.match(spec)]:
                self.data.remove(item)
                if callback:
                    callback(item, cargs)
                retval.append(item.to_rx(spec))
        return retval

    def Match(self, spec):
        return [item for item in self if item.match(spec)]


class ForeignData(Data):
    
    def Sync (self, spec):
        """Update the values of multiple fields on an entity.
        
        Ensures that any specified timestamp remains consistent.
        
        Arguments:
        spec -- A dictionary specifying the values of fields to set.
        """
        self.update(spec)
        if "stamp" in spec:
            self.stamp = spec['stamp']


class ForeignDataSet(DataSet):
    __oserror__ = Cobalt.Util.FailureMode("ForeignData connection")
    __function__ = lambda x:[]
    __procedure__ = None
    __fields__ = []
    
    def Sync(self):
        spec = dict([(field, "*") for field in self.__fields__])
        try:
            foreign_data = self.__function__([spec])
        except Exception:
            self.__oserror__.Fail()
            return
        except:
            Cobalt.Util.logger.error("Unexpected fault during data sync",
                                     exc_info=1)
            return
        self.__oserror__.Pass()
        
        local_ids = [getattr(item, self.__unique__) for item in self]
        foreign_ids = [item_dict[self.__unique__] for item_dict in foreign_data]
        
        # sync removed items
        for item in self:
            if getattr(item, self.__unique__) not in foreign_ids:
                self.remove(item)
        
        # sync new items
        for item_dict in foreign_data:
            if item_dict[self.__unique__] not in local_ids:
                self.Add(item_dict)
        
        # sync all items
        for item_dict in foreign_data:
            item_id = item_dict[self.__unique__]
            self[item_id].Sync(item_dict)
