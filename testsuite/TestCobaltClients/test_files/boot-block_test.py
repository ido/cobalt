import testutils

# ---------------------------------------------------------------------------------
def test_boot_block_combo():
    """
    boot-block test run: combo

    """

    args      = """--free --reboot --block b --jobid 1"""

    cmdout    = ''

    cmderr    = \
"""ERROR: --free may not be specified with --reboot.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_1():
    """
    boot-block test run: free_1

    """

    args      = """--free"""

    cmdout    = ''

    cmderr    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_2():
    """
    boot-block test run: free_2

    """

    args      = """--free --jobid 1"""

    cmdout    = ''

    cmderr    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_free_3():
    """
    boot-block test run: free_3

    """

    args      = """--free --jobid 1 --block b"""

    cmdout    = \
"""Block free on b initiated.
Block b successfully freed.
"""

    cmderr    = ''

    stubout   = \
"""
INITIATE_PROXY_FREE

block: b, type = <type 'str'>
user: gooduser
jobid: 1, type = <type 'int'>

GET_BLOCK_BGSCHED_STATUS

block: b, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_1():
    """
    boot-block test run: reboot_1

    """

    args      = """--reboot"""

    cmdout    = ''

    cmderr    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_2():
    """
    boot-block test run: reboot_2

    """

    args      = """--reboot --jobid 1"""

    cmdout    = ''

    cmderr    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_reboot_3():
    """
    boot-block test run: reboot_3

    """

    args      = """--reboot --jobid 1 --block b"""

    cmdout    = \
"""Block free on b initiated.
Block b successfully freed.
status 1
status 2
status 3
Boot for location b complete.
"""

    cmderr    = ''

    stubout   = \
"""
INITIATE_PROXY_FREE

block: b, type = <type 'str'>
user: gooduser
jobid: 1, type = <type 'int'>

GET_BLOCK_BGSCHED_STATUS

block: b, type = <type 'str'>

INITIATE_PROXY_BOOT

block: b, type = <type 'str'>
user: gooduser
jobid: 1, type = <type 'int'>

GET_BOOT_STATUSES_AND_STRINGS

block: b, type = <type 'str'>

GET_BOOT_STATUSES_AND_STRINGS

block: b, type = <type 'str'>

REAP_BOOT

block: b, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_1():
    """
    boot-block test run: nofree_noreboot_1

    """

    args      = """--jobid 1"""

    cmdout    = ''

    cmderr    = \
"""ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_2():
    """
    boot-block test run: nofree_noreboot_2

    """

    args      = """--block b"""

    cmdout    = ''

    cmderr    = \
"""ERROR: Cobalt jobid not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_nofree_noreboot_3():
    """
    boot-block test run: nofree_noreboot_3

    """

    args      = """--jobid 1 --block b"""

    cmdout    = \
"""status 1
status 2
status 3
Boot for location b complete.
"""

    cmderr    = ''

    stubout   = \
"""
INITIATE_PROXY_BOOT

block: b, type = <type 'str'>
user: gooduser
jobid: 1, type = <type 'int'>

GET_BOOT_STATUSES_AND_STRINGS

block: b, type = <type 'str'>

GET_BOOT_STATUSES_AND_STRINGS

block: b, type = <type 'str'>

REAP_BOOT

block: b, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_help_1():
    """
    boot-block test run: help_1

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

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_help_2():
    """
    boot-block test run: help_2

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

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_version():
    """
    boot-block test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "boot-block.py " + TBD + , Cobalt  + $Version$
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

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_debug_1():
    """
    boot-block test run: debug_1

    """

    args      = """--debug"""

    cmdout    = ''

    cmderr    = \
"""
boot-block.py --debug

ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_boot_block_debug_2():
    """
    boot-block test run: debug_2

    """

    args      = """--d"""

    cmdout    = ''

    cmderr    = \
"""
boot-block.py --d

ERROR: block not specified as option or in environment.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       768, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('boot-block.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

