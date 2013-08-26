"""
This module defines the test argument information list for qselect.py and will 
dynamically be imported by testutils.py to generate the tests for qselect.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "invalid_option", "args" : """-k""", 'new_only' : True, },
    { "tc_name" : "only_arg", "args" : """1""", "new_only" : True, },
    { "tc_name" : "no_args_opts", "args" : "", "old_args" : """-d""", },
    { "tc_name" : "debug_flag", "args" : """-d""", },
    { "tc_name" : "held_option", "args" : """-h user_hold""", },
    { "tc_name" : "nodecount_option", "args" : """-n 312""", },
    { "tc_name" : "state_and_nodecount", "args" : """-n 312 -h user_hold""", },
    { "tc_name" : "walltime", "args" : """-t 10:10:10""", },
    { "tc_name" : "mode", "args" : """--mode vn""", },
    { "tc_name" : "verbose", "args" : """-v""", },
    ]
