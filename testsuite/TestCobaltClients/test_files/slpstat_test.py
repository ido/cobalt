import testutils

# ---------------------------------------------------------------------------------
def test_slpstat_arg_1():
    """
    slpstat test run: arg_1
        Old Command Output:
          Name  Location  Update Time               
          ==========================================
          S0    P0        Mon Apr 22 17:06:10 2013  
          S1    P1        Mon Apr 22 17:06:20 2013  
          S2    P2        Mon Apr 22 17:06:30 2013  
          S3    P3        Mon Apr 22 17:06:40 2013  
          S4    P4        Mon Apr 22 17:06:50 2013  
          

    """

    args      = ''

    cmdout    = \
"""
slpstat.py 

Name  Location  Update Time               
==========================================
S0    P0        Mon Apr 22 17:06:10 2013  
S1    P1        Mon Apr 22 17:06:20 2013  
S2    P2        Mon Apr 22 17:06:30 2013  
S3    P3        Mon Apr 22 17:06:40 2013  
S4    P4        Mon Apr 22 17:06:50 2013  
"""

    stubout   = \
"""
GET_SERVICES

location:*
name:*
stamp:*
tag:service
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_arg_2():
    """
    slpstat test run: arg_2
        Old Command Output:
          no services registered
          

    """

    args      = ''

    cmdout    = \
"""
slpstat.py 

no services registered
"""

    stubout   = \
"""
GET_SERVICES

location:*
name:*
stamp:*
tag:service
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("NO SERVICES")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_arg_3():
    """
    slpstat test run: arg_3
        Old Command Output:
          Name  Location  Update Time               
          ==========================================
          S0    P0        Mon Apr 22 17:06:10 2013  
          S1    P1        Mon Apr 22 17:06:20 2013  
          S2    P2        Mon Apr 22 17:06:30 2013  
          S3    P3        Mon Apr 22 17:06:40 2013  
          S4    P4        Mon Apr 22 17:06:50 2013  
          

    """

    args      = """arg1"""

    cmdout    = \
"""
slpstat.py arg1

No arguments needed
Name  Location  Update Time               
==========================================
S0    P0        Mon Apr 22 17:06:10 2013  
S1    P1        Mon Apr 22 17:06:20 2013  
S2    P2        Mon Apr 22 17:06:30 2013  
S3    P3        Mon Apr 22 17:06:40 2013  
S4    P4        Mon Apr 22 17:06:50 2013  
"""

    stubout   = \
"""
GET_SERVICES

location:*
name:*
stamp:*
tag:service
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_help_1():
    """
    slpstat test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""
slpstat.py --help

Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]

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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_help_2():
    """
    slpstat test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""
slpstat.py -h

Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]

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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_version():
    """
    slpstat test run: version

    """

    args      = """--version"""

    cmdout    = \
"""
slpstat.py --version

version: "slpstat.py " + $Revision: 1221 $ + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result
