import testutils
import os
import pwd
# ---------------------------------------------------------------------------------
def test_qrls_invalid_option():
    """
    qrls test run: invalid_option

        Command Output:
        
        Command Error/Debug:Usage: qrls.py [options] <jobid1> [ ... <jobidN> ]
        
        qrls.py: error: no such option: -k
        
        
    """

    args      = """-k 1"""
    exp_rs    = 512

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qrls_debug_flag():
    """
    qrls test run: debug_flag

        Command Output:
           Failed to remove user hold on jobs: 
              job 1 not found
        
        Command Error/Debug:
        qrls.py -d 1
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'user_hold': '*', 'tag': 'job', 'user': 'georgerojas', 'jobid': 1}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [],
             {'user_hold': False},
             georgerojas,
             )
        
        
           No jobs found.
        Failed to match any jobs
        
        
    """

    args      = """-d 1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qrls_jobid_1():
    """
    qrls test run: jobid_1

        Command Output:
        
        Command Error/Debug:jobid must be an integer: myq
        
        
    """

    args      = """myq 1 2 3 4"""
    exp_rs    = 256

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qrls_jobid_2():
    """
    qrls test run: jobid_2

        Command Output:
           Failed to remove user hold on jobs: 
              job 1 not found
              job 2 not found
              job 3 not found
              job 4 not found
        
        Command Error/Debug:   No jobs found.
        Failed to match any jobs
        
        
    """

    args      = """1 2 3 4"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qrls_jobid_3():
    """
    qrls test run: jobid_3

        Command Output:
           Failed to remove user hold on jobs: 
              job 1 not found
        
        Command Error/Debug:   No jobs found.
        Failed to match any jobs
        
        
    """

    args      = """1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg

# ---------------------------------------------------------------------------------
def test_qrls_dependancy_option():
    """
    qrls test run: dependancy_option

        Command Output:
           Removed dependencies from jobs: 
        
        Command Error/Debug:
        qrls.py -d --dependencies 1 2
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'user_hold': '*', 'tag': 'job', 'user': 'georgerojas', 'jobid': 1}, {'user_hold': '*', 'tag': 'job', 'user': 'georgerojas', 'jobid': 2}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [],
             {'all_dependencies': []},
             georgerojas,
             )
        
        
        
        
    """

    args      = """-d --dependencies 1 2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qrls.py',_args,None) 
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
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg
