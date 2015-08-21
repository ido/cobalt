import testutils

# ---------------------------------------------------------------------------------
def test_setres_id_change_1():
    """
    setres test run: id_change_1

    """

    args      = """--res_id 8"""

    cmdout    = \
"""Setting res id to 8
"""

    cmderr    = ''

    stubout   = \
"""
SET_RES_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--cycle_id 8"""

    cmdout    = \
"""Setting cycle_id to 8
"""

    cmderr    = ''

    stubout   = \
"""
SET_CYCLE_ID

id: 8, type: <type 'int'>
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--res_id 8 --cycle_id 8"""

    cmdout    = \
"""Setting res id to 8
Setting cycle_id to 8
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--res_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = ''

    cmderr    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--cycle_id 8 ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = ''

    cmderr    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--res_id 8 -m -n resname"""

    cmdout    = ''

    cmderr    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--cycle_id 8 -p ANL-R00-R01-2048"""

    cmdout    = ''

    cmderr    = \
"""No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_8():
    """
    setres test run: id_change_8

    """

    args      = """--debug --res_id 8"""

    cmdout    = \
"""Setting res id to 8
"""

    cmderr    = \
"""
setres.py --debug --res_id 8

component: "scheduler.set_res_id", defer: False
  set_res_id(
     8,
     )


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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--cycle_id 8 --res_id 8 --force_id"""

    cmdout    = \
"""WARNING: Forcing res id to 8
WARNING: Forcing cycle id to 8
"""

    cmderr    = ''

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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--force_id"""

    cmdout    = ''

    cmderr    = \
"""--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--force_id -p ANL-R00-R01-2048 -s 2020_12_31-11:59"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
"""

    cmderr    = \
"""--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """--force_id -m -n resname"""

    cmdout    = ''

    cmderr    = \
"""--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m"""

    cmdout    = \
"""Usage: setres.py --help
Usage: setres.py [options] <partition1> ... <partitionN>

"""

    cmderr    = \
"""No arguments or options provided

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname"""

    cmdout    = \
"""[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -D -c 10:10:10"""

    cmdout    = ''

    cmderr    = \
"""Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -D -s 2020_12_31-11:59:10"""

    cmdout    = ''

    cmderr    = \
"""start time '2020_12_31-11:59:10. Error: Bad datetime format string.' is invalid
start time is expected to be in the format: YYYY_MM_DD-HH:MM
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -D -s 2020_12_31-11:59"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
"""

    cmderr    = \
"""Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -D -d 10:10:10"""

    cmdout    = \
"""Setting new start time for for reservation 'resname': Tue Mar 26 22:01:40 2013
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10:30:30 -d 00:01:00"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10 -d 50 -u user1"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
users:user1
users type: <type 'str'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10 -d 50 -u user1:user2"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
users:user1:user2
users type: <type 'str'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10 -d 50 -A myproj -u user1"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
users:user1
users type: <type 'str'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10 -d 50 -A myproj --block_passthrough"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -s 2020_12_31-11:59 -c 10 -d 50 -A myproj --allow_passthrough"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1609415940.0
start type: <type 'float'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname --allow_passthrough --block_passthrough"""

    cmdout    = ''

    cmderr    = \
"""Attribute block_passthrough already set
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-m -n resname -A myproj --block_passthrough ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_15():
    """
    setres test run: modify_15

    """

    args      = """-m -n resname"""

    cmdout    = \
"""[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_16():
    """
    setres test run: modify_16

    """

    args      = """-m -n resname -A myproj --block_passthrough --debug ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = \
"""[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = \
"""
setres.py -m -n resname -A myproj --block_passthrough --debug ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024

component: "system.verify_locations", defer: False
  verify_locations(
     ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024'],
     )


component: "system.verify_locations", defer: False
  verify_locations(
     ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024'],
     )


component: "system.verify_locations", defer: False
  verify_locations(
     ['ANL-R00-R01-2048', 'ANL-R00-1024', 'ANL-R01-1024'],
     )


component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'duration': '*', 'start': '*', 'name': 'resname', 'cycle': '*'}],
     )


component: "scheduler.set_reservations", defer: False
  set_reservations(
     [{'name': 'resname'}],
     {'project': 'myproj', 'block_passthrough': True, 'partitions': 'ANL-R00-R01-2048:ANL-R00-1024:ANL-R01-1024'},
     gooduser,
     )


component: "scheduler.get_reservations", defer: False
  get_reservations(
     [{'project': '*', 'start': '*', 'name': 'resname', 'cycle': '*', 'duration': '*', 'block_passthrough': '*', 'partitions': '*', 'res_id': '*', 'users': '*'}],
     )


component: "scheduler.check_reservations", defer: False
  check_reservations(
     )


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

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_17():
    """
    setres test run: modify_17

    """

    args      = """-m -n resname -s now"""

    cmdout    = \
"""Got starttime Tue Mar 26 21:58:00 2013 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1364335080.0
start type: <type 'float'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_18():
    """
    setres test run: modify_18

    """

    args      = """-m -n resname -s NOW"""

    cmdout    = \
"""Got starttime Tue Mar 26 21:58:00 2013 +0000 (UTC)
[{'users': 'gooduser', 'block_passthrough': True, 'active': True, 'duration': 500, 'partitions': 'P1:P2:P3:P4:P5:P6:P7:P8:P9:P10', 'project': 'proj', 'cycle_id': 10, 'name': 'resname', 'queue': 'kebra', 'start': 1000000, 'cycle': 300, 'res_id': 'id'}]
True
"""

    cmderr    = ''

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
start:1364335080.0
start type: <type 'float'>
user: gooduser

GET_RESERVATIONS

block_passthrough:*
block_passthrough type: <type 'str'>
cycle:*
cycle type: <type 'str'>
duration:*
duration type: <type 'str'>
name:resname
name type: <type 'str'>
partitions:*
partitions type: <type 'str'>
project:*
project type: <type 'str'>
res_id:*
res_id type: <type 'str'>
start:*
start type: <type 'str'>
users:*
users type: <type 'str'>

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-n resname -D"""

    cmdout    = ''

    cmderr    = \
"""Must supply either -p with value or partitions as arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-n resname -D ANL-R00-R01-2048 ANL-R00-1024 ANL-R01-1024"""

    cmdout    = ''

    cmderr    = \
"""Must supply a start time for the reservation with -s
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-n resname -s 2020_12_31-11:59 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
"""

    cmderr    = \
"""Must supply a duration time for the reservation with -d
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-n resname -s 2020_12_31-11:59 -d 50 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-n resname -s 2020_12_31-11:59 -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-s 2020_12_31-11:59 -n resname -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-s 2020_12_31-11:59 -n resname -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
name:resname
name type: <type 'str'>
partitions:ANL-R00-R01-2048
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
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

    """

    args      = """-s 2020_12_31-11:59 -n resname -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
name:resname
name type: <type 'str'>
partitions:ANL-R00-R01-2048
partitions type: <type 'str'>
project:myproj
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_9():
    """
    setres test run: add_res_9

    """

    args      = """-s 2020_12_31-11:59 -n resname -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj --debug"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = \
"""
setres.py -s 2020_12_31-11:59 -n resname -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj --debug

component: "system.verify_locations", defer: False
  verify_locations(
     ['ANL-R00-R01-2048'],
     )


component: "scheduler.add_reservations", defer: False
  add_reservations(
     [{'queue': 'myq', 'name': 'resname', 'block_passthrough': True, 'project': 'myproj', 'start': 1609415940.0, 'duration': 36600, 'users': None, 'cycle': None, 'partitions': 'ANL-R00-R01-2048'}],
     gooduser,
     )


component: "scheduler.check_reservations", defer: False
  check_reservations(
     )


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
name:resname
name type: <type 'str'>
partitions:ANL-R00-R01-2048
partitions type: <type 'str'>
project:myproj
project type: <type 'str'>
queue:myq
queue type: <type 'str'>
start:1609415940.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_10():
    """
    setres test run: add_res_10

    """

    args      = """-s 2020_12_31-11:59 -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj --debug"""

    cmdout    = \
"""Got starttime Thu Dec 31 11:59:00 2020 +0000 (UTC)
Usage: setres.py --help
Usage: setres.py [options] <partition1> ... <partitionN>

"""

    cmderr    = \
"""
setres.py -s 2020_12_31-11:59 -d 10:10:10 -p ANL-R00-R01-2048 --block_passthrough -q myq -A myproj --debug

No arguments or options provided

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_11():
    """
    setres test run: add_res_11

    """

    args      = """-n resname -s now -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Tue Mar 26 21:58:00 2013 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
start:1364335080.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_12():
    """
    setres test run: add_res_12

    """

    args      = """-n resname -s NOW -d 50 -c 10:10:10 ANL-R00-R01-2048 ANL-R00-1024"""

    cmdout    = \
"""Got starttime Tue Mar 26 21:58:00 2013 +0000 (UTC)
True
True
"""

    cmderr    = ''

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
start:1364335080.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_13():
    """
    setres test run: add_res_13

    """

    args      = """-n resname -s NOW -d 50 -c 10:10:10 -p p1:p2:p3 p4"""

    cmdout    = \
"""Got starttime Tue Mar 26 21:58:00 2013 +0000 (UTC)
True
True
"""

    cmderr    = ''

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:36600
cycle type: <type 'int'>
duration:3000
duration type: <type 'int'>
name:resname
name type: <type 'str'>
partitions:p4:p1:p2:p3
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1364335080.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_14():
    """
    setres test run: add_res_14

    """

    args      = """-n resname -s 2020_03_26-16:57 -d 00:01 -c 10:10:10 -p p1:p2:p3 p4"""

    cmdout    = \
"""Got starttime Thu Mar 26 16:57:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:36600
cycle type: <type 'int'>
duration:60
duration type: <type 'int'>
name:resname
name type: <type 'str'>
partitions:p4:p1:p2:p3
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1585241820.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_15():
    """
    setres test run: add_res_15

    """

    args      = """-n resname -s 2020_03_26-16:56 -d 00:01 -c 10:10:10 -p p1:p2:p3 p4"""

    cmdout    = \
"""Got starttime Thu Mar 26 16:56:00 2020 +0000 (UTC)
True
True
"""

    cmderr    = ''

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p4', 'p1', 'p2', 'p3']

ADD_RESERVATIONS

block_passthrough:False
block_passthrough type: <type 'bool'>
cycle:36600
cycle type: <type 'int'>
duration:60
duration type: <type 'int'>
name:resname
name type: <type 'str'>
partitions:p4:p1:p2:p3
partitions type: <type 'str'>
project:None
project type: <type 'NoneType'>
start:1585241760.0
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
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("")

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\n%s" % result

