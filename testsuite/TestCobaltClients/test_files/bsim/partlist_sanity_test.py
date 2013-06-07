import testutils

# ---------------------------------------------------------------------------------
def test_partlist_version_option_1():
    """
    partlist test run: version_option_1

        Command Output:
        version: "partlist.py " + $Revision: 1981 $ + , Cobalt  + $Version$
        
        Command Error/Debug:
        
    """

    args      = """--version"""
    exp_rs    = 0

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_version_option_2():
    """
    partlist test run: version_option_2

        Command Output:
        
        Command Error/Debug:Usage: partlist.py [options] 
        
        partlist.py: error: no such option: -v
        
        
    """

    args      = """-v"""
    exp_rs    = 512

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_debug():
    """
    partlist test run: debug

        Command Output:
        Name  Queue  State  Backfill
        ==============================
        
        Command Error/Debug:
        partlist.py -d
        
        component: "system.get_partitions", defer: True
          get_partitions(
             [{'queue': '*', 'scheduled': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'backfill_time': '*', 'children': '*', 'functional': '*', 'draining': '*', 'size': '*'}],
             )
        
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'queue': '*', 'active': True, 'partitions': '*'}],
             )
        
        
        
        
    """

    args      = """-d"""
    exp_rs    = 0

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

        Command Output:
        Usage: partlist.py [options] 
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
        
        Command Error/Debug:
        
    """

    args      = """-h"""
    exp_rs    = 0

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_help_option_1():
    """
    partlist test run: help_option_1

        Command Output:
        Usage: partlist.py [options] 
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
        
        Command Error/Debug:
        
    """

    args      = """--help"""
    exp_rs    = 0

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_invalid():
    """
    partlist test run: invalid

        Command Output:
        
        Command Error/Debug:Usage: partlist.py [options] 
        
        partlist.py: error: no such option: -k
        
        
    """

    args      = """-k"""
    exp_rs    = 512

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_argument_1():
    """
    partlist test run: argument_1

        Command Output:
        
        Command Error/Debug:No arguments required
        
        
    """

    args      = """arg"""
    exp_rs    = 256

    results = testutils.run_cmd('partlist.py',args,None) 
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
def test_partlist_argument_2():
    """
    partlist test run: argument_2

        Command Output:
        Name  Queue  State  Backfill
        ==============================
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    results = testutils.run_cmd('partlist.py',args,None) 
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
