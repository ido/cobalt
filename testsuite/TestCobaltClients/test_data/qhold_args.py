"""
This module defines the test argument information list for qhold.py and will 
dynamically be imported by testutils.py to generate the tests for qhold.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "invalid_option", "args" : """-k 1""", 'new_only' : True, },
    { "tc_name" : "debg_option", "args" : """-d 1""", "old_args" : """1""", },
    { "tc_name" : "jobid_1", "args" : """myq 1 2 3 4""", },
    { "tc_name" : "jobid_2", "args" : """1 2 3 4""", },
    { "tc_name" : "jobid_3", "args" : """1""", },
    ]
