import testutils

# ---------------------------------------------------------------------------------
def test_qselect_invalid_option():
    """
    qselect test run: invalid_option

        Command Output:
        
        Command Error/Debug:Usage: qselect.py [options]
        
        qselect.py: error: no such option: -k
        
        
    """

    args      = """-k"""
    exp_rs    = 512

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_only_arg():
    """
    qselect test run: only_arg

        Command Output:
        
        Command Error/Debug:qselect takes no arguments
        
        
    """

    args      = """1"""
    exp_rs    = 256

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_no_args_opts():
    """
    qselect test run: no_args_opts

        Command Output:
           The following jobs matched your query:
              5
              6
              7
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_debug_flag():
    """
    qselect test run: debug_flag

        Command Output:
           The following jobs matched your query:
              5
              6
              7
        
        Command Error/Debug:
        qselect.py -d
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'project': '*', 'queue': '*', 'state': '*', 'tag': 'job', 'mode': '*', 'nodes': '*', 'walltime': '*', 'jobid': '*'}],
             )
        
        
        [{'project': None, 'jobid': 5, 'queue': 'default', 'state': 'queued', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 165}, {'project': None, 'jobid': 6, 'queue': 'default', 'state': 'queued', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 150}, {'project': None, 'jobid': 7, 'queue': 'default', 'state': 'queued', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 150}]
        
        
    """

    args      = """-d"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_held_option():
    """
    qselect test run: held_option

        Command Output:
        
        Command Error/Debug:Failed to match any jobs
        
        
    """

    args      = """-h user_hold"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_nodecount_option():
    """
    qselect test run: nodecount_option

        Command Output:
        
        Command Error/Debug:Failed to match any jobs
        
        
    """

    args      = """-n 312"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_state_and_nodecount():
    """
    qselect test run: state_and_nodecount

        Command Output:
        
        Command Error/Debug:Failed to match any jobs
        
        
    """

    args      = """-n 312 -h user_hold"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_walltime():
    """
    qselect test run: walltime

        Command Output:
        
        Command Error/Debug:Failed to match any jobs
        
        
    """

    args      = """-t 10:10:10"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_mode():
    """
    qselect test run: mode

        Command Output:
        
        Command Error/Debug:Failed to match any jobs
        
        
    """

    args      = """--mode vn"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qselect_verbose():
    """
    qselect test run: verbose

        Command Output:
           The following jobs matched your query:
              5
              6
              7
        
        Command Error/Debug:
        
    """

    args      = """-v"""
    exp_rs    = 0

    results = testutils.run_cmd('qselect.py',args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\n\nFailed Data:\n\n" \
        "Return Status %s, Expected Return Status %s\n\n" \
        "Command Output:\n%s\n\n" \
        "Command Error:\n%s\n\n" \
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), args)

    assert result, errmsg
