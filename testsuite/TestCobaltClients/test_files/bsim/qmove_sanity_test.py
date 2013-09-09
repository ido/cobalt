import testutils
import os
import pwd
# ---------------------------------------------------------------------------------
def test_qmove_invalid_option():
    """
    qmove test run: invalid_option

        Command Output:
        
        Command Error/Debug:Usage: qmove.py [options] <queue name> <jobid1> [... <jobidN>]
        
        qmove.py: error: no such option: -k
        
        
    """

    args      = """-k"""
    exp_rs    = 512

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qmove.py',_args,None) 
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
def test_qmove_queue_1():
    """
    qmove test run: queue_1

        Command Output:
        
        Command Error/Debug:Failed to match any jobs or queues
        
        
    """

    args      = """myq 1 2 3"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qmove.py',_args,None) 
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
def test_qmove_queue_2():
    """
    qmove test run: queue_2

        Command Output:
        
        Command Error/Debug:
        qmove.py -d myq 1 2 3
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'georgerojas', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 1}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'georgerojas', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 2}, {'project': '*', 'queue': '*', 'tag': 'job', 'notify': '*', 'user': 'georgerojas', 'nodes': '*', 'walltime': '*', 'procs': '*', 'jobid': 3}],
             )
        
        
        Failed to match any jobs or queues
        
        
    """

    args      = """-d myq 1 2 3"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qmove.py',_args,None) 
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
def test_qmove_queue_3():
    """
    qmove test run: queue_3

        Command Output:
        
        Command Error/Debug:Failed to match any jobs or queues
        
        
    """

    args      = """1 2 3 4"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qmove.py',_args,None) 
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
def test_qmove_queu_4():
    """
    qmove test run: queu_4

        Command Output:
        
        Command Error/Debug:jobid must be an integer: q2
        
        
    """

    args      = """q1 q2 1 2 3"""
    exp_rs    = 256

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qmove.py',_args,None) 
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
