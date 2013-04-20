import testutils

# ---------------------------------------------------------------------------------
def test_qmove_invalid_option():
    """
    qmove test run: invalid_option
        Old Command Output:
          Usage:
          qmove <queue name> <jobid> <jobid>
          

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
        Old Command Output:
          moved job 1 to queue 'kebra'
          moved job 2 to queue 'kebra'
          moved job 3 to queue 'kebra'
          

    """

    args      = """myq 1 2 3"""

    cmdout    = \
"""
qmove.py myq 1 2 3

get_config_option: Option filters not found in section [cqm]
moved job 1 to queue 'kebra'
moved job 2 to queue 'kebra'
moved job 3 to queue 'kebra'
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
user:gooduser
walltime:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:1
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:1
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:myq
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:2
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:2
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:myq
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:3
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:15

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:3
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:myq
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
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
        Old Command Output:
          moved job 2 to queue 'kebra'
          moved job 3 to queue 'kebra'
          moved job 4 to queue 'kebra'
          

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""
qmove.py 1 2 3 4

get_config_option: Option filters not found in section [cqm]
moved job 2 to queue 'kebra'
moved job 3 to queue 'kebra'
moved job 4 to queue 'kebra'
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
user:gooduser
walltime:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:2
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:2
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:1
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:3
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:3
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:1
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:4
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:15

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
is_active:False
jobid:4
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:1
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
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
        Old Command Output:
          jobid must be an integer
          

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

