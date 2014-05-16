import testutils

# ---------------------------------------------------------------------------------
def test_nodelist_arg_1():
    """
    nodelist test run: arg_1

    """

    args      = ''

    cmdout    = \
"""Host  Queue  State  Backfill
==============================
D1    QD1    good   -       
D2    QD2    bad    -       
D3    QD3    ugly   -       
U1    QU1    one    -       
U2    QU2    two    -       
U3    QU3    three  -       
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS


GET_BACKFILL_WINDOWS


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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_arg_2():
    """
    nodelist test run: arg_2

    """

    args      = """arg1"""

    cmdout    = \
"""Host  Queue  State  Backfill
==============================
D1    QD1    good   -       
D2    QD2    bad    -       
D3    QD3    ugly   -       
U1    QU1    one    -       
U2    QU2    two    -       
U3    QU3    three  -       
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS


GET_BACKFILL_WINDOWS


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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_debug():
    """
    nodelist test run: debug

    """

    args      = """-d"""

    cmdout    = \
"""Host  Queue  State  Backfill
==============================
D1    QD1    good   -       
D2    QD2    bad    -       
D3    QD3    ugly   -       
U1    QU1    one    -       
U2    QU2    two    -       
U3    QU3    three  -       
"""

    cmderr    = \
"""
nodelist.py -d

component: "system.get_implementation", defer: False
  get_implementation(
     )


component: "system.get_node_status", defer: False
  get_node_status(
     )


component: "system.get_queue_assignments", defer: False
  get_queue_assignments(
     )


component: "system.get_backfill_windows", defer: False
  get_backfill_windows(
     )


component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'queue': '*', 'active': True, 'partitions': '*'}],
     )


"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_NODES_STATUS


GET_QUEUE_ASSIGNMENTS


GET_BACKFILL_WINDOWS


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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodelist_options_1():
    """
    nodelist test run: options_1

    """

    args      = """-l"""

    cmdout    = ''

    cmderr    = \
"""Usage: nodelist.py

nodelist.py: error: no such option: -l
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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

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
  --noheader   disable display of header information
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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

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
  --noheader   disable display of header information
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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

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

    results = testutils.run_cmd('nodelist.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

