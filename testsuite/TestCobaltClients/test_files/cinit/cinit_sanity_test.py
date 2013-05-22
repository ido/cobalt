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
def test_partadm_activate_partition_ANL_R0=1_M0_512():
    """
    partadm test run: activate_partition_ANL_R0=1_M0_512

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
def test_partadm_list():
    """
    partadm test run: list

        Command Output:
          No reservations data available
          Name              Queue    Size  Geometry  Functional  Scheduled  State  Dependencies
          =======================================================================================
          ANL-R00-R01-2048  default  2048                X           X      idle               
          ANL-R00-1024      default  1024                X           X      idle               
          ANL-R01-1024      default  1024                X           X      idle               
          ANL-R00-M0-512    default  512                 X           X      idle               
          ANL-R00-M1-512    default  512                 X           X      idle               
          ANL-R01-M0-512    default  512                 X           X      idle               
          

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
def test_cqadm_add_default_que():
    """
    cqadm test run: add_default_que

        Command Output:
          Added Queues  
          ==============
          default       
          

    """

    args      = """--addq default"""
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

    args      = """--start default"""
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
def test_qstat_show_ques_prop():
    """
    qstat test run: show_ques_prop

        Command Output:
          get_config_option: Option cqstat_header not found in section [cqm]
          Name     Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
          ==========================================================================================================
          default  None   None     None     None        None       None          None          None        running  
          

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
