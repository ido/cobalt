import testutils

# ---------------------------------------------------------------------------------
def test_schedctl_args_1():
    """
    schedctl test run: args_1

    """

    args      = ''

    cmdout    = \
"""Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN


"""

    cmderr    = \
"""No required options provided

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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_args_2():
    """
    schedctl test run: args_2

    """

    args      = """1"""

    cmdout    = \
"""Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN


"""

    cmderr    = \
"""No required options provided

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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_1():
    """
    schedctl test run: combo_1

    """

    args      = """--start --stop"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: start option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_2():
    """
    schedctl test run: combo_2

    """

    args      = """--stop --status"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: stat option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_3():
    """
    schedctl test run: combo_3

    """

    args      = """--start --status"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: stat option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_4():
    """
    schedctl test run: combo_4

    """

    args      = """--reread-policy --status"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: reread option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_5():
    """
    schedctl test run: combo_5

    """

    args      = """--score 1.1 --stop 1 2 3 4"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: adjust option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_6():
    """
    schedctl test run: combo_6

    """

    args      = """--inherit 1.1 --start 1 2 3 4"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: start, dep_frac option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_7():
    """
    schedctl test run: combo_7

    """

    args      = """--start --savestate /tmp/s"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: savestate option(s)
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_combo_8():
    """
    schedctl test run: combo_8

    """

    args      = """--inherit 1.1 --score 1.1 1 2 3 4"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3, 4
updating inheritance fraction for jobs: 1, 2, 3, 4
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
jobid:4
jobid type: <type 'int'>
new score: 1.1, type = <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
jobid:4
jobid type: <type 'int'>

New Job Info:

dep_frac:1.1
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_start_1():
    """
    schedctl test run: start_1

    """

    args      = """--start 1"""

    cmdout    = \
"""Job Scheduling: ENABLED
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
ENABLE

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_start_2():
    """
    schedctl test run: start_2

    """

    args      = """--start"""

    cmdout    = \
"""Job Scheduling: ENABLED
"""

    cmderr    = ''

    stubout   = \
"""
ENABLE

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_stop_1():
    """
    schedctl test run: stop_1

    """

    args      = """--stop  1"""

    cmdout    = \
"""Job Scheduling: DISABLED
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
DISABLE

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_stop_2():
    """
    schedctl test run: stop_2

    """

    args      = """--stop"""

    cmdout    = \
"""Job Scheduling: DISABLED
"""

    cmderr    = ''

    stubout   = \
"""
DISABLE

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_stop_3():
    """
    schedctl test run: stop_3

    """

    args      = """-d --stop"""

    cmdout    = \
"""Job Scheduling: DISABLED
"""

    cmderr    = \
"""
schedctl.py -d --stop

component: "scheduler.disable", defer: False
  disable(
     gooduser,
     )


"""

    stubout   = \
"""
DISABLE

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_reread_1():
    """
    schedctl test run: reread_1

    """

    args      = """--reread-policy 1"""

    cmdout    = \
"""Attempting to reread utility functions.
"""

    cmderr    = \
"""No arguments needed
"""

    stubout   = \
"""
DEFINE_USER_UTILITY_FUNCTION

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_reread_2():
    """
    schedctl test run: reread_2

    """

    args      = """--reread-policy"""

    cmdout    = \
"""Attempting to reread utility functions.
"""

    cmderr    = ''

    stubout   = \
"""
DEFINE_USER_UTILITY_FUNCTION

whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_save_1():
    """
    schedctl test run: save_1

    """

    args      = """--savestate /tmp/s"""

    cmdout    = \
"""True
"""

    cmderr    = ''

    stubout   = \
"""
SAVE

filename:/tmp/s
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_save_2():
    """
    schedctl test run: save_2

    """

    args      = """--savestate s"""

    cmdout    = ''

    cmderr    = \
"""directory s does not exist
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

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_score_1():
    """
    schedctl test run: score_1

    """

    args      = """--score 0 1 2 3"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
new score: 0, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_score_2():
    """
    schedctl test run: score_2

    """

    args      = """--score 1 1 2 3"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
new score: 1, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_score_3():
    """
    schedctl test run: score_3

    """

    args      = """--score 1.0 1 2 3"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
new score: 1.0, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_score_4():
    """
    schedctl test run: score_4

    """

    args      = """--score -1.0 1 2 3"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
new score: -1.0, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_score_5():
    """
    schedctl test run: score_5

    """

    args      = """--score +1.0 1 2 3"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
new score: +1.0, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_inherit_1():
    """
    schedctl test run: inherit_1

    """

    args      = """--inherit 0 1 2 3"""

    cmdout    = \
"""updating inheritance fraction for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>

New Job Info:

dep_frac:0.0
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_inherit_2():
    """
    schedctl test run: inherit_2

    """

    args      = """--inherit 1 1 2 3"""

    cmdout    = \
"""updating inheritance fraction for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>

New Job Info:

dep_frac:1.0
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_inherit_3():
    """
    schedctl test run: inherit_3

    """

    args      = """--inherit 1.0 1 2 3"""

    cmdout    = \
"""updating inheritance fraction for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>

New Job Info:

dep_frac:1.0
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_inherit_4():
    """
    schedctl test run: inherit_4

    """

    args      = """--inherit -1.0 1 2 3"""

    cmdout    = \
"""updating inheritance fraction for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>

New Job Info:

dep_frac:-1.0
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_schedctl_inherit_5():
    """
    schedctl test run: inherit_5

    """

    args      = """--inherit +1.0 1 2 3"""

    cmdout    = \
"""updating inheritance fraction for jobs: 1, 2, 3
"""

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>

New Job Info:

dep_frac:1.0
dep_frac type: <type 'float'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

