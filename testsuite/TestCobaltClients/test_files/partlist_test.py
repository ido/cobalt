import testutils

# ---------------------------------------------------------------------------------
def test_partlist_version_option_1():
    """
    partlist test run: version_option_1
        Old Command Output:
          partlist $Revision: 1981 $
          cobalt $Version$
          

    """

    args      = """--version"""

    cmdout    = \
"""
partlist.py --version

version: "partlist.py " + $Revision: 1981 $ + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_version_option_2():
    """
    partlist test run: version_option_2
        Old Command Output:
          partlist $Revision: 1981 $
          cobalt $Version$
          

    """

    args      = """-v"""

    cmdout    = \
"""
partlist.py -v

Usage: partlist.py [options] 

partlist.py: error: no such option: -v
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

    """

    args      = """-h"""

    cmdout    = \
"""
partlist.py -h

Usage: partlist.py [options] 

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

    """

    args      = """--help"""

    cmdout    = \
"""
partlist.py --help

Usage: partlist.py [options] 

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_invalid():
    """
    partlist test run: invalid

    """

    args      = """-k"""

    cmdout    = \
"""
partlist.py -k

Usage: partlist.py [options] 

partlist.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_argument_1():
    """
    partlist test run: argument_1

    """

    args      = """arg"""

    cmdout    = \
"""
partlist.py arg

No arguments required
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_argument_2():
    """
    partlist test run: argument_2
        Old Command Output:
          Name  Queue                                                  State  Backfill  Geometry      
          ==============================================================================================
          P10   zq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq     idle   -         48x48x48x48x48
          P9    yours:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
          P8    myq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
          P7    dito:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq   idle   -         48x48x48x48x48
          P6    hhh:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
          P5    bbb:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
          P4    aaa:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
          P3    bello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
          P2    jello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
          P1    kebra:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
          

    """

    args      = ''

    cmdout    = \
"""
partlist.py 

Name  Queue                                                  State  Backfill  Geometry      
==============================================================================================
P10   zq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq     idle   -         48x48x48x48x48
P9    yours:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
P8    myq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
P7    dito:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq   idle   -         48x48x48x48x48
P6    hhh:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
P5    bbb:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
P4    aaa:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -         48x48x48x48x48
P3    bello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
P2    jello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
P1    kebra:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -         48x48x48x48x48
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'functional': '*', 'draining': '*', 'tag': 'partition', 'backfill_time': '*', 'children': '*', 'size': '*', 'name': '*', 'node_geometry': '*', 'queue': '*', 'state': '*'}]

GET_RESERVATIONS

active:True
partitions:*
queue:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

