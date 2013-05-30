import testutils

# ---------------------------------------------------------------------------------
def test_partadm_version_option():
    """
    partadm test run: version_option
        Old Command Output:
          Cobalt Version: $Version$
          

    """

    args      = """--version"""

    cmdout    = \
"""version: "partadm.py " + $Revision: 1981 $ + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_help_option_1():
    """
    partadm test run: help_option_1
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -a                    add the block to the list of managed blocks
            -d                    remove the block from the list of managed blocks
            -l                    list all blocks and their status
            -r, --recursive       recursively add all child blocks of the specified
                                  blocks in the positional arguments
            --queue=QUEUE         set the queues associated with the target blocks to
                                  this list of queues
            --activate            activate the block for scheduling
            --deactivate          deactivate the block for schedulign
            --enable              enable the running of jobs on the target blocks
            --disable             disable the running of jobs on the target blocks
            --fail                mark the block as though it failed diagnostics
                                  (deprecated)
            --unfail              clear failed diagnostics on a block (deprecated)
            --dump                dump a representation of the system's block state
            --xml                 dump a xml representation of the system's blocks for
                                  simulator usage
            --savestate=SAVESTATE
                                  force the system component to write it's statefile
            --boot-stop           disable booting of any jobs
            --boot-start          enable booting of any jobs
            --boot-status         show whether or not booting is enabled
            -b, --blockinfo       print the detailed state and information for all
                                  requested blocks.
            --pg_list             not implemented yet
            -c, --clean_block     force the block to cleanup and clear all internal
                                  reservations on that resource
          

    """

    args      = """-h"""

    cmdout    = \
"""Usage: partadm.py [-a|-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a                    add the block to the list of managed blocks
  -d                    remove the block from the list of managed blocks
  --debug               turn on communication debugging
  -l                    list all blocks and their status
  -r, --recursive       recursively add all child blocks of the specified
                        blocks in the positional arguments
  --queue=QUEUE         set the queues associated with the target blocks to
                        this list of queues.
  --rmq                 Only valid with --queue option. If provided queue(s)
                        will be removed from the target block association.
  --appq                Only valid with --queue option. If provided queue(s)
                        will be appended to the target block association.
  --activate            activate the block for scheduling
  --deactivate          deactivate the block for schedulign
  --enable              enable the running of jobs on the target blocks
  --disable             disable the running of jobs on the target blocks
  --fail                mark the block as though it failed diagnostics
                        (deprecated)
  --unfail              clear failed diagnostics on a block (deprecated)
  --dump                dump a representation of the system's block state
  --xml                 dump a xml representation of the system's blocks for
                        simulator usage
  --savestate=SAVESTATE
                        force the system component to write it's statefile
  --boot-stop           disable booting of any jobs
  --boot-start          enable booting of any jobs
  --boot-status         show whether or not booting is enabled
  -b, --blockinfo       print the detailed state and information for all
                        requested blocks.
  --pg_list             not implemented yet
  -c, --clean_block     force the block to cleanup and clear all internal
                        reservations on that resource
  -i, --list_io         list information on IOBlock status
  --add_io_block        add an IO Block to the list of managed IO blocks
  --del_io_block        delete an IO Block to the list of managed IO blocks
  --boot_io_block       initiate a boot of the IO Blocks as positional
                        arguments
  --free_io_block       initiate a free of the IO Blocks as positional
                        arguments
  --set_io_autoboot     set an IO block to be automatically booted
  --unset_io_autoboot   stop automatically rebooting an IO block
  --io_autoboot_start   enable IO Block autobooting
  --io_autoboot_stop    disable IO Block autobooting
  --io_autoboot_status  get status of IO Block autobooting
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_help_option_2():
    """
    partadm test run: help_option_2
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -a                    add the block to the list of managed blocks
            -d                    remove the block from the list of managed blocks
            -l                    list all blocks and their status
            -r, --recursive       recursively add all child blocks of the specified
                                  blocks in the positional arguments
            --queue=QUEUE         set the queues associated with the target blocks to
                                  this list of queues
            --activate            activate the block for scheduling
            --deactivate          deactivate the block for schedulign
            --enable              enable the running of jobs on the target blocks
            --disable             disable the running of jobs on the target blocks
            --fail                mark the block as though it failed diagnostics
                                  (deprecated)
            --unfail              clear failed diagnostics on a block (deprecated)
            --dump                dump a representation of the system's block state
            --xml                 dump a xml representation of the system's blocks for
                                  simulator usage
            --savestate=SAVESTATE
                                  force the system component to write it's statefile
            --boot-stop           disable booting of any jobs
            --boot-start          enable booting of any jobs
            --boot-status         show whether or not booting is enabled
            -b, --blockinfo       print the detailed state and information for all
                                  requested blocks.
            --pg_list             not implemented yet
            -c, --clean_block     force the block to cleanup and clear all internal
                                  reservations on that resource
          

    """

    args      = """--help"""

    cmdout    = \
"""Usage: partadm.py [-a|-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a                    add the block to the list of managed blocks
  -d                    remove the block from the list of managed blocks
  --debug               turn on communication debugging
  -l                    list all blocks and their status
  -r, --recursive       recursively add all child blocks of the specified
                        blocks in the positional arguments
  --queue=QUEUE         set the queues associated with the target blocks to
                        this list of queues.
  --rmq                 Only valid with --queue option. If provided queue(s)
                        will be removed from the target block association.
  --appq                Only valid with --queue option. If provided queue(s)
                        will be appended to the target block association.
  --activate            activate the block for scheduling
  --deactivate          deactivate the block for schedulign
  --enable              enable the running of jobs on the target blocks
  --disable             disable the running of jobs on the target blocks
  --fail                mark the block as though it failed diagnostics
                        (deprecated)
  --unfail              clear failed diagnostics on a block (deprecated)
  --dump                dump a representation of the system's block state
  --xml                 dump a xml representation of the system's blocks for
                        simulator usage
  --savestate=SAVESTATE
                        force the system component to write it's statefile
  --boot-stop           disable booting of any jobs
  --boot-start          enable booting of any jobs
  --boot-status         show whether or not booting is enabled
  -b, --blockinfo       print the detailed state and information for all
                        requested blocks.
  --pg_list             not implemented yet
  -c, --clean_block     force the block to cleanup and clear all internal
                        reservations on that resource
  -i, --list_io         list information on IOBlock status
  --add_io_block        add an IO Block to the list of managed IO blocks
  --del_io_block        delete an IO Block to the list of managed IO blocks
  --boot_io_block       initiate a boot of the IO Blocks as positional
                        arguments
  --free_io_block       initiate a free of the IO Blocks as positional
                        arguments
  --set_io_autoboot     set an IO block to be automatically booted
  --unset_io_autoboot   stop automatically rebooting an IO block
  --io_autoboot_start   enable IO Block autobooting
  --io_autoboot_stop    disable IO Block autobooting
  --io_autoboot_status  get status of IO Block autobooting
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_no_arg_1():
    """
    partadm test run: no_arg_1

    """

    args      = ''

    cmdout    = \
"""Must supply one of -a or -d or -l or -start or -stop or --queue or -b.
Adding "-r" or "--recursive" will add the children of the blocks passed in.

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_no_arg_2():
    """
    partadm test run: no_arg_2

    """

    args      = """-a"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_debug():
    """
    partadm test run: debug

    """

    args      = """--debug"""

    cmdout    = \
"""
partadm.py --debug

Must supply one of -a or -d or -l or -start or -stop or --queue or -b.
Adding "-r" or "--recursive" will add the children of the blocks passed in.

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_1():
    """
    partadm test run: combo_options_1

    """

    args      = """-a -d ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: delete option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_2():
    """
    partadm test run: combo_options_2

    """

    args      = """-a --enable ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_3():
    """
    partadm test run: combo_options_3

    """

    args      = """-d --enable ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_4():
    """
    partadm test run: combo_options_4

    """

    args      = """--enable --disable ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: disable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_5():
    """
    partadm test run: combo_options_5

    """

    args      = """--deactivate --activate ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_6():
    """
    partadm test run: combo_options_6

    """

    args      = """-a --deactivate ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_7():
    """
    partadm test run: combo_options_7

    """

    args      = """--fail --unfail ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: unfail option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_8():
    """
    partadm test run: combo_options_8

    """

    args      = """--savestate /tmp/savestate -a"""

    cmdout    = \
"""Option combinations not allowed with: savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_9():
    """
    partadm test run: combo_options_9

    """

    args      = """-l --xml"""

    cmdout    = \
"""Option combinations not allowed with: list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_10():
    """
    partadm test run: combo_options_10

    """

    args      = """-l --xml"""

    cmdout    = \
"""Option combinations not allowed with: list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_11():
    """
    partadm test run: combo_options_11

    """

    args      = """-a --queue q1 ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_12():
    """
    partadm test run: combo_options_12

    """

    args      = """--dump --queue q1 ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_13():
    """
    partadm test run: combo_options_13

    """

    args      = """--savestate /tmp/s --xml"""

    cmdout    = \
"""Option combinations not allowed with: savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_14():
    """
    partadm test run: combo_options_14

    """

    args      = """-a -c -b ANL-R00-R01-2048"""

    cmdout    = \
"""Option combinations not allowed with: add, blockinfo, clean_block option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_15():
    """
    partadm test run: combo_options_15

    """

    args      = """--list_io -a"""

    cmdout    = \
"""Name  Size  State  CS Status  BlockComputes  Autoreboot
=========================================================
P1    0     idle   OK               x        x         
P2    1     idle   OK               x        x         
P3    2     idle   OK               x        x         
P4    3     idle   OK               x        x         
P5    4     idle   OK               x        x         
P6    5     idle   OK               x        x         
P7    6     idle   OK               x        x         
P8    7     idle   OK               x        x         
P9    8     idle   OK               x        x         
P10   9     idle   OK               x        x         
"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser

GET_IO_BLOCKS

plist: [{'status': '*', 'name': '*', 'state': '*', 'autoreboot': '*', 'block_computes_for_reboot': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_16():
    """
    partadm test run: combo_options_16

    """

    args      = """--list_io -a ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""Name  Size  State  CS Status  BlockComputes  Autoreboot
=========================================================
P1    0     idle   OK               x        x         
P2    1     idle   OK               x        x         
P3    2     idle   OK               x        x         
P4    3     idle   OK               x        x         
P5    4     idle   OK               x        x         
P6    5     idle   OK               x        x         
P7    6     idle   OK               x        x         
P8    7     idle   OK               x        x         
P9    8     idle   OK               x        x         
P10   9     idle   OK               x        x         
"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-M0-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-M1-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R01-M0-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-M0-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-M1-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R01-M0-512
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_IO_BLOCKS

plist: [{'status': '*', 'name': '*', 'state': '*', 'autoreboot': '*', 'block_computes_for_reboot': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_17():
    """
    partadm test run: combo_options_17

    """

    args      = """--list_io --rmq ANL-R00-M0-512"""

    cmdout    = \
"""Option combinations not allowed with: rmq, list_io, rmq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_18():
    """
    partadm test run: combo_options_18

    """

    args      = """--list_io --appq ANL-R00-M0-512"""

    cmdout    = \
"""Option combinations not allowed with: appq, list_io, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_19():
    """
    partadm test run: combo_options_19

    """

    args      = """--queue q1:q2 --rmq --appq ANL-R00-M0-512"""

    cmdout    = \
"""Option combinations not allowed with: rmq, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_1():
    """
    partadm test run: add_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """-a -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:a
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:a
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_2():
    """
    partadm test run: add_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """-a --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:a
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:a
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_3():
    """
    partadm test run: add_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """-a ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R01-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R01-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_4():
    """
    partadm test run: add_option_4

    """

    args      = """-a -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_5():
    """
    partadm test run: add_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """-a -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-1024
name type: <type 'str'>
queue:default
queue type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
size:*
size type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_1():
    """
    partadm test run: delete_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """-d -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

DEL_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_2():
    """
    partadm test run: delete_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """-d --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

DEL_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_3():
    """
    partadm test run: delete_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """-d ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
DEL_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_4():
    """
    partadm test run: delete_option_4

    """

    args      = """-d -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
DEL_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_5():
    """
    partadm test run: delete_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """-d -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
DEL_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_1():
    """
    partadm test run: enable_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--enable -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:True
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_2():
    """
    partadm test run: enable_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--enable --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:True
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_3():
    """
    partadm test run: enable_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--enable ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:True
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_4():
    """
    partadm test run: enable_option_4

    """

    args      = """--enable -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:True
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_5():
    """
    partadm test run: enable_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--enable -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:True
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_1():
    """
    partadm test run: disable_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--disable -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_2():
    """
    partadm test run: disable_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--disable --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_3():
    """
    partadm test run: disable_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--disable ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_4():
    """
    partadm test run: disable_option_4

    """

    args      = """--disable -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_5():
    """
    partadm test run: disable_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--disable -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
scheduled:False
scheduled type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_1():
    """
    partadm test run: activate_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--activate -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:True
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_2():
    """
    partadm test run: activate_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--activate --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:True
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_3():
    """
    partadm test run: activate_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--activate ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:True
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_4():
    """
    partadm test run: activate_option_4

    """

    args      = """--activate -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:True
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_5():
    """
    partadm test run: activate_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--activate -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:True
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_1():
    """
    partadm test run: deactivate_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--deactivate -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_2():
    """
    partadm test run: deactivate_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--deactivate --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_3():
    """
    partadm test run: deactivate_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--deactivate ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_4():
    """
    partadm test run: deactivate_option_4

    """

    args      = """--deactivate -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_5():
    """
    partadm test run: deactivate_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--deactivate -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
SET_PARTITION

user name: gooduser
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
functional:False
functional type: <type 'bool'>
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_1():
    """
    partadm test run: fail_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--fail -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_2():
    """
    partadm test run: fail_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--fail --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_3():
    """
    partadm test run: fail_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--fail ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}, {'tag': 'partition', 'name': 'ANL-R01-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_4():
    """
    partadm test run: fail_option_4

    """

    args      = """--fail -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_5():
    """
    partadm test run: fail_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--fail -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_1():
    """
    partadm test run: unfail_option_1
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--unfail -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_2():
    """
    partadm test run: unfail_option_2
        Old Command Output:
          ['ANL-R00-R01-2048', 'a']
          

    """

    args      = """--unfail --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children_list': '*'}]

UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_3():
    """
    partadm test run: unfail_option_3
        Old Command Output:
          ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
          

    """

    args      = """--unfail ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    stubout   = \
"""
UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}, {'tag': 'partition', 'name': 'ANL-R01-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R01-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_4():
    """
    partadm test run: unfail_option_4

    """

    args      = """--unfail -b ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-R01-2048
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: ANL-R00-1024
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-R01-2048', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'ANL-R00-1024', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-R01-2048', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'ANL-R00-1024', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_5():
    """
    partadm test run: unfail_option_5
        Old Command Output:
          Initiating cleanup on block ANL-R00-R01-2048
          Initiating cleanup on block ANL-R00-1024
          

    """

    args      = """--unfail -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Initiating cleanup on block ANL-R00-R01-2048
Initiating cleanup on block ANL-R00-1024
"""

    stubout   = \
"""
UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'ANL-R00-1024'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:ANL-R00-1024
name type: <type 'str'>
tag:partition
tag type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: ANL-R00-R01-2048
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: ANL-R00-1024
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_1():
    """
    partadm test run: savestate_option_1
        Old Command Output:
          directory /bad does not exist
          

    """

    args      = """--savestate /bad/save"""

    cmdout    = \
"""directory /bad/save does not exist
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_2():
    """
    partadm test run: savestate_option_2
        Old Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--savestate /tmp/save ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_3():
    """
    partadm test run: savestate_option_3
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          partadm.py: error: --savestate option requires an argument
          

    """

    args      = """--savestate"""

    cmdout    = \
"""Usage: partadm.py [-a|-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


partadm.py: error: --savestate option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_4():
    """
    partadm test run: savestate_option_4
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          

    """

    args      = """--savestate /tmp/save -c ANL-R00-M0-512"""

    cmdout    = \
"""Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_5():
    """
    partadm test run: savestate_option_5

    """

    args      = """--savestate /tmp/save -b ANL-R00-M0-512"""

    cmdout    = \
"""Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_1():
    """
    partadm test run: xml_option_1
        Old Command Output:
          ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
          

    """

    args      = """--xml"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    stubout   = \
"""
GENERATE_XML

name:*
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_2():
    """
    partadm test run: xml_option_2
        Old Command Output:
          ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
          

    """

    args      = """--xml ANL-R00-M0-512"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    stubout   = \
"""
GENERATE_XML

name:*
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_3():
    """
    partadm test run: xml_option_3
        Old Command Output:
          ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
          

    """

    args      = """--xml --recursive ANL-R00-M0-512"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

GENERATE_XML

name:*
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_4():
    """
    partadm test run: xml_option_4

    """

    args      = """--xml --blockinfo"""

    cmdout    = \
"""Name: P1
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P2
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P3
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P4
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P5
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P6
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P7
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P8
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P9
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P10
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P1
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P2
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P3
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P4
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P5
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P6
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P7
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P8
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P9
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P10
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
GENERATE_XML

name:*
name type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P3', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P4', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P5', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P6', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P7', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P8', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P9', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P10', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P1', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P2', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P3', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P4', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P5', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P6', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P7', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P8', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P9', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P10', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_5():
    """
    partadm test run: xml_option_5
        Old Command Output:
          Initiating cleanup on block P1
          Initiating cleanup on block P2
          Initiating cleanup on block P3
          Initiating cleanup on block P4
          Initiating cleanup on block P5
          Initiating cleanup on block P6
          Initiating cleanup on block P7
          Initiating cleanup on block P8
          Initiating cleanup on block P9
          Initiating cleanup on block P10
          

    """

    args      = """--xml --clean_block"""

    cmdout    = \
"""Initiating cleanup on block P1
Initiating cleanup on block P2
Initiating cleanup on block P3
Initiating cleanup on block P4
Initiating cleanup on block P5
Initiating cleanup on block P6
Initiating cleanup on block P7
Initiating cleanup on block P8
Initiating cleanup on block P9
Initiating cleanup on block P10
"""

    stubout   = \
"""
GENERATE_XML

name:*
name type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: P1
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P2
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P3
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P4
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P5
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P6
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P7
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P8
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P9
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P10
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_6():
    """
    partadm test run: xml_option_6

    """

    args      = """--xml --recursive --blockinfo"""

    cmdout    = \
"""Name: P1
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P2
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P3
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P4
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P5
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P6
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P7
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P8
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P9
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P10
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P1
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P2
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P3
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P4
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P5
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P6
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P7
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P8
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P9
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: P10
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GENERATE_XML

name:*
name type: <type 'str'>

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P3', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P4', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P5', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P6', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P7', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P8', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P9', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'P10', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P1', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P2', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P3', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P4', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P5', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P6', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P7', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P8', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P9', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': 'P10', 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_xml_option_7():
    """
    partadm test run: xml_option_7
        Old Command Output:
          Initiating cleanup on block P1
          Initiating cleanup on block P2
          Initiating cleanup on block P3
          Initiating cleanup on block P4
          Initiating cleanup on block P5
          Initiating cleanup on block P6
          Initiating cleanup on block P7
          Initiating cleanup on block P8
          Initiating cleanup on block P9
          Initiating cleanup on block P10
          

    """

    args      = """--xml --recursive --clean_block"""

    cmdout    = \
"""Initiating cleanup on block P1
Initiating cleanup on block P2
Initiating cleanup on block P3
Initiating cleanup on block P4
Initiating cleanup on block P5
Initiating cleanup on block P6
Initiating cleanup on block P7
Initiating cleanup on block P8
Initiating cleanup on block P9
Initiating cleanup on block P10
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GENERATE_XML

name:*
name type: <type 'str'>

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: P1
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P2
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P3
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P4
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P5
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P6
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P7
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P8
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P9
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: P10
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_1():
    """
    partadm test run: queue_option_1
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          partadm.py: error: --queue option requires an argument
          

    """

    args      = """--queue"""

    cmdout    = \
"""Usage: partadm.py [-a|-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


partadm.py: error: --queue option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_2():
    """
    partadm test run: queue_option_2
        Old Command Output:
          'q_4' is not an existing queue
          'q_3' is not an existing queue
          

    """

    args      = """--queue q_4:q_3 ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""'q_4' is not an existing queue
'q_3' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_3():
    """
    partadm test run: queue_option_3
        Old Command Output:
          'q_1' is not an existing queue
          'q_2' is not an existing queue
          'q_3' is not an existing queue
          'q_4' is not an existing queue
          

    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R00-M0-512"""

    cmdout    = \
"""'q_1' is not an existing queue
'q_2' is not an existing queue
'q_3' is not an existing queue
'q_4' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_4():
    """
    partadm test run: queue_option_4
        Old Command Output:
          'q_1' is not an existing queue
          

    """

    args      = """--queue q_1 -c ANL-R00-M0-512"""

    cmdout    = \
"""'q_1' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_5():
    """
    partadm test run: queue_option_5

    """

    args      = """--queue q_2 -b ANL-R00-M0-512"""

    cmdout    = \
"""'q_2' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_6():
    """
    partadm test run: queue_option_6

    """

    args      = """--queue q_1 -r -b ANL-R00-M0-512"""

    cmdout    = \
"""'q_1' is not an existing queue
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_7():
    """
    partadm test run: queue_option_7
        Old Command Output:
          'q_2' is not an existing queue
          

    """

    args      = """--queue q_2 -r -c ANL-R00-M0-512"""

    cmdout    = \
"""'q_2' is not an existing queue
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_8():
    """
    partadm test run: queue_option_8

    """

    args      = """--queue q_1 --appq -r -c ANL-R00-M0-512"""

    cmdout    = \
"""Option combinations not allowed with: appq, clean_block, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_9():
    """
    partadm test run: queue_option_9

    """

    args      = """--queue q_2 --rmq -r -c ANL-R00-M0-512"""

    cmdout    = \
"""Option combinations not allowed with: rmq, clean_block, rmq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_10():
    """
    partadm test run: queue_option_10

    """

    args      = """--queue q_1 --rmq ANL-R00-M0-512 ANL-R00-M1-512"""

    cmdout    = \
"""'q_1' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_11():
    """
    partadm test run: queue_option_11

    """

    args      = """--queue q_1 --appq ANL-R00-M0-512 ANL-R00-M1-512"""

    cmdout    = \
"""'q_1' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_1():
    """
    partadm test run: dump_option_1
        Old Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_2():
    """
    partadm test run: dump_option_2
        Old Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_3():
    """
    partadm test run: dump_option_3
        Old Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump --recursive ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_4():
    """
    partadm test run: dump_option_4

    """

    args      = """--dump --blockinfo"""

    cmdout    = \
"""Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_5():
    """
    partadm test run: dump_option_5
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          

    """

    args      = """--dump --clean_block"""

    cmdout    = \
"""Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_6():
    """
    partadm test run: dump_option_6

    """

    args      = """--dump --recursive --blockinfo"""

    cmdout    = \
"""Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 0
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

Name: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    scheduled                 : True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : A
    children                  : a
    size                      : 9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : a, b, c
    block_computes_for_reboot : True
    autoreboot                : True

"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'io_node_list': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]

GET_IO_BLOCKS

plist: [{'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}, {'status': '*', 'state': '*', 'autoreboot': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'io_drawer_list': '*', 'block_computes_for_reboot': '*', 'io_node_list': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_dump_option_7():
    """
    partadm test run: dump_option_7
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
          

    """

    args      = """--dump --recursive --clean_block"""

    cmdout    = \
"""Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
Initiating cleanup on block {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
var2 : None, type = <type 'NoneType'>
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_1():
    """
    partadm test run: boot_stop_option_1
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_2():
    """
    partadm test run: boot_stop_option_2
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop ANL-R00-M0-512"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_3():
    """
    partadm test run: boot_stop_option_3
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_4():
    """
    partadm test run: boot_stop_option_4
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --blockinfo"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_5():
    """
    partadm test run: boot_stop_option_5
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --clean_block"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_6():
    """
    partadm test run: boot_stop_option_6
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive --blockinfo"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_stop_option_7():
    """
    partadm test run: boot_stop_option_7
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive --clean_block"""

    cmdout    = \
"""Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

HALT_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_1():
    """
    partadm test run: boot_start_option_1
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_2():
    """
    partadm test run: boot_start_option_2
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start ANL-R00-M0-512"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_3():
    """
    partadm test run: boot_start_option_3
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_4():
    """
    partadm test run: boot_start_option_4
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --blockinfo"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_5():
    """
    partadm test run: boot_start_option_5
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --clean_block"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_6():
    """
    partadm test run: boot_start_option_6
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive --blockinfo"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_start_option_7():
    """
    partadm test run: boot_start_option_7
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive --clean_block"""

    cmdout    = \
"""Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

RESUME_BOOTING

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_1():
    """
    partadm test run: boot_status_option_1
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_2():
    """
    partadm test run: boot_status_option_2
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status ANL-R00-M0-512"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_3():
    """
    partadm test run: boot_status_option_3
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children_list': '*'}]

BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_4():
    """
    partadm test run: boot_status_option_4
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --blockinfo"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_5():
    """
    partadm test run: boot_status_option_5
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --clean_block"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_6():
    """
    partadm test run: boot_status_option_6
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive --blockinfo"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_status_option_7():
    """
    partadm test run: boot_status_option_7
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive --clean_block"""

    cmdout    = \
"""Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

BOOTING_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_list_io_1():
    """
    partadm test run: list_io_1

    """

    args      = """--list_io"""

    cmdout    = \
"""Name  Size  State  CS Status  BlockComputes  Autoreboot
=========================================================
P1    0     idle   OK               x        x         
P2    1     idle   OK               x        x         
P3    2     idle   OK               x        x         
P4    3     idle   OK               x        x         
P5    4     idle   OK               x        x         
P6    5     idle   OK               x        x         
P7    6     idle   OK               x        x         
P8    7     idle   OK               x        x         
P9    8     idle   OK               x        x         
P10   9     idle   OK               x        x         
"""

    stubout   = \
"""
GET_IO_BLOCKS

plist: [{'status': '*', 'name': '*', 'state': '*', 'autoreboot': '*', 'block_computes_for_reboot': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_list_io_2():
    """
    partadm test run: list_io_2

    """

    args      = """--list_io ANL-R00-M0-512 ANL-R00-M1-512"""

    cmdout    = \
"""Name  Size  State  CS Status  BlockComputes  Autoreboot
=========================================================
P1    0     idle   OK               x        x         
P2    1     idle   OK               x        x         
P3    2     idle   OK               x        x         
P4    3     idle   OK               x        x         
P5    4     idle   OK               x        x         
P6    5     idle   OK               x        x         
P7    6     idle   OK               x        x         
P8    7     idle   OK               x        x         
P9    8     idle   OK               x        x         
P10   9     idle   OK               x        x         
"""

    stubout   = \
"""
GET_IO_BLOCKS

plist: [{'status': '*', 'name': '*', 'state': '*', 'autoreboot': '*', 'block_computes_for_reboot': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_list_io_3():
    """
    partadm test run: list_io_3

    """

    args      = """-i"""

    cmdout    = \
"""Name  Size  State  CS Status  BlockComputes  Autoreboot
=========================================================
P1    0     idle   OK               x        x         
P2    1     idle   OK               x        x         
P3    2     idle   OK               x        x         
P4    3     idle   OK               x        x         
P5    4     idle   OK               x        x         
P6    5     idle   OK               x        x         
P7    6     idle   OK               x        x         
P8    7     idle   OK               x        x         
P9    8     idle   OK               x        x         
P10   9     idle   OK               x        x         
"""

    stubout   = \
"""
GET_IO_BLOCKS

plist: [{'status': '*', 'name': '*', 'state': '*', 'autoreboot': '*', 'block_computes_for_reboot': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_io_block_1():
    """
    partadm test run: add_io_block_1

    """

    args      = """--add_io_block"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_io_block_2():
    """
    partadm test run: add_io_block_2

    """

    args      = """--add_io_block ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout   = \
"""
ADD_IO_BLOCKS

user name: gooduser
name:ANL-R00-M0-512
name type: <type 'str'>
name:ANL-R00-M1-512
name type: <type 'str'>
name:ANL-R01-M0-512
name type: <type 'str'>
name:ANL-R00-M0-512
name type: <type 'str'>
name:ANL-R00-M1-512
name type: <type 'str'>
name:ANL-R01-M0-512
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_del_io_block_1():
    """
    partadm test run: del_io_block_1

    """

    args      = """--del_io_block"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_del_io_block_2():
    """
    partadm test run: del_io_block_2

    """

    args      = """--del_io_block ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout   = \
"""
DEL_IO_BLOCKS

user name: gooduser
name:ANL-R00-M0-512
name type: <type 'str'>
name:ANL-R00-M1-512
name type: <type 'str'>
name:ANL-R01-M0-512
name type: <type 'str'>
name:ANL-R00-M0-512
name type: <type 'str'>
name:ANL-R00-M1-512
name type: <type 'str'>
name:ANL-R01-M0-512
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_io_block_1():
    """
    partadm test run: boot_io_block_1

    """

    args      = """--boot_io_block"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_boot_io_block_2():
    """
    partadm test run: boot_io_block_2

    """

    args      = """--boot_io_block ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""IO Boot initiated on ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512
"""

    stubout   = \
"""
INITIATE_IO_BOOT

whoami: gooduser
tag: partadm, type = <type 'str'>
parts: ['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_free_io_block_1():
    """
    partadm test run: free_io_block_1

    """

    args      = """--free_io_block"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_free_io_block_2():
    """
    partadm test run: free_io_block_2

    """

    args      = """--free_io_block ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""IO Free initiated on ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512
"""

    stubout   = \
"""
INITIATE_IO_BOOT

whoami: gooduser
force: False, type = <type 'bool'>
parts: ['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_set_io_autoboot_1():
    """
    partadm test run: set_io_autoboot_1

    """

    args      = """--set_io_autoboot"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_set_io_autoboot_2():
    """
    partadm test run: set_io_autoboot_2

    """

    args      = """--set_io_autoboot ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""Autoreboot flag set for IO Blocks: ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512
"""

    stubout   = \
"""
SET_AUTOREBOOT

whoami: gooduser
parts: ['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unset_io_autoboot_1():
    """
    partadm test run: unset_io_autoboot_1

    """

    args      = """--unset_io_autoboot"""

    cmdout    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unset_io_autoboot_2():
    """
    partadm test run: unset_io_autoboot_2

    """

    args      = """--unset_io_autoboot ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""Autoreboot flag unset for IO Blocks: ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512
"""

    stubout   = \
"""
UNSET_AUTOREBOOT

whoami: gooduser
parts: ['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_start_1():
    """
    partadm test run: io_autoboot_start_1

    """

    args      = """--io_autoboot_start"""

    cmdout    = \
"""IO Block autoreboot enabled.
"""

    stubout   = \
"""
ENABLE_IO_AUTOREBOOT

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_start_2():
    """
    partadm test run: io_autoboot_start_2

    """

    args      = """--io_autoboot_start ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""IO Block autoreboot enabled.
"""

    stubout   = \
"""
ENABLE_IO_AUTOREBOOT

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_stop_1():
    """
    partadm test run: io_autoboot_stop_1

    """

    args      = """--io_autoboot_stop"""

    cmdout    = \
"""IO Block autoreboot disabled.
"""

    stubout   = \
"""
DISABLE_IO_AUTOREBOOT

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_stop_2():
    """
    partadm test run: io_autoboot_stop_2

    """

    args      = """--io_autoboot_stop ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""IO Block autoreboot disabled.
"""

    stubout   = \
"""
DISABLE_IO_AUTOREBOOT

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_status_1():
    """
    partadm test run: io_autoboot_status_1

    """

    args      = """--io_autoboot_status"""

    cmdout    = \
"""IO Block autoreboot: ENABLED
"""

    stubout   = \
"""
GET_IO_AUTOREBOOT_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_io_autoboot_status_2():
    """
    partadm test run: io_autoboot_status_2

    """

    args      = """--io_autoboot_status ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = \
"""IO Block autoreboot: ENABLED
"""

    stubout   = \
"""
GET_IO_AUTOREBOOT_STATUS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

