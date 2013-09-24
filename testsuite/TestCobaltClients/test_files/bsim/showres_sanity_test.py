import testutils
import os
import pwd
# ---------------------------------------------------------------------------------
def test_showres_arg_1():
    """
    showres test run: arg_1

        Command Output:
        Reservation  Queue   User  Start                                 Duration  Passthrough  Partitions      Time Remaining  
        ========================================================================================================================
        res2         R.res2  None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R41-1024    00:47:21        
        res1         q2      None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R32-M1-512  00:47:21        
        
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
def test_showres_arg_2():
    """
    showres test run: arg_2

        Command Output:
        Reservation  Queue   User  Start                     Duration  Passthrough  Partitions      Time Remaining  
        ============================================================================================================
        res2         R.res2  None  Tue Sep  3 17:48:00 2013  00:50     Allowed      ANL-R41-1024    00:47:21        
        res1         q2      None  Tue Sep  3 17:48:00 2013  00:50     Allowed      ANL-R32-M1-512  00:47:21        
        
        Command Error/Debug:
        
    """

    args      = """--oldts"""
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
def test_showres_arg_3():
    """
    showres test run: arg_3

        Command Output:
        Reservation  Queue   User  Start                                 Duration  Passthrough  Partitions      Time Remaining  
        ========================================================================================================================
        res2         R.res2  None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R41-1024    00:47:20        
        res1         q2      None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R32-M1-512  00:47:20        
        
        Command Error/Debug:No arguments needed
        
        
    """

    args      = """arg1"""
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
def test_showres_l_option_1():
    """
    showres test run: l_option_1

        Command Output:
        Reservation  Queue   User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions      Time Remaining  
        ==========================================================================================================================================================================
        res2         R.res2  None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Tue Sep  3 23:38:00 2013 +0000 (UTC)  None        Allowed      ANL-R41-1024    00:47:20        
        res1         q2      None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Tue Sep  3 23:38:00 2013 +0000 (UTC)  None        Allowed      ANL-R32-M1-512  00:47:20        
        
        Command Error/Debug:
        
    """

    args      = """-l"""
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
def test_showres_l_option_2():
    """
    showres test run: l_option_2

        Command Output:
        Reservation  Queue   User  Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions      Time Remaining  
        ==================================================================================================================================================
        res2         R.res2  None  Tue Sep  3 17:48:00 2013  00:50     Tue Sep  3 18:38:00 2013  None        Allowed      ANL-R41-1024    00:47:20        
        res1         q2      None  Tue Sep  3 17:48:00 2013  00:50     Tue Sep  3 18:38:00 2013  None        Allowed      ANL-R32-M1-512  00:47:20        
        
        Command Error/Debug:
        
    """

    args      = """-l --oldts"""
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
def test_showres_x_option_1():
    """
    showres test run: x_option_1

        Command Output:
        Reservation  Queue   User  Start                                 Duration  End Time                              Cycle Time  Passthrough  Partitions      Project  ResID  CycleID  Time Remaining  
        ===================================================================================================================================================================================================
        res2         R.res2  None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Tue Sep  3 23:38:00 2013 +0000 (UTC)  None        Allowed      ANL-R41-1024    None     14     -        00:47:20        
        res1         q2      None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Tue Sep  3 23:38:00 2013 +0000 (UTC)  None        Allowed      ANL-R32-M1-512  None     13     -        00:47:20        
        
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
def test_showres_x_option_2():
    """
    showres test run: x_option_2

        Command Output:
        Reservation  Queue   User  Start                     Duration  End Time                  Cycle Time  Passthrough  Partitions      Project  ResID  CycleID  Time Remaining  
        ===========================================================================================================================================================================
        res2         R.res2  None  Tue Sep  3 17:48:00 2013  00:50     Tue Sep  3 18:38:00 2013  None        Allowed      ANL-R41-1024    None     14     -        00:47:19        
        res1         q2      None  Tue Sep  3 17:48:00 2013  00:50     Tue Sep  3 18:38:00 2013  None        Allowed      ANL-R32-M1-512  None     13     -        00:47:19        
        
        Command Error/Debug:
        
    """

    args      = """-x --oldts"""
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
def test_showres_combo():
    """
    showres test run: combo

        Command Output:
        
        Command Error/Debug:Only use -l or -x not both
        
        
    """

    args      = """-l -x"""
    exp_rs    = 256

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
def test_showres_help_1():
    """
    showres test run: help_1

        Command Output:
        Usage: showres [-l] [-x] [--oldts] [--version]
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
          -l           print reservation list verbose
          --oldts      use old timestamp
          -x           print reservations really verbose
        
        Command Error/Debug:
        
    """

    args      = """--help"""
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
def test_showres_help_2():
    """
    showres test run: help_2

        Command Output:
        Usage: showres [-l] [-x] [--oldts] [--version]
        
        Options:
          --version    show program's version number and exit
          -h, --help   show this help message and exit
          -d, --debug  turn on communication debugging
          -l           print reservation list verbose
          --oldts      use old timestamp
          -x           print reservations really verbose
        
        Command Error/Debug:
        
    """

    args      = """-h"""
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
def test_showres_version():
    """
    showres test run: version

        Command Output:
        version: "showres.py " + $Revision: 2154 $ + , Cobalt  + $Version$
        
        Command Error/Debug:
        
    """

    args      = """--version"""
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
def test_showres_debug():
    """
    showres test run: debug

        Command Output:
        Reservation  Queue   User  Start                                 Duration  Passthrough  Partitions      Time Remaining  
        ========================================================================================================================
        res2         R.res2  None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R41-1024    00:47:19        
        res1         q2      None  Tue Sep  3 22:48:00 2013 +0000 (UTC)  00:50     Allowed      ANL-R32-M1-512  00:47:19        
        
        Command Error/Debug:
        showres.py --debug
        
        component: "system.get_implementation", defer: False
          get_implementation(
             )
        
        
        component: "scheduler.get_reservations", defer: False
          get_reservations(
             [{'users': '*', 'block_passthrough': '*', 'duration': '*', 'cycle': '*', 'project': '*', 'cycle_id': '*', 'name': '*', 'queue': '*', 'start': '*', 'partitions': '*', 'res_id': '*'}],
             )
        
        
        
        
    """

    args      = """--debug"""
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
