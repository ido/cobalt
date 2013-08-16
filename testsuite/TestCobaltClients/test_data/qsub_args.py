"""
This module defines the test argument information list for qsub.py and will 
dynamically be imported by testutils.py to generate the tests for qsub.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "all_options_1", "args" : """-v -A myproj --attrs=a=1:b=2 --cwd /tmp -d --debuglog=/tmp/d --dependencies=1:2:3 -e /tmp/e --env v1=1:v2=2 --geometry 198x198x198x198 -h -i /bin/ls -M myemal@gmail.com -n10 -o /tmp/o -O /tmp --proccount 10 -qqueue --run_users user1:user2:user3 --run_project -t 10 --mode smp --kernel kernel -K kopts /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True, 'new_only' : True },
    { "tc_name" : "misc_1", "args" : """--mode c1 -n 512 --env BG_COREDUMPDISABLED=1 --proccount 512 -t 30 -q testing /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "no_options_passed", "args" : """/bin/ls""", 'new_only' : True, },
    { "tc_name" : "non_existant_option", "args" : """-z -t10 -n10 /bin/ls""", 'new_only' : True, },
    { "tc_name" : "debug_flag_only_1", "args" : """-d""", 'new_only' : True, },
    { "tc_name" : "debug_flag_only_2", "args" : """-debug""", "new_only" : True, },
    { "tc_name" : "verbose_flag_only", "args" : """-v""", 'new_only' : True, },
    { "tc_name" : "non_integer_nodecount", "args" : """--mode smp -t50 -nfive --geometry 40x40x50x50   /bin/ls""", "old_args" : "", },
    { "tc_name" : "non_realistic_nodecount", "args" : """--mode smp -t50 -n2048 --geometry 40x40x50x50x1 /bin/ls""", "old_args" : "", },
    { "tc_name" : "invalid_geometry_1", "args" : """--mode smp -t50 -n10 --geometry x /bin/ls""", },
    { "tc_name" : "invalid_geometry_2", "args" : """--mode smp -t50 -n10 --geometry 1x2x3x4 /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "invalid_geometry_3", "args" : """--mode smp -t50 -n10 --geometry 1x2x3x4 /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "invalid_geometry_4", "args" : """--mode smp -t50 -n10 --geometry 48x48x48x48x2  /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "invalid_geometry_5", "args" : """--mode smp -t50 -n10 --geometry 48x48x48x48x3  /bin/ls""", 'skip_list' : ['not_bsim'], },
    { "tc_name" : "invalid_geometry_6", "args" : """--mode smp -t50 -n10 --geometry 128x64x32x4    /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "no_roject_specified", "args" : """-A -t50 -n10 /bin/ls""", },
    { "tc_name" : "project_specified", "args" : """-A who -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "Check_attrs_1", "args" : """--attrs xxxx -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "Check_attrs_2", "args" : """--attrs 1111 -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "Check_attrs_3", "args" : """--attrs xx=:yy -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "Check_attrs_4", "args" : """--attrs xx=one:yy=1:zz=1one -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "cwd_option_1", "args" : """--cwd /tmp/ -t10 -n 10 -e p /bin/ls""", 'new_only' : True },
    { "tc_name" : "cwd_option_2", "args" : """--cwd /tmp -t10 -n 10 -e p /bin/ls""", 'new_only' : True },
    { "tc_name" : "cwd_option_3", "args" : """--cwd /x -t10 -n 10 -e p /bin/ls""", },
    { "tc_name" : "cwd_option_4", "args" : """--cwd /tmp/ -t10 -n 10 -e p -o x /bin/ls""", 'new_only' : True },
    { "tc_name" : "cwd_option_5", "args" : """--cwd /tmp -t10 -n 10 -e p -o x /bin/ls""", 'new_only' : True },
    { "tc_name" : "debuglog_option", "args" : """-t10 -n 10 -e p -o x --debuglog y /bin/ls""", 'new_only' : True },
    { "tc_name" : "inputfile_option_1", "args" : """-i none -t10 -n 10 /bin/ls""", },
    { "tc_name" : "inputfile_option_2", "args" : """-i y -t10 -n 10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "email_option", "args" : """-M g -t10 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "outputprefix", "args" : """-O /tmp -t10 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "invalid_user", "args" : """--run_users naughtyuser -t10 -n10 /bin/ls""", },
    { "tc_name" : "mode_option_1", "args" : """-t10 -n512 --proccount 1023 --mode dual /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "mode_option_2", "args" : """-t10 -n512 --proccount 1023 --mode vn /bin/ls""", 'new_only' : True },
    { "tc_name" : "mode_option_3", "args" : """--mode co -t50 -n10 --geometry 40x40x50x50 /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "mode_option_4", "args" : """-A Acceptance -q testing -n 49152 -t 60 --mode script /bin/ls""", "old_args" : "", 'new_only' : True },
    { "tc_name" : "preboot_option", "args" : """--disable_preboot -t10 -n512 --proccount 1023 --mode dual /bin/ls""", 'skip_list' : ['not_bsim'], 'new_only' : True },
    { "tc_name" : "env_option_1", "args" : """--env var1=val1,var2=val2 -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "env_option_2", "args" : """--env var1=val1:var2=val2 -t50 -n10 /bin/ls""", 'new_only' : True },
    { "tc_name" : "env_option_3", "args" : """--env "var1=val1:var2=svar1\=sval1\:svar2\=sval2:var3=val3" -t50 -n10 -d /bin/ls""", 'new_only' : True, },
    ]
