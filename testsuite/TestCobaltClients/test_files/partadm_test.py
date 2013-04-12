import testutils

# ---------------------------------------------------------------------------------
def test_partadm_version_option():
    """
    partadm test run: version_option
        Old Command Output:
          Cobalt Version: $Version$
          

    """

    args      = """--version"""

    cmdout    = \
"""
partadm.py --version

version: "partadm.py " + $Revision: 1981 $ + , Cobalt  + $Version$
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_help_option_1():
    """
    partadm test run: help_option_1
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -a                    add the block to the list of managed blocks
            -d                    remove the block from the list of managed blocks
            -l                    list all blocks and their status
            -r, --recursive       recursively add all child blocks of the specified
                                  blocks in the positional arguments
            --queue=QUEUE         set the queues associated with the target blocks to
                                  this list of queues
            --activate            activate the block for scheduling
            --deactivate          deactivate the block for schedulign
            --enable              enable the running of jobs on the target blocks
            --disable             disable the running of jobs on the target blocks
            --fail                mark the block as though it failed diagnostics
                                  (deprecated)
            --unfail              clear failed diagnostics on a block (deprecated)
            --dump                dump a representation of the system's block state
            --xml                 dump a xml representation of the system's blocks for
                                  simulator usage
            --savestate=SAVESTATE
                                  force the system component to write it's statefile
            --boot-stop           disable booting of any jobs
            --boot-start          enable booting of any jobs
            --boot-status         show whether or not booting is enabled
            -b, --blockinfo       print the detailed state and information for all
                                  requested blocks.
            --pg_list             not implemented yet
            -c, --clean_block     force the block to cleanup and clear all internal
                                  reservations on that resource
          

    """

    args      = """-h"""

    cmdout    = \
"""
partadm.py -h

Usage: partadm.py [-a] [-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a                    add the block to the list of managed blocks
  -d                    remove the block from the list of managed blocks
  -l                    list all blocks and their status
  -r, --recursive       recursively add all child blocks of the specified
                        blocks in the positional arguments
  --queue=QUEUE         set the queues associated with the target blocks to
                        this list of queues
  --activate            activate the block for scheduling
  --deactivate          deactivate the block for schedulign
  --enable              enable the running of jobs on the target blocks
  --disable             disable the running of jobs on the target blocks
  --fail                mark the block as though it failed diagnostics
                        (deprecated)
  --unfail              clear failed diagnostics on a block (deprecated)
  --dump                dump a representation of the system's block state
  --xml                 dump a xml representation of the system's blocks for
                        simulator usage
  --savestate=SAVESTATE
                        force the system component to write it's statefile
  --boot-stop           disable booting of any jobs
  --boot-start          enable booting of any jobs
  --boot-status         show whether or not booting is enabled
  -b, --blockinfo       print the detailed state and information for all
                        requested blocks.
  --pg_list             not implemented yet
  -c, --clean_block     force the block to cleanup and clear all internal
                        reservations on that resource
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_help_option_2():
    """
    partadm test run: help_option_2
        Old Command Output:
          Usage: partadm.py [-a] [-d] part1 part2 (add or del)
          Usage: partadm.py -l
          Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
          Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
          Usage: partadm.py --queue=queue1:queue2 part1 part2
          Usage: partadm.py --fail part1 part2
          Usage: partadm.py --unfail part1 part2
          Usage: partadm.py --dump
          Usage: partadm.py --xml
          Usage: partadm.py --version
          Usage: partadm.py --savestate filename
          
          Must supply one of -a or -d or -l or -start or -stop or --queue or -b
          Adding "-r" or "--recursive" will add the children of the blocks passed in.
          
          
          
          Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -a                    add the block to the list of managed blocks
            -d                    remove the block from the list of managed blocks
            -l                    list all blocks and their status
            -r, --recursive       recursively add all child blocks of the specified
                                  blocks in the positional arguments
            --queue=QUEUE         set the queues associated with the target blocks to
                                  this list of queues
            --activate            activate the block for scheduling
            --deactivate          deactivate the block for schedulign
            --enable              enable the running of jobs on the target blocks
            --disable             disable the running of jobs on the target blocks
            --fail                mark the block as though it failed diagnostics
                                  (deprecated)
            --unfail              clear failed diagnostics on a block (deprecated)
            --dump                dump a representation of the system's block state
            --xml                 dump a xml representation of the system's blocks for
                                  simulator usage
            --savestate=SAVESTATE
                                  force the system component to write it's statefile
            --boot-stop           disable booting of any jobs
            --boot-start          enable booting of any jobs
            --boot-status         show whether or not booting is enabled
            -b, --blockinfo       print the detailed state and information for all
                                  requested blocks.
            --pg_list             not implemented yet
            -c, --clean_block     force the block to cleanup and clear all internal
                                  reservations on that resource
          

    """

    args      = """--help"""

    cmdout    = \
"""
partadm.py --help

Usage: partadm.py [-a] [-d] part1 part2 (add or del)
Usage: partadm.py -l
Usage: partadm.py [--activate|--deactivate] part1 part2 (functional or not)
Usage: partadm.py [--enable|--disable] part1 part2 (scheduleable or not)
Usage: partadm.py --queue=queue1:queue2 part1 part2
Usage: partadm.py --fail part1 part2
Usage: partadm.py --unfail part1 part2
Usage: partadm.py --dump
Usage: partadm.py --xml
Usage: partadm.py --version
Usage: partadm.py --savestate filename

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a                    add the block to the list of managed blocks
  -d                    remove the block from the list of managed blocks
  -l                    list all blocks and their status
  -r, --recursive       recursively add all child blocks of the specified
                        blocks in the positional arguments
  --queue=QUEUE         set the queues associated with the target blocks to
                        this list of queues
  --activate            activate the block for scheduling
  --deactivate          deactivate the block for schedulign
  --enable              enable the running of jobs on the target blocks
  --disable             disable the running of jobs on the target blocks
  --fail                mark the block as though it failed diagnostics
                        (deprecated)
  --unfail              clear failed diagnostics on a block (deprecated)
  --dump                dump a representation of the system's block state
  --xml                 dump a xml representation of the system's blocks for
                        simulator usage
  --savestate=SAVESTATE
                        force the system component to write it's statefile
  --boot-stop           disable booting of any jobs
  --boot-start          enable booting of any jobs
  --boot-status         show whether or not booting is enabled
  -b, --blockinfo       print the detailed state and information for all
                        requested blocks.
  --pg_list             not implemented yet
  -c, --clean_block     force the block to cleanup and clear all internal
                        reservations on that resource
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_no_arg_1():
    """
    partadm test run: no_arg_1

    """

    args      = ''

    cmdout    = \
"""
partadm.py 

Must supply one of -a or -d or -l or -start or -stop or --queue or -b.
Adding "-r" or "--recursive" will add the children of the blocks passed in.

"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_no_arg_2():
    """
    partadm test run: no_arg_2

    """

    args      = """-a"""

    cmdout    = \
"""
partadm.py -a

At least one partition must be supplied
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_1():
    """
    partadm test run: combo_options_1

    """

    args      = """-a -d PART"""

    cmdout    = \
"""
partadm.py -a -d PART

Option combinations not allowed with: add, delete option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_2():
    """
    partadm test run: combo_options_2

    """

    args      = """-a --enable PART"""

    cmdout    = \
"""
partadm.py -a --enable PART

Option combinations not allowed with: add, enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_3():
    """
    partadm test run: combo_options_3

    """

    args      = """-d --enable PART"""

    cmdout    = \
"""
partadm.py -d --enable PART

Option combinations not allowed with: delete, enable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_4():
    """
    partadm test run: combo_options_4

    """

    args      = """--enable --disable PART"""

    cmdout    = \
"""
partadm.py --enable --disable PART

Option combinations not allowed with: enable, disable option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_5():
    """
    partadm test run: combo_options_5

    """

    args      = """--deactivate --activate PART"""

    cmdout    = \
"""
partadm.py --deactivate --activate PART

Option combinations not allowed with: activate, deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_6():
    """
    partadm test run: combo_options_6

    """

    args      = """-a --deactivate PART"""

    cmdout    = \
"""
partadm.py -a --deactivate PART

Option combinations not allowed with: add, deactivate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_7():
    """
    partadm test run: combo_options_7

    """

    args      = """--fail --unfail PART"""

    cmdout    = \
"""
partadm.py --fail --unfail PART

Option combinations not allowed with: fail, unfail option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_8():
    """
    partadm test run: combo_options_8

    """

    args      = """--savestate /tmp/savestate -a"""

    cmdout    = \
"""
partadm.py --savestate /tmp/savestate -a

Option combinations not allowed with: add, savestate option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_9():
    """
    partadm test run: combo_options_9

    """

    args      = """-l --xml"""

    cmdout    = \
"""
partadm.py -l --xml

Option combinations not allowed with: xml, list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_10():
    """
    partadm test run: combo_options_10

    """

    args      = """-l --xml"""

    cmdout    = \
"""
partadm.py -l --xml

Option combinations not allowed with: xml, list_blocks option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_11():
    """
    partadm test run: combo_options_11

    """

    args      = """-a --queue q1 PART"""

    cmdout    = \
"""
partadm.py -a --queue q1 PART

Option combinations not allowed with: add, queue option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_combo_options_12():
    """
    partadm test run: combo_options_12

    """

    args      = """--dump --queue q1 PART"""

    cmdout    = \
"""
partadm.py --dump --queue q1 PART

Option combinations not allowed with: queue, dump option(s)
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       256, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_1():
    """
    partadm test run: add_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """-a -r PART"""

    cmdout    = \
"""
partadm.py -a -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

ADD_PARTITION

deps:[]
functional:False
name:PART
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:a
queue:default
scheduled:False
size:*
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_2():
    """
    partadm test run: add_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """-a --recursive PART"""

    cmdout    = \
"""
partadm.py -a --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

ADD_PARTITION

deps:[]
functional:False
name:PART
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:a
queue:default
scheduled:False
size:*
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_3():
    """
    partadm test run: add_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """-a PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py -a PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
ADD_PARTITION

deps:[]
functional:False
name:PART1
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:PART2
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:PART3
queue:default
scheduled:False
size:*
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_4():
    """
    partadm test run: add_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """-a -b PART1 PART2"""

    cmdout    = \
"""
partadm.py -a -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
ADD_PARTITION

deps:[]
functional:False
name:PART1
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:PART2
queue:default
scheduled:False
size:*
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_add_option_5():
    """
    partadm test run: add_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """-a -c PART1 PART2"""

    cmdout    = \
"""
partadm.py -a -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
ADD_PARTITION

deps:[]
functional:False
name:PART1
queue:default
scheduled:False
size:*
tag:partition
deps:[]
functional:False
name:PART2
queue:default
scheduled:False
size:*
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_1():
    """
    partadm test run: delete_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """-d -r PART"""

    cmdout    = \
"""
partadm.py -d -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

DEL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_2():
    """
    partadm test run: delete_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """-d --recursive PART"""

    cmdout    = \
"""
partadm.py -d --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

DEL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_3():
    """
    partadm test run: delete_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """-d PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py -d PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
DEL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_4():
    """
    partadm test run: delete_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """-d -b PART1 PART2"""

    cmdout    = \
"""
partadm.py -d -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
DEL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_delete_option_5():
    """
    partadm test run: delete_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """-d -c PART1 PART2"""

    cmdout    = \
"""
partadm.py -d -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
DEL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_1():
    """
    partadm test run: enable_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--enable -r PART"""

    cmdout    = \
"""
partadm.py --enable -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_2():
    """
    partadm test run: enable_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--enable --recursive PART"""

    cmdout    = \
"""
partadm.py --enable --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_3():
    """
    partadm test run: enable_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--enable PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --enable PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_4():
    """
    partadm test run: enable_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--enable -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --enable -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_enable_option_5():
    """
    partadm test run: enable_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--enable -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --enable -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_1():
    """
    partadm test run: disable_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--disable -r PART"""

    cmdout    = \
"""
partadm.py --disable -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_2():
    """
    partadm test run: disable_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--disable --recursive PART"""

    cmdout    = \
"""
partadm.py --disable --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_3():
    """
    partadm test run: disable_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--disable PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --disable PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_4():
    """
    partadm test run: disable_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--disable -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --disable -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_disable_option_5():
    """
    partadm test run: disable_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--disable -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --disable -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_1():
    """
    partadm test run: activate_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--activate -r PART"""

    cmdout    = \
"""
partadm.py --activate -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_2():
    """
    partadm test run: activate_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--activate --recursive PART"""

    cmdout    = \
"""
partadm.py --activate --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_3():
    """
    partadm test run: activate_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--activate PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --activate PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_4():
    """
    partadm test run: activate_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--activate -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --activate -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_activate_option_5():
    """
    partadm test run: activate_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--activate -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --activate -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_1():
    """
    partadm test run: deactivate_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--deactivate -r PART"""

    cmdout    = \
"""
partadm.py --deactivate -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_2():
    """
    partadm test run: deactivate_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--deactivate --recursive PART"""

    cmdout    = \
"""
partadm.py --deactivate --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

SET_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_3():
    """
    partadm test run: deactivate_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--deactivate PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --deactivate PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_4():
    """
    partadm test run: deactivate_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--deactivate -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --deactivate -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_deactivate_option_5():
    """
    partadm test run: deactivate_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--deactivate -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --deactivate -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
SET_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_1():
    """
    partadm test run: fail_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--fail -r PART"""

    cmdout    = \
"""
partadm.py --fail -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

FAIL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_2():
    """
    partadm test run: fail_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--fail --recursive PART"""

    cmdout    = \
"""
partadm.py --fail --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

FAIL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_3():
    """
    partadm test run: fail_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--fail PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --fail PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
FAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_4():
    """
    partadm test run: fail_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--fail -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --fail -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
FAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_fail_option_5():
    """
    partadm test run: fail_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--fail -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --fail -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
FAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_1():
    """
    partadm test run: unfail_option_1
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--unfail -r PART"""

    cmdout    = \
"""
partadm.py --unfail -r PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

UNFAIL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_2():
    """
    partadm test run: unfail_option_2
        Old Command Output:
          ['PART', 'a']
          

    """

    args      = """--unfail --recursive PART"""

    cmdout    = \
"""
partadm.py --unfail --recursive PART

['PART', 'a']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'PART', 'children_list': '*'}]

UNFAIL_PARTITION

name:PART
tag:partition
name:a
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_3():
    """
    partadm test run: unfail_option_3
        Old Command Output:
          ['PART1', 'PART2', 'PART3']
          

    """

    args      = """--unfail PART1 PART2 PART3"""

    cmdout    = \
"""
partadm.py --unfail PART1 PART2 PART3

['PART1', 'PART2', 'PART3']
"""

    stubout   = \
"""
UNFAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition
name:PART3
tag:partition
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_4():
    """
    partadm test run: unfail_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : PART1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 1
              name               : PART2
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--unfail -b PART1 PART2"""

    cmdout    = \
"""
partadm.py --unfail -b PART1 PART2

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : PART1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 1
    name               : PART2
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
UNFAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'PART2', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_unfail_option_5():
    """
    partadm test run: unfail_option_5
        Old Command Output:
          Initiating cleanup on block PART1
          Initiating cleanup on block PART2
          

    """

    args      = """--unfail -c PART1 PART2"""

    cmdout    = \
"""
partadm.py --unfail -c PART1 PART2

Initiating cleanup on block PART1
Initiating cleanup on block PART2
"""

    stubout   = \
"""
UNFAIL_PARTITION

name:PART1
tag:partition
name:PART2
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: PART1
var2 : None
whoami: gooduser

SET_CLEANING

part: PART2
var2 : None
whoami: gooduser
"""

    stubout_file = "stub.out"

    expected_results = ( 
                       0, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result

