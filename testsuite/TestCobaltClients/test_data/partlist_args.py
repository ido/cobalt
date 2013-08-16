"""
This module defines the test argument information list for partlist.py and will 
dynamically be imported by testutils.py to generate the tests for partlist.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "version_option_1", "args" : """--version""", "new_only" : True, },
    { "tc_name" : "version_option_2", "args" : """-v""", "new_only" : True, },
    { "tc_name" : "debug", "args" : """-d""", "new_only" : True,},
    { "tc_name" : "help_option_1", "args" : """-h""", "new_only" : True,},
    { "tc_name" : "help_option_1", "args" : """--help""", "new_only" : True,},
    { "tc_name" : "invalid", "args" : """-k""", "new_only" : True,},
    { "tc_name" : "argument_1", "args" : """arg""", "new_only" : True,},
    { "tc_name" : "argument_2", "args" : "", },
    ]
