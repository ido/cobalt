import testutils

# ---------------------------------------------------------------------------------
def test_qdel_invalid_option():
    """
    qdel test run: invalid_option
        Old Command Output:
          option -k not recognized
          Usage:
          qdel [--version] [-f] <jobid> <jobid>
          

    """

    args      = """-k 1"""

    cmdout    = \
"""Usage: qdel.py [options] <jobid1> [ ... <jobidN>]

qdel.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

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

      Deleted Jobs
JobID  User      
=================
1      gooduser  
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
tag:job
user:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_1():
    """
    qdel test run: jobid_1
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

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_2():
    """
    qdel test run: jobid_2
        Old Command Output:
                Deleted Jobs
          JobID  User      
          =================
          1      gooduser  
          2      gooduser  
          3      gooduser  
          4      gooduser  
          

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""      Deleted Jobs
JobID  User      
=================
1      gooduser  
2      gooduser  
3      gooduser  
4      gooduser  
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
tag:job
user:gooduser
jobid:2
tag:job
user:gooduser
jobid:3
tag:job
user:gooduser
jobid:4
tag:job
user:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_3():
    """
    qdel test run: jobid_3
        Old Command Output:
                Deleted Jobs
          JobID  User      
          =================
          1      gooduser  
          

    """

    args      = """1"""

    cmdout    = \
"""      Deleted Jobs
JobID  User      
=================
1      gooduser  
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
tag:job
user:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

