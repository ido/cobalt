import testutils

# ---------------------------------------------------------------------------------
def test_schedctl_args_1():
    """
    schedctl test run: args_1
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = ''

    cmdout    = \
"""Need at least one option
Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d, --debug           turn on communication debugging
  --stop                stop scheduling jobs
  --start               resume scheduling jobs
  --status              query scheduling status
  --reread-policy       reread the utility function definition file
  --savestate=SAVESTATE
                        write the current state to the specified file
  --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
  --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                        inherited by jobs which depend on the arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          

    """

    args      = """1"""

    cmdout    = \
"""Need at least one option
Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d, --debug           turn on communication debugging
  --stop                stop scheduling jobs
  --start               resume scheduling jobs
  --status              query scheduling status
  --reread-policy       reread the utility function definition file
  --savestate=SAVESTATE
                        write the current state to the specified file
  --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
  --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                        inherited by jobs which depend on the arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--start --stop"""

    cmdout    = \
"""Option combinations not allowed with: stop, start option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--stop --status"""

    cmdout    = \
"""Option combinations not allowed with: stop, stat option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--start --status"""

    cmdout    = \
"""Option combinations not allowed with: start, stat option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--reread-policy --status"""

    cmdout    = \
"""Option combinations not allowed with: stat, reread option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--score 1.1 --stop"""

    cmdout    = \
"""At least one jobid must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--inherit 1.1 --start"""

    cmdout    = \
"""At least one jobid must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Usage: schedctl.py [options]
          
          Options:
            -h, --help            show this help message and exit
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """--start --savestate /tmp/s"""

    cmdout    = \
"""Option combinations not allowed with: start, savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          Job Scheduling: ENABLED
          

    """

    args      = """--start 1"""

    cmdout    = \
"""No arguments needed
Job Scheduling: ENABLED
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          Job Scheduling: ENABLED
          

    """

    args      = """--start"""

    cmdout    = \
"""Job Scheduling: ENABLED
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          Job Scheduling: DISABLED
          

    """

    args      = """--stop  1"""

    cmdout    = \
"""No arguments needed
Job Scheduling: DISABLED
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          Job Scheduling: DISABLED
          

    """

    args      = """--stop"""

    cmdout    = \
"""Job Scheduling: DISABLED
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
                       stubout # Expected stub functions output
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
"""
schedctl.py -d --stop

Job Scheduling: DISABLED
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          Attempting to reread utility functions.
          

    """

    args      = """--reread-policy 1"""

    cmdout    = \
"""No arguments needed
Attempting to reread utility functions.
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          must specify at least one jobid
          Attempting to reread utility functions.
          

    """

    args      = """--reread-policy"""

    cmdout    = \
"""Attempting to reread utility functions.
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
                       stubout # Expected stub functions output
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
        Old Command Output:
          True
          

    """

    args      = """--savestate /tmp/s"""

    cmdout    = \
"""True
"""

    stubout   = \
"""
SAVE

filename:/tmp/s
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
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
        Old Command Output:
          directory  does not exist
          

    """

    args      = """--savestate s"""

    cmdout    = \
"""directory s does not exist
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('schedctl.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

