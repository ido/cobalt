#!/usr/bin/env python

"""Event Simulator executable."""

import inspect 
import optparse
import os
import sys

import Cobalt.Util
from Cobalt.Components.evsim import EventSimulator
from Cobalt.Components.bqsim import BGQsim
from Cobalt.Components.cqsim import ClusterQsim
from Cobalt.Components.histm import HistoryManager
from Cobalt.Components.base import run_component
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.qsim import Qsimulator
from Cobalt.Proxy import ComponentProxy, local_components
from datetime import datetime
import time

arg_list = ['bgjob', 'cjob', 'config_file', 'outputlog', 'interval', 'predict', 'coscheduling']

def profile_main(opts):
    '''profile integrated qsim'''
    import hotshot, hotshot.stats
    prof = hotshot.Profile("qsim.profile")
    prof.runcall(integrated_main, opts)
    
def integrated_main(options):
    TimingServiceLocator()
    
    if opts.predict:
        histm = HistoryManager(**options)
    
    evsim = EventSimulator(**options)
    if opts.bgjob:
        bqsim = BGQsim(**options)
    if opts.cjob:
        cqsim = ClusterQsim(**options)
    
    starttime_sec = time.time()
    
    while not evsim.is_finished():
        evsim.event_driver()
        os.system('clear')
        if opts.bgjob:
            bqsim.print_screen()
            pass
        if opts.cjob:
            cqsim.print_screen()
            pass
       


    endtime_sec = time.time()
    print "----Simulation is finished, please check output log for further analysis.----"
    print "the simulation lasts %s seconds (~%s minutes)" % (int(endtime_sec - starttime_sec), int((endtime_sec - starttime_sec)/60))
    
if __name__ == "__main__":
    
    p = optparse.OptionParser()

    p.add_option("-b", "--bgjob", dest="bgjob", type="string",
        help="file name of the job trace from the Blue Gene system")
    p.add_option("-c", "--cjob", dest="cjob", type="string",
        help="file name of the job trace from the cluster system")
    p.add_option("-p", "--partition", dest="config_file", type="string",
        help="file name of the partition configuration of the Blue Gene system")
    p.add_option("-o", "--output", dest="outputlog", type="string",
        help="featuring string for output log")
    p.add_option("-j", "--job", dest="bgjob", type="string",
        help="file name of the job trace (when scheduling for bg system only)")
    p.add_option("-i", "--interval", dest="interval", type="int",
        help="seconds to wait at each event")
    p.add_option("-P", "--prediction", dest="predict", action="store_true", default=False,
        help="enable walltime prediction")
    p.add_option("-C", "--coscheduling", dest="coscheduling", type="string", default=False,
        help="[hold | yield] specify the coscheduling scheme: 'hold' or 'yield' resource if mate job can not run")
    
    coscheduling_schemes = ["hold", "yield"]
    
    opts, args = p.parse_args()

    if not opts.bgjob and not opts.cjob:
        print "Error: Please specify at least one job trace!"
        p.print_help()
        sys.exit()
        
    if opts.bgjob and not opts.config_file:
        print "Error: Please specify partition configuration file for the Blue Gene system"
        p.print_help()
        sys.exit()
        
    if opts.coscheduling:
        if not opts.coscheduling in coscheduling_schemes:
            print "Error: invalid coscheduling scheme %s. Valid schemes are: %s" % (opts.coscheduling,  coscheduling_schemes)
            p.print_help()
            sys.exit()
        
    options = {}
    for argname in arg_list:
        options[argname] = getattr(opts, argname)
        
    integrated_main(options)
    #profile_main(options)
