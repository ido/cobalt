import testutils

# ---------------------------------------------------------------------------------
def test_qalter_simple_1():
    """
    qalter test run: simple_1
        Old Command Output:
          Failed to match any jobs
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_simple_2():
    """
    qalter test run: simple_2
        Old Command Output:
          True
          nodes changed from 512 to 30
          procs changed from 512 to 30
          

    """

    args      = """-d -n30 1"""

    cmdout    = \
"""
qalter.py -d -n30 1

get_config_option: Option filters not found in section [cqm]
nodes changed from 512 to 30
procs changed from 512 to 30
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:1
location:/tmp
mode:smp
nodes:30
notify:myemail@gmail.com
outputpath:/tmp
procs:30
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_1():
    """
    qalter test run: time_1
        Old Command Output:
          jobid must be an integer
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

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
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 10.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 15.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 20.0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:15.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:20.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

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
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 25.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 30.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 35.0
nodes changed from 2048 to 10
procs changed from 2048 to 10
walltime changed from 20 to 40.0
nodes changed from 2560 to 10
procs changed from 2560 to 10
walltime changed from 25 to 45.0
nodes changed from 3072 to 10
procs changed from 3072 to 10
walltime changed from 30 to 50.0
nodes changed from 3584 to 10
procs changed from 3584 to 10
walltime changed from 35 to 55.0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 7, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:6
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:7
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:25.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:35.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:2048
notify:myemail@gmail.com
outputpath:/tmp
procs:2048
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:20

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:40.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:2560
notify:myemail@gmail.com
outputpath:/tmp
procs:2560
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:25

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:45.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:6
location:/tmp
mode:smp
nodes:3072
notify:myemail@gmail.com
outputpath:/tmp
procs:3072
project:my_project
queue:dito
score:20
state:user_hold
submittime:60
tag:job
user:king
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:6
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:dito
score:20
state:user_hold
submittime:60
tag:job
user:king
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:50.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:7
location:/tmp
mode:smp
nodes:3584
notify:myemail@gmail.com
outputpath:/tmp
procs:3584
project:my_project
queue:myq
score:25
state:user_hold
submittime:60
tag:job
user:queen
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:35

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:7
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:myq
score:25
state:user_hold
submittime:60
tag:job
user:queen
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:55.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_4():
    """
    qalter test run: time_4
        Old Command Output:
          True
          nodes changed from 512 to 10
          procs changed from 512 to 10
          walltime changed from 5 to 30
          nodes changed from 1024 to 10
          procs changed from 1024 to 10
          walltime changed from 10 to 30
          nodes changed from 1536 to 10
          procs changed from 1536 to 10
          walltime changed from 15 to 30
          nodes changed from 2048 to 10
          procs changed from 2048 to 10
          walltime changed from 20 to 30
          nodes changed from 2560 to 10
          procs changed from 2560 to 10
          walltime changed from 25 to 30
          nodes changed from 3072 to 10
          procs changed from 3072 to 10
          walltime changed from 30 to 30
          nodes changed from 3584 to 10
          procs changed from 3584 to 10
          walltime changed from 35 to 30
          nodes changed from 4096 to 10
          procs changed from 4096 to 10
          walltime changed from 40 to 30
          nodes changed from 4608 to 10
          procs changed from 4608 to 10
          walltime changed from 45 to 30
          

    """

    args      = """-d -v -n10 -t30 1 2 3 4 5 6 7 10 15"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t30 1 2 3 4 5 6 7 10 15

get_config_option: Option filters not found in section [cqm]
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 30
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 30
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 30
nodes changed from 2048 to 10
procs changed from 2048 to 10
walltime changed from 20 to 30
nodes changed from 2560 to 10
procs changed from 2560 to 10
walltime changed from 25 to 30
nodes changed from 3072 to 10
procs changed from 3072 to 10
nodes changed from 3584 to 10
procs changed from 3584 to 10
walltime changed from 35 to 30
nodes changed from 4096 to 10
procs changed from 4096 to 10
walltime changed from 40 to 30
nodes changed from 4608 to 10
procs changed from 4608 to 10
walltime changed from 45 to 30
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 15, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:6
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:7
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:10
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:15
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:2048
notify:myemail@gmail.com
outputpath:/tmp
procs:2048
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:20

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:2560
notify:myemail@gmail.com
outputpath:/tmp
procs:2560
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:25

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:6
location:/tmp
mode:smp
nodes:3072
notify:myemail@gmail.com
outputpath:/tmp
procs:3072
project:my_project
queue:dito
score:20
state:user_hold
submittime:60
tag:job
user:king
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:6
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:dito
score:20
state:user_hold
submittime:60
tag:job
user:king
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:7
location:/tmp
mode:smp
nodes:3584
notify:myemail@gmail.com
outputpath:/tmp
procs:3584
project:my_project
queue:myq
score:25
state:user_hold
submittime:60
tag:job
user:queen
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:35

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:7
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:myq
score:25
state:user_hold
submittime:60
tag:job
user:queen
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:10
location:/tmp
mode:smp
nodes:4096
notify:myemail@gmail.com
outputpath:/tmp
procs:4096
project:my_project
queue:yours
score:35
state:user_hold
submittime:60
tag:job
user:girl
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:40

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:10
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:yours
score:35
state:user_hold
submittime:60
tag:job
user:girl
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:15
location:/tmp
mode:smp
nodes:4608
notify:myemail@gmail.com
outputpath:/tmp
procs:4608
project:my_project
queue:zq
score:2
state:user_hold
submittime:60
tag:job
user:boy
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:45

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:15
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:zq
score:2
state:user_hold
submittime:60
tag:job
user:boy
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:30
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_5():
    """
    qalter test run: time_5
        Old Command Output:
          True
          nodes changed from 512 to 10
          procs changed from 512 to 10
          walltime changed from 5 to 0
          nodes changed from 1024 to 10
          procs changed from 1024 to 10
          walltime changed from 10 to 0
          nodes changed from 1536 to 10
          procs changed from 1536 to 10
          walltime changed from 15 to 0
          

    """

    args      = """-d -v -n10 -t00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

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
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:15.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_7():
    """
    qalter test run: time_7
        Old Command Output:
          True
          nodes changed from 512 to 10
          procs changed from 512 to 10
          walltime changed from 5 to 0
          nodes changed from 1024 to 10
          procs changed from 1024 to 10
          walltime changed from 10 to 0
          nodes changed from 1536 to 10
          procs changed from 1536 to 10
          walltime changed from 15 to 0
          

    """

    args      = """-d -v -n10 -t 00:00:30 1 2 3"""

    cmdout    = \
"""
qalter.py -d -v -n10 -t 00:00:30 1 2 3

get_config_option: Option filters not found in section [cqm]
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

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
nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
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
jobid:1
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:jello
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:5.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:bello
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:10.0

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:3
location:/tmp
mode:smp
nodes:10
notify:myemail@gmail.com
outputpath:/tmp
procs:10
project:my_project
queue:aaa
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:15.0
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_option():
    """
    qalter test run: invalid_option
        Old Command Output:
          option -m not recognized
          
          Usage: qalter [-d] [-v] -A <project name> -t <time in minutes>
                        -e <error file path> -o <output file path>
                        --dependencies <jobid1>:<jobid2> --geometry AxBxCxDxE
                        -n <number of nodes> -h --proccount <processor count>
                        -M <email address> --mode <mode co/vn>
                        --run_users <user1>:<user2> --run_project <jobid1> <jobid2>
                        --attrs <attr1=val1>:<attr2=val2>
          
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_email_option():
    """
    qalter test run: email_option
        Old Command Output:
          True
          notify changed from myemail@gmail.com to j@gmail.com
          notify changed from myemail@gmail.com to j@gmail.com
          

    """

    args      = """-d -v -M j@gmail.com 1 2"""

    cmdout    = \
"""
qalter.py -d -v -M j@gmail.com 1 2

get_config_option: Option filters not found in section [cqm]
notify changed from myemail@gmail.com to j@gmail.com
notify changed from myemail@gmail.com to j@gmail.com
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
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
jobid:1
location:/tmp
mode:smp
nodes:512
notify:j@gmail.com
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

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
jobid:2
location:/tmp
mode:smp
nodes:1024
notify:j@gmail.com
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_1():
    """
    qalter test run: mode_1
        Old Command Output:
          Specifed mode 'jjj' not valid, valid modes are
          co
          vn
          script
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_2():
    """
    qalter test run: mode_2
        Old Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_1():
    """
    qalter test run: proccount_1
        Old Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_2():
    """
    qalter test run: proccount_2
        Old Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_nodecount():
    """
    qalter test run: invalid_nodecount
        Old Command Output:
          non-integer node count specified
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_1():
    """
    qalter test run: user_1
        Old Command Output:
          True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
          

    """

    args      = """-d -v --run_users user1:user2:user3 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --run_users user1:user2:user3 1 2 3 4 5

get_config_option: Option filters not found in section [cqm]
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 5, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:5
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
user_list:['gooduser', 'user1', 'user2', 'user3']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
user_list:['gooduser', 'user1', 'user2', 'user3']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
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
user_list:['gooduser', 'user1', 'user2', 'user3']
walltime:15

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:2048
notify:myemail@gmail.com
outputpath:/tmp
procs:2048
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:20

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:4
location:/tmp
mode:smp
nodes:2048
notify:myemail@gmail.com
outputpath:/tmp
procs:2048
project:my_project
queue:bbb
score:60
state:user_hold
submittime:60
tag:job
user:cat
user_hold:False
user_list:['gooduser', 'user1', 'user2', 'user3']
walltime:20

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:2560
notify:myemail@gmail.com
outputpath:/tmp
procs:2560
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
walltime:25

New Job Info:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:5
location:/tmp
mode:smp
nodes:2560
notify:myemail@gmail.com
outputpath:/tmp
procs:2560
project:my_project
queue:hhh
score:30
state:user_hold
submittime:60
tag:job
user:henry
user_hold:False
user_list:['gooduser', 'user1', 'user2', 'user3']
walltime:25
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_2():
    """
    qalter test run: user_2
        Old Command Output:
          user naughtyuser does not exist.
          

    """

    args      = """-d -v --run_users user1:naughtyuser 1 2 3 4 5"""

    cmdout    = \
"""
qalter.py -d -v --run_users user1:naughtyuser 1 2 3 4 5

user naughtyuser does not exist.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_project():
    """
    qalter test run: project
        Old Command Output:
          True
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          

    """

    args      = """-d -v --run_project 10 20 30"""

    cmdout    = \
"""
qalter.py -d -v --run_project 10 20 30

get_config_option: Option filters not found in section [cqm]
run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 30, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:20
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:30
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
jobid:10
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
jobid:10
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:jello
run_project:True
score:50
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['gooduser']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:20
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
jobid:20
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:bello
run_project:True
score:55
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['gooduser']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:30
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
jobid:30
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:aaa
run_project:True
score:40
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['gooduser']
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_1():
    """
    qalter test run: geometry_1
        Old Command Output:
          
          Usage: qalter [-d] [-v] -A <project name> -t <time in minutes>
                        -e <error file path> -o <output file path>
                        --dependencies <jobid1>:<jobid2> --geometry AxBxCxDxE
                        -n <number of nodes> -h --proccount <processor count>
                        -M <email address> --mode <mode co/vn>
                        --run_users <user1>:<user2> --run_project <jobid1> <jobid2>
                        --attrs <attr1=val1>:<attr2=val2>
          
          

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

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_2():
    """
    qalter test run: geometry_2
        Old Command Output:
          Geometry specification 10x10x10x10x10 is invalid.
          Jobs not altered.
          

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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:5
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_3():
    """
    qalter test run: geometry_3
        Old Command Output:
          Geometry requires more nodes than specified for job.
          Jobs not altered.
          

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
user:gooduser
walltime:*
is_active:*
jobid:2
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:3
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:4
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_preboot_1():
    """
    qalter test run: preboot_1
        Old Command Output:
          True
          run_project set to True
          script_preboot set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          script_preboot set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          script_preboot set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          

    """

    args      = """-d -v --enable_preboot --run_project 10 20 30"""

    cmdout    = \
"""
qalter.py -d -v --enable_preboot --run_project 10 20 30

get_config_option: Option filters not found in section [cqm]
run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 30, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:20
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:30
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
jobid:10
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
jobid:10
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:jello
run_project:True
score:50
script_preboot:True
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['gooduser']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:20
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
jobid:20
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:bello
run_project:True
score:55
script_preboot:True
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['gooduser']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:30
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
jobid:30
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:aaa
run_project:True
score:40
script_preboot:True
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['gooduser']
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_preboot_2():
    """
    qalter test run: preboot_2
        Old Command Output:
          True
          run_project set to True
          script_preboot set to False
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          script_preboot set to False
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          script_preboot set to False
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          

    """

    args      = """-d -v --disable_preboot --run_project 10 20 30"""

    cmdout    = \
"""
qalter.py -d -v --disable_preboot --run_project 10 20 30

get_config_option: Option filters not found in section [cqm]
run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 30, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
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
user:gooduser
walltime:*
is_active:*
jobid:20
nodes:*
notify:*
procs:*
project:*
queue:*
tag:job
user:gooduser
walltime:*
is_active:*
jobid:30
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
jobid:10
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
jobid:10
location:/tmp
mode:smp
nodes:512
notify:myemail@gmail.com
outputpath:/tmp
procs:512
project:my_project
queue:jello
run_project:True
score:50
script_preboot:False
state:user_hold
submittime:60
tag:job
user:land
user_hold:False
user_list:['gooduser']
walltime:5

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:20
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
jobid:20
location:/tmp
mode:smp
nodes:1024
notify:myemail@gmail.com
outputpath:/tmp
procs:1024
project:my_project
queue:bello
run_project:True
score:55
script_preboot:False
state:user_hold
submittime:60
tag:job
user:house
user_hold:False
user_list:['gooduser']
walltime:10

SET_JOBS


Original Jobs:

args:
envs:{}
errorpath:/tmp
geometry:None
has_completed:False
jobid:30
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
jobid:30
location:/tmp
mode:smp
nodes:1536
notify:myemail@gmail.com
outputpath:/tmp
procs:1536
project:my_project
queue:aaa
run_project:True
score:40
script_preboot:False
state:user_hold
submittime:60
tag:job
user:dog
user_hold:False
user_list:['gooduser']
walltime:15
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

