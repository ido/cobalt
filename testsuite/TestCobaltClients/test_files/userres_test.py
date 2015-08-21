import testutils

# ---------------------------------------------------------------------------------
def test_userres_arg_1():
    """
    userres test run: arg_1

    """

    args      = ''

    cmdout    = \
"""Usage: userres.py [--version | --help | --debug]  <reservation name(s)>

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

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_2():
    """
    userres test run: arg_2

    """

    args      = """-p p1"""

    cmdout    = ''

    cmderr    = \
"""Usage: userres.py [--version | --help | --debug]  <reservation name(s)>

userres.py: error: no such option: -p
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

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_2():
    """
    userres test run: arg_2

    """

    args      = """s1"""

    cmdout    = \
"""Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_3():
    """
    userres test run: arg_3

    """

    args      = """s1 s2 s3"""

    cmdout    = \
"""Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's2': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's3': Tue Mar 26 22:01:40 2013
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s2
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s3
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_4():
    """
    userres test run: arg_4

    """

    args      = """s1 s2 s3"""

    cmdout    = \
"""Releasing reservation 's1'
Releasing reservation 's2'
Releasing reservation 's3'
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
\RELEASE_RESERVATIONS

name:s1
name type: <type 'str'>
user: gooduser
\RELEASE_RESERVATIONS

name:s2
name type: <type 'str'>
user: gooduser
\RELEASE_RESERVATIONS

name:s3
name type: <type 'str'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("NO CYCLE")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_5():
    """
    userres test run: arg_5

    """

    args      = """s1"""

    cmdout    = ''

    cmderr    = \
"""You are not a user of reservation 's1' and so cannot alter it.
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("BOGUS USER")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_6():
    """
    userres test run: arg_6

    """

    args      = """s1 s2 s3"""

    cmdout    = \
"""Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's2': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's3': Tue Mar 26 22:01:40 2013
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s2
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s3
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_7():
    """
    userres test run: arg_7

    """

    args      = """s1 s2 s3 s4"""

    cmdout    = \
"""Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's2': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's3': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's4': Tue Mar 26 22:01:40 2013
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s4
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s2
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s3
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s4
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_8():
    """
    userres test run: arg_8

    """

    args      = """-d p1 s1 s2 s3"""

    cmdout    = \
"""Setting new start time for for reservation 'p1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's2': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's3': Tue Mar 26 22:01:40 2013
"""

    cmderr    = \
"""
userres.py -d p1 s1 s2 s3

component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'duration': '*', 'start': '*', 'cycle': '*', 'name': 'p1', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's1', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's2', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's3', 'users': '*'}],
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 'p1'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's1'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's2'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's3'}],
     {'start': 1364335300.0},
     gooduser,
     )


"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:p1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:p1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s2
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s3
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_arg_9():
    """
    userres test run: arg_9

    """

    args      = """--debug p1 s1 s2 s3"""

    cmdout    = \
"""Setting new start time for for reservation 'p1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's1': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's2': Tue Mar 26 22:01:40 2013
Setting new start time for for reservation 's3': Tue Mar 26 22:01:40 2013
"""

    cmderr    = \
"""
userres.py --debug p1 s1 s2 s3

component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'duration': '*', 'start': '*', 'cycle': '*', 'name': 'p1', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's1', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's2', 'users': '*'}, {'duration': '*', 'start': '*', 'cycle': '*', 'name': 's3', 'users': '*'}],
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 'p1'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's1'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's2'}],
     {'start': 1364335300.0},
     gooduser,
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 's3'}],
     {'start': 1364335300.0},
     gooduser,
     )


"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:p1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s1
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s2
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:s3
name type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

SET_RESERVATIONS

name:p1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s1
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s2
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

SET_RESERVATIONS

name:s3
name type: <type 'str'>
start:1364335300.0
start type: <type 'float'>
user: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_help_1():
    """
    userres test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: userres.py [--version | --help | --debug]  <reservation name(s)>

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

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_help_2():
    """
    userres test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""Usage: userres.py [--version | --help | --debug]  <reservation name(s)>

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

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_userres_version():
    """
    userres test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "userres.py " + $Id: releaseres.py 1361 2008-08-08 16:22:14Z buettner $ + , Cobalt  + $Version$
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

    results = testutils.run_cmd('userres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

