#!/usr/bin/env python

"""Queue Simulator executable."""

import inspect 
import sys

import Cobalt.Util
from Cobalt.Components.qsim import Qsimulator 
from Cobalt.Components.base import run_component
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.qsim import Qsimulator

__helpmsg__ = "Usage: qsim -j <jobworkload> -p <partition.xml> [--output=<outputlogfile>]\n" +\
        "[--weibull --scale=<scale> --shape=<shape>]  [--failurelog=<failurelog>]\n" +\
        "[--fautlaware --sensitivity=sensitivity --specificity=specificity]\n" +\
        "[--standalone]  [--profile]"

class my_bgsched (BGSched):
    def do_tasks (self):
        for name, func in inspect.getmembers(self, callable):
            if getattr(func, "automatic", False):
                func() 
        
def integrated_main(opts):
    '''run instantiated qsim, together with bgsched, slp,scriptm in one process'''
    TimingServiceLocator()
    ScriptManager()
    qsim = Qsimulator(**opts)
    bgsched = my_bgsched()
    while not qsim.is_finished():
        bgsched.do_tasks()
        
def standalone_main(opts):
    '''run qsim in standalone manner, communicate with other components via socket'''
    print opts['workload']
    print opts['config_file']
    try:
        run_component(Qsimulator, register=True, 
                     cls_kwargs=opts, extra_getopt = ':j:p')
    except KeyboardInterrupt:
        sys.exit(1)
        
def profile_main(opts):
    '''profile integrated qsim'''
    import hotshot, hotshot.stats
    prof = hotshot.Profile("qsim.profile")
    prof.runcall(integrated_main, opts)
    
if __name__ == "__main__":
    
    options = {'weibull':'weibull', 'faultaware':'faultaware',
               'standalone':'standalone', 'profile':'profile'}
    doptions = {'j':'workload', 'p':'config_file', 'failurelog':'failurelog',
                'scale':'scale', 'shape':'shape', 'P': 'policy',
                'sensitivity':'sensitivity', 'specificity':'specificity',
                'output':'outputlog'}

    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)
    
    if not opts['workload'] or not opts['config_file']:
        print "Error: Please specify job work load file path and partition.xml file path!"
        print __helpmsg__
        sys.exit()
        
    if opts['weibull']:
        if opts['failurelog']:
            print "Error: you can use Either failure_log Or weibull distribution to simulate failures, specify one of them"
            print __helpmsg__
            sys.exit()
        
        if not opts['scale'] or not opts['shape']:
            print "Warning: 'scale' and 'shape' parameters not specified,"
            print "use default scale=2,000,000 shape=0.8"
            raw_input("Press Enter to continue ")
    
    if opts['faultaware']:
        if not opts['failurelog'] and not opts['weibull']:
            print "Error: fault-aware simulation, please specify failure-log path OR weibull parameters"
            print __helpmsg__
            sys.exit()
        if not opts['sensitivity'] or not opts['specificity']:
            print "Warning: 'sensitivity' and 'specificity' parameters not specified,"
            print "use default sensitivity=0.7 specificity=0.1"
            raw_input("Press Enter to continue ")
            
    if opts['standalone']:
        standalone_main(opts)
    elif opts['profile']:
        profile_main(opts)
    else:
        integrated_main(opts)
