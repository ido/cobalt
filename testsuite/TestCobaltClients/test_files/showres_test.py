import testutils

# ---------------------------------------------------------------------------------
def test_showres_arg_1():
    """
    showres test run: arg_1
        Old Command Output:
          Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions  
          ====================================================================================================
          *            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     
          

    """

    args      = ''

    cmdout    = \
"""Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions  
====================================================================================================
*            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                     Duration  Passthrough  Partitions  
          ========================================================================================
          *            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Blocked      [P1-10]     
          

    """

    args      = """--oldts"""

    cmdout    = \
"""Reservation  Queue  User   Start                     Duration  Passthrough  Partitions  
========================================================================================
*            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions  
          ====================================================================================================
          *            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     
          

    """

    args      = """arg1"""

    cmdout    = \
"""No arguments needed
Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions  
====================================================================================================
*            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  
          ======================================================================================================================================================
          *            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     
          

    """

    args      = """-l"""

    cmdout    = \
"""Reservation  Queue  User   Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  
======================================================================================================================================================
*            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  
          ==============================================================================================================================
          *            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Tue Mar 26 17:05:00 2013  00:05       Blocked      [P1-10]     
          

    """

    args      = """-l --oldts"""

    cmdout    = \
"""Reservation  Queue  User   Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  
==============================================================================================================================
*            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Tue Mar 26 17:05:00 2013  00:05       Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  
          ===============================================================================================================================================================================
          *            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     proj     id     10       
          

    """

    args      = """-x"""

    cmdout    = \
"""Reservation  Queue  User   Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  
===============================================================================================================================================================================
*            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Tue Mar 26 22:05:00 2013 +0000 (UTC)  00:05       Blocked      [P1-10]     proj     id     10       
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Reservation  Queue  User   Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  
          =======================================================================================================================================================
          *            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Tue Mar 26 17:05:00 2013  00:05       Blocked      [P1-10]     proj     id     10       
          

    """

    args      = """-x --oldts"""

    cmdout    = \
"""Reservation  Queue  User   Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions  Project  ResID  CycleID  
=======================================================================================================================================================
*            kebra  james  Tue Mar 26 16:56:40 2013  00:08     Tue Mar 26 17:05:00 2013  00:05       Blocked      [P1-10]     proj     id     10       
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    cmdout    = \
"""Only use -l or -x not both
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
"""
showres.py --debug

Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions  
====================================================================================================
*            kebra  james  Tue Mar 26 21:56:40 2013 +0000 (UTC)  00:08     Blocked      [P1-10]     
"""

    stubout   = \
"""
GET_IMPLEMENTATION


GET_RESERVATIONS

block_passthrough:*
cycle:*
cycle_id:*
duration:*
name:*
partitions:*
project:*
queue:*
res_id:*
start:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('showres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

