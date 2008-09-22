from Cobalt.StateMachine import StateMachine
from Cobalt.Exceptions import DataStateError, DataStateTransitionError, StateMachineError, StateMachineIllegalEventError, \
    StateMachineNonexistentEventError
import traceback

class TestStateMachine (object):

    def test_init(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                seas = {('Waiting', 'Start') : [self.start1, self.start2], ('Active', 'Stop') : [self.stop]}
                ta = [self.terminate1, self.terminate2]
                StateMachine.__init__(self, {}, seas = seas, terminal_actions = ta)

            def start1(self, event, args):
                pass

            def start2(self, event, args):
                pass
    
            def stop(self, event, args):
                pass

            def terminate1(self):
                pass

            def terminate2(self):
                pass

        tsm = TSM()

    def test_init_terminal_state_missing(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active']
            transitions = [('Waiting', 'Active')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_initial_state_missing(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            # initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_initial_state_bad(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'BadState'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_not_dict(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = 1)

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_key_not_tuple(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {1 : []})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_key_not_2tuple(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {(1, 2, 3) : []})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_key_bad_state(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {('BadState', 'Start') : []})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_key_bad_event(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {('Waiting', 'BadEvent') : []})

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_actions_not_list(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {('Waiting', 'Start') : self.start1})

            def start1(self, event, args):
                pass

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_action_not_method(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            not_method = 1

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {('Waiting', 'Start') : [self.start1, self.not_method]})

            def start1(self, event, args):
                pass

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_seas_action_is_func(self):
        def extern_start_func():
            pass

        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, seas = {('Waiting', 'Start') : [self.start1, extern_start_func]})

            def start1(self, event, args):
                pass

        tsm = TSM()

    def test_init_terminal_actions_not_list(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {}, terminal_actions = self.terminate1)

            def terminate1(self):
                pass

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_init_terminal_action_not_method(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            not_method = 1

            def __init__(self):
                StateMachine.__init__(self, {}, terminal_actions = [self.terminate1, self.not_method])

            def terminate1(self):
                pass

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_add_action(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_action('Waiting', 'Start', self.start1)

            def start1(self, event, args):
                pass

        tsm = TSM()

    def test_add_action_is_func(self):
        def extern_start_func():
            pass

        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_action('Waiting', 'Start', extern_start_func)

        tsm = TSM()

    def test_add_action_bad_state(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_action('BadState', 'Start', self.start1)

            def start1(self, event, args):
                pass

        try:
            tsm = TSM()
            assert False
        except DataStateError:
            pass

    def test_add_action_bad_event(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_action('Waiting', 'BadEvent', self.start1)

            def start1(self, event, args):
                pass

        try:
            tsm = TSM()
            assert False
        except StateMachineNonexistentEventError:
            pass

    def test_add_action_not_method(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            not_method = 1

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_action('Waiting', 'Start', self.not_method)

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_add_terminal_action(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_terminal_action(self.terminate1)

            def terminate1(self):
                pass

        tsm = TSM()

    def test_add_terminal_action_is_func(self):
        def extern_terminate_func():
            pass

        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_terminal_action(extern_terminate_func)

        tsm = TSM()

    def test_add_terminal_action_not_method(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            not_method = 1

            def __init__(self):
                StateMachine.__init__(self, {})
                self.add_terminal_action(self.not_method)

        try:
            tsm = TSM()
            assert False
        except StateMachineError:
            pass

    def test_trigger_nonexistent_event(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                seas = {('Waiting', 'Progress') : []}
                StateMachine.__init__(self, {}, seas = seas)

        tsm = TSM()
        try:
            tsm.trigger_event('BadEvent')
        except StateMachineNonexistentEventError:
            pass

    def test_trigger_illegal_event(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                seas = {('Waiting', 'Start') : []}
                StateMachine.__init__(self, {}, seas = seas)

        tsm = TSM()
        try:
            tsm.trigger_event('Stop')
        except StateMachineIllegalEventError:
            pass

    def test_trigger_args(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                seas = {('Waiting', 'Start') : [self.start]}
                StateMachine.__init__(self, {}, seas = seas)

            def start(self, event, args):
                assert args == {'foo' : "bar", 'baz' : "bif"}, "args = %s" % args

        tsm = TSM()
        tsm.trigger_event('Start', {'foo' : "bar", 'baz' : "bif"})

    def test_run(self):
        class TSM (StateMachine):
            states = ['Waiting', 'Active'] + StateMachine.states
            transitions = [('Waiting', 'Active'), ('Active', 'Terminal')]
            initial_state = 'Waiting'
            events = ['Start', 'Stop'] + StateMachine.events

            def __init__(self):
                seas = {
                    ('Waiting', 'Start') : [self.start1, self.start2],
                    ('Active', 'Progress') : [self.progress],
                    ('Active', 'Stop') : [self.stop],
                    }
                ta = [self.terminate1, self.terminate2]
                StateMachine.__init__(self, {}, seas = seas, terminal_actions = ta)
                self.actions = []

            def start1(self, event, args):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]

            def start2(self, event, args):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]
                self.state = 'Active'
    
            def progress(self, event, args):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]

            def stop(self, event, args):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]
                self.state = 'Terminal'

            def terminate1(self):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]

            def terminate2(self):
                self.actions = self.actions + [traceback.extract_stack()[-1][2]]

        tsm = TSM()
        assert tsm.state == 'Waiting', 'state = %s' % tsm.state

        tsm.actions = []
        tsm.trigger_event('Progress')
        assert tsm.actions == [], "actions run = %s" % tsm.actions
        assert tsm.state == 'Waiting', 'state = %s' % tsm.state

        tsm.actions = []
        tsm.trigger_event('Start')
        assert tsm.actions == ['start1', 'start2'], "actions run = %s" % tsm.actions
        assert tsm.state == 'Active', 'state = %s' % tsm.state

        tsm.actions = []
        tsm.trigger_event('Progress')
        assert tsm.actions == ['progress'], "actions run = %s" % tsm.actions
        assert tsm.state == 'Active', 'state = %s' % tsm.state

        tsm.actions = []
        tsm.trigger_event('Stop')
        assert tsm.actions == ['stop', 'terminate1', 'terminate2'], "actions run = %s" % tsm.actions
        assert tsm.state == 'Terminal', 'state = %s' % tsm.state
