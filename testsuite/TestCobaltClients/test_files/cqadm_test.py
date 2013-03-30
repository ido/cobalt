import testutils

# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_1():
    """
    cqadm test run: getq_option_1

    """

    args      = """--getq"""

    cmdout    = \
"""
cqadm.py --getq

Queue   Users        MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail           State    Cron      Policy    Priority  
==================================================================================================================================================================
queue1  rojas:rich   None     None     20          20         20            20            100         george@therojas.com  running  whocares  mypolicy  urgent    
queue2  georgerojas  None     None     21          21         21            21            101         george@therojas.com  running  whocares  mypolicy  urgent    
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_2():
    """
    cqadm test run: getq_option_2

    """

    args      = """-d --getq"""

    cmdout    = \
"""
cqadm.py -d --getq

[{'users': 'rojas:rich', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'george@therojas.com', 'name': 'queue1', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'georgerojas', 'mintime': None, 'totalnodes': 101, 'cron': 'whocares', 'maxqueued': 21, 'maxusernodes': 21, 'maxnodehours': 21, 'maxtime': None, 'adminemail': 'george@therojas.com', 'name': 'queue2', 'priority': 'urgent', 'state': 'running', 'maxrunning': 21, 'policy': 'mypolicy'}]
Queue   Users        MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail           State    Cron      Policy    Priority  
==================================================================================================================================================================
queue1  rojas:rich   None     None     20          20         20            20            100         george@therojas.com  running  whocares  mypolicy  urgent    
queue2  georgerojas  None     None     21          21         21            21            101         george@therojas.com  running  whocares  mypolicy  urgent    
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_3():
    """
    cqadm test run: getq_option_3

    """

    args      = """-f --getq"""

    cmdout    = \
"""
cqadm.py -f --getq

Queue   Users        MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail           State    Cron      Policy    Priority  
==================================================================================================================================================================
queue1  rojas:rich   None     None     20          20         20            20            100         george@therojas.com  running  whocares  mypolicy  urgent    
queue2  georgerojas  None     None     21          21         21            21            101         george@therojas.com  running  whocares  mypolicy  urgent    
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_1():
    """
    cqadm test run: preempt_job_1

    """

    args      = """-d --preempt 1 2 3"""

    cmdout    = \
"""
cqadm.py -d --preempt 1 2 3

True
"""

    stubout   = \
"""
PREEMPT_JOBS

force:False
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_preempt_job_2():
    """
    cqadm test run: preempt_job_2

    """

    args      = """-f --preempt 1 2 3"""

    cmdout    = \
"""
cqadm.py -f --preempt 1 2 3

"""

    stubout   = \
"""
PREEMPT_JOBS

force:True
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_1():
    """
    cqadm test run: kill_job_1

    """

    args      = """-d -f --kill 1 2 3"""

    cmdout    = \
"""
cqadm.py -d -f --kill 1 2 3

[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:True
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_2():
    """
    cqadm test run: kill_job_2

    """

    args      = """--kill 1 2 3"""

    cmdout    = \
"""
cqadm.py --kill 1 2 3

"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_3():
    """
    cqadm test run: kill_job_3

    """

    args      = """-f --kill 1 2 3"""

    cmdout    = \
"""
cqadm.py -f --kill 1 2 3

"""

    stubout   = \
"""
DEL_JOBS

force:True
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_kill_job_4():
    """
    cqadm test run: kill_job_4

    """

    args      = """-d --kill 1 2 3"""

    cmdout    = \
"""
cqadm.py -d --kill 1 2 3

[{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
"""

    stubout   = \
"""
DEL_JOBS

force:False
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_1():
    """
    cqadm test run: addq_option_1

    """

    args      = """--addq"""

    cmdout    = \
"""
cqadm.py --addq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_addq_option_2():
    """
    cqadm test run: addq_option_2

    """

    args      = """--addq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --addq myq1 myq2 myq3

Added Queues  
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

whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_1():
    """
    cqadm test run: delq_option_1

    """

    args      = """--delq"""

    cmdout    = \
"""
cqadm.py --delq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_delq_option_2():
    """
    cqadm test run: delq_option_2

    """

    args      = """--delq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --delq myq1 myq2 myq3

Deleted Queues  
================
myq1            
myq2            
myq3            
"""

    stubout   = \
"""
DEL_QUEUES

force:False
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_1():
    """
    cqadm test run: stopq_option_1

    """

    args      = """--stopq"""

    cmdout    = \
"""
cqadm.py --stopq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_stopq_option_2():
    """
    cqadm test run: stopq_option_2

    """

    args      = """--stopq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --stopq myq1 myq2 myq3

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'stopped'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_1():
    """
    cqadm test run: startq_option_1

    """

    args      = """--startq"""

    cmdout    = \
"""
cqadm.py --startq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_startq_option_2():
    """
    cqadm test run: startq_option_2

    """

    args      = """--startq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --startq myq1 myq2 myq3

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'running'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_1():
    """
    cqadm test run: drainq_option_1

    """

    args      = """--drainq"""

    cmdout    = \
"""
cqadm.py --drainq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_drainq_option_2():
    """
    cqadm test run: drainq_option_2

    """

    args      = """--drainq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --drainq myq1 myq2 myq3

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'draining'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_1():
    """
    cqadm test run: killq_option_1

    """

    args      = """--killq"""

    cmdout    = \
"""
cqadm.py --killq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_killq_option_2():
    """
    cqadm test run: killq_option_2

    """

    args      = """--killq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --killq myq1 myq2 myq3

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'state': 'dead'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_1():
    """
    cqadm test run: policy_option_1

    """

    args      = """--policy"""

    cmdout    = \
"""
cqadm.py --policy

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --policy option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_2():
    """
    cqadm test run: policy_option_2

    """

    args      = """--policy 'mypolicy'"""

    cmdout    = \
"""
cqadm.py --policy mypolicy

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_policy_option_3():
    """
    cqadm test run: policy_option_3

    """

    args      = """--policy 'mypolicy' myq1 myq2"""

    cmdout    = \
"""
cqadm.py --policy mypolicy myq1 myq2

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'policy': 'mypolicy'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_1():
    """
    cqadm test run: setq_option_1

    """

    args      = """--setq"""

    cmdout    = \
"""
cqadm.py --setq

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setq option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_2():
    """
    cqadm test run: setq_option_2

    """

    args      = """--setq 'a=b b=c a=c'"""

    cmdout    = \
"""
cqadm.py --setq a=b b=c a=c

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setq_option_3():
    """
    cqadm test run: setq_option_3

    """

    args      = """--setq 'a=b b=c a=c' myq1 myq2"""

    cmdout    = \
"""
cqadm.py --setq a=b b=c a=c myq1 myq2

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'a': 'c', 'b': 'c'}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_1():
    """
    cqadm test run: unsetq_option_1

    """

    args      = """--unsetq"""

    cmdout    = \
"""
cqadm.py --unsetq

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --unsetq option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_2():
    """
    cqadm test run: unsetq_option_2

    """

    args      = """--unsetq 'a b a'"""

    cmdout    = \
"""
cqadm.py --unsetq a b a

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_unsetq_option_3():
    """
    cqadm test run: unsetq_option_3

    """

    args      = """--unsetq 'a b a' myq1 myq2"""

    cmdout    = \
"""
cqadm.py --unsetq a b a myq1 myq2

"""

    stubout   = \
"""
SET_QUEUES

queue data:{'a': None, 'b': None}
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_1():
    """
    cqadm test run: setjobid_option_1

    """

    args      = """-j"""

    cmdout    = \
"""
cqadm.py -j

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: -j option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_2():
    """
    cqadm test run: setjobid_option_2

    """

    args      = """--setjobid"""

    cmdout    = \
"""
cqadm.py --setjobid

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --setjobid option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_3():
    """
    cqadm test run: setjobid_option_3

    """

    args      = """-j 1"""

    cmdout    = \
"""
cqadm.py -j 1

"""

    stubout   = \
"""
SET_JOBID

jobid:1
whoami:georgerojas
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_4():
    """
    cqadm test run: setjobid_option_4

    """

    args      = """--setjobid 1"""

    cmdout    = \
"""
cqadm.py --setjobid 1

"""

    stubout   = \
"""
SET_JOBID

jobid:1
whoami:georgerojas
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_setjobid_option_5():
    """
    cqadm test run: setjobid_option_5

    """

    args      = """-j 1 --setjobid 2"""

    cmdout    = \
"""
cqadm.py -j 1 --setjobid 2

"""

    stubout   = \
"""
SET_JOBID

jobid:2
whoami:georgerojas
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_1():
    """
    cqadm test run: run_option_1

    """

    args      = """--run"""

    cmdout    = \
"""
cqadm.py --run

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --run option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_2():
    """
    cqadm test run: run_option_2

    """

    args      = """--run mayaguez"""

    cmdout    = \
"""
cqadm.py --run mayaguez

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_run_option_3():
    """
    cqadm test run: run_option_3

    """

    args      = """--run mayaguez 1 2 3"""

    cmdout    = \
"""
cqadm.py --run mayaguez 1 2 3

"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'name': 'mayaguez'}]

RUN_JOBS

location:['mayaguez']
whoami:georgerojas
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_1():
    """
    cqadm test run: hold_option_1

    """

    args      = """--hold"""

    cmdout    = \
"""
cqadm.py --hold

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_2():
    """
    cqadm test run: hold_option_2

    """

    args      = """--hold 1 2 3"""

    cmdout    = \
"""
cqadm.py --hold 1 2 3

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_3():
    """
    cqadm test run: hold_option_3

    """

    args      = """-d --hold  1 2 3"""

    cmdout    = \
"""
cqadm.py -d --hold 1 2 3

[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': True, 'jobid': 1, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'georgerojas'}, {'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': True, 'jobid': 2, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'georgerojas'}, {'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': True, 'jobid': 3, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'georgerojas'}]
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_hold_option_4():
    """
    cqadm test run: hold_option_4

    """

    args      = """-f --hold  1 2 3"""

    cmdout    = \
"""
cqadm.py -f --hold 1 2 3

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_1():
    """
    cqadm test run: release_option_1

    """

    args      = """--release"""

    cmdout    = \
"""
cqadm.py --release

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_2():
    """
    cqadm test run: release_option_2

    """

    args      = """--release 1 2 3"""

    cmdout    = \
"""
cqadm.py --release 1 2 3

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_3():
    """
    cqadm test run: release_option_3

    """

    args      = """-d --release 1 2 3"""

    cmdout    = \
"""
cqadm.py -d --release 1 2 3

[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': False, 'jobid': 1, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'georgerojas'}, {'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': False, 'jobid': 2, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'georgerojas'}, {'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'admin_hold': False, 'jobid': 3, 'project': 'gdr_project', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'georgerojas'}]
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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_option_4():
    """
    cqadm test run: release_option_4

    """

    args      = """-f --release 1 2 3"""

    cmdout    = \
"""
cqadm.py -f --release 1 2 3

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_release_and_hold():
    """
    cqadm test run: release_and_hold

    """

    args      = """--hold --release 1 2 3"""

    cmdout    = \
"""
cqadm.py --hold --release 1 2 3

Attribute admin_hold already set
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_1():
    """
    cqadm test run: queue_option_1

    """

    args      = """--queue"""

    cmdout    = \
"""
cqadm.py --queue

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --queue option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_2():
    """
    cqadm test run: queue_option_2

    """

    args      = """--queue myq"""

    cmdout    = \
"""
cqadm.py --queue myq

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_queue_option_3():
    """
    cqadm test run: queue_option_3

    """

    args      = """--queue myq 1 2 3"""

    cmdout    = \
"""
cqadm.py --queue myq 1 2 3

"""

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_1():
    """
    cqadm test run: time_option_1

    """

    args      = """--time"""

    cmdout    = \
"""
cqadm.py --time

Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>

cqadm.py: error: --time option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_2():
    """
    cqadm test run: time_option_2

    """

    args      = """--time 50"""

    cmdout    = \
"""
cqadm.py --time 50

At least on jobid or queue name must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_time_option_4():
    """
    cqadm test run: time_option_4

    """

    args      = """--time 50 1 2 3"""

    cmdout    = \
"""
cqadm.py --time 50 1 2 3

"""

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_1():
    """
    cqadm test run: update_all_1

    """

    args      = """--hold --queue myq --time 50 4 5 6"""

    cmdout    = \
"""
cqadm.py --hold --queue myq --time 50 4 5 6

"""

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_update_all_2():
    """
    cqadm test run: update_all_2

    """

    args      = """--release --queue myq --time 50 4 5 6"""

    cmdout    = \
"""
cqadm.py --release --queue myq --time 50 4 5 6

"""

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

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_addq():
    """
    cqadm test run: combine_getq_and_addq

    """

    args      = """--getq --addq myq1 myq2 myq3"""

    cmdout    = \
"""
cqadm.py --getq --addq myq1 myq2 myq3

Option combinations not allowed with: addq, getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_getq_and_setjobid():
    """
    cqadm test run: combine_getq_and_setjobid

    """

    args      = """--getq -j 1 123"""

    cmdout    = \
"""
cqadm.py --getq -j 1 123

Option combinations not allowed with: setjobid, getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_time_and_getq():
    """
    cqadm test run: combine_time_and_getq

    """

    args      = """--time 50 --getq"""

    cmdout    = \
"""
cqadm.py --time 50 --getq

Option combinations not allowed with: getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_release_and_getq():
    """
    cqadm test run: combine_release_and_getq

    """

    args      = """--release --getq 123"""

    cmdout    = \
"""
cqadm.py --release --getq 123

Option combinations not allowed with: getq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_setq_with_queue():
    """
    cqadm test run: combine_setq_with_queue

    """

    args      = """--setq 'a=1 b=2' --queue q 1"""

    cmdout    = \
"""
cqadm.py --setq a=1 b=2 --queue q 1

Option combinations not allowed with: setq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_delq():
    """
    cqadm test run: combine_addq_and_delq

    """

    args      = """--addq --delq q1 q2"""

    cmdout    = \
"""
cqadm.py --addq --delq q1 q2

Option combinations not allowed with: addq, delq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_stopq():
    """
    cqadm test run: combine_addq_and_stopq

    """

    args      = """--stopq --addq q1 q2"""

    cmdout    = \
"""
cqadm.py --stopq --addq q1 q2

Option combinations not allowed with: addq, stopq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_cqadm_combine_addq_and_startq():
    """
    cqadm test run: combine_addq_and_startq

    """

    args      = """--startq --addq q1 q2"""

    cmdout    = \
"""
cqadm.py --startq --addq q1 q2

Option combinations not allowed with: addq, startq option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('cqadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

