import testutils

# ---------------------------------------------------------------------------------
def test_nodelist_arg_1():
    """
    nodelist test run: arg_1
        Old Command Output:
          Host  Queue  State
          ====================
          D1    QD1    good 
          D2    QD2    bad  
          D3    QD3    ugly 
          U1    QU1    one  
          U2    QU2    two  
          U3    QU3    three
          

    """

    args      = ''

    cmdout    = \
"""Host  Queue  State
====================
D1    QD1    good 
D2    QD2    bad  
D3    QD3    ugly 
U1    QU1    one  
U2    QU2    two  
U3    QU3    three
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_arg_2():
    """
    nodelist test run: arg_2
        Old Command Output:
          Host  Queue  State
          ====================
          D1    QD1    good 
          D2    QD2    bad  
          D3    QD3    ugly 
          U1    QU1    one  
          U2    QU2    two  
          U3    QU3    three
          

    """

    args      = """arg1"""

    cmdout    = \
"""No arguments needed
Host  Queue  State
====================
D1    QD1    good 
D2    QD2    bad  
D3    QD3    ugly 
U1    QU1    one  
U2    QU2    two  
U3    QU3    three
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_debug():
    """
    nodelist test run: debug

    """

    args      = """-d"""

    cmdout    = \
"""
nodelist.py -d

Host  Queue  State
====================
D1    QD1    good 
D2    QD2    bad  
D3    QD3    ugly 
U1    QU1    one  
U2    QU2    two  
U3    QU3    three
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_options_1():
    """
    nodelist test run: options_1

    """

    args      = """-l"""

    cmdout    = \
"""Usage: nodelist.py

nodelist.py: error: no such option: -l
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_options_2():
    """
    nodelist test run: options_2

    """

    args      = """--help"""

    cmdout    = \
"""Usage: nodelist.py

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_options_3():
    """
    nodelist test run: options_3

    """

    args      = """-h"""

    cmdout    = \
"""Usage: nodelist.py

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_options_4():
    """
    nodelist test run: options_4

    """

    args      = """--version"""

    cmdout    = \
"""version: "nodelist.py " + TBD + , Cobalt  + TBD
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

