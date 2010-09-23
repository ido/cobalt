"""XML-transportable state objects."""

__revision__ = '$Revision$'

import time
import random
import warnings

import Cobalt.Util
from Cobalt.Exceptions import DataCreationError, IncrIDError, DataStateError, DataStateTransitionError


def get_spec_fields (specs):
    """Given a list of specs, return the set of all fields used."""
    fields = set()
    for spec in specs:
        for field in spec.keys():
            fields.add(field)
    return fields



class IncrID (object):
    
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

    def set(self, val):
        """Set the next id.  val cannot be less than the current value of idnum."""
        if val - 1 < self.idnum:
            raise IncrIDError("The new jobid must be greater than the next jobid (%d)" % (self.idnum + 1))
        else:
            self.idnum = val - 1

class RandomID (object):
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
    fields -- list of public data fields for the entity
    inherent -- a list of fields that cannot be included in the spec
    required -- a list of fields required in the spec
    explicit -- fields that are only returned when explicitly listed in the spec

    Attributes:
    tag -- Misc. label.
    
    Methods:
    update -- Set the value of multiple fields at once.
    match -- Test that a spec identifies a data.
    to_rx -- Convert a data to an explicit spec.
    """
    
    fields = ["tag"]
    inherent = []
    required = []
    explicit = []

    def __init__ (self, spec):
        
        """Initialize a Data item.
        
        Arguments:
        spec -- A dictionary specifying the values of fields on the entity.
        """
        
        self.tag = spec.get("tag", "unknown")
        missing = [item for item in self.required if item not in spec]
        if missing:
            raise DataCreationError, "Missing fields %s" % (":".join(missing))
        inherent = [item for item in self.inherent
                    if item in spec and spec[item] != '*']
        if inherent:
            raise DataCreationError, "Specified inherent field %s" \
                  % (":".join(inherent))

    def match (self, spec):
        """True if every field in spec == the same field on the entity.
        
        Arguments:
        spec -- Dictionary specifying fields and values to match against.
        """
        for field, value in spec.iteritems():
            if not (value == "*" or (field in self.fields and hasattr(self, field) and getattr(self, field) == value)):
                return False
        return True
    
    def to_rx (self, fields=None):
        """Return a transmittable version of an entity.
        
        Arguments:
        fields -- List of fields to include. (default self.fields.keys() - self.explicit.keys())
        """
        if fields is None:
            fields = [field for field in self.fields if field not in self.explicit]
        return dict([(field, getattr(self, field, None)) for field in fields])
    
    def update (self, spec):
        """Update the values of multiple fields on an entity.
        
        Arguments:
        spec -- A dictionary specifying the values of fields to set.
        """
        # warnings.warn("Use of Cobalt.Data.Data.update is deprecated. Use attributes in stead.", DeprecationWarning, stacklevel=2)
        for key, value in spec.iteritems():
            if key not in self.fields:
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
            warnings.warn("Creating new attribute '%s' on '%s' with set." % (field, self), RuntimeWarning, stacklevel=2)
        setattr(self, field, value)


class DataState(Data):
    """Instance class for state machine instances

    Class attributes:
    _states -- list of states
    _transistions -- list of legal state transistions in the form of (old state, new state) tuples
    _initial_state -- starting state (must be in the list of states)

    Properties:
    _state - get current state; transition to a new state (must be a legal transition as defined in the list of transitions)
    """

    _initial_state = None
    _states = []
    _transitions = []

    def __init__(self, spec):
        """Validate states and transitions

        Arguments:
        spec -- a dictionary passed to the underlying Data class

        Exceptions:
        DataStateError -- _states, _transitions or _initial_state contains an improper value; accompanying message contains
            additional information
        """
        Data.__init__(self, spec)

        if not isinstance(self._states, list):
            raise DataStateError("_states attribute is not a list: %s" % (self._states,))

        if self._initial_state == None:
            raise DataStateError("_initial_state is not set")
        if self._initial_state not in self._states:
            raise DataStateError("_initial_state is not a valid state: %s" % (self._initial_state,))

        if not isinstance(self._transitions, list):
            raise DataStateError("_transitions attribute is not a list: %s" % (self._transitions,))
        for transition in self._transitions:
            if not isinstance(transition, tuple) or len(transition) != 2:
                raise DataStateError("_transition is not a 2-tuple: %s" % (transition,))
            old_state, new_state = transition
            if old_state not in self._states:
                raise DataStateError("_transition contains a invalid state: %s" % (old_state,))
            if new_state not in self._states:
                raise DataStateError("_transition contains a invalid state: %s" % (new_state,))

    def __get_state(self):
        """Get the current state"""
        return self.__state

    def __set_state(self, newvalue):
        """Set state to new value, ensuring it is a proper state and respects the state machine"""
        if newvalue not in self._states:
            raise DataStateError(newvalue)
        if not hasattr(self, '_DataState__state'):
            if newvalue != self._initial_state:
                raise DataStateError(newvalue)
        elif (self.__state, newvalue) not in self._transitions:
            raise DataStateTransitionError((self.__state, newvalue))
        self.__state = newvalue
    
    _state = property(__get_state, __set_state, doc = """
Get -- get the current state

Set -- set state to new value, ensuring it is a proper state and respects the state machine

    Exceptions:
    DataStateError -- the specified state is not in the list of valid states or is not a valid initial state
    DataStateTransitionError -- transitioning from the current state to the new state is not legal
""")


class DataList (list):
    
    """A Python list with the Cobalt query interface.
    
    Class attributes:
    item_cls -- the class used to construct new items
    
    Methods:
    q_add -- construct new items in the list
    q_get -- retrieve items from the list
    q_del -- remove items from the list
    """
    
    item_cls = Data
    
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
        matched_items = set()
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
    
    item_cls = Data
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
                callback(item, cargs)
        self.update(new_items)
        return new_items.values()

    def q_get (self, specs, callback=None, cargs={}):
        """Return a list of matching items.
        
        Arguments:
        specs -- a list of dictionaries specifying the objects to match
        callback -- applied to each matched item (optional)
        cargs -- a tuple of arguments to pass to callback after the item
        """
        matched_items = set()
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
    
    def copy (self):
        return self.__class__((key, value) for key, value in self.iteritems())


class ForeignData (Data):
    
    def Sync (self, spec):
        """Update the values of multiple fields on an entity.
        
        Ensures that any specified timestamp remains consistent.
        
        Arguments:
        spec -- A dictionary specifying the values of fields to set.
        """
        for key, value in spec.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)


class ForeignDataDict(DataDict):
    __oserror__ = Cobalt.Util.FailureMode("ForeignData connection")
    __function__ = lambda x:[]
    __procedure__ = None
    __fields__ = []
    
    def Sync(self):
        spec = dict([(field, "*") for field in self.__fields__])
        try:
            foreign_data = self.__function__([spec])
        except:
            self.__oserror__.Fail()
            return
        self.__oserror__.Pass()
        
        local_ids = [getattr(item, self.key) for item in self.itervalues()]
        foreign_ids = [item_dict[self.key] for item_dict in foreign_data]
        
        # sync removed items
        for item in local_ids:
            if item not in foreign_ids:
                del self[item]
        
        # sync new items
        for item_dict in foreign_data:
            if item_dict[self.key] not in local_ids:
                self.q_add([item_dict])
        
        # sync all items
        for item_dict in foreign_data:
            item_id = item_dict[self.key]
            self[item_id].Sync(item_dict)
