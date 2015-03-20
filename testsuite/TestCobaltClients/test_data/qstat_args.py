"""
This module defines the test argument information list for qstat.py and will 
dynamically be imported by testutils.py to generate the tests for qstat.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "version_option", "args" : """--version""", "new_only" : True, },
    { "tc_name" : "help_option", "args" : """-h""", "new_only" : True, },
    { "tc_name" : "debug_only", "args" : """-d""", "new_only" : True, },
    { "tc_name" : "full_option_1", "args" : """-d -f 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_2", "args" : """-f 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_3", "args" : """-f --reverse 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_4", "args" : """-f -l 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_5", "args" : """-f -l --reverse 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_6", "args" : """-f -l --sort user 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_7", "args" : """-f -l --reverse --sort user 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_8", "args" : """-f -l --sort queue 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_9", "args" : """-f -l --reverse --sort queue 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "full_option_10", "args" : """-f""", "new_only" : True, },
    { "tc_name" : "full_option_11", "args" : """-f --header Jobid:State:RunTime  1 2 3""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_1", "args" : """-l""", "new_only" : True, },
    { "tc_name" : "long_option_2", "args" : """-l 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_3", "args" : """-l --reverse 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_4", "args" : """-l --sort user 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_5", "args" : """-l --reverse --sort user 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_6", "args" : """-l --sort queue 1 2 3 4 5""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "long_option_11", "args" : """-l --header Jobid:State:RunTime  1 2 3""", 'skip_list' : ['not_bsim'], "new_only" : True, },
    { "tc_name" : "queue_option_1", "args" : """-f -Q -l 1 2 3""", 'skip_list' : ['not_bsim'], "new_only" : True,},
    { "tc_name" : "queue_option_2", "args" : """-f --reverse -Q -l 1 2 3""", 'skip_list' : ['not_bsim'], "new_only" : True,},
    { "tc_name" : "queue_option_3", "args" : """-f --sort users -Q""", "new_only" : True,},
    { "tc_name" : "queue_option_4", "args" : """-Q""", "new_only" : True,},
    { "tc_name" : "queue_option_5", "args" : """-Q --reverse""", "new_only" : True,},
    { "tc_name" : "queue_option_6", "args" : """-Q --sort users""", "new_only" : True,},
    { "tc_name" : "queue_option_7", "args" : """-Q --sort users --reverse""", "new_only" : True,},
    { "tc_name" : "queue_option_8", "args" : """-Q -l""", "new_only" : True,},
    { "tc_name" : "queue_option_9", "args" : """-Q --reverse -l""", "new_only" : True,},
    { "tc_name" : "queue_option_10", "args" : """-Q --sort users -l""", "new_only" : True,},
    { "tc_name" : "queue_option_11", "args" : """-Q --sort users --reverse -l""", "new_only" : True,},
    { "tc_name" : "queue_option_12", "args" : """-Q --header Jobid:State:RunTime""", "new_only" : True,},
    { "tc_name" : "no_arguments_or_options", "args" : "", "new_only" : True, },
    ]
