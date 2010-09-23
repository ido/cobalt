#!/usr/bin/env python -W ignore::DeprecationWarning

'''Cobalt mpirun'''
__revision__ = ''
__version__ = '$Version$'

import getopt, os, pwd, sys, time, xmlrpclib, logging
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

usehelp = "Usage:\ncobalt-mpirun [--version] [-h] <mpirun arguments>"

if __name__ == '__main__':
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
        
        raise SystemExit, 0
    try:
        idx = sys.argv.index("-partition")
        arglist = sys.argv[1:idx] + sys.argv[idx+2:]
        print "NOTE: the -partition option should not be used, as the job"
        print "will run in the partition reserved by cobalt."
    except ValueError:
        arglist = sys.argv[1:]

    # these flags (which all take an argument) should not be passed to the real mpirun
    bad_args = ["-host", "-backend", "-shape"]
    for a in bad_args:
        try:
            idx = arglist.index(a)
            arglist = arglist[0:idx] + arglist[idx+2:]
            print "NOTE: the %s option should not be used." % a
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

    try:
        cqm = ComponentProxy("queue-manager", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to queue manager"
        sys.exit(1)
        
    response = cqm.get_jobs([{'tag':'job', 'jobid':int(os.environ["COBALT_JOBID"]), 'state':'*', 'procs':'*', 'location':'*', 'walltime':'*', 'outputdir':'*'}])
    if len(response) == 0:
        logger.error("Error: cqm did not find a job with id " + os.environ["COBALT_JOBID"])
        raise SystemExit, 1
    if len(response) > 1:
        logger.error("Error: cqm did not find a unique job with id " + os.environ["COBALT_JOBID"])
        raise SystemExit, 1
         
    j = response[0]
    if j['location'] is None:
        logger.error("Error: cobalt-mpirun's parent is in state '%s' and has not specified a partition." % j['state'])
        raise SystemExit, 1
#    j['location'] = "ANLR00"
    
    arglist = ['-partition', j['location'][0]] + arglist

    # update the current working directory, if not specified on the command line
    # however, mpirun -free gets angry if you specify -cwd, so check for that    
    if "-cwd" not in arglist and "-free" not in arglist:
        arglist = ['-cwd', os.getcwd()] + arglist

    # Add cobalt jobid environment variable to script job, but again, not to be used
    # along with mpirun -free
    if "-free" not in arglist:
        arglist = ['-env', 'COBALT_JOBID='+os.environ["COBALT_JOBID"]] + arglist
    
    if "-np" in sys.argv:
        idx = sys.argv.index("-np")
    elif "-n" in sys.argv:
        idx = sys.argv.index("-n")
    elif "-nodes" in sys.argv:
        idx = sys.argv.index("-nodes")
    else:
        idx = -1
     
    if idx > 0:
        if int(sys.argv[idx+1]) > (int(j['procs']) * 4):
            logger.error("Error: tried to request more processors (%s) than reserved (%s)." % (sys.argv[idx+1], j['procs']))
            raise SystemExit, 1
        
    user = pwd.getpwuid(os.getuid())[0]

    jobspec = {'jobid':int(os.environ["COBALT_JOBID"]), 'user':user, 'true_mpi_args':arglist, 
               'walltime':j['walltime'], 'args':[], 'location':j['location'], 'outputdir':j['outputdir'], }
    for key in io_redirect:
        if io_redirect[key]:
            jobspec.update({key: io_redirect[key]})
               
    try:
        scriptm = ComponentProxy("script-manager", defer=False)
        system = ComponentProxy("system", defer=False)

        # try adding job to queue_manager
        pgid = int(scriptm.invoke_mpi_from_script(jobspec))
        
        # give the process a chance to get started before we check for it
        start = time.time()
        while True:
            r = system.get_process_groups([{'id':pgid, 'state':'*'}])
            if r:
                break
            
            # we'll give it 90 seconds to get started
            if time.time() - start > 90:
                break
            
            time.sleep(5)
        
        while True:
            r = system.get_process_groups([{'id':pgid, 'state':'*'}])
            if r and r[0]['state'] == 'running':
                time.sleep(5)
                continue
            else:
                break
        print "process group %s has completed" % (pgid)
        result = system.wait_process_groups([{'id':pgid, 'exit_status':'*'}])
        
        raise SystemExit, result[0].get('exit_status')
        

    except ComponentLookupError:
        logger.error("Trouble communicating with Cobalt components")
        raise SystemExit, 1
#    except xmlrpclib.Fault, flt:
#        if flt.faultCode == 31:
#            logger.error("System draining. Try again later")
#            raise SystemExit, 1
#        elif flt.faultCode == 30:
#            logger.error("Job submission failed because: \n%s\nCheck 'cqstat -q' and the cqstat manpage for more details." % flt.faultString)
#            raise SystemExit, 1
#        elif flt.faultCode == 1:
#            logger.error("Job submission failed due to queue-manager failure")
#            raise SystemExit, 1
#        else:
#            logger.error("Job submission failed")
#            logger.error(flt)
#            raise SystemExit, 1
#     except:
#         logger.error("Error submitting job")
#         raise SystemExit, 1


