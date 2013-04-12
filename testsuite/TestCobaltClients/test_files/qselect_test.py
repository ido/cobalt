import testutils

# ---------------------------------------------------------------------------------
def test_qselect_invalid_option():
    """
    qselect test run: invalid_option
        Old Command Output:
          option -k not recognized
          
          Usage: qselect [-d] [-v] -A <project name> -q <queue> -n <number of nodes> 
                         -t <time in minutes> -h <hold types> --mode <mode co/vn>
          
          

    """

    args      = """-k"""

    cmdout    = \
"""
qselect.py -k

Usage: qselect.py [options]

qselect.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_only_arg():
    """
    qselect test run: only_arg
        Old Command Output:
          
          Usage: qselect [-d] [-v] -A <project name> -q <queue> -n <number of nodes> 
                         -t <time in minutes> -h <hold types> --mode <mode co/vn>
          
          

    """

    args      = """1"""

    cmdout    = \
"""
qselect.py 1

qselect takes no arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_no_args_opts():
    """
    qselect test run: no_args_opts
        Old Command Output:
           {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'queue': 'jello', 'envs': {}, 'submittime': 60, 'state': '*', 'score': 50, 'location': '/tmp', 'nodes': 512, 'args': '', 'is_active': False, 'user': 'land', 'procs': 512, 'walltime': 5, 'geometry': None, 'user_hold': False, 'jobid': 100, 'project': 'my_project', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']} 
             The following jobs matched your query:
                100
          

    """

    args      = ''

    cmdout    = \
"""
qselect.py 

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:*
project:*
queue:*
state:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_debug_flag():
    """
    qselect test run: debug_flag
        Old Command Output:
           {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'queue': 'jello', 'envs': {}, 'submittime': 60, 'state': '*', 'score': 50, 'location': '/tmp', 'nodes': 512, 'args': '', 'is_active': False, 'user': 'land', 'procs': 512, 'walltime': 5, 'geometry': None, 'user_hold': False, 'jobid': 100, 'project': 'my_project', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']} 
             The following jobs matched your query:
                100
          

    """

    args      = """-d"""

    cmdout    = \
"""
qselect.py -d

[{'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': 60, 'state': '*', 'score': 50, 'location': '/tmp', 'nodes': 512, 'args': '', 'is_active': False, 'user': 'land', 'procs': 512, 'walltime': 5, 'geometry': None, 'user_hold': False, 'jobid': 100, 'queue': 'jello', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']}]
   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:*
project:*
queue:*
state:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_held_option():
    """
    qselect test run: held_option
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """-h user_hold"""

    cmdout    = \
"""
qselect.py -h user_hold

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:*
project:*
queue:*
state:user_hold
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_nodecount_option():
    """
    qselect test run: nodecount_option
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """-n 312"""

    cmdout    = \
"""
qselect.py -n 312

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:312
project:*
queue:*
state:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_state_and_nodecount():
    """
    qselect test run: state_and_nodecount
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """-n 312 -h user_hold"""

    cmdout    = \
"""
qselect.py -n 312 -h user_hold

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:312
project:*
queue:*
state:user_hold
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_walltime():
    """
    qselect test run: walltime
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """-t 10:10:10"""

    cmdout    = \
"""
qselect.py -t 10:10:10

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:*
project:*
queue:*
state:*
tag:job
walltime:610
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_mode():
    """
    qselect test run: mode
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """--mode vn"""

    cmdout    = \
"""
qselect.py --mode vn

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:vn
nodes:*
project:*
queue:*
state:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qselect_verbose():
    """
    qselect test run: verbose
        Old Command Output:
             The following jobs matched your query:
                100
          

    """

    args      = """-v"""

    cmdout    = \
"""
qselect.py -v

   The following jobs matched your query:
      100
"""

    stubout   = \
"""
GET_JOBS

jobid:*
mode:*
nodes:*
project:*
queue:*
state:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qselect.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

