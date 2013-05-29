import testutils

# ---------------------------------------------------------------------------------
def test_schedctl_args_1():
    """
    schedctl test run: args_1

        Command Output:
          Need at least one option
          Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
          Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -d, --debug           turn on communication debugging
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = ''
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_args_2():
    """
    schedctl test run: args_2

        Command Output:
          Need at least one option
          Usage: schedctl.py [--stop | --start | --status | --reread-policy | --savestate]
          Usage: schedctl.py [--score | --inherit] jobid1 .. jobidN
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -d, --debug           turn on communication debugging
            --stop                stop scheduling jobs
            --start               resume scheduling jobs
            --status              query scheduling status
            --reread-policy       reread the utility function definition file
            --savestate=SAVESTATE
                                  write the current state to the specified file
            --score=ADJUST        <jobid> <jobid> adjust the scores of the arguments
            --inherit=DEP_FRAC    <jobid> <jobid> control the fraction of the score
                                  inherited by jobs which depend on the arguments
          

    """

    args      = """1"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_1():
    """
    schedctl test run: combo_1

        Command Output:
          Option combinations not allowed with: start option(s)
          

    """

    args      = """--start --stop"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_2():
    """
    schedctl test run: combo_2

        Command Output:
          Option combinations not allowed with: stat option(s)
          

    """

    args      = """--stop --status"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_3():
    """
    schedctl test run: combo_3

        Command Output:
          Option combinations not allowed with: stat option(s)
          

    """

    args      = """--start --status"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_4():
    """
    schedctl test run: combo_4

        Command Output:
          Option combinations not allowed with: reread option(s)
          

    """

    args      = """--reread-policy --status"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_5():
    """
    schedctl test run: combo_5

        Command Output:
          Option combinations not allowed with: adjust option(s)
          

    """

    args      = """--score 1.1 --stop 1 2 3 4"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_6():
    """
    schedctl test run: combo_6

        Command Output:
          Option combinations not allowed with: start, dep_frac option(s)
          

    """

    args      = """--inherit 1.1 --start 1 2 3 4"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_7():
    """
    schedctl test run: combo_7

        Command Output:
          Option combinations not allowed with: savestate option(s)
          

    """

    args      = """--start --savestate /tmp/s"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_combo_8():
    """
    schedctl test run: combo_8

        Command Output:
          updating scores for jobs: 2, 3, 4
          updating inheritance fraction for jobs: 2, 3, 4
          

    """

    args      = """--inherit 1.1 --score 1.1 1 2 3 4"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_start_1():
    """
    schedctl test run: start_1

        Command Output:
          No arguments needed
          Job Scheduling: ENABLED
          

    """

    args      = """--start 1"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_start_2():
    """
    schedctl test run: start_2

        Command Output:
          Job Scheduling: ENABLED
          

    """

    args      = """--start"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_stop_1():
    """
    schedctl test run: stop_1

        Command Output:
          No arguments needed
          Job Scheduling: DISABLED
          

    """

    args      = """--stop  1"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_stop_2():
    """
    schedctl test run: stop_2

        Command Output:
          Job Scheduling: DISABLED
          

    """

    args      = """--stop"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_stop_3():
    """
    schedctl test run: stop_3

        Command Output:
          
          schedctl.py -d --stop
          
          component: "scheduler.disable", defer: False
            disable(
               georgerojas,
               )
          
          
          Job Scheduling: DISABLED
          

    """

    args      = """-d --stop"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_reread_1():
    """
    schedctl test run: reread_1

        Command Output:
          No arguments needed
          Attempting to reread utility functions.
          

    """

    args      = """--reread-policy 1"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_reread_2():
    """
    schedctl test run: reread_2

        Command Output:
          Attempting to reread utility functions.
          

    """

    args      = """--reread-policy"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_save_1():
    """
    schedctl test run: save_1

        Command Output:
          state saved to file: /tmp/s
          

    """

    args      = """--savestate /tmp/s"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_save_2():
    """
    schedctl test run: save_2

        Command Output:
          directory s does not exist
          

    """

    args      = """--savestate s"""
    exp_rs    = 256

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_score_1():
    """
    schedctl test run: score_1

        Command Output:
          updating scores for jobs: 2, 3
          

    """

    args      = """--score 0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_score_2():
    """
    schedctl test run: score_2

        Command Output:
          updating scores for jobs: 2, 3
          

    """

    args      = """--score 1 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_score_3():
    """
    schedctl test run: score_3

        Command Output:
          updating scores for jobs: 2, 3
          

    """

    args      = """--score 1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_score_4():
    """
    schedctl test run: score_4

        Command Output:
          updating scores for jobs: 2, 3
          

    """

    args      = """--score -1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_score_5():
    """
    schedctl test run: score_5

        Command Output:
          updating scores for jobs: 2, 3
          

    """

    args      = """--score +1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_inherit_1():
    """
    schedctl test run: inherit_1

        Command Output:
          updating inheritance fraction for jobs: 2, 3
          

    """

    args      = """--inherit 0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_inherit_2():
    """
    schedctl test run: inherit_2

        Command Output:
          updating inheritance fraction for jobs: 2, 3
          

    """

    args      = """--inherit 1 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_inherit_3():
    """
    schedctl test run: inherit_3

        Command Output:
          updating inheritance fraction for jobs: 2, 3
          

    """

    args      = """--inherit 1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_inherit_4():
    """
    schedctl test run: inherit_4

        Command Output:
          updating inheritance fraction for jobs: 2, 3
          

    """

    args      = """--inherit -1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
def test_schedctl_inherit_5():
    """
    schedctl test run: inherit_5

        Command Output:
          updating inheritance fraction for jobs: 2, 3
          

    """

    args      = """--inherit +1.0 1 2 3"""
    exp_rs    = 0

    results = testutils.run_cmd('schedctl.py',args,None) 
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
