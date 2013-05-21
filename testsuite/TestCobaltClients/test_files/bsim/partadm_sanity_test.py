import testutils

# ---------------------------------------------------------------------------------
def test_partadm_version_option():
    """
    partadm test run: version_option

        Command Output:
          version: "partadm.py " + $Revision: 1981 $ + , Cobalt  + $Version$
          

    """

    args      = """--version"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_help_option_1():
    """
    partadm test run: help_option_1

        Command Output:
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

    args      = """-h"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_help_option_2():
    """
    partadm test run: help_option_2

        Command Output:
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

    args      = """--help"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_no_arg_1():
    """
    partadm test run: no_arg_1

        Command Output:
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b.
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          

    """

    args      = ''
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_no_arg_2():
    """
    partadm test run: no_arg_2

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """-a"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_debug():
    """
    partadm test run: debug

        Command Output:
          
          partadm.py --debug
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b.
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          

    """

    args      = """--debug"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_1():
    """
    partadm test run: combo_options_1

        Command Output:
          Option combinations not allowed with: delete option(s)
          

    """

    args      = """-a -d PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_2():
    """
    partadm test run: combo_options_2

        Command Output:
          Option combinations not allowed with: enable option(s)
          

    """

    args      = """-a --enable PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_3():
    """
    partadm test run: combo_options_3

        Command Output:
          Option combinations not allowed with: enable option(s)
          

    """

    args      = """-d --enable PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_4():
    """
    partadm test run: combo_options_4

        Command Output:
          Option combinations not allowed with: disable option(s)
          

    """

    args      = """--enable --disable PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_5():
    """
    partadm test run: combo_options_5

        Command Output:
          Option combinations not allowed with: deactivate option(s)
          

    """

    args      = """--deactivate --activate PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_6():
    """
    partadm test run: combo_options_6

        Command Output:
          Option combinations not allowed with: deactivate option(s)
          

    """

    args      = """-a --deactivate PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_7():
    """
    partadm test run: combo_options_7

        Command Output:
          Option combinations not allowed with: unfail option(s)
          

    """

    args      = """--fail --unfail PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_8():
    """
    partadm test run: combo_options_8

        Command Output:
          Option combinations not allowed with: savestate option(s)
          

    """

    args      = """--savestate /tmp/savestate -a"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_9():
    """
    partadm test run: combo_options_9

        Command Output:
          Option combinations not allowed with: list_blocks option(s)
          

    """

    args      = """-l --xml"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_10():
    """
    partadm test run: combo_options_10

        Command Output:
          Option combinations not allowed with: list_blocks option(s)
          

    """

    args      = """-l --xml"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_11():
    """
    partadm test run: combo_options_11

        Command Output:
          Option combinations not allowed with: queue option(s)
          

    """

    args      = """-a --queue q1 PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_12():
    """
    partadm test run: combo_options_12

        Command Output:
          Option combinations not allowed with: dump option(s)
          

    """

    args      = """--dump --queue q1 PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_13():
    """
    partadm test run: combo_options_13

        Command Output:
          Option combinations not allowed with: savestate option(s)
          

    """

    args      = """--savestate /tmp/s --xml"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_combo_options_14():
    """
    partadm test run: combo_options_14

        Command Output:
          Option combinations not allowed with: blockinfo, clean_block option(s)
          

    """

    args      = """-a -c -b PART"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_add_option_1():
    """
    partadm test run: add_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """-a -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_add_option_2():
    """
    partadm test run: add_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """-a --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_add_option_3():
    """
    partadm test run: add_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """-a PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_delete_option_1():
    """
    partadm test run: delete_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """-d -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_delete_option_2():
    """
    partadm test run: delete_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """-d --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_delete_option_3():
    """
    partadm test run: delete_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """-d PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_enable_option_1():
    """
    partadm test run: enable_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--enable -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_enable_option_2():
    """
    partadm test run: enable_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--enable --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_enable_option_3():
    """
    partadm test run: enable_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--enable PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_disable_option_1():
    """
    partadm test run: disable_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--disable -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_disable_option_2():
    """
    partadm test run: disable_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--disable --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_disable_option_3():
    """
    partadm test run: disable_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--disable PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_activate_option_1():
    """
    partadm test run: activate_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--activate -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_activate_option_2():
    """
    partadm test run: activate_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--activate --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_activate_option_3():
    """
    partadm test run: activate_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--activate PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_1():
    """
    partadm test run: deactivate_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--deactivate -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_2():
    """
    partadm test run: deactivate_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--deactivate --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_3():
    """
    partadm test run: deactivate_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--deactivate PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_fail_option_1():
    """
    partadm test run: fail_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--fail -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_fail_option_2():
    """
    partadm test run: fail_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--fail --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_fail_option_3():
    """
    partadm test run: fail_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--fail PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_1():
    """
    partadm test run: unfail_option_1

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--unfail -r PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_2():
    """
    partadm test run: unfail_option_2

        Command Output:
          ['PART', 'a']
          

    """

    args      = """--unfail --recursive PART"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_3():
    """
    partadm test run: unfail_option_3

        Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--unfail PART1 PART2 PART3"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_1():
    """
    partadm test run: savestate_option_1

        Command Output:
          directory /bad/save does not exist
          

    """

    args      = """--savestate /bad/save"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_2():
    """
    partadm test run: savestate_option_2

        Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--savestate /tmp/save p1"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_3():
    """
    partadm test run: savestate_option_3

        Command Output:
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

    args      = """--savestate"""
    exp_rs    = 512

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_queue_option_1():
    """
    partadm test run: queue_option_1

        Command Output:
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

    args      = """--queue"""
    exp_rs    = 512

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_queue_option_2():
    """
    partadm test run: queue_option_2

        Command Output:
          'q1' is not an existing queue
          'q2' is not an existing queue
          

    """

    args      = """--queue q1:q2 p1 p2 p3"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_dump_option_1():
    """
    partadm test run: dump_option_1

        Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_dump_option_2():
    """
    partadm test run: dump_option_2

        Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump p1"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_dump_option_3():
    """
    partadm test run: dump_option_3

        Command Output:
          [{'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'P1', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'P2', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'P3', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'P4', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'P5', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'P6', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'P7', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'P8', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'P9', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}, {'scheduled': True, 'status': 'OK', 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'P10', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c'], 'block_computes_for_reboot': True, 'autoreboot': True}]
          

    """

    args      = """--dump --recursive p1"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_add_io_block_1():
    """
    partadm test run: add_io_block_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--add_io_block"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_del_io_block_1():
    """
    partadm test run: del_io_block_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--del_io_block"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_boot_io_block_1():
    """
    partadm test run: boot_io_block_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--boot_io_block"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_free_io_block_1():
    """
    partadm test run: free_io_block_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--free_io_block"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_set_io_autoboot_1():
    """
    partadm test run: set_io_autoboot_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--set_io_autoboot"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_partadm_unset_io_autoboot_1():
    """
    partadm test run: unset_io_autoboot_1

        Command Output:
          At least one partition must be supplied
          

    """

    args      = """--unset_io_autoboot"""
    exp_rs    = 256

    results = testutils.run_cmd('partadm.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg
