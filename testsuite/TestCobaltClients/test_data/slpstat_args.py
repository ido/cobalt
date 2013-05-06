"""
This module defines the test argument information list for slpstat.py and will 
dynamically be imported by testutils.py to generate the tests for slpstat.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "arg_1", "args" : "", },
    { "tc_name" : "arg_2", "args" : "", "testhook" : "NO SERVICES",},
    { "tc_name" : "arg_3", "args" : """arg1""", },
    { "tc_name" : "debug_1", "args" : """-d""", },
    { "tc_name" : "debug_2", "args" : """-d""", "testhook" : "NO SERVICES",},
    { "tc_name" : "help_1", "args" : """--help""", "new_only" : True,},
    { "tc_name" : "help_2", "args" : """-h""", "new_only" : True,},
    { "tc_name" : "version", "args" : """--version""", "new_only" : True,},
    ]
