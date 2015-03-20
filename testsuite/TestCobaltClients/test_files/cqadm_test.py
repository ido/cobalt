import testutils

# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_1():
    """
    cqadm test run: getq_option_1

    """

    args      = """--getq"""

    cmdout    = \
"""Queue  Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=================================================================================================================================================================
aaa    dog    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    foo     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   wheel   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  bar     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

adminemail:*
adminemail type: <type 'str'>
cron:*
cron type: <type 'str'>
groups:*
groups type: <type 'str'>
maxnodehours:*
maxnodehours type: <type 'str'>
maxqueued:*
maxqueued type: <type 'str'>
maxrunning:*
maxrunning type: <type 'str'>
maxtime:*
maxtime type: <type 'str'>
maxuserjobs:*
maxuserjobs type: <type 'str'>
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
policy:*
policy type: <type 'str'>
priority:*
priority type: <type 'str'>
state:*
state type: <type 'str'>
tag:queue
tag type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_2():
    """
    cqadm test run: getq_option_2

    """

    args      = """-d --getq"""

    cmdout    = \
"""Queue  Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=================================================================================================================================================================
aaa    dog    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    foo     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   wheel   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  bar     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    cmderr    = \
"""
cqadm.py -d --getq

component: "queue-manager.get_queues", defer: True
  get_queues(
     [{'maxuserjobs': '*', 'priority': '*', 'name': '*', 'mintime': '*', 'maxusernodes': '*', 'totalnodes': '*', 'cron': '*', 'state': '*', 'tag': 'queue', 'maxqueued': '*', 'maxrunning': '*', 'groups': '*', 'maxnodehours': '*', 'policy': '*', 'maxtime': '*', 'adminemail': '*', 'users': '*'}],
     )


[{'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'james', 'name': 'kebra', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'land', 'name': 'jello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'house', 'name': 'bello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'dog', 'name': 'aaa', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': 'foo', 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'cat', 'name': 'bbb', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': 'bar', 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'henry', 'name': 'hhh', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': 'wheel', 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'king', 'name': 'dito', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'queen', 'name': 'myq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'girl', 'name': 'yours', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'maxusernodes': 20, 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'groups': None, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'users': 'boy', 'name': 'zq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}]
"""

    stubout   = \
"""
GET_QUEUES

adminemail:*
adminemail type: <type 'str'>
cron:*
cron type: <type 'str'>
groups:*
groups type: <type 'str'>
maxnodehours:*
maxnodehours type: <type 'str'>
maxqueued:*
maxqueued type: <type 'str'>
maxrunning:*
maxrunning type: <type 'str'>
maxtime:*
maxtime type: <type 'str'>
maxuserjobs:*
maxuserjobs type: <type 'str'>
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
policy:*
policy type: <type 'str'>
priority:*
priority type: <type 'str'>
state:*
state type: <type 'str'>
tag:queue
tag type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_3():
    """
    cqadm test run: getq_option_3

    """

    args      = """-f --getq"""

    cmdout    = \
"""Queue  Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
=================================================================================================================================================================
aaa    dog    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bbb    cat    foo     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
bello  house  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
dito   king   wheel   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
hhh    henry  bar     None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
jello  land   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
kebra  james  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
myq    queen  None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
yours  girl   None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
zq     boy    None    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

adminemail:*
adminemail type: <type 'str'>
cron:*
cron type: <type 'str'>
groups:*
groups type: <type 'str'>
maxnodehours:*
maxnodehours type: <type 'str'>
maxqueued:*
maxqueued type: <type 'str'>
maxrunning:*
maxrunning type: <type 'str'>
maxtime:*
maxtime type: <type 'str'>
maxuserjobs:*
maxuserjobs type: <type 'str'>
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
policy:*
policy type: <type 'str'>
priority:*
priority type: <type 'str'>
state:*
state type: <type 'str'>
tag:queue
tag type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_1():
    """
    cqadm test run: preempt_job_1

    """

    args      = """-d --preempt 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --preempt 1 2 3

component: "queue-manager.preempt_jobs", defer: True
  preempt_jobs(
     [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     gooduser,
     False,
     )


True
"""

    stubout   = \
"""
PREEMPT_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_2():
    """
    cqadm test run: preempt_job_2

    """

    args      = """-f --preempt 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
PREEMPT_JOBS

force:True
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_1():
    """
    cqadm test run: kill_job_1

    """

    args      = """-d -f --kill 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d -f --kill 1 2 3

component: "queue-manager.del_jobs", defer: False
  del_jobs(
     [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     True,
     gooduser,
     )


[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:True
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_2():
    """
    cqadm test run: kill_job_2

    """

    args      = """--kill 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_3():
    """
    cqadm test run: kill_job_3

    """

    args      = """-f --kill 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
DEL_JOBS

force:True
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_4():
    """
    cqadm test run: kill_job_4

    """

    args      = """-d --kill 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --kill 1 2 3

component: "queue-manager.del_jobs", defer: False
  del_jobs(
     [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     False,
     gooduser,
     )


[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_1():
    """
    cqadm test run: addq_option_1

    """

    args      = """--addq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_2():
    """
    cqadm test run: addq_option_2

    """

    args      = """--addq myq1 myq2 myq3"""

    cmdout    = \
"""Added Queues  
==============
myq1          
myq2          
myq3          
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

adminemail:*
adminemail type: <type 'str'>
cron:*
cron type: <type 'str'>
groups:*
groups type: <type 'str'>
maxnodehours:*
maxnodehours type: <type 'str'>
maxqueued:*
maxqueued type: <type 'str'>
maxrunning:*
maxrunning type: <type 'str'>
maxtime:*
maxtime type: <type 'str'>
maxuserjobs:*
maxuserjobs type: <type 'str'>
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
policy:*
policy type: <type 'str'>
priority:*
priority type: <type 'str'>
state:*
state type: <type 'str'>
tag:queue
tag type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>

ADD_QUEUES

whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_1():
    """
    cqadm test run: delq_option_1

    """

    args      = """--delq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_2():
    """
    cqadm test run: delq_option_2

    """

    args      = """--delq myq1 myq2 myq3"""

    cmdout    = \
"""Deleted Queues  
================
myq1            
myq2            
myq3            
"""

    cmderr    = ''

    stubout   = \
"""
DEL_QUEUES

force:False
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_1():
    """
    cqadm test run: stopq_option_1

    """

    args      = """--stopq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_2():
    """
    cqadm test run: stopq_option_2

    """

    args      = """--stopq myq1 myq2 myq3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'stopped'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_1():
    """
    cqadm test run: startq_option_1

    """

    args      = """--startq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_2():
    """
    cqadm test run: startq_option_2

    """

    args      = """--startq myq1 myq2 myq3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'running'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_1():
    """
    cqadm test run: drainq_option_1

    """

    args      = """--drainq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_2():
    """
    cqadm test run: drainq_option_2

    """

    args      = """--drainq myq1 myq2 myq3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'draining'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_1():
    """
    cqadm test run: killq_option_1

    """

    args      = """--killq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_2():
    """
    cqadm test run: killq_option_2

    """

    args      = """--killq myq1 myq2 myq3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'dead'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq3
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_1():
    """
    cqadm test run: policy_option_1

    """

    args      = """--policy"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --policy option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_2():
    """
    cqadm test run: policy_option_2

    """

    args      = """--policy 'mypolicy'"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_3():
    """
    cqadm test run: policy_option_3

    """

    args      = """--policy 'mypolicy' myq1 myq2"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'policy': 'mypolicy'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_1():
    """
    cqadm test run: setq_option_1

    """

    args      = """--setq"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setq option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_2():
    """
    cqadm test run: setq_option_2

    """

    args      = """--setq 'a=b b=c a=c'"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_3():
    """
    cqadm test run: setq_option_3

    """

    args      = """--setq 'a=b b=c a=c' myq1 myq2"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'a': 'c', 'b': 'c'}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_1():
    """
    cqadm test run: unsetq_option_1

    """

    args      = """--unsetq"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --unsetq option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_2():
    """
    cqadm test run: unsetq_option_2

    """

    args      = """--unsetq 'a b a'"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_3():
    """
    cqadm test run: unsetq_option_3

    """

    args      = """--unsetq 'a b a' myq1 myq2"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_QUEUES

queue data:{'a': None, 'b': None}
whoami:gooduser
name:myq1
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
name:myq2
name type: <type 'str'>
tag:queue
tag type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_1():
    """
    cqadm test run: setjobid_option_1

    """

    args      = """-j"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: -j option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_2():
    """
    cqadm test run: setjobid_option_2

    """

    args      = """--setjobid"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setjobid option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_3():
    """
    cqadm test run: setjobid_option_3

    """

    args      = """-j 1"""

    cmdout    = ''

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_4():
    """
    cqadm test run: setjobid_option_4

    """

    args      = """--setjobid 1"""

    cmdout    = ''

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_5():
    """
    cqadm test run: setjobid_option_5

    """

    args      = """-j 1 --setjobid 2"""

    cmdout    = ''

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_1():
    """
    cqadm test run: run_option_1

    """

    args      = """--run"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --run option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_2():
    """
    cqadm test run: run_option_2

    """

    args      = """--run mayaguez"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_3():
    """
    cqadm test run: run_option_3

    """

    args      = """--run mayaguez 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
GET_PARTITIONS

plist: [{'name': 'mayaguez'}]

RUN_JOBS

location:['mayaguez']
whoami:gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_1():
    """
    cqadm test run: hold_option_1

    """

    args      = """--hold"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_2():
    """
    cqadm test run: hold_option_2

    """

    args      = """--hold 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_3():
    """
    cqadm test run: hold_option_3

    """

    args      = """-d --hold  1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --hold 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'admin_hold': True},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_4():
    """
    cqadm test run: hold_option_4

    """

    args      = """-f --hold  1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_1():
    """
    cqadm test run: release_option_1

    """

    args      = """--release"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_2():
    """
    cqadm test run: release_option_2

    """

    args      = """--release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_3():
    """
    cqadm test run: release_option_3

    """

    args      = """-d --release 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --release 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'admin_hold': False},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_4():
    """
    cqadm test run: release_option_4

    """

    args      = """-f --release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_and_hold():
    """
    cqadm test run: release_and_hold

    """

    args      = """--hold --release 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""Attribute admin_hold already set
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_1():
    """
    cqadm test run: queue_option_1

    """

    args      = """--queue"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --queue option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_2():
    """
    cqadm test run: queue_option_2

    """

    args      = """--queue myq"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_3():
    """
    cqadm test run: queue_option_3

    """

    args      = """--queue myq 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

queue:myq
queue type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_1():
    """
    cqadm test run: time_option_1

    """

    args      = """--time"""

    cmdout    = ''

    cmderr    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --time option requires an argument
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_2():
    """
    cqadm test run: time_option_2

    """

    args      = """--time 50"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_4():
    """
    cqadm test run: time_option_4

    """

    args      = """--time 50 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

walltime:50
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_1():
    """
    cqadm test run: update_all_1

    """

    args      = """--hold --queue myq --time 50 4 5 6"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
queue:myq
queue type: <type 'str'>
walltime:50
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_2():
    """
    cqadm test run: update_all_2

    """

    args      = """--release --queue myq --time 50 4 5 6"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
queue:myq
queue type: <type 'str'>
walltime:50
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_addq():
    """
    cqadm test run: combine_getq_and_addq

    """

    args      = """--getq --addq myq1 myq2 myq3"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: addq, getq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_setjobid():
    """
    cqadm test run: combine_getq_and_setjobid

    """

    args      = """--getq -j 1 123"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: setjobid, getq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_time_and_getq():
    """
    cqadm test run: combine_time_and_getq

    """

    args      = """--time 50 --getq"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: getq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_release_and_getq():
    """
    cqadm test run: combine_release_and_getq

    """

    args      = """--release --getq 123"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: getq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_setq_with_queue():
    """
    cqadm test run: combine_setq_with_queue

    """

    args      = """--setq 'a=1 b=2' --queue q 1"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: setq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_delq():
    """
    cqadm test run: combine_addq_and_delq

    """

    args      = """--addq --delq q1 q2"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: addq, delq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_stopq():
    """
    cqadm test run: combine_addq_and_stopq

    """

    args      = """--stopq --addq q1 q2"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: addq, stopq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_startq():
    """
    cqadm test run: combine_addq_and_startq

    """

    args      = """--startq --addq q1 q2"""

    cmdout    = ''

    cmderr    = \
"""Option combinations not allowed with: addq, startq option(s)
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_hold_option_1():
    """
    cqadm test run: user_hold_option_1

    """

    args      = """--user-hold"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_hold_option_2():
    """
    cqadm test run: user_hold_option_2

    """

    args      = """--user-hold 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

New Job Info:

user_hold:True
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_hold_option_3():
    """
    cqadm test run: user_hold_option_3

    """

    args      = """-d --user-hold  1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --user-hold 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'user_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'user_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'user_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'user_hold': True},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

New Job Info:

user_hold:True
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_hold_option_4():
    """
    cqadm test run: user_hold_option_4

    """

    args      = """-f --user-hold  1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

New Job Info:

user_hold:True
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_release_option_1():
    """
    cqadm test run: user_release_option_1

    """

    args      = """--user-release"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_release_option_2():
    """
    cqadm test run: user_release_option_2

    """

    args      = """--user-release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_release_option_3():
    """
    cqadm test run: user_release_option_3

    """

    args      = """-d --user-release 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --user-release 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'user_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'user_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'user_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'user_hold': False},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_user_release_option_4():
    """
    cqadm test run: user_release_option_4

    """

    args      = """-f --user-release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
walltime:*
walltime type: <type 'str'>

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_hold_option_1():
    """
    cqadm test run: admin_hold_option_1

    """

    args      = """--admin-hold"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_hold_option_2():
    """
    cqadm test run: admin_hold_option_2

    """

    args      = """--admin-hold 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_hold_option_3():
    """
    cqadm test run: admin_hold_option_3

    """

    args      = """-d --admin-hold  1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --admin-hold 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'admin_hold': True},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_hold_option_4():
    """
    cqadm test run: admin_hold_option_4

    """

    args      = """-f --admin-hold  1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:False
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:False
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:True
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_release_option_1():
    """
    cqadm test run: admin_release_option_1

    """

    args      = """--admin-release"""

    cmdout    = \
"""Usage: cqadm.py --help
Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

"""

    cmderr    = \
"""No arguments or options provided

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_release_option_2():
    """
    cqadm test run: admin_release_option_2

    """

    args      = """--admin-release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_release_option_3():
    """
    cqadm test run: admin_release_option_3

    """

    args      = """-d --admin-release 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""
cqadm.py -d --admin-release 1 2 3

component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
     {'admin_hold': False},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
"""

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_admin_release_option_4():
    """
    cqadm test run: admin_release_option_4

    """

    args      = """-f --admin-release 1 2 3"""

    cmdout    = ''

    cmderr    = ''

    stubout   = \
"""
SET_JOBS


Original Jobs:

user: gooduser
admin_hold:True
admin_hold type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:True
admin_hold type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:*
location type: <type 'str'>
tag:job
tag type: <type 'str'>
walltime:*
walltime type: <type 'str'>

New Job Info:

admin_hold:False
admin_hold type: <type 'bool'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

