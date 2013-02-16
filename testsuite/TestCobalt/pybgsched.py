'''Mockup of the BlueGene/Q scheduing interface for unit-testing purposes.

'''

class BlockFilter(object):

    def __init__(self):
        self.name = None
        self.extended_info=None

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

def getBlocks(bf):
    return [block_dict[bf.name]]


class Action(object):
    _None = 0
    Free = 1
    Boot = 2

block_dict = {}

class Block(object):

    Free = 0
    Allocated = 1
    Booting = 2
    Initialized = 3
    Terminating = 4

    error = None

    def __init__(self, name, size):

        self.name = name
        self.size = size
        self.error = None
        self.users = []
        self.action = Action._None
        block_dict[name] = self
        self.statuses = [self.Free]

    @classmethod
    def set_error(cls, error_message):
        cls.error = error_message

    @classmethod
    def raise_error(cls):
        if cls.error != None:
            msg = cls.error
            cls.error = None
            raise RuntimeError, msg

    def set_status(self, status):
        self.statuses = [status]

    def add_status(self, status):
        self.statuses.append(status)

    def set_action(self, action):
        self.action = action

    @classmethod
    def addUser(cls,block_name, string):
        b = block_dict[block_name]
        b.raise_error()
        b.users.append(string)

    def removeUser(self, string):
        self.raise_error()
        self.users.remove(string)

    @classmethod
    def initiateBoot(cls, loc):
        return

    def getStatus(self):
        self.raise_error()
        if len(self.statuses) > 1:
            status = self.statuses.pop()
            return status
        else:
            return self.statuses[0]

    def getAction(self):
        self.raise_error()
        return self.action
