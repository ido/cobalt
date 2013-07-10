"""
This module defines the test argument information list for releaseres.py and will 
dynamically be imported by testutils.py to generate the tests for showres.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "arg_1", "args" : "", 'new_only' : True, },
    { "tc_name" : "arg_2", "args" : """-p p1""",},
    { "tc_name" : "arg_2", "args" : """s1""",},
    { "tc_name" : "arg_3", "args" : """s1 s2 s3""",},
    { "tc_name" : "arg_4", "args" : """s1 s2 s3""", "testhook" : "NO CYCLE"},
    { "tc_name" : "arg_5", "args" : """s1""", "new_only" : True, "testhook" : "BOGUS USER" },
    { "tc_name" : "arg_6", "args" : """s1 s2 s3""", "new_only" : True, },
    { "tc_name" : "arg_7", "args" : """s1 s2 s3 s4""", "new_only" : True, },
    { "tc_name" : "arg_8", "args" : """-d p1 s1 s2 s3""", "new_only" : True, },
    { "tc_name" : "arg_9", "args" : """--debug p1 s1 s2 s3""", "new_only" : True, },
    { "tc_name" : "help_1", "args" : """--help""", "new_only" : True, },
    { "tc_name" : "help_2", "args" : """-h""", "new_only" : True, },
    { "tc_name" : "version", "args" : """--version""", "new_only" : True, },
    ]
