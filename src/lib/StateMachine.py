'''State Machine'''

__revision__ = '$Revision$'

from Data import DataState
from Exceptions import DataStateError, DataStateTransitionError, StateMachineError, StateMachineIllegalEventError, \
    StateMachineNonexistentEventError
import types

class StateMachine (DataState):
    """
    Generalized state machine driver
    
    Class attributes:
    states -- list of states (must include the 'Terminal' state)
    transitions -- list of legal state transitions in the form of (old state, new state) tuples
    events -- list of events (may include the special 'Progress' state)
    initial_state -- starting state (must be in the list of legal states)

    Methods:
    add_action -- add a new action routine to the list of routines associated with a (state, event) tuple
    add_terminal_action -- add a new action routine to the list of routines executed when the terminal state is reached
    trigger_event -- run the action routines associated with the current state and the supplied event

    Properties:
    state - see DataState class
    """

    events = ['Progress']
    states = DataState.states + ['Terminal']

    def __init__(self, spec, seas = None, terminal_actions = None):
        """
        Initialize a state machine instance

        Arguments:
        spec -- a dictionary passed to the underlying Data class (not used by the state machine)
        seas -- a dictionary mapping (state, event) tuples to lists of action routines
        terminal_actions -- list of action routines to be executed when the state machine reaches the terminal state

        Exceptions:
        StateMachineError -- the state machine is incorrectly configured; accompanying message contains additional information
        """

        # if 'Progress' not in self.events:
        #     raise StateMachineError("progress event removed from list of events")
        if 'Terminal' not in self.states:
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
                if state not in self.states:
                    raise StateMachineError("SEAs dictionary contains an invalid state: %s" % (state,))
                if state == 'Terminal':
                    raise StateMachineError("SEAs dictionary must not contain entries for the 'Terminal' state")
                if event not in self.events:
                    raise StateMachineError("SEAs dictionary contains an invalid event: %s" % (event,))
                # verify that each value in the SEAs dict is a list of action functions
                if not isinstance(actions, list):
                    raise StateMachineError("entry %s in the SEAs dictionary is not a list: %s" % (key, actions))
                for action in actions:
                    if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
                        raise StateMachineError( \
                            "entry %s in the SEAs dictionary has an action that is not a function: %s" % (key, action))
            self._seas = seas
        else:
            self._seas = {}

        if terminal_actions != None:
            if not isinstance(terminal_actions, list):
                raise StateMachineError("terminal_actions is not a list of functions")
            for action in terminal_actions:
                if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
                    raise StateMachineError("terminal_actions list has an element that is not a function: %s" % (action,))
            self._terminal_actions = terminal_actions
        else:
            self._terminal_actions = []

        self.state = self.initial_state

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

        if state not in self.states:
            raise DataStateError(state)
        if event not in self.events:
            raise StateMachineNonexistentEventError(event)
        if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
            raise StateMachineError("action is not a function: %s" % (action,))
        if not self._seas.has_key((state, event)):
            self._seas[(state, event)] = []
        self._seas[(state, event)] = self._seas[(state, event)] + [action]

    def add_terminal_action(self, action):
        """
        Add a new action routine to the list of routines executed when the terminal state is reached

        Arguments:
        action -- action routine to add to the terminal actions list

        Exceptions:
        StateMachineError - the specfied action routine is not a function or method
        """

        if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
            raise StateMachineError("action is not a function: %s" % (action,))
        self._terminal_actions = self._terminal_actions + [action]

    def trigger_event(self, event, args={}):
        """
        Run the action routines associated with the current state and the specified event

        Arguments:
        event -- event to trigger
        args -- dictionary of arguments to pass to the action routines

        Exceptions:
        StateMachineNonexistentEventError -- the specified event is not in the list of valid events
        StateMachineIllegalEventError -- the specified event is not legal for the current state
        """

        if self._seas.has_key((self.state, event)):
            for action in self._seas[(self.state, event)]:
                action(event, args)
            if self.state == 'Terminal':
                for action in self._terminal_actions:
                    action()
                self._terminal_actions = []
        else:
            if event != 'Progress':
                if event in self.events:
                    raise StateMachineIllegalEventError(self.state, event)
                else:
                    raise StateMachineNonexistentEventError(event)
