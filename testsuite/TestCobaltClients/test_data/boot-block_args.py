"""
This module defines the test argument information list for boot-block.py and will 
dynamically be imported by testutils.py to generate the tests for boot-block.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "combo", "args" : """--free --reboot --block b --jobid 1""", },
    { "tc_name" : "free_1", "args" : """--free""", },
    { "tc_name" : "free_2", "args" : """--free --jobid 1""", },
    { "tc_name" : "free_3", "args" : """--free --jobid 1 --block b""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "reboot_1", "args" : """--reboot""", },
    { "tc_name" : "reboot_2", "args" : """--reboot --jobid 1""", },
    { "tc_name" : "reboot_3", "args" : """--reboot --jobid 1 --block b""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "nofree_noreboot_1", "args" : """--jobid 1""", },
    { "tc_name" : "nofree_noreboot_2", "args" : """--block b""", },
    { "tc_name" : "nofree_noreboot_3", "args" : """--jobid 1 --block b""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "help_1", "args" : """--help""", "new_only" : True, },
    { "tc_name" : "help_2", "args" : """-h""", "new_only" : True, },
    { "tc_name" : "version", "args" : """--version""", "new_only" : True, },
    { "tc_name" : "debug_1", "args" : """--debug""", "new_only" : True,},
    { "tc_name" : "debug_2", "args" : """--d""", "new_only" : True,},
    ]
