"""
This module defines the test argument information list for showres.py and will 
dynamically be imported by testutils.py to generate the tests for showres.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "arg_1", "args" : "", 'new_only' : True, },
    { "tc_name" : "arg_2", "args" : """--oldts""", 'new_only' : True, },
    { "tc_name" : "arg_3", "args" : """arg1""", 'new_only' : True, },
    { "tc_name" : "l_option_1", "args" : """-l""", 'new_only' : True, },
    { "tc_name" : "l_option_2", "args" : """-l --oldts""", 'new_only' : True, },
    { "tc_name" : "x_option_1", "args" : """-x""", 'new_only' : True, },
    { "tc_name" : "x_option_2", "args" : """-x --oldts""", 'new_only' : True, },
    { "tc_name" : "combo", "args" : """-l -x""", "new_only" : True,},
    { "tc_name" : "help_1", "args" : """--help""", "new_only" : True,},
    { "tc_name" : "help_2", "args" : """-h""", "new_only" : True,},
    { "tc_name" : "version", "args" : """--version""", "new_only" : True,},
    { "tc_name" : "debug", "args" : """--debug""", "new_only" : True,},
    ]
