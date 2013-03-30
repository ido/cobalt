import testutils

# ---------------------------------------------------------------------------------
def test_qhold_invalid_option():
    """
    qhold test run: invalid_option

    """

    args      = """-k 1"""

    cmdout    = \
"""
qhold.py -k 1

Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]

qhold.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_debg_option():
    """
    qhold test run: debg_option

    """

    args      = """-d 1"""

    cmdout    = \
"""
qhold.py -d 1

Response: [{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'jobid': 1, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 512, 'walltime': 5, 'user_hold': True, 'procs': 512, 'user': 'georgerojas'}]
Placed user hold on jobs: 
      1
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:georgerojas
user_hold:*

SET_JOBS


Original Jobs:

is_active:*
jobid:1
tag:job
user:georgerojas
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

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_1():
    """
    qhold test run: jobid_1

    """

    args      = """myq 1 2 3 4"""

    cmdout    = \
"""
qhold.py myq 1 2 3 4

jobid must be an integer: myq
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_2():
    """
    qhold test run: jobid_2

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""
qhold.py 1 2 3 4

Placed user hold on jobs: 
      1
      2
      3
      4
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:georgerojas
user_hold:*
jobid:2
tag:job
user:georgerojas
user_hold:*
jobid:3
tag:job
user:georgerojas
user_hold:*
jobid:4
tag:job
user:georgerojas
user_hold:*

SET_JOBS


Original Jobs:

is_active:*
jobid:1
tag:job
user:georgerojas
user_hold:*
is_active:*
jobid:2
tag:job
user:georgerojas
user_hold:*
is_active:*
jobid:3
tag:job
user:georgerojas
user_hold:*
is_active:*
jobid:4
tag:job
user:georgerojas
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

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_jobid_3():
    """
    qhold test run: jobid_3

    """

    args      = """1"""

    cmdout    = \
"""
qhold.py 1

Placed user hold on jobs: 
      1
"""

    stubout   = \
"""
GET_JOBS

jobid:1
tag:job
user:georgerojas
user_hold:*

SET_JOBS


Original Jobs:

is_active:*
jobid:1
tag:job
user:georgerojas
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

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qhold_dependancy_option():
    """
    qhold test run: dependancy_option

    """

    args      = """--dependencies 1 2"""

    cmdout    = \
"""
qhold.py --dependencies 1 2

Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]

qhold.py: error: no such option: --dependencies
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qhold.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

