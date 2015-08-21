import testutils

# ---------------------------------------------------------------------------------
def test_slpstat_arg_1():
    """
    slpstat test run: arg_1

    """

    args      = ''

    cmdout    = \
"""Name  Location  Update Time               
==========================================
S0    P0        Mon Apr 22 22:06:10 2013  
S1    P1        Mon Apr 22 22:06:20 2013  
S2    P2        Mon Apr 22 22:06:30 2013  
S3    P3        Mon Apr 22 22:06:40 2013  
S4    P4        Mon Apr 22 22:06:50 2013  
"""

    cmderr    = ''

    stubout   = \
"""
GET_SERVICES

location:*
location type: <type 'str'>
name:*
name type: <type 'str'>
stamp:*
stamp type: <type 'str'>
tag:service
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_arg_2():
    """
    slpstat test run: arg_2

    """

    args      = ''

    cmdout    = \
"""no services registered
"""

    cmderr    = ''

    stubout   = \
"""
GET_SERVICES

location:*
location type: <type 'str'>
name:*
name type: <type 'str'>
stamp:*
stamp type: <type 'str'>
tag:service
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("NO SERVICES")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_arg_3():
    """
    slpstat test run: arg_3

    """

    args      = """arg1"""

    cmdout    = \
"""Name  Location  Update Time               
==========================================
S0    P0        Mon Apr 22 22:06:10 2013  
S1    P1        Mon Apr 22 22:06:20 2013  
S2    P2        Mon Apr 22 22:06:30 2013  
S3    P3        Mon Apr 22 22:06:40 2013  
S4    P4        Mon Apr 22 22:06:50 2013  
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
GET_SERVICES

location:*
location type: <type 'str'>
name:*
name type: <type 'str'>
stamp:*
stamp type: <type 'str'>
tag:service
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_debug_1():
    """
    slpstat test run: debug_1

    """

    args      = """-d"""

    cmdout    = \
"""Name  Location  Update Time               
==========================================
S0    P0        Mon Apr 22 22:06:10 2013  
S1    P1        Mon Apr 22 22:06:20 2013  
S2    P2        Mon Apr 22 22:06:30 2013  
S3    P3        Mon Apr 22 22:06:40 2013  
S4    P4        Mon Apr 22 22:06:50 2013  
"""

    cmderr    = \
"""
slpstat.py -d

component: "service-location.get_services", defer: False
  get_services(
     [{'stamp': '*', 'tag': 'service', 'name': '*', 'location': '*'}],
     )


"""

    stubout   = \
"""
GET_SERVICES

location:*
location type: <type 'str'>
name:*
name type: <type 'str'>
stamp:*
stamp type: <type 'str'>
tag:service
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_debug_2():
    """
    slpstat test run: debug_2

    """

    args      = """-d"""

    cmdout    = \
"""no services registered
"""

    cmderr    = \
"""
slpstat.py -d

component: "service-location.get_services", defer: False
  get_services(
     [{'stamp': '*', 'tag': 'service', 'name': '*', 'location': '*'}],
     )


"""

    stubout   = \
"""
GET_SERVICES

location:*
location type: <type 'str'>
name:*
name type: <type 'str'>
stamp:*
stamp type: <type 'str'>
tag:service
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("NO SERVICES")

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_help_1():
    """
    slpstat test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_help_2():
    """
    slpstat test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_slpstat_version():
    """
    slpstat test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "slpstat.py " + $Revision: 1221 $ + , Cobalt  + $Version$
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

    results = testutils.run_cmd('slpstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

