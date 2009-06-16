'''State Machine'''

__revision__ = '$Revision$'

from Data import DataState
from Exceptions import DataStateError, DataStateTransitionError, StateMachineError, StateMachineIllegalEventError, \
    StateMachineNonexistentEventError

class StateMachine (DataState):
    """
    Generalized state machine driver
    
    Class attributes:
    _states -- list of states (must include the 'Terminal' state)
    _transitions -- list of legal state transitions in the form of (old state, new state) tuples
    _events -- list of events (may include the special 'Progress' state)
    _initial_state -- starting state (must be in the list of legal states)

    Methods:
    add_action -- add a new action routine to the list of routines associated with a (state, event) tuple
    add_terminal_action -- add a new action routine to the list of routines executed when the terminal state is reached
    trigger_event -- run the action routines associated with the current state and the supplied event

    Properties:
    _state - see DataState class
    _event -- event currently being triggered (None when not executing trigger_event routine)
    """

    _events = ['Progress']
    _states = DataState._states + ['Terminal']

    def __init__(self, spec, seas = None, terminal_actions = None):
        """
        Initialize a state machine instance

        Arguments:
        spec -- a dictionary passed to the underlying Data class (not used by the state machine)
        seas -- a dictionary mapping (state, event) tuples to lists of action routines
        terminal_actions -- list of action routines to be executed when the state machine reaches the terminal state; more
            specifically, each element in the list is a tuple of (action, args) where args is passed to action when it is called

        Exceptions:
        StateMachineError -- the state machine is incorrectly configured; accompanying message contains additional information
        """

        # if 'Progress' not in self._events:
        #     raise StateMachineError("progress event removed from list of events")
        if 'Terminal' not in self._states:
            raise StateMachineError("terminal state removed from list of states")

        try:
            DataState.__init__(self, spec)
        except DataStateError, e:
            raise StateMachineError(e.args)

        if seas != None:
            if not isinstance(seas, dict):
                raise StateMachineError("supplied SEAs parameter is not a dictionary")
            for key, actions in seas.iteritems():
                # verify that each key in the SEAs dict has a valid state and event
                if not isinstance(key, tuple) or len(key) != 2:
                    raise StateMachineError("SEAs dictionary contains an invalid (state, event) tuple: %s" % (key,))
                state, event = key
                if state not in self._states:
                    raise StateMachineError("SEAs dictionary contains an invalid state: %s" % (state,))
                if state == 'Terminal':
                    raise StateMachineError("SEAs dictionary must not contain entries for the 'Terminal' state")
                if event not in self._events:
                    raise StateMachineError("SEAs dictionary contains an invalid event: %s" % (event,))
                # verify that each value in the SEAs dict is a list of action functions
                if not isinstance(actions, list):
                    raise StateMachineError("entry %s in the SEAs dictionary is not a list: %s" % (key, actions))
                for action in actions:
                    if not callable(action):
                        raise StateMachineError( \
                            "entry %s in the SEAs dictionary has an action that is not a function: %s" % (key, action))
            self.__seas = seas
        else:
            self.__seas = {}

        if terminal_actions != None:
            if not isinstance(terminal_actions, list):
                raise StateMachineError("terminal_actions is not a list")
            item_num  = 0
            for item in terminal_actions:
                if not isinstance(item, tuple) or len(item) != 2:
                    raise StateMachineError("terminal_actions entry %d is not a tuple of size 2: %s" % (item_num, item))
                action, args = item
                if not callable(action):
                    raise StateMachineError("the action in entry %d of the terminal_actions is not a function: %s" % \
                        (item_num, action))
                if not isinstance(args, dict):
                    raise StateMachineError("the arguments in entry %d of the terminal_actions is not a dictionary: %s" % \
                        (item_num, action))
            self.__terminal_actions = terminal_actions
        else:
            self.__terminal_actions = []

        self.__event = None

        DataState._state.__set__(self, self._initial_state)

    def __get_event(self):
        '''return the event currently being triggered'''
        return self.__event

    _event = property(__get_event)

    def add_action(self, state, event, action):
        """
        Add a new action routine to the list of routines executed when the event is triggered in the specified state

        Arguments:
        state -- state portion of (state, event) tuple
        event -- event portion of (state, event) tuple
        action -- action routine to add to the actions list associated with (state, event) tuple

        Exceptions:
        DataStateError -- the specified state is not in the list of valid states
        StateMachineNonexistentEventError -- the specified event is not in the list of valid events
        StateMachineError - the specfied action routine is not a function or method
        """

        if state not in self._states:
            raise DataStateError(state)
        if event not in self._events:
            raise StateMachineNonexistentEventError(event)
        if not callable(action):
            raise StateMachineError("action is not a function: %s" % (action,))
        if not self.__seas.has_key((state, event)):
            self.__seas[(state, event)] = []
        self.__seas[(state, event)] += [action]

    def add_terminal_action(self, action, args = {}):
        """
        Add a new action routine to the list of routines executed when the terminal state is reached

        Arguments:
        action -- action routine to add to the terminal actions list
        args -- dictionary of arguments to pass to the action routine

        Exceptions:
        StateMachineError - the specfied action routine is not a function or method
        """

        if not callable(action):
            raise StateMachineError("action is not a function: %s" % (action,))
        if not isinstance(args, dict):
            raise StateMachineError("args is not a dictionary: %s" % (action,))
        self.__terminal_actions += [(action, args)]

    def trigger_event(self, event, args = {}):
        """
        Run the action routines associated with the current state and the specified event

        Arguments:
        event -- event to trigger
        args -- dictionary of arguments to pass to the action routines

        Exceptions:
        StateMachineNonexistentEventError -- the specified event is not in the list of valid events
        StateMachineIllegalEventError -- the specified event is not legal for the current state
        """

        if self.__seas.has_key((DataState._state.__get__(self), event)):
            self.__event = event
            for action in self.__seas[(DataState._state.__get__(self), event)]:
                action(args)
            if DataState._state.__get__(self) == 'Terminal':
                for action, ta_args in self.__terminal_actions:
                    action(ta_args)
                self.__terminal_actions = []
            self.__event = None
        else:
            if event != 'Progress':
                if event in self._events:
                    raise StateMachineIllegalEventError(DataState._state.__get__(self), event)
                else:
                    raise StateMachineNonexistentEventError(event)
