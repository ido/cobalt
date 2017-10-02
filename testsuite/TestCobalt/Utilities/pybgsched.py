'''Mockup of the BlueGene/Q scheduing interface for unit-testing purposes.
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

'''

class BlockFilter(object):

    def __init__(self):
        self.name = None
        self.extended_info=None

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

class IOBlockFilter(BlockFilter):

    def __init__(self):
        self.name = None
        self.extended_info=None

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

def getBlocks(bf):
    block_dict[bf.name].raise_error()
    return [block_dict[bf.name]]

def getIOBlocks(bf):
    io_block_dict[bf.name].raise_error()
    return [io_block_dict[bf.name]]

class Action(object):
    _None = 0
    Free = 1
    Boot = 2

block_dict = {}
io_block_dict = {}


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
        self.boot_options = ''

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

    def getBootOptions(self):
        self.raise_error()
        return self.boot_options

    def setBootOptions(self, val):
        self.boot_options = val

    def update(self):
        self.raise_error()

class IOBlock(Block):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.error = None
        self.users = []
        self.action = Action._None
        io_block_dict[name] = self
        self.statuses = [self.Free]
        self.boot_options = ''

    @classmethod
    def initiateBoot(cls, location, allow_holes, uninit1, uninit2):
        return

    def getBootOptions(self):
        self.raise_error()
        return self.boot_options

    def setBootOptions(self, val):
        self.boot_options = val

    def update(self):
        self.raise_error()

class StringVector(object):

    def size(self):
        return 0
