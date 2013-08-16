"""
This module defines the test argument information list for qmove.py and will 
dynamically be imported by testutils.py to generate the tests for qmove.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "invalid_option", "args" : """-k""", 'new_only' : True, },
    { "tc_name" : "queue_1", "args" : """myq 1 2 3""", },
    { "tc_name" : "queue_2", "args" : """-d myq 1 2 3""", "new_only" : True, },
    { "tc_name" : "queue_3", "args" : """1 2 3 4""", "skip_list" : ['not_bsim'], },
    { "tc_name" : "queu_4", "args" : """q1 q2 1 2 3""", },
    ]
