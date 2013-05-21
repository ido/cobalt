import testutils

# ---------------------------------------------------------------------------------
def test_qmove_invalid_option():
    """
    qmove test run: invalid_option

        Command Output:
          Usage: qmove.py [options] <queue name> <jobid1> [... <jobidN>]
          
          qmove.py: error: no such option: -k
          

    """

    args      = """-k"""
    exp_rs    = 512

    results = testutils.run_cmd('qmove.py',args,None) 
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
def test_qmove_queue_1():
    """
    qmove test run: queue_1

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          moved job 1 to queue 'kebra'
          moved job 2 to queue 'kebra'
          moved job 3 to queue 'kebra'
          

    """

    args      = """myq 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qmove.py',args,None) 
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
def test_qmove_queue_2():
    """
    qmove test run: queue_2

        Command Output:
          
          qmove.py -d myq 1 2 3
          
          get_config_option: Option filters not found in section [cqm]
          component: "queue-manager.get_jobs", defer: False
            get_jobs(
               [{'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 1}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 2}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'gooduser', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 3}],
               )
          
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': 512, 'walltime': 5, 'queue': 'jello', 'envs': {}, 'user_hold': False, 'jobid': 1, 'project': 'my_project', 'submittime': 60, 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': 512, 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'land'}],
               {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': 60, 'state': 'user_hold', 'score': 50, 'location': '/tmp', 'nodes': 512, 'args': '', 'is_active': False, 'user': 'land', 'procs': 512, 'walltime': 5, 'geometry': None, 'user_hold': False, 'jobid': 1, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
               gooduser,
               )
          
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': 1024, 'walltime': 10, 'queue': 'bello', 'envs': {}, 'user_hold': False, 'jobid': 2, 'project': 'my_project', 'submittime': 60, 'state': 'user_hold', 'score': 55, 'location': '/tmp', 'nodes': 1024, 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'house'}],
               {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': 60, 'state': 'user_hold', 'score': 55, 'location': '/tmp', 'nodes': 1024, 'args': '', 'is_active': False, 'user': 'house', 'procs': 1024, 'walltime': 10, 'geometry': None, 'user_hold': False, 'jobid': 2, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
               gooduser,
               )
          
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'errorpath': '/tmp', 'args': '', 'is_active': False, 'geometry': None, 'mode': 'smp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'procs': 1536, 'walltime': 15, 'queue': 'aaa', 'envs': {}, 'user_hold': False, 'jobid': 3, 'project': 'my_project', 'submittime': 60, 'state': 'user_hold', 'score': 40, 'location': '/tmp', 'nodes': 1536, 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy'], 'user': 'dog'}],
               {'errorpath': '/tmp', 'outputpath': '/tmp', 'tag': 'job', 'notify': 'myemail@gmail.com', 'has_completed': False, 'project': 'my_project', 'envs': {}, 'submittime': 60, 'state': 'user_hold', 'score': 40, 'location': '/tmp', 'nodes': 1536, 'args': '', 'is_active': False, 'user': 'dog', 'procs': 1536, 'walltime': 15, 'geometry': None, 'user_hold': False, 'jobid': 3, 'queue': 'myq', 'mode': 'smp', 'user_list': ['james', 'land', 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl', 'boy']},
               gooduser,
               )
          
          
          moved job 1 to queue 'kebra'
          moved job 2 to queue 'kebra'
          moved job 3 to queue 'kebra'
          

    """

    args      = """-d myq 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('qmove.py',args,None) 
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
def test_qmove_queue_3():
    """
    qmove test run: queue_3

        Command Output:
          get_config_option: Option filters not found in section [cqm]
          moved job 2 to queue 'kebra'
          moved job 3 to queue 'kebra'
          moved job 4 to queue 'kebra'
          

    """

    args      = """1 2 3 4"""
    exp_rs    = 0

    results = testutils.run_cmd('qmove.py',args,None) 
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
def test_qmove_queu_4():
    """
    qmove test run: queu_4

        Command Output:
          jobid must be an integer: q2
          

    """

    args      = """q1 q2 1 2 3"""
    exp_rs    = 256

    results = testutils.run_cmd('qmove.py',args,None) 
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
