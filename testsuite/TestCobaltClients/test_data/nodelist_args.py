"""
This module defines the test argument information list for nodelist.py and will 
dynamically be imported by testutils.py to generate the tests for nodelist.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "arg_1", "args" : "", },
    { "tc_name" : "arg_2", "args" : """arg1""", },
    { "tc_name" : "debug", "args" : """-d""", },
    { "tc_name" : "options_1", "args" : """-l""",},
    { "tc_name" : "options_2", "args" : """--help""",},
    { "tc_name" : "options_3", "args" : """-h""",},
    { "tc_name" : "options_4", "args" : """--version""",},
    ]
