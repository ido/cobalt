import testutils

# ---------------------------------------------------------------------------------
def test_nodeadm_args_1():
    """
    nodeadm test run: args_1

    """

    args      = ''

    cmdout    = \
"""Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

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

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_args_2():
    """
    nodeadm test run: args_2

    """

    args      = """p1"""

    cmdout    = \
"""Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

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

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_combo_1():
    """
    nodeadm test run: combo_1

    """

    args      = """--up --down p1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: up option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_combo_2():
    """
    nodeadm test run: combo_2

    """

    args      = """--up -l p1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: list_nstates option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_combo_3():
    """
    nodeadm test run: combo_3

    """

    args      = """--list --queue q1 p1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_combo_4():
    """
    nodeadm test run: combo_4

    """

    args      = """--up --queue q1 p1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: queue option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_combo_5():
    """
    nodeadm test run: combo_5

    """

    args      = """--down --list p1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: list_nstates option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_up_1():
    """
    nodeadm test run: up_1

    """

    args      = """--up p1 p2 p3"""

    cmdout    = \
"""nodes marked up:
   U1
   U2
   U3
   U4
   U5

nodes that weren't in the down list:
   p1
   p2
   p3
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_UP

whoami: gooduser
args: ['p1', 'p2', 'p3']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_up_2():
    """
    nodeadm test run: up_2

    """

    args      = """--up U1 U2 U5 p1"""

    cmdout    = \
"""nodes marked up:
   U1
   U2
   U3
   U4
   U5

nodes that weren't in the down list:
   p1
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_UP

whoami: gooduser
args: ['U1', 'U2', 'U5', 'p1']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_down_1():
    """
    nodeadm test run: down_1

    """

    args      = """--down p1 p2 p3"""

    cmdout    = \
"""nodes marked down:
   D1
   D2
   D3
   D4
   D5

unknown nodes:
   p1
   p2
   p3
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_DOWN

whoami: gooduser
p1
p2
p3
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_down_2():
    """
    nodeadm test run: down_2

    """

    args      = """-d --down p1 p2 p3"""

    cmdout    = \
"""nodes marked down:
   D1
   D2
   D3
   D4
   D5

unknown nodes:
   p1
   p2
   p3
"""

    cmderr    = \
"""
nodeadm.py -d --down p1 p2 p3

component: "system.get_implementation", defer: False
  get_implementation(
     )


component: "system.nodes_down", defer: False
  nodes_down(
     ['p1', 'p2', 'p3'],
     gooduser,
     )


"""

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_DOWN

whoami: gooduser
p1
p2
p3
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_down_3():
    """
    nodeadm test run: down_3

    """

    args      = """--down D1 D2 D5 p1"""

    cmdout    = \
"""nodes marked down:
   D1
   D2
   D3
   D4
   D5

unknown nodes:
   p1
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_DOWN

whoami: gooduser
D1
D2
D5
p1
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_list_1():
    """
    nodeadm test run: list_1

    """

    args      = """-l"""

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

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_list_2():
    """
    nodeadm test run: list_2

    """

    args      = """-l p1"""

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

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_queue_1():
    """
    nodeadm test run: queue_1

    """

    args      = """--queue QU1"""

    cmdout    = \
"""Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

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

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_nodeadm_queue_2():
    """
    nodeadm test run: queue_2

    """

    args      = """--queue "QU1 QD1" U1 D1 P1"""

    cmdout    = \
"""QU1 QD1
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_QUEUE_ASSIGNMENTS

whoami: gooduser
args: ['U1', 'D1', 'P1']
queues: QU1 QD1
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

