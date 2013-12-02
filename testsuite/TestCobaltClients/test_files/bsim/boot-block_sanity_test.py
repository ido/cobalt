import testutils
import os
import pwd
# ---------------------------------------------------------------------------------
def test_boot_block_combo():
    """
    boot-block test run: combo

        Command Output:
        
        Command Error/Debug:ERROR: --free may not be specified with --reboot.
        
        
    """

    args      = """--free --reboot --block b --jobid 1"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_free_1():
    """
    boot-block test run: free_1

        Command Output:
        
        Command Error/Debug:ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--free"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_free_2():
    """
    boot-block test run: free_2

        Command Output:
        
        Command Error/Debug:ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--free --jobid 1"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_free_3():
    """
    boot-block test run: free_3

        Command Output:
        
        Command Error/Debug:component error: XMLRPC failure <Fault 1: 'initiate_proxy_free'> in system.initiate_proxy_free
        
        
        
    """

    args      = """--free --jobid 1 --block b"""
    exp_rs    = 256

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_reboot_1():
    """
    boot-block test run: reboot_1

        Command Output:
        
        Command Error/Debug:ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--reboot"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_reboot_2():
    """
    boot-block test run: reboot_2

        Command Output:
        
        Command Error/Debug:ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--reboot --jobid 1"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_reboot_3():
    """
    boot-block test run: reboot_3

        Command Output:
        
        Command Error/Debug:component error: XMLRPC failure <Fault 1: 'initiate_proxy_free'> in system.initiate_proxy_free
        
        
        
    """

    args      = """--reboot --jobid 1 --block b"""
    exp_rs    = 256

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_nofree_noreboot_1():
    """
    boot-block test run: nofree_noreboot_1

        Command Output:
        
        Command Error/Debug:ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--jobid 1"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_nofree_noreboot_2():
    """
    boot-block test run: nofree_noreboot_2

        Command Output:
        
        Command Error/Debug:ERROR: Cobalt jobid not specified as option or in environment.
        
        
    """

    args      = """--block b"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_nofree_noreboot_3():
    """
    boot-block test run: nofree_noreboot_3

        Command Output:
        
        Command Error/Debug:component error: XMLRPC failure <Fault 1: 'initiate_proxy_boot'> in system.initiate_proxy_boot
        
        
        
    """

    args      = """--jobid 1 --block b"""
    exp_rs    = 256

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_help_1():
    """
    boot-block test run: help_1

        Command Output:
        Usage: boot-block.py [options]
        
        Options:
          --version      show program's version number and exit
          -h, --help     show this help message and exit
          -d, --debug    turn on communication debugging
          --block=BLOCK  Name of block to boot.
          --reboot       If the block is already booted, free the block and reboot.
          --free         Free the block, if booted.  May not be combined with reboot
          --jobid=JOBID  Specify a cobalt jobid for this boot.
        
        Command Error/Debug:
        
    """

    args      = """--help"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_help_2():
    """
    boot-block test run: help_2

        Command Output:
        Usage: boot-block.py [options]
        
        Options:
          --version      show program's version number and exit
          -h, --help     show this help message and exit
          -d, --debug    turn on communication debugging
          --block=BLOCK  Name of block to boot.
          --reboot       If the block is already booted, free the block and reboot.
          --free         Free the block, if booted.  May not be combined with reboot
          --jobid=JOBID  Specify a cobalt jobid for this boot.
        
        Command Error/Debug:
        
    """

    args      = """-h"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_version():
    """
    boot-block test run: version

        Command Output:
        version: "boot-block.py " + TBD + , Cobalt  + $Version$
        
        Command Error/Debug:
        
    """

    args      = """--version"""
    exp_rs    = 0

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_debug_1():
    """
    boot-block test run: debug_1

        Command Output:
        
        Command Error/Debug:
        boot-block.py --debug
        
        ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--debug"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
def test_boot_block_debug_2():
    """
    boot-block test run: debug_2

        Command Output:
        
        Command Error/Debug:
        boot-block.py --d
        
        ERROR: block not specified as option or in environment.
        
        
    """

    args      = """--d"""
    exp_rs    = 768

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('boot-block.py',_args,None) 
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
