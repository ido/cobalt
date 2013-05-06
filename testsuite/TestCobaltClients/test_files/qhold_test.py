import testutils

# ---------------------------------------------------------------------------------
def test_qhold_invalid_option():
    """
    qhold test run: invalid_option
        Old Command Output:
          option -k not recognized
          Usage:
          qhold [--version] <jobid> <jobid>
          

    """

    args      = """-k 1"""

    cmdout    = \
"""Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]

qhold.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_debg_option():
    """
    qhold test run: debg_option
        Old Command Output:
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """-d 1"""

    cmdout    = \
"""
qhold.py -d 1

Response: [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
   Failed to place user hold on jobs: 
      job 1 encountered an unexpected problem while attempting to place the 'user hold'
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:gooduser
user_hold:*

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
jobid:1
tag:job
user:gooduser
user_hold:*

New Job Info:

user_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_1():
    """
    qhold test run: jobid_1
        Old Command Output:
          jobid must be an integer
          

    """

    args      = """myq 1 2 3 4"""

    cmdout    = \
"""jobid must be an integer: myq
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_2():
    """
    qhold test run: jobid_2
        Old Command Output:
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
                job 2 encountered an unexpected problem while attempting to place the 'user hold'
                job 3 encountered an unexpected problem while attempting to place the 'user hold'
                job 4 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""   Failed to place user hold on jobs: 
      job 1 encountered an unexpected problem while attempting to place the 'user hold'
      job 2 encountered an unexpected problem while attempting to place the 'user hold'
      job 3 encountered an unexpected problem while attempting to place the 'user hold'
      job 4 encountered an unexpected problem while attempting to place the 'user hold'
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:gooduser
user_hold:*
jobid:2
tag:job
user:gooduser
user_hold:*
jobid:3
tag:job
user:gooduser
user_hold:*
jobid:4
tag:job
user:gooduser
user_hold:*

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
jobid:1
tag:job
user:gooduser
user_hold:*
is_active:*
jobid:2
tag:job
user:gooduser
user_hold:*
is_active:*
jobid:3
tag:job
user:gooduser
user_hold:*
is_active:*
jobid:4
tag:job
user:gooduser
user_hold:*

New Job Info:

user_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_3():
    """
    qhold test run: jobid_3
        Old Command Output:
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """1"""

    cmdout    = \
"""   Failed to place user hold on jobs: 
      job 1 encountered an unexpected problem while attempting to place the 'user hold'
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:gooduser
user_hold:*

SET_JOBS


Original Jobs:

user: gooduser
is_active:*
jobid:1
tag:job
user:gooduser
user_hold:*

New Job Info:

user_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_dependancy_option():
    """
    qhold test run: dependancy_option
        Old Command Output:
          option --dependencies not recognized
          Usage:
          qhold [--version] <jobid> <jobid>
          

    """

    args      = """--dependencies 1 2"""

    cmdout    = \
"""Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]

qhold.py: error: no such option: --dependencies
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

