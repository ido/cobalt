"""
Header Test

Usage: not important
version: whatever

OPTIONS DEFINITIONS:

'-f','--full',dest='full',help='show more verbose information',action='store_true'
'-l','--long',dest='long',help='show job info in vertical format',action='store_true'
'-Q',dest='Q',help='show queues and properties',action='store_true'
'--header',dest='header',type='string',help='specify custom header',callback=cb_split

"""
# ---------------------------------------------------------------------------------
from Cobalt.arg_parser import ArgParse
from Cobalt.client_utils import header_info
from os import environ
from Cobalt.client_utils import (cb_debug, cb_split)

def test_header1():
    """
    Test environment variable CQSTAT_HEADER 1
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ['CQSTAT_HEADER'] = 'custom:cqheader'
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom', 'cqheader']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)

def test_header2():
    """
    Test environment variable CQSTAT_HEADER 2
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ['QSTAT_HEADER'] = 'custom:qheader'
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom', 'cqheader']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)

def test_header3():
    """
    Test environment variable CQSTAT_HEADER_FULL 1
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ['CQSTAT_HEADER_FULL'] = 'custom:cqheader:full'
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['-f']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom','cqheader','full']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)

def test_header4():
    """
    Test environment variable CQSTAT_HEADER_FULL 2
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ['QSTAT_HEADER_FULL'] = 'custom:qheader:full'
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['-f']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom','cqheader','full']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)

def test_header5():
    """
    Test environment variable QSTAT_HEADER
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ.pop('CQSTAT_HEADER')
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom','qheader']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)


def test_header6():
    """
    Test environment variable QSTAT_HEADER_FULL
    """
    delim = ':'
    callbacks = [
        # <cb function>     <cb args (tuple) >
        ( cb_debug        , () ),
        ( cb_split        , (delim,) ) ]

    environ.pop('CQSTAT_HEADER_FULL')
    parser = ArgParse(__doc__, callbacks)
    parser.parse_it(['-f']) # parse the command line
    h = header_info(parser)
    if h.header == ['custom','qheader','full']:
        good = True
    else:
        good = False
    assert good, "Wrong value for header: %s" % str(h.header)

