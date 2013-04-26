import testutils

# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_arg_1():
    """
    get-bootable-blocks test run: arg_1
        Old Command Output:
          Must specify a block location for search
          

    """

    args      = ''

    cmdout    = \
"""Must specify a block location for search
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_arg_2():
    """
    get-bootable-blocks test run: arg_2
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_size_1():
    """
    get-bootable-blocks test run: size_1
        Old Command Output:
          Must specify a block location for search
          

    """

    args      = """--size 1024"""

    cmdout    = \
"""Must specify a block location for search
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_size_2():
    """
    get-bootable-blocks test run: size_2
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--size 1024 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: 1024
geoometry: 
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_1():
    """
    get-bootable-blocks test run: geometry_1
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry 1              arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_2():
    """
    get-bootable-blocks test run: geometry_2
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry geo            arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_3():
    """
    get-bootable-blocks test run: geometry_3
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry 90x90x90x90x90 arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_4():
    """
    get-bootable-blocks test run: geometry_4
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry 90x90x90x90    arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_5():
    """
    get-bootable-blocks test run: geometry_5
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry -9x90x90x90x2  arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_6():
    """
    get-bootable-blocks test run: geometry_6
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 9x10x11x12x2   arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 9x10x11x12x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_7():
    """
    get-bootable-blocks test run: geometry_7
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 90x90x90x90x1  arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 90x90x90x90x1
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_8():
    """
    get-bootable-blocks test run: geometry_8
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 90x90x90x90x2  arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 90x90x90x90x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_9():
    """
    get-bootable-blocks test run: geometry_9
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry 90x90x90x90x3  arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_10():
    """
    get-bootable-blocks test run: geometry_10
        Old Command Output:
          Invalid Geometry. Geometry must be in the form of AxBxCxDxE
          

    """

    args      = """--geometry 90x90x90x90x11 arg"""

    cmdout    = \
"""Invalid Geometry. Geometry must be in the form of AxBxCxDxE
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_11():
    """
    get-bootable-blocks test run: geometry_11
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 99x99x99x99x2  arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 99x99x99x99x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_12():
    """
    get-bootable-blocks test run: geometry_12
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 00x00x00x00x2  arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 0x0x0x0x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_13():
    """
    get-bootable-blocks test run: geometry_13
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 100x00x00x00x2 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 100x0x0x0x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_14():
    """
    get-bootable-blocks test run: geometry_14
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 00x100x00x00x2 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 0x100x0x0x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_15():
    """
    get-bootable-blocks test run: geometry_15
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 00x00x100x00x2 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 0x0x100x0x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_geometry_16():
    """
    get-bootable-blocks test run: geometry_16
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 00x00x00x100x2 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: None
geoometry: 0x0x0x100x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_combo():
    """
    get-bootable-blocks test run: combo
        Old Command Output:
          I1
          I2
          I3
          I4
          I5
          

    """

    args      = """--geometry 00x00x00x00x2 --size 2048 arg"""

    cmdout    = \
"""I1
I2
I3
I4
I5
"""

    stubout   = \
"""
GET_IDLE_BLOCKS

block location: arg
query size: 2048
geoometry: 0x0x0x0x2
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_help_1():
    """
    get-bootable-blocks test run: help_1
        Old Command Output:
          Usage: get-bootable-blocks.py [options]
          
          Options:
            -h, --help           show this help message and exit
            --size=BLOCK_SIZE    Constrain blocks to a particular nodecount
            --geometry=GEOMETRY  Constrain blocks to a particular geometry
          

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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_help_2():
    """
    get-bootable-blocks test run: help_2
        Old Command Output:
          Usage: get-bootable-blocks.py [options]
          
          Options:
            -h, --help           show this help message and exit
            --size=BLOCK_SIZE    Constrain blocks to a particular nodecount
            --geometry=GEOMETRY  Constrain blocks to a particular geometry
          

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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_version():
    """
    get-bootable-blocks test run: version
        Old Command Output:
          Usage: get-bootable-blocks.py [options]
          
          get-bootable-blocks.py: error: no such option: --version
          

    """

    args      = """--version"""

    cmdout    = \
"""version: "get-bootable-blocks.py " + TBD + , Cobalt  + TBD
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_get_bootable_blocks_debug():
    """
    get-bootable-blocks test run: debug

    """

    args      = """--debug"""

    cmdout    = \
"""
get-bootable-blocks.py --debug

Must specify a block location for search
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('get-bootable-blocks.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

