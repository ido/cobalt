"""
This module defines the test argument information list for qalter.py and will 
dynamically be imported by testutils.py to generate the tests for qalter.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "simple_1", "args" : """-d -n30""", 'new_only' : True, },
    { "tc_name" : "simple_2", "args" : """-d -n30 1""", "new_only" : True, }, 
    { "tc_name" : "simple_3", "args" : """-n30 1""", "new_only" : True, }, 
    { "tc_name" : "time_1", "args" : """-v n10 -t5 1 2 3""", 'new_only' : True, },
    { "tc_name" : "time_2", "args" : """-v -n10 -t+5 1 2 3""", "new_only" : True,},
    { "tc_name" : "time_3", "args" : """-v -n10 -t+20 1 2 3 4 5 6 7""", "new_only" : True, 'skip_list' : ['not_bsim'], },
    { "tc_name" : "time_4", "args" : """-v -n10 -t30 1 2 3 4 5 6 7 10 15""", "new_only" : True, 'skip_list' : ['not_bsim'], },
    { "tc_name" : "time_5", "args" : """-v -n10 -t00:00:30 1 2 3""", "new_only" : True, },
    { "tc_name" : "time_6", "args" : """-v -n10 -t+00:00:30 1 2 3""", "new_only" : True, },
    { "tc_name" : "time_7", "args" : """-v -n10 -t 00:00:30 1 2 3""", "new_only" : True, },
    { "tc_name" : "time_8", "args" : """-v -n10 -t +00:00:30 1 2 3""", "new_only" : True, },
    { "tc_name" : "invalid_option", "args" : """-v -m j@gmail.com""", 'new_only' : True, },
    { "tc_name" : "email_option", "args" : """-v -M j@gmail.com 1 2""", "new_only" : True, },
    { "tc_name" : "mode_1", "args" : """-v --mode jjj  -n40 -t50 -e p -o o 1 2 3""", },
    { "tc_name" : "mode_2", "args" : """-v --mode dual -n40 -t50 -e p -o o 1 2 3""", "new_only" : True, },
    { "tc_name" : "proccount_1", "args" : """-v --mode dual -n512 --proccount one -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10""", },
    { "tc_name" : "proccount_2", "args" : """-v --mode dual -n512 --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10""", "new_only" : True, },
    { "tc_name" : "invalid_nodecount", "args" : """-v --mode dual -nfiver --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10""", },
    { "tc_name" : "user_1", "args" : """-v --run_users user1:user2:user3 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "user_2", "args" : """-v --run_users user1:naughtyuser 1 2 3 4 5""", },
    { "tc_name" : "user_3", "args" : """-v --run_users user1:root 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, "testhook" : "JOB_RUNNING", },
    { "tc_name" : "project", "args" : """-v --run_project 10 20 30""", "new_only" : True, },
    { "tc_name" : "geometry_1", "args" : """-v --geometry 10 1 2 3 4 5""", 'new_only': True, },
    { "tc_name" : "geometry_2", "args" : """-v --geometry 10x10x10x10x10 1 2 3 4 5""", 'new_only' : True, },
    { "tc_name" : "geometry_3", "args" : """-v --geometry 04x04x04x04    1 2 3 4""", "new_only" : True, 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_4", "args" : """-v --geometry 10x10x10x10x1  1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "geometry_5", "args" : """-v --geometry 04x04x04x04x2  1 2 3 4""", "new_only" : True, 'skip_list' : ['not_bsim'], },
    { "tc_name" : "preboot_1", "args" : """-v --enable_preboot --run_project 10 20 30""", "new_only" : True, },
    { "tc_name" : "preboot_2", "args" : """-v --disable_preboot --run_project 10 20 30""", "new_only" : True,  },
    { "tc_name" : "defer_1", "args" : """--defer""", "new_only": True, },
    { "tc_name" : "defer_2", "args" : """--defer 1 2 3 4 5""", "new_only": True, 'skip_list' : ['not_bsim'], },
    ]
