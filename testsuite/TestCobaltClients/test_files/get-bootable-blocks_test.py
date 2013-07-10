import testutils

# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_arg_1():
    """
    get-bootable-blocks test run: arg_1

    """

    args      = ''

    cmdout    = \
"""Usage: get-bootable-blocks.py [options] <block location>

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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_arg_2():
    """
    get-bootable-blocks test run: arg_2

    """

    args      = """arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_size_1():
    """
    get-bootable-blocks test run: size_1

    """

    args      = """--size 1024"""

    cmdout    = \
"""Usage: get-bootable-blocks.py [options] <block location>

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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_size_2():
    """
    get-bootable-blocks test run: size_2

    """

    args      = """--size 1024 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_1():
    """
    get-bootable-blocks test run: geometry_1

    """

    args      = """--geometry 1              arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_2():
    """
    get-bootable-blocks test run: geometry_2

    """

    args      = """--geometry geo            arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_3():
    """
    get-bootable-blocks test run: geometry_3

    """

    args      = """--geometry 90x90x90x90x90 arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_4():
    """
    get-bootable-blocks test run: geometry_4

    """

    args      = """--geometry 90x90x90x90    arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_5():
    """
    get-bootable-blocks test run: geometry_5

    """

    args      = """--geometry -9x90x90x90x2  arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_6():
    """
    get-bootable-blocks test run: geometry_6

    """

    args      = """--geometry 9x10x11x12x2   arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_7():
    """
    get-bootable-blocks test run: geometry_7

    """

    args      = """--geometry 90x90x90x90x1  arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_8():
    """
    get-bootable-blocks test run: geometry_8

    """

    args      = """--geometry 90x90x90x90x2  arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_9():
    """
    get-bootable-blocks test run: geometry_9

    """

    args      = """--geometry 90x90x90x90x3  arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_10():
    """
    get-bootable-blocks test run: geometry_10

    """

    args      = """--geometry 90x90x90x90x11 arg"""

    cmdout    = ''

    cmderr    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_11():
    """
    get-bootable-blocks test run: geometry_11

    """

    args      = """--geometry 99x99x99x99x2  arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_12():
    """
    get-bootable-blocks test run: geometry_12

    """

    args      = """--geometry 00x00x00x00x2  arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_13():
    """
    get-bootable-blocks test run: geometry_13

    """

    args      = """--geometry 100x00x00x00x2 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_14():
    """
    get-bootable-blocks test run: geometry_14

    """

    args      = """--geometry 00x100x00x00x2 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_15():
    """
    get-bootable-blocks test run: geometry_15

    """

    args      = """--geometry 00x00x100x00x2 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_16():
    """
    get-bootable-blocks test run: geometry_16

    """

    args      = """--geometry 00x00x00x100x2 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_combo():
    """
    get-bootable-blocks test run: combo

    """

    args      = """--geometry 00x00x00x00x2 --size 2048 arg"""

    cmdout    = ''

    cmderr    = \
"""component error: Following exception while trying to excecute system.get_idle_blocks: global name 'queue_size' is not defined

"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_help_1():
    """
    get-bootable-blocks test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: get-bootable-blocks.py [options] <block location>

Options:
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  -d, --debug          turn on communication debugging
  --size=QUERY_SIZE    Constrain blocks to a particular nodecount
  --geometry=GEO_LIST  Constrain blocks to a particular geometry
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_help_2():
    """
    get-bootable-blocks test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""Usage: get-bootable-blocks.py [options] <block location>

Options:
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  -d, --debug          turn on communication debugging
  --size=QUERY_SIZE    Constrain blocks to a particular nodecount
  --geometry=GEO_LIST  Constrain blocks to a particular geometry
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_version():
    """
    get-bootable-blocks test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "get-bootable-blocks.py " + TBD + , Cobalt  + TBD
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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_debug():
    """
    get-bootable-blocks test run: debug

    """

    args      = """--debug"""

    cmdout    = \
"""Usage: get-bootable-blocks.py [options] <block location>

"""

    cmderr    = \
"""
get-bootable-blocks.py --debug

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

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

