import testutils

# ---------------------------------------------------------------------------------
def test_qhold_invalid_option():
    """
    qhold test run: invalid_option

        Command Output:
          Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]
          
          qhold.py: error: no such option: -k
          

    """

    args      = """-k 1"""
    exp_rs    = 512

    results = testutils.run_cmd('qhold.py',args,None) 
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
def test_qhold_debg_option():
    """
    qhold test run: debg_option

        Command Output:
          
          qhold.py -d 1
          
          component: "queue-manager.get_jobs", defer: False
            get_jobs(
               [{'user_hold': '*', 'tag': 'job', 'user': 'gooduser', 'jobid': 1}],
               )
          
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'gooduser', 'jobid': 1}],
               {'user_hold': True},
               gooduser,
               )
          
          
          Response: [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}]
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """-d 1"""
    exp_rs    = 0

    results = testutils.run_cmd('qhold.py',args,None) 
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
def test_qhold_jobid_1():
    """
    qhold test run: jobid_1

        Command Output:
          jobid must be an integer: myq
          

    """

    args      = """myq 1 2 3 4"""
    exp_rs    = 256

    results = testutils.run_cmd('qhold.py',args,None) 
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
def test_qhold_jobid_2():
    """
    qhold test run: jobid_2

        Command Output:
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
                job 2 encountered an unexpected problem while attempting to place the 'user hold'
                job 3 encountered an unexpected problem while attempting to place the 'user hold'
                job 4 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """1 2 3 4"""
    exp_rs    = 0

    results = testutils.run_cmd('qhold.py',args,None) 
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
def test_qhold_jobid_3():
    """
    qhold test run: jobid_3

        Command Output:
             Failed to place user hold on jobs: 
                job 1 encountered an unexpected problem while attempting to place the 'user hold'
          

    """

    args      = """1"""
    exp_rs    = 0

    results = testutils.run_cmd('qhold.py',args,None) 
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
def test_qhold_dependancy_option():
    """
    qhold test run: dependancy_option

        Command Output:
          Usage: qhold.py [options] <jobid1> [ ... <jobidN> ]
          
          qhold.py: error: no such option: --dependencies
          

    """

    args      = """--dependencies 1 2"""
    exp_rs    = 512

    results = testutils.run_cmd('qhold.py',args,None) 
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
