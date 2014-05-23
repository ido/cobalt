import testutils

# ---------------------------------------------------------------------------------
def test_qalter_simple_1():
    """
    qalter test run: simple_1

    """

    args      = """-d -n30"""

    cmdout    = \
"""Usage: qalter.py --help
Usage: qalter.py [options] <jobid1> ... <jobidN>

"""

    cmderr    = \
"""
qalter.py -d -n30

No Jobid(s) given

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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_simple_2():
    """
    qalter test run: simple_2

    """

    args      = """-d -n30 1"""

    cmdout    = \
"""nodes changed from 512 to 30
procs changed from 512 to 30
"""

    cmderr    = \
"""
qalter.py -d -n30 1

component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 1, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'gooduser'}],
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'errorpath': '/tmp', 'args': '', 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': '512', 'walltime': '5', 'queue': 'jello', 'envs': {}, 'user_hold': False, 'jobid': 1, 'project': 'my_project', 'submittime': '60', 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': '512', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'land'}],
     {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': '60', 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': 30, 'args': '', 'user': 'land', 'procs': 30, 'walltime': '5', 'geometry': None, 'user_hold': False, 'jobid': 1, 'queue': 'jello', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
     gooduser,
     )


[{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
"""

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:30
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:30
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_simple_3():
    """
    qalter test run: simple_3

    """

    args      = """-n30 1"""

    cmdout    = \
"""nodes changed from 512 to 30
procs changed from 512 to 30
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:30
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:30
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_1():
    """
    qalter test run: time_1

    """

    args      = """-v n10 -t5 1 2 3"""

    cmdout    = \
"""Usage: qalter.py --help
Usage: qalter.py [options] <jobid1> ... <jobidN>

"""

    cmderr    = \
"""No required options provided

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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_2():
    """
    qalter test run: time_2

    """

    args      = """-v -n10 -t+5 1 2 3"""

    cmdout    = \
"""nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 10.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 15.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 20.0
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:20.0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_3():
    """
    qalter test run: time_3

    """

    args      = """-v -n10 -t+20 1 2 3 4 5 6 7"""

    cmdout    = \
"""nodes changed from 512 to 10
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
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:6
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:7
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:25.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:35.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2048
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2048
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:20
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:40.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2560
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2560
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:25
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:45.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:3072
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:3072
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:dito
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:20
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:king
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:dito
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:20
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:king
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:50.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:7
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:3584
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:3584
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:25
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:queen
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:35
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:7
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:25
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:queen
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:55.0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_4():
    """
    qalter test run: time_4

    """

    args      = """-v -n10 -t30 1 2 3 4 5 6 7 10 15"""

    cmdout    = \
"""nodes changed from 512 to 10
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
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:6
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:7
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:10
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:15
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2048
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2048
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:20
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2560
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2560
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:25
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:3072
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:3072
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:dito
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:20
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:king
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:6
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:dito
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:20
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:king
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:7
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:3584
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:3584
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:25
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:queen
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:35
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:7
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:25
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:queen
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:4096
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:4096
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:yours
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:35
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:girl
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:40
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:yours
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:35
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:girl
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:15
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:4608
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:4608
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:zq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:2
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:boy
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:45
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:15
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:zq
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:2
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:boy
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:30
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_5():
    """
    qalter test run: time_5

    """

    args      = """-v -n10 -t00:00:30 1 2 3"""

    cmdout    = \
"""nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_6():
    """
    qalter test run: time_6

    """

    args      = """-v -n10 -t+00:00:30 1 2 3"""

    cmdout    = \
"""nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15.0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_7():
    """
    qalter test run: time_7

    """

    args      = """-v -n10 -t 00:00:30 1 2 3"""

    cmdout    = \
"""nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 0
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_time_8():
    """
    qalter test run: time_8

    """

    args      = """-v -n10 -t +00:00:30 1 2 3"""

    cmdout    = \
"""nodes changed from 512 to 10
procs changed from 512 to 10
walltime changed from 5 to 5.0
nodes changed from 1024 to 10
procs changed from 1024 to 10
walltime changed from 10 to 10.0
nodes changed from 1536 to 10
procs changed from 1536 to 10
walltime changed from 15 to 15.0
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10.0
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:10
procs type: <type 'int'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15.0
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_option():
    """
    qalter test run: invalid_option

    """

    args      = """-v -m j@gmail.com"""

    cmdout    = ''

    cmderr    = \
"""Usage: qalter.py --help
Usage: qalter.py [options] <jobid1> ... <jobidN>

qalter.py: error: no such option: -m
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_email_option():
    """
    qalter test run: email_option

    """

    args      = """-v -M j@gmail.com 1 2"""

    cmdout    = \
"""notify changed from myemail@gmail.com to j@gmail.com
notify changed from myemail@gmail.com to j@gmail.com
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:j@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:j@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_1():
    """
    qalter test run: mode_1

    """

    args      = """-v --mode jjj  -n40 -t50 -e p -o o 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'jjj' not valid, valid modes are
co
vn
script
interactive
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_mode_2():
    """
    qalter test run: mode_2

    """

    args      = """-v --mode dual -n40 -t50 -e p -o o 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'dual' not valid, valid modes are
co
vn
script
interactive
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_1():
    """
    qalter test run: proccount_1

    """

    args      = """-v --mode dual -n512 --proccount one -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'dual' not valid, valid modes are
co
vn
script
interactive
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_proccount_2():
    """
    qalter test run: proccount_2

    """

    args      = """-v --mode dual -n512 --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'dual' not valid, valid modes are
co
vn
script
interactive
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_invalid_nodecount():
    """
    qalter test run: invalid_nodecount

    """

    args      = """-v --mode dual -nfiver --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'dual' not valid, valid modes are
co
vn
script
interactive
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_1():
    """
    qalter test run: user_1

    """

    args      = """-v --run_users user1:user2:user3 1 2 3 4 5"""

    cmdout    = \
"""user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser', 'user1', 'user2', 'user3']
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:1
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:2
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:3
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2048
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2048
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:20
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:4
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2048
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2048
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bbb
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:60
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:cat
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:20
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2560
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2560
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:25
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:5
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:2560
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:2560
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:hhh
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:30
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:henry
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:25
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_2():
    """
    qalter test run: user_2

    """

    args      = """-v --run_users user1:naughtyuser 1 2 3 4 5"""

    cmdout    = ''

    cmderr    = \
"""user naughtyuser does not exist.
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_user_3():
    """
    qalter test run: user_3

    """

    args      = """-v --run_users user1:root 1 2 3 4 5"""

    cmdout    = ''

    cmderr    = \
"""Modifying a job while running is currently not supported
"""

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("JOB_RUNNING")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_project():
    """
    qalter test run: project

    """

    args      = """-v --run_project 10 20 30"""

    cmdout    = \
"""run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:10
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:20
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:30
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:15
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_1():
    """
    qalter test run: geometry_1

    """

    args      = """-v --geometry 10 1 2 3 4 5"""

    cmdout    = ''

    cmderr    = \
"""Invalid geometry entered: 
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_2():
    """
    qalter test run: geometry_2

    """

    args      = """-v --geometry 10x10x10x10x10 1 2 3 4 5"""

    cmdout    = ''

    cmderr    = \
"""Invalid geometry entered: 
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_3():
    """
    qalter test run: geometry_3

    """

    args      = """-v --geometry 04x04x04x04    1 2 3 4"""

    cmdout    = ''

    cmderr    = \
"""get_config_option: Option type not found in section [system]
Invalid Geometry
"""

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_4():
    """
    qalter test run: geometry_4

    """

    args      = """-v --geometry 10x10x10x10x1  1 2 3 4 5"""

    cmdout    = ''

    cmderr    = \
"""get_config_option: Option type not found in section [system]
Invalid Geometry
"""

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_geometry_5():
    """
    qalter test run: geometry_5

    """

    args      = """-v --geometry 04x04x04x04x2  1 2 3 4"""

    cmdout    = ''

    cmderr    = \
"""get_config_option: Option type not found in section [system]
Invalid Geometry
"""

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_preboot_1():
    """
    qalter test run: preboot_1

    """

    args      = """-v --enable_preboot --run_project 10 20 30"""

    cmdout    = \
"""run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to True
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:10
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:20
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:30
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:50
score type: <type 'int'>
script_preboot:True
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:55
score type: <type 'int'>
script_preboot:True
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:40
score type: <type 'int'>
script_preboot:True
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:15
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_preboot_2():
    """
    qalter test run: preboot_2

    """

    args      = """-v --disable_preboot --run_project 10 20 30"""

    cmdout    = \
"""run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
run_project set to True
script_preboot set to False
user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:10
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:20
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:30
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:50
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:10
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:512
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:512
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:jello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:50
score type: <type 'int'>
script_preboot:False
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:land
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:5
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:55
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:20
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1024
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1024
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:bello
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:55
score type: <type 'int'>
script_preboot:False
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:house
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

SET_JOBS


Original Jobs:

user: gooduser
args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
score:40
score type: <type 'int'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']
user_list type: <type 'list'>
walltime:15
walltime type: <type 'str'>

New Job Info:

args:
args type: <type 'str'>
envs:{}
envs type: <type 'dict'>
errorpath:/tmp
errorpath type: <type 'str'>
geometry:None
geometry type: <type 'NoneType'>
has_completed:False
has_completed type: <type 'bool'>
jobid:30
jobid type: <type 'int'>
location:/tmp
location type: <type 'str'>
mode:smp
mode type: <type 'str'>
nodes:1536
nodes type: <type 'str'>
notify:myemail@gmail.com
notify type: <type 'str'>
outputpath:/tmp
outputpath type: <type 'str'>
procs:1536
procs type: <type 'str'>
project:my_project
project type: <type 'str'>
queue:aaa
queue type: <type 'str'>
resid:None
resid type: <type 'NoneType'>
run_project:True
run_project type: <type 'bool'>
score:40
score type: <type 'int'>
script_preboot:False
script_preboot type: <type 'bool'>
state:user_hold
state type: <type 'str'>
submittime:60
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
user:dog
user type: <type 'str'>
user_hold:False
user_hold type: <type 'bool'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:15
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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_defer_1():
    """
    qalter test run: defer_1

    """

    args      = """--defer"""

    cmdout    = \
"""Usage: qalter.py --help
Usage: qalter.py [options] <jobid1> ... <jobidN>

"""

    cmderr    = \
"""No Jobid(s) given

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

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qalter_defer_2():
    """
    qalter test run: defer_2

    """

    args      = """--defer 1 2 3 4 5"""

    cmdout    = \
"""updating scores for jobs: 1, 2, 3, 4, 5
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

is_active:*
is_active type: <type 'str'>
jobid:1
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:2
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:3
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:4
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>
is_active:*
is_active type: <type 'str'>
jobid:5
jobid type: <type 'int'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
walltime:*
walltime type: <type 'str'>

ADJUST_JOB_SCORES

jobid:1
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
jobid:4
jobid type: <type 'int'>
jobid:5
jobid type: <type 'int'>
new score: 0, type = <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qalter.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

