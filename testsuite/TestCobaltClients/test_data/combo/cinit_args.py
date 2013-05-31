import time
"""
This module is use for generating combo cobalt client commands on a Brooklyn or real system
"""

year    = str(time.localtime(time.time()).tm_year+10)
mon     = str(time.localtime(time.time()).tm_mon)
day     = str(time.localtime(time.time()).tm_mday)
hr      = str(time.localtime(time.time()).tm_hour)
minutes = str(time.localtime(time.time()).tm_min)

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
    {"tc_name" : "activate_partition_ANL_R01_M0_512"   , "command" : "partadm", "args" : "--activate ANL-R01-M0-512"},
    {"tc_name" : "list_1"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "delete_default_que"                  , "command" : "cqadm"  , "args" : "--delq default"},
    {"tc_name" : "add_queues"                          , "command" : "cqadm"  , "args" : "--addq default q_1 q_2 q_3 q_4"},
    {"tc_name" : "start_default"                       , "command" : "cqadm"  , "args" : "--start default q_1 q_2 q_3 q_4"},
    {"tc_name" : "get_queues"                          , "command" : "cqadm"  , "args" : "--getq"},
    {"tc_name" : "qstat_2"                             , "command" : "qstat"  , "args" : "-Q"},
    {"tc_name" : "add_que_associations_1"              , "command" : "partadm", "args" : """--queue q_1:q_2:q_3:q_4 ANL-R00-R01-2048 ANL-R00-1024"""},
    {"tc_name" : "list_3"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "add_que_associations_2"              , "command" : "partadm", "args" : """--queue q_1:q_2:q_3:q_4 ANL-R01-1024 ANL-R00-M1-512"""},
    {"tc_name" : "list_4"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "add_que_associations_3"              , "command" : "partadm", "args" : """--queue default:q_1 ANL-R00-M0-512"""},
    {"tc_name" : "list_5"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "rmq_1"                               , "command" : "partadm", "args" : """--queue q_3 --rmq ANL-R00-R01-2048 ANL-R00-1024"""},
    {"tc_name" : "list_6"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "rmq_2"                               , "command" : "partadm", "args" : """--queue q_2 --rmq ANL-R00-R01-2048"""},
    {"tc_name" : "list_7"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "appq_1"                              , "command" : "partadm", "args" : """--queue q_3 --appq ANL-R00-R01-2048 ANL-R00-1024"""},
    {"tc_name" : "list_8"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "appq_2"                              , "command" : "partadm", "args" : """--queue q_2 --appq ANL-R00-R01-2048"""},
    {"tc_name" : "list_9"                              , "command" : "partadm", "args" : "-l"},
    {"tc_name" : "qstat_2"                             , "command" : "qstat"  , "args" : "-Q"},
    {"tc_name" : "setres_1"                            , "command" : "setres" , "args" : "-n george -s %s_%s_%s-%s:%s -d 50  -q q_1 ANL-R00-R01-2048" % (year, mon, day, hr, minutes) },
    {"tc_name" : "showres_1"                           , "command" : "showres", "args" : "-x"},
    {"tc_name" : "setres_2"                            , "command" : "setres" , "args" : "-n george -m -d 300"},
    {"tc_name" : "showres_2"                           , "command" : "showres", "args" : "-x"},
    {"tc_name" : "setres_3"                            , "command" : "setres" , "args" : "-n res_passed -s 2010_12_1-10:30 -d 50  -q q_1 ANL-R00-R01-2048"},
    {"tc_name" : "showres_3"                           , "command" : "showres", "args" : "-x"},
    ]
