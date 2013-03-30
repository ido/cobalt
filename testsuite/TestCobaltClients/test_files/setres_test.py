import testutils

# ---------------------------------------------------------------------------------
def test_setres_id_change_1():
    """
    setres test run: id_change_1

    """

    args      = """--res_id 8"""

    cmdout    = \
"""
setres.py --res_id 8

Setting res id to 8
"""

    stubout   = \
"""
SET_RES_ID

id: 8
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_2():
    """
    setres test run: id_change_2

    """

    args      = """--cycle_id 8"""

    cmdout    = \
"""
setres.py --cycle_id 8

Setting cycle_id to 8
"""

    stubout   = \
"""
SET_CYCLE_ID

id: 8
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_3():
    """
    setres test run: id_change_3

    """

    args      = """--res_id 8 --cycle_id 8"""

    cmdout    = \
"""
setres.py --res_id 8 --cycle_id 8

Setting res id to 8
Setting cycle_id to 8
"""

    stubout   = \
"""
SET_RES_ID

id: 8

SET_CYCLE_ID

id: 8
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_4():
    """
    setres test run: id_change_4

    """

    args      = """--res_id 8 p1 p2 p3"""

    cmdout    = \
"""
setres.py --res_id 8 p1 p2 p3

No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_5():
    """
    setres test run: id_change_5

    """

    args      = """--cycle_id 8 p1 p2 p3"""

    cmdout    = \
"""
setres.py --cycle_id 8 p1 p2 p3

No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_6():
    """
    setres test run: id_change_6

    """

    args      = """--res_id 8 -m -n resname"""

    cmdout    = \
"""
setres.py --res_id 8 -m -n resname

No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_id_change_7():
    """
    setres test run: id_change_7

    """

    args      = """--cycle_id 8 -p p1"""

    cmdout    = \
"""
setres.py --cycle_id 8 -p p1

No partition arguments or other options allowed with id change options
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_1():
    """
    setres test run: force_1

    """

    args      = """--cycle_id 8 --res_id 8 --force_id"""

    cmdout    = \
"""
setres.py --cycle_id 8 --res_id 8 --force_id

WARNING: Forcing res id to 8
WARNING: Forcing cycle id to 8
"""

    stubout   = \
"""
FORCE_RES_ID

id: 8

FORCE_CYCLE_ID

id: 8
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_2():
    """
    setres test run: force_2

    """

    args      = """--force_id"""

    cmdout    = \
"""
setres.py --force_id

ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_3():
    """
    setres test run: force_3

    """

    args      = """--force_id -p p1 -s 2013_03_09-10:30"""

    cmdout    = \
"""
setres.py --force_id -p p1 -s 2013_03_09-10:30

Got starttime Sat Mar  9 16:30:00 2013 +0000 (UTC)
ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_force_4():
    """
    setres test run: force_4

    """

    args      = """--force_id -m -n resname"""

    cmdout    = \
"""
setres.py --force_id -m -n resname

ERROR:root:--force_id can only be used with --cycle_id and/or --res_id.
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_1():
    """
    setres test run: modify_1

    """

    args      = """-m"""

    cmdout    = \
"""
setres.py -m

-m must by called with -n <reservation name>
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_2():
    """
    setres test run: modify_2

    """

    args      = """-m -n resname"""

    cmdout    = \
"""
setres.py -m -n resname

True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_3():
    """
    setres test run: modify_3

    """

    args      = """-m -n resname -D -c 10:10:10"""

    cmdout    = \
"""
setres.py -m -n resname -D -c 10:10:10

Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_4():
    """
    setres test run: modify_4

    """

    args      = """-m -n resname -D -s 2013_03_9-10:10:10"""

    cmdout    = \
"""
setres.py -m -n resname -D -s 2013_03_9-10:10:10

Error: start time '2013_03_9-10:10:10' is invalid
start time is expected to be in the format: YYYY_MM_DD-HH:MM
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_5():
    """
    setres test run: modify_5

    """

    args      = """-m -n resname -D -s 2013_03_9-10:10"""

    cmdout    = \
"""
setres.py -m -n resname -D -s 2013_03_9-10:10

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
Cannot use -D while changing start or cycle time
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_6():
    """
    setres test run: modify_6

    """

    args      = """-m -n resname -D -d 10:10:10"""

    cmdout    = \
"""
setres.py -m -n resname -D -d 10:10:10

Setting new start time for for reservation 'resname': Tue Mar 26 17:01:40 2013
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
defer:True
start:1364335300.0
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_7():
    """
    setres test run: modify_7

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10:30:30 -d 00:01:00"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10:30:30 -d 00:01:00

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
cycle:37800
duration:60
start:1362845400.0
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_8():
    """
    setres test run: modify_8

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u georgerojas"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u georgerojas

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
cycle:600
duration:3000
start:1362845400.0
users:georgerojas
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_9():
    """
    setres test run: modify_9

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u georgerojas:georgerojas"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -u georgerojas:georgerojas

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
cycle:600
duration:3000
start:1362845400.0
users:georgerojas:georgerojas
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_10():
    """
    setres test run: modify_10

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj -u georgerojas"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj -u georgerojas

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
cycle:600
duration:3000
project:myproj
start:1362845400.0
users:georgerojas
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_11():
    """
    setres test run: modify_11

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --block_passthrough"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --block_passthrough

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
block_passthrough:True
cycle:600
duration:3000
project:myproj
start:1362845400.0
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_12():
    """
    setres test run: modify_12

    """

    args      = """-m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --allow_passthrough"""

    cmdout    = \
"""
setres.py -m -n resname -s 2013_03_9-10:10 -c 10 -d 50 -A myproj --allow_passthrough

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
"""

    stubout   = \
"""
GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
block_passthrough:False
cycle:600
duration:3000
project:myproj
start:1362845400.0
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_13():
    """
    setres test run: modify_13

    """

    args      = """-m -n resname --allow_passthrough --block_passthrough"""

    cmdout    = \
"""
setres.py -m -n resname --allow_passthrough --block_passthrough

Attribute block_passthrough already set
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_modify_14():
    """
    setres test run: modify_14

    """

    args      = """-m -n resname -A myproj --block_passthrough p1 p2 p3"""

    cmdout    = \
"""
setres.py -m -n resname -A myproj --block_passthrough p1 p2 p3

True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p1', 'p2', 'p3']

VERIFY_LOCATIONS

location list: ['p1', 'p2', 'p3']

GET_RESERVATIONS

cycle:*
duration:*
name:resname
start:*

SET_RESERVATIONS

name:resname
block_passthrough:True
partitions:p1:p2:p3
project:myproj
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_1():
    """
    setres test run: add_res_1

    """

    args      = """-n resname -D"""

    cmdout    = \
"""
setres.py -n resname -D

ERROR:root:Must supply either -p with value or partitions as arguments
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_2():
    """
    setres test run: add_res_2

    """

    args      = """-n resname -D p1 p2 p3"""

    cmdout    = \
"""
setres.py -n resname -D p1 p2 p3

Must supply a start time for the reservation with -s
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_3():
    """
    setres test run: add_res_3

    """

    args      = """-n resname -s 2013_03_9-10:10 p1 p2"""

    cmdout    = \
"""
setres.py -n resname -s 2013_03_9-10:10 p1 p2

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
Must supply a duration time for the reservation with -d
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_4():
    """
    setres test run: add_res_4

    """

    args      = """-n resname -s 2013_03_9-10:10 -d 50 p1 p2"""

    cmdout    = \
"""
setres.py -n resname -s 2013_03_9-10:10 -d 50 p1 p2

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1', 'p2']

VERIFY_LOCATIONS

location list: ['p1', 'p2']

ADD_RESERVATIONS

block_passthrough:False
cycle:None
duration:3000
name:resname
partitions:p1:p2
project:None
start:1362845400.0
users:None
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_5():
    """
    setres test run: add_res_5

    """

    args      = """-n resname -s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2"""

    cmdout    = \
"""
setres.py -n resname -s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1', 'p2']

VERIFY_LOCATIONS

location list: ['p1', 'p2']

ADD_RESERVATIONS

block_passthrough:False
cycle:36600
duration:3000
name:resname
partitions:p1:p2
project:None
start:1362845400.0
users:None
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_6():
    """
    setres test run: add_res_6

    """

    args      = """-s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2"""

    cmdout    = \
"""
setres.py -s 2013_03_9-10:10 -d 50 -c 10:10:10 p1 p2

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1', 'p2']

VERIFY_LOCATIONS

location list: ['p1', 'p2']

ADD_RESERVATIONS

block_passthrough:False
cycle:36600
duration:3000
name:system
partitions:p1:p2
project:None
start:1362845400.0
users:None
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_7():
    """
    setres test run: add_res_7

    """

    args      = """-s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough"""

    cmdout    = \
"""
setres.py -s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1']

ADD_RESERVATIONS

block_passthrough:True
cycle:None
duration:36600
name:system
partitions:p1
project:None
start:1362845400.0
users:None
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_setres_add_res_8():
    """
    setres test run: add_res_8

    """

    args      = """-s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough -q myq -A myproj"""

    cmdout    = \
"""
setres.py -s 2013_03_9-10:10 -d 10:10:10 -p p1 --block_passthrough -q myq -A myproj

Got starttime Sat Mar  9 16:10:00 2013 +0000 (UTC)
True
True
"""

    stubout   = \
"""
VERIFY_LOCATIONS

location list: ['p1']

ADD_RESERVATIONS

block_passthrough:True
cycle:None
duration:36600
name:system
partitions:p1
project:myproj
queue:myq
start:1362845400.0
users:None
user: georgerojas

CHECK_RESERVATIONS

"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('setres.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

