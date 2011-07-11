#!/usr/bin/env python

'''This script simulates the standard bridge mpirun for brooklyn'''

import signal, sys, Cobalt.Proxy, time, datetime, math, os, random
import Cobalt.Util

def timestamp():
    now = datetime.datetime.now()
    stamp = "<" + now.strftime("%h %m ") + now.time().isoformat() + ">"
    return stamp

def signal_handler(signum, frame):
    print >> sys.stderr, timestamp() + " BE_MPI (ERROR): Received SIGTERM"
    print >> sys.stderr, timestamp() + " BE_MPI (Info) : Cleaning up"
    try:
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : Destroying partition " + partition + " (nuke)"
        brooklyn.ReleasePartition(partition)
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : Partition " + partition + " switched to state FREE ('F')"
    except:
        print "BE_MPI (ERROR): Failure destroying partition " + partition
        print "BE_MPI (ERROR): You will have to restart brooklyn.py"

    print >> sys.stderr, timestamp() + " BE_MPI (Info) : ==    BE completed   =="
    print >> sys.stderr, timestamp() + " FE_MPI (ERROR): Failure list:"
    print >> sys.stderr, timestamp() + " FE_MPI (ERROR):   - 1. Job was killed by SIGTERM"
    print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
    print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   1 =="
    raise SystemExit, 1

signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    for flag in ['-partition', '-np', '-mode']:
        if flag not in sys.argv[1:]:
            print >> sys.stderr, "ERROR: %s is a required flag" % (flag)
            raise SystemExit, 1
    partition = sys.argv[sys.argv.index('-partition') + 1]
    mode = sys.argv[sys.argv.index('-mode') + 1]
    size = int(sys.argv[sys.argv.index('-np') + 1])
    if mode == 'vn':
        size = int(math.ceil(float(size) / 2))
   
    print "ENVIRONMENT"
    print "-----------"
    for envvar in os.environ.keys():
        print envvar + "=" + os.environ[envvar]

    print
    print >> sys.stderr, timestamp() + " FE_MPI (Info) : Initializing MPIRUN"    

    try:
        brooklyn = Cobalt.Proxy.system()
    except:
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR): East River transit failure: bridge is missing"
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR): Terminating due to asphyxia"
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR): Failure list:"
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR):   - 1. Job execution failed - job switched to an error state (simulator not running?)"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   1 =="
        raise SystemExit, 1

    walltime = 0

    try:
        jobid = os.environ["COBALT_JOBID"]
        bjobid = int(jobid) + 1024   # Why not?
        try:
            cqm = Cobalt.Proxy.queue_manager()
            query =  [{'tag':'job', 'user':'*', 'walltime':'*', 'jobid':jobid}]
            response = cqm.GetJobs(query)
            for j in response:
                pct = float(os.environ.get("OVERTIME_FRAC", 0))
                if random.random() < pct:
                    walltime = float(j['walltime']) * 60 * 2.0
                else:
                    walltime = float(j['walltime']) * 60 * 0.9
        except Cobalt.Proxy.CobaltComponentError:
            print >> sys.stderr, timestamp() + " FE_MPI (Info) : Failed to connect to queue manager"
            print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
            print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   1 =="
            raise SystemExit, 1
    except:
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : COBALT_JOBID not found, can't determine runtime"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Using first argument of job instead"
        
        walltime = int(sys.argv[sys.argv.index('-args') + 1]) * 60

        bjobid = 99999  # Why not, indeed
        
    stat = brooklyn.ReservePartition(partition, size)
    if not stat:
        print >> sys.stderr, timestamp() + " BE_MPI (ERROR): Failed to run process on partition"
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : ==    BE completed   =="
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR): Failure list:"
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR):   - 1. Job execution failed - job switched to an error state (failure #42)"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   1 =="
        raise SystemExit, 1

    try:
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Adding job"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Job added with the following id: " + str(bjobid)
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Simulated job will terminate in " + str(walltime) + " seconds"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Waiting for job to terminate"
        # Some stuff for the stdout stream
        print "Running job with args: " + str(sys.argv)
        print "Sleeping for " + str(walltime) + " seconds"
        sys.stdout.flush()
        Cobalt.Util.sleep(walltime)
        print "Wake up!  Time to die!"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Job " + str(bjobid) + " switched to state TERMINATED ('T')"
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : Job sucessfully terminated"
    except:
        print >> sys.stderr, timestamp() + " FE_MPI (ERROR): Job run failure of some sort; may have been killed"
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : Destroying partition " + partition
        pct = float(os.environ.get("FAILED_RELEASE_FRAC", 0))
        if random.random() < pct:
            pass
        else:
            brooklyn.ReleasePartition(partition)
            print >> sys.stderr, timestamp() + " BE_MPI (Info) : Partition " + partition + " switched to state FREE ('F')"
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : ==    BE completed   =="
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
        print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   1 =="
        raise SystemExit, 1

    print >> sys.stderr, timestamp() + " BE_MPI (Info) : Destroying partition " + partition
    pct = float(os.environ.get("FAILED_RELEASE_FRAC", 0))
    if random.random() < pct:
        pass
    else:
        brooklyn.ReleasePartition(partition)
        print >> sys.stderr, timestamp() + " BE_MPI (Info) : Partition " + partition + " switched to state FREE ('F')"
    print >> sys.stderr, timestamp() + " BE_MPI (Info) : ==    BE completed   =="
    print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==    FE completed   =="
    print >> sys.stderr, timestamp() + " FE_MPI (Info) : ==  Exit status:   0 =="


