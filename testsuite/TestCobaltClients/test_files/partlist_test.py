import testutils

# ---------------------------------------------------------------------------------
def test_partlist_version_option_1():
    """
    partlist test run: version_option_1

    """

    args      = """--version"""

    cmdout    = \
"""version: "partlist.py " + $Revision: 1981 $ + , Cobalt  + $Version$
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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_version_option_2():
    """
    partlist test run: version_option_2

    """

    args      = """-v"""

    cmdout    = ''

    cmderr    = \
"""Usage: partlist.py [options] 

partlist.py: error: no such option: -v
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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_debug():
    """
    partlist test run: debug

    """

    args      = """-d"""

    cmdout    = \
"""Name  Queue                                                  State  Backfill
==============================================================================
P10   zq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq     idle   -       
P9    yours:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P8    myq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P7    dito:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq   idle   -       
P6    hhh:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P5    bbb:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P4    aaa:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P3    bello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P2    jello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P1    kebra:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
"""

    cmderr    = \
"""
partlist.py -d

component: "system.get_partitions", defer: True
  get_partitions(
     [{'queue': '*', 'scheduled': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'backfill_time': '*', 'children': '*', 'functional': '*', 'draining': '*', 'size': '*'}],
     )


component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'queue': '*', 'active': True, 'partitions': '*'}],
     )


"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'queue': '*', 'scheduled': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'backfill_time': '*', 'children': '*', 'functional': '*', 'draining': '*', 'size': '*'}]

GET_RESERVATIONS

active:True
active type: <type 'bool'>
partitions:*
partitions type: <type 'str'>
queue:*
queue type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

    """

    args      = """-h"""

    cmdout    = \
"""Usage: partlist.py [options] 

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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: partlist.py [options] 

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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_invalid():
    """
    partlist test run: invalid

    """

    args      = """-k"""

    cmdout    = ''

    cmderr    = \
"""Usage: partlist.py [options] 

partlist.py: error: no such option: -k
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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_argument_1():
    """
    partlist test run: argument_1

    """

    args      = """arg"""

    cmdout    = ''

    cmderr    = \
"""No arguments required
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

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partlist_argument_2():
    """
    partlist test run: argument_2

    """

    args      = ''

    cmdout    = \
"""Name  Queue                                                  State  Backfill
==============================================================================
P10   zq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq     idle   -       
P9    yours:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P8    myq:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P7    dito:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq   idle   -       
P6    hhh:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P5    bbb:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P4    aaa:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq    idle   -       
P3    bello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P2    jello:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
P1    kebra:kebra:jello:bello:aaa:bbb:hhh:dito:myq:yours:zq  idle   -       
"""

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'queue': '*', 'scheduled': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'backfill_time': '*', 'children': '*', 'functional': '*', 'draining': '*', 'size': '*'}]

GET_RESERVATIONS

active:True
active type: <type 'bool'>
partitions:*
partitions type: <type 'str'>
queue:*
queue type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('partlist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

