import testutils

# ---------------------------------------------------------------------------------
def test_qstat_version_option():
    """
    qstat test run: version_option

    """

    args      = """--version"""

    cmdout    = \
"""version: "qstat.py " + $Revision: 406 $ + , Cobalt  + $Version$
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_help_option():
    """
    qstat test run: help_option

    """

    args      = """-h"""

    cmdout    = \
"""Usage: qstat.py [options] <jobids1> ... <jobidsN>

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d, --debug           turn non communication debugging
  -f, --full            show more verbose information
  -l, --long            show job info in vertical format
  -Q                    show queues and properties
  --reverse             show output in reverse
  --header=HEADER       specify custom header
  --sort=SORT           sort output by specified attribute
  -u USER, --user=USER  Specify username
"""

    cmderr    = ''

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_debug_only():
    """
    qstat test run: debug_only

    """

    args      = """-d"""

    cmdout    = \
"""JobID  User  WallTime  Nodes  State  Location  
===============================================
100    land  00:05:00  512    *      /tmp      
"""

    cmderr    = \
"""
qstat.py -d

component: "queue-manager.get_queues", defer: True
  get_queues(
     [{'state': '*', 'name': '*'}],
     )


component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': '*', 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}],
     )


"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:*
jobid type: <type 'str'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_1():
    """
    qstat test run: full_option_1

    """

    args      = """-d -f 1 2 3 4 5"""

    cmdout    = \
"""JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
5      -        henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
3      -        dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      -        land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      -        house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
4      -        cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
"""

    cmderr    = \
"""
qstat.py -d -f 1 2 3 4 5

component: "queue-manager.get_queues", defer: True
  get_queues(
     [{'state': '*', 'name': '*'}],
     )


component: "queue-manager.get_jobs", defer: False
  get_jobs(
     [{'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': 1, 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}, {'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': 2, 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}, {'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': 3, 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}, {'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': 4, 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}, {'timeremaining': '*', 'kernel': '*', 'ion_kerneloptions': '*', 'errorpath': '*', 'kerneloptions': '*', 'args': '*', 'geometry': '*', 'maxtasktime': '*', 'jobname': '*', 'outputpath': '*', 'tag': 'job', 'notify': '*', 'user': '*', 'dependencies': '*', 'path': '*', 'ion_kernel': '*', 'outputdir': '*', 'procs': '*', 'walltime': '*', 'short_state': '*', 'index': '*', 'preemptable': '*', 'score': '*', 'envs': '*', 'project': '*', 'user_hold': '*', 'user_list': '*', 'admin_hold': '*', 'jobid': 5, 'queue': '*', 'submittime': '*', 'state': '*', 'queuedtime': '*', 'command': '*', 'location': '*', 'starttime': '*', 'nodes': '*', 'runtime': '*', 'attrs': '*', 'dep_frac': '*', 'mode': '*'}],
     )


"""

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_2():
    """
    qstat test run: full_option_2

    """

    args      = """-f 1 2 3 4 5"""

    cmdout    = \
"""JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
5      -        henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
3      -        dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      -        land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      -        house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
4      -        cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_3():
    """
    qstat test run: full_option_3

    """

    args      = """-f --reverse 1 2 3 4 5"""

    cmdout    = \
"""JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
4      -        cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
2      -        house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
1      -        land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
3      -        dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
5      -        henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_4():
    """
    qstat test run: full_option_4

    """

    args      = """-f -l 1 2 3 4 5"""

    cmdout    = \
"""JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_5():
    """
    qstat test run: full_option_5

    """

    args      = """-f -l --reverse 1 2 3 4 5"""

    cmdout    = \
"""JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_6():
    """
    qstat test run: full_option_6

    """

    args      = """-f -l --sort user 1 2 3 4 5"""

    cmdout    = \
"""JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_7():
    """
    qstat test run: full_option_7

    """

    args      = """-f -l --reverse --sort user 1 2 3 4 5"""

    cmdout    = \
"""JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_8():
    """
    qstat test run: full_option_8

    """

    args      = """-f -l --sort queue 1 2 3 4 5"""

    cmdout    = \
"""JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_9():
    """
    qstat test run: full_option_9

    """

    args      = """-f -l --reverse --sort queue 1 2 3 4 5"""

    cmdout    = \
"""JobID: 1
    JobName           : -
    User              : land
    WallTime          : 00:05:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 512
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 512
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : jello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  50.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 5
    JobName           : -
    User              : henry
    WallTime          : 00:25:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2560
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2560
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : hhh
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  30.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 2
    JobName           : -
    User              : house
    WallTime          : 00:10:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1024
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1024
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bello
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  55.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 4
    JobName           : -
    User              : cat
    WallTime          : 00:20:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 2048
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 2048
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : bbb
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  60.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

JobID: 3
    JobName           : -
    User              : dog
    WallTime          : 00:15:00
    QueuedTime        : 378981:57:19
    RunTime           : N/A
    TimeRemaining     : N/A
    Nodes             : 1536
    State             : *
    Location          : /tmp
    Mode              : smp
    Procs             : 1536
    Preemptable       : -
    User_Hold         : False
    Admin_Hold        : -
    Queue             : aaa
    StartTime         : N/A
    Index             : -
    SubmitTime        : Thu Jan 01 00:01:00 1970 +0000 (UTC)
    Path              : -
    OutputDir         : -
    ErrorPath         : /tmp
    OutputPath        : /tmp
    Envs              : 
    Command           : -
    Args              : 
    Kernel            : -
    KernelOptions     : -
    ION_Kernel        : -
    ION_KernelOptions : -
    Project           : my_project
    Dependencies      : -
    S                 : -
    Notify            : myemail@gmail.com
    Score             :  40.0  
    Maxtasktime       : -
    attrs             : -
    dep_frac          : -
    user_list         : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry          : Any

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_10():
    """
    qstat test run: full_option_10

    """

    args      = """-f"""

    cmdout    = \
"""JobID  JobName  User  Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
=======================================================================================================================
100    -        land   50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:*
jobid type: <type 'str'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_11():
    """
    qstat test run: full_option_11

    """

    args      = """-f --header Jobid:State:RunTime  1 2 3"""

    cmdout    = \
"""JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
3      -        dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      -        land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      -        house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_1():
    """
    qstat test run: long_option_1

    """

    args      = """-l"""

    cmdout    = \
"""JobID: 100
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:*
jobid type: <type 'str'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_2():
    """
    qstat test run: long_option_2

    """

    args      = """-l 1 2 3 4 5"""

    cmdout    = \
"""JobID: 1
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

JobID: 2
    User     : house
    WallTime : 00:10:00
    Nodes    : 1024
    State    : *
    Location : /tmp

JobID: 3
    User     : dog
    WallTime : 00:15:00
    Nodes    : 1536
    State    : *
    Location : /tmp

JobID: 4
    User     : cat
    WallTime : 00:20:00
    Nodes    : 2048
    State    : *
    Location : /tmp

JobID: 5
    User     : henry
    WallTime : 00:25:00
    Nodes    : 2560
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_3():
    """
    qstat test run: long_option_3

    """

    args      = """-l --reverse 1 2 3 4 5"""

    cmdout    = \
"""JobID: 5
    User     : henry
    WallTime : 00:25:00
    Nodes    : 2560
    State    : *
    Location : /tmp

JobID: 4
    User     : cat
    WallTime : 00:20:00
    Nodes    : 2048
    State    : *
    Location : /tmp

JobID: 3
    User     : dog
    WallTime : 00:15:00
    Nodes    : 1536
    State    : *
    Location : /tmp

JobID: 2
    User     : house
    WallTime : 00:10:00
    Nodes    : 1024
    State    : *
    Location : /tmp

JobID: 1
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_4():
    """
    qstat test run: long_option_4

    """

    args      = """-l --sort user 1 2 3 4 5"""

    cmdout    = \
"""JobID: 4
    User     : cat
    WallTime : 00:20:00
    Nodes    : 2048
    State    : *
    Location : /tmp

JobID: 3
    User     : dog
    WallTime : 00:15:00
    Nodes    : 1536
    State    : *
    Location : /tmp

JobID: 5
    User     : henry
    WallTime : 00:25:00
    Nodes    : 2560
    State    : *
    Location : /tmp

JobID: 2
    User     : house
    WallTime : 00:10:00
    Nodes    : 1024
    State    : *
    Location : /tmp

JobID: 1
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_5():
    """
    qstat test run: long_option_5

    """

    args      = """-l --reverse --sort user 1 2 3 4 5"""

    cmdout    = \
"""JobID: 1
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

JobID: 2
    User     : house
    WallTime : 00:10:00
    Nodes    : 1024
    State    : *
    Location : /tmp

JobID: 5
    User     : henry
    WallTime : 00:25:00
    Nodes    : 2560
    State    : *
    Location : /tmp

JobID: 3
    User     : dog
    WallTime : 00:15:00
    Nodes    : 1536
    State    : *
    Location : /tmp

JobID: 4
    User     : cat
    WallTime : 00:20:00
    Nodes    : 2048
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_6():
    """
    qstat test run: long_option_6

    """

    args      = """-l --sort queue 1 2 3 4 5"""

    cmdout    = \
"""JobID: 1
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

JobID: 2
    User     : house
    WallTime : 00:10:00
    Nodes    : 1024
    State    : *
    Location : /tmp

JobID: 3
    User     : dog
    WallTime : 00:15:00
    Nodes    : 1536
    State    : *
    Location : /tmp

JobID: 4
    User     : cat
    WallTime : 00:20:00
    Nodes    : 2048
    State    : *
    Location : /tmp

JobID: 5
    User     : henry
    WallTime : 00:25:00
    Nodes    : 2560
    State    : *
    Location : /tmp

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:4
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:5
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_11():
    """
    qstat test run: long_option_11

    """

    args      = """-l --header Jobid:State:RunTime  1 2 3"""

    cmdout    = \
"""Jobid: 1
    State   : *
    RunTime : N/A

Jobid: 2
    State   : *
    RunTime : N/A

Jobid: 3
    State   : *
    RunTime : N/A

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:1
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:2
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
walltime:*
walltime type: <type 'str'>
admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:3
jobid type: <type 'int'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_1():
    """
    qstat test run: queue_option_1

    """

    args      = """-f -Q -l 1 2 3"""

    cmdout    = \
"""Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:1
name type: <type 'str'>
state:*
state type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:2
name type: <type 'str'>
state:*
state type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:3
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_2():
    """
    qstat test run: queue_option_2

    """

    args      = """-f --reverse -Q -l 1 2 3"""

    cmdout    = \
"""Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:1
name type: <type 'str'>
state:*
state type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:2
name type: <type 'str'>
state:*
state type: <type 'str'>
totalnodes:*
totalnodes type: <type 'str'>
users:*
users type: <type 'str'>
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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:3
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_3():
    """
    qstat test run: queue_option_3

    """

    args      = """-f --sort users -Q"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
zq     boy    None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
aaa    dog    None    None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
myq    queen  None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_4():
    """
    qstat test run: queue_option_4

    """

    args      = """-Q"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
aaa    dog    None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
myq    queen  None    None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
zq     boy    None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_5():
    """
    qstat test run: queue_option_5

    """

    args      = """-Q --reverse"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
zq     boy    None    None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
myq    queen  None    None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
aaa    dog    None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_6():
    """
    qstat test run: queue_option_6

    """

    args      = """-Q --sort users"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
zq     boy    None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
aaa    dog    None    None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
myq    queen  None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_7():
    """
    qstat test run: queue_option_7

    """

    args      = """-Q --sort users --reverse"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
myq    queen  None    None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
aaa    dog    None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
zq     boy    None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_8():
    """
    qstat test run: queue_option_8

    """

    args      = """-Q -l"""

    cmdout    = \
"""Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_9():
    """
    qstat test run: queue_option_9

    """

    args      = """-Q --reverse -l"""

    cmdout    = \
"""Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_10():
    """
    qstat test run: queue_option_10

    """

    args      = """-Q --sort users -l"""

    cmdout    = \
"""Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_11():
    """
    qstat test run: queue_option_11

    """

    args      = """-Q --sort users --reverse -l"""

    cmdout    = \
"""Name: myq
    Users        : queen
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: jello
    Users        : land
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: dito
    Users        : king
    Groups       : wheel
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: kebra
    Users        : james
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bello
    Users        : house
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: hhh
    Users        : henry
    Groups       : bar
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: yours
    Users        : girl
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: aaa
    Users        : dog
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: bbb
    Users        : cat
    Groups       : foo
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

Name: zq
    Users        : boy
    Groups       : None
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_12():
    """
    qstat test run: queue_option_12

    """

    args      = """-Q --header Jobid:State:RunTime"""

    cmdout    = \
"""Name   Users  Groups  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
================================================================================================================
aaa    dog    None    None     None     20          20         20            20            100         running  
bbb    cat    foo     None     None     20          20         20            20            100         running  
bello  house  None    None     None     20          20         20            20            100         running  
dito   king   wheel   None     None     20          20         20            20            100         running  
hhh    henry  bar     None     None     20          20         20            20            100         running  
jello  land   None    None     None     20          20         20            20            100         running  
kebra  james  None    None     None     20          20         20            20            100         running  
myq    queen  None    None     None     20          20         20            20            100         running  
yours  girl   None    None     None     20          20         20            20            100         running  
zq     boy    None    None     None     20          20         20            20            100         running  
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_QUEUES

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
maxusernodes:*
maxusernodes type: <type 'str'>
mintime:*
mintime type: <type 'str'>
name:*
name type: <type 'str'>
state:*
state type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_no_arguments_or_options():
    """
    qstat test run: no_arguments_or_options

    """

    args      = ''

    cmdout    = \
"""JobID  User  WallTime  Nodes  State  Location  
===============================================
100    land  00:05:00  512    *      /tmp      
"""

    cmderr    = ''

    stubout   = \
"""
GET_QUEUES

name:*
name type: <type 'str'>
state:*
state type: <type 'str'>

GET_JOBS

admin_hold:*
admin_hold type: <type 'str'>
args:*
args type: <type 'str'>
attrs:*
attrs type: <type 'str'>
command:*
command type: <type 'str'>
dep_frac:*
dep_frac type: <type 'str'>
dependencies:*
dependencies type: <type 'str'>
envs:*
envs type: <type 'str'>
errorpath:*
errorpath type: <type 'str'>
geometry:*
geometry type: <type 'str'>
index:*
index type: <type 'str'>
ion_kernel:*
ion_kernel type: <type 'str'>
ion_kerneloptions:*
ion_kerneloptions type: <type 'str'>
jobid:*
jobid type: <type 'str'>
jobname:*
jobname type: <type 'str'>
kernel:*
kernel type: <type 'str'>
kerneloptions:*
kerneloptions type: <type 'str'>
location:*
location type: <type 'str'>
maxtasktime:*
maxtasktime type: <type 'str'>
mode:*
mode type: <type 'str'>
nodes:*
nodes type: <type 'str'>
notify:*
notify type: <type 'str'>
outputdir:*
outputdir type: <type 'str'>
outputpath:*
outputpath type: <type 'str'>
path:*
path type: <type 'str'>
preemptable:*
preemptable type: <type 'str'>
procs:*
procs type: <type 'str'>
project:*
project type: <type 'str'>
queue:*
queue type: <type 'str'>
queuedtime:*
queuedtime type: <type 'str'>
runtime:*
runtime type: <type 'str'>
score:*
score type: <type 'str'>
short_state:*
short_state type: <type 'str'>
starttime:*
starttime type: <type 'str'>
state:*
state type: <type 'str'>
submittime:*
submittime type: <type 'str'>
tag:job
tag type: <type 'str'>
timeremaining:*
timeremaining type: <type 'str'>
user:*
user type: <type 'str'>
user_hold:*
user_hold type: <type 'str'>
user_list:*
user_list type: <type 'str'>
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

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

