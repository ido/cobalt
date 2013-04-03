#!/usr/bin/env python
"""
Generate Tests

Usage: %prog [options] [argsfile1 ... argsfileN]

OPTIONS DEFINITIONS:

Option with no values:

'-o','--opath',dest='opath',type='string',help='path of old commands'
'-n','--npath',dest='npath',type='string',help='path of new commands'
'-t','--tpath',dest='tpath',type='string',default='test_data',help='path of test data (default: test_data/)'
'-s','--stubo',dest='stubo',type='string',default='stub.out',help='stub functions output file (default: stub.out)'

Option with values: None

"""
import os
import sys
import glob
import re
import difflib
from arg_parser import ArgParse

NEW_ONLY_TAG    = '<NEW_ONLY>'
CMD_OUTPUT      = 'cmd.out'
ARGS_FILES      = '*_args.txt'

# Template constants
DS  = '<DOCSTR>'
AR  = '<ARGS>'
CO  = '<CMDOUT>'
SO  = '<STUBOUT>'
RS  = '<RS>'
TQ  = '<TQ>'
TC  = '<TC_COMMENT>'
CM  = '<CMD>'
SF  = '<STUBFILE>'
ES  = '\\\n""""""' # empty string 
RTQ = '"""'

TEST_TEMPLATE = \
"""
# ---------------------------------------------------------------------------------
def test_<CMD>_<TC_COMMENT>():
    <TQ>
<DOCSTR>
    <TQ>

    args      = <TQ><ARGS><TQ>

    cmdout    = \\
<TQ><CMDOUT><TQ>

    stubout   = \\
<TQ><STUBOUT><TQ>

    stubout_file = "<STUBFILE>"

    expected_results = ( 
                       <RS>, # Expected return status 
                       cmdout, # Expected command output
                       stubout # Expected stub functions output
                       ) 

    results = testutils.run_cmd('<CMD>.py',args,stubout_file) 
    result  = testutils.validate_results(results,expected_results)

    correct = 1
    assert result == correct, "Result:\\n%s" % result

"""

# get command name
cn_p = re.compile(r'(.*)'+ARGS_FILES[1:])
getname = lambda fn: '' if cn_p.match(fn) == None else cn_p.sub(r'\1',fn)

# new_only comment lambda function defintion
ic_p = re.compile(r'(.*)#.*')
stripcomment = lambda data: ic_p.sub(r'\1',data)

# get comment lambda function definition
cm_p = re.compile(r'.*#.*<tc:(\w*)>.*')
getcomment = lambda data: '' if cm_p.match(data) == None else cm_p.sub(r'\1',data)

# get expected return status lambda function definition
rs_p = re.compile(r'.*#.*<rs:(\d*)>.*')
getrs = lambda data: '' if rs_p.match(data) == None else rs_p.sub(r'\1',data)

# indent buffer
indent = lambda x,buf:'\n'.join([(x*' ')+line for line in buf.split('\n')])

def gettest(cmd,tc_comment,docstr,args,retstat,cmdout,stubout,stubout_file):
    """
    Get Test from template with all tags replace
    """
    return TEST_TEMPLATE.replace(CM,cmd).replace(TC,tc_comment).replace(TQ,RTQ).    \
        replace(DS,docstr).replace(AR,args).replace(CO,cmdout).replace(SO,stubout). \
        replace(RS,str(retstat)).replace(ES,"''").replace(SF,stubout_file)

def get_output(filename):
    """
    get output from the specified filename. delete file after getting the data
    """
    output = ''
    if os.path.isfile(filename):
        fd = open(filename,'r')
        output = fd.read()
        fd.close()
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
    retstat     = results[0]
    cmdout      = results[1]
    stubout     = results[2]
    exp_retstat = expected_results[0]
    exp_cmdout  = expected_results[1]
    exp_stubout = expected_results[2]

    # Validate expected results
    if int(retstat) != int(exp_retstat):
        result  = "*** RETURN STATUS DOES NOT MATCH ***\n"
        result += "Expected Return Status: %s, Actual Return Status: %s\n" % (str(exp_retstat),str(retstat))

    elif exp_stubout:
        cfunc = lambda e,a: e != a
        compare_function = cfunc if stubout_compare_func == None else stubout_compare_function
        if compare_function(exp_stubout,stubout):
            diffs   = getdiff(exp_stubout,stubout)
            result  = "*** STUB OUTPUT DOES NOT MATCH ***\n"
            result += diffs

    elif exp_cmdout:
        if exp_cmdout != cmdout:
            diffs   = getdiff(exp_cmdout,cmdout)
            result  = "*** COMMAND OUTPUT DOES NOT MATCH ***\n"
            result += diffs

    return result 

def run_cmd(cmd, args, stubout_file):
    """
    Run the specified command with arguments and pass the results back.
    If the everything passed then returns 1 else returns data.
    If the getdata flag is set then it will return the command output information and no validation is done.
    """
    # run command and redirect output to a temp log file
    retstat = os.system(cmd + ' ' + args + '&> %s' % CMD_OUTPUT)
    cmdout  = get_output(CMD_OUTPUT)
    stubout = get_output(stubout_file)
    return (retstat,cmdout,stubout)

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
        retlist = [ args_path + args + '_args.txt' for args in args_list]
    else:
        retlist = glob.glob(args_path+ARGS_FILES)
    return retlist

def gentest(fd, cmd, tc_comment, args, old_results, new_results, stubout_file):
    """
    This function will do validation of the generated data and compare the expected outpus
    and then generate the test for the specified arguments
    """
    docstr  = '    %s test run: %s\n' % (cmd,tc_comment)
    result  = 1
    if old_results:
        docstr += '        Old Command Output:\n' + indent(10,old_results[1])
        # redefine old_results to use the new return status and command output
        old_results = (new_results[0], new_results[1], old_results[2])
        result  = validate_results(old_results, new_results)
        stubout = old_results[2] # need the old command stub output for generated test
    else:
        stubout = new_results[2] # no old so use new

    if result != 1:
        docstr += indent(4,result)
        
    retstat = new_results[0] # need the new return status for generated test
    cmdout  = new_results[1] # need the new command output for generated test

    test = gettest(cmd,tc_comment,docstr,args,retstat,cmdout,stubout,stubout_file)

    fd.write(test)

def gentests(opath,npath,args_path,args_list,stubout_file):
    """
    write run the arguments are write the test data
    """
    argsfile_list = get_argsfile_list(args_list,args_path)

    # go through every client command file 
    for argsfile in argsfile_list:
    
        argslist = getlines(argsfile) # get the list of command line arguments 
        path_info = os.path.split(argsfile)
        name      = getname(path_info[1])

        old_cmd = "%s%s.py" % (opath,name)
        new_cmd = "%s%s.py" % (npath,name)

        fd = open('%s_test.py' % name,'w')

        # testutils module needs to be imported by the test file
        fd.write("import testutils\n")

        for args in argslist:
            if args    == '' : continue # skip null line
            if args[0] == '#': continue # skip comment line
            tc_comment = getcomment(args) # get the comment if there is one
            new_only   = args.find(NEW_ONLY_TAG) != -1 or old_cmd == new_cmd # only new command applies not old
            args       = stripcomment(args).split('|') # strip out comments
            #
            # if there are two args then old command is different arg for same functionality
            if len(args) == 2:
                old_args = args[0].strip()
                new_args = args[1].strip()
            else:
                old_args = args[0].strip()
                new_args = args[0].strip()
            # flag new command only
            if new_only:
                oresults = None
            else:
                oresults = run_cmd(old_cmd,old_args,stubout_file)
            nresults = run_cmd(new_cmd,new_args,stubout_file)
            gentest(fd, name, tc_comment, new_args, oresults, nresults, stubout_file)
        fd.close()

def main():
    """
    test_clients main function.
    """
    parser = ArgParse(__doc__,None)
    parser.parse_it() # parse the command line

    args_list  = parser.args if not parser.no_args() else None
    
    # go and generate the test
    opath = parser.options.opath + '/' if parser.options.opath else ''
    npath = parser.options.npath + '/' if parser.options.npath else ''
    tpath = parser.options.tpath + '/'
    gentests(opath,npath,tpath,args_list,parser.options.stubo)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except:
        print("*** FATAL EXCEPTION: %s ***",str(sys.exc_info()))
        raise
