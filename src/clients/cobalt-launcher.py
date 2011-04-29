#!/usr/bin/env python

import sys
import os
import optparse
import re

if __name__ == '__main__':
    p = optparse.OptionParser()
    
    p.add_option("--cwd", action="store", dest="cwd", help="current working directory to use")
    p.add_option("--jobid", action="store", dest="jobid", help="jobid")
    p.add_option("--nf", action="store", dest="nodefile", help="nodefile")
    p.add_option("--exe", action="store", dest="executable", help="executable path")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)
        
    opt, args = p.parse_args(sys.argv[:9])
    
    args = sys.argv[9:]

    os.environ['COBALT_JOBID'] = opt.jobid
    os.environ['COBALT_NODEFILE'] = opt.nodefile

    os.chdir(opt.cwd)
    
    #assume rest of args are to go to the executable and have the user script deal with it
    arg_tuple = (opt.executable, ) + tuple(args)

    try:
        os.execvpe(opt.executable, arg_tuple, os.environ)
    except Exception, e:
        print >> sys.stderr, "error executing %s" % opt.executable
        print >> sys.stderr, e
