import testutils

# ---------------------------------------------------------------------------------
def test_qdel_invalid_option():
    """
    qdel test run: invalid_option

        Command Output:
          Usage: qdel.py [options] <jobid1> [ ... <jobidN>]
          
          qdel.py: error: no such option: -k
          

    """

    args      = """-k 1"""
    exp_rs    = 512

    results = testutils.run_cmd('qdel.py',args,None) 
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
def test_qdel_debug_option():
    """
    qdel test run: debug_option

        Command Output:
          
          qdel.py -d 1
          
          component: "queue-manager.del_jobs", defer: True
            del_jobs(
               [{'tag': 'job', 'user': 'georgerojas', 'jobid': 1}],
               False,
               georgerojas,
               )
          
          
          

    """

    args      = """-d 1"""
    exp_rs    = 0

    results = testutils.run_cmd('qdel.py',args,None) 
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
def test_qdel_jobid_1():
    """
    qdel test run: jobid_1

        Command Output:
          jobid must be an integer: myq
          

    """

    args      = """myq 1 2 3 4"""
    exp_rs    = 256

    results = testutils.run_cmd('qdel.py',args,None) 
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
def test_qdel_jobid_2():
    """
    qdel test run: jobid_2

        Command Output:
          

    """

    args      = """1 2 3 4"""
    exp_rs    = 0

    results = testutils.run_cmd('qdel.py',args,None) 
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
def test_qdel_jobid_3():
    """
    qdel test run: jobid_3

        Command Output:
          

    """

    args      = """1"""
    exp_rs    = 0

    results = testutils.run_cmd('qdel.py',args,None) 
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
