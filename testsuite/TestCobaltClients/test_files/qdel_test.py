import testutils

# ---------------------------------------------------------------------------------
def test_qdel_invalid_option():
    """
    qdel test run: invalid_option

    """

    args      = """-k 1"""

    cmdout    = ''

    cmderr    = \
"""Usage: qdel.py [options] <jobid1> [ ... <jobidN>]

qdel.py: error: no such option: -k
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
"""      Deleted Jobs
JobID  User      
=================
1      gooduser  
"""

    cmderr    = \
"""
qdel.py -d 1

component: "queue-manager.del_jobs", defer: True
  del_jobs(
     [{'tag': 'job', 'user': 'gooduser', 'jobid': 1}],
     False,
     gooduser,
     )


"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qdel_jobid_2():
    """
    qdel test run: jobid_2

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

    cmderr    = ''

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
jobid:2
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
jobid:3
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
jobid:4
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """1"""

    cmdout    = \
"""      Deleted Jobs
JobID  User      
=================
1      gooduser  
"""

    cmderr    = ''

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qdel.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

