'''Base state class to use with the Trireme statemachine.

'''
class DuplicateStateError(Exception):
    pass

class BaseTriremeState(object):

    _short_string = 'base'
    _destination_states = frozenset([])

    def __init__(self, context=None):
        self.context = context

    def __str__(self):
        return self._short_string

    def __repr__(self):
        return "<State '%s'>" % self._short_string

    def __hash__(self):
        return hash(self._short_string)

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def destination_states(self):
        '''List of states that are considered valid transitions from this state

        '''
        return self._destination_states

    def exit(self):
        '''Actions to execute on exiting a state

        '''
        pass

    def progress(self):
        '''Method called by statemachine.  This performs any actions needed by
        the state including checks to see which class to transition to.
        progress methods must return the next state to transition to, or return
        a handle back to the current state object.

        '''
        raise NotImplementedError('Progress has not been overridden.')

    def get_valid_transition_dict(self):
        '''Get a list of the valid state-to-state-transitions appropriate for use
        in TriremeStateMachine's statemachine.

        '''
        transition_dict = {}
        for state in self._destination_states:
            transition_dict[state._short_string] = state._short_string
        return transition_dict

    def validate_transition(self, new_state):
        '''Verify that a state transition is legal.

        '''
        if not isinstance(new_state, BaseTriremeState):
            raise TypeError, "%s is not a BaseTriremeState object"
        if new_state not in self._destination_states:
            return False
        return True
