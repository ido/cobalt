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

Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

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

Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

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
def test_partadm_combo_options_13():
    """
    partadm test run: combo_options_13

    """

    args      = """--savestate /tmp/s --xml"""

    cmdout    = \
"""
partadm.py --savestate /tmp/s --xml

Option combinations not allowed with: xml, savestate option(s)
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
def test_partadm_combo_options_14():
    """
    partadm test run: combo_options_14

    """

    args      = """-a -c -b PART"""

    cmdout    = \
"""
partadm.py -a -c -b PART

Option combinations not allowed with: blockinfo, clean_block option(s)
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


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_1():
    """
    partadm test run: savestate_option_1
        Old Command Output:
          directory /bad does not exist
          

    """

    args      = """--savestate /bad/save"""

    cmdout    = \
"""
partadm.py --savestate /bad/save

directory /bad/save does not exist
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
def test_partadm_savestate_option_2():
    """
    partadm test run: savestate_option_2
        Old Command Output:
          [{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
          

    """

    args      = """--savestate /tmp/save p1"""

    cmdout    = \
"""
partadm.py --savestate /tmp/save p1

[{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]
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
def test_partadm_savestate_option_3():
    """
    partadm test run: savestate_option_3
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
          
          
          
          partadm.py: error: --savestate option requires an argument
          

    """

    args      = """--savestate"""

    cmdout    = \
"""
partadm.py --savestate

Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


partadm.py: error: --savestate option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_savestate_option_4():
    """
    partadm test run: savestate_option_4
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          

    """

    args      = """--savestate /tmp/save -c p1"""

    cmdout    = \
"""
partadm.py --savestate /tmp/save -c p1

Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
def test_partadm_savestate_option_5():
    """
    partadm test run: savestate_option_5
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 2
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 3
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : aaa
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 4
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bbb
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 5
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : hhh
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 6
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : dito
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 7
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : myq
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 8
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : yours
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 9
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : zq
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--savestate /tmp/save -b p1"""

    cmdout    = \
"""
partadm.py --savestate /tmp/save -b p1

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 2
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 3
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : aaa
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 4
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bbb
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 5
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : hhh
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 6
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : dito
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 7
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : myq
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 8
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : yours
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 9
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : zq
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
SAVE

filename:/tmp/save
plist: [{'name': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_xml_option_1():
    """
    partadm test run: xml_option_1
        Old Command Output:
          ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
          

    """

    args      = """--xml"""

    cmdout    = \
"""
partadm.py --xml

['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
"""

    stubout   = \
"""\GENERATE_XML

name:*
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
def test_partadm_xml_option_2():
    """
    partadm test run: xml_option_2
        Old Command Output:
          ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
          

    """

    args      = """--xml p1"""

    cmdout    = \
"""
partadm.py --xml p1

['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
"""

    stubout   = \
"""\GENERATE_XML

name:*
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
def test_partadm_xml_option_3():
    """
    partadm test run: xml_option_3
        Old Command Output:
          ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
          

    """

    args      = """--xml --recursive p1"""

    cmdout    = \
"""
partadm.py --xml --recursive p1

['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]
\GENERATE_XML

name:*
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
def test_partadm_xml_option_4():
    """
    partadm test run: xml_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : A
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
              name               : B
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 2
              name               : C
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 3
              name               : D
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : aaa
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 4
              name               : E
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bbb
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 5
              name               : F
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : hhh
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 6
              name               : G
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : dito
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 7
              name               : H
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : myq
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 8
              name               : I
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : yours
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 9
              name               : J
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : zq
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--xml --blockinfo"""

    cmdout    = \
"""
partadm.py --xml --blockinfo

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : A
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
    name               : B
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 2
    name               : C
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 3
    name               : D
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : aaa
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 4
    name               : E
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bbb
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 5
    name               : F
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : hhh
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 6
    name               : G
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : dito
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 7
    name               : H
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : myq
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 8
    name               : I
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : yours
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 9
    name               : J
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : zq
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""\GENERATE_XML

name:*

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'A', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'B', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'C', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'D', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'E', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'F', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'G', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'H', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'I', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'J', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_xml_option_5():
    """
    partadm test run: xml_option_5
        Old Command Output:
          Initiating cleanup on block A
          Initiating cleanup on block B
          Initiating cleanup on block C
          Initiating cleanup on block D
          Initiating cleanup on block E
          Initiating cleanup on block F
          Initiating cleanup on block G
          Initiating cleanup on block H
          Initiating cleanup on block I
          Initiating cleanup on block J
          

    """

    args      = """--xml --clean_block"""

    cmdout    = \
"""
partadm.py --xml --clean_block

Initiating cleanup on block A
Initiating cleanup on block B
Initiating cleanup on block C
Initiating cleanup on block D
Initiating cleanup on block E
Initiating cleanup on block F
Initiating cleanup on block G
Initiating cleanup on block H
Initiating cleanup on block I
Initiating cleanup on block J
"""

    stubout   = \
"""\GENERATE_XML

name:*

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: A
var2 : None
whoami: gooduser

SET_CLEANING

part: B
var2 : None
whoami: gooduser

SET_CLEANING

part: C
var2 : None
whoami: gooduser

SET_CLEANING

part: D
var2 : None
whoami: gooduser

SET_CLEANING

part: E
var2 : None
whoami: gooduser

SET_CLEANING

part: F
var2 : None
whoami: gooduser

SET_CLEANING

part: G
var2 : None
whoami: gooduser

SET_CLEANING

part: H
var2 : None
whoami: gooduser

SET_CLEANING

part: I
var2 : None
whoami: gooduser

SET_CLEANING

part: J
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
def test_partadm_xml_option_6():
    """
    partadm test run: xml_option_6
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : A
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
              name               : B
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 2
              name               : C
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 3
              name               : D
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : aaa
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 4
              name               : E
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bbb
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 5
              name               : F
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : hhh
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 6
              name               : G
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : dito
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 7
              name               : H
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : myq
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 8
              name               : I
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : yours
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 9
              name               : J
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : zq
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--xml --recursive --blockinfo"""

    cmdout    = \
"""
partadm.py --xml --recursive --blockinfo

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : A
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
    name               : B
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 2
    name               : C
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 3
    name               : D
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : aaa
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 4
    name               : E
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bbb
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 5
    name               : F
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : hhh
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 6
    name               : G
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : dito
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 7
    name               : H
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : myq
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 8
    name               : I
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : yours
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 9
    name               : J
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : zq
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\GENERATE_XML

name:*

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'A', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'B', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'C', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'D', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'E', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'F', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'G', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'H', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'I', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'J', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_xml_option_7():
    """
    partadm test run: xml_option_7
        Old Command Output:
          Initiating cleanup on block A
          Initiating cleanup on block B
          Initiating cleanup on block C
          Initiating cleanup on block D
          Initiating cleanup on block E
          Initiating cleanup on block F
          Initiating cleanup on block G
          Initiating cleanup on block H
          Initiating cleanup on block I
          Initiating cleanup on block J
          

    """

    args      = """--xml --recursive --clean_block"""

    cmdout    = \
"""
partadm.py --xml --recursive --clean_block

Initiating cleanup on block A
Initiating cleanup on block B
Initiating cleanup on block C
Initiating cleanup on block D
Initiating cleanup on block E
Initiating cleanup on block F
Initiating cleanup on block G
Initiating cleanup on block H
Initiating cleanup on block I
Initiating cleanup on block J
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\GENERATE_XML

name:*

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: A
var2 : None
whoami: gooduser

SET_CLEANING

part: B
var2 : None
whoami: gooduser

SET_CLEANING

part: C
var2 : None
whoami: gooduser

SET_CLEANING

part: D
var2 : None
whoami: gooduser

SET_CLEANING

part: E
var2 : None
whoami: gooduser

SET_CLEANING

part: F
var2 : None
whoami: gooduser

SET_CLEANING

part: G
var2 : None
whoami: gooduser

SET_CLEANING

part: H
var2 : None
whoami: gooduser

SET_CLEANING

part: I
var2 : None
whoami: gooduser

SET_CLEANING

part: J
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
def test_partadm_queue_option_1():
    """
    partadm test run: queue_option_1
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
          
          
          
          partadm.py: error: --queue option requires an argument
          

    """

    args      = """--queue"""

    cmdout    = \
"""
partadm.py --queue

Usage: partadm.py [-a|-d] part1 part2 (add or del)
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
Usage: partadm.py [--boot-stop|--boot-start|--boot-status]

Must supply one of -a or -d or -l or -start or -stop or --queue or -b
Adding "-r" or "--recursive" will add the children of the blocks passed in.


partadm.py: error: --queue option requires an argument
"""

    stubout   = ''

    stubout_file = "stub.out"

    expected_results = ( 
                       512, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('partadm.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\n%s" % result


# ---------------------------------------------------------------------------------
def test_partadm_queue_option_2():
    """
    partadm test run: queue_option_2
        Old Command Output:
          'q1' is not an existing queue
          'q2' is not an existing queue
          

    """

    args      = """--queue q1:q2 p1 p2 p3"""

    cmdout    = \
"""
partadm.py --queue q1:q2 p1 p2 p3

'q1' is not an existing queue
'q2' is not an existing queue
"""

    stubout   = \
"""
GET_QUEUES

name:*
tag:queue
"""

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
def test_partadm_queue_option_3():
    """
    partadm test run: queue_option_3
        Old Command Output:
          ['p1']
          

    """

    args      = """--queue kebra:bbb:myq p1"""

    cmdout    = \
"""
partadm.py --queue kebra:bbb:myq p1

['p1']
"""

    stubout   = \
"""
GET_QUEUES

name:*
tag:queue

SET_PARTITION

name:p1
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
def test_partadm_queue_option_4():
    """
    partadm test run: queue_option_4
        Old Command Output:
          Initiating cleanup on block p1
          

    """

    args      = """--queue kebra:bbb:myq -c p1"""

    cmdout    = \
"""
partadm.py --queue kebra:bbb:myq -c p1

Initiating cleanup on block p1
"""

    stubout   = \
"""
GET_QUEUES

name:*
tag:queue

SET_PARTITION

name:p1
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: p1
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
def test_partadm_queue_option_5():
    """
    partadm test run: queue_option_5
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : p1
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : kebra
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--queue kebra:bbb:myq -b p1"""

    cmdout    = \
"""
partadm.py --queue kebra:bbb:myq -b p1

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : p1
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : kebra
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
GET_QUEUES

name:*
tag:queue

SET_PARTITION

name:p1
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'p1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_queue_option_6():
    """
    partadm test run: queue_option_6
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : p1
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
              name               : a
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--queue kebra:bbb -r -b p1"""

    cmdout    = \
"""
partadm.py --queue kebra:bbb -r -b p1

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : p1
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
    name               : a
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]

GET_QUEUES

name:*
tag:queue

SET_PARTITION

name:p1
tag:partition
name:a
tag:partition

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'p1', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': 'a', 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_queue_option_7():
    """
    partadm test run: queue_option_7
        Old Command Output:
          Initiating cleanup on block p1
          Initiating cleanup on block a
          

    """

    args      = """--queue kebra:bbb -r -c p1"""

    cmdout    = \
"""
partadm.py --queue kebra:bbb -r -c p1

Initiating cleanup on block p1
Initiating cleanup on block a
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]

GET_QUEUES

name:*
tag:queue

SET_PARTITION

name:p1
tag:partition
name:a
tag:partition

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: p1
var2 : None
whoami: gooduser

SET_CLEANING

part: a
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
def test_partadm_dump_option_1():
    """
    partadm test run: dump_option_1
        Old Command Output:
          [{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
          

    """

    args      = """--dump"""

    cmdout    = \
"""
partadm.py --dump

[{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
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
def test_partadm_dump_option_2():
    """
    partadm test run: dump_option_2
        Old Command Output:
          [{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
          

    """

    args      = """--dump p1"""

    cmdout    = \
"""
partadm.py --dump p1

[{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
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
def test_partadm_dump_option_3():
    """
    partadm test run: dump_option_3
        Old Command Output:
          [{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
          

    """

    args      = """--dump --recursive p1"""

    cmdout    = \
"""
partadm.py --dump --recursive p1

[{'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}]
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]
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
def test_partadm_dump_option_4():
    """
    partadm test run: dump_option_4
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 2
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 3
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : aaa
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 4
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bbb
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 5
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : hhh
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 6
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : dito
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 7
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : myq
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 8
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : yours
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 9
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : zq
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--dump --blockinfo"""

    cmdout    = \
"""
partadm.py --dump --blockinfo

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 2
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 3
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : aaa
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 4
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bbb
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 5
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : hhh
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 6
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : dito
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 7
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : myq
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 8
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : yours
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 9
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : zq
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_dump_option_5():
    """
    partadm test run: dump_option_5
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          

    """

    args      = """--dump --clean_block"""

    cmdout    = \
"""
partadm.py --dump --clean_block

Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
def test_partadm_dump_option_6():
    """
    partadm test run: dump_option_6
        Old Command Output:
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 0
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : jello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 2
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bello
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 3
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : aaa
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 4
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : bbb
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 5
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : hhh
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 6
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : dito
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 7
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : myq
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 8
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : yours
              relatives          : ['b']
              parents            : a, b, c
          
          scheduled: True
              functional         : True
              draining           : False
              passthrough_blocks : A
              children           : a
              size               : 9
              name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
              node_geometry      : ['48', '48', '48', '48', '48']
              state              : idle
              queue              : zq
              relatives          : ['b']
              parents            : a, b, c
          
          

    """

    args      = """--dump --recursive --blockinfo"""

    cmdout    = \
"""
partadm.py --dump --recursive --blockinfo

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 0
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : jello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 2
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bello
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 3
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : aaa
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 4
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : bbb
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 5
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : hhh
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 6
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : dito
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 7
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : myq
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 8
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : yours
    relatives          : ['b']
    parents            : a, b, c

scheduled: True
    functional         : True
    draining           : False
    passthrough_blocks : A
    children           : a
    size               : 9
    name               : {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
    node_geometry      : ['48', '48', '48', '48', '48']
    state              : idle
    queue              : zq
    relatives          : ['b']
    parents            : a, b, c

"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

GET_BLOCKS

plist: [{'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}, {'freeing': '*', 'extents': '*', 'corner_node': '*', 'wiring_conflict_list': '*', 'draining': '*', 'passthrough_blocks': '*', 'backfill_time': '*', 'children': '*', 'size': '*', 'node_geometry': '*', 'node_list': '*', 'state': '*', 'parents': '*', 'wire_list': '*', 'cleanup_pending': '*', 'scheduled': '*', 'block_type': '*', 'used_by': '*', 'reserved_by': '*', 'node_card_list': '*', 'midplane_list': '*', 'funcitonal': '*', 'name': {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}, 'midplane_geometry': '*', 'passthrough_midplane_list': '*', 'queue': '*', 'subblock_parent': '*', 'reserved_until': '*'}]
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
def test_partadm_dump_option_7():
    """
    partadm test run: dump_option_7
        Old Command Output:
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
          

    """

    args      = """--dump --recursive --clean_block"""

    cmdout    = \
"""
partadm.py --dump --recursive --clean_block

Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
Initiating cleanup on block {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

GET_PARTITIONS

plist: [{'scheduled': '*', 'queue': '*', 'state': '*', 'tag': 'partition', 'name': '*', 'deps': '*', 'functional': '*', 'size': '*'}]

SCHED_STATUS


BOOTING_STATUS


SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 0, 'name': 'A', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'kebra', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 1, 'name': 'B', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'jello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 2, 'name': 'C', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bello', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 3, 'name': 'D', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'aaa', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 4, 'name': 'E', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'bbb', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 5, 'name': 'F', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'hhh', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 6, 'name': 'G', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'dito', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 7, 'name': 'H', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'myq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 8, 'name': 'I', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'yours', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
var2 : None
whoami: gooduser

SET_CLEANING

part: {'scheduled': True, 'functional': True, 'draining': False, 'passthrough_blocks': ['A'], 'children': ['a'], 'size': 9, 'name': 'J', 'node_geometry': ['48', '48', '48', '48', '48'], 'state': 'idle', 'queue': 'zq', 'relatives': ['b'], 'parents': ['a', 'b', 'c']}
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
def test_partadm_boot_stop_option_1():
    """
    partadm test run: boot_stop_option_1
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop"""

    cmdout    = \
"""
partadm.py --boot-stop

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""\HALT_BOOTING

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
def test_partadm_boot_stop_option_2():
    """
    partadm test run: boot_stop_option_2
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop p1"""

    cmdout    = \
"""
partadm.py --boot-stop p1

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""\HALT_BOOTING

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
def test_partadm_boot_stop_option_3():
    """
    partadm test run: boot_stop_option_3
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive p1"""

    cmdout    = \
"""
partadm.py --boot-stop --recursive p1

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]
\HALT_BOOTING

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
def test_partadm_boot_stop_option_4():
    """
    partadm test run: boot_stop_option_4
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-stop --blockinfo

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""\HALT_BOOTING

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
def test_partadm_boot_stop_option_5():
    """
    partadm test run: boot_stop_option_5
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --clean_block"""

    cmdout    = \
"""
partadm.py --boot-stop --clean_block

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""\HALT_BOOTING

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
def test_partadm_boot_stop_option_6():
    """
    partadm test run: boot_stop_option_6
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-stop --recursive --blockinfo

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\HALT_BOOTING

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
def test_partadm_boot_stop_option_7():
    """
    partadm test run: boot_stop_option_7
        Old Command Output:
          Halting booting: halting scheduling is advised
          

    """

    args      = """--boot-stop --recursive --clean_block"""

    cmdout    = \
"""
partadm.py --boot-stop --recursive --clean_block

Halting booting: halting scheduling is advised
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\HALT_BOOTING

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
def test_partadm_boot_start_option_1():
    """
    partadm test run: boot_start_option_1
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start"""

    cmdout    = \
"""
partadm.py --boot-start

Enabling booting
"""

    stubout   = \
"""\RESUME_BOOTING

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
def test_partadm_boot_start_option_2():
    """
    partadm test run: boot_start_option_2
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start p1"""

    cmdout    = \
"""
partadm.py --boot-start p1

Enabling booting
"""

    stubout   = \
"""\RESUME_BOOTING

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
def test_partadm_boot_start_option_3():
    """
    partadm test run: boot_start_option_3
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive p1"""

    cmdout    = \
"""
partadm.py --boot-start --recursive p1

Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]
\RESUME_BOOTING

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
def test_partadm_boot_start_option_4():
    """
    partadm test run: boot_start_option_4
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-start --blockinfo

Enabling booting
"""

    stubout   = \
"""\RESUME_BOOTING

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
def test_partadm_boot_start_option_5():
    """
    partadm test run: boot_start_option_5
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --clean_block"""

    cmdout    = \
"""
partadm.py --boot-start --clean_block

Enabling booting
"""

    stubout   = \
"""\RESUME_BOOTING

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
def test_partadm_boot_start_option_6():
    """
    partadm test run: boot_start_option_6
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-start --recursive --blockinfo

Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\RESUME_BOOTING

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
def test_partadm_boot_start_option_7():
    """
    partadm test run: boot_start_option_7
        Old Command Output:
          Enabling booting
          

    """

    args      = """--boot-start --recursive --clean_block"""

    cmdout    = \
"""
partadm.py --boot-start --recursive --clean_block

Enabling booting
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []
\RESUME_BOOTING

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
def test_partadm_boot_status_option_1():
    """
    partadm test run: boot_status_option_1
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status"""

    cmdout    = \
"""
partadm.py --boot-status

Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

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
def test_partadm_boot_status_option_2():
    """
    partadm test run: boot_status_option_2
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status p1"""

    cmdout    = \
"""
partadm.py --boot-status p1

Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

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
def test_partadm_boot_status_option_3():
    """
    partadm test run: boot_status_option_3
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive p1"""

    cmdout    = \
"""
partadm.py --boot-status --recursive p1

Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: [{'tag': 'partition', 'name': 'p1', 'children_list': '*'}]

BOOTING_STATUS

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
def test_partadm_boot_status_option_4():
    """
    partadm test run: boot_status_option_4
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-status --blockinfo

Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

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
def test_partadm_boot_status_option_5():
    """
    partadm test run: boot_status_option_5
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --clean_block"""

    cmdout    = \
"""
partadm.py --boot-status --clean_block

Block Booting: ENABLED
"""

    stubout   = \
"""
BOOTING_STATUS

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
def test_partadm_boot_status_option_6():
    """
    partadm test run: boot_status_option_6
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive --blockinfo"""

    cmdout    = \
"""
partadm.py --boot-status --recursive --blockinfo

Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

BOOTING_STATUS

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
def test_partadm_():
    """
    partadm test run: 
        Old Command Output:
          Block Booting: ENABLED
          

    """

    args      = """--boot-status --recursive --clean_block"""

    cmdout    = \
"""
partadm.py --boot-status --recursive --clean_block

Block Booting: ENABLED
"""

    stubout   = \
"""
GET_PARTITIONS

plist: []

BOOTING_STATUS

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

