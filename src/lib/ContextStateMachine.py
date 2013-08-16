import Cobalt.TriremeStateMachine

class ContextStateMachine(object):
    '''Instance of Trireme State Machine usning contexts and state objects.

        _state_list = list of state classes to register with the machine.
        context =  External information for the object needed by the states to perform their transitions
        initialstate = when a new statemachine instantiated, the starting state of the machine
        exceptionstate = in the event of an exception or error, which state to default to

    '''

    _state_list = []
    _state_instances = []

    def __init__(self, context, initialstate, exceptionstate):
        self.context = context
        self.__statemachine = Cobalt.TriremeStateMachine.StateMachineProcessor()
        self.initialize_state_machine(context, initialstate, exceptionstate)

    def initialize_state_machine(self, context, initialstate, exceptionstate):

        for state in self._state_list:
            state_instance = state(self.context)
            self._state_instances.append(state_instance)
            self.__statemachine.add_transition(str(state_instance), state_instance.progress, state_instance.get_valid_transition_dict())
        self.__statemachine.set_initialstate(initialstate)
        self.__statemachine.set_exceptionstate(exceptionstate)
        self.__statemachine.initialize()
        self.__statemachine.start()

    @property
    def state(self):
        '''current state of statemachine'''
        return self.__statemachine.get_state()

    def get_details(self):
        return {}

    def __str__(self):
        return str(self.get_details())

    def progress(self):
        self.__statemachine.process()

