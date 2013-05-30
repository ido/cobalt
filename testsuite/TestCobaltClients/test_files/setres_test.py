import testutils

# ---------------------------------------------------------------------------------
def test_setres_id_change_1():
    """
    setres test run: id_change_1
        Old Command Output:
          Setting res id to 8
          

    """

    args      = """--res_id 8"""

    cmdout    = \
"""Setting res id to 8
"""

    stubout   = \
"""
SET_RES_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_1():
    """
    setres test run: id_change_1

    """

    args      = """--debub --res_id 8"""

    cmdout    = \
"""Usage: setres.py [options] <partition1> ... <partitionN>

setres.py: error: no such option: --debub
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_2():
    """
    setres test run: id_change_2
        Old Command Output:
          Setting cycle_id to 8
          

    """

    args      = """--cycle_id 8"""

    cmdout    = \
"""Setting cycle id to 8
"""

    stubout   = \
"""
SET_CYCLE_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_3():
    """
    setres test run: id_change_3
        Old Command Output:
          Setting res id to 8
          Setting cycle_id to 8
          

    """

    args      = """--res_id 8 --cycle_id 8"""

    cmdout    = \
"""Setting res id to 8
Setting cycle id to 8
"""

    stubout   = \
"""
SET_RES_ID

id: 8, type: <type 'int'>

SET_CYCLE_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_4():
    """
    setres test run: id_change_4
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """--res_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_5():
    """
    setres test run: id_change_5
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """--cycle_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_6():
    """
    setres test run: id_change_6
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """--res_id 8 -m -n resname"""

    cmdout    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_7():
    """
    setres test run: id_change_7
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """--cycle_id 8 -p ANL-R00-R01-2048"""

    cmdout    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_1():
    """
    setres test run: force_1
        Old Command Output:
          WARNING: Forcing res id to 8
          WARNING: Forcing cycle id to 8
          

    """

    args      = """--cycle_id 8 --res_id 8 --force_id"""

    cmdout    = \
"""WARNING: Forcing res id to 8
WARNING: Forcing cycle id to 8
"""

    stubout   = \
"""
FORCE_RES_ID

id: 8, type: <type 'int'>

FORCE_CYCLE_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_2():
    """
    setres test run: force_2
        Old Command Output:
          

    """

    args      = """--force_id"""

    cmdout    = \
"""ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_3():
    """
    setres test run: force_3
        Old Command Output:
          --force_id can only be used with --cycle_id and/or --res_id.
          

    """

    args      = """--force_id -p ANL-R00-R01-2048 -s 2013_03_09-10:30"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:30:00 2013 +0000 (UTC)
ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_4():
    """
    setres test run: force_4
        Old Command Output:
          --force_id can only be used with --cycle_id and/or --res_id.
          

    """

    args      = """--force_id -m -n resname"""

    cmdout    = \
"""ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_1():
    """
    setres test run: modify_1
        Old Command Output:
          -m must by called with -n <reservation name>
          

    """

    args      = """-m"""

    cmdout    = \
"""-m must by called with -n <reservation name>
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_2():
    """
    setres test run: modify_2
        Old Command Output:
          True
          

    """

    args      = """-m -n resname"""

    cmdout    = \
"""True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_3():
    """
    setres test run: modify_3
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-m -n resname -D -c 10:10:10"""

    cmdout    = \
"""Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_4():
    """
    setres test run: modify_4
        Old Command Output:
          Error: start time '2013_03_9-10:10:10' is invalid
          start time is expected to be in the format: YYYY_MM_DD-HH:MM
          

    """

    args      = """-m -n resname -D -s 2013_03_9-10:10:10"""

    cmdout    = \
"""start time '2013_03_9-10:10:10' is invalid
start time is expected to be in the format: YYYY_MM_DD-HH:MM
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_5():
    """
    setres test run: modify_5
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-m -n resname -D -s 2013_03_9-10:10"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_6():
    """
    setres test run: modify_6
        Old Command Output:
          Setting new start time for for reservation 'resname': Tue Mar 26 17:01:40 2013
          True
          

    """

    args      = """-m -n resname -D -d 10:10:10"""

    cmdout    = \
"""Setting new start time for for reservation 'resname': Tue Mar 26 17:01:40 2013
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
defer:True
defer type: <type 'bool'>
start:1364335300.0
start type: <type 'float'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_7():
    """
    setres test run: modify_7
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10:30:30 -d 00:01:00"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
cycle:37800
cycle type: <type 'int'>
duration:60
duration type: <type 'int'>
start:1362845400.0
start type: <type 'float'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_8():
    """
    setres test run: modify_8
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u user1"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
cycle:600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
start:1362845400.0
start type: <type 'float'>
users:user1
users type: <type 'str'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_9():
    """
    setres test run: modify_9
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u user1:user2"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
cycle:600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
start:1362845400.0
start type: <type 'float'>
users:user1:user2
users type: <type 'str'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_10():
    """
    setres test run: modify_10
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj -u user1"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
cycle:600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
project:myproj
project type: <type 'str'>
start:1362845400.0
start type: <type 'float'>
users:user1
users type: <type 'str'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_11():
    """
    setres test run: modify_11
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --block_passthrough"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
block_passthrough:True
block_passthrough type: <type 'bool'>
cycle:600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
project:myproj
project type: <type 'str'>
start:1362845400.0
start type: <type 'float'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_12():
    """
    setres test run: modify_12
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --allow_passthrough"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
project:myproj
project type: <type 'str'>
start:1362845400.0
start type: <type 'float'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_13():
    """
    setres test run: modify_13
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-m -n resname --allow_passthrough --block_passthrough"""

    cmdout    = \
"""Attribute block_passthrough already set
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_14():
    """
    setres test run: modify_14
        Old Command Output:
          True
          

    """

    args      = """-m -n resname -A myproj --block_passthrough ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']

VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']

VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024']

GET_RESERVATIONS

cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
start:*
start type: <type 'str'>

SET_RESERVATIONS

name:resname
name type: <type 'str'>
block_passthrough:True
block_passthrough type: <type 'bool'>
partitions:ANL-R00-R01-2048:ANL-R00-1024:ANL-R01-1024
partitions type: <type 'str'>
project:myproj
project type: <type 'str'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_1():
    """
    setres test run: add_res_1
        Old Command Output:
          Must supply either -p with value or partitions as arguments
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-n resname -D"""

    cmdout    = \
"""ERROR:root:Must supply either -p with value or partitions as arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_2():
    """
    setres test run: add_res_2
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-n resname -D ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""Must supply a start time for the reservation with -s
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_3():
    """
    setres test run: add_res_3
        Old Command Output:
          Usage: setres.py [--version] [-m] -n name -s <starttime> -d <duration> 
                            -c <cycle time> -p <partition> -q <queue name> 
                            -D -u <user> [-f] [partion1] .. [partionN]
                            --res_id <new res_id>
                            --cycle_id <new cycle_id>
                            --block_passthrough
          starttime is in format: YYYY_MM_DD-HH:MM
          duration may be in minutes or HH:MM:SS
          cycle time may be in minutes or DD:HH:MM:SS
          queue name is only needed to specify a name other than the default
          cycle time, queue name, and user are optional
          

    """

    args      = """-n resname -s 2013_03_9-10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
Must supply a duration time for the reservation with -d
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_4():
    """
    setres test run: add_res_4
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          True
          

    """

    args      = """-n resname -s 2013_03_9-10:10 -d 50 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:None
cycle type: <type 'NoneType'>
duration:3000
duration type: <type 'int'>
name:resname
name type: <type 'str'>
partitions:ANL-R00-R01-2048:ANL-R00-1024
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1362845400.0
start type: <type 'float'>
users:None
users type: <type 'NoneType'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_5():
    """
    setres test run: add_res_5
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          True
          

    """

    args      = """-n resname -s 2013_03_9-10:10 -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:36600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
name:resname
name type: <type 'str'>
partitions:ANL-R00-R01-2048:ANL-R00-1024
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1362845400.0
start type: <type 'float'>
users:None
users type: <type 'NoneType'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_6():
    """
    setres test run: add_res_6
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          True
          

    """

    args      = """-s 2013_03_9-10:10 -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048', 'ANL-R00-1024']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:36600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
name:system
name type: <type 'str'>
partitions:ANL-R00-R01-2048:ANL-R00-1024
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1362845400.0
start type: <type 'float'>
users:None
users type: <type 'NoneType'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_7():
    """
    setres test run: add_res_7
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          True
          

    """

    args      = """-s 2013_03_9-10:10 -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048']

ADD_RESERVATIONS

block_passthrough:True
block_passthrough type: <type 'bool'>
cycle:None
cycle type: <type 'NoneType'>
duration:36600
duration type: <type 'int'>
name:system
name type: <type 'str'>
partitions:ANL-R00-R01-2048
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1362845400.0
start type: <type 'float'>
users:None
users type: <type 'NoneType'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_8():
    """
    setres test run: add_res_8
        Old Command Output:
          Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
          True
          True
          

    """

    args      = """-s 2013_03_9-10:10 -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj"""

    cmdout    = \
"""Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['ANL-R00-R01-2048']

ADD_RESERVATIONS

block_passthrough:True
block_passthrough type: <type 'bool'>
cycle:None
cycle type: <type 'NoneType'>
duration:36600
duration type: <type 'int'>
name:system
name type: <type 'str'>
partitions:ANL-R00-R01-2048
partitions type: <type 'str'>
project:myproj
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
start:1362845400.0
start type: <type 'float'>
users:None
users type: <type 'NoneType'>
user: gooduser

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

