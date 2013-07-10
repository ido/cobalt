#!/usr/bin/env python
"""
Generate Tests

Usage: %prog [options] [argsfile1 ... argsfileN]

All python args files shall follow the following naming convention: <command>_args.py.
Test files generated will follow the following naming convention: <command>_test.py.
If new command in not environment variable PATH or in the same directory then -n option is needed.
If old command is not in the same directory then -o option is needed.

OPTIONS DEFINITIONS:

'-o','--opath',dest='opath',type='string',help='path of old commands',callback=cb_path
'-n','--npath',dest='npath',type='string',help='path of new commands',callback=cb_path
'-t','--tpath',dest='tpath',type='string',help='path of test argument files',callback=cb_path

'-s','--stubo',dest='stubo',type='string',default='stub.out', /
  help='stub functions output file (default: stub.out)'

'--sanity-tests',dest='sanity',action='store_true', default=False, /
  help='Generate tests to check for return status and fata errors'

'--compare-tests', dest='compare',action='store_true', default=False, /
  help='Generate tests to compare output using old commands, -o options needs be supplied'

'--skip-list',dest='skip_list',type='string', /
  help='skip tests matching skip list (format: <str1>:...:<strN>)', callback=cb_skip_list

"""
import os
import sys
import glob
import re
import difflib
import os
import pwd

if __name__ == '__main__':
    from arg_parser import ArgParse

CMD_OUTPUT      = 'cmd.out'
CMD_ERROR       = 'cmd.err'
ARGS_FILES      = '*_args.py'
TESTHOOK_FILE   = '.testhook'

# Template constants
DS  = '<DOCSTR>'
AR  = '<ARGS>'
CO  = '<CMDOUT>'
CE  = '<CMDERR>'
SO  = '<STUBOUT>'
RS  = '<RS>'
TQ  = '<TQ>'
TC  = '<TC_NAME>'
TH  = '<TEST_HOOK>'
CM  = '<CMD>'
NM  = '<NAME>'
SF  = '<STUBFILE>'
ES1 = '\\\n""""""' # empty string 
ES2 = '""""""' # empty string
RTQ = '"""'

TEST_TEMPLATE = \
"""
# ---------------------------------------------------------------------------------
def test_<NAME>_<TC_NAME>():
    <TQ>
<DOCSTR>
    <TQ>

    args      = <TQ><ARGS><TQ>

    cmdout    = \\
<TQ><CMDOUT><TQ>

    cmderr    = \\
<TQ><CMDERR><TQ>

    stubout   = \\
<TQ><STUBOUT><TQ>

    stubout_file = "<STUBFILE>"

    expected_results = ( 
                       <RS>, # Expected return status 
                       cmdout, # Expected command output
                       stubout, # Expected stub functions output
                       cmderr, # Expected command error output 
                       ) 

    testutils.save_testhook("<TEST_HOOK>")

    results = testutils.run_cmd('<CMD>.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    testutils.remove_testhook()

    correct = 1
    assert result == correct, "Result:\\n%s" % result

"""

SANITY_TEST_TEMPLATE = \
"""
# ---------------------------------------------------------------------------------
def test_<NAME>_<TC_NAME>():
    <TQ>
<DOCSTR>
    <TQ>

    args      = <TQ><ARGS><TQ>
    exp_rs    = <RS>

    user    = pwd.getpwuid(os.getuid())[0] 
    _args   = args.replace('<USER>',user)

    results = testutils.run_cmd('<CMD>.py',_args,None) 
    rs      = results[0]
    cmd_out = results[1]
    cmd_err = results[3]

    # Test Pass Criterias
    no_rs_err     = (rs == exp_rs)
    no_fatal_exc  = (cmd_out.find("FATAL EXCEPTION") == -1)

    result = no_rs_err and no_fatal_exc

    errmsg  = "\\n\\nFailed Data:\\n\\n" \\
        "Return Status %s, Expected Return Status %s\\n\\n" \\
        "Command Output:\\n%s\\n\\n" \\
        "Command Error:\\n%s\\n\\n" \\
        "Arguments: %s" % (str(rs), str(exp_rs), str(cmd_out), str(cmd_err), _args)

    assert result, errmsg
"""

# get command name
cn_p = re.compile(r'(.*)'+ARGS_FILES[1:])
getname = lambda fn: '' if cn_p.match(fn) == None else cn_p.sub(r'\1',fn)

# indent buffer
indent = lambda x,buf:'\n'.join([(x*' ')+line for line in buf.split('\n')])

def getcmd(path, args_info, name):
    """
    This function will get the command name
    """
    if 'command' in args_info:
        _cmd  = "%s%s.py" % (path, args_info['command'])
        _name = args_info['command']
    else:
        _cmd  = "%s%s.py" % (path, name)
        _name = name
    return (_name, _cmd)


def save_testhook(testhook):
    """
    save the test information string that can be use to control testing permutations
    """
    if testhook != '' and testhook != None:
        fd = open(TESTHOOK_FILE,'w')
        fd.write(testhook)
        fd.close()

def get_testhook():
    """
    get the saved test information 
    """
    info = get_output(TESTHOOK_FILE,False)
    return info

def remove_testhook():
    """
    remove the test info file
    """
    if os.path.isfile(TESTHOOK_FILE):
        os.remove(TESTHOOK_FILE)

def get_test(cmd, tc_name, docstr, args, rs, cmdout, stubout, stubout_file, thook, cmderr):
    """
    Get Test from template with all tags replace
    """
    return TEST_TEMPLATE.replace(CM,cmd).replace(TC,tc_name).replace(TQ,RTQ).                      \
        replace(DS,docstr).replace(AR,args).replace(CO,cmdout).replace(SO,stubout).                \
        replace(RS,str(rs)).replace(TH,thook).replace(NM,cmd.replace('-','_')).replace(CE,cmderr). \
        replace(SF,stubout_file).replace(ES1,"''").replace(ES2,"''")

def get_sanity_test(cmd, tc_name, docstr, args, rs):
    """
    Get Return Status Test from template with all tags replace
    """
    return SANITY_TEST_TEMPLATE.replace(CM,cmd).replace(TC,tc_name).replace(TQ,RTQ). \
        replace(DS,docstr).replace(AR,args).replace(RS,str(rs)).replace(ES1,"''").   \
        replace(ES2,"''").replace(NM,cmd.replace('-','_'))

def get_output(filename,remove_file = True):
    """
    get output from the specified filename. delete file after getting the data
    """
    output = ''
    if os.path.isfile(filename):
        fd = open(filename,'r')
        output = fd.read()
        fd.close()
        if remove_file:
            os.remove(filename)
    return output

def getdiff(buf1,buf2):
    """
    do a diff on the two specified buffers
    """
    dfunc = lambda diff: diff[2] if diff[0] not in ['+','-'] else '<' + diff[0]+diff[2]+'> '
    return ''.join([ dfunc(diff) for diff in list(difflib.ndiff(buf1,buf2))])

def validate_results(results,expected_results,stubout_compare_func = None):
    """
    Validate the results against expected results and return 1 if all validate correctly otherwise return 
    """
    result = 1
    rs          = results[0]
    cmdout      = results[1]
    stubout     = results[2]
    exp_rs      = expected_results[0]
    exp_cmdout  = expected_results[1]
    exp_stubout = expected_results[2]

    cfunc = lambda e,a: e != a
    compare_function = cfunc if stubout_compare_func == None else stubout_compare_func

    # Validate expected results
    if int(rs) != int(exp_rs):
        result  = "*** RETURN STATUS DOES NOT MATCH ***\n"
        result += "Expected Return Status: %s, Actual Return Status: %s\n" % (str(exp_rs),str(rs))

    elif compare_function(exp_stubout, stubout):
        diffs   = getdiff(exp_stubout, stubout)
        result  = "*** STUB OUTPUT DOES NOT MATCH ***\n"
        result += diffs

    elif exp_cmdout != cmdout:
        line_sep = "\n--------------------------------------------\n"
        result   = "\n*** COMMAND OUTPUT DOES NOT MATCH ***\n\nExpected Output:\n%s%sActual Output:\n%s\n" % \
            (exp_cmdout, line_sep, cmdout)

    return result 

def run_cmd(cmd, args, stubout_file = None):
    """
    Run the specified command with arguments and pass the results back.
    If the everything passed then returns 1 else returns data.
    If the getdata flag is set then it will return the command output information and no validation is done.
    """
    # run command and redirect output to a temp log file
    rs      = os.system(cmd + ' ' + args + ' 1> %s 2> %s' % (CMD_OUTPUT, CMD_ERROR))
    cmdout  = get_output(CMD_OUTPUT)
    cmderr  = get_output(CMD_ERROR)
    stubout = get_output(stubout_file) if stubout_file is not None else ''
    return (rs, cmdout, stubout, cmderr)

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

def get_argsfile_list(args_list,args_path):
    """
    This function will get the files that contain the arguments to test
    """
    if args_list != None:
        retlist = [ args_path + args + ARGS_FILES[1:] for args in args_list]
    else:
        retlist = glob.glob(args_path+ARGS_FILES)
    return retlist

def gen_test(fd, cmd, tc_name, args, old_results, new_results, stubout_file, thook):
    """
    This function will do validation of the generated data and compare the expected outpus
    and then generate the test for the specified arguments
    """
    docstr  = '    %s test run: %s\n' % (cmd,tc_name)
    result  = 1
    if old_results:
        # redefine old_results to use the new return status 
        old_results = (new_results[0], old_results[1], old_results[2], old_results[3])
        result  = validate_results(old_results, new_results)
        cmdout  = old_results[1]
        stubout = old_results[2]
    else:
        # no old so use new
        cmdout  = new_results[1]
        stubout = new_results[2]


    if result != 1:
        docstr += indent(4,result)
        
    rs     = new_results[0] # need the new return status for generated test
    cmderr = new_results[3] # need the new command error output

    test = get_test(cmd, tc_name, docstr, args, rs, cmdout, stubout, stubout_file, thook, cmderr)

    fd.write(test)

def gen_sanity_test(fd, cmd, tc_name, args, new_results):
    """
    This function will a rs validation of the return status
    """
    rs      = new_results[0] # need the new return status for generated test
    cmdout  = new_results[1] # need the new command output for generated test
    cmderr  = new_results[3] 
    docstr  = '    %s test run: %s\n\n' % (cmd,tc_name,)
    docstr += indent(8,'Command Output:\n%s\nCommand Error/Debug:%s\n' % (cmdout, cmderr))
    test    = get_sanity_test(cmd, tc_name, docstr, args, rs)
    fd.write(test)

def skip_test(args_info , skip_list):
    """
    This function will return true if any of the skip strings are in the args_info
    """
    retstat = False
    if 'skip_list' in args_info:
        if set.intersection(set(args_info['skip_list']),set(skip_list)) != set([]):
            retstat = True

    return retstat

def gen_tests(opath, npath, args_path, args_list, stubout_file, skip_list):
    """
    write run the arguments are write the test data
    """
    argsfile_list = get_argsfile_list(args_list,args_path)

    # go through every client command file 
    for argsfile in argsfile_list:
        path_info   = os.path.split(argsfile)
        name        = getname(path_info[1])
        temp_module = path_info[1][:-3]
        os.system('cp %s %s.py' % (argsfile,temp_module))
        argsmod   = __import__(temp_module)

        fd = open('%s_test.py' % name,'w')

        # testutils module needs to be imported by the test file
        fd.write("import testutils\n")

        for args_info in argsmod.test_argslist:

            if skip_test(args_info, skip_list):
                continue

            (_name, old_cmd)   = getcmd(opath, args_info, name)
            (_name, new_cmd)   = getcmd(npath, args_info, name)
            tc_name   = args_info['tc_name']  # get the comment if there is one
            new_args  = args_info['args']
            thook     = args_info['testhook'] if 'testhook' in args_info else '' # get test hook
            new_only  = (args_info['new_only'] if 'new_only' in args_info else False) or (old_cmd == new_cmd)
            old_args  = args_info['old_args'] if 'old_args' in args_info else new_args
            save_testhook(thook)
            oresults  = None if new_only else run_cmd(old_cmd, old_args, stubout_file)
            nresults  = run_cmd(new_cmd, new_args, stubout_file)

            remove_testhook()
            gen_test(fd, _name, tc_name, new_args, oresults, nresults, stubout_file, thook)

        fd.close()
        os.system('rm %s.*' % temp_module)

def gen_sanity_tests(npath, args_path, args_list, skip_list):
    """
    write run the arguments are write the rs test data
    """
    argsfile_list = get_argsfile_list(args_list,args_path)

    # go through every client command file 
    for argsfile in argsfile_list:

        path_info   = os.path.split(argsfile)
        name        = getname(path_info[1])
        temp_module = path_info[1][:-3]
        os.system('cp %s %s.py' % (argsfile,temp_module))
        argsmod   = __import__(temp_module)

        fd = open('%s_sanity_test.py' % name,'w')

        # testutils module needs to be imported by the test file
        fd.write("import testutils\nimport os\nimport pwd")

        for args_info in argsmod.test_argslist:

            if skip_test(args_info, skip_list): 
                continue

            tc_name  = args_info['tc_name']  
            args     = args_info['args']

            (_name, cmd) = getcmd(npath, args_info, name)
            user  = pwd.getpwuid(os.getuid())[0] 
            _args = args.replace('<USER>', user)

            results  = run_cmd(cmd,_args)
            gen_sanity_test(fd, _name, tc_name, args, results)

        fd.close()
        os.system('rm %s.*' % temp_module)

def cb_path(option,opt_str,value,parser,*args):
    """
    This callback will validate the path and store it.
    """
    # validate the path
    if not os.path.isdir(value):
        print(os.getcwd())
        print("directory %s does not exist" % value)
        sys.exit(1)
    setattr(parser.values,option.dest,value) # set the option

def cb_skip_list(option,opt_str,value,parser,*args):
    """
    This callback will validate and get the skip list 
    """
    # Validate skip list
    try:
        skip_list = value.split(':')
        setattr(parser.values,option.dest,skip_list) # set the option
    except:
        print("Invalid skip list")
        sys.exit(1)

def main():
    """
    test_clients main function.
    """

    # list of callback with its arguments
    callbacks = [(cb_path, ()), (cb_skip_list, ())]

    parser = ArgParse(__doc__,callbacks)
    parser.parse_it() # parse the command line

    args_list  = parser.args if not parser.no_args() else None
    
    # go and generate the test
    opath     = parser.options.opath + '/' if parser.options.opath else ''
    npath     = parser.options.npath + '/' if parser.options.npath else ''
    tpath     = parser.options.tpath + '/' if parser.options.tpath else ''
    skip_list = parser.options.skip_list if parser.options.skip_list is not None else []
    if parser.options.sanity:
        gen_sanity_tests(npath, tpath, args_list, skip_list)
    elif parser.options.compare:
        gen_tests(opath, npath, tpath, args_list, parser. options.stubo, skip_list)
    else:
        print("Specify Type of Test")

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        print("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
