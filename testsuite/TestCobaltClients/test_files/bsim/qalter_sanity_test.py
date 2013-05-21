import testutils

# ---------------------------------------------------------------------------------
def test_qalter_simple_1():
    """
    qalter test run: simple_1

        Command Output:
          
          qalter.py -d -n30
          
          No Jobid(s) given
          

    """

    args      = """-d -n30"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_simple_2():
    """
    qalter test run: simple_2

        Command Output:
          
          qalter.py -d -n30 1
          
          get_config_option: Option filters not found in section [cqm]
          component: "queue-manager.get_jobs", defer: False
            get_jobs(
               [{'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'is_active': '*', 'procs': '*', 'jobid': 1}],
               )
          
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'errorpath': '/tmp', 'args': '', 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': 512, 'walltime': 5, 'queue': 'jello', 'envs': {}, 'user_hold': False, 'jobid': 1, 'project': 'my_project', 'submittime': 60, 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': 512, 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'land'}],
               {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': 60, 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': 30, 'args': '', 'user': 'land', 'procs': 30, 'walltime': 5, 'geometry': None, 'user_hold': False, 'jobid': 1, 'queue': 'jello', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
               gooduser,
               )
          
          
          nodes changed from 512 to 30
          procs changed from 512 to 30
          [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
          

    """

    args      = """-d -n30 1"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_simple_3():
    """
    qalter test run: simple_3

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          nodes changed from 512 to 30
          procs changed from 512 to 30
          

    """

    args      = """-n30 1"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_1():
    """
    qalter test run: time_1

        Command Output:
          jobid must be an integer: n10
          

    """

    args      = """-v n10 -t5 1 2 3"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_2():
    """
    qalter test run: time_2

        Command Output:
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
          

    """

    args      = """-v -n10 -t+5 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_3():
    """
    qalter test run: time_3

        Command Output:
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
          

    """

    args      = """-v -n10 -t+20 1 2 3 4 5 6 7"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_4():
    """
    qalter test run: time_4

        Command Output:
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
          

    """

    args      = """-v -n10 -t30 1 2 3 4 5 6 7 10 15"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_5():
    """
    qalter test run: time_5

        Command Output:
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
          

    """

    args      = """-v -n10 -t00:00:30 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_6():
    """
    qalter test run: time_6

        Command Output:
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
          

    """

    args      = """-v -n10 -t+00:00:30 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_7():
    """
    qalter test run: time_7

        Command Output:
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
          

    """

    args      = """-v -n10 -t 00:00:30 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_time_8():
    """
    qalter test run: time_8

        Command Output:
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
          

    """

    args      = """-v -n10 -t +00:00:30 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_invalid_option():
    """
    qalter test run: invalid_option

        Command Output:
          Usage: qalter.py [options] <jobid1> ... <jobidN>
          
          qalter.py: error: no such option: -m
          

    """

    args      = """-v -m j@gmail.com"""
    exp_rs    = 512

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_email_option():
    """
    qalter test run: email_option

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          notify changed from myemail@gmail.com to j@gmail.com
          notify changed from myemail@gmail.com to j@gmail.com
          

    """

    args      = """-v -M j@gmail.com 1 2"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_mode_1():
    """
    qalter test run: mode_1

        Command Output:
          Specifed mode 'jjj' not valid, valid modes are
          co
          vn
          script
          

    """

    args      = """-v --mode jjj  -n40 -t50 -e p -o o 1 2 3"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_mode_2():
    """
    qalter test run: mode_2

        Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

    """

    args      = """-v --mode dual -n40 -t50 -e p -o o 1 2 3"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_proccount_1():
    """
    qalter test run: proccount_1

        Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

    """

    args      = """-v --mode dual -n512 --proccount one -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_proccount_2():
    """
    qalter test run: proccount_2

        Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

    """

    args      = """-v --mode dual -n512 --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_invalid_nodecount():
    """
    qalter test run: invalid_nodecount

        Command Output:
          Specifed mode 'dual' not valid, valid modes are
          co
          vn
          script
          

    """

    args      = """-v --mode dual -nfiver --proccount 1023 -t50 -e /tmp/p -o /tmp/o 1 2 3 4 5 6 7 8 9 10"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_user_2():
    """
    qalter test run: user_2

        Command Output:
          user naughtyuser does not exist.
          

    """

    args      = """-v --run_users user1:naughtyuser 1 2 3 4 5"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_project():
    """
    qalter test run: project

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          run_project set to True
          user_list changed from ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'] to ['gooduser']
          

    """

    args      = """-v --run_project 10 20 30"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_geometry_1():
    """
    qalter test run: geometry_1

        Command Output:
          Invalid geometry entered: 
          

    """

    args      = """-v --geometry 10 1 2 3 4 5"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_geometry_2():
    """
    qalter test run: geometry_2

        Command Output:
          Invalid geometry entered: 
          

    """

    args      = """-v --geometry 10x10x10x10x10 1 2 3 4 5"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_geometry_5():
    """
    qalter test run: geometry_5

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          geometry changed from None to [4, 4, 4, 4, 2]
          geometry changed from None to [4, 4, 4, 4, 2]
          geometry changed from None to [4, 4, 4, 4, 2]
          geometry changed from None to [4, 4, 4, 4, 2]
          

    """

    args      = """-v --geometry 04x04x04x04x2  1 2 3 4"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_preboot_1():
    """
    qalter test run: preboot_1

        Command Output:
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
          

    """

    args      = """-v --enable_preboot --run_project 10 20 30"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_preboot_2():
    """
    qalter test run: preboot_2

        Command Output:
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
          

    """

    args      = """-v --disable_preboot --run_project 10 20 30"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_defer_1():
    """
    qalter test run: defer_1

        Command Output:
          No Jobid(s) given
          

    """

    args      = """--defer"""
    exp_rs    = 256

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qalter_defer_2():
    """
    qalter test run: defer_2

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          updating scores for jobs: 1, 2, 3, 4, 5
          

    """

    args      = """--defer 1 2 3 4 5"""
    exp_rs    = 0

    results = testutils.run_cmd('qalter.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), args)

    assert result, errmsg
