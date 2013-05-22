"""
This module is use for generating combo cobalt client commands on a Brooklyn or real system
"""

test_argslist = [
    {"tc_name" : "delete_partions"                     , "command" : "partadm", "args" : "-d '*'"},

    {"tc_name" : "add_partition_ANL_R00_R01_2048"      , "command" : "partadm", "args" : "-a ANL-R00-R01-2048"},
    {"tc_name" : "enable_partition_ANL_R00_R01_2048"   , "command" : "partadm", "args" : "--enable ANL-R00-R01-2048"},
    {"tc_name" : "activate_partition_ANL_R00_R01_2048" , "command" : "partadm", "args" : "--activate ANL-R00-R01-2048"},
    {"tc_name" : "add_partition_ANL_R00_1024"          , "command" : "partadm", "args" : "-a ANL-R00-1024"},
    {"tc_name" : "enable_partition_ANL_R00_1024"       , "command" : "partadm", "args" : "--enable ANL-R00-1024"},
    {"tc_name" : "activate_partition_ANL_R00_1024"     , "command" : "partadm", "args" : "--activate ANL-R00-1024"},
    {"tc_name" : "add_partition_ANL_R01_1024"          , "command" : "partadm", "args" : "-a ANL-R01-1024"},
    {"tc_name" : "enable_partition_ANL_R01_1024"       , "command" : "partadm", "args" : "--enable ANL-R01-1024"},
    {"tc_name" : "activate_partition_ANL_R01_1024"     , "command" : "partadm", "args" : "--activate ANL-R01-1024"},
    {"tc_name" : "add_partition_ANL_R00_M0_512"        , "command" : "partadm", "args" : "-a ANL-R00-M0-512"},
    {"tc_name" : "enable_partition_ANL_R00_M0_512"     , "command" : "partadm", "args" : "--enable ANL-R00-M0-512"},
    {"tc_name" : "activate_partition_ANL_R00_M0_512"   , "command" : "partadm", "args" : "--activate ANL-R00-M0-512"},
    {"tc_name" : "add_partition_ANL_R00_M1_512"        , "command" : "partadm", "args" : "-a ANL-R00-M1-512"},
    {"tc_name" : "enable_partition_ANL_R00_M1_512"     , "command" : "partadm", "args" : "--enable ANL-R00-M1-512"},
    {"tc_name" : "activate_partition_ANL_R00_M1_512"   , "command" : "partadm", "args" : "--activate ANL-R00-M1-512"},
    {"tc_name" : "add_partition_ANL_R01_M0_512"        , "command" : "partadm", "args" : "-a ANL-R01-M0-512"},
    {"tc_name" : "enable_partition_ANL_R01_M0_512"     , "command" : "partadm", "args" : "--enable ANL-R01-M0-512"},
    {"tc_name" : "activate_partition_ANL_R0=1_M0_512"   , "command" : "partadm", "args" : "--activate ANL-R01-M0-512"},
    {"tc_name" : "list"                                , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "delete_default_que"                  , "command" : "cqadm"  , "args" : "--delq default"},
    {"tc_name" : "add_default_que"                     , "command" : "cqadm"  , "args" : "--addq default"},
    {"tc_name" : "start_default"                       , "command" : "cqadm"  , "args" : "--start default"},
    {"tc_name" : "get_queues"                          , "command" : "cqadm"  , "args" : "--getq"},
    {"tc_name" : "show_ques_prop"                      , "command" : "qstat"  , "args" : "-Q"},
    ]
