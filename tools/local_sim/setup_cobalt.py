#!/usr/bin/env python
"""
This python script will setup the cobalt brooklyn sim 

Usage: %prog [options]

OPTIONS DEFINITIONS:

'-c','--cobalt', dest='cobalt', default='cobalt', help='Cobalt repo name'
'-b','--branch', dest='branch', default='develop', help='Branch to clone from'
'-s','--sim-path', dest='sim_path', default='./', help="Path of the cobalt simulation environment'
'-n','--name', dest='sysroot', default='sysroot-brooklyn', help name of the system root directory'
"""
import os
from arg_parser import ArgParse

def main():
    """
    setup Cobalt Brooklyn sim
    """
    parser = ArgParse(__doc__)
    parser.parse_it() # parse the command line

    os.chdir(parser.options.sim_path)
    
    # clone the repo
    os.system('git clone -b %s git://git.mcs.anl.gov/cobalt.git %s' % (parser.options.branch, parser.options.cobalt))

    os.mkdir(parser.options.sysroot)
    os.mkdir(parser.options.sysroot + 'etc')
    os.mkdir(parser.options.sysroot + 'var')
    os.mkdir(parser.options.sysroot + 'tmp')
    
    local_sim = parser.options.cobalt + '/tools/local_sim/'
    os.system('cp %s/simulator.xml .'         % local_sim)
    os.system('cp %s/cstart.sh     .'         % local_sim)
    os.system('cp %s/cinit.sh      .'         % local_sim)
    os.system('cp %s/cobalt.conf    %s/etc/'  % (parser.options.sysroot))
    os.system('cp %s/partlist-*.txt %s/etc/'  % (parser.options.sysroot))
    os.system('cp %/stest-*.py      %s/etc/'  % (parser.options.sysroot))

    os.system('ln -s %s/src/lib %s/src/Cobalt')
