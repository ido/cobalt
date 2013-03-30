import testutils

def test_qsub_all_options():
    """
    qsub test run: all_options

    """

    args      = """-v -A myproj --attrs=a=1:b=2 --cwd /tmp -d --debuglog=/tmp/d --dependencies=1:2:3 -e /tmp/e --env v1=1:v2=2 --geometry 198x198x198x198 -h -i /bin/ls -M george@therojas.com -n10 -o /tmp/o -O /tmp --proccount 10 -qqueue --run_users georgerojas:georgerojas --run_project -t 10 --mode smp --kernel kernel -K kopts /bin/ls"""

    cmdout    = \
"""
qsub.py -v -A myproj --attrs=a=1:b=2 --cwd /tmp -d --debuglog=/tmp/d --dependencies=1:2:3 -e /tmp/e --env v1=1:v2=2 --geometry 198x198x198x198 -h -i /bin/ls -M george@therojas.com -n10 -o /tmp/o -O /tmp --proccount 10 -qqueue --run_users georgerojas:georgerojas --run_project -t 10 --mode smp --kernel kernel -K kopts /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
GET_JOBS

jobid:1
jobid:3
jobid:2

ADD_JOBS

all_dependencies:1:2:3
args:[]
attrs:{'a': '1', 'b': '2'}
cobalt_log_file:/tmp/d
command:/bin/ls
cwd:/tmp
envs:{'v1': '1', 'v2': '2'}
errorpath:/tmp/e
geometry:[198, 198, 198, 198, 2]
inputfile:/bin/ls
jobid:*
kernel:kernel
kerneloptions:kopts
mode:smp
nodes:10
notify:george@therojas.com
outputdir:/tmp
outputpath:/tmp/o
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:10
project:myproj
queue:queue
run_project:True
script_preboot:True
tag:job
umask:18
user:georgerojas
user_hold:True
user_list:['georgerojas', 'georgerojas']
walltime:10

VALIDATE_JOB

attrs:{'a': '1', 'b': '2'}
cwd:/tmp
debug:True
debuglog:/tmp/d
dependencies:1:2:3
disable_preboot:False
env:v1=1:v2=2
error:/tmp/e
forcenoval:False
geometry:198x198x198x198
held:True
inputfile:/bin/ls
kernel:kernel
kerneloptions:kopts
mode:smp
nodecount:10
notify:george@therojas.com
output:/tmp/o
outputprefix:/tmp
preemptable:False
proccount:10
project:myproj
queue:queue
run_project:True
time:10
umask:False
user_list:georgerojas:georgerojas
verbose:True
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Eric_1():
    """
    qsub test run: Eric_1

    """

    args      = """--mode c1 -n 512 --env BG_COREDUMPDISABLED=1 --proccount 512 -t 30 -q testing /gpfs/mira-fs0/projects/Acceptance/harness_workspace/at-fp-exit-th-stability_151/911_31768/src/MPI_matrix_multiplication_16384x32768_o3"""

    cmdout    = \
"""
qsub.py --mode c1 -n 512 --env BG_COREDUMPDISABLED=1 --proccount 512 -t 30 -q testing /gpfs/mira-fs0/projects/Acceptance/harness_workspace/at-fp-exit-th-stability_151/911_31768/src/MPI_matrix_multiplication_16384x32768_o3

command /gpfs/mira-fs0/projects/Acceptance/harness_workspace/at-fp-exit-th-stability_151/911_31768/src/MPI_matrix_multiplication_16384x32768_o3 not found, or is not a file
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Eric_2():
    """
    qsub test run: Eric_2

    """

    args      = """-A Acceptance -q testing -n 4096 -t 120 --mode script --env base_directory=/gpfs/mira-fs0/projects/Acceptance/harness_workspace:source_directory=/gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src/script.sh /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src/src/mc/x.adlb.12c-6_states n32768-no3pi.gfmc1a.in 8 8"""

    cmdout    = \
"""
qsub.py -A Acceptance -q testing -n 4096 -t 120 --mode script --env base_directory=/gpfs/mira-fs0/projects/Acceptance/harness_workspace:source_directory=/gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src/script.sh /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-gfmc-performance_178/1405_30034/src/src/mc/x.adlb.12c-6_states n32768-no3pi.gfmc1a.in 8 8

node count out of realistic range
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Eric_3():
    """
    qsub test run: Eric_3

    """

    args      = """-A Acceptance -q testing -n 49152 -t 60 --mode script /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-mpi-benchmark_144/905_31576/src/pingpong/script.sh /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-mpi-benchmark_144/905_31576/src"""

    cmdout    = \
"""
qsub.py -A Acceptance -q testing -n 49152 -t 60 --mode script /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-mpi-benchmark_144/905_31576/src/pingpong/script.sh /gpfs/mira-fs0/projects/Acceptance/harness_workspace/app-mpi-benchmark_144/905_31576/src

node count out of realistic range
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_no_options_passed():
    """
    qsub test run: no_options_passed

    """

    args      = """/bin/ls"""

    cmdout    = \
"""
qsub.py /bin/ls

No required options entered
'time' not provided
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_non_existant_option():
    """
    qsub test run: non_existant_option

    """

    args      = """-z -t10 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -z -t10 -n10 /bin/ls

Usage: qsub.py [options] <executable> [<excutable options>]

qsub.py: error: no such option: -z
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_debug_flag_only():
    """
    qsub test run: debug_flag_only

    """

    args      = """-d"""

    cmdout    = \
"""
qsub.py -d

No required options entered
'time' not provided
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_verbose_flag_only():
    """
    qsub test run: verbose_flag_only

    """

    args      = """-v"""

    cmdout    = \
"""
qsub.py -v

No required options entered
'time' not provided
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_non_integer_nodecount():
    """
    qsub test run: non_integer_nodecount

    """

    args      = """--mode smp -t50 -nfive --geometry 40x40x50x50 /bin/ls"""

    cmdout    = \
"""
qsub.py --mode smp -t50 -nfive --geometry 40x40x50x50 /bin/ls

Usage: qsub.py [options] <executable> [<excutable options>]

qsub.py: error: option -n: invalid integer value: 'five'
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_non_realistic_nodecount():
    """
    qsub test run: non_realistic_nodecount

    """

    args      = """--mode smp -t50 -n2048 --geometry 40x40x50x50 /bin/ls"""

    cmdout    = \
"""
qsub.py --mode smp -t50 -n2048 --geometry 40x40x50x50 /bin/ls

node count out of realistic range
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_invalid_geometry():
    """
    qsub test run: invalid_geometry

    """

    args      = """--mode smp -t50 -n10 --geometry x /bin/ls"""

    cmdout    = \
"""
qsub.py --mode smp -t50 -n10 --geometry x /bin/ls

Invalid geometry entered: 
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_no_roject_specified():
    """
    qsub test run: no_roject_specified

    """

    args      = """-A -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -A -t50 -n10 /bin/ls

'time' not provided
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_project_specified():
    """
    qsub test run: project_specified

    """

    args      = """-A who -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -A who -t50 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
project:who
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:who
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Check_attrs_1():
    """
    qsub test run: Check_attrs_1

    """

    args      = """--attrs xxxx -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py --attrs xxxx -t50 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
attrs:{'xxxx': 'true'}
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{'xxxx': 'true'}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Check_attrs_2():
    """
    qsub test run: Check_attrs_2

    """

    args      = """--attrs 1111 -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py --attrs 1111 -t50 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
attrs:{'1111': 'true'}
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{'1111': 'true'}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Check_attrs_3():
    """
    qsub test run: Check_attrs_3

    """

    args      = """--attrs xx=:yy -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py --attrs xx=:yy -t50 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
attrs:{'yy': 'true', 'xx': ''}
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{'yy': 'true', 'xx': ''}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_Check_attrs_4():
    """
    qsub test run: Check_attrs_4

    """

    args      = """--attrs xx=one:yy=1:zz=1one -t50 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py --attrs xx=one:yy=1:zz=1one -t50 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
attrs:{'yy': '1', 'xx': 'one', 'zz': '1one'}
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{'yy': '1', 'xx': 'one', 'zz': '1one'}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_cwd_option_1():
    """
    qsub test run: cwd_option_1

    """

    args      = """--cwd /tmp/ -t10 -n 10 -e p /bin/ls"""

    cmdout    = \
"""
qsub.py --cwd /tmp/ -t10 -n 10 -e p /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/tmp/
errorpath:/tmp//p
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/tmp/
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/tmp/
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:p
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_cwd_option_2():
    """
    qsub test run: cwd_option_2

    """

    args      = """--cwd /tmp -t10 -n 10 -e p /bin/ls"""

    cmdout    = \
"""
qsub.py --cwd /tmp -t10 -n 10 -e p /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/tmp
errorpath:/tmp/p
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/tmp
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/tmp
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:p
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_cwd_option_3():
    """
    qsub test run: cwd_option_3

    """

    args      = """--cwd /x -t10 -n 10 -e p /bin/ls"""

    cmdout    = \
"""
qsub.py --cwd /x -t10 -n 10 -e p /bin/ls

directory /x/p does not exist
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_cwd_option_4():
    """
    qsub test run: cwd_option_4

    """

    args      = """--cwd /tmp/ -t10 -n 10 -e p -o x /bin/ls"""

    cmdout    = \
"""
qsub.py --cwd /tmp/ -t10 -n 10 -e p -o x /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/tmp/
errorpath:/tmp//p
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/tmp/
outputpath:/tmp//x
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/tmp/
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:p
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:x
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_cwd_option_5():
    """
    qsub test run: cwd_option_5

    """

    args      = """--cwd /tmp -t10 -n 10 -e p -o x /bin/ls"""

    cmdout    = \
"""
qsub.py --cwd /tmp -t10 -n 10 -e p -o x /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/tmp
errorpath:/tmp/p
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/tmp
outputpath:/tmp/x
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/tmp
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:p
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:x
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_debuglog_option():
    """
    qsub test run: debuglog_option

    """

    args      = """-t10 -n 10 -e p -o x --debuglog y /bin/ls"""

    cmdout    = \
"""
qsub.py -t10 -n 10 -e p -o x --debuglog y /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
cobalt_log_file:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients/y
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
errorpath:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients/p
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
outputpath:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients/x
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:y
dependencies:False
disable_preboot:False
env:False
error:p
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:x
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_inputfile_option_1():
    """
    qsub test run: inputfile_option_1

    """

    args      = """-i none -t10 -n 10 /bin/ls"""

    cmdout    = \
"""
qsub.py -i none -t10 -n 10 /bin/ls

file /Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients/none not found, or is not a file
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_inputfile_option_2():
    """
    qsub test run: inputfile_option_2

    """

    args      = """-i y -t10 -n 10 /bin/ls"""

    cmdout    = \
"""
qsub.py -i y -t10 -n 10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
inputfile:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients/y
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:y
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_email_option():
    """
    qsub test run: email_option

    """

    args      = """-M g -t10 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -M g -t10 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:False
nodes:10
notify:g
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:g
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_outputprefix():
    """
    qsub test run: outputprefix

    """

    args      = """-O /tmp -t10 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -O /tmp -t10 -n10 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
WARNING: failed to create cobalt log file at: /tmp.cobaltlog
         Permission denied
"""

    stubout   = \
"""
ADD_JOBS

args:[]
cobalt_log_file:/tmp.cobaltlog
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
errorpath:/tmp.error
jobid:*
kernel:default
mode:False
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
outputpath:/tmp.output
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:False
nodecount:10
notify:False
output:False
outputprefix:/tmp
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_invalid_user():
    """
    qsub test run: invalid_user

    """

    args      = """-run_users bobo -t10 -n10 /bin/ls"""

    cmdout    = \
"""
qsub.py -run_users bobo -t10 -n10 /bin/ls

Usage: qsub.py [options] <executable> [<excutable options>]

qsub.py: error: no such option: -r
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_mode_option_1():
    """
    qsub test run: mode_option_1

    """

    args      = """-t10 -n512 --proccount 1023 --mode dual /bin/ls"""

    cmdout    = \
"""
qsub.py -t10 -n512 --proccount 1023 --mode dual /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:dual
nodes:512
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:1023
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:dual
nodecount:512
notify:False
output:False
outputprefix:False
preemptable:False
proccount:1023
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_mode_option_2():
    """
    qsub test run: mode_option_2

    """

    args      = """-t10 -n512 --proccount 1023 --mode vn /bin/ls"""

    cmdout    = \
"""
qsub.py -t10 -n512 --proccount 1023 --mode vn /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
jobid:*
kernel:default
mode:vn
nodes:512
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:1023
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:10

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:False
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:vn
nodecount:512
notify:False
output:False
outputprefix:False
preemptable:False
proccount:1023
project:False
queue:default
run_project:False
time:10
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------


def test_qsub_mode_option_3():
    """
    qsub test run: mode_option_3

    """

    args      = """--mode co -t50 -n10 --geometry 40x40x50x50 /bin/ls"""

    cmdout    = \
"""
qsub.py --mode co -t50 -n10 --geometry 40x40x50x50 /bin/ls

get_config_option: Option filters not found in section [cqm]
1
"""

    stubout   = \
"""
ADD_JOBS

args:[]
command:/bin/ls
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
geometry:[40, 40, 50, 50, 2]
jobid:*
kernel:default
mode:co
nodes:10
outputdir:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
path:/Users/georgerojas/p/Cobalt/client-refactor/src/clients:/Users/georgerojas/p/Cobalt/client-refactor/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/git/bin:~/bin
procs:False
queue:default
run_project:False
script_preboot:True
tag:job
umask:18
user:georgerojas
user_list:['georgerojas']
walltime:50

VALIDATE_JOB

attrs:{}
cwd:/Users/georgerojas/p/Cobalt/client-refactor/testsuite/TestCobaltClients
debug:False
debuglog:False
dependencies:False
disable_preboot:False
env:False
error:False
forcenoval:False
geometry:40x40x50x50
held:False
inputfile:False
kernel:default
kerneloptions:False
mode:co
nodecount:10
notify:False
output:False
outputprefix:False
preemptable:False
proccount:False
project:False
queue:default
run_project:False
time:50
umask:False
user_list:False
verbose:False
version:False

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('qsub.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

# ---------------------------------------------------------------------------------

