#!/usr/bin/env python
"""
Cobalt Client Test Framework
"""
import os
import logging
import sys
import glob
import re
import difflib

IGNORE_TAG      = '<IGNORE>'
FAIL            = 'FAIL'
PASS            = 'PASS'
IGNORE          = 'IGNORE'
LOGFILE         = 'test_results.log'
ARGS_FILES      = '*_args.txt'
PATHFILES       = '_paths.txt'
OUTFILE         = 'proxystub.log'
CMD_OUTPUT      = 'cmd.log'

logger          = logging.getLogger()
fh              = logging.FileHandler(LOGFILE)

fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

# get command name
cn_p = re.compile(r'(.*)'+ARGS_FILES[1:])
getname = lambda fn: '' if cn_p.match(fn) == None else cn_p.sub(r'\1',fn)

# ignore comment lambda function defintion
ic_p = re.compile(r'(.*)#.*')
stripcomment = lambda data: ic_p.sub(r'\1',data)

# get comment lambda function definition
cm_p = re.compile(r'.*#(.*)')
getcomment = lambda data: '' if cm_p.match(data) == None else cm_p.sub(r'\1',data)

def run_cmd(cmd,cmd_suffix,args,comment):
    """
    run the specified command with arguments and pass the results back
    """
    dontcare,cmdname = os.path.split(cmd)
    cmdname = cmdname.replace('.py','').replace(' ','') + '_' + str(cmd_suffix) + '.log'
    cfd = open(cmdname,'a')
    cfd.write('\n====================================================\n# %s:\n%s' % (comment,args) )
    cfd.close()

    # run command and redirect output to /dev/null. don't care about this output... for now :)
    rs = os.system(cmd + ' ' + args + '&> %s' % CMD_OUTPUT)
    
    buf = ''
    if os.path.isfile(OUTFILE):
        fd = open(cmdname,'a')
        fd.write('\n------------------------------------------\nPROXY COMMAND OUTPUT:\n')
        fd.close()
        os.system('cat %s >> %s' % (OUTFILE   ,cmdname) )
        fd = open(cmdname,'a')
        fd.write('\n------------------------------------------\nCLIENT COMMAND OUTPUT:\n')
        fd.close()
        os.system('cat %s >> %s' % (CMD_OUTPUT,cmdname) )
        fd = open(OUTFILE,'r')
        buf = fd.read()
        fd.close()
    return rs,buf

def getlines(filename):
    """
    reads the file and get the lines without new line char
    """
    if not os.path.isfile(filename): return None
    fd   = open(filename,'r')
    lines = fd.read()
    lines = lines.split('\n')
    fd.close()
    return lines

def write_test_data():
    """
    write run the arguments are write the test data
    """
    # open the test data file to write to it. 
    fd = open('client_test_data.txt','w')

    argsfile_list = glob.glob(ARGS_FILES) # get the list of files with command args test runs

    ret_status = 0 # init return status ok

    # go through every client command file 
    for argsfile in argsfile_list:
        argslist = getlines(argsfile) # get the list of command line arguments 
        name     = getname(argsfile)
        paths    = getlines(name+PATHFILES)
        if paths == None: continue
        cmd1     = "%s/%s.py" % (paths[0],name)
        cmd2     = "%s/%s.py" % (paths[1],name)

        for args in argslist:
            print args
            continue
            if args    == '' : continue # skip null line
            if args[0] == '#': continue # skip comment line
            comment  = getcomment(args) # get the comment if there is one
            ignore   = args.find(IGNORE_TAG) != -1 # ignore failures if args is tagged
            args     = stripcomment(args).split('|') # strip out comments
            if len(args) == 2:
                arg1 = args[0]
                arg2 = args[1]
            else:
                arg1 = args[0]
                arg2 = args[0]
            rs1,buf1 = run_cmd(cmd1,1,arg1,comment)
            print(buf1)
            fd.write(buf1)
    fd.close()

    return ret_status

def test():
    """
    functon that will run a list of commands pairs and make sure that they are functionally the same
    """
    argsfile_list = glob.glob(ARGS_FILES) # get the list of files with command args test runs

    ret_status = 0 # init return status ok

    # go through every client command file 
    for argsfile in argsfile_list:
        argslist = getlines(argsfile) # get the list of command line arguments 
        name     = getname(argsfile)
        paths    = getlines(name+PATHFILES)
        if paths == None: continue
        cmd1     = "%s/%s.py" % (paths[0],name)
        cmd2     = "%s/%s.py" % (paths[1],name)

        logger.info('\n\n*************************************************************************************************')
        logger.info('cmd1: ' + cmd1)
        logger.info('cmd2: ' + cmd2)
        logger.info(    '*************************************************************************************************')

        for args in argslist:
            if args    == '' : continue # skip null line
            if args[0] == '#': continue # skip comment line
            comment  = getcomment(args) # get the comment if there is one
            ignore   = args.find(IGNORE_TAG) != -1 # ignore failures if args is tagged
            args     = stripcomment(args).split('|') # strip out comments
            if len(args) == 2:
                arg1 = args[0]
                arg2 = args[1]
            else:
                arg1 = args[0]
                arg2 = args[0]
            rs1,buf1 = run_cmd(cmd1,1,arg1,comment)
            rs2,buf2 = run_cmd(cmd2,2,arg2,comment)
            result = PASS
            if (buf1 != buf2):
                ret_status = 1
                if ignore: 
                    result = IGNORE # ignore failure ... no diff required but mark it as ignored
                else: 
                    result = FAIL
            logger.info('====================================================')
            if arg1 == arg2:
                logger.info('%s - %s\ncmd1 and cmd2 use:\n%s' % (result,comment,arg1))
            else:
                logger.info('%s - %s:\ncmd1: %s\ncmd2: %s' % (result,comment,arg1,arg2))
                
            # if failed then log the diffs
            if result == FAIL:
                dfunc = lambda diff: diff[2] if diff[0] not in ['+','-'] else '<' + diff[0]+diff[2]+'> '
                diffs = ''.join([ dfunc(diff) for diff in list(difflib.ndiff(buf1,buf2))])
                logger.info(diffs)

    return ret_status

#r = test()
r = write_test_data()
