"""
This module defines the test argument information list for qrls.py and will 
dynamically be imported by testutils.py to generate the tests for qrls.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "invalid_option", "args" : """-k 1""", },
    { "tc_name" : "debug_flag", "args" : """-d 1""", },
    { "tc_name" : "jobid_1", "args" : """myq 1 2 3 4""", },
    { "tc_name" : "jobid_2", "args" : """1 2 3 4""", },
    { "tc_name" : "jobid_3", "args" : """1""", },
    { "tc_name" : "dependancy_option", "args" : """-d --dependencies 1 2""", },
    ]
