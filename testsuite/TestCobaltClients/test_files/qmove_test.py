import testutils

# ---------------------------------------------------------------------------------
def test_qmove_invalid_option():
    """
    qmove test run: invalid_option

    """

    args      = """-k"""

    cmdout    = \
"""
qmove.py -k

Usage: qmove.py [options] <queue name> <jobid1> [... <jobidN>]

qmove.py: error: no such option: -k
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queue_1():
    """
    qmove test run: queue_1

    """

    args      = """myq 1 2 3"""

    cmdout    = \
"""
qmove.py myq 1 2 3

get_config_option: Option filters not found in section [cqm]
moved job 1 to queue 'myq'
moved job 2 to queue 'myq'
moved job 3 to queue 'myq'
"""

    stubout   = \
"""
GET_JOBS

jobid:1
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
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
is_active:False
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
is_active:False
jobid:1
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:myq
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
is_active:False
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
is_active:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:myq
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
is_active:False
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
is_active:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:myq
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queue_2():
    """
    qmove test run: queue_2

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""
qmove.py 1 2 3 4

get_config_option: Option filters not found in section [cqm]
moved job 2 to queue '1'
moved job 3 to queue '1'
moved job 4 to queue '1'
"""

    stubout   = \
"""
GET_JOBS

jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:georgerojas
walltime:*
jobid:4
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
is_active:False
jobid:2
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
is_active:False
jobid:2
location:/Users/georgerojas/myphthon
mode:smp
nodes:512
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:512
project:gdr_project
queue:1
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
is_active:False
jobid:3
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
is_active:False
jobid:3
location:/Users/georgerojas/myphthon
mode:smp
nodes:1024
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1024
project:gdr_project
queue:1
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:10

SET_JOBS


Original Jobs:

envs:
errorpath:/Users/georgerojas/mypython
has_completed:False
is_active:False
jobid:4
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
is_active:False
jobid:4
location:/Users/georgerojas/myphthon
mode:smp
nodes:1536
notify:george@therojas.com
outputpath:/Users/georgerojas/mypython
procs:1536
project:gdr_project
queue:1
state:user_hold
submittime:60
tag:job
user:georgerojas
user_hold:False
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queu_3():
    """
    qmove test run: queu_3

    """

    args      = """q1 q2 1 2 3"""

    cmdout    = \
"""
qmove.py q1 q2 1 2 3

jobid must be an integer: q2
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

