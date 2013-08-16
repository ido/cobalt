
Cobalt client tests are located in the following directory structure in the Cobalt repo:

../cobalt/testsuite/TestCobaltClients - 

../TESTUTILS_README.txt - this file

../testutils.py - utility to generate tests output: *_test.py

../oldcmds - directory containing the old Cobalt client commands prior to refactoring.
             The following are the Cobalt client commands:

             boot-block.py
             cqadm.py
             get-bootable-blocks.py
             nodeadm.py
             nodelist.py
             partadm.py
             partlist.py
             qalter.py
             qdel.py
             qhold.py
             qmove.py
             qrls.py
             qselect.py
             qstat.py
             qsub.py
             schedctl.py
             setres.py
             showres.py
             slpstat.py

../test_data - directory containing the modules for each Cobalt client command containing the arguments to test.
               The following are the files (one for each Cobalt client command):

             boot-block_args.py
             cqadm_args.py
             get-bootable-blocks_args.py
             nodeadm_args.py
             nodelist_args.py
             partadm_args.py
             partlist_args.py
             qalter_args.py
             qdel_args.py
             qhold_args.py
             qmove_args.py
             qrls_args.py
             qselect_args.py
             qstat_args.py
             qsub_args.py
             schedctl_args.py
             setres_args.py
             showres_args.py
             slpstat_args.py

             These modules get consumed by the test utility python module 'testutils.py'. 
             'testutils.py' will import the modules to generate the Cobalt client commands tests 
             (the ones residing in ../test_files).

             Each module contains a single list of dictionaries objects called 'test_argslist'.
             Each dictionary is composed of the following keys:

             'tc_name'  - Name of the test case. This is used as a sufix to the test function 
                          that nosetests runs. MANDATORY key.
             'args'     - Arguments to the Cobalt client command. MANDATORY key.
             'old_args' - If the arguments to an old version of the command is different than the new version then
                          this should have the old arguments here.
             'new_only' - This specifies that this argument is only valid for the new implementation of the command. 
                          Boolean (True,False)
             'testhook' - This is a string that gets stored in a .testhook for a test stub to read. In this case
                          the stub is ./testlib/Proxy.py

../test_files - directory containing the auto-generated test files.
                The following are the files (one for each Cobalt client command):

             boot-block_test.py
             cqadm_test.py
             get-bootable-blocks_test.py
             nodeadm_test.py
             nodelist_test.py
             partadm_test.py
             partlist_test.py
             qalter_test.py
             qdel_test.py
             qhold_test.py
             qmove_test.py
             qrls_test.py
             qselect_test.py
             qstat_test.py
             qsub_test.py
             schedctl_test.py
             setres_test.py
             showres_test.py
             slpstat_test.py
                  
             The tests are auto-generated from the python modules located in ../test_data

             To re-generate all the Cobalt client command tests do the following:

             ./testutils.py -o oldcmds -t test_data

             To generate a specific cobalt client commands do the following:

             ./testutils.py -o oldcmds -t test_data qsub qalter ...

             Where 'oldcmds' is the directory where the baseline of Cobalt client commands where refactored and
             'test_data' is the directory where all the Cobalt client test argument modules reside.

             If you wish add an argument test to a particular Cobalt client command then added to 'test_argslist' list
             as a dictionary in the format described above.

             If you are adding a argument test that only works for the new refactored code then use the 'new_only' key.

             The 'testhook' key is useful for allowing for stubs to take different actions in order to test different 
             permutations with the same arguments.

             When you run 'testutils.py' it will place the files in the current working directory, so you need to 
             move them to ../test_files once they are ready.

../testlib - contains Proxy.py - Proxy stub used when running the tests.

The following is the Jenkins setup in order to run the tests: 
_______________________________________________________________________________________________________________________________________________
#!/bin/bash -x

cd cobalt
ln -s "$WORKSPACE/cobalt/src/lib" "$WORKSPACE/cobalt/src/Cobalt"
ln -s misc/partitions.xml simulator.xml
export PYTHONPATH="$WORKSPACE/cobalt/testsuite/TestCobaltClients":"$WORKSPACE/cobalt/src":"$WORKSPACE/cobalt/testsuite/TestCobaltClients/testlib"
export PATH="$WORKSPACE/cobalt/src/clients":"$WORKSPACE/cobalt/src/clients/POSIX":"$PATH"
export COBALT_CONFIG_FILES="$WORKSPACE/cobalt/testsuite/TestCobaltClients/test_data/cobalt.conf"

rm -rf testsuite/TestCobaltClients/Cobalt
rm -rf testsuite/TestCobaltClients/testlib/Components

ln -sf "$WORKSPACE/cobalt/src/lib/client_utils.py"             testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/Exceptions.py"               testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/Logging.py"                  testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/JSONEncoders.py"             testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/arg_parser.py"               testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/Util.py"                     testsuite/TestCobaltClients/testlib/
ln -sf "$WORKSPACE/cobalt/src/lib/__init__.py"                 testsuite/TestCobaltClients/testlib/
ln -s  "$WORKSPACE/cobalt/src/lib/Components"                  testsuite/TestCobaltClients/testlib/
ln -s  "$WORKSPACE/cobalt/testsuite/TestCobaltClients/testlib" testsuite/TestCobaltClients/Cobalt

cd testsuite/TestCobaltClients

nosetests --with-xunit --xunit-file=../../clients_xunit.xml -v
_______________________________________________________________________________________________________________________________________________

To run the tests do the following:

export P=<parent dir where the cobalt repor resides>

# ---- only once ----
export COBALT_SOURCE_DIR=$P/Cobalt/cobalt
export COBALT_RUNTIME_DIR=$P/Cobalt/sysroot-brooklyn
export COBALT_SYSTEM_TYPE=BGSIM
export COBALT_CONFIG_FILES=$COBALT_RUNTIME_DIR/etc/cobalt.conf
export PATH=${COBALT_SOURCE_DIR}/src/clients:${COBALT_SOURCE_DIR}/src/clients/POSIX:$PATH_BASIS
export PYTHONPATH=$COBALT_SOURCE_DIR/testsuite/TestCobaltClients/:$COBALT_SOURCE_DIR/src:$COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib

rm -rf $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/Components
rm -rf $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/Cobalt

ln -fs $COBALT_SOURCE_DIR/src/lib/client_utils.py $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/Exceptions.py   $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/Logging.py      $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/JSONEncoders.py $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/arg_parser.py   $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/Util.py         $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/__init__.py     $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs $COBALT_SOURCE_DIR/src/lib/Components      $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/testlib/
ln -fs testlib                                    $COBALT_SOURCE_DIR/testsuite/TestCobaltClients/Cobalt
# ----

cd $COBALT_SOURCE?DIR/testsuite/TestCobaltClients
nosetest -v


