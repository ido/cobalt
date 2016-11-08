"""
This module defines the test argument information list for nodeadm.py and will 
dynamically be imported by testutils.py to generate the tests for nodeadm.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "args_1", "args" : "", 'new_only' : True },
    { "tc_name" : "args_2", "args" : """p1""", "new_only" : True, },
    { "tc_name" : "combo_1", "args" : """--up --down p1""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "combo_2", "args" : """--up -l p1""", "new_only" : True,'skip_list' : ['not_bsim'], },
    { "tc_name" : "combo_3", "args" : """--list_nstates --queue q1 p1""", "new_only" : True,'skip_list' : ['not_bsim'], },
    { "tc_name" : "combo_4", "args" : """--up --queue q1 p1""", "new_only" : True,'skip_list' : ['not_bsim'], },
    { "tc_name" : "combo_5", "args" : """--down --list_nstates p1""", "new_only" : True,'skip_list' : ['not_bsim'], },
    { "tc_name" : "up_1", "args" : """--up p1 p2 p3""",  "new_only" : True,},
    { "tc_name" : "up_2", "args" : """--up U1 U2 U5 p1""",  "new_only" : True,},
    { "tc_name" : "down_1", "args" : """--down p1 p2 p3""", "new_only" : True,},
    { "tc_name" : "down_2", "args" : """-d --down p1 p2 p3""", "new_only" : True,},
    { "tc_name" : "down_3", "args" : """--down D1 D2 D5 p1""", "new_only" : True, },
    { "tc_name" : "list_1", "args" : """-l""", "new_only": True, "new_only" : True,},
    { "tc_name" : "list_2", "args" : """-l p1""", "new_only": True},
    { "tc_name" : "list_details_1", "args": """-b""", "new_only": True},
    { "tc_name" : "list_details_2", "args": """-b D1""", "new_only": True},
    { "tc_name" : "queue_1", "args" : """--queue QU1""", "new_only" : True, },
    { "tc_name" : "queue_2", "args" : """--queue "QU1 QD1" U1 D1 P1""", "new_only" : True, },
    ]
