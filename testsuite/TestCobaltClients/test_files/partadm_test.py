import testutils

# ---------------------------------------------------------------------------------
def test_partadm_version_option():
    """
    partadm test run: version_option

    """

    args      = """--version"""

    cmdout    = \
"""version: "partadm.py " + $Revision: 1981 $ + , Cobalt  + $Version$
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-h"""

    cmdout    = \
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--help"""

    cmdout    = \
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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


"""

    cmderr    = \
"""No arguments or options provided

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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


"""

    cmderr    = \
"""
partadm.py --debug

No arguments or options provided

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: delete option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: disable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: unfail option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: add, blockinfo, clean_block option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""WARNING: IO Block information only exists on BG/Q-type systems.
"""

    stubout   = \
"""
ADD_PARTITION

user name: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""WARNING: IO Block information only exists on BG/Q-type systems.
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: rmq, list_io, rmq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: appq, list_io, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: rmq, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-a -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
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
name:c
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
name:d
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
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:b
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
name:c
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
name:d
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-a --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
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
name:c
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
name:d
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
deps:[]
deps type: <type 'list'>
functional:False
functional type: <type 'bool'>
name:b
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
name:c
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
name:d
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-a ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-a -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-d -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-d --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-d ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-d -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--enable -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--enable --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--enable ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--enable -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--disable -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--disable --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--disable ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--disable -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--activate -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--activate --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--activate ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--activate -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--deactivate -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--deactivate --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
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
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--deactivate ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--deactivate -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--fail -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}, {'tag': 'partition', 'name': 'b'}, {'tag': 'partition', 'name': 'c'}, {'tag': 'partition', 'name': 'd'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--fail --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

FAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}, {'tag': 'partition', 'name': 'b'}, {'tag': 'partition', 'name': 'c'}, {'tag': 'partition', 'name': 'd'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--fail ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--fail -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--unfail -r ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}, {'tag': 'partition', 'name': 'b'}, {'tag': 'partition', 'name': 'c'}, {'tag': 'partition', 'name': 'd'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--unfail --recursive ANL-R00-R01-2048"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'a', 'b', 'c', 'd']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048', 'children': '*'}]

UNFAIL_PARTITION

user name: gooduser
part list: [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}, {'tag': 'partition', 'name': 'a'}, {'tag': 'partition', 'name': 'b'}, {'tag': 'partition', 'name': 'c'}, {'tag': 'partition', 'name': 'd'}]
name:ANL-R00-R01-2048
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:a
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:b
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:c
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
name:d
name type: <type 'str'>
tag:partition
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--unfail ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : ANL-R00-R01-2048
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : ANL-R00-1024
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

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

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-R01-2048', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'ANL-R00-1024', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--unfail -c ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--savestate /bad/save"""

    cmdout    = ''

    cmderr    = \
"""directory /bad/save does not exist
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--savestate /tmp/save ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--savestate"""

    cmdout    = ''

    cmderr    = \
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--savestate /tmp/save -c ANL-R00-M0-512"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 2
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 3
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 4
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 5
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 6
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 7
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 8
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 9
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--xml"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--xml ANL-R00-M0-512"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--xml --recursive ANL-R00-M0-512"""

    cmdout    = \
"""['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]

GENERATE_XML

name:*
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : P1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : P2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 2
    name                      : P3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 3
    name                      : P4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 4
    name                      : P5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 5
    name                      : P6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 6
    name                      : P7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 7
    name                      : P8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 8
    name                      : P9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 9
    name                      : P10
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

    stubout   = \
"""
GENERATE_XML

name:*
name type: <type 'str'>

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P1', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P2', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P3', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P4', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P5', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P6', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P7', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P8', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P9', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P10', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--xml --clean_block"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : P1
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : P2
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 2
    name                      : P3
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 3
    name                      : P4
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 4
    name                      : P5
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 5
    name                      : P6
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 6
    name                      : P7
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 7
    name                      : P8
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 8
    name                      : P9
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 9
    name                      : P10
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []

GENERATE_XML

name:*
name type: <type 'str'>

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P1', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P2', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P3', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P4', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P5', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P6', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P7', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P8', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P9', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': 'P10', 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--xml --recursive --clean_block"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []

GENERATE_XML

name:*
name type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--queue"""

    cmdout    = ''

    cmderr    = \
"""Usage: partadm.py --help
Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--queue q_4:q_3 ANL-R00-M0-512 ANL-R00-M1-512 ANL-R01-M0-512"""

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R00-M0-512"""

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--queue q_1 -c ANL-R00-M0-512"""

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""'q_1' is not an existing queue
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--queue q_2 -r -c ANL-R00-M0-512"""

    cmdout    = ''

    cmderr    = \
"""'q_2' is not an existing queue
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: appq, clean_block, appq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: rmq, clean_block, rmq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--dump"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--dump ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--dump --recursive ANL-R00-M0-512"""

    cmdout    = \
"""[{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 2
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 3
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 4
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 5
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 6
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 7
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 8
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 9
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--dump --clean_block"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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
"""scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 0
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : kebra
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 1
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : jello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 2
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bello
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 3
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : aaa
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 4
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : bbb
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 5
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : hhh
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 6
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : dito
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 7
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : myq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 8
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : yours
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

scheduled: True
    status                    : OK
    functional                : True
    draining                  : False
    passthrough_blocks        : ['A']
    children                  : ['a', 'b', 'c', 'd']
    size                      : 9
    name                      : {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}
    node_geometry             : ['48', '48', '48', '48', '48']
    state                     : idle
    queue                     : zq
    relatives                 : ['b']
    parents                   : ['a', 'b', 'c']
    block_computes_for_reboot : True
    autoreboot                : True

"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}, {'scheduled': '*', 'freeing': '*', 'funcitonal': '*', 'block_type': '*', 'name': {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a', 'b', 'c', 'd'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, 'backfill_time': '*', 'used_by': '*', 'reserved_by': '*', 'state': '*', 'draining': '*', 'queue': '*', 'wiring_conflicts': '*', 'node_card_list': '*', 'parents': '*', 'size': '*', 'wire_list': '*', 'cleanup_pending': '*', 'switch_list': '*', 'children': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--dump --recursive --clean_block"""

    cmdout    = \
"""Force clenaing not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop --recursive --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-stop --recursive --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start --recursive --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-start --recursive --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status --recursive ANL-R00-M0-512"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'ANL-R00-M0-512', 'children': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status --recursive --blockinfo"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--boot-status --recursive --clean_block"""

    cmdout    = \
"""Boot control not available for BG/P systems
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: []
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""WARNING: IO Block information only exists on BG/Q-type systems.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""WARNING: IO Block information only exists on BG/Q-type systems.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""WARNING: IO Block information only exists on BG/Q-type systems.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

    stubout   = \
"""
INITIATE_IO_BOOT

whoami: gooduser
parts: ['ANL-R00-M0-512', 'ANL-R00-M1-512', 'ANL-R01-M0-512']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
"""At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    cmdout    = ''

    cmderr    = \
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

