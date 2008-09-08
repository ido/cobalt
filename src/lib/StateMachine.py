'''State Machine'''

__revision__ = '$Revision$'

from Data import DataState
from Exceptions import DataStateError, DataStateTransitionError, StateMachineError, StateMachineIllegalEventError, \
    StateMachineNonexistentEventError
import types

class StateMachine (DataState):
    events = ['Progress']
    DataState.states = ['Terminal']

    def __init__(self, spec):
        if 'Progress' not in self.events:
            raise StateMachineError("Progress event removed from list of events")
        if 'Terminal' not in self.states:
            raise StateMachineError("Terminal state removed from list of states")

        DataState.__init__(self, spec)

        if spec.has_key('actions'):
            if not isinstance(spec['actions'], dict):
                raise StateMachineError("actions is not a dictionary")
            for key, actions in spec['actions'].iteritems():
                # verify that each actions entry has a valid state and event
                if not isinstance(key, tuple) or not len(key) == 2:
                    raise StateMachineError("action dictionary contains an invalid (state, event) tuple: %s" % key)
                state, event = key
                if state not in self.states:
                    raise StateMachineError("action dictionary contains an invalid state: %s" % state)
                if event not in self.events:
                    raise StateMachineError("action dictionary contains an invalid event: %s" % event)
                # verify that each actions entry is a list
                if not isinstance(actions, list):
                    raise StateMachineError("entry %s in the action dictionary is not a list of functions: %s" % (key, actions))
                # verify that each entry in the actions list is a function
                for action in actions:
                    if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
                        raise StateMachineError( \
                            "entry %s in the action dictionary has an element that is not a function: %s" % (key, action))
            self._actions = spec['actions']
        else:
            self._actions = {}
        if spec.has_key('terminal_actions'):
            if not isinstance(spec['terminal_actions'], type.list):
                raise StateMachineError("terminal_actions is not a list of functions")
            for action in terminal_actions:
                if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
                    raise StateMachineError("terminal_actions list has an element that is not a function: %s" % action)
            self._terminal_actions = spec['terminal_actions']
        else:
            self._terminal_actions = []
        if spec.has_key('state'):
            self.state = spec['state']

    def add_action(self, state, event, action):
        if state not in self.states:
            raise DataStateError(state)
        if event not in self.events:
            raise StateMachineNonexistentEventError(event)
        if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
            raise StateMachineError("action is not a function: %s" % action)
        if not self._actions.has_key((state, event)):
            self._actions[(state, event)] = []
        self._actions[(state, event)] = self._actions[(state, event)] + [action]

    def add_terminal_action(self, action):
        if not isinstance(action, types.FunctionType) and not isinstance(action, types.MethodType):
            raise StateMachineError("action is not a function: %s" % action)
        self._terminal_actions = self._terminal_actions + [action]

    def trigger_event(self, event, args={}):
        if self._actions.has_key((self.state, event)):
            for action in self._actions[(self.state, event)]:
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

#------------------------------------------------------------------------------

import traceback

def main():
    class TestJobStateMachine (StateMachine):
        StateMachine.states = ['Queued', 'Starting', 'Running', 'Killing'] + StateMachine.states
        StateMachine.transitions = [
            ('Queued', 'Starting'),
            ('Starting', 'Running'),
            ('Starting', 'Terminal'),
            ('Running', 'Terminal'),
            ('Running', 'Killing'),
            ('Killing', 'Terminal'),
            ]
        StateMachine.initial_state = 'Queued'
        StateMachine.events = ['Run', 'Kill', 'JobExit'] + StateMachine.events

        def __init__(self):
            actions = {
                ('Queued', 'Run') : [self.job_init],
                ('Starting', 'Run') : [],
                ('Starting', 'Kill') : [self.kill_starting],
                ('Starting', 'Progress') : [self.job_run],
                ('Running', 'Kill') : [self.kill_running],
                ('Running', 'JobExit') : [self.job_finished],
                ('Killing', 'Kill') : [],
                ('Killing', 'JobExit') : [self.job_finished],
                }
            StateMachine.__init__(self, {'actions' : actions, 'state' : 'Queued'})

        def job_init(self, event, args):
            print "%s.%s: state=%s, event=%s, args=%s" % \
                (self.__class__.__name__, traceback.extract_stack()[-1][2], self.state, event, args)
            self.state = 'Starting'

        def job_run(self, event, args):
            print "%s.%s: state=%s, event=%s" % (self.__class__.__name__, traceback.extract_stack()[-1][2], self.state, event)
            self.state = 'Running'

        def job_finished(self, event, args):
            print "%s.%s: state=%s, event=%s" % (self.__class__.__name__, traceback.extract_stack()[-1][2], self.state, event)
            self.state = 'Terminal'

        def kill_starting(self, event, args):
            print "%s.%s: state=%s, event=%s" % (self.__class__.__name__, traceback.extract_stack()[-1][2], self.state, event)
            self.state = 'Terminal'

        def kill_running(self, event, args):
            print "%s.%s: state=%s, event=%s" % (self.__class__.__name__, traceback.extract_stack()[-1][2], self.state, event)
            self.state = 'Killing'

    def cleanup_job():
        print "%s: state=%s" % (traceback.extract_stack()[-1][2], tjsm.state)
        print ""

    tjsm = TestJobStateMachine()
    tjsm.add_terminal_action(cleanup_job)
    tjsm.trigger_event('Run', {'p1' : "bar", 'p2' : "baz"})
    tjsm.trigger_event('Progress')
    tjsm.trigger_event('JobExit')
    tjsm.trigger_event('Progress')

    tjsm = TestJobStateMachine()
    tjsm.add_terminal_action(cleanup_job)
    tjsm.trigger_event('Run')
    tjsm.trigger_event('Progress')
    tjsm.trigger_event('Kill')
    tjsm.trigger_event('Kill')
    tjsm.trigger_event('JobExit')

    tjsm = TestJobStateMachine()
    tjsm.add_terminal_action(cleanup_job)
    tjsm.trigger_event('Run')
    tjsm.trigger_event('Kill')

    try:
        tjsm = TestJobStateMachine()
        tjsm.add_terminal_action(cleanup_job)
        tjsm.trigger_event('Kill')
    except StateMachineIllegalEventError, e:
        print "Correctly caught illegal event:", e
        print ""

    def double_run(event, args):
        print "%s: state=%s, event=%s" % (traceback.extract_stack()[-1][2], tjsm.state, event)

    tjsm = TestJobStateMachine()
    tjsm.add_action('Running', 'Run', double_run)
    tjsm.add_terminal_action(cleanup_job)
    tjsm.trigger_event('Run')
    tjsm.trigger_event('Progress')
    tjsm.trigger_event('Run')
    tjsm.trigger_event('JobExit')


if __name__ == '__main__':
    main()
