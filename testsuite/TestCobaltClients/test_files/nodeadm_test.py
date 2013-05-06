import testutils

# ---------------------------------------------------------------------------------
def test_nodeadm_args_1():
    """
    nodeadm test run: args_1
        Old Command Output:
          Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]
          
          Options:
            -h, --help     show this help message and exit
            --down         mark nodes as down
            --up           mark nodes as up (even if allocated)
            --queue=QUEUE  set queue associations
            -l             list node states
          

    """

    args      = ''

    cmdout    = \
"""No arguments provided
Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -d, --debug    turn on communication debugging
  --down         mark nodes as down
  --up           mark nodes as up (even if allocated)
  --queue=QUEUE  set queue associations
  -l, --list     list node states
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]
          
          Options:
            -h, --help     show this help message and exit
            --down         mark nodes as down
            --up           mark nodes as up (even if allocated)
            --queue=QUEUE  set queue associations
            -l             list node states
          

    """

    args      = """p1"""

    cmdout    = \
"""Need at least one option
Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -d, --debug    turn on communication debugging
  --down         mark nodes as down
  --up           mark nodes as up (even if allocated)
  --queue=QUEUE  set queue associations
  -l, --list     list node states
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          --down and --up cannot be used together
          

    """

    args      = """--up --down p1"""

    cmdout    = \
"""Option combinations not allowed with: down, up option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    cmdout    = \
"""Option combinations not allowed with: up, queue, list option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    cmdout    = \
"""Option combinations not allowed with: queue, list option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    stubout   = \
"""
GET_IMPLEMENTATION


NODES_UP

whoami: gooduser
args: ['p1']
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    cmdout    = \
"""Option combinations not allowed with: down, queue, list option(s)
"""

    stubout   = \
"""
GET_IMPLEMENTATION

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          nodes marked up:
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          nodes marked up:
             U1
             U2
             U3
             U4
             U5
          
          nodes that weren't in the down list:
             p1
          

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
                       stubout # Expected stub functions output
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
        Old Command Output:
          nodes marked down:
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
                       stubout # Expected stub functions output
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
"""
nodeadm.py -d --down p1 p2 p3

nodes marked down:
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          nodes marked down:
             D1
             D2
             D3
             D4
             D5
          
          unknown nodes:
             p1
          

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
                       stubout # Expected stub functions output
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

    args      = """-l"""

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

    args      = """-l p1"""

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
        Old Command Output:
          Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]
          
          Options:
            -h, --help     show this help message and exit
            --down         mark nodes as down
            --up           mark nodes as up (even if allocated)
            --queue=QUEUE  set queue associations
            -l             list node states
          

    """

    args      = """--queue QU1"""

    cmdout    = \
"""No arguments provided
Usage: nodeadm.py [-l] [--down part1 part2] [--up part1 part2]"

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -d, --debug    turn on communication debugging
  --down         mark nodes as down
  --up           mark nodes as up (even if allocated)
  --queue=QUEUE  set queue associations
  -l, --list     list node states
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          QU1 QD1
          

    """

    args      = """--queue "QU1 QD1" U1 D1 P1"""

    cmdout    = \
"""QU1 QD1
"""

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
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('nodeadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

