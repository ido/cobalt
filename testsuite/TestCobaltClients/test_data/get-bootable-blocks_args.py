"""
This module defines the test argument information list for get-bootable-blocks.py and will 
dynamically be imported by testutils.py to generate the tests for get-bootable-blocks.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "arg_1", "args" : "", 'new_only' : True, },
    { "tc_name" : "arg_2", "args" : """arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "size_1", "args" : """--size 1024""", 'new_only' : True, },
    { "tc_name" : "size_2", "args" : """--size 1024 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_1", "args" : """--geometry 1              arg""", },
    { "tc_name" : "geometry_2", "args" : """--geometry geo            arg""", },
    { "tc_name" : "geometry_3", "args" : """--geometry 90x90x90x90x90 arg""", },
    { "tc_name" : "geometry_4", "args" : """--geometry 90x90x90x90    arg""", },
    { "tc_name" : "geometry_5", "args" : """--geometry -9x90x90x90x2  arg""", },
    { "tc_name" : "geometry_6", "args" : """--geometry 9x10x11x12x2   arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_7", "args" : """--geometry 90x90x90x90x1  arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_8", "args" : """--geometry 90x90x90x90x2  arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_9", "args" : """--geometry 90x90x90x90x3  arg""", },
    { "tc_name" : "geometry_10", "args" : """--geometry 90x90x90x90x11 arg""", },
    { "tc_name" : "geometry_11", "args" : """--geometry 99x99x99x99x2  arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_12", "args" : """--geometry 00x00x00x00x2  arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_13", "args" : """--geometry 100x00x00x00x2 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_14", "args" : """--geometry 00x100x00x00x2 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_15", "args" : """--geometry 00x00x100x00x2 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "geometry_16", "args" : """--geometry 00x00x00x100x2 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "combo", "args" : """--geometry 00x00x00x00x2 --size 2048 arg""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "help_1", "args" : """--help""", "new_only" : True, },
    { "tc_name" : "help_2", "args" : """-h""", "new_only" : True, },
    { "tc_name" : "version", "args" : """--version""", "new_only" : True, },
    { "tc_name" : "debug", "args" : """--debug""", "new_only" : True,},
    ]
