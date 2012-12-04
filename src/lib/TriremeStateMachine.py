#!/usr/bin/python
# -*- coding: utf-8 -*-
"""State machine classes"""

class StateMachineError(Exception):
    pass

class StoredFunction(object):
    """An object to store a function and its arguments for execution later"""
    def __init__(self, func, args, kwargs):
        """Initilize the object"""
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.results = None

    def __call__(self):
        """Allow the object to be call just as if it were a function"""
        self.results = self.func(*self.args, **self.kwargs)
        return self.results

class StateMachineProcessor(object):
    """State machine class"""
    def __init__(self):
        """set up default variables"""
        self.active = True
        self.transitions = {}
        self.events = {} #occur every process on a state
        self.triggers = {} #occur on change to a state
        self.__state = None
        self.__initial_state = None
        self.__exception_state = None

    def set_state(self, state):
        """set the state"""
        if state not in self.transitions.keys():
            raise StateMachineError("%s is not a valid state" % state)
        else:
            self.__state = state

    def get_state(self):
        """get the current state"""
        return self.__state

    def get_next_state(self):
        """get the next state for the machine"""
        return self.get_current_directions()

    def set_exceptionstate(self, state):
        """set the exception state
        if you have no directions, this is the state it will use."""
        self.__exception_state = state

    def get_exceptionstate(self):
        """get the exception state"""
        return self.__exception_state

    def set_initialstate(self, state):
        """set the initial state"""
        self.__initial_state = state

    def get_initialstate(self):
        """get the initial state"""
        return self.__initial_state

    def add_transition(self, transition, function, resultdct):
        """add a transition"""
        transdct = {}
        transdct['function'] = function
        transdct['directions'] = resultdct
        self.transitions[transition] = transdct

    def initialize(self):
        """Check to make sure everything is ready to go."""
        assert self.__initial_state != None, "Initial State not set."
        self.set_state(self.get_initialstate())
        assert self.__state != None, "Current state not set."
        assert self.__exception_state != None, "Exception state not set."

    def get_current_function(self):
        """Get the current function to execute"""
        return self.transitions[self.get_state()]['function']

    def get_current_directions(self):
        """Based on the output from the function determin the function"""
        return self.transitions[self.get_state()]['directions']

    def add_event(self, state, func):
        """This adds a event that occur at the rising edge of the given state"""
        if not self.events.has_key(state):
            self.events[state] = []
        self.events[state].append(func)

    def get_events(self, state):
        """return the events for a state"""
        return self.events[state]

    def add_trigger(self, state, func):
        """This adds a trigger that occur at the rising edge of the given
        state"""
        if not self.triggers.has_key(state):
            self.triggers[state] = []
        self.triggers[state].append(func)

    def get_triggers(self, state):
        """return the trigger for a state"""
        return self.triggers[state]

    def start(self):
        """set the process to active"""
        self.active = True

    def stop(self):
        """set the process to inactive"""
        self.active = False

    def fire_event(self):
        """fire an event if one exists
        This can be used to stop processing or execute a function when a 
        state is changed to something else.
        Occurs at any time"""
        #check if there is an event
        state = self.get_state()
        if state in self.events.keys():
            funcs = self.get_events(state)
            for func in funcs:
                func()

    def fire_trigger(self, new_state):
        """fire an event if one exists
        This can be used to stop processing or execute a function when a
        state is changed to something else.
        Only occures on a transition."""
        if self.get_state() != new_state:
            #check if there is an event
            if new_state in self.triggers.keys():
                funcs = self.get_triggers(new_state)
                for func in funcs:
                    func()

    def process(self, *args, **kargs):
        """get the current state function,
        execute the function,
        move to the next state in the result director"""
        #FIXME: pass the process arguments in
        new_state = self.get_state()
        if self.active == True:
            func = self.get_current_function()
            ret = func()
            directions = self.get_current_directions()
            new_state = directions.get(ret, self.get_exceptionstate())

            self.fire_event()
            self.fire_trigger(new_state)
            self.set_state(new_state)
        return new_state
