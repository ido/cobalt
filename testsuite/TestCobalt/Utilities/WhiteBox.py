# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
'''white box testing tools'''

__revision__ = '$Revision:$'

__all__ = ["WHITEBOX_TESTING", "whitebox"]

WHITEBOX_TESTING = False

from nose.tools import make_decorator

def whitebox(func):
    """the test should only be included if white box testing is enabled"""
    if not WHITEBOX_TESTING:
        func.__test__ = False
    return func
