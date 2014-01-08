import testutils
import os
import pwd
# ---------------------------------------------------------------------------------
def test_partadm_delete_partions():
    """
    partadm test run: delete_partions

        Command Output:
        []
        
        Command Error/Debug:
        
    """

    args      = """-d '*'"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R00_R01_2048():
    """
    partadm test run: add_partition_ANL_R00_R01_2048

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R00-R01-2048', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 2048}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R00_R01_2048():
    """
    partadm test run: enable_partition_ANL_R00_R01_2048

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R00_R01_2048():
    """
    partadm test run: activate_partition_ANL_R00_R01_2048

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R00_1024():
    """
    partadm test run: add_partition_ANL_R00_1024

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R00-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R00_1024():
    """
    partadm test run: enable_partition_ANL_R00_1024

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R00_1024():
    """
    partadm test run: activate_partition_ANL_R00_1024

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R01_1024():
    """
    partadm test run: add_partition_ANL_R01_1024

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R01-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R01-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R01_1024():
    """
    partadm test run: enable_partition_ANL_R01_1024

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R01-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R01-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R01_1024():
    """
    partadm test run: activate_partition_ANL_R01_1024

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R01-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R01-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R00_M0_512():
    """
    partadm test run: add_partition_ANL_R00_M0_512

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R00-M0-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R00_M0_512():
    """
    partadm test run: enable_partition_ANL_R00_M0_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R00_M0_512():
    """
    partadm test run: activate_partition_ANL_R00_M0_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R00_M1_512():
    """
    partadm test run: add_partition_ANL_R00_M1_512

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R00-M1-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R00-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R00_M1_512():
    """
    partadm test run: enable_partition_ANL_R00_M1_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R00-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R00_M1_512():
    """
    partadm test run: activate_partition_ANL_R00_M1_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R00-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_partition_ANL_R01_M0_512():
    """
    partadm test run: add_partition_ANL_R01_M0_512

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R01-M0-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R01-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_enable_partition_ANL_R01_M0_512():
    """
    partadm test run: enable_partition_ANL_R01_M0_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R01-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R01-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_activate_partition_ANL_R01_M0_512():
    """
    partadm test run: activate_partition_ANL_R01_M0_512

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R01-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R01-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_1():
    """
    partadm test run: list_1

        Command Output:
        Name              Queue    Size  Functional  Scheduled  State  Dependencies
        =============================================================================
        ANL-R00-R01-2048  default  2048      X           X      idle               
        ANL-R00-1024      default  1024      X           X      idle               
        ANL-R01-1024      default  1024      X           X      idle               
        ANL-R00-M0-512    default  512       X           X      idle               
        ANL-R00-M1-512    default  512       X           X      idle               
        ANL-R01-M0-512    default  512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_cqadm_delete_default_que():
    """
    cqadm test run: delete_default_que

        Command Output:
        Deleted Queues  
        ================
        
        Command Error/Debug:Failed to match any jobs or queues
        
        
    """

    args      = """--delq default"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
        
        Command Error/Debug:
        
    """

    args      = """--addq default q_1 q_2 q_3 q_4"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_cqadm_start_default():
    """
    cqadm test run: start_default

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--start default q_1 q_2 q_3 q_4"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
        
        Command Error/Debug:
        
    """

    args      = """--getq"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_1():
    """
    qstat test run: qstat_1

        Command Output:
        Name     Users  MinTime  MaxTime  MaxRunning  MaxQueued  MaxUserNodes  MaxNodeHours  TotalNodes  State    
        ==========================================================================================================
        default  None   None     None     None        None       None          None          None        running  
        q_1      None   None     None     None        None       None          None          None        running  
        q_2      None   None     None     None        None       None          None          None        running  
        q_3      None   None     None     None        None       None          None          None        running  
        q_4      None   None     None     None        None       None          None          None        running  
        
        Command Error/Debug:
        
    """

    args      = """-Q"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_partadm_add_que_associations_1():
    """
    partadm test run: add_que_associations_1

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-1024'}, {'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_3():
    """
    partadm test run: list_3

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R01-1024      default          1024      X           X      idle               
        ANL-R00-M0-512    default          512       X           X      idle               
        ANL-R00-M1-512    default          512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_que_associations_2():
    """
    partadm test run: add_que_associations_2

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M1-512'}, {'tag': 'partition', 'name': 'ANL-R01-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_1:q_2:q_3:q_4 ANL-R01-1024 ANL-R00-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_4():
    """
    partadm test run: list_4

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default          512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_add_que_associations_3():
    """
    partadm test run: add_que_associations_3

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R00-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--queue default:q_1 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_5():
    """
    partadm test run: list_5

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_2:q_3:q_4  2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default:q_1      512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_rmq_1():
    """
    partadm test run: rmq_1

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}], [{'tag': 'partition', 'name': 'ANL-R00-1024'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_3 --rmq ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_6():
    """
    partadm test run: list_6

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_2:q_4      2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_4      1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default:q_1      512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_rmq_2():
    """
    partadm test run: rmq_2

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_2 --rmq ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_7():
    """
    partadm test run: list_7

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_4          2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_4      1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default:q_1      512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_appq_1():
    """
    partadm test run: appq_1

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}], [{'tag': 'partition', 'name': 'ANL-R00-1024'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_3 --appq ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_8():
    """
    partadm test run: list_8

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_4:q_3      2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_4:q_3  1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default:q_1      512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_appq_2():
    """
    partadm test run: appq_2

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R00-R01-2048'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q_2 --appq ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_list_9():
    """
    partadm test run: list_9

        Command Output:
        Name              Queue            Size  Functional  Scheduled  State  Dependencies
        =====================================================================================
        ANL-R00-R01-2048  q_1:q_4:q_3:q_2  2048      X           X      idle               
        ANL-R00-1024      q_1:q_2:q_4:q_3  1024      X           X      idle               
        ANL-R01-1024      q_1:q_2:q_3:q_4  1024      X           X      idle               
        ANL-R00-M0-512    default:q_1      512       X           X      idle               
        ANL-R00-M1-512    q_1:q_2:q_3:q_4  512       X           X      idle               
        ANL-R01-M0-512    default          512       X           X      idle               
        
        Command Error/Debug:
        
    """

    args      = """-l"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
        
        Command Error/Debug:
        
    """

    args      = """-Q"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_setres_setres_1():
    """
    setres test run: setres_1

        Command Output:
        Got starttime Thu Jun 30 15:30:00 2022 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'george', 'queue': 'q_1', 'start': 1656603000.0, 'duration': 3000, 'cycle': None, 'res_id': 1, 'partitions': 'ANL-R00-R01-2048'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n george -s 2022_06_30-10:30 -d 50  -q q_1 ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_1():
    """
    showres test run: showres_1

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  Time Remaining  
        ====================================================================================================================================================================================================
        george       q_1    None  Thu Jun 30 15:30:00 2022 +0000 (UTC)  00:50     Thu Jun 30 16:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_2():
    """
    setres test run: setres_2

        Command Output:
        [{'name': 'george', 'block_passthrough': False, 'project': None, 'start': 1656603000.0, 'cycle': None, 'duration': 18000, 'partitions': 'ANL-R00-R01-2048', 'res_id': 1, 'users': None}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n george -m -d 300"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_2():
    """
    showres test run: showres_2

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  Time Remaining  
        ====================================================================================================================================================================================================
        george       q_1    None  Thu Jun 30 15:30:00 2022 +0000 (UTC)  05:00     Thu Jun 30 20:30:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_3():
    """
    setres test run: setres_3

        Command Output:
        Got starttime Thu Dec 01 16:30:00 2022 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'david', 'queue': 'q_1', 'start': 1669912200.0, 'duration': 3000, 'cycle': None, 'res_id': 2, 'partitions': 'ANL-R00-R01-2048'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n david -s 2022_12_1-10:30 -d 50  -q q_1 ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_3():
    """
    showres test run: showres_3

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  Time Remaining  
        ====================================================================================================================================================================================================
        george       q_1    None  Thu Jun 30 15:30:00 2022 +0000 (UTC)  05:00     Thu Jun 30 20:30:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     1      -        Not Started     
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     2      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_qsub_qsub_1():
    """
    qsub test run: qsub_1

        Command Output:
        1
        
        Command Error/Debug:
        
    """

    args      = """-h -t 50  -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_2():
    """
    qsub test run: qsub_2

        Command Output:
        2
        
        Command Error/Debug:
        
    """

    args      = """-h -t 100 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_3():
    """
    qsub test run: qsub_3

        Command Output:
        3
        
        Command Error/Debug:
        
    """

    args      = """-h -t 150 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_4():
    """
    qsub test run: qsub_4

        Command Output:
        4
        
        Command Error/Debug:
        
    """

    args      = """--dep 1:2:3 -t 150 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_5():
    """
    qsub test run: qsub_5

        Command Output:
        5
        
        Command Error/Debug:WARNING: dependencies 60 do not match jobs currently in the queue
        
        
    """

    args      = """--dep 1:2:3:4:60 -t 150 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_3():
    """
    qstat test run: qstat_3

        Command Output:
        JobID  User   WallTime  Nodes  State      Location  
        ====================================================
        1      rojas  00:50:00  30     user_hold  None      
        2      rojas  01:40:00  30     user_hold  None      
        3      rojas  02:30:00  30     user_hold  None      
        4      rojas  02:30:00  30     dep_hold   None      
        5      rojas  02:30:00  30     dep_hold   None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qalter_qalter_1():
    """
    qalter test run: qalter_1

        Command Output:
        walltime changed from 50 to 60.0
        walltime changed from 100 to 110.0
        walltime changed from 150 to 160.0
        walltime changed from 150 to 160.0
        walltime changed from 150 to 160.0
        
        Command Error/Debug:
        qalter.py --debug -t +10 1 2 3 4 5
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 1, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 2, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 3, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 4, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 5, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 1, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 50, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 1, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '60.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 2, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 100, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 2, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '110.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 3, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 150, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 3, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '160.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 4, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 150, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 4, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '160.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 150, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 5, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '160.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 160, 'procs': 30, 'notify': None}]
        
        
    """

    args      = """--debug  -t +10 1 2 3 4 5"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qalter.py',_args,None) 
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
def test_qstat_qstat_4():
    """
    qstat test run: qstat_4

        Command Output:
        JobID  User   WallTime  Nodes  State      Location  
        ====================================================
        1      rojas  01:00:00  30     user_hold  None      
        2      rojas  01:50:00  30     user_hold  None      
        3      rojas  02:40:00  30     user_hold  None      
        4      rojas  02:40:00  30     dep_hold   None      
        5      rojas  02:40:00  30     dep_fail   None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qalter_qalter_2():
    """
    qalter test run: qalter_2

        Command Output:
        walltime changed from 60 to 55.0
        walltime changed from 110 to 105.0
        walltime changed from 160 to 155.0
        walltime changed from 160 to 155.0
        walltime changed from 160 to 155.0
        
        Command Error/Debug:
        qalter.py --debug -t -5 1 2 3 4 5
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 1, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 2, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 3, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 4, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 5, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 1, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 60, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 1, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '55.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 2, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 110, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 2, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '105.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 3, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 160, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 3, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '155.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 4, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 160, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 4, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '155.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 160, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 5, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '155.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 155, 'procs': 30, 'notify': None}]
        
        
    """

    args      = """--debug  -t -5 1 2 3 4 5"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qalter.py',_args,None) 
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
def test_qstat_qstat_5():
    """
    qstat test run: qstat_5

        Command Output:
        JobID  User   WallTime  Nodes  State      Location  
        ====================================================
        1      rojas  00:55:00  30     user_hold  None      
        2      rojas  01:45:00  30     user_hold  None      
        3      rojas  02:35:00  30     user_hold  None      
        4      rojas  02:35:00  30     dep_hold   None      
        5      rojas  02:35:00  30     dep_fail   None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qalter_qalter_3():
    """
    qalter test run: qalter_3

        Command Output:
        walltime changed from 55 to 65.0
        walltime changed from 105 to 115.0
        walltime changed from 155 to 165.0
        walltime changed from 155 to 165.0
        walltime changed from 155 to 165.0
        
        Command Error/Debug:
        qalter.py --debug -t +10 1 2 3 4 5
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 1, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 2, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 3, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 4, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 5, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 1, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 55, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 1, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '65.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 2, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 105, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 2, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '115.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 3, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 155, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 3, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '165.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 4, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 155, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 4, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '165.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 155, 'procs': 30, 'notify': None}],
             {'queue': 'default', 'mode': 'smp', 'jobid': 5, 'project': None, 'tag': 'job', 'notify': None, 'nodes': 30, 'walltime': '165.0', 'procs': 30, 'user': 'rojas'},
             rojas,
             )
        
        
        [{'project': None, 'user': 'rojas', 'jobid': 5, 'queue': 'default', 'tag': 'job', 'mode': 'smp', 'nodes': 30, 'walltime': 165, 'procs': 30, 'notify': None}]
        
        
    """

    args      = """--debug  -t +10 1 2 3 4 5"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qalter.py',_args,None) 
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
def test_qstat_qstat_6():
    """
    qstat test run: qstat_6

        Command Output:
        JobID  User   WallTime  Nodes  State      Location  
        ====================================================
        1      rojas  01:05:00  30     user_hold  None      
        2      rojas  01:55:00  30     user_hold  None      
        3      rojas  02:45:00  30     user_hold  None      
        4      rojas  02:45:00  30     dep_hold   None      
        5      rojas  02:45:00  30     dep_fail   None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qrls_qrls_1():
    """
    qrls test run: qrls_1

        Command Output:
           Failed to remove user hold on jobs: 
              job 4 does not have a 'user hold'
              job 5 does not have a 'user hold'
           Removed user hold on jobs: 
              1
              2
              3
        
        Command Error/Debug:
        qrls.py -d 1 2 3 4 5
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 1}, {'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 2}, {'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 3}, {'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 4}, {'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 5}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 1}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 2}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 3}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 4}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 5}],
             {'user_hold': False},
             rojas,
             )
        
        
        Response: [{'user_hold': False, 'tag': 'job', 'is_active': False, 'user': 'rojas', 'jobid': 1}, {'user_hold': False, 'tag': 'job', 'is_active': False, 'user': 'rojas', 'jobid': 2}, {'user_hold': False, 'tag': 'job', 'is_active': False, 'user': 'rojas', 'jobid': 3}, {'user_hold': False, 'tag': 'job', 'is_active': False, 'user': 'rojas', 'jobid': 4}, {'user_hold': False, 'tag': 'job', 'is_active': False, 'user': 'rojas', 'jobid': 5}]
        
        
    """

    args      = """-d 1 2 3 4 5"""
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
def test_qstat_qstat_7():
    """
    qstat test run: qstat_7

        Command Output:
        JobID  User   WallTime  Nodes  State     Location  
        ===================================================
        1      rojas  01:05:00  30     queued    None      
        2      rojas  01:55:00  30     queued    None      
        3      rojas  02:45:00  30     queued    None      
        4      rojas  02:45:00  30     dep_hold  None      
        5      rojas  02:45:00  30     dep_fail  None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qrls_qrls_2():
    """
    qrls test run: qrls_2

        Command Output:
           Removed dependencies from jobs: 
              4
              5
        
        Command Error/Debug:
        qrls.py -d --dep 4 5
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 4}, {'user_hold': '*', 'tag': 'job', 'user': 'rojas', 'jobid': 5}],
             )
        
        
        component: "queue-manager.set_jobs", defer: False
          set_jobs(
             [{'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 4}, {'user_hold': '*', 'tag': 'job', 'is_active': '*', 'user': 'rojas', 'jobid': 5}],
             {'all_dependencies': []},
             rojas,
             )
        
        
        
        
    """

    args      = """-d --dep 4 5"""
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
def test_qstat_qstat_8():
    """
    qstat test run: qstat_8

        Command Output:
        JobID  User   WallTime  Nodes  State   Location  
        =================================================
        1      rojas  01:05:00  30     queued  None      
        2      rojas  01:55:00  30     queued  None      
        3      rojas  02:45:00  30     queued  None      
        4      rojas  02:45:00  30     queued  None      
        5      rojas  02:45:00  30     queued  None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_6():
    """
    qsub test run: qsub_6

        Command Output:
        6
        
        Command Error/Debug:
        qsub.py --debug -t 150 -n 30 /bin/ls
        
        component: "system.validate_job", defer: False
          validate_job(
             {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': False, 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '150', 'jobname': False, 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': False, 'error': False, 'nodecount': '30', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
             )
        
        
        component: "queue-manager.add_jobs", defer: False
          add_jobs(
             [{'kernel': 'default', 'args': [], 'outputdir': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'user_list': ['rojas'], 'umask': 18, 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'tag': 'job', 'command': '/bin/ls', 'mode': 'smp', 'run_project': False, 'path': '/home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin', 'nodes': 30, 'walltime': '150', 'ion_kernel': 'default', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'procs': 30, 'user': 'rojas'}],
             )
        
        
        
        
    """

    args      = """--debug -t 150 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_7():
    """
    qsub test run: qsub_7

        Command Output:
        7
        
        Command Error/Debug:
        qsub.py --debug -t 150 -n 30 /bin/ls
        
        component: "system.validate_job", defer: False
          validate_job(
             {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': False, 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '150', 'jobname': False, 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': False, 'error': False, 'nodecount': '30', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
             )
        
        
        component: "queue-manager.add_jobs", defer: False
          add_jobs(
             [{'kernel': 'default', 'args': [], 'outputdir': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'user_list': ['rojas'], 'umask': 18, 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'tag': 'job', 'command': '/bin/ls', 'mode': 'smp', 'run_project': False, 'path': '/home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin', 'nodes': 30, 'walltime': '150', 'ion_kernel': 'default', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'procs': 30, 'user': 'rojas'}],
             )
        
        
        
        
    """

    args      = """--debug -t 150 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_9():
    """
    qstat test run: qstat_9

        Command Output:
        JobID  User   WallTime  Nodes  State   Location  
        =================================================
        1      rojas  01:05:00  30     queued  None      
        2      rojas  01:55:00  30     queued  None      
        3      rojas  02:45:00  30     queued  None      
        4      rojas  02:45:00  30     queued  None      
        5      rojas  02:45:00  30     queued  None      
        6      rojas  02:30:00  30     queued  None      
        7      rojas  02:30:00  30     queued  None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qalter_qalter_4():
    """
    qalter test run: qalter_4

        Command Output:
        updating scores for jobs: 6, 7
        
        Command Error/Debug:
        qalter.py --debug --defer 6 7
        
        component: "queue-manager.get_jobs", defer: False
          get_jobs(
             [{'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 6, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}, {'is_active': '*', 'tag': 'job', 'notify': '*', 'procs': '*', 'walltime': '*', 'queue': '*', 'jobid': 7, 'project': '*', 'mode': '*', 'nodes': '*', 'user': 'rojas'}],
             )
        
        
        component: "queue-manager.adjust_job_scores", defer: True
          adjust_job_scores(
             [{'jobid': 6}, {'jobid': 7}],
             0,
             rojas,
             )
        
        
        
        
    """

    args      = """--debug  --defer 6 7"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qalter.py',_args,None) 
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
def test_qstat_qstat_10():
    """
    qstat test run: qstat_10

        Command Output:
        JobID  User   WallTime  Nodes  State   Location  
        =================================================
        1      rojas  01:05:00  30     queued  None      
        2      rojas  01:55:00  30     queued  None      
        3      rojas  02:45:00  30     queued  None      
        4      rojas  02:45:00  30     queued  None      
        5      rojas  02:45:00  30     queued  None      
        6      rojas  02:30:00  30     queued  None      
        7      rojas  02:30:00  30     queued  None      
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_setres_setres_4():
    """
    setres test run: setres_4

        Command Output:
        Got starttime Wed Dec 01 16:30:00 2032 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'res1', 'queue': 'q_1', 'start': 1985531400.0, 'duration': 3000, 'cycle': None, 'res_id': 3, 'partitions': 'ANL-R00-R01-2048:ANL-R00-1024'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n res1 -s 2032_12_1-10:30 -d 50  -q q_1 ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_setres_setres_5():
    """
    setres test run: setres_5

        Command Output:
        Got starttime Thu Dec 01 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'res2', 'queue': 'q_1', 'start': 2017067400.0, 'duration': 3000, 'cycle': None, 'res_id': 4, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n res2 -s 2033_12_1-10:30 -d 50  -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_4():
    """
    showres test run: showres_4

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions                     Project  ResID  CycleID  Time Remaining  
        =================================================================================================================================================================================================================
        george       q_1    None  Thu Jun 30 15:30:00 2022 +0000 (UTC)  05:00     Thu Jun 30 20:30:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048               None     1      -        Not Started     
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048               None     2      -        Not Started     
        res1         q_1    None  Wed Dec 01 16:30:00 2032 +0000 (UTC)  00:50     Wed Dec 01 17:20:00 2032 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048:ANL-R00-1024  None     3      -        Not Started     
        res2         q_1    None  Thu Dec 01 16:30:00 2033 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2033 +0000 (UTC)  None        Allowed      ANL-R01-1024:ANL-R00-M0-512    None     4      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_releaseres_releaseres_1():
    """
    releaseres test run: releaseres_1

        Command Output:
        Released reservation 'res2' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        Released reservation 'res1' for partitions: ['ANL-R00-R01-2048', 'ANL-R00-1024']
        Released reservation 'george' for partitions: ['ANL-R00-R01-2048']
        
        Command Error/Debug:
        releaseres.py -d res1 res2 george
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'res1', 'partitions': '*'}, {'name': 'res2', 'partitions': '*'}, {'name': 'george', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'res1', 'partitions': '*'}, {'name': 'res2', 'partitions': '*'}, {'name': 'george', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d res1 res2 george"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_setres_setres_6():
    """
    setres test run: setres_6

        Command Output:
        Got starttime Thu Dec 01 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': 'rojas', 'block_passthrough': False, 'name': 'r1', 'queue': 'q_1', 'start': 2017067400.0, 'duration': 3000, 'cycle': None, 'res_id': 5, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r1 -u <USER> -s 2033_12_1-10:30 -d 50 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_setres_setres_7():
    """
    setres test run: setres_7

        Command Output:
        Got starttime Fri Dec 02 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': 'rojas', 'block_passthrough': False, 'name': 'r2', 'queue': 'q_1', 'start': 2017153800.0, 'duration': 3000, 'cycle': None, 'res_id': 6, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r2 -u <USER> -s 2033_12_2-10:30 -d 50 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_setres_setres_8():
    """
    setres test run: setres_8

        Command Output:
        Got starttime Sat Dec 03 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': 'rojas', 'block_passthrough': False, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512', 'queue': 'q_1', 'start': 2017240200.0, 'duration': 3000, 'cycle': 4320, 'res_id': 7, 'name': 'rc1'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n rc1 -u <USER> -s 2033_12_3-10:30 -d 50 -c 72 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_setres_setres_9():
    """
    setres test run: setres_9

        Command Output:
        Got starttime Sun Dec 04 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': 'rojas', 'block_passthrough': False, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512', 'queue': 'q_1', 'start': 2017326600.0, 'duration': 3000, 'cycle': 4320, 'res_id': 8, 'name': 'rc2'}]
        Warning: reservation 'rc1' overlaps reservation 'rc2'
        Warning: reservation 'rc1' overlaps reservation 'rc2'
        
        
        Command Error/Debug:
        
    """

    args      = """-n rc2 -u <USER> -s 2033_12_4-10:30 -d 50 -c 72 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_5():
    """
    showres test run: showres_5

        Command Output:
        Reservation  Queue  User   Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions                   Project  ResID  CycleID  Time Remaining  
        ================================================================================================================================================================================================================
        david        q_1    None   Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048             None     2      -        Not Started     
        r1           q_1    rojas  Thu Dec 01 16:30:00 2033 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2033 +0000 (UTC)  None        Allowed      ANL-R01-1024:ANL-R00-M0-512  None     5      -        Not Started     
        r2           q_1    rojas  Fri Dec 02 16:30:00 2033 +0000 (UTC)  00:50     Fri Dec 02 17:20:00 2033 +0000 (UTC)  None        Allowed      ANL-R01-1024:ANL-R00-M0-512  None     6      -        Not Started     
        rc1          q_1    rojas  Sat Dec 03 16:30:00 2033 +0000 (UTC)  00:50     Sat Dec 03 17:20:00 2033 +0000 (UTC)  01:12       Allowed      ANL-R01-1024:ANL-R00-M0-512  None     7      1        Not Started     
        rc2          q_1    rojas  Sun Dec 04 16:30:00 2033 +0000 (UTC)  00:50     Sun Dec 04 17:20:00 2033 +0000 (UTC)  01:12       Allowed      ANL-R01-1024:ANL-R00-M0-512  None     8      2        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_userres_userres_1():
    """
    userres test run: userres_1

        Command Output:
        Releasing reservation 'r1'
        Releasing reservation 'r2'
        
        Command Error/Debug:
        
    """

    args      = """r1 r2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('userres.py',_args,None) 
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
def test_userres_userres_2():
    """
    userres test run: userres_2

        Command Output:
        Setting new start time for for reservation 'rc1': Sat Dec  3 11:42:00 2033
        Setting new start time for for reservation 'rc2': Sun Dec  4 11:42:00 2033
        
        Command Error/Debug:
        
    """

    args      = """rc1 rc2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('userres.py',_args,None) 
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
def test_releaseres_releaseres_2():
    """
    releaseres test run: releaseres_2

        Command Output:
        Released reservation 'rc1' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        Released reservation 'rc2' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        
        Command Error/Debug:
        releaseres.py -d rc1 rc2
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'rc1', 'partitions': '*'}, {'name': 'rc2', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'rc1', 'partitions': '*'}, {'name': 'rc2', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d rc1 rc2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_setres_setres_10():
    """
    setres test run: setres_10

        Command Output:
        Got starttime Thu Dec 01 16:30:00 2033 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'r1', 'queue': 'q_1', 'start': 2017067400.0, 'duration': 3000, 'cycle': None, 'res_id': 9, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r1 -s 2033_12_1-10:30 -d 50 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_userres_userres_3():
    """
    userres test run: userres_3

        Command Output:
        
        Command Error/Debug:Reservation subset matched
        You are not a user of reservation 'r1' and so cannot alter it.
        
        
    """

    args      = """r1 r2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('userres.py',_args,None) 
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
def test_showres_showres_6():
    """
    showres test run: showres_6

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions                   Project  ResID  CycleID  Time Remaining  
        ===============================================================================================================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048             None     2      -        Not Started     
        r1           q_1    None  Thu Dec 01 16:30:00 2033 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2033 +0000 (UTC)  None        Allowed      ANL-R01-1024:ANL-R00-M0-512  None     9      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_releaseres_releaseres_3():
    """
    releaseres test run: releaseres_3

        Command Output:
        Released reservation 'r1' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        
        Command Error/Debug:
        releaseres.py -d r1
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d r1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_showres_showres_7():
    """
    showres test run: showres_7

        Command Output:
        Reservation  Queue  User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions        Project  ResID  CycleID  Time Remaining  
        ====================================================================================================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Thu Dec 01 17:20:00 2022 +0000 (UTC)  None        Allowed      ANL-R00-R01-2048  None     2      -        Not Started     
        
        Command Error/Debug:
        
    """

    args      = """-x"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_11():
    """
    setres test run: setres_11

        Command Output:
        Got starttime Wed Jan 08 22:58:00 2014 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'r1', 'queue': 'q_1', 'start': 1389221880.0, 'duration': 3000, 'cycle': None, 'res_id': 10, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r1 -s now -d 50 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_releaseres_releaseres_4():
    """
    releaseres test run: releaseres_4

        Command Output:
        Released reservation 'r1' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        
        Command Error/Debug:
        releaseres.py -d r1
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d r1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_qsub_qsub_8():
    """
    qsub test run: qsub_8

        Command Output:
        8
        
        Command Error/Debug:
        qsub.py --env A=one:B=two:C=x\=1\:y\=2\:z\=3:D=four -t 150 -n 30 -d /bin/ls
        
        component: "system.validate_job", defer: False
          validate_job(
             {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': 'A=one:B=two:C=x\\=1\\:y\\=2\\:z\\=3:D=four', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '150', 'jobname': False, 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': False, 'error': False, 'nodecount': '30', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
             )
        
        
        component: "queue-manager.add_jobs", defer: False
          add_jobs(
             [{'kernel': 'default', 'args': [], 'outputdir': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'envs': {'A': 'one', 'C': 'x=1:y=2:z=3', 'B': 'two', 'D': 'four'}, 'user_list': ['rojas'], 'umask': 18, 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'tag': 'job', 'command': '/bin/ls', 'mode': 'smp', 'run_project': False, 'path': '/home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin', 'nodes': 30, 'walltime': '150', 'ion_kernel': 'default', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'procs': 30, 'user': 'rojas'}],
             )
        
        
        Environment Vars: {'A': 'one', 'C': 'x=1:y=2:z=3', 'B': 'two', 'D': 'four'}
        
        
    """

    args      = """--env "A=one:B=two:C=x\=1\:y\=2\:z\=3:D=four" -t 150 -n 30 -d /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_9():
    """
    qsub test run: qsub_9

        Command Output:
        9
        
        Command Error/Debug:
        
    """

    args      = """-t 50 -n 30 -h /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_10():
    """
    qstat test run: qstat_10

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State      Location        Mode  Procs  Queue    StartTime                             
        ==============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:00    N/A       30     user_hold  None            smp   30     default  N/A                                   
        8      N/A      rojas    0.1    02:30:00  00:00:00    N/A       30     queued     None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:09  30     starting   ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        5      N/A      rojas    0.1    02:45:00  00:00:17    N/A       30     queued     None            smp   30     default  N/A                                   
        7      N/A      rojas    0.1    02:30:00  00:00:12    N/A       30     queued     None            smp   30     default  N/A                                   
        1      N/A      rojas    0.1    01:05:00  00:00:18    N/A       30     queued     None            smp   30     default  N/A                                   
        3      N/A      rojas    0.1    02:45:00  00:00:17    N/A       30     queued     None            smp   30     default  N/A                                   
        6      N/A      rojas    0.1    02:30:00  00:00:12    N/A       30     queued     None            smp   30     default  N/A                                   
        4      N/A      rojas    0.1    02:45:00  00:00:17    N/A       30     queued     None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_1():
    """
    cqadm test run: cqadm_1

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--admin-hold 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_11():
    """
    qstat test run: qstat_11

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State      Location        Mode  Procs  Queue    StartTime                             
        ==============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:00    N/A       30     user_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:10  30     starting   ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:01    N/A       30     queued     None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:17    N/A       30     queued     None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:12    N/A       30     queued     None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:19    N/A       30     queued     None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:18    N/A       30     queued     None            smp   30     default  N/A                                   
        6      N/A      rojas    0.2    02:30:00  00:00:13    N/A       30     queued     None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:18    N/A       30     queued     None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_2():
    """
    cqadm test run: cqadm_2

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--user-release 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_12():
    """
    qstat test run: qstat_12

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State       Location        Mode  Procs  Queue    StartTime                             
        ===============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:01    N/A       30     admin_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:11  30     starting    ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:02    N/A       30     queued      None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:18    N/A       30     queued      None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:13    N/A       30     queued      None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:20    N/A       30     queued      None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:00  30     starting    ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:13    N/A       30     queued      None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:18    N/A       30     queued      None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_3():
    """
    cqadm test run: cqadm_3

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--user-hold 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_13():
    """
    qstat test run: qstat_13

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State      Location        Mode  Procs  Queue    StartTime                             
        ==============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:02    N/A       30     user_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:11  30     starting   ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:02    N/A       30     queued     None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:19    N/A       30     queued     None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:14    N/A       30     queued     None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:20    N/A       30     queued     None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:00  30     starting   ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:14    N/A       30     queued     None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:19    N/A       30     queued     None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_4():
    """
    cqadm test run: cqadm_4

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--admin-release 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_14():
    """
    qstat test run: qstat_14

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State      Location        Mode  Procs  Queue    StartTime                             
        ==============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:02    N/A       30     user_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:12  30     starting   ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:03    N/A       30     queued     None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:19    N/A       30     queued     None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:14    N/A       30     queued     None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:21    N/A       30     queued     None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:01  30     starting   ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:15    N/A       30     queued     None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:20    N/A       30     queued     None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_5():
    """
    cqadm test run: cqadm_5

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--hold 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_15():
    """
    qstat test run: qstat_15

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State      Location        Mode  Procs  Queue    StartTime                             
        ==============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:03    N/A       30     user_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:12  30     starting   ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:03    N/A       30     queued     None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:20    N/A       30     queued     None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:15    N/A       30     queued     None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:21    N/A       30     queued     None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:01  30     starting   ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:15    N/A       30     queued     None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:20    N/A       30     queued     None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_6():
    """
    cqadm test run: cqadm_6

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--user-release 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_16():
    """
    qstat test run: qstat_16

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State       Location        Mode  Procs  Queue    StartTime                             
        ===============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:04    N/A       30     admin_hold  None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:13  30     starting    ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:04    N/A       30     queued      None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:20    N/A       30     queued      None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:15    N/A       30     queued      None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:22    N/A       30     queued      None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:02  30     starting    ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:16    N/A       30     queued      None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:21    N/A       30     queued      None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_cqadm_cqadm_7():
    """
    cqadm test run: cqadm_7

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--release 9"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_qstat_qstat_17():
    """
    qstat test run: qstat_17

        Command Output:
        JobID  JobName  User   Score    WallTime  QueuedTime  RunTime   Nodes  State     Location        Mode  Procs  Queue    StartTime                             
        =============================================================================================================================================================
        9      N/A      rojas    0.1    00:50:00  00:00:04    N/A       30     queued    None            smp   30     default  N/A                                   
        2      N/A      rojas    0.1    01:55:00  00:00:08    00:00:14  30     starting  ANL-R01-M0-512  smp   30     default  Wed Jan 08 22:58:38 2014 +0000 (UTC)  
        8      N/A      rojas    0.1    02:30:00  00:00:05    N/A       30     queued    None            smp   30     default  N/A                                   
        5      N/A      rojas    0.2    02:45:00  00:00:21    N/A       30     queued    None            smp   30     default  N/A                                   
        7      N/A      rojas    0.2    02:30:00  00:00:16    N/A       30     queued    None            smp   30     default  N/A                                   
        1      N/A      rojas    0.2    01:05:00  00:00:23    N/A       30     queued    None            smp   30     default  N/A                                   
        3      N/A      rojas    0.2    02:45:00  00:00:19    00:00:03  30     starting  ANL-R00-M0-512  smp   30     default  Wed Jan 08 22:58:49 2014 +0000 (UTC)  
        6      N/A      rojas    0.2    02:30:00  00:00:16    N/A       30     queued    None            smp   30     default  N/A                                   
        4      N/A      rojas    0.2    02:45:00  00:00:21    N/A       30     queued    None            smp   30     default  N/A                                   
        
        Command Error/Debug:
        
    """

    args      = """-f"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_setres_setres_12():
    """
    setres test run: setres_12

        Command Output:
        Got starttime Sun Jan 01 16:30:00 2034 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'name': 'r1', 'queue': 'q_1', 'start': 2019745800.0, 'duration': 3000, 'cycle': None, 'res_id': 11, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r1 -s 2034-01-01-10:30 -u '*' -d 50 -q q_1 ANL-R01-1024 ANL-R00-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_8():
    """
    showres test run: showres_8

        Command Output:
        Reservation  Queue  User  Start                                 Duration  Passthrough  Partitions                   Time Remaining  
        ====================================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048             Not Started     
        r1           q_1    None  Sun Jan 01 16:30:00 2034 +0000 (UTC)  00:50     Allowed      ANL-R01-1024:ANL-R00-M0-512  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_13():
    """
    setres test run: setres_13

        Command Output:
        [{'name': 'r1', 'block_passthrough': False, 'project': None, 'start': 2019745800.0, 'cycle': None, 'duration': 3000, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512', 'res_id': 11, 'users': 'rojas'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-m -n r1 -u <USER>"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_9():
    """
    showres test run: showres_9

        Command Output:
        Reservation  Queue  User   Start                                 Duration  Passthrough  Partitions                   Time Remaining  
        =====================================================================================================================================
        david        q_1    None   Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048             Not Started     
        r1           q_1    rojas  Sun Jan 01 16:30:00 2034 +0000 (UTC)  00:50     Allowed      ANL-R01-1024:ANL-R00-M0-512  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_14():
    """
    setres test run: setres_14

        Command Output:
        [{'name': 'r1', 'block_passthrough': False, 'project': None, 'start': 2019745800.0, 'cycle': None, 'duration': 3000, 'partitions': 'ANL-R01-1024:ANL-R00-M0-512', 'res_id': 11, 'users': None}]
        
        
        Command Error/Debug:
        
    """

    args      = """-m -n r1 -u '*'"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_10():
    """
    showres test run: showres_10

        Command Output:
        Reservation  Queue  User  Start                                 Duration  Passthrough  Partitions                   Time Remaining  
        ====================================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048             Not Started     
        r1           q_1    None  Sun Jan 01 16:30:00 2034 +0000 (UTC)  00:50     Allowed      ANL-R01-1024:ANL-R00-M0-512  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_releaseres_releaseres_5():
    """
    releaseres test run: releaseres_5

        Command Output:
        Released reservation 'r1' for partitions: ['ANL-R01-1024', 'ANL-R00-M0-512']
        
        Command Error/Debug:
        releaseres.py -d r1
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d r1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_showres_showres_11():
    """
    showres test run: showres_11

        Command Output:
        Reservation  Queue  User  Start                                 Duration  Passthrough  Partitions        Time Remaining  
        =========================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_setres_setres_15():
    """
    setres test run: setres_15

        Command Output:
        Got starttime Sun Jan 01 16:30:00 2034 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'queue': 'q_1', 'start': 2019745800.0, 'cycle': None, 'duration': 3000, 'partitions': 'ANL-R00-R01-2048:ANL-R01-1024:ANL-R00-M0-512', 'res_id': 12, 'name': 'r1'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n r1 -s 2034-01-01-10:30 -u '*' -d 50 -q q_1 -p ANL-R01-1024:ANL-R00-M0-512 ANL-R00-R01-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_showres_showres_12():
    """
    showres test run: showres_12

        Command Output:
        Reservation  Queue  User  Start                                 Duration  Passthrough  Partitions                                    Time Remaining  
        =====================================================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048                              Not Started     
        r1           q_1    None  Sun Jan 01 16:30:00 2034 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048:ANL-R01-1024:ANL-R00-M0-512  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_releaseres_releaseres_6():
    """
    releaseres test run: releaseres_6

        Command Output:
        Released reservation 'r1' for partitions: ['ANL-R00-R01-2048', 'ANL-R01-1024', 'ANL-R00-M0-512']
        
        Command Error/Debug:
        releaseres.py -d r1
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'r1', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d r1"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_showres_showres_13():
    """
    showres test run: showres_13

        Command Output:
        Reservation  Queue  User  Start                                 Duration  Passthrough  Partitions        Time Remaining  
        =========================================================================================================================
        david        q_1    None  Thu Dec 01 16:30:00 2022 +0000 (UTC)  00:50     Allowed      ANL-R00-R01-2048  Not Started     
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('showres.py',_args,None) 
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
def test_qsub_qsub_10():
    """
    qsub test run: qsub_10

        Command Output:
        10
        
        Command Error/Debug:
        
    """

    args      = """--jobname "myjob_\$jobid" --env "myenv=myvar_\$jobid" -t 50 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_11():
    """
    qstat test run: qstat_11

        Command Output:
        JobID: 10
            JobName           : myjob_10
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : smp
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:58:58 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : None
            OutputPath        : None
            Envs              : myenv=myvar_10
            Command           : /bin/ls
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 10"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_11():
    """
    qsub test run: qsub_11

        Command Output:
        11
        
        Command Error/Debug:
        
    """

    args      = """--jobname "myjob_\$jobid" -o "myout_\$jobid" -t 50 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_12():
    """
    qstat test run: qstat_12

        Command Output:
        JobID: 11
            JobName           : myjob_11
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : smp
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:58:59 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : None
            OutputPath        : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/myout_11
            Envs              : 
            Command           : /bin/ls
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 11"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_12():
    """
    qsub test run: qsub_12

        Command Output:
        12
        
        Command Error/Debug:
        
    """

    args      = """-o "myout_\$jobid" -e "myerr_\$jobid" --debuglog mydebug_\$jobid -t 50 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_13():
    """
    qstat test run: qstat_13

        Command Output:
        JobID: 12
            JobName           : myout_12
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : smp
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:59:00 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/myerr_12
            OutputPath        : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/myout_12
            Envs              : 
            Command           : /bin/ls
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 12"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_13():
    """
    qsub test run: qsub_13

        Command Output:
        13
        
        Command Error/Debug:
        
    """

    args      = """-O "outpref_\$jobid" -t 50 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_14():
    """
    qstat test run: qstat_14

        Command Output:
        JobID: 13
            JobName           : outpref_13
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : smp
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:59:00 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/outpref_13.error
            OutputPath        : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/outpref_13.output
            Envs              : 
            Command           : /bin/ls
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 13"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_14():
    """
    qsub test run: qsub_14

        Command Output:
        14
        
        Command Error/Debug:
        
    """

    args      = """--jobname "myjob_\$jobid" -O "outpref_\$jobid" -t 50 -n 30 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_15():
    """
    qstat test run: qstat_15

        Command Output:
        JobID: 14
            JobName           : myjob_14
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : smp
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:59:01 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/outpref_14.error
            OutputPath        : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/outpref_14.output
            Envs              : 
            Command           : /bin/ls
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 14"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_15():
    """
    qsub test run: qsub_15

        Command Output:
        15
        
        Command Error/Debug:
        qsub.py --mode script -n 100 -t 75 --env a=1:c=3:b=2 --mode script --jobname $COBALT_JOBID-job --debug cobalt_script3.sh
        
        component: "system.validate_job", defer: False
          validate_job(
             {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': 'a=1:c=3:b=2', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '75', 'jobname': '$COBALT_JOBID-job', 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': 'script', 'error': False, 'nodecount': '100', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
             )
        
        
        component: "queue-manager.add_jobs", defer: False
          add_jobs(
             [{'kernel': 'default', 'args': [], 'outputdir': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'envs': {'a': '1', 'c': '3', 'b': '2'}, 'jobname': '$COBALT_JOBID-job', 'user_list': ['rojas'], 'umask': 18, 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'tag': 'job', 'command': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/cobalt_script3.sh', 'mode': 'script', 'run_project': False, 'path': '/home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin', 'nodes': 100, 'walltime': '75', 'ion_kernel': 'default', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'procs': 100, 'user': 'rojas'}],
             )
        
        
        Environment Vars: {'a': '1', 'c': '3', 'b': '2'}
        
        
    """

    args      = """cobalt_script3.sh"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_16():
    """
    qstat test run: qstat_16

        Command Output:
        JobID: 15
            JobName           : 15-job
            User              : rojas
            WallTime          : 01:15:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 100
            State             : queued
            Location          : None
            Mode              : script
            Procs             : 100
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:59:02 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : None
            OutputPath        : None
            Envs              : a=1 c=3 b=2
            Command           : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/cobalt_script3.sh
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 15"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qsub_qsub_16():
    """
    qsub test run: qsub_16

        Command Output:
        16
        
        Command Error/Debug:
        qsub.py --mode script -n 100 -t 75 --env a=1:c=3:b=2 --mode script --jobname $COBALT_JOBID-job --debug -t 50 -n 30 cobalt_script3.sh
        
        component: "system.validate_job", defer: False
          validate_job(
             {'kernel': 'default', 'verbose': False, 'held': False, 'notify': False, 'ion_kerneloptions': False, 'project': False, 'preemptable': False, 'outputprefix': False, 'umask': False, 'version': False, 'env': 'a=1:c=3:b=2', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'run_project': False, 'forcenoval': False, 'kerneloptions': False, 'time': '50', 'jobname': '$COBALT_JOBID-job', 'debug': True, 'dependencies': False, 'debuglog': False, 'ion_kernel': 'default', 'proccount': False, 'disable_preboot': False, 'geometry': False, 'queue': 'default', 'mode': 'script', 'error': False, 'nodecount': '30', 'output': False, 'inputfile': False, 'attrs': {}, 'user_list': False, 'interactive': False},
             )
        
        
        component: "queue-manager.add_jobs", defer: False
          add_jobs(
             [{'kernel': 'default', 'args': [], 'outputdir': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'envs': {'a': '1', 'c': '3', 'b': '2'}, 'jobname': '$COBALT_JOBID-job', 'user_list': ['rojas'], 'umask': 18, 'jobid': '*', 'queue': 'default', 'script_preboot': True, 'tag': 'job', 'command': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/cobalt_script3.sh', 'mode': 'script', 'run_project': False, 'path': '/home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin', 'nodes': 30, 'walltime': '50', 'ion_kernel': 'default', 'cwd': '/home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients', 'procs': 30, 'user': 'rojas'}],
             )
        
        
        Environment Vars: {'a': '1', 'c': '3', 'b': '2'}
        
        
    """

    args      = """-t 50 -n 30 cobalt_script3.sh"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_17():
    """
    qstat test run: qstat_17

        Command Output:
        JobID: 16
            JobName           : 16-job
            User              : rojas
            WallTime          : 00:50:00
            QueuedTime        : 00:00:00
            RunTime           : N/A
            TimeRemaining     : N/A
            Nodes             : 30
            State             : queued
            Location          : None
            Mode              : script
            Procs             : 30
            Preemptable       : False
            User_Hold         : False
            Admin_Hold        : False
            Queue             : default
            StartTime         : N/A
            Index             : None
            SubmitTime        : Wed Jan 08 22:59:02 2014 +0000 (UTC)
            Path              : /home/rojas/p/Cobalt/cobalt/src/clients:/home/rojas/p/Cobalt/cobalt/src/clients/POSIX:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin
            OutputDir         : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients
            ErrorPath         : None
            OutputPath        : None
            Envs              : a=1 c=3 b=2
            Command           : /home/rojas/p/Cobalt/cobalt/testsuite/TestCobaltClients/cobalt_script3.sh
            Args              : 
            Kernel            : default
            KernelOptions     : None
            ION_Kernel        : default
            ION_KernelOptions : None
            Project           : None
            Dependencies      : 
            S                 : Q
            Notify            : None
            Score             :   0.1  
            Maxtasktime       : None
            attrs             : {}
            dep_frac          : None
            user_list         : rojas
            Geometry          : Any
        
        
        Command Error/Debug:
        
    """

    args      = """-f -l 16"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
def test_qdel_qdel_1():
    """
    qdel test run: qdel_1

        Command Output:
              Deleted Jobs
        JobID  User   
        ==============
        1      rojas  
        2      rojas  
        3      rojas  
        4      rojas  
        5      rojas  
        6      rojas  
        7      rojas  
        8      rojas  
        9      rojas  
        10     rojas  
        11     rojas  
        12     rojas  
        13     rojas  
        14     rojas  
        15     rojas  
        16     rojas  
        
        Command Error/Debug:
        
    """

    args      = """1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qdel.py',_args,None) 
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
def test_releaseres_releaseres_7():
    """
    releaseres test run: releaseres_7

        Command Output:
        Released reservation 'david' for partitions: ['ANL-R00-R01-2048']
        
        Command Error/Debug:
        releaseres.py -d david
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'name': 'david', 'partitions': '*'}],
             )
        
        
        component: "scheduler.release_reservations", defer: False
          release_reservations(
             [{'name': 'david', 'partitions': '*'}],
             rojas,
             )
        
        
        
        
    """

    args      = """-d david"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('releaseres.py',_args,None) 
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
def test_partadm_partadm_add_7():
    """
    partadm test run: partadm_add_7

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R32-R33-2048', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 2048}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R32-R33-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_enable_7():
    """
    partadm test run: partadm_enable_7

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-R33-2048'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R32-R33-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_activate_7():
    """
    partadm test run: partadm_activate_7

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-R33-2048'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R32-R33-2048"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_add_8():
    """
    partadm test run: partadm_add_8

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R32-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R32-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_enable_8():
    """
    partadm test run: partadm_enable_8

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R32-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_activate_8():
    """
    partadm test run: partadm_activate_8

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R32-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_add_9():
    """
    partadm test run: partadm_add_9

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R32-M0-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R32-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_enable_9():
    """
    partadm test run: partadm_enable_9

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R32-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_activate_9():
    """
    partadm test run: partadm_activate_9

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-M0-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R32-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_add_10():
    """
    partadm test run: partadm_add_10

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R32-M1-512', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 512}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R32-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_enable_10():
    """
    partadm test run: partadm_enable_10

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-M1-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R32-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_activate_10():
    """
    partadm test run: partadm_activate_10

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R32-M1-512'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R32-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_add_11():
    """
    partadm test run: partadm_add_11

        Command Output:
        [{'scheduled': False, 'name': 'ANL-R41-1024', 'functional': False, 'queue': 'default', 'tag': 'partition', 'deps': None, 'size': 1024}]
        
        Command Error/Debug:
        
    """

    args      = """-a ANL-R41-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_enable_11():
    """
    partadm test run: partadm_enable_11

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R41-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--enable ANL-R41-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_partadm_activate_11():
    """
    partadm test run: partadm_activate_11

        Command Output:
        [{'tag': 'partition', 'name': 'ANL-R41-1024'}]
        
        Command Error/Debug:
        
    """

    args      = """--activate ANL-R41-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_cqadm_add_queues_q1():
    """
    cqadm test run: add_queues_q1

        Command Output:
        Added Queues  
        ==============
        q1            
        q2            
        
        Command Error/Debug:
        
    """

    args      = """--addq q1 q2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_cqadm_start_queues_q1():
    """
    cqadm test run: start_queues_q1

        Command Output:
        
        Command Error/Debug:
        
    """

    args      = """--start q1 q2"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('cqadm.py',_args,None) 
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
def test_partadm_appq_q1():
    """
    partadm test run: appq_q1

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R32-M0-512'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q1 --appq ANL-R32-M0-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_partadm_appq_q2():
    """
    partadm test run: appq_q2

        Command Output:
        [[{'tag': 'partition', 'name': 'ANL-R32-M1-512'}]]
        
        Command Error/Debug:
        
    """

    args      = """--queue q2 --appq ANL-R32-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('partadm.py',_args,None) 
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
def test_setres_setres_16():
    """
    setres test run: setres_16

        Command Output:
        Got starttime Wed Jan 08 22:59:00 2014 +0000 (UTC)
        [{'project': None, 'users': None, 'block_passthrough': False, 'queue': 'q2', 'start': 1389221940.0, 'cycle': None, 'duration': 3000, 'partitions': 'ANL-R32-M1-512', 'res_id': 13, 'name': 'res1'}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n res1 -s now -u '*' -d 50 -q q2 -p ANL-R32-M1-512"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_setres_setres_17():
    """
    setres test run: setres_17

        Command Output:
        Got starttime Wed Jan 08 22:59:00 2014 +0000 (UTC)
        [{'users': None, 'block_passthrough': False, 'name': 'res2', 'project': None, 'start': 1389221940.0, 'duration': 3000, 'partitions': 'ANL-R41-1024', 'res_id': 14, 'cycle': None}]
        
        
        Command Error/Debug:
        
    """

    args      = """-n res2 -s now -u '*' -d 50 -p ANL-R41-1024"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('setres.py',_args,None) 
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
def test_qsub_qsub_17():
    """
    qsub test run: qsub_17

        Command Output:
        17
        
        Command Error/Debug:
        
    """

    args      = """-t0 -n 256 -q q1 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_18():
    """
    qsub test run: qsub_18

        Command Output:
        18
        
        Command Error/Debug:
        
    """

    args      = """-t0 -n 256 -q q2 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qsub_qsub_19():
    """
    qsub test run: qsub_19

        Command Output:
        19
        
        Command Error/Debug:
        
    """

    args      = """-t0 -n 1024 -q R.res2 /bin/ls"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qsub.py',_args,None) 
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
def test_qstat_qstat_18():
    """
    qstat test run: qstat_18

        Command Output:
        JobID  User   WallTime  Nodes  State    Location        
        ========================================================
         2     rojas  01:55:00  30     exiting  ANL-R01-M0-512  
         3     rojas  02:45:00  30     exiting  ANL-R00-M0-512  
        17     rojas  00:00:00  256    queued   None            
        18     rojas  00:00:00  256    queued   None            
        19     rojas  00:00:00  1024   queued   None            
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('qstat.py',_args,None) 
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
