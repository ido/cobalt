import testutils

# ---------------------------------------------------------------------------------
def test_qsub_all_options_1():
    """
    qsub test run: all_options_1

    """

    args      = """-v -A myproj --attrs=a=1:b=2 --cwd /tmp -d --debuglog=/tmp/d --dependencies=1:2:3 -e /tmp/e --env v1=1:v2=2 --geometry 198x198x198x198 -h -i /bin/ls -M myemal@gmail.com -n10 -o /tmp/o -O tmp --proccount 10 -qqueue --run_users user1:user2:user3 --run_project -t 10 --mode script --kernel kernel -K kopts /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = \
"""
qsub.py -v -A myproj --attrs=a=1:b=2 --cwd /tmp -d --debuglog=/tmp/d --dependencies=1:2:3 -e /tmp/e --env v1=1:v2=2 --geometry 198x198x198x198 -h -i /bin/ls -M myemal@gmail.com -n10 -o /tmp/o -O tmp --proccount 10 -qqueue --run_users user1:user2:user3 --run_project -t 10 --mode script --kernel kernel -K kopts /bin/ls

component: "queue-manager.get_jobs", defer: True
  get_jobs(
     [{'jobid': 1}, {'jobid': 3}, {'jobid': 2}],
     )


component: "system.validate_job", defer: False
  validate_job(
     {'kernel': 'kernel', 'verbose': True, 'held': True, 'notify': 'myemal@gmail.com', 'ion_kerneloptions': False, 'project': 'myproj', 'preemptable': False, 'forcenoval': False, 'umask': False, 'version': False, 'env': 'v1=1:v2=2', 'cwd': '/tmp', 'run_project': True, 'outputprefix': 'tmp', 'kerneloptions': 'kopts', 'time': '10', 'jobname': False, 'debug': True, 'dependencies': '1:2:3', 'debuglog': '/tmp/d', 'ion_kernel': 'default', 'proccount': '10', 'disable_preboot': False, 'geometry': '198x198x198x198', 'queue': 'queue', 'mode': 'script', 'error': '/tmp/e', 'nodecount': '10', 'output': '/tmp/o', 'inputfile': '/bin/ls', 'attrs': {'a': '1', 'b': '2'}, 'user_list': 'user1:user2:user3', 'interactive': False},
     )


fd 1 not associated with a terminal device
component: "queue-manager.add_jobs", defer: False
  add_jobs(
     [{'kernel': 'kernel', 'errorpath': '/tmp/e', 'outputpath': '/tmp/o', 'tag': 'job', 'notify': 'myemal@gmail.com', 'outputdir': '/tmp', 'queue': 'queue', 'envs': {'v1': '1', 'v2': '2'}, 'umask': 18, 'submithost': 'foo.bar', 'nodes': 10, 'cwd': '/tmp', 'run_project': True, 'ttysession': None, 'kerneloptions': 'kopts', 'args': [], 'cobalt_log_file': '/tmp/d', 'user': 'gooduser', 'path': '/tmp', 'ion_kernel': 'default', 'procs': '10', 'walltime': '10', 'geometry': [198, 198, 198, 198, 2], 'user_hold': True, 'jobid': '*', 'project': 'myproj', 'script_preboot': True, 'command': '/bin/ls', 'mode': 'script', 'all_dependencies': '1:2:3', 'attrs': {'a': '1', 'b': '2'}, 'user_list': ['gooduser', 'user1', 'user2', 'user3'], 'inputfile': '/bin/ls'}],
     )


Environment Vars: {'v1': '1', 'v2': '2'}
"""

    stubout   = \
"""
GET_JOBS

jobid:1
jobid type: <type 'int'>
jobid:3
jobid type: <type 'int'>
jobid:2
jobid type: <type 'int'>

ADD_JOBS

all_dependencies:1:2:3
all_dependencies type: <type 'str'>
args:[]
args type: <type 'list'>
attrs:{'a': '1', 'b': '2'}
attrs type: <type 'dict'>
cobalt_log_file:/tmp/d
cobalt_log_file type: <type 'str'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'v1': '1', 'v2': '2'}
envs type: <type 'dict'>
errorpath:/tmp/e
errorpath type: <type 'str'>
geometry:[198, 198, 198, 198, 2]
geometry type: <type 'list'>
inputfile:/bin/ls
inputfile type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:kernel
kernel type: <type 'str'>
kerneloptions:kopts
kerneloptions type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:myemal@gmail.com
notify type: <type 'str'>
outputdir:/tmp
outputdir type: <type 'str'>
outputpath:/tmp/o
outputpath type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:10
procs type: <type 'str'>
project:myproj
project type: <type 'str'>
queue:queue
queue type: <type 'str'>
run_project:True
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_hold:True
user_hold type: <type 'bool'>
user_list:['gooduser', 'user1', 'user2', 'user3']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{'a': '1', 'b': '2'}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:True
debug type: <type 'bool'>
debuglog:/tmp/d
debuglog type: <type 'str'>
dependencies:1:2:3
dependencies type: <type 'str'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:v1=1:v2=2
env type: <type 'str'>
error:/tmp/e
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:198x198x198x198
geometry type: <type 'str'>
held:True
held type: <type 'bool'>
inputfile:/bin/ls
inputfile type: <type 'str'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:kernel
kernel type: <type 'str'>
kerneloptions:kopts
kerneloptions type: <type 'str'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:myemal@gmail.com
notify type: <type 'str'>
output:/tmp/o
output type: <type 'str'>
outputprefix:tmp
outputprefix type: <type 'str'>
preemptable:False
preemptable type: <type 'bool'>
proccount:10
proccount type: <type 'str'>
project:myproj
project type: <type 'str'>
queue:queue
queue type: <type 'str'>
run_project:True
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:user1:user2:user3
user_list type: <type 'str'>
verbose:True
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_misc_1():
    """
    qsub test run: misc_1

    """

    args      = """--mode script -n 512 --env BG_COREDUMPDISABLED=1 --proccount 512 -t 30 -q testing /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'BG_COREDUMPDISABLED': '1'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:512
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:testing
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:30
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:BG_COREDUMPDISABLED=1
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:512
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:512
proccount type: <type 'str'>
project:False
project type: <type 'bool'>
queue:testing
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:30
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_no_options_passed():
    """
    qsub test run: no_options_passed

    """

    args      = """/bin/ls"""

    cmdout    = \
"""Usage: qsub.py --help
Usage: qsub.py [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.


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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_non_existant_option():
    """
    qsub test run: non_existant_option

    """

    args      = """-z -t10 -n10 /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""Usage: qsub.py --help
Usage: qsub.py [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.


qsub.py: error: no such option: -z
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_debug_flag_only_1():
    """
    qsub test run: debug_flag_only_1

    """

    args      = """-d"""

    cmdout    = \
"""Usage: qsub.py --help
Usage: qsub.py [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.


"""

    cmderr    = \
"""
qsub.py -d

No executable or script specified

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_debug_flag_only_2():
    """
    qsub test run: debug_flag_only_2

    """

    args      = """-debug"""

    cmdout    = \
"""Usage: qsub.py --help
Usage: qsub.py [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.


"""

    cmderr    = \
"""
qsub.py -debug

No executable or script specified

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_verbose_flag_only():
    """
    qsub test run: verbose_flag_only

    """

    args      = """-v"""

    cmdout    = \
"""Usage: qsub.py --help
Usage: qsub.py [options] <executable> [<excutable options>]

Refer to man pages for JOBID EXPANSION and SCRIPT JOB DIRECTIVES.


"""

    cmderr    = \
"""No executable or script specified

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_non_integer_nodecount():
    """
    qsub test run: non_integer_nodecount

    """

    args      = """--mode smp -t50 -nfive --geometry 40x40x50x50   /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'smp' not valid, valid modes are
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_non_realistic_nodecount():
    """
    qsub test run: non_realistic_nodecount

    """

    args      = """--mode smp -t50 -n2048 --geometry 40x40x50x50x1 /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""Specifed mode 'smp' not valid, valid modes are
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_1():
    """
    qsub test run: invalid_geometry_1

    """

    args      = """--mode script -t50 -n10 --geometry x /bin/ls"""

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_2():
    """
    qsub test run: invalid_geometry_2

    """

    args      = """--mode script -t50 -n10 --geometry 1x2x3x4 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
geometry:[1, 2, 3, 4, 2]
geometry type: <type 'list'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:1x2x3x4
geometry type: <type 'str'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_3():
    """
    qsub test run: invalid_geometry_3

    """

    args      = """--mode script -t50 -n10 --geometry 1x2x3x4 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
geometry:[1, 2, 3, 4, 2]
geometry type: <type 'list'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:1x2x3x4
geometry type: <type 'str'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_4():
    """
    qsub test run: invalid_geometry_4

    """

    args      = """--mode script -t50 -n10 --geometry 48x48x48x48x2  /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
geometry:[48, 48, 48, 48, 2]
geometry type: <type 'list'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:48x48x48x48x2
geometry type: <type 'str'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_5():
    """
    qsub test run: invalid_geometry_5

    """

    args      = """--mode script -t50 -n10 --geometry 48x48x48x48x3  /bin/ls"""

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_geometry_6():
    """
    qsub test run: invalid_geometry_6

    """

    args      = """--mode script -t50 -n10 --geometry 128x64x32x4    /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
geometry:[128, 64, 32, 4, 2]
geometry type: <type 'list'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:128x64x32x4
geometry type: <type 'str'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_no_roject_specified():
    """
    qsub test run: no_roject_specified

    """

    args      = """-A -t50 -n10 /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""'time' not provided
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_project_specified():
    """
    qsub test run: project_specified

    """

    args      = """-A who -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
project:who
project type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:who
project type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_Check_attrs_1():
    """
    qsub test run: Check_attrs_1

    """

    args      = """--attrs xxxx -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
attrs:{'xxxx': 'true'}
attrs type: <type 'dict'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{'xxxx': 'true'}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_Check_attrs_2():
    """
    qsub test run: Check_attrs_2

    """

    args      = """--attrs 1111 -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
attrs:{'1111': 'true'}
attrs type: <type 'dict'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{'1111': 'true'}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_Check_attrs_3():
    """
    qsub test run: Check_attrs_3

    """

    args      = """--attrs xx=:yy -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
attrs:{'yy': 'true', 'xx': ''}
attrs type: <type 'dict'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{'yy': 'true', 'xx': ''}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_Check_attrs_4():
    """
    qsub test run: Check_attrs_4

    """

    args      = """--attrs xx=one:yy=1:zz=1one -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
attrs:{'yy': '1', 'xx': 'one', 'zz': '1one'}
attrs type: <type 'dict'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{'yy': '1', 'xx': 'one', 'zz': '1one'}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_cwd_option_1():
    """
    qsub test run: cwd_option_1

    """

    args      = """--cwd /tmp/ -t10 -n 10 -e p /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp/
cwd type: <type 'str'>
errorpath:/tmp//p
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp/
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp/
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:p
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_cwd_option_2():
    """
    qsub test run: cwd_option_2

    """

    args      = """--cwd /tmp -t10 -n 10 -e p /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
errorpath:/tmp/p
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:p
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_cwd_option_3():
    """
    qsub test run: cwd_option_3

    """

    args      = """--cwd /x -t10 -n 10 -e p /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""directory /x/p does not exist
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_cwd_option_4():
    """
    qsub test run: cwd_option_4

    """

    args      = """--cwd /tmp/ -t10 -n 10 -e p -o x /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp/
cwd type: <type 'str'>
errorpath:/tmp//p
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp/
outputdir type: <type 'str'>
outputpath:/tmp//x
outputpath type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp/
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:p
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:x
output type: <type 'str'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_cwd_option_5():
    """
    qsub test run: cwd_option_5

    """

    args      = """--cwd /tmp -t10 -n 10 -e p -o x /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
errorpath:/tmp/p
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
outputpath:/tmp/x
outputpath type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:p
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:x
output type: <type 'str'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_debuglog_option():
    """
    qsub test run: debuglog_option

    """

    args      = """-t10 -n 10 -e p -o x --debuglog y /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
cobalt_log_file:/tmp/y
cobalt_log_file type: <type 'str'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
errorpath:/tmp/p
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
outputpath:/tmp/x
outputpath type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:y
debuglog type: <type 'str'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:p
error type: <type 'str'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:x
output type: <type 'str'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_inputfile_option_1():
    """
    qsub test run: inputfile_option_1

    """

    args      = """-i none -t10 -n 10 /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""file /tmp/none not found, or is not a file
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_inputfile_option_2():
    """
    qsub test run: inputfile_option_2

    """

    args      = """-i y -t10 -n 10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
inputfile:/tmp/y
inputfile type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:y
inputfile type: <type 'str'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_email_option():
    """
    qsub test run: email_option

    """

    args      = """-M g -t10 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
notify:g
notify type: <type 'str'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:g
notify type: <type 'str'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_outputprefix():
    """
    qsub test run: outputprefix

    """

    args      = """-O tmp -t10 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
cobalt_log_file:/tmp/tmp.cobaltlog
cobalt_log_file type: <type 'str'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
errorpath:/tmp/tmp.error
errorpath type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
outputpath:/tmp/tmp.output
outputpath type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:tmp
outputprefix type: <type 'str'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_invalid_user():
    """
    qsub test run: invalid_user

    """

    args      = """--run_users naughtyuser -t10 -n10 /bin/ls"""

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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_mode_option_1():
    """
    qsub test run: mode_option_1

    """

    args      = """-t10 -n512 --proccount 1023 --mode vn /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:vn
mode type: <type 'str'>
nodes:512
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:1023
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:vn
mode type: <type 'str'>
nodecount:512
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:1023
proccount type: <type 'str'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_mode_option_2():
    """
    qsub test run: mode_option_2

    """

    args      = """-t10 -n512 --proccount 1023 --mode vn /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:vn
mode type: <type 'str'>
nodes:512
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:1023
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:vn
mode type: <type 'str'>
nodecount:512
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:1023
proccount type: <type 'str'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_mode_option_3():
    """
    qsub test run: mode_option_3

    """

    args      = """--mode script -t50 -n10 --geometry 40x40x50x50 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
geometry:[40, 40, 50, 50, 2]
geometry type: <type 'list'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:40x40x50x50
geometry type: <type 'str'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_mode_option_4():
    """
    qsub test run: mode_option_4

    """

    args      = """-A Acceptance -q testing -n 49152 -t 60 --mode script /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""node count out of realistic range
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_preboot_option():
    """
    qsub test run: preboot_option

    """

    args      = """--disable_preboot -t10 -n512 --proccount 1023 --mode vn /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:vn
mode type: <type 'str'>
nodes:512
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:1023
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:False
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:10
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:True
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:vn
mode type: <type 'str'>
nodecount:512
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:1023
proccount type: <type 'str'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:10
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_env_option_1():
    """
    qsub test run: env_option_1

    """

    args      = """--env var1=val1,var2=val2 -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'var1': 'val1,var2=val2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:var1=val1,var2=val2
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_env_option_2():
    """
    qsub test run: env_option_2

    """

    args      = """--env var1=val1:var2=val2 -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'var1': 'val1', 'var2': 'val2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:var1=val1:var2=val2
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_env_option_3():
    """
    qsub test run: env_option_3

    """

    args      = """--env "var1=val1:var2=svar1\=sval1\:svar2\=sval2:var3=val3" -t50 -n10 -d /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = \
"""
qsub.py --env var1=val1:var2=svar1\=sval1\:svar2\=sval2:var3=val3 -t50 -n10 -d /bin/ls

component: "system.validate_job", defer: False
  validate_job(
     {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': 'var1=val1:var2=svar1\\=sval1\\:svar2\\=sval2:var3=val3', 'cwd': '/tmp', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '50', 'jobname': False, 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': False, 'error': False, 'nodecount': '10', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
     )


fd 1 not associated with a terminal device
component: "queue-manager.add_jobs", defer: False
  add_jobs(
     [{'kernel': 'default', 'tag': 'job', 'outputdir': '/tmp', 'envs': {'var1': 'val1', 'var3': 'val3', 'var2': 'svar1=sval1:svar2=sval2'}, 'umask': 18, 'command': '/bin/ls', 'nodes': 10, 'cwd': '/tmp', 'run_project': False, 'ttysession': None, 'args': [], 'user': 'gooduser', 'path': '/tmp', 'ion_kernel': 'default', 'procs': '512', 'walltime': '50', 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'submithost': 'foo.bar', 'mode': 'c1', 'user_list': ['gooduser']}],
     )


Environment Vars: {'var1': 'val1', 'var3': 'val3', 'var2': 'svar1=sval1:svar2=sval2'}
"""

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'var1': 'val1', 'var3': 'val3', 'var2': 'svar1=sval1:svar2=sval2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:True
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:var1=val1:var2=svar1\=sval1\:svar2\=sval2:var3=val3
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_env_option_4():
    """
    qsub test run: env_option_4

    """

    args      = """--env var1=val1 --env "var2=svar1\=sval1\:svar2\=sval2" --env var3=val3 -t50 -n10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'var1': 'val1', 'var3': 'val3', 'var2': 'svar1=sval1:svar2=sval2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:var1=val1:var2=svar1\=sval1\:svar2\=sval2:var3=val3
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_script_1():
    """
    qsub test run: script_1

    """

    args      = """cobalt_script1.sh"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/tmp/cobalt_script1.sh
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'a': '1', 'c': '3', 'b': '2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:100
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:75
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:a=1:c=3:b=2
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:100
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:75
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_script_2():
    """
    qsub test run: script_2

    """

    args      = """-t 50 cobalt_script1.sh"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/tmp/cobalt_script1.sh
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
envs:{'a': '1', 'c': '3', 'b': '2'}
envs type: <type 'dict'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:script
mode type: <type 'str'>
nodes:100
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:a=1:c=3:b=2
env type: <type 'str'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:script
mode type: <type 'str'>
nodecount:100
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_script_3():
    """
    qsub test run: script_3

    """

    args      = """--mode vn cobalt_script1.sh"""

    cmdout    = ''

    cmderr    = \
"""Mode already set to 'script' and trying to set it again to 'vn'
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_script_4():
    """
    qsub test run: script_4

    """

    args      = """-d cobalt_script2.sh"""

    cmdout    = ''

    cmderr    = \
"""
qsub.py -d cobalt_script2.sh

Mode already set to 'script' and trying to set it again to 'vn'
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_walltime_0():
    """
    qsub test run: walltime_0

    """

    args      = """-t0 -n 10 /bin/ls"""

    cmdout    = \
"""1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

args:[]
args type: <type 'list'>
command:/bin/ls
command type: <type 'str'>
cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:c1
mode type: <type 'str'>
nodes:10
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:0
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:False
mode type: <type 'bool'>
nodecount:10
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:0
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_1():
    """
    qsub test run: interactive_1

    """

    args      = """-I -t50 -n 1 /bin/ls"""

    cmdout    = ''

    cmderr    = \
"""An executable may not be specified if using the interactive option.
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_2():
    """
    qsub test run: interactive_2

    """

    args      = """-I -t50 -n 1 -i inputfile"""

    cmdout    = ''

    cmderr    = \
"""Cannot specify an input file for interactive jobs.
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_4():
    """
    qsub test run: interactive_4

    """

    args      = """-I -t50 -n 1 --mode script"""

    cmdout    = ''

    cmderr    = \
"""Mode already set to 'interactive' and trying to set it again to 'script'
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

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_5():
    """
    qsub test run: interactive_5

    """

    args      = """-I -t50 -n 1"""

    cmdout    = \
"""Wait for job 1 to start...
Opening interactive session to /
Deleting interactive job 1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:interactive
mode type: <type 'str'>
nodes:1
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:interactive
mode type: <type 'str'>
nodecount:1
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>


GET_IMPLEMENTATION


GET_JOBS

jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
resid:*
resid type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>

DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("JOB_RUNNING")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_6():
    """
    qsub test run: interactive_6

    """

    args      = """--interactive -t50 -n 1"""

    cmdout    = \
"""Wait for job 1 to start...
Opening interactive session to /
Deleting interactive job 1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:interactive
mode type: <type 'str'>
nodes:1
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:interactive
mode type: <type 'str'>
nodecount:1
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>


GET_IMPLEMENTATION


GET_JOBS

jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
resid:*
resid type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>

DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("JOB_RUNNING")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qsub_interactive_7():
    """
    qsub test run: interactive_7

    """

    args      = """--mode interactive -t50 -n 1"""

    cmdout    = \
"""Wait for job 1 to start...
Opening interactive session to /
Deleting interactive job 1
"""

    cmderr    = ''

    stubout   = \
"""
ADD_JOBS

cwd:/tmp
cwd type: <type 'str'>
ion_kernel:default
ion_kernel type: <type 'str'>
jobid:*
jobid type: <type 'str'>
kernel:default
kernel type: <type 'str'>
mode:interactive
mode type: <type 'str'>
nodes:1
nodes type: <type 'int'>
outputdir:/tmp
outputdir type: <type 'str'>
path:/tmp
path type: <type 'str'>
procs:512
procs type: <type 'str'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
script_preboot:True
script_preboot type: <type 'bool'>
submithost:foo.bar
submithost type: <type 'str'>
tag:job
tag type: <type 'str'>
ttysession:None
ttysession type: <type 'NoneType'>
umask:18
umask type: <type 'int'>
user:gooduser
user type: <type 'str'>
user_list:['gooduser']
user_list type: <type 'list'>
walltime:50
walltime type: <type 'str'>

VALIDATE_JOB

attrs:{}
attrs type: <type 'dict'>
cwd:/tmp
cwd type: <type 'str'>
debug:False
debug type: <type 'bool'>
debuglog:False
debuglog type: <type 'bool'>
dependencies:False
dependencies type: <type 'bool'>
disable_preboot:False
disable_preboot type: <type 'bool'>
env:False
env type: <type 'bool'>
error:False
error type: <type 'bool'>
forcenoval:False
forcenoval type: <type 'bool'>
geometry:False
geometry type: <type 'bool'>
held:False
held type: <type 'bool'>
inputfile:False
inputfile type: <type 'bool'>
interactive:False
interactive type: <type 'bool'>
ion_kernel:default
ion_kernel type: <type 'str'>
ion_kerneloptions:False
ion_kerneloptions type: <type 'bool'>
jobname:False
jobname type: <type 'bool'>
kernel:default
kernel type: <type 'str'>
kerneloptions:False
kerneloptions type: <type 'bool'>
mode:interactive
mode type: <type 'str'>
nodecount:1
nodecount type: <type 'str'>
notify:False
notify type: <type 'bool'>
output:False
output type: <type 'bool'>
outputprefix:False
outputprefix type: <type 'bool'>
preemptable:False
preemptable type: <type 'bool'>
proccount:False
proccount type: <type 'bool'>
project:False
project type: <type 'bool'>
queue:default
queue type: <type 'str'>
run_project:False
run_project type: <type 'bool'>
time:50
time type: <type 'str'>
umask:False
umask type: <type 'bool'>
user_list:False
user_list type: <type 'bool'>
verbose:False
verbose type: <type 'bool'>
version:False
version type: <type 'bool'>


GET_IMPLEMENTATION


GET_JOBS

jobid:1
jobid type: <type 'int'>
location:*
location type: <type 'str'>
resid:*
resid type: <type 'str'>
state:*
state type: <type 'str'>
tag:job
tag type: <type 'str'>

DEL_JOBS

force:False
whoami:gooduser
jobid:1
jobid type: <type 'int'>
tag:job
tag type: <type 'str'>
user:gooduser
user type: <type 'str'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("JOB_RUNNING")

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

