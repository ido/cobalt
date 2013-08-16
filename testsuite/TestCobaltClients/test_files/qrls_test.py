import testutils

# ---------------------------------------------------------------------------------
def test_qrls_invalid_option():
    """
    qrls test run: invalid_option

    """

    args      = """-k 1"""

    cmdout    = ''

    cmderr    = \
"""Usage: qrls.py [options] <jobid1> [ ... <jobidN> ]

qrls.py: error: no such option: -k
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

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qrls_debug_flag():
    """
    qrls test run: debug_flag

    """

    args      = """-d 1"""

    cmdout    = \
"""   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
"""

    cmderr    = \
"""
qrls.py -d 1

component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'user_hold': '*', 'tag': 'job', 'user': 'gooduser', 'jobid': 1}],
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'gooduser', 'jobid': 1}],
     {'user_hold': False},
     gooduser,
     )


Response: [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
"""

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

New Job Info:

user_hold:False
user_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qrls_jobid_1():
    """
    qrls test run: jobid_1

    """

    args      = """myq 1 2 3 4"""

    cmdout    = ''

    cmderr    = \
"""jobid must be an integer: myq
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

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qrls_jobid_2():
    """
    qrls test run: jobid_2

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
      job 2 does not have a 'user hold'
      job 3 does not have a 'user hold'
      job 4 does not have a 'user hold'
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
jobid:2
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
jobid:3
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
jobid:4
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

New Job Info:

user_hold:False
user_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qrls_jobid_3():
    """
    qrls test run: jobid_3

    """

    args      = """1"""

    cmdout    = \
"""   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

New Job Info:

user_hold:False
user_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qrls_dependancy_option():
    """
    qrls test run: dependancy_option

    """

    args      = """-d --dependencies 1 2"""

    cmdout    = \
"""   Removed dependencies from jobs: 
      1
      2
"""

    cmderr    = \
"""
qrls.py -d --dependencies 1 2

component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'user_hold': '*', 'tag': 'job', 'user': 'gooduser', 'jobid': 1}, {'user_hold': '*', 'tag': 'job', 'user': 'gooduser', 'jobid': 2}],
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'gooduser', 'jobid': 1}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'gooduser', 'jobid': 2}],
     {'all_dependencies': []},
     gooduser,
     )


"""

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
jobid:2
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>

New Job Info:

all_dependencies:[]
all_dependencies type: <type 'list'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

