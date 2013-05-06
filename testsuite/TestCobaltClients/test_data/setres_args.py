"""
This module defines the test argument information list for setres.py and will 
dynamically be imported by testutils.py to generate the tests for setres.py.

Refer to the TESTUTILS_README.txt for more information about the usage of this module and testutils.py

test_argslist - is a list of dictionaries, each dictionary has all the necessary info for a test.

"""

test_argslist = [
    { "tc_name" : "id_change_1", "args" : """--res_id 8""", },
    { "tc_name" : "id_change_1", "args" : """--debub --res_id 8""", "new_only" : True,},
    { "tc_name" : "id_change_2", "args" : """--cycle_id 8""", },
    { "tc_name" : "id_change_3", "args" : """--res_id 8 --cycle_id 8""", },
    { "tc_name" : "id_change_4", "args" : """--res_id 8 p1 p2 p3""", "old_args" : "", },
    { "tc_name" : "id_change_5", "args" : """--cycle_id 8 p1 p2 p3""", "old_args" : "", },
    { "tc_name" : "id_change_6", "args" : """--res_id 8 -m -n resname""", "old_args" : "", },
    { "tc_name" : "id_change_7", "args" : """--cycle_id 8 -p p1""", "old_args" : "", },
    { "tc_name" : "force_1", "args" : """--cycle_id 8 --res_id 8 --force_id""", },
    { "tc_name" : "force_2", "args" : """--force_id""", },
    { "tc_name" : "force_3", "args" : """--force_id -p p1 -s 2013_03_09-10:30""", },
    { "tc_name" : "force_4", "args" : """--force_id -m -n resname""", },
    { "tc_name" : "modify_1", "args" : """-m""", },
    { "tc_name" : "modify_2", "args" : """-m -n resname""", },
    { "tc_name" : "modify_3", "args" : """-m -n resname -D -c 10:10:10""", "old_args" : "", },
    { "tc_name" : "modify_4", "args" : """-m -n resname -D -s 2013_03_9-10:10:10""", },
    { "tc_name" : "modify_5", "args" : """-m -n resname -D -s 2013_03_9-10:10""", "old_args" : "", },
    { "tc_name" : "modify_6", "args" : """-m -n resname -D -d 10:10:10""", },
    { "tc_name" : "modify_7", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10:30:30 -d 00:01:00""", },
    { "tc_name" : "modify_8", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u user1""", },
    { "tc_name" : "modify_9", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u user1:user2""", },
    { "tc_name" : "modify_10", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj -u user1""", },
    { "tc_name" : "modify_11", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --block_passthrough""", },
    { "tc_name" : "modify_12", "args" : """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --allow_passthrough""", },
    { "tc_name" : "modify_13", "args" : """-m -n resname --allow_passthrough --block_passthrough""", "old_args" : "", },
    { "tc_name" : "modify_14", "args" : """-m -n resname -A myproj --block_passthrough p1 p2 p3""", },
    { "tc_name" : "add_res_1", "args" : """-n resname -D""", },
    { "tc_name" : "add_res_2", "args" : """-n resname -D p1 p2 p3""", "old_args" : "", },
    { "tc_name" : "add_res_3", "args" : """-n resname -s 2013_03_9-10:10 p1 p2""", "old_args" : "", },
    { "tc_name" : "add_res_4", "args" : """-n resname -s 2013_03_9-10:10 -d 50 p1 p2""", },
    { "tc_name" : "add_res_5", "args" : """-n resname -s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2""", },
    { "tc_name" : "add_res_6", "args" : """-s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2""", },
    { "tc_name" : "add_res_7", "args" : """-s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough""", },
    { "tc_name" : "add_res_8", "args" : """-s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough -q myq -A myproj""", },
    ]
