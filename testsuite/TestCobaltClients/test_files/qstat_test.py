import testutils

# ---------------------------------------------------------------------------------
def test_qstat_version_option():
    """
    qstat test run: version_option
        Old Command Output:
          qstat $Revision: 406 $
          cobalt $Version$
          

    """

    args      = """--version"""

    cmdout    = \
"""version: "qstat.py " + $Revision: 406 $ + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_help_option():
    """
    qstat test run: help_option
        Old Command Output:
          Usage: qstat [-d] [-f] [-l] [-u username] [--sort <fields>] [--header <fields>] [--reverse] [<jobid|queue> ...]
                 qstat [-d] -Q <queue> <queue>
                 qstat [--version]
          

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

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_debug_only():
    """
    qstat test run: debug_only
        Old Command Output:
          JobID  User  WallTime  Nodes  State  Location  
          ===============================================
          100    land  00:05:00  512    *      /tmp      
          

    """

    args      = """-d"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  User  WallTime  Nodes  State  Location  
===============================================
100    land  00:05:00  512    *      /tmp      
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:*
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_1():
    """
    qstat test run: full_option_1
        Old Command Output:
          JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
          ========================================================================================================================
          5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
          3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
          1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
          2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
          4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
          

    """

    args      = """-d -f 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_2():
    """
    qstat test run: full_option_2
        Old Command Output:
          JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
          ========================================================================================================================
          5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
          3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
          1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
          2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
          4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
          

    """

    args      = """-f 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_3():
    """
    qstat test run: full_option_3
        Old Command Output:
          JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
          ========================================================================================================================
          4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
          2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
          1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
          3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
          5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
          

    """

    args      = """-f --reverse 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
4      tmp      cat     60.0    00:20:00  378981:57:19  N/A      2048   *      /tmp      smp   2048   bbb    N/A        
2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
5      tmp      henry   30.0    00:25:00  378981:57:19  N/A      2560   *      /tmp      smp   2560   hhh    N/A        
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_4():
    """
    qstat test run: full_option_4
        Old Command Output:
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_5():
    """
    qstat test run: full_option_5
        Old Command Output:
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l --reverse 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_6():
    """
    qstat test run: full_option_6
        Old Command Output:
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l --sort user 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_7():
    """
    qstat test run: full_option_7
        Old Command Output:
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l --reverse --sort user 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_8():
    """
    qstat test run: full_option_8
        Old Command Output:
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l --sort queue 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_9():
    """
    qstat test run: full_option_9
        Old Command Output:
          JobID: 1
              JobName       : tmp
              User          : land
              WallTime      : 00:05:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 512
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 512
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : jello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  50.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 5
              JobName       : tmp
              User          : henry
              WallTime      : 00:25:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2560
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2560
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : hhh
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  30.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 2
              JobName       : tmp
              User          : house
              WallTime      : 00:10:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1024
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1024
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bello
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  55.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 4
              JobName       : tmp
              User          : cat
              WallTime      : 00:20:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 2048
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 2048
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : bbb
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  60.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          JobID: 3
              JobName       : tmp
              User          : dog
              WallTime      : 00:15:00
              QueuedTime    : 378981:57:19
              RunTime       : N/A
              TimeRemaining : N/A
              Nodes         : 1536
              State         : *
              Location      : /tmp
              Mode          : smp
              Procs         : 1536
              Preemptable   : -
              User_Hold     : False
              Admin_Hold    : -
              Queue         : aaa
              StartTime     : N/A
              Index         : -
              SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
              Path          : -
              OutputDir     : -
              ErrorPath     : /tmp
              OutputPath    : /tmp
              Envs          : 
              Command       : -
              Args          : 
              Kernel        : -
              KernelOptions : -
              Project       : my_project
              Dependencies  : -
              S             : -
              Notify        : myemail@gmail.com
              Score         :  40.0  
              Maxtasktime   : -
              attrs         : -
              dep_frac      : -
              user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
              Geometry      : Any
          
          

    """

    args      = """-f -l --reverse --sort queue 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 1
    JobName       : tmp
    User          : land
    WallTime      : 00:05:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 512
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 512
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : jello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  50.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 5
    JobName       : tmp
    User          : henry
    WallTime      : 00:25:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2560
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2560
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : hhh
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  30.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 2
    JobName       : tmp
    User          : house
    WallTime      : 00:10:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1024
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1024
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bello
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  55.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 4
    JobName       : tmp
    User          : cat
    WallTime      : 00:20:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 2048
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 2048
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : bbb
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  60.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

JobID: 3
    JobName       : tmp
    User          : dog
    WallTime      : 00:15:00
    QueuedTime    : 378981:57:19
    RunTime       : N/A
    TimeRemaining : N/A
    Nodes         : 1536
    State         : *
    Location      : /tmp
    Mode          : smp
    Procs         : 1536
    Preemptable   : -
    User_Hold     : False
    Admin_Hold    : -
    Queue         : aaa
    StartTime     : N/A
    Index         : -
    SubmitTime    : Thu Jan  1 00:01:00 1970 +0000 (UTC)
    Path          : -
    OutputDir     : -
    ErrorPath     : /tmp
    OutputPath    : /tmp
    Envs          : 
    Command       : -
    Args          : 
    Kernel        : -
    KernelOptions : -
    Project       : my_project
    Dependencies  : -
    S             : -
    Notify        : myemail@gmail.com
    Score         :  40.0  
    Maxtasktime   : -
    attrs         : -
    dep_frac      : -
    user_list     : james:land:house:dog:cat:henry:king:queen:girl:boy
    Geometry      : Any

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_10():
    """
    qstat test run: full_option_10
        Old Command Output:
          JobID  JobName  User  Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
          =======================================================================================================================
          100    tmp      land   50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
          

    """

    args      = """-f"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  JobName  User  Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
=======================================================================================================================
100    tmp      land   50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:*
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_full_option_11():
    """
    qstat test run: full_option_11
        Old Command Output:
          JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
          ========================================================================================================================
          3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
          1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
          2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
          

    """

    args      = """-f --header Jobid:State:RunTime  1 2 3"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  JobName  User   Score    WallTime  QueuedTime    RunTime  Nodes  State  Location  Mode  Procs  Queue  StartTime  
========================================================================================================================
3      tmp      dog     40.0    00:15:00  378981:57:19  N/A      1536   *      /tmp      smp   1536   aaa    N/A        
1      tmp      land    50.0    00:05:00  378981:57:19  N/A      512    *      /tmp      smp   512    jello  N/A        
2      tmp      house   55.0    00:10:00  378981:57:19  N/A      1024   *      /tmp      smp   1024   bello  N/A        
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_1():
    """
    qstat test run: long_option_1
        Old Command Output:
          JobID: 100
              User     : land
              WallTime : 00:05:00
              Nodes    : 512
              State    : *
              Location : /tmp
          
          

    """

    args      = """-l"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 100
    User     : land
    WallTime : 00:05:00
    Nodes    : 512
    State    : *
    Location : /tmp

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:*
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_2():
    """
    qstat test run: long_option_2
        Old Command Output:
          JobID: 1
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

    args      = """-l 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 1
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

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_3():
    """
    qstat test run: long_option_3
        Old Command Output:
          JobID: 5
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

    args      = """-l --reverse 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 5
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

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_4():
    """
    qstat test run: long_option_4
        Old Command Output:
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

    args      = """-l --sort user 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
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

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_5():
    """
    qstat test run: long_option_5
        Old Command Output:
          JobID: 1
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

    args      = """-l --reverse --sort user 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 1
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

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_6():
    """
    qstat test run: long_option_6
        Old Command Output:
          JobID: 1
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

    args      = """-l --sort queue 1 2 3 4 5"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID: 1
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

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:4
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:5
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_long_option_11():
    """
    qstat test run: long_option_11
        Old Command Output:
          Jobid: 1
              State   : *
              RunTime : N/A
          
          Jobid: 2
              State   : *
              RunTime : N/A
          
          Jobid: 3
              State   : *
              RunTime : N/A
          
          

    """

    args      = """-l --header Jobid:State:RunTime  1 2 3"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Jobid: 1
    State   : *
    RunTime : N/A

Jobid: 2
    State   : *
    RunTime : N/A

Jobid: 3
    State   : *
    RunTime : N/A

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:1
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:2
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:3
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_1():
    """
    qstat test run: queue_option_1
        Old Command Output:
          Name: aaa
              Users        : dog
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-f -Q -l 1 2 3"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: aaa
    Users        : dog
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:1
state:*
totalnodes:*
users:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:2
state:*
totalnodes:*
users:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:3
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_2():
    """
    qstat test run: queue_option_2
        Old Command Output:
          Name: zq
              Users        : boy
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-f --reverse -Q -l 1 2 3"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: zq
    Users        : boy
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:1
state:*
totalnodes:*
users:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:2
state:*
totalnodes:*
users:*
maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:3
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_3():
    """
    qstat test run: queue_option_3
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          zq     boy    None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          aaa    dog    None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          myq    queen  None     None     20          20         20            20            100         running  
          

    """

    args      = """-f --sort users -Q"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
zq     boy    None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
aaa    dog    None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
myq    queen  None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_4():
    """
    qstat test run: queue_option_4
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          aaa    dog    None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          myq    queen  None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          zq     boy    None     None     20          20         20            20            100         running  
          

    """

    args      = """-Q"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
aaa    dog    None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
myq    queen  None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
zq     boy    None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_5():
    """
    qstat test run: queue_option_5
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          zq     boy    None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          myq    queen  None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          aaa    dog    None     None     20          20         20            20            100         running  
          

    """

    args      = """-Q --reverse"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
zq     boy    None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
myq    queen  None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
aaa    dog    None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_6():
    """
    qstat test run: queue_option_6
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          zq     boy    None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          aaa    dog    None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          myq    queen  None     None     20          20         20            20            100         running  
          

    """

    args      = """-Q --sort users"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
zq     boy    None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
aaa    dog    None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
myq    queen  None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_7():
    """
    qstat test run: queue_option_7
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          myq    queen  None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          aaa    dog    None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          zq     boy    None     None     20          20         20            20            100         running  
          

    """

    args      = """-Q --sort users --reverse"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
myq    queen  None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
aaa    dog    None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
zq     boy    None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_8():
    """
    qstat test run: queue_option_8
        Old Command Output:
          Name: aaa
              Users        : dog
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-Q -l"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: aaa
    Users        : dog
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_9():
    """
    qstat test run: queue_option_9
        Old Command Output:
          Name: zq
              Users        : boy
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-Q --reverse -l"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: zq
    Users        : boy
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_10():
    """
    qstat test run: queue_option_10
        Old Command Output:
          Name: zq
              Users        : boy
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-Q --sort users -l"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: zq
    Users        : boy
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_11():
    """
    qstat test run: queue_option_11
        Old Command Output:
          Name: myq
              Users        : queen
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
              MinTime      : None
              MaxTime      : None
              MaxRunning   : 20
              MaxQueued    : 20
              MaxUserNodes : 20
              MaxNodeHours : 20
              TotalNodes   : 100
              State        : running
          
          

    """

    args      = """-Q --sort users --reverse -l"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name: myq
    Users        : queen
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
    MinTime      : None
    MaxTime      : None
    MaxRunning   : 20
    MaxQueued    : 20
    MaxUserNodes : 20
    MaxNodeHours : 20
    TotalNodes   : 100
    State        : running

"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_queue_option_12():
    """
    qstat test run: queue_option_12
        Old Command Output:
          Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ========================================================================================================
          aaa    dog    None     None     20          20         20            20            100         running  
          bbb    cat    None     None     20          20         20            20            100         running  
          bello  house  None     None     20          20         20            20            100         running  
          dito   king   None     None     20          20         20            20            100         running  
          hhh    henry  None     None     20          20         20            20            100         running  
          jello  land   None     None     20          20         20            20            100         running  
          kebra  james  None     None     20          20         20            20            100         running  
          myq    queen  None     None     20          20         20            20            100         running  
          yours  girl   None     None     20          20         20            20            100         running  
          zq     boy    None     None     20          20         20            20            100         running  
          

    """

    args      = """-Q --header Jobid:State:RunTime"""

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
Name   Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
========================================================================================================
aaa    dog    None     None     20          20         20            20            100         running  
bbb    cat    None     None     20          20         20            20            100         running  
bello  house  None     None     20          20         20            20            100         running  
dito   king   None     None     20          20         20            20            100         running  
hhh    henry  None     None     20          20         20            20            100         running  
jello  land   None     None     20          20         20            20            100         running  
kebra  james  None     None     20          20         20            20            100         running  
myq    queen  None     None     20          20         20            20            100         running  
yours  girl   None     None     20          20         20            20            100         running  
zq     boy    None     None     20          20         20            20            100         running  
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_QUEUES

maxnodehours:*
maxqueued:*
maxrunning:*
maxtime:*
maxusernodes:*
mintime:*
name:*
state:*
totalnodes:*
users:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_qstat_no_arguments_or_options():
    """
    qstat test run: no_arguments_or_options
        Old Command Output:
          JobID  User  WallTime  Nodes  State  Location  
          ===============================================
          100    land  00:05:00  512    *      /tmp      
          

    """

    args      = ''

    cmdout    = \
"""get_config_option: Option cqstat_header not found in section [cqm]
JobID  User  WallTime  Nodes  State  Location  
===============================================
100    land  00:05:00  512    *      /tmp      
"""

    stubout   = \
"""
GET_QUEUES

name:*
state:*

GET_JOBS

admin_hold:*
args:*
attrs:*
command:*
dep_frac:*
dependencies:*
envs:*
errorpath:*
geometry:*
index:*
jobid:*
kernel:*
kerneloptions:*
location:*
maxtasktime:*
mode:*
nodes:*
notify:*
outputdir:*
outputpath:*
path:*
preemptable:*
procs:*
project:*
queue:*
queuedtime:*
runtime:*
score:*
short_state:*
starttime:*
state:*
submittime:*
tag:job
timeremaining:*
user:*
user_hold:*
user_list:*
walltime:*
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testinfo("")

    results = testutils.run_cmd('qstat.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testinfo()

    correct = 1
    assert result == correct, "Result:\n%s" % result

