import testutils

# ---------------------------------------------------------------------------------
def test_qselect_invalid_option():
    """
    qselect test run: invalid_option

    """

    args      = """-k"""

    cmdout    = ''

    cmderr    = \
"""Usage: qselect.py [options]

qselect.py: error: no such option: -k
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

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_only_arg():
    """
    qselect test run: only_arg

    """

    args      = """1"""

    cmdout    = ''

    cmderr    = \
"""qselect takes no arguments
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

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_no_args_opts():
    """
    qselect test run: no_args_opts

    """

    args      = ''

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_debug_flag():
    """
    qselect test run: debug_flag

    """

    args      = """-d"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = \
"""
qselect.py -d

component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'project': '*', 'queue': '*', 'state': '*', 'tag': 'job', 'mode': '*', 'nodes': '*', 'walltime': '*', 'jobid': '*'}],
     )


[{'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': '60', 'state': '*', 'score': 50, 'location': '/tmp', 'nodes': '512', 'args': '', 'is_active': False, 'user': 'land', 'procs': '512', 'walltime': '5', 'geometry': None, 'user_hold': False, 'jobid': 100, 'queue': 'jello', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']}]
"""

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_held_option():
    """
    qselect test run: held_option

    """

    args      = """-h user_hold"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:user_hold
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_nodecount_option():
    """
    qselect test run: nodecount_option

    """

    args      = """-n 312"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:312
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_state_and_nodecount():
    """
    qselect test run: state_and_nodecount

    """

    args      = """-n 312 -h user_hold"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:312
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:user_hold
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_walltime():
    """
    qselect test run: walltime

    """

    args      = """-t 10:10:10"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:610
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_mode():
    """
    qselect test run: mode

    """

    args      = """--mode vn"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:vn
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_verbose():
    """
    qselect test run: verbose

    """

    args      = """-v"""

    cmdout    = \
"""   The following jobs matched your query:
      100
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:*
jobid type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

