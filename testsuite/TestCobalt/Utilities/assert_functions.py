# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""Helper and convenience functions for common assert cases"""


def assert_match(test, expect, desc, comp=None):
    '''Assert that we have a match, log failure in convenient way otherwise.
        comp should correspond to a boolean __eq__ function, if None, will
        use default == comparitor.
    '''
    if comp is None:
        comp = lambda a, b: a == b
    assert comp(test, expect), "FAILED MATCH: %s: Expected: %s; Got %s" % (desc, str(expect), str(test))

def assert_not_match(test, expect, desc, comp=None):
    '''Assert non-matching test and expected result.  Default comparitor
    corresponds to __ne__ function.  By default will use !=.

    '''
    if comp is None:
        comp = lambda a, b: a != b

    assert comp(test, expect), "FAILED NON-MATCH: %s: Got %s for both" % (desc,
            str(test))
