import testutils

# ---------------------------------------------------------------------------------
def test_cqadm_getq_option_1():
    """
    cqadm test run: getq_option_1

        Command Output:
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """--getq"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_getq_option_2():
    """
    cqadm test run: getq_option_2

        Command Output:
          
          cqadm.py -d --getq
          
          component: "queue-manager.get_queues", defer: True
            get_queues(
               [{'maxuserjobs': '*', 'priority': '*', 'name': '*', 'mintime': '*', 'totalnodes': '*', 'cron': '*', 'state': '*', 'tag': 'queue', 'maxqueued': '*', 'maxrunning': '*', 'maxusernodes': '*', 'maxnodehours': '*', 'policy': '*', 'maxtime': '*', 'adminemail': '*', 'users': '*'}],
               )
          
          
          [{'users': 'james', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'kebra', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'land', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'jello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'house', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bello', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'dog', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'aaa', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'cat', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'bbb', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'henry', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'hhh', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'king', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'dito', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'queen', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'myq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'girl', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'yours', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}, {'users': 'boy', 'mintime': None, 'totalnodes': 100, 'cron': 'whocares', 'maxqueued': 20, 'maxusernodes': 20, 'maxnodehours': 20, 'maxtime': None, 'adminemail': 'myemail@gmail.com', 'name': 'zq', 'priority': 'urgent', 'state': 'running', 'maxrunning': 20, 'policy': 'mypolicy'}]
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """-d --getq"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_getq_option_3():
    """
    cqadm test run: getq_option_3

        Command Output:
          Queue  Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail         State    Cron      Policy    Priority  
          =========================================================================================================================================================
          aaa    dog    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bbb    cat    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          bello  house  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          dito   king   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          hhh    henry  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          jello  land   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          kebra  james  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          myq    queen  None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          yours  girl   None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          zq     boy    None     None     20          20         20            20            100         myemail@gmail.com  running  whocares  mypolicy  urgent    
          

    """

    args      = """-f --getq"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_preempt_job_1():
    """
    cqadm test run: preempt_job_1

        Command Output:
          
          cqadm.py -d --preempt 1 2 3
          
          component: "queue-manager.preempt_jobs", defer: True
            preempt_jobs(
               [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
               gooduser,
               False,
               )
          
          
          True
          

    """

    args      = """-d --preempt 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_preempt_job_2():
    """
    cqadm test run: preempt_job_2

        Command Output:
          

    """

    args      = """-f --preempt 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_kill_job_1():
    """
    cqadm test run: kill_job_1

        Command Output:
          
          cqadm.py -d -f --kill 1 2 3
          
          component: "queue-manager.del_jobs", defer: False
            del_jobs(
               [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
               True,
               gooduser,
               )
          
          
          [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
          

    """

    args      = """-d -f --kill 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_kill_job_2():
    """
    cqadm test run: kill_job_2

        Command Output:
          

    """

    args      = """--kill 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_kill_job_3():
    """
    cqadm test run: kill_job_3

        Command Output:
          

    """

    args      = """-f --kill 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_kill_job_4():
    """
    cqadm test run: kill_job_4

        Command Output:
          
          cqadm.py -d --kill 1 2 3
          
          component: "queue-manager.del_jobs", defer: False
            del_jobs(
               [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
               False,
               gooduser,
               )
          
          
          [{'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}]
          

    """

    args      = """-d --kill 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_addq_option_1():
    """
    cqadm test run: addq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--addq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_addq_option_2():
    """
    cqadm test run: addq_option_2

        Command Output:
          Added Queues  
          ==============
          myq1          
          myq2          
          myq3          
          

    """

    args      = """--addq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_delq_option_1():
    """
    cqadm test run: delq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--delq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_delq_option_2():
    """
    cqadm test run: delq_option_2

        Command Output:
          Deleted Queues  
          ================
          myq1            
          myq2            
          myq3            
          

    """

    args      = """--delq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_stopq_option_1():
    """
    cqadm test run: stopq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--stopq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_stopq_option_2():
    """
    cqadm test run: stopq_option_2

        Command Output:
          

    """

    args      = """--stopq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_startq_option_1():
    """
    cqadm test run: startq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--startq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_startq_option_2():
    """
    cqadm test run: startq_option_2

        Command Output:
          

    """

    args      = """--startq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_drainq_option_1():
    """
    cqadm test run: drainq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--drainq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_drainq_option_2():
    """
    cqadm test run: drainq_option_2

        Command Output:
          

    """

    args      = """--drainq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_killq_option_1():
    """
    cqadm test run: killq_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--killq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_killq_option_2():
    """
    cqadm test run: killq_option_2

        Command Output:
          

    """

    args      = """--killq myq1 myq2 myq3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_policy_option_1():
    """
    cqadm test run: policy_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --policy option requires an argument
          

    """

    args      = """--policy"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_policy_option_2():
    """
    cqadm test run: policy_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--policy 'mypolicy'"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_policy_option_3():
    """
    cqadm test run: policy_option_3

        Command Output:
          

    """

    args      = """--policy 'mypolicy' myq1 myq2"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setq_option_1():
    """
    cqadm test run: setq_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --setq option requires an argument
          

    """

    args      = """--setq"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setq_option_2():
    """
    cqadm test run: setq_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--setq 'a=b b=c a=c'"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setq_option_3():
    """
    cqadm test run: setq_option_3

        Command Output:
          

    """

    args      = """--setq 'a=b b=c a=c' myq1 myq2"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_unsetq_option_1():
    """
    cqadm test run: unsetq_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --unsetq option requires an argument
          

    """

    args      = """--unsetq"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_unsetq_option_2():
    """
    cqadm test run: unsetq_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--unsetq 'a b a'"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_unsetq_option_3():
    """
    cqadm test run: unsetq_option_3

        Command Output:
          

    """

    args      = """--unsetq 'a b a' myq1 myq2"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setjobid_option_1():
    """
    cqadm test run: setjobid_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: -j option requires an argument
          

    """

    args      = """-j"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setjobid_option_2():
    """
    cqadm test run: setjobid_option_2

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --setjobid option requires an argument
          

    """

    args      = """--setjobid"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setjobid_option_3():
    """
    cqadm test run: setjobid_option_3

        Command Output:
          

    """

    args      = """-j 1"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setjobid_option_4():
    """
    cqadm test run: setjobid_option_4

        Command Output:
          

    """

    args      = """--setjobid 1"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_setjobid_option_5():
    """
    cqadm test run: setjobid_option_5

        Command Output:
          

    """

    args      = """-j 1 --setjobid 2"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_run_option_1():
    """
    cqadm test run: run_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --run option requires an argument
          

    """

    args      = """--run"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_run_option_2():
    """
    cqadm test run: run_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--run mayaguez"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_hold_option_1():
    """
    cqadm test run: hold_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--hold"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_hold_option_2():
    """
    cqadm test run: hold_option_2

        Command Output:
          

    """

    args      = """--hold 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_hold_option_3():
    """
    cqadm test run: hold_option_3

        Command Output:
          
          cqadm.py -d --hold 1 2 3
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': False, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
               {'admin_hold': True},
               gooduser,
               )
          
          
          [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
          

    """

    args      = """-d --hold  1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_hold_option_4():
    """
    cqadm test run: hold_option_4

        Command Output:
          

    """

    args      = """-f --hold  1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_release_option_1():
    """
    cqadm test run: release_option_1

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--release"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_release_option_2():
    """
    cqadm test run: release_option_2

        Command Output:
          

    """

    args      = """--release 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_release_option_3():
    """
    cqadm test run: release_option_3

        Command Output:
          
          cqadm.py -d --release 1 2 3
          
          component: "queue-manager.set_jobs", defer: False
            set_jobs(
               [{'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 1}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 2}, {'admin_hold': True, 'tag': 'job', 'location': '*', 'walltime': '*', 'jobid': 3}],
               {'admin_hold': False},
               gooduser,
               )
          
          
          [{'queue': 'kebra', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 1, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 512, 'walltime': 5, 'user_hold': False, 'procs': 512, 'user': 'james'}, {'queue': 'jello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 2, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1024, 'walltime': 10, 'user_hold': False, 'procs': 1024, 'user': 'land'}, {'queue': 'bello', 'has_completed': False, 'errorpath': '/tmp', 'mode': 'smp', 'outputpath': '/tmp', 'is_active': False, 'jobid': 3, 'project': 'my_project', 'tag': 'job', 'notify': 'myemag@gmail.com', 'nodes': 1536, 'walltime': 15, 'user_hold': False, 'procs': 1536, 'user': 'house'}]
          

    """

    args      = """-d --release 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_release_option_4():
    """
    cqadm test run: release_option_4

        Command Output:
          

    """

    args      = """-f --release 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_release_and_hold():
    """
    cqadm test run: release_and_hold

        Command Output:
          Attribute admin_hold already set
          

    """

    args      = """--hold --release 1 2 3"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_queue_option_1():
    """
    cqadm test run: queue_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --queue option requires an argument
          

    """

    args      = """--queue"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_queue_option_2():
    """
    cqadm test run: queue_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--queue myq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_time_option_1():
    """
    cqadm test run: time_option_1

        Command Output:
          Usage: cqadm.py [options] <jobid> <jobid> OR <queue> <queue>
          
          cqadm.py: error: --time option requires an argument
          

    """

    args      = """--time"""
    exp_rs    = 512

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_time_option_2():
    """
    cqadm test run: time_option_2

        Command Output:
          At least on jobid or queue name must be supplied
          

    """

    args      = """--time 50"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_time_option_4():
    """
    cqadm test run: time_option_4

        Command Output:
          

    """

    args      = """--time 50 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_getq_and_addq():
    """
    cqadm test run: combine_getq_and_addq

        Command Output:
          Option combinations not allowed with: addq, getq option(s)
          

    """

    args      = """--getq --addq myq1 myq2 myq3"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_getq_and_setjobid():
    """
    cqadm test run: combine_getq_and_setjobid

        Command Output:
          Option combinations not allowed with: setjobid, getq option(s)
          

    """

    args      = """--getq -j 1 123"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_time_and_getq():
    """
    cqadm test run: combine_time_and_getq

        Command Output:
          Option combinations not allowed with: getq option(s)
          

    """

    args      = """--time 50 --getq"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_release_and_getq():
    """
    cqadm test run: combine_release_and_getq

        Command Output:
          Option combinations not allowed with: getq option(s)
          

    """

    args      = """--release --getq 123"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_setq_with_queue():
    """
    cqadm test run: combine_setq_with_queue

        Command Output:
          Option combinations not allowed with: setq option(s)
          

    """

    args      = """--setq 'a=1 b=2' --queue q 1"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_addq_and_delq():
    """
    cqadm test run: combine_addq_and_delq

        Command Output:
          Option combinations not allowed with: addq, delq option(s)
          

    """

    args      = """--addq --delq q1 q2"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_addq_and_stopq():
    """
    cqadm test run: combine_addq_and_stopq

        Command Output:
          Option combinations not allowed with: addq, stopq option(s)
          

    """

    args      = """--stopq --addq q1 q2"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
def test_cqadm_combine_addq_and_startq():
    """
    cqadm test run: combine_addq_and_startq

        Command Output:
          Option combinations not allowed with: addq, startq option(s)
          

    """

    args      = """--startq --addq q1 q2"""
    exp_rs    = 256

    results = testutils.run_cmd('cqadm.py',args,None) 
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
