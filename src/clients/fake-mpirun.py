#!/usr/bin/env python

'''Cobalt fake mpirun'''
__revision__ = ''
__version__ = '$Version$'

import getopt, os, pwd, sys, time, xmlrpclib, logging
import Cobalt.Logging, Cobalt.Util
from Cobalt.Proxy import ComponentProxy, ComponentLookupError

usehelp = "Usage:\nfake-mpirun [--version] [-h] <mpirun arguments>"

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "fake-mpirun %s" % __revision__
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
    
        
    level = 30
    if '-d' in sys.argv:
        level = 10

    Cobalt.Logging.setup_logging('fake-mpirun', to_syslog=False, level=level)
    logger = logging.getLogger('fake-mpirun')

    try:
        os.environ["COBALT_JOBID"] = os.environ["COBALT_JOBID"]
    except KeyError:
        logger.error("fake-mpirun must be invoked by a script submitted to cobalt.")
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
        logger.error("Error: fake-mpirun's parent is in state '%s' and has not specified a partition." % j['state'])
        raise SystemExit, 1
#    j['location'] = "ANLR00"
    
    arglist += ['-partition', j['location']]
    
    
    if "-np" in sys.argv:
        idx = sys.argv.index("-np")
    elif "-n" in sys.argv:
        idx = sys.argv.index("-n")
    elif "-nodes" in sys.argv:
        idx = sys.argv.index("-nodes")
    else:
        idx = -1
     
    if idx > 0:
        if int(sys.argv[idx+1]) > int(j['procs']):
            logger.error("Error: tried to request more processors (%s) than reserved (%s)." % (sys.argv[idx+1], j['procs']))
            raise SystemExit, 1
        
    user = pwd.getpwuid(os.getuid())[0]

    jobspec = {'jobid':int(os.environ["COBALT_JOBID"]), 'user':user, 'true_mpi_args':arglist, 'walltime':j['walltime'], 'args':[], 'location':j['location'], 'outputdir':j['outputdir']}
    try:
        cqm = ComponentProxy("queue-manager", defer=False)
        system = ComponentProxy("system", defer=False)

        # try adding job to queue_manager
        pgid = cqm.invoke_mpi_from_script(jobspec)
        
        # give the process a chance to get started before we check for it
        time.sleep(10)
        while True:
            r = system.get_process_groups([{'id':pgid, 'state':'*'}])
            state = r[0]['state']
            if state == 'running':
                time.sleep(5)
                continue
            else:
                break
        print "process group %s has completed" % (pgid)
        result = system.wait_process_groups([{'id':pgid, 'exit_status':'*'}])
        
        raise SystemExit, result[0].get('exit_status')
        

    except ComponentLookupError:
        logger.error("Can't connect to the process manager")
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


