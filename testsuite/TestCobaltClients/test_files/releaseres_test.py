import testutils

# ---------------------------------------------------------------------------------
def test_releaseres_arg_1():
    """
    releaseres test run: arg_1

    """

    args      = ''

    cmdout    = \
"""releaseres [--version] -p <partition> name
"""

    cmderr    = \
"""Need at least one reservation
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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_2():
    """
    releaseres test run: arg_2

    """

    args      = """s1"""

    cmdout    = \
"""Released reservation 's1', matched on 3 partitions
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

name:s1
name type: <type 'str'>
\RELEASE_RESERVATIONS

name:s1
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

    testutils.save_testhook("")

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_3():
    """
    releaseres test run: arg_3

    """

    args      = """s1 s2"""

    cmdout    = \
"""Released reservation 's1,s2', matched on 3 partitions
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
\RELEASE_RESERVATIONS

name:s1
name type: <type 'str'>
name:s2
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

    testutils.save_testhook("")

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_4():
    """
    releaseres test run: arg_4

    """

    args      = """s1 s2 s3"""

    cmdout    = \
"""Released reservation 's1,s2,s3', matched on 3 partitions
"""

    cmderr    = ''

    stubout   = \
"""
GET_RESERVATIONS

name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
name:s3
name type: <type 'str'>
\RELEASE_RESERVATIONS

name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_5():
    """
    releaseres test run: arg_5

    """

    args      = """-p p1"""

    cmdout    = ''

    cmderr    = \
"""Usage: releaseres.py [--version | --help | --debug] <reservation name>

releaseres.py: error: no such option: -p
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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_6():
    """
    releaseres test run: arg_6

    """

    args      = """-p p1 s1 s2 s3"""

    cmdout    = ''

    cmderr    = \
"""Usage: releaseres.py [--version | --help | --debug] <reservation name>

releaseres.py: error: no such option: -p
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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_7():
    """
    releaseres test run: arg_7

    """

    args      = """-t s1 s2 s3"""

    cmdout    = \
"""option -t not recognized
releaseres [--version] -p <partition> name
"""

    cmderr    = \
"""Usage: releaseres.py [--version | --help | --debug] <reservation name>

releaseres.py: error: no such option: -t
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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_8():
    """
    releaseres test run: arg_8

    """

    args      = """-d p1 s1 s2 s3"""

    cmdout    = \
"""Released reservation 'p1,s1,s2,s3', matched on 3 partitions
"""

    cmderr    = \
"""
releaseres.py -d p1 s1 s2 s3

component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'name': 'p1'}, {'name': 's1'}, {'name': 's2'}, {'name': 's3'}],
     )


component: "scheduler.release_reservations", defer: False
  release_reservations(
     [{'name': 'p1'}, {'name': 's1'}, {'name': 's2'}, {'name': 's3'}],
     gooduser,
     )


"""

    stubout   = \
"""
GET_RESERVATIONS

name:p1
name type: <type 'str'>
name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
name:s3
name type: <type 'str'>
\RELEASE_RESERVATIONS

name:p1
name type: <type 'str'>
name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_arg_9():
    """
    releaseres test run: arg_9

    """

    args      = """--debug p1 s1 s2 s3"""

    cmdout    = \
"""Released reservation 'p1,s1,s2,s3', matched on 3 partitions
"""

    cmderr    = \
"""
releaseres.py --debug p1 s1 s2 s3

component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'name': 'p1'}, {'name': 's1'}, {'name': 's2'}, {'name': 's3'}],
     )


component: "scheduler.release_reservations", defer: False
  release_reservations(
     [{'name': 'p1'}, {'name': 's1'}, {'name': 's2'}, {'name': 's3'}],
     gooduser,
     )


"""

    stubout   = \
"""
GET_RESERVATIONS

name:p1
name type: <type 'str'>
name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
name:s3
name type: <type 'str'>
\RELEASE_RESERVATIONS

name:p1
name type: <type 'str'>
name:s1
name type: <type 'str'>
name:s2
name type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_help_1():
    """
    releaseres test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: releaseres.py [--version | --help | --debug] <reservation name>

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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_help_2():
    """
    releaseres test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""Usage: releaseres.py [--version | --help | --debug] <reservation name>

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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_releaseres_version():
    """
    releaseres test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "releaseres.py " + $Id: releaseres.py 2146 2011-04-29 16:19:22Z richp $ + , Cobalt  + $Version$
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

    results = testutils.run_cmd('releaseres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

