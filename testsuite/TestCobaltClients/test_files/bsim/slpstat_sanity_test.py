import testutils

# ---------------------------------------------------------------------------------
def test_slpstat_arg_1():
    """
    slpstat test run: arg_1

        Command Output:
        Name                  Location                                 Update Time               
        =========================================================================================
        system                https://Georges-MacBook-Pro.local:54115  Thu Jun  6 21:55:56 2013  
        queue-manager         https://Georges-MacBook-Pro.local:54102  Thu Jun  6 21:55:54 2013  
        scheduler             https://Georges-MacBook-Pro.local:54096  Thu Jun  6 21:55:54 2013  
        system_script_forker  https://Georges-MacBook-Pro.local:54100  Thu Jun  6 21:56:04 2013  
        bg_mpirun_forker      https://Georges-MacBook-Pro.local:54094  Thu Jun  6 21:55:56 2013  
        user_script_forker    https://Georges-MacBook-Pro.local:54097  Thu Jun  6 21:55:56 2013  
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_arg_2():
    """
    slpstat test run: arg_2

        Command Output:
        Name                  Location                                 Update Time               
        =========================================================================================
        system                https://Georges-MacBook-Pro.local:54115  Thu Jun  6 21:55:56 2013  
        queue-manager         https://Georges-MacBook-Pro.local:54102  Thu Jun  6 21:55:54 2013  
        scheduler             https://Georges-MacBook-Pro.local:54096  Thu Jun  6 21:55:54 2013  
        system_script_forker  https://Georges-MacBook-Pro.local:54100  Thu Jun  6 21:56:04 2013  
        bg_mpirun_forker      https://Georges-MacBook-Pro.local:54094  Thu Jun  6 21:55:56 2013  
        user_script_forker    https://Georges-MacBook-Pro.local:54097  Thu Jun  6 21:55:56 2013  
        
        Command Error/Debug:
        
    """

    args      = ''
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_arg_3():
    """
    slpstat test run: arg_3

        Command Output:
        Name                  Location                                 Update Time               
        =========================================================================================
        system                https://Georges-MacBook-Pro.local:54115  Thu Jun  6 21:55:56 2013  
        queue-manager         https://Georges-MacBook-Pro.local:54102  Thu Jun  6 21:55:54 2013  
        scheduler             https://Georges-MacBook-Pro.local:54096  Thu Jun  6 21:55:54 2013  
        system_script_forker  https://Georges-MacBook-Pro.local:54100  Thu Jun  6 21:56:04 2013  
        bg_mpirun_forker      https://Georges-MacBook-Pro.local:54094  Thu Jun  6 21:55:56 2013  
        user_script_forker    https://Georges-MacBook-Pro.local:54097  Thu Jun  6 21:55:56 2013  
        
        Command Error/Debug:No arguments needed
        
        
    """

    args      = """arg1"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_debug_1():
    """
    slpstat test run: debug_1

        Command Output:
        Name                  Location                                 Update Time               
        =========================================================================================
        system                https://Georges-MacBook-Pro.local:54115  Thu Jun  6 21:55:56 2013  
        queue-manager         https://Georges-MacBook-Pro.local:54102  Thu Jun  6 21:55:54 2013  
        scheduler             https://Georges-MacBook-Pro.local:54096  Thu Jun  6 21:55:54 2013  
        system_script_forker  https://Georges-MacBook-Pro.local:54100  Thu Jun  6 21:56:04 2013  
        bg_mpirun_forker      https://Georges-MacBook-Pro.local:54094  Thu Jun  6 21:55:56 2013  
        user_script_forker    https://Georges-MacBook-Pro.local:54097  Thu Jun  6 21:55:56 2013  
        
        Command Error/Debug:
        slpstat.py -d
        
        component: "service-location.get_services", defer: False
          get_services(
             [{'stamp': '*', 'tag': 'service', 'name': '*', 'location': '*'}],
             )
        
        
        
        
    """

    args      = """-d"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_debug_2():
    """
    slpstat test run: debug_2

        Command Output:
        Name                  Location                                 Update Time               
        =========================================================================================
        system                https://Georges-MacBook-Pro.local:54115  Thu Jun  6 21:55:56 2013  
        queue-manager         https://Georges-MacBook-Pro.local:54102  Thu Jun  6 21:55:54 2013  
        scheduler             https://Georges-MacBook-Pro.local:54096  Thu Jun  6 21:55:54 2013  
        system_script_forker  https://Georges-MacBook-Pro.local:54100  Thu Jun  6 21:56:04 2013  
        bg_mpirun_forker      https://Georges-MacBook-Pro.local:54094  Thu Jun  6 21:55:56 2013  
        user_script_forker    https://Georges-MacBook-Pro.local:54097  Thu Jun  6 21:55:56 2013  
        
        Command Error/Debug:
        slpstat.py -d
        
        component: "service-location.get_services", defer: False
          get_services(
             [{'stamp': '*', 'tag': 'service', 'name': '*', 'location': '*'}],
             )
        
        
        
        
    """

    args      = """-d"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_help_1():
    """
    slpstat test run: help_1

        Command Output:
        Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
        
        Command Error/Debug:
        
    """

    args      = """--help"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_help_2():
    """
    slpstat test run: help_2

        Command Output:
        Usage: slpstat.py [options] <queue name> <jobid1> [... <jobidN>]
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
        
        Command Error/Debug:
        
    """

    args      = """-h"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
def test_slpstat_version():
    """
    slpstat test run: version

        Command Output:
        version: "slpstat.py " + $Revision: 1221 $ + , Cobalt  + $Version$
        
        Command Error/Debug:
        
    """

    args      = """--version"""
    exp_rs    = 0

    results = testutils.run_cmd('slpstat.py',args,None) 
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
