import testutils

# ---------------------------------------------------------------------------------
def test_boot_block_combo():
    """
    boot-block test run: combo
        Old Command Output:
          ERROR: --free may not be specified with --reboot.
          

    """

    args      = """--free --reboot --block b --jobid 1"""

    cmdout    = \
"""ERROR: --free may not be specified with --reboot.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_1():
    """
    boot-block test run: free_1
        Old Command Output:
          ERROR: block not specified as option or in environment.
          

    """

    args      = """--free"""

    cmdout    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_2():
    """
    boot-block test run: free_2
        Old Command Output:
          ERROR: block not specified as option or in environment.
          

    """

    args      = """--free --jobid 1"""

    cmdout    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_3():
    """
    boot-block test run: free_3
        Old Command Output:
          Block free on b initiated.
          Block b successfully freed.
          

    """

    args      = """--free --jobid 1 --block b"""

    cmdout    = \
"""Block free on b initiated.
Block b successfully freed.
"""

    stubout   = \
"""
INITIATE_PROXY_FREE

block: b
user: gooduser
jobid: 1

GET_BLOCK_BGSCHED_STATUS

block: b
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_1():
    """
    boot-block test run: reboot_1
        Old Command Output:
          ERROR: block not specified as option or in environment.
          

    """

    args      = """--reboot"""

    cmdout    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_2():
    """
    boot-block test run: reboot_2
        Old Command Output:
          ERROR: block not specified as option or in environment.
          

    """

    args      = """--reboot --jobid 1"""

    cmdout    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_3():
    """
    boot-block test run: reboot_3
        Old Command Output:
          Block free on b initiated.
          Block b successfully freed.
          status 1
          status 2
          status 3
          Boot for locaiton b complete.
          

    """

    args      = """--reboot --jobid 1 --block b"""

    cmdout    = \
"""Block free on b initiated.
Block b successfully freed.
Boot for locaiton b complete.
status 1
status 2
status 3
"""

    stubout   = \
"""
INITIATE_PROXY_FREE

block: b
user: gooduser
jobid: 1

GET_BLOCK_BGSCHED_STATUS

block: b

INITIATE_PROXY_BOOT

block: b
user: gooduser
jobid: 1

GET_BOOT_STATUSES_AND_STRINGS

block: b

GET_BOOT_STATUSES_AND_STRINGS

block: b

REAP_BOOT

block: b
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_1():
    """
    boot-block test run: nofree_noreboot_1
        Old Command Output:
          ERROR: block not specified as option or in environment.
          

    """

    args      = """--jobid 1"""

    cmdout    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_2():
    """
    boot-block test run: nofree_noreboot_2
        Old Command Output:
          ERROR: Cobalt jobid not specified as option or in environment.
          

    """

    args      = """--block b"""

    cmdout    = \
"""ERROR: Cobalt jobid not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_3():
    """
    boot-block test run: nofree_noreboot_3
        Old Command Output:
          status 1
          status 2
          status 3
          Boot for locaiton b complete.
          

    """

    args      = """--jobid 1 --block b"""

    cmdout    = \
"""Boot for locaiton b complete.
status 1
status 2
status 3
"""

    stubout   = \
"""
INITIATE_PROXY_BOOT

block: b
user: gooduser
jobid: 1

GET_BOOT_STATUSES_AND_STRINGS

block: b

GET_BOOT_STATUSES_AND_STRINGS

block: b

REAP_BOOT

block: b
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_help_1():
    """
    boot-block test run: help_1
        Old Command Output:
          Usage: Instruct Cobalt's system component to boot a block on your behalf.
          
          Options:
            --version      show program's version number and exit
            -h, --help     show this help message and exit
            --block=BLOCK  Name of block to boot.
            --reboot       If the block is already booted, free the block and reboot.
            --free         Free the block, if booted.  May not be combined with reboot
            --jobid=JOBID  Specify a cobalt jobid for this boot.
          

    """

    args      = """--help"""

    cmdout    = \
"""Usage: boot-block.py [options]

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -d, --debug    turn on communication debugging
  --block=BLOCK  Name of block to boot.
  --reboot       If the block is already booted, free the block and reboot.
  --free         Free the block, if booted.  May not be combined with reboot
  --jobid=JOBID  Specify a cobalt jobid for this boot.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_help_2():
    """
    boot-block test run: help_2
        Old Command Output:
          Usage: Instruct Cobalt's system component to boot a block on your behalf.
          
          Options:
            --version      show program's version number and exit
            -h, --help     show this help message and exit
            --block=BLOCK  Name of block to boot.
            --reboot       If the block is already booted, free the block and reboot.
            --free         Free the block, if booted.  May not be combined with reboot
            --jobid=JOBID  Specify a cobalt jobid for this boot.
          

    """

    args      = """-h"""

    cmdout    = \
"""Usage: boot-block.py [options]

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -d, --debug    turn on communication debugging
  --block=BLOCK  Name of block to boot.
  --reboot       If the block is already booted, free the block and reboot.
  --free         Free the block, if booted.  May not be combined with reboot
  --jobid=JOBID  Specify a cobalt jobid for this boot.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_version():
    """
    boot-block test run: version
        Old Command Output:
          $Version$
          

    """

    args      = """--version"""

    cmdout    = \
"""version: "boot-block.py " + TBD + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_debug_1():
    """
    boot-block test run: debug_1

    """

    args      = """--debug"""

    cmdout    = \
"""
boot-block.py --debug

ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_debug_2():
    """
    boot-block test run: debug_2

    """

    args      = """--d"""

    cmdout    = \
"""
boot-block.py --d

ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

