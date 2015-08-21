import testutils

# ---------------------------------------------------------------------------------
def test_showres_arg_1():
    """
    showres test run: arg_1

    """

    args      = ''

    cmdout    = \
"""Reservation  Queue  User      Start                                 Duration  Passthrough  Partitions  Remaining  T-Minus  
===========================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_arg_2():
    """
    showres test run: arg_2

    """

    args      = """--oldts"""

    cmdout    = \
"""Reservation  Queue  User      Start                     Duration  Passthrough  Partitions  Remaining  T-Minus  
===============================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013  00:08     Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_arg_3():
    """
    showres test run: arg_3

    """

    args      = """arg1"""

    cmdout    = \
"""Reservation  Queue  User      Start                                 Duration  Passthrough  Partitions  Remaining  T-Minus  
===========================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_l_option_1():
    """
    showres test run: l_option_1

    """

    args      = """-l"""

    cmdout    = \
"""Reservation  Queue  User      Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  Remaining  T-Minus  
=============================================================================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_l_option_2():
    """
    showres test run: l_option_2

    """

    args      = """-l --oldts"""

    cmdout    = \
"""Reservation  Queue  User      Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  Remaining  T-Minus  
=====================================================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013  00:08     Tue Mar 26 22:05:00 2013  00:05       Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_x_option_1():
    """
    showres test run: x_option_1

    """

    args      = """-x"""

    cmdout    = \
"""Reservation  Queue  User      Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  Remaining  T-Minus  
======================================================================================================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     proj     id     10       15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_x_option_2():
    """
    showres test run: x_option_2

    """

    args      = """-x --oldts"""

    cmdout    = \
"""Reservation  Queue  User      Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  Remaining  T-Minus  
==============================================================================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013  00:08     Tue Mar 26 22:05:00 2013  00:05       Blocked      [P1-10]     proj     id     10       15:56:40   active   
"""

    cmderr    = ''

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_combo():
    """
    showres test run: combo

    """

    args      = """-l -x"""

    cmdout    = ''

    cmderr    = \
"""Only use -l or -x not both
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

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_help_1():
    """
    showres test run: help_1

    """

    args      = """--help"""

    cmdout    = \
"""Usage: showres [-l] [-x] [--oldts] [--version]

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
  -l           print reservation list verbose
  --oldts      use old timestamp
  -x           print reservations really verbose
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

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_help_2():
    """
    showres test run: help_2

    """

    args      = """-h"""

    cmdout    = \
"""Usage: showres [-l] [-x] [--oldts] [--version]

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d, --debug  turn on communication debugging
  -l           print reservation list verbose
  --oldts      use old timestamp
  -x           print reservations really verbose
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

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_version():
    """
    showres test run: version

    """

    args      = """--version"""

    cmdout    = \
"""version: "showres.py " + $Revision: 2154 $ + , Cobalt  + $Version$
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

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_showres_debug():
    """
    showres test run: debug

    """

    args      = """--debug"""

    cmdout    = \
"""Reservation  Queue  User      Start                                 Duration  Passthrough  Partitions  Remaining  T-Minus  
===========================================================================================================================
*            kebra  gooduser  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     15:56:40   active   
"""

    cmderr    = \
"""
showres.py --debug

component: "system.get_implementation", defer: False
  get_implementation(
     )


component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'users': '*', 'block_passthrough': '*', 'duration': '*', 'cycle': '*', 'project': '*', 'cycle_id': '*', 'name': '*', 'queue': '*', 'start': '*', 'partitions': '*', 'res_id': '*'}],
     )


"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
cycle_id:*
cycle_id type: <type 'str'>
duration:*
duration type: <type 'str'>
name:*
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
res_id:*
res_id type: <type 'str'>
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

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

