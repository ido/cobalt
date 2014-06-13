import testutils

# ---------------------------------------------------------------------------------
def test_qmove_invalid_option():
    """
    qmove test run: invalid_option

    """

    args      = """-k"""

    cmdout    = ''

    cmderr    = \
"""Usage: qmove.py [options] <queue name> <jobid1> [... <jobidN>]

qmove.py: error: no such option: -k
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

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queue_1():
    """
    qmove test run: queue_1

    """

    args      = """myq 1 2 3"""

    cmdout    = \
"""moved job 1 to queue 'kebra'
moved job 2 to queue 'kebra'
moved job 3 to queue 'kebra'
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
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
jobid:2
jobid type: <type 'int'>
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
jobid:3
jobid type: <type 'int'>
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queue_2():
    """
    qmove test run: queue_2

    """

    args      = """-d myq 1 2 3"""

    cmdout    = \
"""moved job 1 to queue 'kebra'
moved job 2 to queue 'kebra'
moved job 3 to queue 'kebra'
"""

    cmderr    = \
"""
qmove.py -d myq 1 2 3

component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 1}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 2}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 3}],
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': '512', 'walltime': '5', 'queue': 'jello', 'envs': {}, 'user_hold': False, 'jobid': 1, 'project': 'my_project', 'submittime': '60', 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': '512', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'land'}],
     {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': '60', 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': '512', 'args': '', 'is_active': False, 'user': 'land', 'procs': '512', 'walltime': '5', 'geometry': None, 'user_hold': False, 'jobid': 1, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
     gooduser,
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': '1024', 'walltime': '10', 'queue': 'bello', 'envs': {}, 'user_hold': False, 'jobid': 2, 'project': 'my_project', 'submittime': '60', 'state': 'user_hold', 'score': 55, 'location': '/tmp', 'nodes': '1024', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'house'}],
     {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': '60', 'state': 'user_hold', 'score': 55, 'location': '/tmp', 'nodes': '1024', 'args': '', 'is_active': False, 'user': 'house', 'procs': '1024', 'walltime': '10', 'geometry': None, 'user_hold': False, 'jobid': 2, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
     gooduser,
     )


component: "queue-manager.set_jobs", defer: False
  set_jobs(
     [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': '1536', 'walltime': '15', 'queue': 'aaa', 'envs': {}, 'user_hold': False, 'jobid': 3, 'project': 'my_project', 'submittime': '60', 'state': 'user_hold', 'score': 40, 'location': '/tmp', 'nodes': '1536', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'dog'}],
     {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': '60', 'state': 'user_hold', 'score': 40, 'location': '/tmp', 'nodes': '1536', 'args': '', 'is_active': False, 'user': 'dog', 'procs': '1536', 'walltime': '15', 'geometry': None, 'user_hold': False, 'jobid': 3, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
     gooduser,
     )


"""

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
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
jobid:2
jobid type: <type 'int'>
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
jobid:3
jobid type: <type 'int'>
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
is_active:False
is_active type: <type 'bool'>
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
is_active:False
is_active type: <type 'bool'>
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
queue:myq
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queue_3():
    """
    qmove test run: queue_3

    """

    args      = """1 2 3 4"""

    cmdout    = \
"""moved job 2 to queue 'kebra'
moved job 3 to queue 'kebra'
moved job 4 to queue 'kebra'
"""

    cmderr    = ''

    stubout   = \
"""
GET_JOBS

jobid:2
jobid type: <type 'int'>
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
jobid:3
jobid type: <type 'int'>
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
jobid:4
jobid type: <type 'int'>
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
is_active:False
is_active type: <type 'bool'>
jobid:2
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
is_active:False
is_active type: <type 'bool'>
jobid:2
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
queue:1
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
is_active:False
is_active type: <type 'bool'>
jobid:3
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
is_active:False
is_active type: <type 'bool'>
jobid:3
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
queue:1
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
is_active:False
is_active type: <type 'bool'>
jobid:4
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
is_active:False
is_active type: <type 'bool'>
jobid:4
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
queue:1
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
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qmove_queu_4():
    """
    qmove test run: queu_4

    """

    args      = """q1 q2 1 2 3"""

    cmdout    = ''

    cmderr    = \
"""jobid must be an integer: q2
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

    results = testutils.run_cmd('qmove.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

