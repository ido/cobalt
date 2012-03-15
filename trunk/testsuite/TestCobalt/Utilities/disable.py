'''Decorator for disabling tests'''

__revision__ = '$Revision:$'


from nose.tools import make_decorator

def disabled(func):
    '''Mark a test as being intentionally disabled

    '''
    func.__test__ = False

    return func
