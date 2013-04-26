import testutils

# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_1():
    """
    cqadm test run: getq_option_1
        Old Command Output:
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """--getq"""

    cmdout    = \
"""Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=========================================================================================================================================================
aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    stubout   = \
"""
GET_QUEUES

adminemail:*
cron:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxuserjobs:*
maxusernodes:*
mintime:*
name:*
policy:*
priority:*
state:*
tag:queue
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_2():
    """
    cqadm test run: getq_option_2
        Old Command Output:
           {'users': 'dog', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'aaa', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}      {'users': 'cat', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bbb', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}      {'users': 'house', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}  {'users': 'king', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'dito', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}    {'users': 'henry', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'hhh', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}    {'users': 'land', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'jello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}   {'users': 'james', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'kebra', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}  {'users': 'queen', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'myq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}    {'users': 'girl', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'yours', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}   {'users': 'boy', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'zq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}      
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """-d --getq"""

    cmdout    = \
"""[{'users': 'james', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'kebra', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'land', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'jello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'house', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'dog', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'aaa', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'cat', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bbb', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'henry', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'hhh', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'king', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'dito', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'queen', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'myq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'girl', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'yours', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'boy', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'zq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}]
Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=========================================================================================================================================================
aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    stubout   = \
"""
GET_QUEUES

adminemail:*
cron:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxuserjobs:*
maxusernodes:*
mintime:*
name:*
policy:*
priority:*
state:*
tag:queue
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_3():
    """
    cqadm test run: getq_option_3
        Old Command Output:
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """-f --getq"""

    cmdout    = \
"""Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=========================================================================================================================================================
aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    stubout   = \
"""
GET_QUEUES

adminemail:*
cron:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxuserjobs:*
maxusernodes:*
mintime:*
name:*
policy:*
priority:*
state:*
tag:queue
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_1():
    """
    cqadm test run: preempt_job_1
        Old Command Output:
          True
          

    """

    args      = """-d --preempt 1 2 3"""

    cmdout    = \
"""True
"""

    stubout   = \
"""
PREEMPT_JOBS

force:False
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_2():
    """
    cqadm test run: preempt_job_2
        Old Command Output:
          

    """

    args      = """-f --preempt 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
PREEMPT_JOBS

force:True
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_1():
    """
    cqadm test run: kill_job_1
        Old Command Output:
          

    """

    args      = """-d -f --kill 1 2 3"""

    cmdout    = \
"""[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:True
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_2():
    """
    cqadm test run: kill_job_2
        Old Command Output:
          

    """

    args      = """--kill 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_3():
    """
    cqadm test run: kill_job_3
        Old Command Output:
           {'tag': 'job', 'jobid': 1, 'location': '*', 'walltime': '*'}  {'tag': 'job', 'jobid': 2, 'location': '*', 'walltime': '*'}  {'tag': 'job', 'jobid': 3, 'location': '*', 'walltime': '*'} 
          

    """

    args      = """-f --kill 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
DEL_JOBS

force:True
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_4():
    """
    cqadm test run: kill_job_4
        Old Command Output:
           {'tag': 'job', 'jobid': 1, 'location': '*', 'walltime': '*'}  {'tag': 'job', 'jobid': 2, 'location': '*', 'walltime': '*'}  {'tag': 'job', 'jobid': 3, 'location': '*', 'walltime': '*'} 
          

    """

    args      = """-d --kill 1 2 3"""

    cmdout    = \
"""[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_1():
    """
    cqadm test run: addq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--addq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_2():
    """
    cqadm test run: addq_option_2
        Old Command Output:
          Added Queues  
          ==============
          myq1          
          myq2          
          myq3          
          

    """

    args      = """--addq myq1 myq2 myq3"""

    cmdout    = \
"""Added Queues  
==============
myq1          
myq2          
myq3          
"""

    stubout   = \
"""
GET_QUEUES

adminemail:*
cron:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxuserjobs:*
maxusernodes:*
mintime:*
name:*
policy:*
priority:*
state:*
tag:queue
totalnodes:*
users:*

ADD_QUEUES

whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_1():
    """
    cqadm test run: delq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--delq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_2():
    """
    cqadm test run: delq_option_2
        Old Command Output:
          Deleted Queues  
          ================
          myq1            
          myq2            
          myq3            
          

    """

    args      = """--delq myq1 myq2 myq3"""

    cmdout    = \
"""Deleted Queues  
================
myq1            
myq2            
myq3            
"""

    stubout   = \
"""
DEL_QUEUES

force:False
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_1():
    """
    cqadm test run: stopq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--stopq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_2():
    """
    cqadm test run: stopq_option_2
        Old Command Output:
          

    """

    args      = """--stopq myq1 myq2 myq3"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'stopped'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_1():
    """
    cqadm test run: startq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--startq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_2():
    """
    cqadm test run: startq_option_2
        Old Command Output:
          

    """

    args      = """--startq myq1 myq2 myq3"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'running'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_1():
    """
    cqadm test run: drainq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--drainq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_2():
    """
    cqadm test run: drainq_option_2
        Old Command Output:
          

    """

    args      = """--drainq myq1 myq2 myq3"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'draining'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_1():
    """
    cqadm test run: killq_option_1
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--killq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_2():
    """
    cqadm test run: killq_option_2
        Old Command Output:
          

    """

    args      = """--killq myq1 myq2 myq3"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'dead'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
name:myq3
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_1():
    """
    cqadm test run: policy_option_1
        Old Command Output:
          option --policy requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--policy"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --policy option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_2():
    """
    cqadm test run: policy_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--policy 'mypolicy'"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_3():
    """
    cqadm test run: policy_option_3
        Old Command Output:
          

    """

    args      = """--policy 'mypolicy' myq1 myq2"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'policy': 'mypolicy'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_1():
    """
    cqadm test run: setq_option_1
        Old Command Output:
          option --setq requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--setq"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setq option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_2():
    """
    cqadm test run: setq_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--setq 'a=b b=c a=c'"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_3():
    """
    cqadm test run: setq_option_3
        Old Command Output:
          

    """

    args      = """--setq 'a=b b=c a=c' myq1 myq2"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'a': 'c', 'b': 'c'}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_1():
    """
    cqadm test run: unsetq_option_1
        Old Command Output:
          option --unsetq requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--unsetq"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --unsetq option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_2():
    """
    cqadm test run: unsetq_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--unsetq 'a b a'"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_3():
    """
    cqadm test run: unsetq_option_3
        Old Command Output:
          

    """

    args      = """--unsetq 'a b a' myq1 myq2"""

    cmdout    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'a': None, 'b': None}
whoami:gooduser
name:myq1
tag:queue
name:myq2
tag:queue
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_1():
    """
    cqadm test run: setjobid_option_1
        Old Command Output:
          option -j requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """-j"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: -j option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_2():
    """
    cqadm test run: setjobid_option_2
        Old Command Output:
          option --setjobid requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--setjobid"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setjobid option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_3():
    """
    cqadm test run: setjobid_option_3
        Old Command Output:
          

    """

    args      = """-j 1"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBID

jobid:1
whoami:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_4():
    """
    cqadm test run: setjobid_option_4
        Old Command Output:
          

    """

    args      = """--setjobid 1"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBID

jobid:1
whoami:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_5():
    """
    cqadm test run: setjobid_option_5
        Old Command Output:
          

    """

    args      = """-j 1 --setjobid 2"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBID

jobid:2
whoami:gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_1():
    """
    cqadm test run: run_option_1
        Old Command Output:
          option --run requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--run"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --run option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_2():
    """
    cqadm test run: run_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--run mayaguez"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_3():
    """
    cqadm test run: run_option_3
        Old Command Output:
          

    """

    args      = """--run mayaguez 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'name': 'mayaguez'}]

RUN_JOBS

location:['mayaguez']
whoami:gooduser
jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_1():
    """
    cqadm test run: hold_option_1
        Old Command Output:
          you must specify a jobid to hold
          

    """

    args      = """--hold"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_2():
    """
    cqadm test run: hold_option_2
        Old Command Output:
          

    """

    args      = """--hold 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:False
jobid:1
location:*
tag:job
walltime:*
admin_hold:False
jobid:2
location:*
tag:job
walltime:*
admin_hold:False
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_3():
    """
    cqadm test run: hold_option_3
        Old Command Output:
           {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 512, 'walltime': 5, 'project': 'my_project', 'user_hold': False, 'jobid': 1, 'queue': 'kebra', 'mode': 'smp', 'nodes': 512, 'user': 'james'}     {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 1024, 'walltime': 10, 'project': 'my_project', 'user_hold': False, 'jobid': 2, 'queue': 'jello', 'mode': 'smp', 'nodes': 1024, 'user': 'land'}   {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 1536, 'walltime': 15, 'project': 'my_project', 'user_hold': False, 'jobid': 3, 'queue': 'bello', 'mode': 'smp', 'nodes': 1536, 'user': 'house'} 
          

    """

    args      = """-d --hold  1 2 3"""

    cmdout    = \
"""[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:False
jobid:1
location:*
tag:job
walltime:*
admin_hold:False
jobid:2
location:*
tag:job
walltime:*
admin_hold:False
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_4():
    """
    cqadm test run: hold_option_4
        Old Command Output:
          

    """

    args      = """-f --hold  1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:False
jobid:1
location:*
tag:job
walltime:*
admin_hold:False
jobid:2
location:*
tag:job
walltime:*
admin_hold:False
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:True
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_1():
    """
    cqadm test run: release_option_1
        Old Command Output:
          you must specify a jobid to release
          

    """

    args      = """--release"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_2():
    """
    cqadm test run: release_option_2
        Old Command Output:
          

    """

    args      = """--release 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:True
jobid:1
location:*
tag:job
walltime:*
admin_hold:True
jobid:2
location:*
tag:job
walltime:*
admin_hold:True
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_3():
    """
    cqadm test run: release_option_3
        Old Command Output:
           {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 512, 'walltime': 5, 'project': 'my_project', 'user_hold': False, 'jobid': 1, 'queue': 'kebra', 'mode': 'smp', 'nodes': 512, 'user': 'james'}     {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 1024, 'walltime': 10, 'project': 'my_project', 'user_hold': False, 'jobid': 2, 'queue': 'jello', 'mode': 'smp', 'nodes': 1024, 'user': 'land'}   {'errorpath': '/tmp', 'is_active': False, 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemag@gmail.com', 'has_completed': False, 'procs': 1536, 'walltime': 15, 'project': 'my_project', 'user_hold': False, 'jobid': 3, 'queue': 'bello', 'mode': 'smp', 'nodes': 1536, 'user': 'house'} 
          

    """

    args      = """-d --release 1 2 3"""

    cmdout    = \
"""[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:True
jobid:1
location:*
tag:job
walltime:*
admin_hold:True
jobid:2
location:*
tag:job
walltime:*
admin_hold:True
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_4():
    """
    cqadm test run: release_option_4
        Old Command Output:
          

    """

    args      = """-f --release 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:True
jobid:1
location:*
tag:job
walltime:*
admin_hold:True
jobid:2
location:*
tag:job
walltime:*
admin_hold:True
jobid:3
location:*
tag:job
walltime:*

New Job Info:

admin_hold:False
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_and_hold():
    """
    cqadm test run: release_and_hold
        Old Command Output:
          Only one of --hold or --release can be used at once
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--hold --release 1 2 3"""

    cmdout    = \
"""Attribute admin_hold already set
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_1():
    """
    cqadm test run: queue_option_1
        Old Command Output:
          option --queue requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--queue"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --queue option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_2():
    """
    cqadm test run: queue_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--queue myq"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_3():
    """
    cqadm test run: queue_option_3
        Old Command Output:
          

    """

    args      = """--queue myq 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*

New Job Info:

queue:myq
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_1():
    """
    cqadm test run: time_option_1
        Old Command Output:
          option --time requires argument
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--time"""

    cmdout    = \
"""Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --time option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_2():
    """
    cqadm test run: time_option_2
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--time 50"""

    cmdout    = \
"""At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_4():
    """
    cqadm test run: time_option_4
        Old Command Output:
          

    """

    args      = """--time 50 1 2 3"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

jobid:1
location:*
tag:job
walltime:*
jobid:2
location:*
tag:job
walltime:*
jobid:3
location:*
tag:job
walltime:*

New Job Info:

walltime:50
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_1():
    """
    cqadm test run: update_all_1
        Old Command Output:
          

    """

    args      = """--hold --queue myq --time 50 4 5 6"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:False
jobid:4
location:*
tag:job
walltime:*
admin_hold:False
jobid:5
location:*
tag:job
walltime:*
admin_hold:False
jobid:6
location:*
tag:job
walltime:*

New Job Info:

admin_hold:True
queue:myq
walltime:50
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_2():
    """
    cqadm test run: update_all_2
        Old Command Output:
          

    """

    args      = """--release --queue myq --time 50 4 5 6"""

    cmdout    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

admin_hold:True
jobid:4
location:*
tag:job
walltime:*
admin_hold:True
jobid:5
location:*
tag:job
walltime:*
admin_hold:True
jobid:6
location:*
tag:job
walltime:*

New Job Info:

admin_hold:False
queue:myq
walltime:50
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_addq():
    """
    cqadm test run: combine_getq_and_addq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--getq --addq myq1 myq2 myq3"""

    cmdout    = \
"""Option combinations not allowed with: addq, getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_setjobid():
    """
    cqadm test run: combine_getq_and_setjobid
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--getq -j 1 123"""

    cmdout    = \
"""Option combinations not allowed with: setjobid, getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_time_and_getq():
    """
    cqadm test run: combine_time_and_getq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--time 50 --getq"""

    cmdout    = \
"""Option combinations not allowed with: getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_release_and_getq():
    """
    cqadm test run: combine_release_and_getq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--release --getq 123"""

    cmdout    = \
"""Option combinations not allowed with: getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_setq_with_queue():
    """
    cqadm test run: combine_setq_with_queue
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--setq 'a=1 b=2' --queue q 1"""

    cmdout    = \
"""Option combinations not allowed with: setq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_delq():
    """
    cqadm test run: combine_addq_and_delq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--addq --delq q1 q2"""

    cmdout    = \
"""Option combinations not allowed with: addq, delq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_stopq():
    """
    cqadm test run: combine_addq_and_stopq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--stopq --addq q1 q2"""

    cmdout    = \
"""Option combinations not allowed with: addq, stopq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_startq():
    """
    cqadm test run: combine_addq_and_startq
        Old Command Output:
          At least one jobid or queue name must be supplied
          Usage: cqadm [--version] [-d] [--hold] [--release] [--run=<location>] [--preempt] [--kill] [--delete] [--queue=queuename] [--time=time] <jobid> <jobid>
                 cqadm [-d] [-f] [--addq] [--delq] [--getq] [--stopq] [--startq] [--drainq] [--killq] [--setq "property=value property=value"] [--unsetq "property property"] --policy=<qpolicy> <queue> <queue>
                 cqadm [-j <next jobid>]
                 cqadm [--savestate <filename>]
          

    """

    args      = """--startq --addq q1 q2"""

    cmdout    = \
"""Option combinations not allowed with: addq, startq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

