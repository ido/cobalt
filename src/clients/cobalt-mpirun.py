#!/usr/bin/env python

'''Cobalt mpirun

This mediates the execution of an mpirun on behalf of a user running a script
job.  When invoked, the script expects the following environment variables:

    COBALT_NODEFILE
    COBALT_JOBID
    COBALT_RESID
    COBALT_PAETNAME
    COBALT_JOBSIZE

Once invoked, this will handle argument mapping to mpirun.


'''
__revision__ = ''
__version__ = '$Version$'

import getopt
import os 
import pwd
import sys
import time
import xmlrpclib
import logging
import ConfigParser

import Cobalt.Logging
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
from Cobalt import CONFIG_FILES
import Cobalt.Util

usehelp = "Usage:\ncobalt-mpirun [--version] [-h] <mpirun arguments>"

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILES)

def get_config_entry(section, option, default=None):

    if not config.has_section(section):
        return default
    try:
        value = config.get(section,option)
    except ConfigParser.NoOptionError:
        value = default
    return value

def check_env(env_name):
    try:
        os.environ[env_name]
    except KeyError:
        print >> sys.stderr, "Environment variable %s expected, but not found! Aborting." % env_name
        sys.exit(1)


if __name__ == '__main__':

    #RUNNING AS COBALT GROUP:
    if '--version' in sys.argv:
        print "cobalt-mpirun %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0
    if '-h' in sys.argv:
        print usehelp
        print """\
        
        This program is meant to be called from scripts submitted to 
        run using the cobalt queueing system.  It takes all of the same arguments
        as the system mpirun, but suppresses the -partition argument.  This
        argument will be set by the queueing system once it has decided where
        to run your job.
        """
        
        raise SystemExit, 1
    try:
        idx = sys.argv.index("-partition")
        arglist = sys.argv[1:idx] + sys.argv[idx+2:]
        print >> sys.stderr, "NOTE: the -partition option should not be used, as the job"
        print >> sys.stderr, "will run in the partition reserved by cobalt."
    except ValueError:
        arglist = sys.argv[1:]


    #NOTE: validation of jobid, resid, and partition information is being handled
    #by the scheduler library that mpirun includes.  I'm not sure if we should
    #do some sort of attempted internal validation --PMR
    expected_envs = ["COBALT_JOBID", "COBALT_PARTNAME", "COBALT_PARTSIZE"]

    run_cmd = get_config_entry("bgpm", "mpirun", None)
    if run_cmd == None:
        print >> sys.stderr, "FATAL: cobalt.conf entry for mpirun not found.  Aborting run."
        sys.exit(1)

    for expected_env in expected_envs:
        #if this check fails, the program will abort
        check_env(expected_env)

    #setgid as user:
    try:
        user = pwd.getpwuid(os.getuid()).pw_name
    except:
        print >> sys.stderr, "FATAL: failed to find a legitimate uid."
        sys.exit(1)
    try:        
        os.setgid(pwd.getpwnam(user).pw_gid)
    except OSError:
        print >> sys.stderr, "FATAL: failed to reset group" 
        sys.exit(1)



    #BEYOND THIS POINT, RUNNING AS USER'S GID


    # these flags (which all take an argument) should not be passed to the real mpirun
    bad_args = ["-host", "-backend", "-shape"]
    for a in bad_args:
        try:
            idx = arglist.index(a)
            arglist = arglist[0:idx] + arglist[idx+2:]
            print >> sys.stderr, "NOTE: the %s option should not be used." % a
        except ValueError:
            pass
    
    my_args = ["stdin", "stdout", "stderr"]
    io_redirect = {}
    for a in my_args:
        try:
            idx = arglist.index("--" + a)
            value = arglist[idx+1]
            io_redirect[a] = value
            arglist = arglist[0:idx] + arglist[idx+2:]
        except ValueError:
            io_redirect[a] = None

    level = 30
    if '-d' in sys.argv:
        level = 10

    Cobalt.Logging.setup_logging('cobalt-mpirun', to_syslog=False, level=level)
    logger = logging.getLogger('cobalt-mpirun')

    try:
        os.environ["COBALT_JOBID"] = os.environ["COBALT_JOBID"]
    except KeyError:
        logger.error("cobalt-mpirun must be invoked by a script submitted to cobalt.")
        raise SystemExit, 1

    arglist = ['-partition', os.environ["COBALT_PARTNAME"]] + arglist

    # update the current working directory, if not specified on the command line
    # however, mpirun -free gets angry if you specify -cwd, so check for that    
    if "-cwd" not in arglist and "-free" not in arglist:
        arglist = ['-cwd', os.getcwd()] + arglist


    # Add cobalt jobid environment variable to script job, but again, not to be used
    # along with mpirun -free
    env_str = ''
    if '-env' in arglist:
        env_str = arglist[arglist.index("-env") + 1]
        arglist.remove(env_str)
        arglist.remove('-env')

    if "-free" not in arglist:
        cobalt_env_str = "COBALT_JOBID=%s" % os.getenv("COBALT_JOBID")
    
    if os.environ.has_key("COBALT_RESID"):
        cobalt_env_str = cobalt_env_str + ":COBALT_RESID=%s" % os.environ["COBALT_RESID"]
    if os.environ.has_key("COBALT_JOB_ENVS"):
        cobalt_env_str = cobalt_env_str + ":" + os.environ("COBALT_JOB_ENVS")

    env_str = env_str + cobalt_env_str

    #if "-free" not in arglist:
    #    arglist = ['-env', 'COBALT_JOBID='+os.environ["COBALT_JOBID"]] + arglist
    
    if env_str != '':
        arglist = ['-env', env_str] + arglist

    if "-np" in sys.argv:
        idx = sys.argv.index("-np")
    elif "-n" in sys.argv:
        idx = sys.argv.index("-n")
    elif "-nodes" in sys.argv:
        idx = sys.argv.index("-nodes")
    else:
        idx = -1
     
    if idx > 0:
        if int(sys.argv[idx+1]) > (int(os.environ["COBALT_PARTSIZE"]) * 4):
            logger.error("Error: tried to request more processors (%s) than reserved (%s)." % \
                    (sys.argv[idx+1], int(os.environ["COBALT_PARTSIZE"]) * 4))
            raise SystemExit, 1
        
    for key in io_redirect:
        if io_redirect[key]:
            jobspec.update({key: io_redirect[key]})

    #don't fork, just exec. Keep the PID the same for user scripts (?)
    arglist.insert(0, run_cmd)
    try:
        os.execvpe(run_cmd, arglist, os.environ)
    except Exception, e:
        print >> sys.stderr, "error executing %s" % opt.executable
        print >> sys.stderr, e
        sys.exit(1)


