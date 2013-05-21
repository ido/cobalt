import testutils

# ---------------------------------------------------------------------------------
def test_nodelist_arg_1():
    """
    nodelist test run: arg_1

        Command Output:
          Host  Queue  State
          ====================
          D1    QD1    good 
          D2    QD2    bad  
          D3    QD3    ugly 
          U1    QU1    one  
          U2    QU2    two  
          U3    QU3    three
          

    """

    args      = ''
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_arg_2():
    """
    nodelist test run: arg_2

        Command Output:
          No arguments needed
          Host  Queue  State
          ====================
          D1    QD1    good 
          D2    QD2    bad  
          D3    QD3    ugly 
          U1    QU1    one  
          U2    QU2    two  
          U3    QU3    three
          

    """

    args      = """arg1"""
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_debug():
    """
    nodelist test run: debug

        Command Output:
          
          nodelist.py -d
          
          component: "system.get_implementation", defer: False
            get_implementation(
               )
          
          
          component: "system.get_node_status", defer: False
            get_node_status(
               )
          
          
          component: "system.get_queue_assignments", defer: False
            get_queue_assignments(
               )
          
          
          Host  Queue  State
          ====================
          D1    QD1    good 
          D2    QD2    bad  
          D3    QD3    ugly 
          U1    QU1    one  
          U2    QU2    two  
          U3    QU3    three
          

    """

    args      = """-d"""
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_options_1():
    """
    nodelist test run: options_1

        Command Output:
          Usage: nodelist.py
          
          nodelist.py: error: no such option: -l
          

    """

    args      = """-l"""
    exp_rs    = 512

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_options_2():
    """
    nodelist test run: options_2

        Command Output:
          Usage: nodelist.py
          
          Options:
            --version    show program's version number and exit
            -h, --help   show this help message and exit
            -d, --debug  turn on communication debugging
          

    """

    args      = """--help"""
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_options_3():
    """
    nodelist test run: options_3

        Command Output:
          Usage: nodelist.py
          
          Options:
            --version    show program's version number and exit
            -h, --help   show this help message and exit
            -d, --debug  turn on communication debugging
          

    """

    args      = """-h"""
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
def test_nodelist_options_4():
    """
    nodelist test run: options_4

        Command Output:
          version: "nodelist.py " + TBD + , Cobalt  + TBD
          

    """

    args      = """--version"""
    exp_rs    = 0

    results = testutils.run_cmd('nodelist.py',args,None) 
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
