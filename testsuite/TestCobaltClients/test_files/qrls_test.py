import testutils

def test_qrls_invalid_option():
    """
    qrls test run: invalid_option

    """

    args      = """-k 1"""

    cmdout    = \
"""
qrls.py -k 1

Usage: qrls.py [options] <jobid1> [ ... <jobidN> ]

qrls.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qrls_debug_flag():
    """
    qrls test run: debug_flag

    """

    args      = """-d 1"""

    cmdout    = \
"""
qrls.py -d 1

Response: [{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'jobid': 1, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'georgerojas'}]
   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
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

user_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qrls_jobid_1():
    """
    qrls test run: jobid_1

    """

    args      = """myq 1 2 3 4"""

    cmdout    = \
"""
qrls.py myq 1 2 3 4

jobid must be an integer: myq
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qrls_jobid_2():
    """
    qrls test run: jobid_2

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""
qrls.py 1 2 3 4

   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
      job 2 does not have a 'user hold'
      job 3 does not have a 'user hold'
      job 4 does not have a 'user hold'
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

user_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qrls_jobid_3():
    """
    qrls test run: jobid_3

    """

    args      = """1"""

    cmdout    = \
"""
qrls.py 1

   Failed to remove user hold on jobs: 
      job 1 does not have a 'user hold'
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

user_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qrls_dependancy_option():
    """
    qrls test run: dependancy_option

    """

    args      = """-d --dependencies 1 2"""

    cmdout    = \
"""
qrls.py -d --dependencies 1 2

   Removed dependencies from jobs: 
      1
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

New Job Info:

all_dependencies:[]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qrls.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------

