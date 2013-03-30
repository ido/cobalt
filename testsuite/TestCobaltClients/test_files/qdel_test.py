import testutils

# ---------------------------------------------------------------------------------
def test_qdel_invalid_option():
    """
    qdel test run: invalid_option

    """

    args      = """-k 1"""

    cmdout    = \
"""
qdel.py -k 1

Usage: qdel.py [options] <jobid1> [ ... <jobidN>]

qdel.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_debug_option():
    """
    qdel test run: debug_option

    """

    args      = """-d 1"""

    cmdout    = \
"""
qdel.py -d 1

Usage: qdel.py [options] <jobid1> [ ... <jobidN>]

qdel.py: error: no such option: -d
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_1():
    """
    qdel test run: jobid_1

    """

    args      = """myq 1 2 3 4"""

    cmdout    = \
"""
qdel.py myq 1 2 3 4

jobid must be an integer: myq
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_2():
    """
    qdel test run: jobid_2

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""
qdel.py 1 2 3 4

      Deleted Jobs
JobID  User         
====================
1      georgerojas  
2      georgerojas  
3      georgerojas  
4      georgerojas  
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:georgerojas
jobid:1
tag:job
user:georgerojas
jobid:2
tag:job
user:georgerojas
jobid:3
tag:job
user:georgerojas
jobid:4
tag:job
user:georgerojas
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_3():
    """
    qdel test run: jobid_3

    """

    args      = """1"""

    cmdout    = \
"""
qdel.py 1

      Deleted Jobs
JobID  User         
====================
1      georgerojas  
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:georgerojas
jobid:1
tag:job
user:georgerojas
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

