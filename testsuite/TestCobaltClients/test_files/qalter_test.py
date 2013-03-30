import testutils

# ---------------------------------------------------------------------------------
def test_qalter_simple_1():
    """
    qalter test run: simple_1

    """

    args      = """-d -n30"""

    cmdout    = \
"""
qalter.py -d -n30

No Jobid(s) given
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_simple_2():
    """
    qalter test run: simple_2

    """

    args      = """-d -n30 1"""

    cmdout    = \
"""
qalter.py -d -n30 1

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 30
nodes changed from 512 to 30
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 1, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 30, 'walltime': 5, 'user_hold': False, 'procs': 30, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:30
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:30
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_1():
    """
    qalter test run: time_1

    """

    args      = """-d -v n10 -t5 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v n10 -t5 1 2 3

jobid must be an integer: n10
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_2():
    """
    qalter test run: time_2

    """

    args      = """-d -v -n10 -t+5 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t+5 1 2 3

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 10.0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 15.0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 20.0
nodes changed from 1536 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 3, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': '20.0', 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:20.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_3():
    """
    qalter test run: time_3

    """

    args      = """-d -v -n10 -t+20 1 2 3 4 5 6 7"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t+20 1 2 3 4 5 6 7

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 25.0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 30.0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 35.0
nodes changed from 1536 to 10
procs changed from 2048 to 10
walltime changed from 20 to 40.0
nodes changed from 2048 to 10
procs changed from 2560 to 10
walltime changed from 25 to 45.0
nodes changed from 2560 to 10
procs changed from 3072 to 10
walltime changed from 30 to 50.0
nodes changed from 3072 to 10
procs changed from 3584 to 10
walltime changed from 35 to 55.0
nodes changed from 3584 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 7, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': '55.0', 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:6
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:7
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:25.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:35.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:2048
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2048
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:20

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:40.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:2560
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2560
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:25

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:45.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:6
location:/Users/georgerojas/myphthon
mode:smp
nodes:3072
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:3072
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:6
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:50.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:7
location:/Users/georgerojas/myphthon
mode:smp
nodes:3584
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:3584
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:35

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:7
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:55.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_4():
    """
    qalter test run: time_4

    """

    args      = """-d -v -n10 -t30 1 2 3 4 5 6 7 10 15"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t30 1 2 3 4 5 6 7 10 15

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 30
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 30
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 30
nodes changed from 1536 to 10
procs changed from 2048 to 10
walltime changed from 20 to 30
nodes changed from 2048 to 10
procs changed from 2560 to 10
walltime changed from 25 to 30
nodes changed from 2560 to 10
procs changed from 3072 to 10
nodes changed from 3072 to 10
procs changed from 3584 to 10
walltime changed from 35 to 30
nodes changed from 3584 to 10
procs changed from 4096 to 10
walltime changed from 40 to 30
nodes changed from 4096 to 10
procs changed from 4608 to 10
walltime changed from 45 to 30
nodes changed from 4608 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 15, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': 30, 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:6
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:7
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:10
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:15
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:2048
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2048
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:20

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:2560
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2560
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:25

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:6
location:/Users/georgerojas/myphthon
mode:smp
nodes:3072
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:3072
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:6
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:7
location:/Users/georgerojas/myphthon
mode:smp
nodes:3584
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:3584
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:35

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:7
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:10
location:/Users/georgerojas/myphthon
mode:smp
nodes:4096
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:4096
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:40

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:10
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:15
location:/Users/georgerojas/myphthon
mode:smp
nodes:4608
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:4608
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:45

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:15
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:30
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_5():
    """
    qalter test run: time_5

    """

    args      = """-d -v -n10 -t00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
nodes changed from 1536 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 3, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': 0, 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_6():
    """
    qalter test run: time_6

    """

    args      = """-d -v -n10 -t+00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t+00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
nodes changed from 1536 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 3, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': '15.0', 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_7():
    """
    qalter test run: time_7

    """

    args      = """-d -v -n10 -t 00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t 00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
nodes changed from 1536 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 3, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': 0, 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_8():
    """
    qalter test run: time_8

    """

    args      = """-d -v -n10 -t +00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t +00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 512 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1024 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
nodes changed from 1536 to 10
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 3, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'nodes': 10, 'walltime': '15.0', 'user_hold': False, 'procs': 10, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10.0

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:10
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:10
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_option():
    """
    qalter test run: invalid_option

    """

    args      = """-d -v -m j@gmail.com"""

    cmdout    = \
"""
qalter.py -d -v -m j@gmail.com

Usage: qalter.py [options] <jobids1> ... <jobidsN>

qalter.py: error: no such option: -m
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_email_option():
    """
    qalter test run: email_option

    """

    args      = """-d -v -M j@gmail.com 1 2"""

    cmdout    = \
"""
qalter.py -d -v -M j@gmail.com 1 2

get_config_option: Option filters not found in section [cqm]
notify changed from george@therojas.com to j@gmail.com
notify changed from george@therojas.com to j@gmail.com
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 2, 'project': 'gdr_project', 'submittime': 60, 'state': 'user_hold', 'tag': 'job', 'notify': 'j@gmail.com', 'envs': '', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:j@gmail.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:j@gmail.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_1():
    """
    qalter test run: mode_1

    """

    args      = """-d -v --mode jjj  -n40 -t50 -e p -o o 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v --mode jjj -n40 -t50 -e p -o o 1 2 3

Specifed mode 'jjj' not valid, valid modes are
co
vn
script
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_2():
    """
    qalter test run: mode_2

    """

    args      = """-d -v --mode dual -n40 -t50 -e p -o o 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v --mode dual -n40 -t50 -e p -o o 1 2 3

Specifed mode 'dual' not valid, valid modes are
co
vn
script
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_1():
    """
    qalter test run: proccount_1

    """

    args      = """-d -v --mode dual -n512 --proccount one -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = \
"""
qalter.py -d -v --mode dual -n512 --proccount one -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10

Specifed mode 'dual' not valid, valid modes are
co
vn
script
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_2():
    """
    qalter test run: proccount_2

    """

    args      = """-d -v --mode dual -n512 --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = \
"""
qalter.py -d -v --mode dual -n512 --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10

Specifed mode 'dual' not valid, valid modes are
co
vn
script
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_nodecount():
    """
    qalter test run: invalid_nodecount

    """

    args      = """-d -v --mode dual -nfiver --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = \
"""
qalter.py -d -v --mode dual -nfiver --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10

Specifed mode 'dual' not valid, valid modes are
co
vn
script
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_1():
    """
    qalter test run: user_1

    """

    args      = """-d -v --run_users georgerojas:georgerojas 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --run_users georgerojas:georgerojas 1 2 3 4 5

get_config_option: Option filters not found in section [cqm]
user_list set to ['georgerojas', 'georgerojas']
user_list set to ['georgerojas', 'georgerojas']
user_list set to ['georgerojas', 'georgerojas']
user_list set to ['georgerojas', 'georgerojas']
user_list set to ['georgerojas', 'georgerojas']
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'user_list': ['georgerojas', 'georgerojas'], 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 5, 'project': 'gdr_project', 'submittime': 60, 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'envs': '', 'nodes': 2560, 'walltime': 25, 'user_hold': False, 'procs': 2560, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas', 'georgerojas']
walltime:5

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas', 'georgerojas']
walltime:10

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas', 'georgerojas']
walltime:15

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:2048
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2048
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:20

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:2048
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2048
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas', 'georgerojas']
walltime:20

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:2560
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2560
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:25

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:5
location:/Users/georgerojas/myphthon
mode:smp
nodes:2560
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:2560
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas', 'georgerojas']
walltime:25
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_2():
    """
    qalter test run: user_2

    """

    args      = """-d -v --run_users georgerojas:george 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --run_users georgerojas:george 1 2 3 4 5

user george does not exist.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_project():
    """
    qalter test run: project

    """

    args      = """-d -v --run_project 10 20 30"""

    cmdout    = \
"""
qalter.py -d -v --run_project 10 20 30

get_config_option: Option filters not found in section [cqm]
user_list set to ['georgerojas']
run_project set to True
user_list set to ['georgerojas']
run_project set to True
user_list set to ['georgerojas']
run_project set to True
[{'queue': 'default', 'has_completed': False, 'errorpath': '/Users/georgerojas/mypython', 'submittime': 60, 'mode': 'smp', 'outputpath': '/Users/georgerojas/mypython', 'user_list': ['georgerojas'], 'is_active': False, 'location': '/Users/georgerojas/myphthon', 'jobid': 30, 'project': 'gdr_project', 'envs': '', 'state': 'user_hold', 'tag': 'job', 'notify': 'george@therojas.com', 'run_project': True, 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'georgerojas'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:10
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:20
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:30
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:10
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:5

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:10
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:default
run_project:True
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas']
walltime:5

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:20
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:20
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:default
run_project:True
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas']
walltime:10

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:30
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15

New Job Info:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
jobid:30
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:default
run_project:True
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
user_list:['georgerojas']
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_1():
    """
    qalter test run: geometry_1

    """

    args      = """-d -v --geometry 10 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --geometry 10 1 2 3 4 5

Invalid geometry entered: 
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_2():
    """
    qalter test run: geometry_2

    """

    args      = """-d -v --geometry 10x10x10x10x10 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --geometry 10x10x10x10x10 1 2 3 4 5

get_config_option: Option filters not found in section [cqm]
Geometry specification 10x10x10x10x10 is invalid.
Jobs not altered.
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_3():
    """
    qalter test run: geometry_3

    """

    args      = """-d -v --geometry 04x04x04x04x04 1 2 3 4"""

    cmdout    = \
"""
qalter.py -d -v --geometry 04x04x04x04x04 1 2 3 4

get_config_option: Option filters not found in section [cqm]
Geometry requires more nodes than specified for job.
Jobs not altered.
"""

    stubout   = \
"""
GET_JOBS

is_active:*
jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

