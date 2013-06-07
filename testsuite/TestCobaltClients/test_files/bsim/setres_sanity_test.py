import testutils

# ---------------------------------------------------------------------------------
def test_setres_id_change_1():
    """
    setres test run: id_change_1

        Command Output:
        Setting res id to 8
        
        Command Error/Debug:
        
    """

    args      = """--res_id 8"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_1():
    """
    setres test run: id_change_1

        Command Output:
        
        Command Error/Debug:Usage: setres.py [options] <partition1> ... <partitionN>
        
        setres.py: error: no such option: --debub
        
        
    """

    args      = """--debub --res_id 8"""
    exp_rs    = 512

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_2():
    """
    setres test run: id_change_2

        Command Output:
        Setting cycle_id to 8
        
        Command Error/Debug:
        
    """

    args      = """--cycle_id 8"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_3():
    """
    setres test run: id_change_3

        Command Output:
        Setting res id to 8
        Setting cycle_id to 8
        
        Command Error/Debug:
        
    """

    args      = """--res_id 8 --cycle_id 8"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_4():
    """
    setres test run: id_change_4

        Command Output:
        
        Command Error/Debug:No partition arguments or other options allowed with id change options
        
        
    """

    args      = """--res_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_5():
    """
    setres test run: id_change_5

        Command Output:
        
        Command Error/Debug:No partition arguments or other options allowed with id change options
        
        
    """

    args      = """--cycle_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_6():
    """
    setres test run: id_change_6

        Command Output:
        
        Command Error/Debug:No partition arguments or other options allowed with id change options
        
        
    """

    args      = """--res_id 8 -m -n resname"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_id_change_7():
    """
    setres test run: id_change_7

        Command Output:
        
        Command Error/Debug:No partition arguments or other options allowed with id change options
        
        
    """

    args      = """--cycle_id 8 -p ANL-R00-R01-2048"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_force_1():
    """
    setres test run: force_1

        Command Output:
        WARNING: Forcing res id to 8
        WARNING: Forcing cycle id to 8
        
        Command Error/Debug:
        
    """

    args      = """--cycle_id 8 --res_id 8 --force_id"""
    exp_rs    = 0

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_force_2():
    """
    setres test run: force_2

        Command Output:
        
        Command Error/Debug:ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
        
        
    """

    args      = """--force_id"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_force_3():
    """
    setres test run: force_3

        Command Output:
        Got starttime Sat Mar  9 16:30:00 2013 +0000 (UTC)
        
        Command Error/Debug:ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
        
        
    """

    args      = """--force_id -p ANL-R00-R01-2048 -s 2013_03_09-10:30"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_force_4():
    """
    setres test run: force_4

        Command Output:
        
        Command Error/Debug:ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
        
        
    """

    args      = """--force_id -m -n resname"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_modify_1():
    """
    setres test run: modify_1

        Command Output:
        
        Command Error/Debug:-m must by called with -n <reservation name>
        
        
    """

    args      = """-m"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_modify_3():
    """
    setres test run: modify_3

        Command Output:
        
        Command Error/Debug:Cannot use -D while changing start or cycle time
        
        
    """

    args      = """-m -n resname -D -c 10:10:10"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_modify_4():
    """
    setres test run: modify_4

        Command Output:
        
        Command Error/Debug:start time '2013_03_9-10:10:10' is invalid
        start time is expected to be in the format: YYYY_MM_DD-HH:MM
        
        
    """

    args      = """-m -n resname -D -s 2013_03_9-10:10:10"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_modify_5():
    """
    setres test run: modify_5

        Command Output:
        Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
        
        Command Error/Debug:Cannot use -D while changing start or cycle time
        
        
    """

    args      = """-m -n resname -D -s 2013_03_9-10:10"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_modify_13():
    """
    setres test run: modify_13

        Command Output:
        
        Command Error/Debug:Attribute block_passthrough already set
        
        
    """

    args      = """-m -n resname --allow_passthrough --block_passthrough"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_add_res_1():
    """
    setres test run: add_res_1

        Command Output:
        
        Command Error/Debug:ERROR:root:Must supply either -p with value or partitions as arguments
        
        
    """

    args      = """-n resname -D"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_add_res_2():
    """
    setres test run: add_res_2

        Command Output:
        
        Command Error/Debug:Must supply a start time for the reservation with -s
        
        
    """

    args      = """-n resname -D ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
def test_setres_add_res_3():
    """
    setres test run: add_res_3

        Command Output:
        Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
        
        Command Error/Debug:Must supply a duration time for the reservation with -d
        
        
    """

    args      = """-n resname -s 2013_03_9-10:10 ANL-R00-R01-2048 ANL-R00-1024"""
    exp_rs    = 256

    results = testutils.run_cmd('setres.py',args,None) 
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
