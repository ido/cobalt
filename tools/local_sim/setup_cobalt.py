#!/usr/bin/env python
"""
This python script will setup the cobalt brooklyn sim by getting the cobalt repo and setting up all the files needed.

Usage: %prog [options]

OPTIONS DEFINITIONS:

'-r','--repo', dest='repo', default='git://git.mcs.anl.gov/cobalt.git',help='Cobalt Repo to clone from'
'-c','--cobalt', dest='cobalt', default='cobalt', help='Name of the dir to clone the cobalt repo. Only use with --create option'
'-s','--sim-path', dest='sim_path', default='./', help='Path of the cobalt simulation environment. Only use with --create option'
'-b','--branch',dest='branch', default='master', help='name of branch to clone from. Only use with --create option'
'--skip-clone', dest='skip_clone', action='store_true', help='if specified it will skip cloning the repo'
"""
import os
import sys
import subprocess
from arg_parser import ArgParse

COBALT_SETUP = \
"""
export COBALT_SOURCE_DIR="<SIMPATH>"/cobalt
export COBALT_RUNTIME_DIR="<SIMPATH>"/sysroot-brooklyn
export COBALT_SYSTEM_TYPE=BGSIM
export COBALT_CONFIG_FILES="$COBALT_RUNTIME_DIR"/etc/cobalt.conf
if test -z "${PATH_BASIS}" ; then
    export PATH_BASIS="$PATH"
fi
export PATH="${COBALT_SOURCE_DIR}"/src/clients:"${COBALT_SOURCE_DIR}"/src/clients/POSIX:$PATH_BASIS
export PYTHONPATH="$COBALT_SOURCE_DIR/src":$COBALT_SOURCE_DIR/testsuite
export COBALT_SIM="<SIMPATH>"

alias cobalt-client-sim='source "<SIMPATH>"/cobalt_client_setup'
alias cobalt-brooklyn-sim='source "<SIMPATH>"/cobalt_setup'
alias cobalt-reset-sim='source "<SIMPATH>"/rm_cobalt_testlinks; source "<SIMPATH>"/cobalt_setup'
alias cobalt-stop='kill `cat "<SIMPATH>"/sysroot-brooklyn/var/run/cobalt/*`'
alias cobalt-clean='rm -rf "<SIMPATH>"/sysroot-brooklyn/var'
"""

COBALT_CLIENT_SETUP = \
"""
export PYTHONPATH="$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/
export PYTHONPATH="$PYTHONPATH":"$COBALT_SOURCE_DIR"/src
export PYTHONPATH="$PYTHONPATH":"$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib

cd "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients

rm -rf testlib/Components
rm -rf Cobalt

ln -fs "$COBALT_SOURCE_DIR"/src/lib/client_utils.py  testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/Exceptions.py    testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/Logging.py       testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/JSONEncoders.py  testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/arg_parser.py    testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/Util.py          testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/__init__.py      testlib/
ln -fs "$COBALT_SOURCE_DIR"/src/lib/Components       testlib/
ln -fs testlib                                       Cobalt
"""

RM_COBALT_TESTLINKS = \
"""
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/client_utils.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/Exceptions.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/Logging.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/JSONEncoders.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/arg_parser.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/Util.py
rm "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/__init__.py
rm -rf "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/testlib/Components
rm -rf "$COBALT_SOURCE_DIR"/testsuite/TestCobaltClients/Cobalt
"""

def main():
    """
    setup Cobalt Brooklyn sim
    """
    parser = ArgParse(__doc__)
    parser.parse_it() # parse the command line

    sysroot = 'sysroot-brooklyn'

    def create_bsim():
        if os.path.exists(parser.options.sim_path):
            if not os.path.isdir(parser.options.sim_path):
                print >> sys.stderr, "Sim path %s exists but not a directory" % parser.options.sim_path
                sys.exit(1)
        else:
            if os.path.isdir(os.path.dirname(parser.options.sim_path)):
                os.mkdir(parser.options.sim_path)
            else:
                print >> sys.stderr, "Parent %s not a directory" % os.path.dirname(parser.options.sim_path)
                sys.exit(1)

        os.chdir(parser.options.sim_path)
        curr_dir = os.getcwd()
        
        cdir  = parser.options.cobalt
        crepo = parser.options.repo

        if not parser.options.skip_clone:
            subprocess.call(('git','clone', '-b', parser.options.branch, crepo, cdir))

        os.mkdir(sysroot)
        os.mkdir(sysroot + '/etc')
        os.mkdir(sysroot + '/var')
        os.mkdir(sysroot + '/tmp')

        sysroot_etc = '%s/etc/' % sysroot
        local_sim   = parser.options.cobalt + '/tools/local_sim/'
        subprocess.call(('cp','%s/simulator.xml' % local_sim, '.'))
        subprocess.call(('cp','%s/cstart.sh'     % local_sim, '.'))
        subprocess.call(('cp','%s/cinit.sh'      % local_sim, '.'))
        subprocess.call(('cp','%s/cobalt.key'    % local_sim, sysroot_etc))
        subprocess.call(('cp','%s/cobalt.cert'   % local_sim, sysroot_etc))

        subprocess.call( ('cp', '%s/cobalt.conf' % local_sim, sysroot_etc))

        files = os.listdir(local_sim)

        for _file in files:
            if _file.find('partlist-') != -1 or _file.find('stest-') != -1:
                subprocess.call(('cp', local_sim+'/'+_file, sysroot_etc))

        cobalt_dir = parser.options.cobalt
        subprocess.call( ('ln', '-s', 'lib', '%s/src/Cobalt' % cobalt_dir) )

        os.chdir(cobalt_dir+'/src/components')
        subprocess.call( ('ln', '-s', '../../../simulator.xml', 'simulator.xml') )

        os.chdir('../../../'+sysroot_etc)
        subprocess.call(('ln', '-s', 'partlist-R00-R01.txt', 'partlist.txt'))

        os.chdir(curr_dir)
        fd = open('cobalt_setup','w')
        fd.write(COBALT_SETUP.replace('<SIMPATH>', curr_dir))
        fd.close()
        fd = open('cobalt_client_setup','w')
        fd.write(COBALT_CLIENT_SETUP.replace('<SIMPATH>', curr_dir))
        fd.close()
        fd = open('rm_cobalt_testlinks','w')
        fd.write(RM_COBALT_TESTLINKS.replace('<SIMPATH>', curr_dir))
        fd.close()

    create_bsim()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception, e:
        print("*** FATAL EXCEPTION: %s ***" % e)
        sys.exit(1)
