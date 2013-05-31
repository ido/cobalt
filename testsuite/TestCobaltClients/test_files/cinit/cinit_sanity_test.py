import testutils

# ---------------------------------------------------------------------------------
def test_partadm_delete_partions():
    """
    partadm test run: delete_partions

        Command Output:
          []
          

    """

    args      = """-d '*'"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R00_R01_2048():
    """
    partadm test run: add_partition_ANL_R00_R01_2048

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R00-R01-2048', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 2048}]
          

    """

    args      = """-a ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R00_R01_2048():
    """
    partadm test run: enable_partition_ANL_R00_R01_2048

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
          

    """

    args      = """--enable ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R00_R01_2048():
    """
    partadm test run: activate_partition_ANL_R00_R01_2048

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
          

    """

    args      = """--activate ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R00_1024():
    """
    partadm test run: add_partition_ANL_R00_1024

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R00-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
          

    """

    args      = """-a ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R00_1024():
    """
    partadm test run: enable_partition_ANL_R00_1024

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-1024'}]
          

    """

    args      = """--enable ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R00_1024():
    """
    partadm test run: activate_partition_ANL_R00_1024

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-1024'}]
          

    """

    args      = """--activate ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R01_1024():
    """
    partadm test run: add_partition_ANL_R01_1024

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R01-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
          

    """

    args      = """-a ANL-R01-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R01_1024():
    """
    partadm test run: enable_partition_ANL_R01_1024

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R01-1024'}]
          

    """

    args      = """--enable ANL-R01-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R01_1024():
    """
    partadm test run: activate_partition_ANL_R01_1024

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R01-1024'}]
          

    """

    args      = """--activate ANL-R01-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R00_M0_512():
    """
    partadm test run: add_partition_ANL_R00_M0_512

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R00-M0-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
          

    """

    args      = """-a ANL-R00-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R00_M0_512():
    """
    partadm test run: enable_partition_ANL_R00_M0_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
          

    """

    args      = """--enable ANL-R00-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R00_M0_512():
    """
    partadm test run: activate_partition_ANL_R00_M0_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
          

    """

    args      = """--activate ANL-R00-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R00_M1_512():
    """
    partadm test run: add_partition_ANL_R00_M1_512

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R00-M1-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
          

    """

    args      = """-a ANL-R00-M1-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R00_M1_512():
    """
    partadm test run: enable_partition_ANL_R00_M1_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}]
          

    """

    args      = """--enable ANL-R00-M1-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R00_M1_512():
    """
    partadm test run: activate_partition_ANL_R00_M1_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}]
          

    """

    args      = """--activate ANL-R00-M1-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_partition_ANL_R01_M0_512():
    """
    partadm test run: add_partition_ANL_R01_M0_512

        Command Output:
          [{'scheduled': False, 'name': 'ANL-R01-M0-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
          

    """

    args      = """-a ANL-R01-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_enable_partition_ANL_R01_M0_512():
    """
    partadm test run: enable_partition_ANL_R01_M0_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R01-M0-512'}]
          

    """

    args      = """--enable ANL-R01-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_activate_partition_ANL_R01_M0_512():
    """
    partadm test run: activate_partition_ANL_R01_M0_512

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R01-M0-512'}]
          

    """

    args      = """--activate ANL-R01-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_1():
    """
    partadm test run: list_1

        Command Output:
          No reservations data available
          Name              Queue    Size  Functional  Scheduled  State  Dependencies
          =============================================================================
          ANL-R00-R01-2048  default  2048      X           X      idle               
          ANL-R00-1024      default  1024      X           X      idle               
          ANL-R01-1024      default  1024      X           X      idle               
          ANL-R00-M0-512    default  512       X           X      idle               
          ANL-R00-M1-512    default  512       X           X      idle               
          ANL-R01-M0-512    default  512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_cqadm_delete_default_que():
    """
    cqadm test run: delete_default_que

        Command Output:
          Failed to match any jobs or queues
          Deleted Queues  
          ================
          

    """

    args      = """--delq default"""
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
def test_cqadm_add_queues():
    """
    cqadm test run: add_queues

        Command Output:
          Added Queues  
          ==============
          default       
          q_4           
          q_3           
          q_2           
          q_1           
          

    """

    args      = """--addq default q_1 q_2 q_3 q_4"""
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
def test_cqadm_start_default():
    """
    cqadm test run: start_default

        Command Output:
          

    """

    args      = """--start default q_1 q_2 q_3 q_4"""
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
def test_cqadm_get_queues():
    """
    cqadm test run: get_queues

        Command Output:
          Queue    Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  AdminEmail  State    Cron  Policy   Priority  
          ===============================================================================================================================================
          default  None   None     None     None        None       None          None          None        None        running  None  default  0         
          q_1      None   None     None     None        None       None          None          None        None        running  None  default  0         
          q_2      None   None     None     None        None       None          None          None        None        running  None  default  0         
          q_3      None   None     None     None        None       None          None          None        None        running  None  default  0         
          q_4      None   None     None     None        None       None          None          None        None        running  None  default  0         
          

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
def test_qstat_qstat_2():
    """
    qstat test run: qstat_2

        Command Output:
          Name     Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ==========================================================================================================
          default  None   None     None     None        None       None          None          None        running  
          q_1      None   None     None     None        None       None          None          None        running  
          q_2      None   None     None     None        None       None          None          None        running  
          q_3      None   None     None     None        None       None          None          None        running  
          q_4      None   None     None     None        None       None          None          None        running  
          

    """

    args      = """-Q"""
    exp_rs    = 0

    results = testutils.run_cmd('qstat.py',args,None) 
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
def test_partadm_add_que_associations_1():
    """
    partadm test run: add_que_associations_1

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-1024'}, {'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
          

    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_3():
    """
    partadm test run: list_3

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R01-1024      default          1024      X           X      idle               
          ANL-R00-M0-512    default          512       X           X      idle               
          ANL-R00-M1-512    default          512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_que_associations_2():
    """
    partadm test run: add_que_associations_2

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}, {'tag': 'partition', 'name': 'ANL-R01-1024'}]
          

    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R01-1024 ANL-R00-M1-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_4():
    """
    partadm test run: list_4

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default          512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_add_que_associations_3():
    """
    partadm test run: add_que_associations_3

        Command Output:
          [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
          

    """

    args      = """--queue default:q_1 ANL-R00-M0-512"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_5():
    """
    partadm test run: list_5

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default:q_1      512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_rmq_1():
    """
    partadm test run: rmq_1

        Command Output:
          [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}], [{'tag': 'partition', 'name': 'ANL-R00-1024'}]]
          

    """

    args      = """--queue q_3 --rmq ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_6():
    """
    partadm test run: list_6

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_2:q_4      2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_4      1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default:q_1      512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_rmq_2():
    """
    partadm test run: rmq_2

        Command Output:
          [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]]
          

    """

    args      = """--queue q_2 --rmq ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_7():
    """
    partadm test run: list_7

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_4          2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_4      1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default:q_1      512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_appq_1():
    """
    partadm test run: appq_1

        Command Output:
          [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}], [{'tag': 'partition', 'name': 'ANL-R00-1024'}]]
          

    """

    args      = """--queue q_3 --appq ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_8():
    """
    partadm test run: list_8

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_4:q_3      2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_4:q_3  1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default:q_1      512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_appq_2():
    """
    partadm test run: appq_2

        Command Output:
          [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]]
          

    """

    args      = """--queue q_2 --appq ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_partadm_list_9():
    """
    partadm test run: list_9

        Command Output:
          No reservations data available
          Name              Queue            Size  Functional  Scheduled  State  Dependencies
          =====================================================================================
          ANL-R00-R01-2048  q_1:q_4:q_3:q_2  2048      X           X      idle               
          ANL-R00-1024      q_1:q_2:q_4:q_3  1024      X           X      idle               
          ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
          ANL-R00-M0-512    default:q_1      512       X           X      idle               
          ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
          ANL-R01-M0-512    default          512       X           X      idle               
          

    """

    args      = """-l"""
    exp_rs    = 0

    results = testutils.run_cmd('partadm.py',args,None) 
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
def test_qstat_qstat_2():
    """
    qstat test run: qstat_2

        Command Output:
          Name     Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ==========================================================================================================
          default  None   None     None     None        None       None          None          None        running  
          q_1      None   None     None     None        None       None          None          None        running  
          q_2      None   None     None     None        None       None          None          None        running  
          q_3      None   None     None     None        None       None          None          None        running  
          q_4      None   None     None     None        None       None          None          None        running  
          

    """

    args      = """-Q"""
    exp_rs    = 0

    results = testutils.run_cmd('qstat.py',args,None) 
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
def test_setres_setres_1():
    """
    setres test run: setres_1

        Command Output:
          Got starttime Wed May 31 20:00:00 2023 +0000 (UTC)
          [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'george', 'queue': 'q_1', 'start': 1685563200.0, 'duration': 3000, 'cycle': None, 'res_id': 1, 'partitions': 'ANL-R00-R01-2048'}]
          
          

    """

    args      = """-n george -s 2023_5_31-15:0 -d 50  -q q_1 ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_showres_showres_1():
    """
    showres test run: showres_1

        Command Output:
          Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  
          ====================================================================================================================================================================================
          george       q_1    None  Wed May 31 20:00:00 2023 +0000 (UTC)  00:50     Wed May 31 20:50:00 2023 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        
          

    """

    args      = """-x"""
    exp_rs    = 0

    results = testutils.run_cmd('showres.py',args,None) 
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
def test_setres_setres_2():
    """
    setres test run: setres_2

        Command Output:
          
          

    """

    args      = """-n george -m -d 300"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_showres_showres_2():
    """
    showres test run: showres_2

        Command Output:
          Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  
          ====================================================================================================================================================================================
          george       q_1    None  Wed May 31 20:00:00 2023 +0000 (UTC)  05:00     Thu Jun  1 01:00:00 2023 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        
          

    """

    args      = """-x"""
    exp_rs    = 0

    results = testutils.run_cmd('showres.py',args,None) 
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
def test_setres_setres_3():
    """
    setres test run: setres_3

        Command Output:
          Got starttime Wed Dec  1 16:30:00 2010 +0000 (UTC)
          [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'res_passed', 'queue': 'q_1', 'start': 1291221000.0, 'duration': 3000, 'cycle': None, 'res_id': 2, 'partitions': 'ANL-R00-R01-2048'}]
          
          

    """

    args      = """-n res_passed -s 2010_12_1-10:30 -d 50  -q q_1 ANL-R00-R01-2048"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_showres_showres_3():
    """
    showres test run: showres_3

        Command Output:
          Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  
          ====================================================================================================================================================================================
          res_passed   q_1    None  Wed Dec  1 16:30:00 2010 +0000 (UTC)  00:50     Wed Dec  1 17:20:00 2010 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     2      -        
          george       q_1    None  Wed May 31 20:00:00 2023 +0000 (UTC)  05:00     Thu Jun  1 01:00:00 2023 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        
          

    """

    args      = """-x"""
    exp_rs    = 0

    results = testutils.run_cmd('showres.py',args,None) 
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
